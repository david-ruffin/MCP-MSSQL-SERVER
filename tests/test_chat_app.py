import pytest
import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch, AsyncMock
from chat_app import PocketDBAClient

class TestPocketDBAClient:
    """Test the Pocket DBA chat client"""
    
    @pytest.fixture
    def client(self):
        """Create a client instance with mocked Anthropic"""
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            client = PocketDBAClient()
            return client
    
    def test_client_initialization(self):
        """Test client initializes with API key"""
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            client = PocketDBAClient()
            assert client.connected == False
            assert client.tools == []
            assert client.anthropic is not None
    
    def test_client_requires_api_key(self):
        """Test client raises error without API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not found"):
                PocketDBAClient()
    
    @pytest.mark.asyncio
    async def test_connect_to_server(self, client):
        """Test connecting to MCP server"""
        # Mock the MCP client
        with patch('chat_app.Client') as MockClient:
            mock_client_instance = AsyncMock()
            MockClient.return_value = mock_client_instance
            
            # Mock list_tools response
            mock_tool = Mock()
            mock_tool.name = "execute_sql"
            mock_tool.description = "Execute SQL"
            mock_tool.inputSchema = {}
            mock_client_instance.list_tools.return_value = [mock_tool]
            
            # Test connection
            await client._connect_to_server()
            
            assert client.connected == True
            assert len(client.tools) == 1
            assert client.tools[0]["name"] == "execute_sql"
    
    def test_format_sql_results(self, client):
        """Test SQL result formatting"""
        # Test normal results
        data = "col1,col2,col3\nval1,val2,val3\nval4,val5,val6"
        result = client._format_sql_results(data)
        assert "Results (2 rows)" in result
        assert "| col1 | col2 | col3 |" in result
        assert "| val1 | val2 | val3 |" in result
        
        # Test error
        error_data = "Error: Something went wrong"
        result = client._format_sql_results(error_data)
        assert result == "❌ Error: Something went wrong"
        
        # Test empty results
        empty_data = "col1,col2,col3"
        result = client._format_sql_results(empty_data)
        assert "No results found" in result
    
    def test_format_table_description(self, client):
        """Test table description formatting"""
        data = "COLUMN_NAME,DATA_TYPE,IS_NULLABLE,COLUMN_DEFAULT,MAX_LENGTH\nid,int,NO,,\nname,varchar,YES,,50"
        result = client._format_table_description(data)
        assert "Table Structure:" in result
        assert "| id | int | NO |" in result
        assert "| name | varchar | YES |" in result
    
    def test_format_relationships(self, client):
        """Test relationship formatting"""
        data = "CONSTRAINT_NAME,COLUMN_NAME,REFERENCED_TABLE,REFERENCED_COLUMN\nFK_Order_Customer,CustomerID,Customer,ID"
        result = client._format_relationships(data)
        assert "Foreign Key Relationships:" in result
        assert "| FK_Order_Customer | CustomerID | Customer.ID |" in result
        
        # Test no relationships
        no_rel_data = "CONSTRAINT_NAME,COLUMN_NAME,REFERENCED_TABLE,REFERENCED_COLUMN"
        result = client._format_relationships(no_rel_data)
        assert "No relationships found" in result
    
    @pytest.mark.asyncio
    async def test_process_query(self, client):
        """Test query processing with mocked Anthropic"""
        client.connected = True
        client.tools = [{"name": "execute_sql", "description": "Execute SQL", "input_schema": {}}]
        
        # Mock Anthropic response
        mock_response = Mock()
        mock_content = Mock()
        mock_content.type = 'text'
        mock_content.text = 'I will help you find the tables.'
        mock_response.content = [mock_content]
        
        with patch.object(client.anthropic.messages, 'create', return_value=mock_response):
            with patch.object(client, 'mcp_client') as mock_mcp:
                mock_mcp.call_tool = AsyncMock()
                mock_result = Mock()
                mock_result.text = "TABLE_NAME\nCustomer\nProduct"
                mock_mcp.call_tool.return_value = [mock_result]
                
                messages = await client._process_query("What tables do we have?", [])
                
                assert len(messages) > 0
                assert messages[0]["role"] == "assistant"
                assert "help you find" in messages[0]["content"]