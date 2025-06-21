from mcp.server.fastmcp import FastMCP
import uuid6
from typing import List

# Create an MCP server instance
mcp = FastMCP(name="UUIDv7Server", description="Provides UUIDv7 generation tools.")

@mcp.tool()
def get_uuidv7() -> str:
    """
    Generates and returns a single UUIDv7 string.
    """
    return str(uuid6.uuid7())

@mcp.tool()
def get_uuidv7_batch(count: int) -> List[str]:
    """
    Generates and returns a list of UUIDv7 strings.

    Args:
        count: The number of UUIDv7 strings to generate.
               Must be a positive integer.

    Returns:
        A list of UUIDv7 strings.

    Raises:
        ValueError: If count is not a positive integer.
    """
    if not isinstance(count, int) or count <= 0:
        raise ValueError("Count must be a positive integer.")
    return [str(uuid6.uuid7()) for _ in range(count)]

def main():
    """
    Runs the MCP server.
    This function is referenced in pyproject.toml as the entry point.
    """
    mcp.run()

if __name__ == "__main__":
    main()
