from pathlib import Path
from app.server import mcp

WORKSPACE = Path("workspace").resolve()


@mcp.tool()
def list_files() -> list[str]:
    """
    List all files and folders inside the workspace.
    """

    return [item.name for item in WORKSPACE.iterdir()]