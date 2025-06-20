## Testing Memories

- Always run comprehensive tests before committing code changes
- Implement unit tests, integration tests, and regression tests
- Verify code functionality across different scenarios and edge cases
- Use     pytest and unittest for every task to confirm its complete and working. then once complete add it to the repo
- Lets remove unittest from our testing and ONLY use pytest
- For every task, test and create test files if needed. Before committing to GitHub, delete test files unless you think we should keep them. Add them to a test folder if needed

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
- All commits should be remote github server, never local

## Task Completion and Validation

- When you think you finish a task, do not message until you've run tests to confidently confirm the task is working and have proof
- Wait for user approval before submitting to GitHub
- Create a roadmap.md file to outline project tasks and steps at a high level
- The roadmap should focus on WHAT needs to be done, not HOW (implementation details will be discovered during engineering)
- Incorporate roadmap information into README.md to provide clear project direction