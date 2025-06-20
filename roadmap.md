# SQL Server MCP - "DBA in Your Pocket" Project Requirements Document

## Project Vision
Transform how business owners interact with their data by creating a conversational interface that replaces the traditional static BI workflow. Instead of requesting reports from DBAs and waiting for Power Platform visualizations, business owners can have real-time conversations with their database and get instant insights.

## Problem Statement
**Current State:** Business owner → Question → DBA → SQL Query → Power Platform → Static Report → Limited Follow-up
**Target State:** Business owner → Conversational AI → Dynamic Query → Instant Insights → Unlimited Follow-up

## Core Requirements

### Functional Requirements
- **Read-Only Database Access**: Complete visibility into SQL Server database with zero write permissions
- **Natural Language Queries**: Business owners can ask any question about their data in plain English
- **Dynamic Visualizations**: Claude can create charts, graphs, and reports on-the-fly
- **Correlation Discovery**: AI can suggest and find hidden patterns in the data
- **Conversational Flow**: Maintains context across multiple questions and follow-ups

### Technical Architecture

#### MCP Server (Python 3.12)
**Core Components:**
- **Database Connection Manager**: SQL Server connection via pyodbc
- **stdio Transport**: Communication with Claude via JSON-RPC
- **Tool Implementations**: Four essential database tools

**Required Tools:**
1. **`list_tables`**: Discover all tables in the database
2. **`describe_table`**: Show table structure (columns, types, constraints)
3. **`get_relationships`**: Show foreign keys and table relationships
4. **`execute_query`**: Run read-only SELECT statements with validation

**Database Discovery Features:**
- Complete schema introspection
- Relationship mapping between tables
- Column metadata (data types, nullability, constraints)
- Index information for query optimization suggestions

#### MCP Client (Gradio Framework)
**Components:**
- **Chat Interface**: Streamlined conversation UI
- **Message Router**: Handles communication between user, Claude, and MCP server
- **Session Manager**: Maintains conversation context
- **Result Renderer**: Displays data tables, charts, and visualizations

#### Integration Layer
**Claude Integration:**
- Uses Claude's built-in SQL knowledge for query generation
- Leverages Claude's analytical capabilities for trend identification
- Utilizes Claude's visualization skills for chart creation

### Business Use Cases

#### Primary Scenarios
1. **Exploratory Analysis**: "Show me sales trends over the last 6 months"
2. **Correlation Discovery**: "Find me interesting patterns in customer behavior"
3. **Ad-hoc Reporting**: "Compare performance across regions"
4. **Data Validation**: "Are there any data quality issues I should know about?"
5. **Strategic Insights**: "What factors most influence customer retention?"

#### Advanced Capabilities
- **Multi-table Analysis**: Claude can automatically join related tables
- **Time Series Analysis**: Identify trends, seasonality, and anomalies
- **Cohort Analysis**: Track customer behavior over time
- **Segmentation**: Identify distinct customer or product groups
- **Forecasting**: Basic predictive insights based on historical data

### Security & Safety

#### Data Protection
- **Read-Only Access**: No INSERT, UPDATE, DELETE, or DDL operations
- **Query Validation**: Server validates all queries before execution
- **Connection Security**: Secure connection strings and credential management
- **Error Handling**: Graceful handling of malformed queries

#### Access Control
- **Authentication**: Database credentials managed securely
- **Authorization**: Respect existing database permissions
- **Audit Trail**: Log all queries for compliance and monitoring

### Technical Implementation

#### Development Environment
- **Python Version**: 3.12.x
- **Virtual Environment**: Standard venv (avoid overengineering)
- **Key Dependencies**:
  - `mcp` - Official MCP Python SDK
  - `pyodbc` - SQL Server connectivity
  - `gradio` - Chat interface
  - `pandas` - Data manipulation (if needed)
  - `sqlparse` - Query validation

#### Deployment Architecture
```
Business Owner → Gradio Chat UI → Claude (LLM) → MCP Client → MCP Server → SQL Server
```

#### Data Flow
1. User asks question in natural language
2. Claude converts to appropriate SQL query
3. MCP client sends query request to server
4. Server validates and executes query
5. Results returned to Claude for analysis/visualization
6. Claude presents insights back to user

### Success Criteria

#### Minimum Viable Product
- [ ] Connect to SQL Server database
- [ ] Discover complete database schema
- [ ] Execute read-only queries safely
- [ ] Maintain conversational context
- [ ] Generate basic visualizations

#### Advanced Features (Future)
- [ ] Query optimization suggestions
- [ ] Data export capabilities
- [ ] Scheduled insight reports
- [ ] Integration with existing BI tools
- [ ] Multi-database support

### User Experience Goals

#### For Business Owners
- **Immediacy**: Get answers in seconds, not days
- **Accessibility**: No SQL knowledge required
- **Conversational**: Natural follow-up questions
- **Comprehensive**: Access to all business data
- **Insightful**: AI suggests relevant analysis

#### For Technical Teams
- **Security**: No risk to production data
- **Compliance**: Full audit trail of data access
- **Performance**: Optimized queries that don't impact operations
- **Maintainability**: Simple, clean codebase

### Development Phases

#### Phase 1: Core Server (Week 1)
- Set up Python 3.12 virtual environment
- Implement basic MCP server with stdio transport
- Create three core tools (list_tables, describe_table, execute_query)
- Test with Claude Desktop

#### Phase 2: Client Interface (Week 2)
- Build Gradio chat interface
- Implement MCP client with message routing
- Test end-to-end conversation flow

#### Phase 3: Enhancement (Week 3)
- Add relationship discovery tool
- Improve error handling and validation
- Performance optimization
- User experience refinements

### Technical Constraints

#### Performance
- Query timeout limits to prevent long-running operations
- Result set size limits to maintain responsiveness
- Connection pooling for efficiency

#### Compatibility
- SQL Server 2016+ compatibility
- Python 3.12+ for modern language features
- Cross-platform support (macOS, Linux, Windows)

### Risk Mitigation

#### Data Security
- No data persistence in MCP components
- Query logging without storing results
- Secure credential management

#### Performance Impact
- Read-only operations only
- Query complexity analysis
- Resource usage monitoring

#### User Safety
- Clear indication of data limitations
- Guidance on interpretation of AI-generated insights
- Emphasis on human judgment for business decisions

---

## Expected Outcome
A proof-of-concept that demonstrates how conversational AI can democratize data access, enabling business owners to explore their data independently while maintaining security and accuracy. The system should feel like having a senior data analyst available 24/7 for any business question.