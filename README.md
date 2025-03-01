# IOL MCP Tool

A Model Context Protocol (MCP) tool for interacting with Invertir Online (IOL) API through Claude Desktop.

## Prerequisites

- Claude Desktop App for Mac
- Python 3.8+
- IOL trading account
- Environment variables setup with your IOL credentials

## Installation

1. Clone this repository:

```bash
git clone https://github.com/fernandezpablo85/mcpiol.git
cd mcpiol
```

2. Install uv if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install dependencies:

```bash
uv pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your IOL credentials:

```bash
IOL_USER=your_username
IOL_PASS=your_password
```

## Configure Claude Desktop

1. Open Claude Desktop configuration directory:

```bash
open ~/Library/Application\ Support/Claude
```

2. Create or edit `claude_desktop_config.json`:

```bash
touch ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

3. Add the following configuration:

```json
{
  "mcpServers": {
    "iol": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/YOUR_USERNAME/projects/playground/mcpiol",
        "run",
        "main.py"
      ]
    }
  }
}
```

**Important notes:**

- Replace `YOUR_USERNAME` with your actual username
- Both the `command` and `--directory` paths must be absolute paths
- You can find your uv installation path by running `which uv` in the terminal

## Available Tools

The following MCP tools will be available in Claude Desktop:

1. `get_profile_data`: Get your IOL profile information
2. `get_portfolio`: View your current investment portfolio
3. `get_past_week_performance`: Get a stock's performance over the last week
4. `get_operations`: List your trading operations with optional filters
5. `get_operation_details`: Get detailed information about a specific operation

## Usage Examples

In Claude Desktop, you can use these commands:

```
get_profile_data
```

Returns your IOL account profile information.

```
get_portfolio
```

Shows your current investment portfolio.

```
get_past_week_performance --stock_symbol GGAL
```

Shows the last week's performance for GGAL stock.

```
get_operations --start_date 2024-01-01 --end_date 2024-01-31
```

Lists operations between the specified dates.

```
get_operation_details --operation_number 123456
```

Shows detailed information for operation #123456.

## Running Tests

To run the test suite:

```bash
pytest tests/test_client.py -v
```

For coverage report:

```bash
pytest tests/test_client.py --cov=client -v
```

## Troubleshooting

1. If tools don't appear in Claude Desktop:

   - Verify your configuration file is correct
   - Restart Claude Desktop
   - Check Python path and dependencies

2. If authentication fails:
   - Verify your .env file exists and has correct credentials
   - Check IOL API status
   - Ensure your IOL account is active

## License

MIT

## Contributing

Feel free to open issues or submit pull requests.
