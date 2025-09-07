# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides Claude Desktop with tools to control FreeCAD through natural language. The server exposes FreeCAD's CAD modeling capabilities as MCP tools, allowing users to create 3D models, perform boolean operations, and export designs.

## Development Commands

### Package Management
- `uv sync` - Install dependencies and sync the virtual environment
- `uv add <package>` - Add a new dependency
- `uv run <command>` - Run commands in the project's virtual environment

### Running the Server
- `uv run mcp-server-freecad` - Start the MCP server (primary entry point)
- `python main.py` - Alternative way to start the server
- `python test_server.py` - Test the server setup and verify FreeCAD integration

### Testing and Validation
- `python test_server.py` - Comprehensive test suite that verifies:
  - Module imports work correctly
  - Server instance can be created
  - Entry points are configured properly
  - FreeCAD integration is functional

## Architecture

### Core Components

**MCPServerFreeCAD** (`src/mcp_server_freecad/server.py:34`): Main server class that:
- Initializes the FastMCP server
- Sets up all FreeCAD tool handlers
- Manages FreeCAD document state
- Handles graceful degradation when FreeCAD is unavailable

**Tool System**: Each FreeCAD operation is exposed as an MCP tool:
- Geometric primitives: `create_box`, `create_cylinder`, `create_sphere`
- Document management: `create_document`, `save_document`, `list_objects`
- Operations: `boolean_operation`, `move_object`, `rotate_object`
- Export: `export_stl`
- Advanced features: `create_sketch`, `create_pad`, `create_pocket` (partially implemented)

### FreeCAD Integration

The server imports FreeCAD modules with graceful fallback:
- Primary modules: `FreeCAD`, `Part`, `Draft`, `PartDesign`, `Sketcher`, `FreeCADGui`
- Mock objects are created when FreeCAD is unavailable to prevent crashes
- Operations check `FREECAD_AVAILABLE` flag before executing

### State Management

- `self.doc`: Current FreeCAD document instance
- `self.active_body`: Currently active PartDesign body (for advanced operations)
- Documents are auto-created when needed for primitive operations

## FreeCAD Requirements

FreeCAD must be installed and its Python modules available in the Python path. The server logs warnings when FreeCAD is unavailable but continues to run for testing purposes.

### Common Setup Issues and Solutions

**Issue: `ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'`**

This occurs when FreeCAD's Python version doesn't match your current Python environment. FreeCAD typically bundles its own Python interpreter.

**Solutions:**

1. **Install FreeCAD with matching Python version** (Recommended)
   ```bash
   # Install FreeCAD via conda/mamba with Python 3.13
   mamba install freecad -c conda-forge
   ```

2. **Use system Python that matches FreeCAD**
   - Check FreeCAD's Python version: typically Python 3.11
   - Switch to matching Python version using pyenv/conda
   - Install the MCP server in that environment

3. **Alternative: Run without FreeCAD for development**
   ```bash
   # The server will run in mock mode for testing MCP integration
   uv run mcp-server-freecad
   ```

**macOS Specific Issues:**
- FreeCAD.app bundles Python 3.11 but your system may use Python 3.13
- The bundled Python cannot be easily extended with additional packages
- Consider using Homebrew or conda-forge FreeCAD installations instead

**Other Common Issues:**
- FreeCAD Python modules not in PYTHONPATH
- Version compatibility between FreeCAD and Python
- Missing FreeCAD installation
- Permission issues with system-wide FreeCAD installations

## Entry Points

The project uses multiple entry point configurations:
- `pyproject.toml` defines `mcp-server-freecad = "main:main"`
- `__main__.py` provides module execution support
- `main.py` contains the primary entry function

## Development Notes

### Adding New Tools
1. Create async method in `MCPServerFreeCAD` class (prefixed with `_`)
2. Add corresponding `@self.server.tool()` decorator in `setup_tools()`
3. Add reference to `self._registered_tools` list
4. Update `handle_tool_call()` method for the new tool

### FreeCAD Operation Patterns
- Check document exists, create if needed
- Use FreeCAD API to create/modify objects
- Call `self.doc.recompute()` after changes
- Return descriptive success messages
- Handle object name generation with fallbacks

## Claude Desktop Integration

Configure Claude Desktop with:
```json
{
  "mcpServers": {
    "freecad": {
      "command": "uv",
      "args": ["run", "mcp-server-freecad"],
      "cwd": "/absolute/path/to/mcp-server-freecad"
    }
  }
}
```

See `CLAUDE_DESKTOP_CONFIG.md` for detailed configuration options and troubleshooting.