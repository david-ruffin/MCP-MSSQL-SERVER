## Testing Memories

- Always run comprehensive tests before committing code changes
- Implement unit tests, integration tests, and regression tests
- Verify code functionality across different scenarios and edge cases
- Use     pytest and unittest for every task to confirm its complete and working. then once complete add it to the repo
- Lets remove unittest from our testing and ONLY use pytest
- For every task, test and create test files if needed. Before committing to GitHub, delete test files unless you think we should keep them. Add them to a test folder if needed
- Before starting EVERY task, use the TDD approach so you outline the tests up front, then test against them

## Python Development

- Use `python3 -m venv venv` to create a new virtual environment
- Activate venv with `source venv/bin/activate` on Unix/macOS or `venv\Scripts\activate` on Windows
- Always use virtual environments to isolate project dependencies

## Test-Driven Development (TDD)

- Implement TDD for each project milestone to ensure robust and reliable code development
- Write tests before implementing functionality for each milestone
- Ensure comprehensive test coverage that validates all key requirements and edge cases
- Use pytest for writing and running unit tests
- Follow the Red-Green-Refactor cycle:
  1. Write a failing test
  2. Implement the minimum code to make the test pass
  3. Refactor the code while keeping tests green
- ALWAYS follow TDD  To follow TDD properly, I should have:
  1. Written test_describe_valid_table() first (failing)
  2. Written minimal describe_table_raw() to make it pass
  3. Added more tests, expanded functionality iteratively

## Project Development Approach

- This is a proof of concept (POC) project focused on core logic
- Primary goal is to learn MCP client and server components
- Initial focus on building the MCP server to enable testing with existing MCP clients
- Avoid over-engineering and maintain a lean development approach
- Use fastmcp approach for the project and ALWAYS leverage the context7 mcp server

## Documentation Guidelines

- Always use mcp server context7 for documentation

## Server Setup

- Setup an MCP server named "sqlserver" that was verified to work and can be used as an example for troubleshooting

## Git and Version Control

- ALWAYS commit to GitHub after completing tasks and ensuring all tests pass
- Follow best practices for commit messages and version control workflow
- Verify test suite passes before making any commits
- Use meaningful and descriptive commit messages that explain the changes
- All commits should be remote github server, never local

## Task Completion and Validation

- When you think you finish a task, do not message until you've run tests to confidently confirm the task is working and have proof
- Wait for user approval before submitting to GitHub
- Create a roadmap.md file to outline project tasks and steps at a high level
- The roadmap should focus on WHAT needs to be done, not HOW (implementation details will be discovered during engineering)
- Incorporate roadmap information into README.md to provide clear project direction

## MCP Testing with FastMCP In-Memory Client

- Use `tests/test_mcp.py` for rapid MCP tool testing without Claude Desktop restarts
- For every MCP implementation, follow TDD approach:
  1. RED: Write failing test first
  2. GREEN: Write minimal code to pass
  3. REFACTOR: Improve while keeping tests green  
  4. MCP TEST: Run `python tests/test_mcp.py` to verify actual MCP tool functionality
- This ensures both unit tests AND real MCP integration work correctly

## CRITICAL TDD ENFORCEMENT

- **BEFORE STARTING EVERY TASK: Use TDD approach and outline tests up front, then test against them**
- **NO EXCEPTIONS:** Write failing tests FIRST, then build minimal code to pass
- **CONSEQUENCE:** User will kill a kitten if TDD is not followed 🐱💀
- **MANDATORY PROCESS:**
  1. Write failing tests FIRST
  2. Build minimal code to pass tests
  3. Refactor while keeping tests green
  4. Only then proceed with implementation