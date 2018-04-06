import bpy
from PIL import Image

from bpy.props import (StringProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

bl_info = {
    "name": "Image Pixels as Objects",
    "category": "Object",
}

# icone = Image.open("/home/gwidion/tmp12/labirinto.png")

def check_color(context, imagem, use_materials):
    for coluna in range(imagem.width):
        for linha in range(imagem.height):
            pixel = imagem.getpixel((coluna,linha))
            if use_materials:
                bpy.ops.mesh.primitive_cube_add(radius=.5, view_align=False, enter_editmode=False, location=(coluna, -linha, 0))
                try:
                    material = bpy.data.materials[str(pixel)]
                except KeyError:
                    bpy.ops.material.new()
                    material = bpy.data.materials["Material"]
                    material.name = str(pixel)
                    material.diffuse_color = tuple(c/255 for c in pixel)[0:3]
                context.active_object.data.materials.append(material)
            else:
                if ((len(pixel) == 4 and pixel[3]!=0)
                        or (len(pixel) == 3 and pixel==(0,0,0))):
                    bpy.ops.mesh.primitive_cube_add(
                        radius=.5, view_align=False,
                        enter_editmode=False,
                        location=(coluna, -linha, 0)
                    )


class PixelsAsObjects(bpy.types.Operator):
    """Load image pixels as blender objects"""

    bl_idname = "add.pixels_as_objects"        # unique identifier for buttons and menu items to reference.
    bl_label = "Load image pixels as objects"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):        # execute() is called by blender when running the operator.

        image = Image.open(context.scene.pixels_as_objects.path)
        check_color(context, image, context.scene.pixels_as_objects.use_materials)
        return {'FINISHED'}


class PixelSettings(PropertyGroup):

    path = StringProperty(
        name="",
        description="Path to file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH')

        # context.window_manager.fileselect_add(self)
    use_materials = bpy.props.BoolProperty(
        name = "",
        description = "Use Materials from pixel colors"
    )




class PixelsAsObjectsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Pixels to Objects"
    bl_idname = "SCENE_PT_pixels_to_objects_2"
    #bl_space_type = 'PROPERTIES'
    #bl_region_type = 'WINDOW'
    #bl_context = "scene"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_context = "objectmode"

    def draw(self, context):
        print("desenhando o painel")
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        layout.label(text=" Image to pick:")
        row = layout.row()
        row.prop(scene.pixels_as_objects, "path", text="")
        row.prop(scene.pixels_as_objects, "use_materials", text="Use materials")
        row.operator("add.pixels_as_objects")
        # col.prop(scn.my_tool, "path", text="")
        # context.window_manager.fileselect_add(self)


def register():
    print("Rodando o register")
    bpy.utils.register_module(__name__)
    bpy.types.Scene.pixels_as_objects = PointerProperty(type=PixelSettings)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
