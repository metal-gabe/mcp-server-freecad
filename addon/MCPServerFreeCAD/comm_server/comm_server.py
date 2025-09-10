import FreeCAD
import FreeCADGui
import threading
from xmlrpc.server import SimpleXMLRPCServer
from PySide import QtCore

from .freecad_rpc import FreeCADRPC
from .utils import process_gui_tasks, request_queue, response_queue
from .commands import StartRPCServerCommand, StopRPCServerCommand

rpc_server_instance = None
rpc_server_thread = None


def start_rpc_server(host="localhost", port=9875):
    global rpc_server_thread, rpc_server_instance

    if rpc_server_instance:
        return "RPC Server already running."

    rpc_server_instance = SimpleXMLRPCServer(
        (host, port), allow_none=True, logRequests=False
    )
    rpc_server_instance.register_instance(FreeCADRPC())

    def server_loop():
        FreeCAD.Console.PrintMessage(f"RPC Server started at {host}:{port}\n")
        rpc_server_instance.serve_forever()

    rpc_server_thread = threading.Thread(target=server_loop, daemon=True)
    rpc_server_thread.start()

    QtCore.QTimer.singleShot(500, process_gui_tasks)

    return f"RPC Server started at {host}:{port}."


def stop_rpc_server():
    global rpc_server_instance, rpc_server_thread

    if rpc_server_instance:
        rpc_server_instance.shutdown()
        rpc_server_thread.join()
        rpc_server_instance = None
        rpc_server_thread = None
        FreeCAD.Console.PrintMessage("RPC Server stopped.\n")
        return "RPC Server stopped."

    return "RPC Server was not running."


FreeCADGui.addCommand("Start_RPC_Server", StartRPCServerCommand())
FreeCADGui.addCommand("Stop_RPC_Server", StopRPCServerCommand())
