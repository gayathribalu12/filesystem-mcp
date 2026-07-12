from pathlib import Path

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Workspace directory (sandbox)
WORKSPACE_DIR = BASE_DIR / "workspace"

# Server Configuration
SERVER_NAME = "Filesystem MCP"
SERVER_VERSION = "1.0.0"

# Allowed workspace
ALLOWED_ROOT = WORKSPACE_DIR.resolve()