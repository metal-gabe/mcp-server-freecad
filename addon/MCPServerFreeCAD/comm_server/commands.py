# ruff: noqa
# type: ignore
import FreeCAD
from .comm_server import start_comm_server, stop_comm_server


class StartCommServerCommand:
    def GetResources(self):
        return {"MenuText": "Start Comm Server", "ToolTip": "Start Comm Server"}

    def Activated(self):
        msg = start_comm_server()
        FreeCAD.Console.PrintMessage(msg + "\n")

    def IsActive(self):
        return True


class StopCommServerCommand:
    def GetResources(self):
        return {"MenuText": "Stop Comm Server", "ToolTip": "Stop Comm Server"}

    def Activated(self):
        msg = stop_comm_server()
        FreeCAD.Console.PrintMessage(msg + "\n")

    def IsActive(self):
        return True
