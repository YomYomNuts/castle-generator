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
    wallWidth = bpy.props.FloatProperty(name="Width of wall", description="Width of wall", default=3)
    wallHeight = bpy.props.FloatProperty(name="Height of wall", description="Height of wall", default=5)
    
	# Crenels
    indexVertexGroup = bpy.props.IntProperty(name="Index edges", description="Index edges", default=3)
    lowWallHeight = bpy.props.FloatProperty(name="Height low wall", description="Height of low wall", default=1)
    lowWallWidth = bpy.props.FloatProperty(name="Width low wall", description="Width of low wall", default=0.5)
    beginByCrenel = bpy.props.BoolProperty(name="Begin by crenel", description="Begin by a crenel", default=True)
    inverseSensCreation = bpy.props.BoolProperty(name="Inverse sens creation", description="Inverse the sens of creation", default=False)
    crenelLength = bpy.props.FloatProperty(name="Length crenel", description="Length of crenel", default=0.4)
    merlonLength = bpy.props.FloatProperty(name="Length merlon", description="Length of merlon", default=0.6)
    merlonHeight = bpy.props.FloatProperty(name="Height merlon", description="Height of merlon", default=0.5)
    
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
        objects = [obj for obj in bpy.context.scene.objects if obj.select]
		
        if len(objects) == 2 and objects[0] != None and objects[1] != None:
            # Wall
            layout.label("Wall", icon='ACTION')
            row = layout.row()
            box = row.box()
            box.prop(castlegenerator, 'wallWidth')
            box.prop(castlegenerator, 'wallHeight')
            box.operator("castlegenerator.generatewalls", text="Generate walls", icon="MESH_CUBE")
            layout.row()
        elif len(objects) == 1 and objects[0] != None:
            # Crenel
            layout.label("Crenels", icon='ACTION')
            row = layout.row()
            box = row.box()
            box.prop(castlegenerator, 'indexVertexGroup')
            box.prop(castlegenerator, 'lowWallHeight')
            box.prop(castlegenerator, 'lowWallWidth')
            box.prop(castlegenerator, 'beginByCrenel')
            box.prop(castlegenerator, 'inverseSensCreation')
            box.prop(castlegenerator, 'crenelLength')
            box.prop(castlegenerator, 'merlonLength')
            box.prop(castlegenerator, 'merlonHeight')
            box.operator("castlegenerator.generatecrenels", text="Generate crenels", icon="PINNED")
        else:
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


class OBJECT_OT_GenerateWalls(bpy.types.Operator):
    bl_idname = "castlegenerator.generatewalls"
    bl_label = "Generate walls"
    def execute(self, context):
        castlegenerator = bpy.context.window_manager.castlegenerator
        objects = [obj for obj in bpy.context.scene.objects if obj.select]
		
        if len(objects) == 2 and objects[0] != None and objects[1] != None:
            WallGenerator(objects[0], objects[1], castlegenerator.wallWidth, castlegenerator.wallHeight)
        return{'FINISHED'}


class OBJECT_OT_GenerateCrenels(bpy.types.Operator):
    bl_idname = "castlegenerator.generatecrenels"
    bl_label = "Generate crenels"
    def execute(self, context):
        castlegenerator = bpy.context.window_manager.castlegenerator
        objects = [obj for obj in bpy.context.scene.objects if obj.select]
		
        if len(objects) == 1 and objects[0] != None:
            CrenelGenerator(objects[0], castlegenerator.indexVertexGroup, castlegenerator.lowWallHeight, castlegenerator.lowWallWidth, castlegenerator.beginByCrenel, castlegenerator.inverseSensCreation, castlegenerator.crenelLength, castlegenerator.merlonLength, castlegenerator.merlonHeight)
        return{'FINISHED'}


class OBJECT_OT_GenerateTowers(bpy.types.Operator):
    bl_idname = "castlegenerator.generatetowers"
    bl_label = "Generate towers"
    def execute(self, context):
        castlegenerator = bpy.context.window_manager.castlegenerator
        if bpy.context.active_object != None:
            positionTowers = WallGenerator.getPositionBaseTowers()
            index = 0
            for pos in positionTowers:
                if index == 0:
                    Tower(pos, castlegenerator.lodTower, castlegenerator.radiusTower, castlegenerator.heightBodyTower, castlegenerator.heightBaseTower, castlegenerator.offsetBaseTower, castlegenerator.heightWallTower, castlegenerator.heightRempartTower, castlegenerator.offsetRempartTower)
                else:
                    bpy.ops.object.duplicate_move(TRANSFORM_OT_translate={"value":(0,0,0)})
                    bpy.context.active_object.location = pos
                index += 1
        else:
            print("No wall selected!!")
        return{'FINISHED'}


classes = [propertiesCastleGenerator, panelCastleGenerator, OBJECT_OT_GenerateWalls, OBJECT_OT_GenerateCrenels, OBJECT_OT_GenerateTowers]

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