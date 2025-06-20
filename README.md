# Pocket DBA MCP Server - "DBA in Your Pocket"

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/david-ruffin/pocket-dba-mcp-server)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.8.1-green.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## Project Vision

Transform how business owners interact with their data by creating a conversational interface that replaces the traditional static BI workflow. Instead of requesting reports from DBAs and waiting for Power Platform visualizations, business owners can have real-time conversations with their database and get instant insights.

**Current State:** Business owner → Question → DBA → SQL Query → Power Platform → Static Report → Limited Follow-up

**Target State:** Business owner → Conversational AI → Dynamic Query → Instant Insights → Unlimited Follow-up

## Current Implementation Status

✅ **Phase 1 Complete**: Core MCP Server with FastMCP
- FastMCP server implementation with stdio transport
- Read-only SQL Server access with security validation  
- Basic tools: `execute_sql` with query validation
- Resources: `list_tables` and `get_table_data`
- Comprehensive test suite (9 tests passing)
- Proven integration with Claude Desktop

## Features

### Current Capabilities
- **Read-Only Database Access**: Complete visibility into SQL Server database with zero write permissions
- **Security-First Design**: Advanced SQL injection prevention and query validation
- **FastMCP Implementation**: Simplified syntax with decorators for rapid development
- **Schema Discovery**: List all database tables and their structure
- **Query Execution**: Execute validated SELECT statements safely
- **Error Handling**: Graceful handling of malformed queries and connection issues

### Architecture
```
Business Owner → Claude Desktop → FastMCP Client → pocket-dba-mcp-server → SQL Server
```

## Installation & Setup

### Prerequisites
- Python 3.12+
- Microsoft ODBC Driver 18 for SQL Server
- SQL Server database access

### Quick Start
```bash
git clone https://github.com/david-ruffin/pocket-dba-mcp-server.git
cd pocket-dba-mcp-server
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration
Create a `.env` file:
```env
MSSQL_SERVER=your_server
MSSQL_DATABASE=your_database  
MSSQL_USER=your_username
MSSQL_PASSWORD=your_password
MSSQL_DRIVER={ODBC Driver 18 for SQL Server}
```

### Claude Desktop Integration
Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "pocket-dba": {
      "command": "/path/to/pocket-dba-mcp-server/venv/bin/python",
      "args": ["/path/to/pocket-dba-mcp-server/src/mssql/server.py"],
      "env": {
        "MSSQL_SERVER": "your_server",
        "MSSQL_DATABASE": "your_database",
        "MSSQL_USER": "your_username", 
        "MSSQL_PASSWORD": "your_password",
        "MSSQL_DRIVER": "{ODBC Driver 18 for SQL Server}"
      }
    }
  }
}
```

## Project Structure
```
pocket-dba-mcp-server/
├── src/mssql/
│   ├── server.py          # FastMCP server implementation
│   └── server_old.py      # Legacy standard MCP version
├── tests/
│   └── test_server.py     # Comprehensive test suite
├── screenshots/           # Project demonstrations
├── .env                   # Database configuration (create from template)
├── .env.example          # Configuration template
├── CLAUDE.md             # Project development instructions
├── requirements.txt      # Python dependencies
├── roadmap.md           # Detailed project requirements
└── README.md           # This file
```

## Current Tools & Resources

### Tools
- **`execute_sql`**: Execute read-only SELECT queries with validation

### Resources  
- **`mssql://tables`**: List all database tables
- **`mssql://table/{table_name}`**: Get table data (top 100 rows)

## Development Roadmap

### Phase 1: Core Server ✅ COMPLETE
- [x] Set up Python 3.12 virtual environment
- [x] Implement FastMCP server with stdio transport  
- [x] Create execute_sql tool with security validation
- [x] Add table listing and data resources
- [x] Comprehensive test suite
- [x] Claude Desktop integration verified

### Phase 2: Enhanced Database Discovery
- [ ] Implement `describe_table` tool for schema inspection
- [ ] Add `get_relationships` tool for foreign key discovery
- [ ] Create table metadata resources (columns, types, constraints)
- [ ] Add index information for query optimization
- [ ] Implement connection pooling for efficiency

### Phase 3: Advanced Query Capabilities  
- [ ] Add query complexity analysis and timeout limits
- [ ] Implement result set size limits for performance
- [ ] Create audit trail logging for compliance
- [ ] Add query optimization suggestions
- [ ] Support for WITH clauses and CTEs

### Phase 4: Client Interface Development
- [ ] Build Gradio chat interface
- [ ] Implement MCP client with message routing
- [ ] Create session manager for conversation context
- [ ] Add result renderer for data visualization
- [ ] Test end-to-end conversation flow

### Phase 5: Business Intelligence Features
- [ ] Multi-table analysis capabilities
- [ ] Time series analysis and trend identification
- [ ] Cohort analysis for customer behavior tracking
- [ ] Data segmentation and pattern discovery
- [ ] Basic forecasting based on historical data

### Phase 6: Production Readiness
- [ ] Performance optimization and monitoring
- [ ] Enhanced error handling and recovery
- [ ] Data export capabilities  
- [ ] Integration with existing BI tools
- [ ] Multi-database support

## Business Use Cases

### Primary Scenarios
1. **Exploratory Analysis**: "Show me sales trends over the last 6 months"
2. **Correlation Discovery**: "Find me interesting patterns in customer behavior"  
3. **Ad-hoc Reporting**: "Compare performance across regions"
4. **Data Validation**: "Are there any data quality issues I should know about?"
5. **Strategic Insights**: "What factors most influence customer retention?"

### Advanced Capabilities (Future)
- **Multi-table Analysis**: Claude automatically joins related tables
- **Time Series Analysis**: Identify trends, seasonality, and anomalies
- **Segmentation**: Identify distinct customer or product groups
- **Forecasting**: Predictive insights based on historical data

## Security & Safety

### Data Protection
- **Read-Only Access**: No INSERT, UPDATE, DELETE, or DDL operations
- **Query Validation**: Server validates all queries before execution  
- **SQL Injection Prevention**: Advanced pattern detection and blocking
- **Connection Security**: Secure credential management
- **Error Handling**: Graceful handling without data exposure

### Access Control
- **Authentication**: Database credentials managed securely
- **Authorization**: Respects existing database permissions
- **Audit Trail**: Logs all queries for compliance and monitoring

## Testing

Run the comprehensive test suite:
```bash
source venv/bin/activate
python -m pytest tests/ -v
```

Current test coverage:
- Database connection validation
- Query security validation (9 different attack patterns)
- SQL execution with valid/invalid queries
- Resource listing and data retrieval
- Error handling for malformed requests

## Performance Considerations

### Current Limitations
- Query timeout: 30 seconds default
- Result set: Top 100 rows for table data
- Read-only operations only
- Single connection per request

### Planned Optimizations
- Connection pooling for efficiency
- Query complexity analysis  
- Resource usage monitoring
- Caching for frequently accessed metadata

## User Experience Goals

### For Business Owners
- **Immediacy**: Get answers in seconds, not days
- **Accessibility**: No SQL knowledge required
- **Conversational**: Natural follow-up questions
- **Comprehensive**: Access to all business data
- **Insightful**: AI suggests relevant analysis

### For Technical Teams  
- **Security**: No risk to production data
- **Compliance**: Full audit trail of data access
- **Performance**: Optimized queries that don't impact operations
- **Maintainability**: Simple, clean codebase

## Expected Outcome

A proof-of-concept that demonstrates how conversational AI can democratize data access, enabling business owners to explore their data independently while maintaining security and accuracy. The system should feel like having a senior data analyst available 24/7 for any business question.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`python -m pytest tests/ -v`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Dependencies

```
fastmcp>=2.8.1
pyodbc>=4.0.35
python-dotenv>=1.0.1
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*"Democratizing data access through conversational AI"*