# ruff: noqa
# type: ignore
class MCPAddonFreeCADWorkbench(Workbench):
    MenuText = "Claude Desktop MCP Addon"
    ToolTip = "Addon for MCP Communication between Claude Desktop and FreeCAD"

    def Initialize(self):
        from comm_server import comm_server

        commands = ["Start_Comm_Server", "Stop_Comm_Server"]
        self.appendToolbar("FreeCAD MCP", commands)
        self.appendMenu("FreeCAD MCP", commands)

    def Activated(self):
        pass

    def Deactivated(self):
        pass

    def ContextMenu(self):
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(MCPAddonFreeCADWorkbench())
