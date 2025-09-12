from dataclasses import dataclass
from typing import Any, Dict, Literal

from fastmcp import FastMCP
from loguru import logger


@dataclass
class FreeCADOperation:
    description: str
    operation: str
    parameters: Dict[str, Any]


class MCPServerFreeCAD:
    def __init__(self):
        self.active_body = None
        self.doc = None
        self.server = FastMCP("freecad-mcp")
        self.setup_tools()

    ## ==========================================================================
    ## PUBLIC METHODS
    ## ==========================================================================
    def setup_tools(self):
        @self.server.tool(
            name="boolean_operation",
            description="Perform boolean operations (cut, intersection, union)",
        )
        async def boolean_operation(
            operation: Literal["cut", "intersection", "union"],
            base_object: str,
            tool_object: str,
            result_name: str | None = None,
        ) -> str:
            args: Dict[str, Any] = {
                "operation": operation,
                "base_object": base_object,
                "tool_object": tool_object,
            }

            if result_name is not None:
                args["result_name"] = result_name

            return await self._boolean_operation(args)

        @self.server.tool(
            name="create_box", description="Create a rectangular box/cube"
        )
        async def create_box(
            length: float,
            width: float,
            height: float,
            x: float = 0,
            y: float = 0,
            z: float = 0,
            name: str | None = None,
        ) -> str:
            args: Dict[str, Any] = {
                "length": length,
                "width": width,
                "height": height,
                "position": {"x": x, "y": y, "z": z},
            }

            if name is not None:
                args["name"] = name

            return await self._create_box(args)

        @self.server.tool(name="create_cylinder", description="Create a cylinder")
        async def create_cylinder(
            radius: float,
            height: float,
            x: float = 0,
            y: float = 0,
            z: float = 0,
            name: str | None = None,
        ) -> str:
            args: Dict[str, Any] = {
                "radius": radius,
                "height": height,
                "position": {"x": x, "y": y, "z": z},
            }

            if name is not None:
                args["name"] = name

            return await self._create_cylinder(args)

        @self.server.tool(
            name="create_document", description="Create a new FreeCAD document"
        )
        async def create_document(name: str) -> str:
            return await self._create_document({"name": name})

        @self.server.tool(
            name="create_pad", description="Create a pad (extrusion) from a sketch"
        )
        async def create_pad(
            sketch_name: str,
            length: float,
            reversed: bool = False,
            name: str | None = None,
        ) -> str:
            args: Dict[str, Any] = {
                "sketch_name": sketch_name,
                "length": length,
                "reversed": reversed,
            }

            if name is not None:
                args["name"] = name

            return await self._create_pad(args)

        @self.server.tool(
            name="create_pocket", description="Create a pocket (cut) from a sketch"
        )
        async def create_pocket(
            sketch_name: str, length: float, name: str | None = None
        ) -> str:
            args: Dict[str, Any] = {
                "sketch_name": sketch_name,
                "length": length,
            }

            if name is not None:
                args["name"] = name

            return await self._create_pocket(args)

        @self.server.tool(
            name="create_sketch", description="Create a new sketch on a plane"
        )
        async def create_sketch(
            plane: Literal["XY", "XZ", "YZ", "custom"], name: str | None = None
        ) -> str:
            args: Dict[str, Any] = {"plane": plane}

            if name is not None:
                args["name"] = name

            return await self._create_sketch(args)

        @self.server.tool(name="create_sphere", description="Create a sphere")
        async def create_sphere(
            radius: float,
            x: float = 0,
            y: float = 0,
            z: float = 0,
            name: str | None = None,
        ) -> str:
            args: Dict[str, Any] = {
                "radius": radius,
                "position": {"x": x, "y": y, "z": z},
            }

            if name is not None:
                args["name"] = name

            return await self._create_sphere(args)

        @self.server.tool(name="export_stl", description="Export objects to STL file")
        async def export_stl(objects: list[str], filepath: str) -> str:
            return await self._export_stl({"objects": objects, "filepath": filepath})

        @self.server.tool(
            name="list_objects", description="List all objects in the current document"
        )
        async def list_objects() -> str:
            return await self._list_objects()

        @self.server.tool(
            name="move_object", description="Move an object to a new position"
        )
        async def move_object(object_name: str, x: float, y: float, z: float) -> str:
            return await self._move_object(
                {
                    "object_name": object_name,
                    "vector": {"x": x, "y": y, "z": z},
                }
            )

        @self.server.tool(
            name="rotate_object", description="Rotate an object around an axis"
        )
        async def rotate_object(
            object_name: str, ax: float, ay: float, az: float, angle: float
        ) -> str:
            return await self._rotate_object(
                {
                    "object_name": object_name,
                    "axis": {"x": ax, "y": ay, "z": az},
                    "angle": angle,
                }
            )

        @self.server.tool(name="save_document", description="Save the current document")
        async def save_document(filepath: str) -> str:
            return await self._save_document({"filepath": filepath})

        # Keep references so static analyzers (e.g., Pylance/PyCharm) treat these as accessed
        # even though the decorator registers them for runtime use.
        self._registered_tools = [
            boolean_operation,
            create_box,
            create_cylinder,
            create_document,
            create_pad,
            create_pocket,
            create_sketch,
            create_sphere,
            export_stl,
            list_objects,
            move_object,
            rotate_object,
            save_document,
        ]

    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        try:
            if tool_name == "boolean_operation":
                return await self._boolean_operation(arguments)
            elif tool_name == "create_box":
                return await self._create_box(arguments)
            elif tool_name == "create_cylinder":
                return await self._create_cylinder(arguments)
            elif tool_name == "create_document":
                return await self._create_document(arguments)
            elif tool_name == "create_pad":
                return await self._create_pad(arguments)
            elif tool_name == "create_pocket":
                return await self._create_pocket(arguments)
            elif tool_name == "create_sketch":
                return await self._create_sketch(arguments)
            elif tool_name == "create_sphere":
                return await self._create_sphere(arguments)
            elif tool_name == "export_stl":
                return await self._export_stl(arguments)
            elif tool_name == "list_objects":
                return await self._list_objects()
            elif tool_name == "move_object":
                return await self._move_object(arguments)
            elif tool_name == "rotate_object":
                return await self._rotate_object(arguments)
            elif tool_name == "save_document":
                return await self._save_document(arguments)
            else:
                return f"Unknown tool: {tool_name}"
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"

    ## ==========================================================================
    ## PRIVATE METHODS
    ## ==========================================================================
    async def _boolean_operation(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.info(
                "BooleanOperation: No document available, ignoring boolean operation..."
            )
            return "No document available"

        base_name = args["base_object"]
        operation = args["operation"]
        result_name = args.get("result_name", f"{operation}_{len(self.doc.Objects)}")
        tool_name = args["tool_object"]

        base_obj = self.doc.getObject(base_name)
        tool_obj = self.doc.getObject(tool_name)

        if not base_obj or not tool_obj:
            return f"Could not find objects: {base_name}, {tool_name}"

        if operation == "cut":
            result = self.doc.addObject("Part::Cut", result_name)
        elif operation == "intersection":
            result = self.doc.addObject("Part::Common", result_name)
        elif operation == "union":
            result = self.doc.addObject("Part::Fuse", result_name)
        else:
            return f"Unknown operation: {operation}"

        result.Base = base_obj
        result.Tool = tool_obj

        self.doc.recompute()
        return f"Created {operation} operation '{result_name}'"

    async def _create_box(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.info("CreateBox: No document available, creating new document...")
            self.doc = FreeCAD.newDocument("Document")

        height = args["height"]
        length = args["length"]
        name = args.get("name", f"Box_{len(self.doc.Objects)}")
        position = args.get("position", {"x": 0, "y": 0, "z": 0})
        width = args["width"]

        box = self.doc.addObject("Part::Box", name)
        box.Height = height
        box.Length = length
        box.Placement.Base = FreeCAD.Vector(position["x"], position["y"], position["z"])
        box.Width = width

        self.doc.recompute()
        return f"Created box '{name}' with dimensions {length}x{width}x{height}mm"

    async def _create_cylinder(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.info(
                "CreateCylinder: No document available, creating new document..."
            )
            self.doc = FreeCAD.newDocument("Document")

        height = args["height"]
        name = args.get("name", f"Cylinder_{len(self.doc.Objects)}")
        position = args.get("position", {"x": 0, "y": 0, "z": 0})
        radius = args["radius"]

        cylinder = self.doc.addObject("Part::Cylinder", name)
        cylinder.Height = height
        cylinder.Placement.Base = FreeCAD.Vector(
            position["x"], position["y"], position["z"]
        )
        cylinder.Radius = radius

        self.doc.recompute()
        return f"Created cylinder '{name}' with radius {radius}mm and height {height}mm"

    async def _create_document(self, args: Dict[str, Any]) -> str:
        logger.info("CreateDocument: Starting new document creation...")
        doc_name = args.get("name", "Document")
        self.doc = FreeCAD.newDocument(doc_name)
        return f"Created document: {doc_name}"

    async def _create_sketch(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.info("CreateSketch: No document available, creating new document...")
            self.doc = FreeCAD.newDocument("Document")

        return f"Not implemented: {str(args)}"

    async def _create_sphere(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.info("CreateSphere: No document available, creating new document...")
            self.doc = FreeCAD.newDocument("Document")

        name = args.get("name", f"Sphere_{len(self.doc.Objects)}")
        position = args.get("position", {"x": 0, "y": 0, "z": 0})
        radius = args["radius"]

        sphere = self.doc.addObject("Part::Sphere", name)
        sphere.Placement.Base = FreeCAD.Vector(
            position["x"], position["y"], position["z"]
        )
        sphere.Radius = radius

        self.doc.recompute()
        return f"Created sphere '{name}' with radius {radius}mm"

    async def _create_pad(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.info("CreatePad: No document available, creating new document...")
            self.doc = FreeCAD.newDocument("Document")

        # TODO: Implement PartDesign Pad operation from a sketch
        # Expected args: sketch_name (str), length (float), reversed (bool), name (str)
        return f"Not implemented: create_pad {str(args)}"

    async def _create_pocket(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.info("CreatePocket: No document available, creating new document...")
            self.doc = FreeCAD.newDocument("Document")

        # TODO: Implement PartDesign Pocket operation from a sketch
        # Expected args: sketch_name (str), length (float), name (str)
        return f"Not implemented: create_pocket {str(args)}"

    async def _export_stl(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.warning(
                "ExportSTL: No document available, nothing to export, ignoring request..."
            )
            return "No document available"

        filepath = args["filepath"]
        object_names = args["objects"]
        objects = []

        for name in object_names:
            obj = self.doc.getObject(name)

            if obj:
                logger.debug(f"ExportSTL: Adding object to list: {name}")
                objects.append(obj)

        if len(objects) > 0:
            logger.debug(f"ExportSTL: Exporting {len(objects)} objects to: {filepath}")
            import Mesh

            meshes = []

            for obj in objects:
                logger.debug(f"ExportSTL: Adding object to mesh: {obj.Label}")
                mesh = Mesh.Mesh()
                mesh.addFacets(obj.Shape.tessellate(0.1))
                meshes.append(mesh)

            if len(meshes) == 1:
                meshes[0].write(filepath)
            else:
                combined = meshes[0]

                for mesh in meshes[1:]:
                    combined.addMesh(mesh)

                combined.write(filepath)

            logger.debug(f"ExportSTL: Exported {len(objects)} objects to: {filepath}")
            return f"Exported {len(objects)} objects to: {filepath}"
        else:
            logger.debug("ExportSTL: No valid objects found for export")
            return "No valid objects found for export"

    async def _list_objects(self) -> str:
        if not self.doc:
            logger.warning(
                "ListObjects: No document available, nothing to list, ignoring request..."
            )
            return "No document available"

        objects = []

        for obj in self.doc.Objects:
            obj_type = obj.TypeId.split("::")[-1] if "::" in obj.TypeId else obj.TypeId
            objects.append(f"- {obj.Label} ({obj_type})")

        logger.debug(f"ListObjects: Found {len(objects)} objects in document")
        return f"Objects in document:\n" + "\n".join(objects)

    async def _move_object(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.warning("MoveObject: No document available, ignoring request...")
            return "No document available"

        object_name = args["object_name"]
        obj = self.doc.getObject(object_name)
        vec = args["vector"]

        if not obj:
            logger.warning(f"MoveObject: Object not found: {object_name}")
            return f"Object not found: {object_name}"

        ox = float(vec.get("x", 0))
        oy = float(vec.get("y", 0))
        oz = float(vec.get("z", 0))

        current = obj.Placement.Base
        obj.Placement.Base = FreeCAD.Vector(
            current.x + ox, current.y + oy, current.z + oz
        )

        self.doc.recompute()
        return f"Moved '{object_name}' by ({ox}, {oy}, {oz})"

    async def _rotate_object(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.warning("RotateObject: No document available, ignoring request...")
            return "No document available"

        angle = float(args["angle"])  # degrees
        axis = args["axis"]
        object_name = args["object_name"]
        obj = self.doc.getObject(object_name)

        if not obj:
            logger.warning(f"RotateObject: Object not found: {object_name}")
            return f"Object not found: {object_name}"

        ox = float(axis.get("x", 0))
        oy = float(axis.get("y", 0))
        oz = float(axis.get("z", 1))

        base = obj.Placement.Base
        rotation = FreeCAD.Rotation(FreeCAD.Vector(ox, oy, oz), angle)
        obj.Placement = FreeCAD.Placement(base, rotation)

        self.doc.recompute()
        return (
            f"Rotated '{object_name}' around axis ({ox}, {oy}, {oz}) by {angle} degrees"
        )

    async def _save_document(self, args: Dict[str, Any]) -> str:
        if not self.doc:
            logger.warning(
                "SaveDocument: No document available, nothing to save, ignoring request..."
            )
            return "No document available"

        filepath = args["filepath"]
        self.doc.saveAs(filepath)
        logger.debug(f"SaveDocument: Document saved to: {filepath}")
        return f"Document saved to: {filepath}"
