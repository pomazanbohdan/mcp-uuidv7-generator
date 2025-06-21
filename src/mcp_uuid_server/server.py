from mcp.server.fastmcp import FastMCP
import uuid6
from typing import List
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create an MCP server instance
mcp = FastMCP(name="UUIDv7Server", description="Provides UUIDv7 generation tools.")

@mcp.tool()
def get_uuidv7() -> str:
    """
    Generates and returns a single UUIDv7 string.
    """
    uuid_value = str(uuid6.uuid7())
    logger.info(f"Generated UUIDv7: {uuid_value}")
    return uuid_value

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
        logger.error(f"Invalid count parameter: {count}. Must be a positive integer.")
        raise ValueError("Count must be a positive integer.")
    
    logger.info(f"Generating batch of {count} UUIDv7 strings")
    uuids = [str(uuid6.uuid7()) for _ in range(count)]
    logger.info(f"Successfully generated {len(uuids)} UUIDv7 strings")
    return uuids

def main():
    """
    Runs the MCP server.
    This function is referenced in pyproject.toml as the entry point.
    """
    logger.info("Starting UUIDv7 MCP Server...")
    logger.info("Server name: UUIDv7Server")
    logger.info("Available tools:")
    logger.info("  - get_uuidv7: Generate a single UUIDv7")
    logger.info("  - get_uuidv7_batch: Generate multiple UUIDv7s")
    logger.info("Server is ready to accept connections.")
    
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
    finally:
        logger.info("UUIDv7 MCP Server stopped")

if __name__ == "__main__":
    main()
