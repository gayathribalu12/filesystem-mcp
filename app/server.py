from pathlib import Path
from datetime import datetime
import shutil

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
    
@mcp.tool()
def write_file(path: str, content: str) -> dict:
    """
    Create or overwrite a UTF-8 text file inside the workspace.
    """

    try:

        file_path = safe_path(path)

        # Create parent folders if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "message": "File written successfully.",
            "path": path,
            "size": file_path.stat().st_size
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def append_file(path: str, content: str) -> dict:
    """
    Append text to an existing file.
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

        with open(file_path, "a", encoding="utf-8") as file:
            file.write(content)

        return {
            "success": True,
            "message": "Content appended successfully.",
            "path": path,
            "size": file_path.stat().st_size
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }

@mcp.tool()
def create_directory(path: str) -> dict:
    """
    Create a new directory inside the workspace.
    """

    try:
        directory = safe_path(path)

        directory.mkdir(parents=True, exist_ok=True)

        return {
            "success": True,
            "message": "Directory created successfully.",
            "path": path
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def delete_directory(path: str) -> dict:
    """
    Delete an empty directory.
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

        directory.rmdir()

        return {
            "success": True,
            "message": "Directory deleted successfully.",
            "path": path
        }

    except OSError:
        return {
            "success": False,
            "message": "Directory is not empty."
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def delete_file(path: str) -> dict:
    """
    Delete a file from the workspace.
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

        file_path.unlink()

        return {
            "success": True,
            "message": "File deleted successfully.",
            "path": path
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def copy_file(source: str, destination: str) -> dict:
    """
    Copy a file inside the workspace.
    """

    try:

        source_path = safe_path(source)
        destination_path = safe_path(destination)

        if not source_path.exists():
            return {
                "success": False,
                "message": "Source file does not exist."
            }

        if not source_path.is_file():
            return {
                "success": False,
                "message": "Source is not a file."
            }

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source_path, destination_path)

        return {
            "success": True,
            "message": "File copied successfully.",
            "source": source,
            "destination": destination
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def move_file(source: str, destination: str) -> dict:
    """
    Move a file inside the workspace.
    """

    try:

        source_path = safe_path(source)
        destination_path = safe_path(destination)

        if not source_path.exists():
            return {
                "success": False,
                "message": "Source file does not exist."
            }

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(source_path), str(destination_path))

        return {
            "success": True,
            "message": "File moved successfully.",
            "source": source,
            "destination": destination
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def rename_file(path: str, new_name: str) -> dict:
    """
    Rename a file.
    """

    try:

        file_path = safe_path(path)

        if not file_path.exists():
            return {
                "success": False,
                "message": "File does not exist."
            }

        new_path = file_path.with_name(new_name)

        file_path.rename(new_path)

        return {
            "success": True,
            "message": "File renamed successfully.",
            "old_path": path,
            "new_path": str(new_path.relative_to(WORKSPACE))
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }

@mcp.tool()
def search_files(query: str) -> dict:
    """
    Search for files inside the workspace by name.
    """

    try:

        matches = []

        for file in WORKSPACE.rglob("*"):

            if file.is_file() and query.lower() in file.name.lower():

                matches.append(str(file.relative_to(WORKSPACE)))

        return {
            "success": True,
            "query": query,
            "matches": sorted(matches),
            "count": len(matches)
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def tree(path: str = ".") -> dict:
    """
    Display the directory tree.
    """

    try:

        root = safe_path(path)

        if not root.exists():
            return {
                "success": False,
                "message": "Path does not exist."
            }

        tree_output = []

        def build_tree(folder, indent=""):

            entries = sorted(folder.iterdir())

            for index, entry in enumerate(entries):

                connector = "└── " if index == len(entries) - 1 else "├── "

                tree_output.append(
                    indent + connector + entry.name
                )

                if entry.is_dir():

                    extension = "    " if index == len(entries) - 1 else "│   "

                    build_tree(entry, indent + extension)

        tree_output.append(root.name)

        build_tree(root)

        return {
            "success": True,
            "tree": "\n".join(tree_output)
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def metadata(path: str) -> dict:
    """
    Get metadata about a file or directory.
    """

    try:

        item = safe_path(path)

        if not item.exists():
            return {
                "success": False,
                "message": "Path does not exist."
            }

        stat = item.stat()

        return {
            "success": True,
            "name": item.name,
            "path": str(item.relative_to(WORKSPACE)),
            "type": "directory" if item.is_dir() else "file",
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def validate_path(path: str) -> dict:
    """
    Validate whether a path is safe and inside the workspace.
    """

    try:

        resolved = safe_path(path)

        return {
            "success": True,
            "valid": True,
            "path": str(resolved.relative_to(WORKSPACE))
        }

    except Exception as e:

        return {
            "success": False,
            "valid": False,
            "message": str(e)
        }
    
@mcp.tool()
def workspace_info() -> dict:
    """
    Return information about the workspace.
    """

    total_files = sum(1 for p in WORKSPACE.rglob("*") if p.is_file())
    total_directories = sum(1 for p in WORKSPACE.rglob("*") if p.is_dir())

    return {
        "success": True,
        "workspace": str(WORKSPACE),
        "total_files": total_files,
        "total_directories": total_directories
    }

@mcp.tool()
def file_exists(path: str) -> dict:
    """
    Check if a file exists.
    """

    try:

        file_path = safe_path(path)

        return {
            "success": True,
            "exists": file_path.exists(),
            "is_file": file_path.is_file(),
            "is_directory": file_path.is_dir()
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def directory_exists(path: str) -> dict:
    """
    Check if a directory exists.
    """

    try:

        directory = safe_path(path)

        return {
            "success": True,
            "exists": directory.exists(),
            "is_directory": directory.is_dir()
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }

@mcp.tool()
def summarize_file(path: str) -> dict:
    """
    Summarize a text file.
    """

    try:

        file_path = safe_path(path)

        if not file_path.exists():
            return {
                "success": False,
                "message": "File does not exist."
            }

        text = file_path.read_text(encoding="utf-8")

        words = len(text.split())
        lines = len(text.splitlines())
        chars = len(text)

        return {
            "success": True,
            "summary": {
                "lines": lines,
                "words": words,
                "characters": chars,
                "preview": text[:200]
            }
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def directory_summary(path: str = ".") -> dict:
    """
    Generate statistics for a directory.
    """

    try:

        folder = safe_path(path)

        files = 0
        directories = 0
        total_size = 0

        for item in folder.rglob("*"):

            if item.is_file():
                files += 1
                total_size += item.stat().st_size

            elif item.is_dir():
                directories += 1

        return {
            "success": True,
            "path": path,
            "files": files,
            "directories": directories,
            "total_size_bytes": total_size
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def generate_readme() -> dict:
    """
    Generate a simple README for the workspace.
    """

    try:

        files = sum(1 for f in WORKSPACE.rglob("*") if f.is_file())
        folders = sum(1 for f in WORKSPACE.rglob("*") if f.is_dir())

        content = f"""# Workspace Summary

Generated by Filesystem MCP

Files: {files}

Directories: {folders}
"""

        readme = WORKSPACE / "README.md"

        readme.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "message": "README generated successfully.",
            "path": "README.md"
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
    
@mcp.tool()
def explain_file(path: str) -> dict:
    """
    Explain a file using simple statistics.
    """

    try:

        file_path = safe_path(path)

        text = file_path.read_text(encoding="utf-8")

        return {
            "success": True,
            "file": path,
            "explanation": {
                "extension": file_path.suffix,
                "lines": len(text.splitlines()),
                "words": len(text.split()),
                "empty": len(text.strip()) == 0
            }
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