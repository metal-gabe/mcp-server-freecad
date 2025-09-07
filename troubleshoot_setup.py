#!/usr/bin/env python3
"""
Comprehensive troubleshooting script for MCP FreeCAD server setup.
This script diagnoses common issues and provides solutions.
"""
import sys
import os
import subprocess
from pathlib import Path

def check_uv_installation():
    """Check if uv is properly installed."""
    print("=== Checking uv installation ===")
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ uv is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ uv is not working properly")
            return False
    except FileNotFoundError:
        print("❌ uv is not installed or not in PATH")
        return False

def check_entry_point():
    """Check if the mcp-server-freecad entry point works."""
    print("\n=== Checking entry point ===")
    try:
        # Test with a quick timeout to avoid hanging
        result = subprocess.run(['uv', 'run', 'mcp-server-freecad', '--help'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Entry point works")
            return True
        else:
            print(f"❌ Entry point failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✅ Entry point starts (timed out waiting for help)")
        return True
    except FileNotFoundError:
        print("❌ Entry point not found")
        return False

def check_freecad_installation():
    """Check FreeCAD installation and Python module availability."""
    print("\n=== Checking FreeCAD installation ===")

    # Check if FreeCAD app exists
    freecad_app = Path("/Applications/FreeCAD.app")
    if freecad_app.exists():
        print(f"✅ FreeCAD app found at {freecad_app}")
    else:
        print("❌ FreeCAD app not found in /Applications/")
        return False

    # Check if FreeCAD Python modules are accessible
    try:
        import FreeCAD
        print(f"✅ FreeCAD Python module imported successfully (version: {FreeCAD.Version()})")
        return True
    except ImportError as e:
        print(f"❌ FreeCAD Python modules not accessible: {e}")

        # Suggest common FreeCAD Python paths
        common_paths = [
            "/Applications/FreeCAD.app/Contents/Resources/lib",
            "/Applications/FreeCAD.app/Contents/lib",
            "/Applications/FreeCAD.app/Contents/Resources/lib/python3.11/site-packages"
        ]

        print("\n🔧 Possible solutions:")
        print("1. Add FreeCAD Python path to PYTHONPATH:")
        for path in common_paths:
            if Path(path).exists():
                print(f"   export PYTHONPATH=\"{path}:$PYTHONPATH\"")

        print("\n2. Check actual FreeCAD Python paths:")
        freecad_lib = freecad_app / "Contents" / "Resources" / "lib"
        if freecad_lib.exists():
            print(f"   Found lib directory: {freecad_lib}")
            for item in freecad_lib.iterdir():
                if item.is_dir() and "python" in item.name:
                    print(f"   Python directory: {item}")

        return False

def check_claude_desktop_config():
    """Check Claude Desktop configuration."""
    print("\n=== Checking Claude Desktop configuration ===")

    config_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    if config_path.exists():
        print(f"✅ Claude Desktop config found at {config_path}")
        try:
            import json
            with open(config_path) as f:
                config = json.load(f)

            if "mcpServers" in config and "freecad" in config["mcpServers"]:
                freecad_config = config["mcpServers"]["freecad"]
                print("✅ FreeCAD MCP server configured")
                print(f"   Command: {freecad_config.get('command', 'Not set')}")
                print(f"   Args: {freecad_config.get('args', 'Not set')}")
                print(f"   Working directory: {freecad_config.get('cwd', 'Not set')}")

                # Check if the working directory exists and is correct
                cwd = freecad_config.get('cwd')
                if cwd and Path(cwd).exists():
                    print("✅ Working directory exists")
                    if Path(cwd).resolve() == Path.cwd().resolve():
                        print("✅ Working directory matches current directory")
                    else:
                        print(f"⚠️  Working directory mismatch. Config: {cwd}, Current: {Path.cwd()}")
                elif cwd:
                    print(f"❌ Working directory does not exist: {cwd}")

            else:
                print("❌ FreeCAD MCP server not configured")
                print("\n🔧 Add this to your claude_desktop_config.json:")
                print(f'''{{
  "mcpServers": {{
    "freecad": {{
      "command": "uv",
      "args": ["run", "mcp-server-freecad"],
      "cwd": "{Path.cwd()}"
    }}
  }}
}}''')
        except Exception as e:
            print(f"❌ Error reading config: {e}")
    else:
        print(f"❌ Claude Desktop config not found at {config_path}")
        print("🔧 Create the config file with the FreeCAD MCP server configuration")

def test_server_startup():
    """Test if the server can start properly."""
    print("\n=== Testing server startup ===")
    try:
        result = subprocess.run(['python', 'test_server.py'],
                              capture_output=True, text=True, timeout=30)
        if "Server instance created successfully" in result.stdout:
            print("✅ Server can be created")
        if "Entry points work correctly" in result.stdout:
            print("✅ Entry points configured correctly")
        if "FreeCAD modules not available" in result.stderr:
            print("⚠️  FreeCAD modules not available (expected if not configured)")
        if result.returncode == 0:
            print("✅ test_server.py completed successfully")
        else:
            print(f"❌ test_server.py failed: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⚠️  Server test timed out (server might be running)")
    except Exception as e:
        print(f"❌ Error running server test: {e}")

def main():
    """Run all troubleshooting checks."""
    print("🔧 MCP FreeCAD Server Troubleshooting")
    print("=" * 50)

    checks = [
        check_uv_installation,
        check_entry_point,
        check_freecad_installation,
        check_claude_desktop_config,
        test_server_startup
    ]

    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed with error: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    print("📊 Summary:")
    passed = sum(results)
    total = len(results)
    print(f"✅ {passed}/{total} checks passed")

    if passed == total:
        print("\n🎉 All checks passed! The MCP server should work with Claude Desktop.")
    else:
        print("\n⚠️  Some issues found. Please address the failed checks above.")

if __name__ == "__main__":
    main()
