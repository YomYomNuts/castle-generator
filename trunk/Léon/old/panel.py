import bpy
from bpy.props import *
from wallGenerator import *
from tower import *

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
    # Walls
    positionCenter = bpy.props.FloatVectorProperty(name="Central position castle", description="Central position of the castle", subtype="XYZ")
    distanceFirstWall = bpy.props.IntProperty(name="Distance first wall", description="Distance between the first wall and the central position", default=300)
    minimalWallLenghtFirst = bpy.props.IntProperty(name="Minimal lenght first wall", description="Minimal lenght of the first wall", default=171)
    maximalWallLenghtFirst = bpy.props.IntProperty(name="Maximal lenght first wall", description="Maximal lenght of the first wall", default=171)
    widthWallFirst = bpy.props.IntProperty(name="Width first wall", description="Width of the first wall", default=5)
    minimalHeightWallFirst = bpy.props.IntProperty(name="Minimal height first wall", description="Minimal height of the first wall", default=100)
    maximalHeightWallFirst = bpy.props.IntProperty(name="Maximal height first wall", description="Maximal height of the first wall", default=100)
    
    # Towers
    lodTower = bpy.props.IntProperty(name="Number vertices", description="Number vertices of the base of tower", default=16)
    radiusTower = bpy.props.IntProperty(name="Size Tower", description="Size of the base of tower", default=20)
    heightBodyTower = bpy.props.IntProperty(name="Height body tower", description="Height tower until ramparts", default=100)
    heightBaseTower = bpy.props.IntProperty(name="Height curve", description="Height curve", default=4)
    offsetBaseTower = bpy.props.IntProperty(name="Offset curve", description="Offset of the curve", default=2)
    heightWallTower = bpy.props.IntProperty(name="Height wall tower", description="Height tower between ramparts and roof", default=20)
    heightRempartTower = bpy.props.IntProperty(name="Height rampart tower", description="Height ramparts of tower", default=50)
    offsetRempartTower = bpy.props.IntProperty(name="Offset rampart tower", description="Offset ramparts of tower", default=30)


class panelCastleGenerator(bpy.types.Panel):
    bl_label = "Castle Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    def draw(self, context):
        layout = self.layout
        castlegenerator = bpy.context.window_manager.castlegenerator
        
        # Wall
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
        
        # Tower
        layout.label("Towers", icon='ACTION')
        row = layout.row()
        box = row.box()
        box.prop(castlegenerator, 'lodTower')
        box.prop(castlegenerator, 'radiusTower')
        box.prop(castlegenerator, 'heightBodyTower')
        box.prop(castlegenerator, 'heightBaseTower')
        box.prop(castlegenerator, 'offsetBaseTower')
        box.prop(castlegenerator, 'heightWallTower')
        box.prop(castlegenerator, 'heightRempartTower')
        box.prop(castlegenerator, 'offsetRempartTower')
        box.operator("castlegenerator.generatetowers", text="Generate towers", icon="PINNED")
        box.operator("castlegenerator.refreshtowers", text="Refresh towers", icon="PINNED")


class OBJECT_OT_GenerateWalls(bpy.types.Operator):
    bl_idname = "castlegenerator.generatewalls"
    bl_label = "Generate walls"
    def execute(self, context):
        castlegenerator = bpy.context.window_manager.castlegenerator
        wall = WallGenerator(castlegenerator.positionCenter, castlegenerator.distanceFirstWall, castlegenerator.minimalWallLenghtFirst, castlegenerator.maximalWallLenghtFirst, castlegenerator.widthWallFirst, castlegenerator.minimalHeightWallFirst, castlegenerator.maximalHeightWallFirst)
        return{'FINISHED'}

tower = Tower((0,0,0), 16, 10, 20, 20, 20, 20, 20, 20)
		
class OBJECT_OT_GenerateTowers(bpy.types.Operator):
	bl_idname = "castlegenerator.generatetowers"
	bl_label = "Generate towers"
	def execute(self, context):
		castlegenerator = bpy.context.window_manager.castlegenerator
		tower = Tower((0,0,0), castlegenerator.lodTower, castlegenerator.radiusTower, castlegenerator.heightBodyTower, castlegenerator.heightBaseTower, castlegenerator.offsetBaseTower, castlegenerator.heightWallTower, castlegenerator.heightRempartTower, castlegenerator.offsetRempartTower)
		return{'FINISHED'}

class OBJECT_OT_RefreshTowers(bpy.types.Operator):
	bl_idname = "castlegenerator.refreshtowers"
	bl_label = "Refresh Towers"
	def execute(self, context):
		castlegenerator = bpy.context.window_manager.castlegenerator
		tower.refresh(castlegenerator.lodTower)
		return{'FINISHED'}


classes = [propertiesCastleGenerator, panelCastleGenerator, OBJECT_OT_GenerateWalls, OBJECT_OT_GenerateTowers, OBJECT_OT_RefreshTowers]

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