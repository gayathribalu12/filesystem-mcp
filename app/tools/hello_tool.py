from app.mcp_instance import mcp

@mcp.tool()
def hello(name: str = "World") -> str:
    return f"Hello, {name}!"