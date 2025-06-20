#!/usr/bin/env python3
"""
Test the chat interface components
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chat_app import PocketDBAClient

async def test_chat_client():
    """Test the chat client functionality"""
    print("🧪 Testing Pocket DBA Chat Client...\n")
    
    client = PocketDBAClient()
    
    # Test connection
    print("1. Testing connection...")
    result = client.connect_to_server()
    print(f"   {result}\n")
    
    if not client.connected:
        print("❌ Connection failed, cannot continue testing")
        return
    
    # Test simple message processing
    print("2. Testing message processing...")
    try:
        messages, _ = client.process_message("What tables do we have?", [])
        print(f"   Messages returned: {len(messages)}")
        for msg in messages:
            print(f"   - {msg['role']}: {msg['content'][:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ Chat client test completed!")

if __name__ == "__main__":
    asyncio.run(test_chat_client())