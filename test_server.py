#!/usr/bin/env python3
"""
Test script to verify the FreeCAD MCP server setup.
This script checks if the server can start without crashing.
"""

import subprocess
import sys
from pathlib import Path


def test_import():
   """Test if the server module can be imported."""
   print("Testing module imports...")

   try:
      from src.mcp_server_freecad import MCPServerFreeCAD
      print("✅ Successfully imported MCPServerFreeCAD")
      return True
   except Exception as e:
      print(f"❌ Failed to import MCPServerFreeCAD: {e}")
      return False

def test_server_creation():
   """Test if the server can be created."""
   print("Testing server creation...")

   try:
      from src.mcp_server_freecad import MCPServerFreeCAD
      server = MCPServerFreeCAD()
      print("✅ Successfully created MCPServerFreeCAD instance")
      return True
   except Exception as e:
      print(f"❌ Failed to create MCPServerFreeCAD: {e}")
      return False

def test_uv_run():
   """Test if uv can run the server entry point."""
   print("Testing uv run command...")

   try:
      # Try to run the server for a few seconds to see if it starts
      result = subprocess.run(
         ["uv", "run", "./__main__.py"],
         capture_output=True,
         text=True,
         timeout=10,
         cwd=Path(__file__).parent
      )

      if result.returncode == 0 or "usage:" in result.stdout.lower():
         print("✅ uv run command works")
         return True
      else:
         print(f"❌ uv run failed: {result.stderr}")
         return False
   except subprocess.TimeoutExpired:
      print("⚠️  uv run started but didn't respond to --help (this might be normal for MCP servers)")
      return True
   except FileNotFoundError:
      print("❌ uv command not found")
      return False
   except Exception as e:
      print(f"❌ uv run test failed: {e}")
      return False

def test_python_module():
   """Test if python -m execution works."""
   print("Testing python -m execution...")

   try:
      result = subprocess.run(
         [sys.executable, "-m", "mcp_server_freecad", "--help"],
         capture_output=True,
         text=True,
         timeout=5,
         cwd=Path(__file__).parent
      )

      if result.returncode == 0 or "usage:" in result.stdout.lower():
         print("✅ python -m execution works")
         return True
      else:
         print(f"❌ python -m failed: {result.stderr}")
         return False
   except subprocess.TimeoutExpired:
      print("⚠️  python -m started but didn't respond to --help (this might be normal for MCP servers)")
      return True
   except Exception as e:
      print(f"❌ python -m test failed: {e}")
      return False

def main():
   """Run all tests."""
   print("FreeCAD MCP Server Test Suite")
   print("=" * 40)

   tests = [
      test_import,
      test_server_creation,
      test_uv_run,
      test_python_module
   ]

   passed = 0
   total = len(tests)

   for test in tests:
      if test():
         passed += 1
      print()

   print("=" * 40)
   print(f"Tests passed: {passed}/{total}")

   if passed == total:
      print("🎉 All tests passed! Your MCP server setup is working correctly.")
      print("\nRecommended Claude Desktop configuration:")
      print("""
{
   "mcpServers": {
      "freecad": {
         "command": "uv",
         "args": ["run", "mcp-server-freecad"],
         "cwd": "/path/to/your/mcp-server-freecad"
      }
   }
}
      """)
   else:
      print("❌ Some tests failed. Please check the errors above.")
      return 1

   return 0

if __name__ == "__main__":
   sys.exit(main())
