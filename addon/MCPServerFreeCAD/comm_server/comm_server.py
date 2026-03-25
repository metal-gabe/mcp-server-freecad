# ruff: noqa
# type: ignore
import FreeCAD
import FreeCADGui
import threading
from xmlrpc.server import SimpleXMLRPCServer
from PySide import QtCore

from .freecad_rpc import FreeCADRPC
from .utils import process_gui_tasks
from .commands import StartCommServerCommand, StopCommServerCommand

comm_server_instance = None
comm_server_thread = None


def start_comm_server(host="localhost", port=7890):
    global comm_server_thread, comm_server_instance

    if comm_server_instance:
        return "Comm Server already running."

    comm_server_instance = SimpleXMLRPCServer(
        (host, port), allow_none=True, logRequests=False
    )

    comm_server_instance.register_instance(FreeCADRPC())

    def server_loop():
        FreeCAD.Console.PrintMessage(f"Comm Server started at {host}:{port}\n")
        comm_server_instance.serve_forever()

    comm_server_thread = threading.Thread(target=server_loop, daemon=True)
    comm_server_thread.start()

    QtCore.QTimer.singleShot(500, process_gui_tasks)

    return f"RPC Server started at {host}:{port}."


def stop_rpc_server():
    global comm_server_instance, comm_server_thread

    if comm_server_instance:
        comm_server_instance.shutdown()
        comm_server_thread.join()
        comm_server_instance = None
        comm_server_thread = None
        FreeCAD.Console.PrintMessage("RPC Server stopped.\n")
        return "RPC Server stopped."

    return "RPC Server was not running."


FreeCADGui.addCommand("Start_Comm_Server", StartCommServerCommand())
FreeCADGui.addCommand("Stop_Comm_Server", StopCommServerCommand())
