from pathlib import Path
from datetime import datetime

from mcp.server.fastmcp import FastMCP

# ==========================================================
# MCP SERVER
# ==========================================================

mcp = FastMCP("Filesystem MCP")

# ==========================================================
# CONFIGURATION
# ==========================================================

SERVER_NAME = "Filesystem MCP"
SERVER_VERSION = "1.0.0"

WORKSPACE = Path("workspace").resolve()

# Create workspace automatically if it doesn't exist
WORKSPACE.mkdir(exist_ok=True)

# ==========================================================
# UTILITY FUNCTIONS
# ==========================================================

def safe_path(path: str = ".") -> Path:
    """
    Resolve a path safely inside the workspace.
    Prevents path traversal attacks.
    """

    target = (WORKSPACE / path).resolve()

    if not str(target).startswith(str(WORKSPACE)):
        raise ValueError("Access denied: Path is outside the workspace.")

    return target


# ==========================================================
# PHASE 1 - BASIC TOOLS
# ==========================================================

@mcp.tool()
def hello(name: str = "World") -> str:
    """
    Returns a greeting message.
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
    Returns information about the server.
    """

    return {
        "name": SERVER_NAME,
        "version": SERVER_VERSION,
        "status": "running",
        "workspace": str(WORKSPACE),
        "timestamp": datetime.now().isoformat()
    }


# ==========================================================
# PHASE 2 - DIRECTORY TOOLS
# ==========================================================

@mcp.tool()
def list_files(path: str = ".") -> dict:
    """
    List all files in a directory.
    """

    try:

        directory = safe_path(path)

        if not directory.exists():
            return {
                "success": False,
                "message": "Directory does not exist."
            }

        if not directory.is_dir():
            return {
                "success": False,
                "message": "Provided path is not a directory."
            }

        files = sorted(
            file.name
            for file in directory.iterdir()
            if file.is_file()
        )

        return {
            "success": True,
            "path": path,
            "files": files,
            "count": len(files)
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


@mcp.tool()
def list_directories(path: str = ".") -> dict:
    """
    List all directories in a directory.
    """

    try:

        directory = safe_path(path)

        if not directory.exists():
            return {
                "success": False,
                "message": "Directory does not exist."
            }

        if not directory.is_dir():
            return {
                "success": False,
                "message": "Provided path is not a directory."
            }

        directories = sorted(
            folder.name
            for folder in directory.iterdir()
            if folder.is_dir()
        )

        return {
            "success": True,
            "path": path,
            "directories": directories,
            "count": len(directories)
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


# ==========================================================
# PHASE 3 - FILE TOOLS
# ==========================================================

@mcp.tool()
def read_file(path: str) -> dict:
    """
    Read a UTF-8 text file from the workspace.
    """

    try:

        file_path = safe_path(path)

        if not file_path.exists():
            return {
                "success": False,
                "message": "File does not exist."
            }

        if not file_path.is_file():
            return {
                "success": False,
                "message": "Provided path is not a file."
            }

        content = file_path.read_text(encoding="utf-8")

        return {
            "success": True,
            "path": path,
            "content": content,
            "size": file_path.stat().st_size
        }

    except UnicodeDecodeError:

        return {
            "success": False,
            "message": "Binary files are not supported."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":
    mcp.run()