# Filesystem MCP Server

## Overview

Filesystem MCP Server is a Python-based implementation of the Model Context Protocol (MCP) that provides secure filesystem operations through a standardized set of MCP tools.

The server exposes file management, directory management, search, metadata inspection, workspace utilities, and analysis capabilities while restricting all operations to a sandboxed workspace directory.

This project demonstrates how MCP servers can safely expose local filesystem functionality to MCP-compatible clients such as Claude Desktop, MCP Inspector, and other AI applications.

---

## Features

### Core Server

- Hello Tool
- Ping Tool
- Server Information

### Directory Management

- List Files
- List Directories
- Create Directory
- Delete Directory

### File Management

- Read File
- Write File
- Append File
- Delete File

### File Operations

- Copy File
- Move File
- Rename File

### Search & Inspection

- Search Files
- Directory Tree Visualization
- File & Directory Metadata

### Workspace Security

- Secure Path Validation
- Workspace Information
- File Existence Validation
- Directory Existence Validation

### Workspace Analysis

- File Summary
- Directory Summary
- Automatic README Generation
- File Structure Explanation

---

## Architecture

```
                     MCP Client
                          │
                          │
                 Model Context Protocol
                          │
                          ▼
                Filesystem MCP Server
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
  Directory Tools    File Tools     Search Tools
        │                 │                 │
        └──────────────┬────────────────────┘
                       │
                Security Layer
                  (safe_path)
                       │
                       ▼
              Sandboxed Workspace
```

---

## Project Structure

```
filesystem-mcp/
│
├── app/
│   └── server.py
│
├── workspace/
│   ├── hello.txt
│   ├── notes.txt
│   ├── images/
│   └── projects/
│
├── tests/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12 |
| Protocol | Model Context Protocol (MCP) |
| SDK | MCP Python SDK |
| Filesystem | pathlib |
| File Operations | shutil |
| Development Tool | MCP Inspector |
| Version Control | Git |
| Repository | GitHub |

---

## Installation

Clone the repository

```bash
git clone https://github.com/gayathribalu12/filesystem-mcp.git
```

Navigate into the project

```bash
cd filesystem-mcp
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Server

Start the MCP server using the MCP development command.

```bash
mcp dev app/server.py
```

The MCP Inspector will launch automatically, allowing all registered tools to be tested interactively.

---

## Available Tools

| Category | Tool |
|----------|------|
| Server | hello |
| Server | ping |
| Server | server_info |
| Directory | list_files |
| Directory | list_directories |
| Directory | create_directory |
| Directory | delete_directory |
| File | read_file |
| File | write_file |
| File | append_file |
| File | delete_file |
| Operations | copy_file |
| Operations | move_file |
| Operations | rename_file |
| Search | search_files |
| Search | tree |
| Search | metadata |
| Security | validate_path |
| Security | workspace_info |
| Security | file_exists |
| Security | directory_exists |
| Analysis | summarize_file |
| Analysis | directory_summary |
| Analysis | generate_readme |
| Analysis | explain_file |

---

## Security Model

Every filesystem operation passes through a centralized path validation mechanism.

The server ensures:

- All paths are resolved safely.
- Path traversal attacks are blocked.
- Operations are restricted to the workspace directory.
- Files outside the sandbox cannot be accessed.

Example of blocked access:

```
../../../Windows/System32
```

Response:

```json
{
    "success": false,
    "message": "Access denied: Path is outside the workspace."
}
```

---

## Example Workflow

1. Start the MCP Server.
2. Connect using MCP Inspector.
3. Create directories.
4. Create and write files.
5. Read file contents.
6. Copy and move files.
7. Rename files.
8. Search for files.
9. Display directory tree.
10. Retrieve metadata.
11. Generate workspace summaries.

---

## Learning Outcomes

This project demonstrates practical implementation of:

- Model Context Protocol (MCP)
- Python Filesystem Programming
- Secure Filesystem Design
- Sandboxed File Operations
- Tool Registration using MCP SDK
- Metadata Extraction
- Directory Traversal
- Workspace Analysis
- Git-based Development Workflow

---

## Future Improvements

Possible enhancements include:

- Recursive directory deletion
- File compression and extraction
- File hashing
- Duplicate file detection
- Permission management
- Syntax-aware code summarization
- LLM integration for intelligent file analysis
- Remote filesystem support
- Cloud storage connectors
- REST API wrapper

---

## Repository Statistics

- Language: Python
- Architecture: Single-file MCP Server
- Total MCP Tools: 25
- Security: Sandboxed Workspace
- Protocol: Model Context Protocol (MCP)

---

## Author

Gayathri Balu

GitHub: https://github.com/gayathribalu12
