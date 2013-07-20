import bpy
from bpy.props import *
from utils import *
from wallGenerator import *
from groundGenerator import *
from doorGenerator import *
from towerGenerator import *

bl_info = {
    "name": "Castle Generator",
    "author": "Leon Denise and Guillaume Noisette",
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
    
    # Door
    doorHeight = bpy.props.FloatProperty(name="Height door", description="Height of door", default=3)
    doorWidth = bpy.props.FloatProperty(name="Width door", description="Width of door", default=2)
    doorPositionPercent = bpy.props.FloatProperty(name="Position door", description="Position in percent of door", default=50)
    
    # Towers
    numVertsTower = bpy.props.IntProperty(name="NumVerts", description="Number of vertices of the cylinder", default=24, min=3, max=64)
    radiusTower = bpy.props.FloatProperty(name="Radius", description="Radius of the tower", default=5.0, min=2.0, max=100.0)
    totalHeightTower = bpy.props.FloatProperty(name="TotalHeight", description="Total Height of the tower", default=20.0, min=5.0, max=100.0)
    crenauxTower = bpy.props.BoolProperty(name="Crenaux", default=True)
    poteauxTower = bpy.props.BoolProperty(name="Poteaux", default=False)
    doorTower = bpy.props.BoolProperty(name="Porte", default=False)
    rembardeTower = bpy.props.BoolProperty(name="Rembarde", default=False)


class panelCastleGeneratorGround(bpy.types.Panel):
    bl_label = "Castle Generator - Ground"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    def draw(self, context):
        layout = self.layout
        castlegenerator = bpy.context.window_manager.castlegenerator
        # Ground
        layout.label("Ground", icon='ACTION')
        row = layout.row()
        box = row.box()
        box.operator("castlegenerator.generateground", text="Generate ground", icon="BRUSH_ADD")

class panelCastleGeneratorWall(bpy.types.Panel):
    bl_label = "Castle Generator - Wall"
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
            box.operator("castlegenerator.generatecrenels", text="Generate crenels", icon="UNLINKED")
            
            # Door
            layout.label("Door", icon='UV_ISLANDSEL')
            row = layout.row()
            box = row.box()
            box.prop(castlegenerator, 'doorHeight')
            box.prop(castlegenerator, 'doorWidth')
            box.prop(castlegenerator, 'doorPositionPercent')
            box.operator("castlegenerator.generatedoor", text="Generate door", icon="SNAP_FACE")

class panelCastleGeneratorTower(bpy.types.Panel):
    bl_label = "Castle Generator - Tower"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    def draw(self, context):
        layout = self.layout
        castlegenerator = bpy.context.window_manager.castlegenerator
        
        # Tower
        layout.label("Tower", icon='PINNED')
        row = layout.row()
        box = row.box()
        box.prop(castlegenerator, 'numVertsTower')
        box.prop(castlegenerator, 'radiusTower')
        box.prop(castlegenerator, 'totalHeightTower')
        box.prop(castlegenerator, 'crenauxTower')
        box.prop(castlegenerator, 'poteauxTower')
        box.prop(castlegenerator, 'doorTower')
        box.prop(castlegenerator, 'rembardeTower')
        box.operator("castlegenerator.generatetowers", text="Generate tower", icon="MESH_CYLINDER")

class panelCastleGeneratorCapture(bpy.types.Panel):
    bl_label = "Castle Generator - Capture"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    def draw(self, context):
        layout = self.layout
        castlegenerator = bpy.context.window_manager.castlegenerator
        
        # Capture
        layout.label("Capture", icon='RENDER_REGION')
        row = layout.row()
        box = row.box()
        box.operator("castlegenerator.positioncapture", text="Position capture", icon="SCENE")


class OBJECT_OT_GenerateGround(bpy.types.Operator):
    bl_idname = "castlegenerator.generateground"
    bl_label = "Generate ground"
    def execute(self, context):
        GroundGenerator()
        return{'FINISHED'}

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

class OBJECT_OT_GenerateDoor(bpy.types.Operator):
    bl_idname = "castlegenerator.generatedoor"
    bl_label = "Generate door"
    def execute(self, context):
        castlegenerator = bpy.context.window_manager.castlegenerator
        objects = [obj for obj in bpy.context.scene.objects if obj.select]
		
        if len(objects) == 1 and objects[0] != None:
            DoorGenerator(objects[0], castlegenerator.doorHeight, castlegenerator.doorWidth, castlegenerator.doorPositionPercent)
        return{'FINISHED'}

class OBJECT_OT_GenerateTowers(bpy.types.Operator):
    bl_idname = "castlegenerator.generatetowers"
    bl_label = "Generate towers"
    def execute(self, context):
        castlegenerator = bpy.context.window_manager.castlegenerator
        
        TowerGenerator(bpy.context.scene.cursor_location.copy(), castlegenerator.numVertsTower, castlegenerator.radiusTower, castlegenerator.totalHeightTower, castlegenerator.crenauxTower, castlegenerator.poteauxTower, castlegenerator.doorTower, castlegenerator.rembardeTower)
        return{'FINISHED'}

class OBJECT_OT_PositionCapture(bpy.types.Operator):
    bl_idname = "castlegenerator.positioncapture"
    bl_label = "Position capture"
    def execute(self, context):
        castlegenerator = bpy.context.window_manager.castlegenerator
        
        # Add Camera to scene and set to view
        removeFromCollection(bpy.data.cameras, 'Camera')
        bpy.ops.object.camera_add()
        bpy.data.cameras["Camera"].clip_end = 1000.0
        bpy.data.objects["Camera"].name = "tmp.camera"
        bpy.ops.view3d.camera_to_view()
        bpy.data.worlds[0].light_settings.use_ambient_occlusion = True
        bpy.data.worlds[0].light_settings.use_environment_light = True
        bpy.context.scene.render.use_edge_enhance = True
        bpy.ops.render.render()
        
        return{'FINISHED'}


classes = [propertiesCastleGenerator, panelCastleGeneratorGround, panelCastleGeneratorWall, panelCastleGeneratorTower, panelCastleGeneratorCapture, OBJECT_OT_GenerateGround, OBJECT_OT_GenerateWalls, OBJECT_OT_GenerateCrenels, OBJECT_OT_GenerateDoor, OBJECT_OT_GenerateTowers, OBJECT_OT_PositionCapture]

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