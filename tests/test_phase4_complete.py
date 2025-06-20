import pytest
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch, AsyncMock
from chat_app import PocketDBAClient

class TestPhase4Complete:
    """Comprehensive tests for Phase 4 chat interface - written FIRST (TDD)"""
    
    def test_test_mode_initialization(self):
        """Test client can initialize in TEST_MODE without API key"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            assert client.test_mode == True
            assert client.anthropic is None
            assert client.connected == False
    
    def test_production_mode_requires_api_key(self):
        """Test production mode requires API key"""
        with patch.dict(os.environ, {'TEST_MODE': 'false'}, clear=True):
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not found"):
                PocketDBAClient()
    
    def test_production_mode_with_api_key(self):
        """Test production mode works with API key"""
        with patch.dict(os.environ, {'TEST_MODE': 'false', 'ANTHROPIC_API_KEY': 'test-key'}):
            client = PocketDBAClient()
            assert client.test_mode == False
            assert client.anthropic is not None
    
    @pytest.mark.asyncio
    async def test_test_mode_handles_table_query(self):
        """Test TEST_MODE handles 'what tables' query correctly"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            client.connected = True
            
            # Mock MCP client
            client.mcp_client = AsyncMock()
            mock_result = Mock()
            mock_result.text = "TABLE_NAME\nCustomer\nProduct\nAddress"
            client.mcp_client.call_tool.return_value = [mock_result]
            
            messages = await client._process_query_test_mode("What tables do we have?")
            
            assert len(messages) == 2
            assert "check what tables" in messages[0]["content"]
            assert "Execute Sql" in messages[1]["content"]
            assert "Customer" in messages[1]["content"]
            client.mcp_client.call_tool.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_test_mode_handles_customer_count_query(self):
        """Test TEST_MODE handles customer count query"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            client.connected = True
            
            client.mcp_client = AsyncMock()
            mock_result = Mock()
            mock_result.text = "customer_count\n847"
            client.mcp_client.call_tool.return_value = [mock_result]
            
            messages = await client._process_query_test_mode("How many customers do we have?")
            
            assert len(messages) == 2
            assert "count the customers" in messages[0]["content"]
            assert "Execute Sql" in messages[1]["content"]
            client.mcp_client.call_tool.assert_called_with("execute_sql", {
                "query": "SELECT COUNT(*) as customer_count FROM SalesLT.Customer"
            })
    
    @pytest.mark.asyncio 
    async def test_test_mode_handles_table_structure_query(self):
        """Test TEST_MODE handles table structure query"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            client.connected = True
            
            client.mcp_client = AsyncMock()
            mock_result = Mock()
            mock_result.text = "COLUMN_NAME,DATA_TYPE,IS_NULLABLE\nCustomerID,int,NO\nFirstName,varchar,NO"
            client.mcp_client.call_tool.return_value = [mock_result]
            
            messages = await client._process_query_test_mode("Show me Customer table structure")
            
            assert len(messages) == 2
            assert "Customer table structure" in messages[0]["content"]
            assert "Describe Table" in messages[1]["content"]
            client.mcp_client.call_tool.assert_called_with("describe_table", {
                "table_name": "SalesLT.Customer"
            })
    
    @pytest.mark.asyncio
    async def test_test_mode_handles_relationships_query(self):
        """Test TEST_MODE handles relationships query"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            client.connected = True
            
            client.mcp_client = AsyncMock()
            mock_result = Mock()
            mock_result.text = "CONSTRAINT_NAME,COLUMN_NAME,REFERENCED_TABLE,REFERENCED_COLUMN\nFK_Order_Customer,CustomerID,Customer,ID"
            client.mcp_client.call_tool.return_value = [mock_result]
            
            messages = await client._process_query_test_mode("Show me relationships")
            
            assert len(messages) == 2
            assert "table relationships" in messages[0]["content"]
            assert "Get Relationships" in messages[1]["content"]
            client.mcp_client.call_tool.assert_called_with("get_relationships", {
                "table_name": "SalesLT.SalesOrderHeader"
            })
    
    @pytest.mark.asyncio
    async def test_test_mode_handles_unknown_query(self):
        """Test TEST_MODE handles unknown/unsupported query"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            client.connected = True
            
            messages = await client._process_query_test_mode("Some random question")
            
            assert len(messages) == 1
            assert "TEST MODE" in messages[0]["content"]
            assert "production" in messages[0]["content"]
    
    def test_process_message_requires_connection(self):
        """Test process_message returns error when not connected"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            client.connected = False
            
            result, textbox = client.process_message("test", [])
            
            assert len(result) == 2
            assert result[1]["role"] == "assistant"
            assert "connect to the database server first" in result[1]["content"]
    
    def test_format_sql_results_with_large_dataset(self):
        """Test SQL results formatting limits to 10 rows"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            
            # Create data with 15 rows
            data_lines = ["col1,col2"] + [f"val{i},data{i}" for i in range(15)]
            data = "\n".join(data_lines)
            
            result = client._format_sql_results(data)
            
            assert "Results (15 rows)" in result
            assert "Showing first 10 of 15 rows" in result
            # Should only show first 10 data rows plus header
            result_lines = result.split('\n')
            table_lines = [line for line in result_lines if line.startswith('|') and '---' not in line]
            assert len(table_lines) == 11  # header + 10 data rows
    
    def test_format_table_description_handles_empty_data(self):
        """Test table description formatting handles edge cases"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            
            # Test with only header
            result = client._format_table_description("COLUMN_NAME,DATA_TYPE")
            assert "No table information found" in result
            
            # Test with error
            result = client._format_table_description("Error: Table not found")
            assert "❌ Error: Table not found" == result
    
    def test_format_relationships_handles_empty_data(self):
        """Test relationships formatting handles edge cases"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            
            # Test with only header
            result = client._format_relationships("CONSTRAINT_NAME,COLUMN_NAME")
            assert "No relationships found" in result
            
            # Test with error
            result = client._format_relationships("Error: Invalid table")
            assert "❌ Error: Invalid table" == result
    
    @pytest.mark.asyncio
    async def test_connection_with_mcp_server(self):
        """Test connection to MCP server works"""
        with patch.dict(os.environ, {'TEST_MODE': 'true'}, clear=True):
            client = PocketDBAClient()
            
            # Mock the MCP client and connection
            with patch('chat_app.Client') as MockClient:
                mock_client_instance = AsyncMock()
                MockClient.return_value = mock_client_instance
                
                # Mock successful connection
                mock_client_instance.__aenter__ = AsyncMock(return_value=mock_client_instance)
                
                # Mock list_tools response  
                mock_tool1 = Mock()
                mock_tool1.name = "execute_sql"
                mock_tool1.description = "Execute SQL"
                mock_tool1.inputSchema = {}
                
                mock_tool2 = Mock()
                mock_tool2.name = "describe_table"
                mock_tool2.description = "Describe table"
                mock_tool2.inputSchema = {}
                
                mock_client_instance.list_tools.return_value = [mock_tool1, mock_tool2]
                
                result = await client._connect_to_server()
                
                assert "Connected to Pocket DBA Server" in result
                assert "execute_sql, describe_table" in result
                assert client.connected == True
                assert len(client.tools) == 2
                assert client.tools[0]["name"] == "execute_sql"