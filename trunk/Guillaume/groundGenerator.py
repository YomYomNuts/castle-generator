import bpy
from utils import *

class GroundGenerator:
    def __init__(self):
        # Find all the vertex that form the ground
        objects = [x for x in bpy.context.scene.objects]
        listVertices = []
        for object in objects:
            if "TOWERGENERATOR" in object.name.upper():
                listVertices.append(object.location)
        
        # Create the meshes
        object = createMesh("GroundGenerator", (0,0,0), listVertices, [], [])
        bpy.context.scene.objects.active = object
        object.select = True
        
        # Do the face
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.mode_set(mode='OBJECT')
        if len(object.data.polygons) > 0 and  object.data.polygons[0].normal.z < 0:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.flip_normals()
            bpy.ops.object.mode_set(mode='OBJECT')