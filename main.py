from server import MCPServerFreeCAD  # type: ignore[attr-defined]

if __name__ == "__main__":
    MCPServerFreeCAD().server.run()  # pyright: ignore[reportUnknownMemberType]
