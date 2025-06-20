#!/usr/bin/env python3
"""
Simple MCP test client for pocket-dba server
Uses FastMCP's in-memory testing capability
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import Client
from src.mssql.server import mcp

def test_all_tools():
    """Test all available MCP tools"""
    
    async def run_tests():
        print("🚀 Testing pocket-dba MCP server...\n")
        
        # Connect to server instance directly (in-memory)
        async with Client(mcp) as client:
        
        # List available tools
        print("📋 Available tools:")
        tools = await client.list_tools()
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        print()
        
        # Test execute_sql tool
        print("🔍 Testing execute_sql tool:")
        try:
            result = await client.call_tool("execute_sql", {
                "query": "SELECT COUNT(*) as customer_count FROM SalesLT.Customer"
            })
            print(f"✅ Result: {result[0].text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        print()
        
        # Test describe_table tool
        print("🔍 Testing describe_table tool:")
        try:
            result = await client.call_tool("describe_table", {
                "table_name": "SalesLT.Customer"
            })
            print(f"✅ Customer table structure:")
            lines = result[0].text.split('\n')
            for i, line in enumerate(lines[:6]):  # Show first 5 columns
                print(f"   {line}")
            if len(lines) > 6:
                print(f"   ... and {len(lines) - 6} more columns")
        except Exception as e:
            print(f"❌ Error: {e}")
        print()
        
        # Test get_relationships tool
        print("🔍 Testing get_relationships tool:")
        try:
            result = await client.call_tool("get_relationships", {
                "table_name": "SalesLT.SalesOrderHeader"
            })
            print(f"✅ SalesOrderHeader relationships:")
            lines = result[0].text.split('\n')
            for line in lines[:5]:  # Show first few relationships
                print(f"   {line}")
            if len(lines) > 5:
                print(f"   ... and {len(lines) - 5} more relationships")
        except Exception as e:
            print(f"❌ Error: {e}")
        print()
        
        # Test invalid query (security validation)
        print("🔒 Testing security validation:")
        try:
            result = await client.call_tool("execute_sql", {
                "query": "DROP TABLE SalesLT.Customer"
            })
            print(f"❌ Security failed: {result[0].text}")
        except Exception as e:
            print(f"✅ Security working: Query rejected")
        print()
        
        # Test invalid table name
        print("🔍 Testing invalid table name:")
        try:
            result = await client.call_tool("describe_table", {
                "table_name": "NonExistentTable"
            })
            print(f"✅ Proper error handling: {result[0].text}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n✅ All tests completed!")
    
    asyncio.run(run_tests())

if __name__ == "__main__":
    test_all_tools()