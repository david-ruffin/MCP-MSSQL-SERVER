## Testing Memories

- Always run comprehensive tests before committing code changes
- Implement unit tests, integration tests, and regression tests
- Verify code functionality across different scenarios and edge cases

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