from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Filesystem MCP")

SERVER_NAME = "Filesystem MCP"
SERVER_VERSION = "1.0.0"


@mcp.tool()
def hello(name: str = "World") -> str:
    """
    Returns a greeting.
    """
    return f"Hello, {name}! Welcome to Filesystem MCP."


@mcp.tool()
def ping() -> str:
    """
    Health check.
    """
    return "Pong!"


@mcp.tool()
def server_info() -> dict:
    """
    Returns server information.
    """
    return {
        "name": SERVER_NAME,
        "version": SERVER_VERSION,
        "status": "running",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    mcp.run()