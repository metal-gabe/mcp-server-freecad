#!/usr/bin/env python3
"""
Wrapper script to run the MCP server with FreeCAD's Python environment.
This resolves Python version compatibility issues between FreeCAD and the current Python.
"""

import os
import sys
import subprocess
import tempfile

def create_freecad_runner():
    """Create a temporary Python script that runs within FreeCAD's environment"""

    # Get the absolute path to our server code
    server_path = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(server_path, "src")

    runner_code = f'''
import sys
sys.path.insert(0, "{src_path}")

# Install required dependencies in FreeCAD's environment
try:
    import pip
    pip.main(['install', '--quiet', 'fastmcp>=2.11.3', 'loguru>=0.7.3'])
except:
    # Try subprocess if pip.main doesn't work
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', 'fastmcp>=2.11.3', 'loguru>=0.7.3'])

# Now run our server
from mcp_server_freecad.main import main
main()
'''

    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(runner_code)
        return f.name

def main():
    """Run the MCP server using FreeCAD's Python"""

    # Check if FreeCAD is available
    freecad_python_paths = [
        "/Applications/FreeCAD.app/Contents/Resources/bin/python",
        "/usr/bin/freecad-python",  # Linux
        "C:\\Program Files\\FreeCAD\\bin\\python.exe",  # Windows
    ]

    freecad_python = None
    for path in freecad_python_paths:
        if os.path.exists(path):
            freecad_python = path
            break

    if not freecad_python:
        print("❌ FreeCAD Python not found. Please install FreeCAD or run with regular Python.")
        print("Available paths checked:")
        for path in freecad_python_paths:
            print(f"  - {path}")
        sys.exit(1)

    print(f"🚀 Using FreeCAD Python: {freecad_python}")

    # Create temporary runner script
    runner_script = create_freecad_runner()

    try:
        # Set environment variables for FreeCAD
        env = os.environ.copy()
        env['PYTHONPATH'] = '/Applications/FreeCAD.app/Contents/Resources'
        env['LD_LIBRARY_PATH'] = '/Applications/FreeCAD.app/Contents/Resources/lib'

        # Run the server with FreeCAD's Python
        subprocess.run([freecad_python, runner_script], env=env)

    finally:
        # Clean up temporary file
        try:
            os.unlink(runner_script)
        except:
            pass

if __name__ == "__main__":
    main()
