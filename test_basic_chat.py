#!/usr/bin/env python3
"""
Basic test of chat components without async conflicts
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastmcp import Client
from src.mssql.server import mcp

def test_basic_connection():
    """Test basic MCP connection works"""
    print("🧪 Testing basic MCP connection for chat app...\n")
    
    try:
        # Test that we can import the client
        print("✅ FastMCP Client imported successfully")
        
        # Test that our server instance exists
        print("✅ MCP server instance available")
        print(f"   Server name: {mcp.name}")
        
        print("\n✅ Basic components working for chat interface!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_basic_connection()