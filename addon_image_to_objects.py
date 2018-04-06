import os

import bpy
from bpy.props import StringProperty, PointerProperty, BoolProperty

from bpy.types import Panel, Operator, PropertyGroup


bl_info = {
    "name": "Image Pixels as Objects",
    "category": "Object",
}


def check_color(context, image_path, use_materials):
    bpy.ops.image.open(
        filepath=image_path,
        directory="",
        relative_path=True,
        show_multiview=False
    )
    image = bpy.data.images[os.path.basename(image_path)]
    for col in range(image.size[0]):
        for row in range(image.size[1]):
            offset = (row * image.size[0] + col) * 4
            pixel = image.pixels[offset:offset+4]
            if not pixel[3]:
                continue
            bpy.ops.mesh.primitive_cube_add(
                radius=.5,
                view_align=False,
                enter_editmode=False,
                location=(col, row, 0)
            )
            if use_materials:
                color_name = "#" + "".join("%X" % int(255 * c) for c in pixel[:3])
                try:
                    material = bpy.data.materials[color_name]
                except KeyError:
                    bpy.ops.material.new()
                    material = bpy.data.materials["Material"]
                    material.name = color_name
                    material.diffuse_color = tuple(c for c in pixel)[0:3]
                context.active_object.data.materials.append(material)
    bpy.data.images.remove(image)


class PixelsAsObjects(Operator):
    """Load image pixels as blender objects"""

    bl_idname = "add.pixels_as_objects"
    bl_label = "Load image pixels as objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        check_color(
            context,
            context.scene.pixels_as_objects.path,
            context.scene.pixels_as_objects.use_materials
        )
        return {'FINISHED'}


class PixelSettings(PropertyGroup):

    path = StringProperty(
        name="",
        description="Path to file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )

    use_materials = BoolProperty(
        name = "",
        description = "Use Materials from pixel colors"
    )


class PixelsAsObjectsPanel(Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Pixels to Objects"
    bl_idname = "SCENE_PT_pixels_to_objects_2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Create"
    bl_context = "objectmode"

    def draw(self, context):
        print("desenhando o painel")
        layout = self.layout

        scene = context.scene

        layout.label(text=" Image to pick:")
        row = layout.row()
        row.prop(scene.pixels_as_objects, "path", text="")
        row = layout.row()
        row.prop(scene.pixels_as_objects, "use_materials", text="Use materials")
        row = layout.row()
        row.operator("add.pixels_as_objects")


def register():
    print("Rodando o register")
    bpy.utils.register_module(__name__)
    bpy.types.Scene.pixels_as_objects = PointerProperty(type=PixelSettings)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
