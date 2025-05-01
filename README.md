# Python MSSQL MCP Server

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/david-ruffin/MCP-MSSQL-SERVER)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![MCP](https://img.shields.io/badge/MCP-1.2.0-green.svg)](https://github.com/modelcontextprotocol)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-teal.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

A Model Context Protocol server implementation in Python that provides access to Microsoft SQL Server databases. This server enables Language Models to inspect table schemas and execute SQL queries through a standardized interface.

## Features

### Core Functionality
* Asynchronous operation using Python's `asyncio`
* Environment-based configuration using `python-dotenv`
* Comprehensive logging system
* Connection pooling and management via pyodbc
* Error handling and recovery
* FastAPI integration for API endpoints
* Pydantic models for data validation
* MSSQL connection handling with ODBC Driver

## Prerequisites

* Python 3.x
* Required Python packages:
  * pyodbc
  * pydantic
  * python-dotenv
  * mcp-server
* ODBC Driver 17 for SQL Server

## Installation

```bash
git clone https://github.com/david-ruffin/MCP-MSSQL-SERVER.git
cd MCP-MSSQL-SERVER
pip install -r requirements.txt
```

## Screenshots

![MCP MSSQL Server Demo](screenshots/2025-01-27_05-43-34.png)

The screenshot above demonstrates the server being used with Claude to analyze and visualize SQL data.

## Project Structure

```
PY-MCP-MSSQL/
├── src/
│   └── mssql/
│       ├── __init__.py
│       └── server.py
├── tests/
│   ├── __init__.py
│   ├── test_mssql.py
│   └── test_packages.py
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

### Directory Structure Explanation
* `src/mssql/` - Main source code directory
  * `__init__.py` - Package initialization
  * `server.py` - Main server implementation
* `tests/` - Test files directory
  * `__init__.py` - Test package initialization
  * `test_mssql.py` - MSSQL functionality tests
  * `test_packages.py` - Package dependency tests
* `.env` - Environment configuration file (not in git)
* `.env.example` - Example environment configuration
* `.gitignore` - Git ignore rules
* `README.md` - Project documentation
* `requirements.txt` - Project dependencies

## Configuration

Create a `.env` file in the project root:

```env
MSSQL_SERVER=your_server
MSSQL_DATABASE=your_database
MSSQL_USER=your_username
MSSQL_PASSWORD=your_password
MSSQL_DRIVER={ODBC Driver 17 for SQL Server}
```

## ODBC Driver Setup & Verification

**Important:** This server relies on the Microsoft ODBC Driver for SQL Server (version 17 or 18 recommended) being installed on the system where the server runs.

### 🔍 How to Verify Installation

**macOS / Linux:**

Open your terminal and run:

```bash
odbcinst -q -d
```

Look for output similar to this (the exact version might differ):

```
[ODBC Driver 18 for SQL Server]
```

**Windows (Command Prompt or PowerShell):**

Run this command in PowerShell:

```powershell
Get-OdbcDriver | Where-Object Name -like "*SQL Server*"
```

Alternatively, open the ODBC Data Sources administrator:

1.  Press `Win + R`, type `odbcad32.exe`, and press Enter.
2.  Go to the "Drivers" tab.
3.  Look for "ODBC Driver 17 for SQL Server" or "ODBC Driver 18 for SQL Server".

### 🛠️ Installation if Missing

If the required driver is not installed:

*   **macOS / Linux:** Follow Microsoft's official installation guide:
    [Install the Microsoft ODBC driver for SQL Server (Linux)](https://learn.microsoft.com/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)
*   **Windows:** Download and install the driver from Microsoft:
    [Download ODBC Driver for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
    *Direct link for ODBC Driver 18 (check the page for the latest):* [https://go.microsoft.com/fwlink/?linkid=2221350](https://go.microsoft.com/fwlink/?linkid=2221350)

### 🧪 Test Connection Manually (Optional)

After configuring your `.env` file (see Configuration section above), you can test the connection directly using `pyodbc` from your Python environment (ensure `pyodbc` is installed via `requirements.txt`):

```python
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv() # Load variables from .env

server = os.getenv('MSSQL_SERVER')
database = os.getenv('MSSQL_DATABASE')
username = os.getenv('MSSQL_USER')
password = os.getenv('MSSQL_PASSWORD')
driver = os.getenv('MSSQL_DRIVER') # Make sure this matches your installed driver

if not all([server, database, username, password, driver]):
    print("Error: Ensure MSSQL_SERVER, MSSQL_DATABASE, MSSQL_USER, MSSQL_PASSWORD, and MSSQL_DRIVER are set in your .env file")
else:
    try:
        # Note: TrustServerCertificate=yes might be needed for Azure SQL or certain configs
        # Adjust other parameters like Port if necessary
        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
        )
        print(f"Attempting to connect with:\n{conn_str}\n")
        conn = pyodbc.connect(conn_str)
        print("Connection Successful!")
        conn.close()
        print("Connection Closed.")
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Connection Failed. SQLSTATE: {sqlstate}")
        print(ex)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

```

### ✅ Final `.env` Example

Make sure your `.env` file looks similar to this, replacing the placeholder values with your actual credentials and ensuring the `MSSQL_DRIVER` matches the exact name shown by `odbcinst -q -d` or the ODBC Administrator:

```ini
MSSQL_SERVER=your_server.database.windows.net
MSSQL_DATABASE=your_database_name
MSSQL_USER=your_db_username
MSSQL_PASSWORD=your_secret_password
MSSQL_DRIVER=ODBC Driver 18 for SQL Server
```

## API Implementation Details

### Resource Listing
```python
@app.list_resources()
async def list_resources() -> list[Resource]
```
* Lists all available tables in the database
* Returns table names with URIs in the format `mssql://<table_name>/data`
* Includes table descriptions and MIME types

### Resource Reading
```python
@app.read_resource()
async def read_resource(uri: AnyUrl) -> str
```
* Reads data from specified table
* Accepts URIs in the format `mssql://<table_name>/data`
* Returns first 100 rows in CSV format
* Includes column headers

### SQL Execution
```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]
```
* Executes SQL queries
* Supports both SELECT and modification queries
* Returns results in CSV format for SELECT queries
* Returns affected row count for modification queries

## Usage with MCP Clients (Claude Desktop, Cursor, WindSurf, etc.)

Add this server to your MCP client configuration file. The exact file location depends on the client:

*   **Claude Desktop:**
    *   macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
    *   Windows: `%APPDATA%\Claude\claude_desktop_config.json`
*   **Cursor:** Check Cursor's MCP settings documentation.
*   **WindSurf:** Check WindSurf's MCP settings documentation.

Add an entry for this server under the `mcpServers` key, adjusting paths as needed:

```json
{
  "mcpServers": {
    "MCP-MSSQL": { // You can choose a name for the server
      "command": "<path_to_your_venv>/bin/python",
      "args": [
        "<path_to_project_root>/src/mssql/server.py"
      ],
      "env": {
        "MSSQL_SERVER": "your_server", // See .env configuration
        "MSSQL_DATABASE": "your_database",
        "MSSQL_USER": "your_username", 
        "MSSQL_PASSWORD": "your_password", 
        "MSSQL_DRIVER": "{ODBC Driver 17 for SQL Server}" // Or your installed driver name
      }
    },
    // ... other servers ...
  }
}
```

**Notes:**

*   Replace `<path_to_your_venv>` with the absolute path to the Python interpreter inside your project's virtual environment.
*   Replace `<path_to_project_root>` with the absolute path to the root directory of this project (`MCP-MSSQL-SERVER`).
*   The values in the `env` section should match your `.env` file. Ensure the Python script can access these environment variables or the `.env` file itself when run by the MCP client.
*   The server name (`MCP-MSSQL` in this example) is how you will refer to this server's tools within the client (e.g., `@MCP-MSSQL list_tables`).

## Error Handling

The server implements comprehensive error handling for:
* Database connection failures
* Invalid SQL queries
* Resource access errors
* URI validation
* Tool execution errors

All errors are logged and returned with appropriate error messages.

## Security Features

* Environment variable based configuration
* Connection string security
* Result set size limits
* Input validation through Pydantic
* Proper SQL query handling

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Requirements

Create a `requirements.txt` file with:

```
fastapi>=0.104.1
pydantic>=2.10.6
uvicorn>=0.34.0 
python-dotenv>=1.0.1
pyodbc>=4.0.35
anyio>=4.5.0
mcp==1.2.0
```

These versions have been tested and verified to work together. The key components are:
* `fastapi` and `uvicorn` for the API server
* `pydantic` for data validation
* `pyodbc` for SQL Server connectivity
* `mcp` for Model Context Protocol implementation
* `python-dotenv` for environment configuration
* `anyio` for asynchronous I/O support