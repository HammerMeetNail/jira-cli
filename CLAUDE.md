# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Installation
```bash
# Always use development mode installation
pip install -e .

### Development Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

### Configuration
Before using the CLI, configure your Jira credentials:
```bash
jira-cli configure
```

Or set environment variables:
```bash
export JIRA_DOMAIN="mycompany.atlassian.net"  # Just domain, NO https:// prefix
export JIRA_API_TOKEN="your_api_token"
export JIRA_API_VERSION="2"  # Optional, defaults to 2
```

**IMPORTANT**: `JIRA_DOMAIN` should be just the domain name without `https://` prefix.

### Bulk Issue Creation
Use the `create_issues_from_md.py` script for creating multiple issues:
```bash
# Dry run to preview
./create_issues_from_md.py bulk_test_jira_data.md --project MYPROJ --dry-run

# With label
./create_issues_from_md.py bulk_test_jira_data.md --project MYPROJ --label "incident-response" --dry-run

# Generate shell script
./create_issues_from_md.py bulk_test_jira_data.md --project MYPROJ --save-script create.sh --dry-run
```

### Testing
Currently, test files exist but are empty. When implementing tests:
- Use the existing test structure in `jira_cli/tests/`
- Test files: `test_commands.py` and `test_utils.py`

## Architecture

This is a Click-based CLI application for interacting with Jira's REST API.

### Core Structure
- **Entry Point**: `jira_cli/cli.py` - Main CLI group with verbose logging support
- **Commands**: `jira_cli/commands/` - Each command is a separate module
- **Utilities**: `jira_cli/utils/` - Shared functionality

### Key Components

1. **API Client** (`utils/api.py`):
   - Central `make_request()` function handles all API communication
   - Automatic authentication header injection
   - Request/response logging when verbose mode is enabled
   - Error handling with detailed logging

2. **Configuration** (`utils/config.py`):
   - Config stored in `~/.jira_cli_config`
   - Environment variables take precedence
   - Required: `JIRA_DOMAIN`, `JIRA_API_TOKEN`
   - Optional: `JIRA_API_VERSION` (defaults to 2)

3. **Logging** (`utils/logging.py`):
   - Logger singleton with verbose mode support
   - Logs API requests/responses when `--verbose` flag is used
   - Structured logging for debugging

4. **Commands**:
   - `create` - Create new issues
   - `get` - Retrieve issue details  
   - `update` - Modify issues
   - `delete` - Remove issues
   - `comment` - Manage comments
   - `attachment` - Handle attachments
   - `transition` - Move issues through workflow states
   - `search` - Query issues with JQL
   - `watch` - Manage issue watchers
   - `dashboard` - View recent activity
   - `configure` - Interactive setup

### API Integration Pattern
All commands follow this pattern:
1. Parse CLI arguments
2. Get configuration via `get_config()`
3. Call `make_request()` with appropriate endpoint
4. Handle response/errors
5. Format output for CLI

### Adding New Features
1. Create new command module in `jira_cli/commands/`
2. Use `@click.command()` decorator
3. Import and add to main CLI group in `cli.py`
4. Use `make_request()` for API calls
5. Follow existing error handling patterns

## Important Notes

### Domain Configuration Issue
- The most common setup issue is including `https://` in `JIRA_DOMAIN`
- Always use just the domain: `mycompany.atlassian.net` not `https://mycompany.atlassian.net`
- The code automatically adds the `https://` prefix

### Available Scripts
- `create_issues_from_md.py` - Bulk issue creation from markdown files
- `bulk_test_jira_data.md` - Example markdown file with test issues

### Installation Requirements
- Always use virtual environment: `python -m venv venv && source venv/bin/activate`
- Always use development mode: `pip install -e .`