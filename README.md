# FreeCAD MCP Server

An MCP server for Claude Desktop that allows you to control FreeCAD using natural language prompts.

## Installation

To install, first download or clone this repo to your computer. Then make sure you have the proper prerequisites installed and working. 

### Prerequisites 

1. **uv Manager** 
   1. See docs for installation methods: https://docs.astral.sh/uv/#installation 
2. **FreeCAD** 
   1. Ensure FreeCAD is installed: 
      1. download: https://www.freecad.org/downloads.php?lang=en 
      2. homebrew: `brew install --cask freecad` 

Next, there are two parts to configure to get everything working: 

1. The MCP server for Claude Desktop 
2. The addon server for the FreeCAD app 

## Setting up the MCP Server 

Before starting Claude Desktop & the FreeCAD app, you'll need to install the Python dependencies for this server. 

Inside of the `/absolute/path/to/your/mcp-server-freecad/` repo that you downloaded, run `uv sync` to install the necessary packages. 

Then, add this to your Claude Desktop configuration file: 

```json
{
  "mcpServers": {
    "freecad": {
      "command": "uv",
      "args": [
        "--directory=/absolute/path/to/your/mcp-server-freecad/",
        "run",
        "mcp-server-freecad"
      ]
    }
  }
}
```

> [!IMPORTANT]
> Replace `/absolute/path/to/your/mcp-server-freecad` with the actual absolute path to this directory. 

### Claude Desktop Configuration File Locations 

```shell
/Users/<YourUsername>/Library/Application Support/Claude/claude_desktop_config.json # macOS 

%APPDATA%\Claude\claude_desktop_config.json # Windows

/Users/<YourUsername>/.config/claude/claude_desktop_config.json # Linux 
```

## Setting up the AddOn Server 

For this step, you'll need to copy the addon folder from this repo into FreeCAD's `Mod` folder. 

````shell
# Copy this 
/absolute/path/to/your/mcp-server-freecad/addon/MCPServerFreeCAD 

# Into here 
/Users/<YourUsername>/Library/Application Support/FreeCAD/Mod # macOS 
- or - 
/Users/<YourUsername>/.local/share/FreeCAD/Mod # Linux 
- or - 
C:\Users\<YourUsername>\AppData\Roaming\FreeCAD\Mod # Windows 
````

Then start up FreeCAD and select "Claude MCP AddOn" as the workbench. 

You should see some menubar buttons (*towards the top*) that allow you to start or stop the addon server. 

Start the addon server and Claude Desktop prompts should now be working! 

## Verification 

After configuring, you should see the FreeCAD server listed in Claude Desktop's MCP servers section, and you can use commands like:

- "Create a new FreeCAD document"
- "Add a box with dimensions 10x20x5"
- "List all objects in the document"
- "Export the objects to STL file"

