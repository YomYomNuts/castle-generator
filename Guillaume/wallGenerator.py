import bpy
import mathutils
import math
from utils import *

# Class WallGenerator
class WallGenerator:
    def __init__(self, object1, object2, wallWidth=3, wallHeight=5):
        self.object1 = object1
        self.object2 = object2
        self.wallWidth = wallWidth
        self.wallHeight = wallHeight
        self.createWall()
    
    def createWall(self):
        # Do the rotation for take the good position of the intersection
        location = getPositionRotationY(self.object1.location, self.object2.location, math.pi/2)
        verticesObject1 = intersectionCircleLine(location, self.object1.location, self.wallWidth)
        
        # Do the rotation for take the good position of the intersection
        location = getPositionRotationY(self.object2.location, self.object1.location, math.pi/2)
        verticesObject2 = intersectionCircleLine(location, self.object2.location, self.wallWidth)
        
        # Make the wall
        if verticesObject1[0] != None and verticesObject2 != None:
            # Do the extrude
            verticesObject1 += (mathutils.Vector((verticesObject1[0].x, verticesObject1[0].y, verticesObject1[0].z + self.wallHeight)), mathutils.Vector((verticesObject1[1].x, verticesObject1[1].y, verticesObject1[1].z + self.wallHeight)))
            verticesObject2 += (mathutils.Vector((verticesObject2[0].x, verticesObject2[0].y, verticesObject2[0].z + self.wallHeight)), mathutils.Vector((verticesObject2[1].x, verticesObject2[1].y, verticesObject2[1].z + self.wallHeight)))
            
            # Do the edges
            listEdges = ((0, 1), (0, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 7), (6, 7), (0, 4), (1, 5), (2, 6), (3, 7))
            
            # Do the faces
            listFaces = [(0, 1, 3, 2), (4, 5, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5), (0, 1, 5, 4), (2, 3, 7, 6)]
            
            # Create the meshes
            object = createMesh("WallGenerator", (0,0,0), verticesObject1 + verticesObject2, listEdges, listFaces)
            

obejcts = [obj for obj in bpy.context.scene.objects if obj.select]
WallGenerator(obejcts[0], obejcts[1])