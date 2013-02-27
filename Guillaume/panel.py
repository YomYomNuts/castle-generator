import bpy
from bpy.props import *
from wallGenerator import *
#from tower import *

bl_info = {
    "name": "Castle Generator",
    "author": "Léon Denise and Guillaume Noisette",
    "version": (0, 1, 0),
    "blender": (2, 6, 6),
    "api": 36373,
    "location": "View3D > Tools",
    "description": "Addon for generating a castle",
    'category': 'Object'
    }

class propertiesCastleGenerator(bpy.types.PropertyGroup):
    positionCenter = bpy.props.FloatVectorProperty(name="Central position castle", description="Central position of the castle")
    distanceFirstWall = bpy.props.IntProperty(name="Distance first wall", description="Distance between the first wall and the central position", default=20)
    minimalWallLenghtFirst = bpy.props.IntProperty(name="Minimal lenght first wall", description="Minimal lenght of the first wall", default=20)
    maximalWallLenghtFirst = bpy.props.IntProperty(name="Maximal lenght first wall", description="Maximal lenght of the first wall", default=26)
    widthWallFirst = bpy.props.IntProperty(name="Width first wall", description="Width of the first wall", default=4)
    minimalHeightWallFirst = bpy.props.IntProperty(name="Minimal height first wall", description="Minimal height of the first wall", default=10)
    maximalHeightWallFirst = bpy.props.IntProperty(name="Maximal height first wall", description="Maximal height of the first wall", default=15)

class panelCastleGenerator(bpy.types.Panel):
    bl_label = "Castle Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    def draw(self, context):
        layout = self.layout
        castlegenerator = bpy.context.window_manager.castlegenerator
        
        layout.label("Wall", icon='ACTION')
        row = layout.row()
        box = row.box()
        box.prop(castlegenerator, 'positionCenter')
        box.prop(castlegenerator, 'distanceFirstWall')
        box.prop(castlegenerator, 'minimalWallLenghtFirst')
        box.prop(castlegenerator, 'maximalWallLenghtFirst')
        box.prop(castlegenerator, 'widthWallFirst')
        box.prop(castlegenerator, 'minimalHeightWallFirst')
        box.prop(castlegenerator, 'maximalHeightWallFirst')
        box.operator("castlegenerator.generatewalls", text="Generate walls", icon="MESH_CUBE")
        layout.row()
        
        layout.label("Towers", icon='ACTION')
        row = layout.row()
        box = row.box()
        box.operator("castlegenerator.generatetowers", text="Generate towers", icon="PINNED")


class OBJECT_OT_GenerateWalls(bpy.types.Operator):
    bl_idname = "castlegenerator.generatewalls"
    bl_label = "Generate walls"
    def execute(self, context):
        castlegenerator = bpy.context.window_manager.castlegenerator
        wall = WallGenerator()
        return{'FINISHED'}

class OBJECT_OT_GenerateTowers(bpy.types.Operator):
    bl_idname = "castlegenerator.generatetowers"
    bl_label = "Generate towers"
    def execute(self, context):
        castlegenerator = bpy.context.window_manager.castlegenerator
        WallGenerator.getPositionBaseTowers()
        return{'FINISHED'}


classes = [propertiesCastleGenerator, panelCastleGenerator, OBJECT_OT_GenerateWalls, OBJECT_OT_GenerateTowers]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.castlegenerator = bpy.props.PointerProperty(type=propertiesCastleGenerator)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.WindowManager.castlegenerator
    
if __name__ == "__main__":
    register()