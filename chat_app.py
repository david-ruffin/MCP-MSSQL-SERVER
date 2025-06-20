#!/usr/bin/env python3
"""
Pocket DBA Chat Interface
Business-friendly chat interface for database queries using natural language
"""
import asyncio
import os
import sys
import json
from typing import List, Dict, Any, Union
from contextlib import AsyncExitStack

import gradio as gr
from gradio.components.chatbot import ChatMessage
from fastmcp import Client
from anthropic import Anthropic
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.mssql.server import mcp

# Load environment variables
load_dotenv()

class PocketDBAClient:
    def __init__(self):
        self.mcp_client = None
        self.test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
        
        # Ensure API key is loaded from environment (not needed in test mode)
        if not self.test_mode:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment. Please add it to your .env file.")
            self.anthropic = Anthropic(api_key=api_key)
        else:
            self.anthropic = None  # No API client needed in test mode
            
        self.tools = []
        self.connected = False
        self.exit_stack = None
    
    def connect_to_server(self) -> str:
        """Connect to the pocket-dba MCP server"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self._connect_to_server())
    
    async def _connect_to_server(self) -> str:
        """Async connection to MCP server"""
        try:
            # Connect to our FastMCP server instance directly (in-memory)
            self.mcp_client = Client(mcp)
            await self.mcp_client.__aenter__()
            
            # List available tools
            tools_response = await self.mcp_client.list_tools()
            self.tools = [{
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            } for tool in tools_response]
            
            self.connected = True
            tool_names = [tool["name"] for tool in self.tools]
            return f"✅ Connected to Pocket DBA Server. Available tools: {', '.join(tool_names)}"
            
        except Exception as e:
            self.connected = False
            return f"❌ Connection failed: {str(e)}"
    
    def process_message(self, message: str, history: List[Union[Dict[str, Any], ChatMessage]]) -> tuple:
        """Process user message and return updated chat history"""
        if not self.connected:
            return history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": "❌ Please connect to the database server first using the Connect button."}
            ], gr.Textbox(value="")
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        new_messages = loop.run_until_complete(self._process_query(message, history))
        return history + [{"role": "user", "content": message}] + new_messages, gr.Textbox(value="")
    
    async def _process_query(self, message: str, history: List[Union[Dict[str, Any], ChatMessage]]):
        """Async processing of user query with Claude and MCP tools"""
        try:
            # TEST MODE: Return canned responses without API calls
            if self.test_mode:
                return await self._process_query_test_mode(message)
            
            # Convert history to Claude format
            claude_messages = []
            for msg in history:
                if isinstance(msg, ChatMessage):
                    role, content = msg.role, msg.content
                else:
                    role, content = msg.get("role"), msg.get("content")
                
                if role in ["user", "assistant", "system"]:
                    claude_messages.append({"role": role, "content": content})
            
            # Add current message
            claude_messages.append({"role": "user", "content": message})
            
            # Call Claude with our MCP tools
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=claude_messages,
                tools=self.tools,
                system="""You are a helpful database assistant called "Pocket DBA". You help business owners query their SQL Server database using natural language.

Available tools:
1. execute_sql - Run SELECT queries to get data
2. describe_table - Get table structure and columns  
3. get_relationships - Find foreign key relationships between tables

Guidelines:
- Always be helpful and explain what you're doing
- Use execute_sql for data queries
- Use describe_table to understand table structure before writing complex queries
- Use get_relationships to understand how tables connect
- Format query results in a readable way
- Only run SELECT queries (read-only)
- If you need to understand the database structure, start with describe_table or get_relationships"""
            )

            result_messages = []
            
            # Process Claude's response
            for content in response.content:
                if content.type == 'text':
                    result_messages.append({
                        "role": "assistant", 
                        "content": content.text
                    })
                    
                elif content.type == 'tool_use':
                    tool_name = content.name
                    tool_args = content.input
                    
                    # Execute the MCP tool
                    try:
                        tool_result = await self.mcp_client.call_tool(tool_name, tool_args)
                        result_data = tool_result[0].text if tool_result else "No data returned"
                        
                        # Format the result nicely
                        if tool_name == "execute_sql":
                            formatted_result = self._format_sql_results(result_data)
                        elif tool_name == "describe_table":
                            formatted_result = self._format_table_description(result_data)
                        elif tool_name == "get_relationships":
                            formatted_result = self._format_relationships(result_data)
                        else:
                            formatted_result = result_data
                        
                        result_messages.append({
                            "role": "assistant",
                            "content": f"📊 **{tool_name.replace('_', ' ').title()}**\n\n{formatted_result}"
                        })
                        
                    except Exception as e:
                        result_messages.append({
                            "role": "assistant",
                            "content": f"❌ Error executing {tool_name}: {str(e)}"
                        })
            
            return result_messages
            
        except Exception as e:
            return [{
                "role": "assistant",
                "content": f"❌ Error processing your request: {str(e)}"
            }]
    
    async def _process_query_test_mode(self, message: str):
        """Process queries in test mode with canned responses"""
        message_lower = message.lower()
        
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        # Canned responses for common queries
        if "tables" in message_lower:
            # Simulate execute_sql tool call
            result = await self.mcp_client.call_tool("execute_sql", {
                "query": "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
            })
            formatted = self._format_sql_results(result[0].text if result else "")
            return [
                {"role": "assistant", "content": "I'll check what tables are in your database."},
                {"role": "assistant", "content": f"📊 **Execute Sql**\n\n{formatted}"}
            ]
            
        elif "customer" in message_lower and ("count" in message_lower or "many" in message_lower):
            # Simulate count query
            result = await self.mcp_client.call_tool("execute_sql", {
                "query": "SELECT COUNT(*) as customer_count FROM SalesLT.Customer"
            })
            formatted = self._format_sql_results(result[0].text if result else "")
            return [
                {"role": "assistant", "content": "Let me count the customers for you."},
                {"role": "assistant", "content": f"📊 **Execute Sql**\n\n{formatted}"}
            ]
            
        elif "structure" in message_lower or "describe" in message_lower:
            # Extract table name if mentioned
            if "customer" in message_lower:
                result = await self.mcp_client.call_tool("describe_table", {
                    "table_name": "SalesLT.Customer"
                })
                formatted = self._format_table_description(result[0].text if result else "")
                return [
                    {"role": "assistant", "content": "I'll show you the Customer table structure."},
                    {"role": "assistant", "content": f"📊 **Describe Table**\n\n{formatted}"}
                ]
            
        elif "relationship" in message_lower:
            # Default relationships query
            result = await self.mcp_client.call_tool("get_relationships", {
                "table_name": "SalesLT.SalesOrderHeader"
            })
            formatted = self._format_relationships(result[0].text if result else "")
            return [
                {"role": "assistant", "content": "I'll show you the table relationships."},
                {"role": "assistant", "content": f"📊 **Get Relationships**\n\n{formatted}"}
            ]
        
        # Default response
        return [{
            "role": "assistant",
            "content": "TEST MODE: I understand your question. In production, I would use Claude to generate the appropriate SQL query and return results."
        }]
    
    def _format_sql_results(self, data: str) -> str:
        """Format SQL query results for display"""
        if data.startswith("Error:"):
            return f"❌ {data}"
        
        lines = data.strip().split('\n')
        if len(lines) <= 1:
            return "No results found."
        
        # Create a simple table format
        header = lines[0].split(',')
        rows = [line.split(',') for line in lines[1:]]
        
        result = f"**Results ({len(rows)} rows):**\n\n"
        result += "| " + " | ".join(header) + " |\n"
        result += "|" + "|".join([" --- " for _ in header]) + "|\n"
        
        for row in rows[:10]:  # Limit to first 10 rows for display
            result += "| " + " | ".join(row) + " |\n"
        
        if len(rows) > 10:
            result += f"\n*Showing first 10 of {len(rows)} rows*"
        
        return result
    
    def _format_table_description(self, data: str) -> str:
        """Format table description for display"""
        if data.startswith("Error:"):
            return f"❌ {data}"
        
        lines = data.strip().split('\n')
        if len(lines) <= 1:
            return "No table information found."
        
        result = "**Table Structure:**\n\n"
        result += "| Column | Type | Nullable | Default | Max Length |\n"
        result += "|--------|------|----------|---------|------------|\n"
        
        for line in lines[1:]:  # Skip header
            parts = line.split(',')
            if len(parts) >= 5:
                col_name, data_type, nullable, default, max_len = parts[:5]
                result += f"| {col_name} | {data_type} | {nullable} | {default or 'None'} | {max_len or 'N/A'} |\n"
        
        return result
    
    def _format_relationships(self, data: str) -> str:
        """Format relationship data for display"""
        if data.startswith("Error:"):
            return f"❌ {data}"
        
        lines = data.strip().split('\n')
        if len(lines) <= 1:
            return "No relationships found for this table."
        
        result = "**Foreign Key Relationships:**\n\n"
        result += "| Constraint | Column | References |\n"
        result += "|------------|--------|------------|\n"
        
        for line in lines[1:]:  # Skip header
            parts = line.split(',')
            if len(parts) >= 4:
                constraint, column, ref_table, ref_column = parts[:4]
                result += f"| {constraint} | {column} | {ref_table}.{ref_column} |\n"
        
        return result

# Initialize the client
client = PocketDBAClient()

def create_interface():
    """Create the Gradio interface"""
    with gr.Blocks(title="Pocket DBA - Database Assistant", theme=gr.themes.Soft()) as demo:
        gr.Markdown("""
        # 🗃️ Pocket DBA - Your Database Assistant
        
        Ask questions about your database in plain English. I'll help you find the data you need!
        """)
        
        with gr.Row():
            connect_btn = gr.Button("🔌 Connect to Database", variant="primary")
            status = gr.Textbox(
                label="Connection Status", 
                value="Click 'Connect to Database' to start",
                interactive=False,
                container=False
            )
        
        chatbot = gr.Chatbot(
            value=[], 
            height=500,
            type="messages",
            show_copy_button=True,
            avatar_images=("👤", "🤖"),
            bubble_full_width=False
        )
        
        with gr.Row():
            msg = gr.Textbox(
                label="Ask about your database",
                placeholder="e.g., 'Show me our top 10 customers' or 'What tables do we have?'",
                scale=4,
                container=False
            )
            clear_btn = gr.Button("🗑️ Clear Chat", scale=1)
        
        gr.Markdown("""
        ### Example Questions:
        - "What tables do we have?"
        - "Show me the structure of the Customer table"
        - "How many customers do we have?"
        - "What are our top selling products?"
        - "Show me recent orders"
        """)
        
        # Event handlers
        connect_btn.click(
            client.connect_to_server, 
            outputs=status
        )
        
        msg.submit(
            client.process_message, 
            [msg, chatbot], 
            [chatbot, msg]
        )
        
        clear_btn.click(
            lambda: [], 
            None, 
            chatbot
        )
        
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )