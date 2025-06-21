# MCP UUID Server

A Model Context Protocol (MCP) server for generating UUIDv7 strings.

## Created with vibe-coding using trae.ai

## Features

- Get a single UUIDv7 string.
- Get a batch of UUIDv7 strings.

## Usage

To use this server with an MCP client like Claude Desktop, you can configure it as follows. This example assumes you are running the server directly from its source code.

First, ensure you have Python installed and the necessary dependencies (see Development section).

Then, in your MCP client configuration (e.g., `claude-desktop-settings.json`):

```json
{
  "mcpServers": {
    "uuid_v7_generator": {
      "command": "python",
      "args": ["/path/to/your/mcp-uuid-server/mcp_uuid_server/server.py"],
      // Optional: specify the working directory if needed
      // "cwd": "/path/to/your/mcp-uuid-server/"
    }
  }
}
```

Replace `/path/to/your/mcp-uuid-server/` with the actual path to where you have cloned or placed the server code.

If the server were packaged and published in a way that `uvx` could run it (like some official MCP servers), the configuration might look like this (this is a hypothetical example as this server is not currently published this way):

```json
{
  "mcpServers": {
    "uuid_v7_generator": {
      "command": "uvx",
      "args": ["mcp-uuid-server"]
    }
  }
}
```

### Running the Server Directly

You can run the server directly for development or local use:

```bash
python /path/to/your/mcp-uuid-server/mcp_uuid_server/server.py
```

The server will start and listen for MCP client connections on stdin/stdout.

### Available Tools

1.  **`get_uuidv7`**:
    *   Description: Generates and returns a single UUIDv7 string.
    *   Arguments: None
    *   Returns: A string representing a UUIDv7.

2.  **`get_uuidv7_batch`**:
    *   Description: Generates and returns a list of UUIDv7 strings.
    *   Arguments:
        *   `count` (integer): The number of UUIDv7 strings to generate. Must be a positive integer.
    *   Returns: A list of strings, where each string is a UUIDv7.

## Development

To set up the development environment:

1.  Clone the repository.
2.  It's recommended to create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use .venv\Scripts\activate
    ```
3.  Install the dependencies from `pyproject.toml` (which includes `mcp` and `uuid6`):
    ```bash
    pip install .
    ```
    For editable mode, which is useful during development as changes to the source code are immediately reflected without needing to reinstall:
    ```bash
    pip install -e .
    ```

4.  Run the server directly for testing:
    ```bash
    python mcp_uuid_server/server.py
    ```
