from mcp.server.fastmcp import FastMCP
from .uuid_core import get_uuidv7, get_uuidv7_batch
from typing import List
import logging
import sys
import json
import threading
import importlib.metadata

logger = logging.getLogger(__name__)

# Create an MCP server instance
mcp = FastMCP(name="UUIDv7Server", description="Provides UUIDv7 generation tools.")

# --- HTTP Server (FastMCP) Tools ---
@mcp.tool()
def get_uuidv7_http() -> str:
    """
    Generates and returns a single UUIDv7 string via HTTP.
    """
    return get_uuidv7()

@mcp.tool()
def get_uuidv7_batch_http(count: int) -> List[str]:
    """
    Generates and returns a list of UUIDv7 strings via HTTP.
    """
    return get_uuidv7_batch(count)

# --- Логіка STDIO сервера ---
def _handle_stdio_request(request_json: str):
    """
    Handles a single request received via stdio. (Private function)
    """
    response = {"id": None, "result": None, "error": None}
    try:
        request_data = json.loads(request_json)
        method = request_data.get("method")
        params = request_data.get("params", {})
        response["id"] = request_data.get("id")

        if method == "get_uuidv7":
            result = get_uuidv7()
            response["result"] = result
        elif method == "get_uuidv7_batch":
            count = params.get("count")
            if count is None:
                raise ValueError("Missing 'count' parameter for get_uuidv7_batch.")
            result = get_uuidv7_batch(count)
            response["result"] = result
        else:
            raise ValueError(f"Unknown method: '{method}'")

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e} - Request: '{request_json}'", exc_info=True)
        response["error"] = {"code": -32700, "message": "Parse error", "data": str(e)}
    except ValueError as e:
        logger.error(f"Invalid request error: {e}")
        response["error"] = {"code": -32602, "message": "Invalid params", "data": str(e)}
    except Exception as e:
        logger.error(f"Internal server error: {e}", exc_info=True)
        response["error"] = {"code": -32603, "message": "Internal error", "data": str(e)}
    
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()

def _run_stdio_server_loop():
    """
    Main loop for the stdio server, intended to run in a separate thread.
    """
    logger.info("STDIO thread started. Waiting for requests on stdin...")
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            logger.debug(f"STDIO received: {line}")
            _handle_stdio_request(line)
    except Exception as e:
        logger.error(f"Critical error in STDIO thread: {e}", exc_info=True)

def main():
    """
    Starts the UUIDv7 server in both HTTP and STDIO modes simultaneously.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - [%(threadName)s] - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stderr)])

    try:
        version = importlib.metadata.version("mcp-uuid-server")
        logger.info(f"Server version: {version}")
    except importlib.metadata.PackageNotFoundError:
        logger.warning("Could not determine server version.")

    logger.info("Starting server in combined mode (HTTP + STDIO)...")

    # Start the stdio server in a background daemon thread
    stdio_thread = threading.Thread(target=_run_stdio_server_loop, name="STDIO_Thread", daemon=True)
    stdio_thread.start()

    # Start the HTTP server in the main thread
    logger.info("Starting HTTP server...")
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Received stop signal. Shutting down...")
    finally:
        logger.info("Server stopped.")

if __name__ == "__main__":
    main()
