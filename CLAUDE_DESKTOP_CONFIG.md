# Claude Desktop Configuration for FreeCAD MCP Server

This document provides configuration examples for connecting your FreeCAD MCP server to Claude Desktop.

## Prerequisites

1. **FreeCAD Installation**: Ensure FreeCAD is installed and available in your Python environment
2. **Dependencies**: Install required Python packages using `uv sync` or `pip install -e .`
3. **Test Setup**: Run `python test_server.py` to verify your setup

## Configuration Options

### Option 1: Using `uv run` (Recommended)

Add this to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "freecad": {
      "command": "uv",
      "args": ["run", "freecad-mcp-server"],
      "cwd": "/absolute/path/to/your/mcp-server-freecad"
    }
  }
}
```

**Important**: Replace `/absolute/path/to/your/mcp-server-freecad` with the actual absolute path to this directory.

### Option 2: Direct Python Execution

```json
{
  "mcpServers": {
    "freecad": {
      "command": "python",
      "args": ["-m", "freecad_mcp_server"],
      "cwd": "/absolute/path/to/your/mcp-server-freecad"
    }
  }
}
```

### Option 3: Using Absolute Python Path

```json
{
  "mcpServers": {
    "freecad": {
      "command": "/absolute/path/to/python",
      "args": ["main.py"],
      "cwd": "/absolute/path/to/your/mcp-server-freecad"
    }
  }
}
```

## Claude Desktop Configuration File Locations

### macOS
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Windows
```
%APPDATA%\Claude\claude_desktop_config.json
```

### Linux
```
~/.config/claude/claude_desktop_config.json
```

## Troubleshooting

### "spawn uv run ENOENT" Error

This error occurs when:
1. **uv not found**: Install uv using `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. **Wrong working directory**: Ensure `cwd` points to this project directory
3. **Missing entry point**: This should be fixed by the `[project.scripts]` section in `pyproject.toml`

### "FreeCAD modules not available" Warning

1. Install FreeCAD: https://www.freecad.org/downloads.php
2. Ensure FreeCAD Python modules are in your Python path
3. You may need to add FreeCAD's Python directory to your `PYTHONPATH`

### Testing Your Configuration

1. Run the test script: `python test_server.py`
2. Check Claude Desktop logs for connection errors
3. Restart Claude Desktop after configuration changes

## Environment Variables

You may need to set these environment variables:

```bash
# Add FreeCAD Python modules to path
export PYTHONPATH="/Applications/FreeCAD.app/Contents/Resources/lib/python3.11/site-packages:$PYTHONPATH"

# On Linux, FreeCAD may be at:
# export PYTHONPATH="/usr/lib/freecad-python3/lib:$PYTHONPATH"
```

## Example Complete Configuration

```json
{
  "mcpServers": {
    "freecad": {
      "command": "uv",
      "args": ["run", "freecad-mcp-server"],
      "cwd": "/Users/username/projects/mcp-server-freecad",
      "env": {
        "PYTHONPATH": "/Applications/FreeCAD.app/Contents/Resources/lib/python3.11/site-packages"
      }
    }
  }
}
```

## Verification

After configuring, you should see the FreeCAD server listed in Claude Desktop's MCP servers section, and you can use commands like:

- "Create a new FreeCAD document"
- "Add a box with dimensions 10x20x5"
- "List all objects in the document"
- "Export the objects to STL file"