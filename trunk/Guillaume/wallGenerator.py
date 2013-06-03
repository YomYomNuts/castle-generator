import bpy
import mathutils
import math
from utils import *
from math import *

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
            listFaces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 2, 6, 4), (1, 5, 7, 3), (0, 4, 5, 1), (2, 3, 7, 6)]
            
            # Create the meshes
            object = createMesh("WallGenerator", (0,0,0), verticesObject1 + verticesObject2, listEdges, listFaces)
            bpy.context.scene.objects.active = object
            object.select = True
            
            # Create the vertex groups
            i = 0
            while i < 4:
                bpy.ops.object.vertex_group_add()
                object.vertex_groups[i].name = str(i)
                i += 1
            
            # Add the edges to vertex groups
            object.vertex_groups[0].add([2, 6], 1, 'ADD')
            object.vertex_groups[1].add([3, 7], 1, 'ADD')
            object.vertex_groups[2].add([2, 3], 1, 'ADD')
            object.vertex_groups[3].add([6, 7], 1, 'ADD')


# Class CrenelGenerator
class CrenelGenerator:
    def __init__(self, object, indexVertexGroup=3, lowWallHeight=1, lowWallWidth=0.5, beginByCrenel=True, inverseSensCreation=False, crenelLength=0.4, merlonLength=0.6, merlonHeight=0.5):
        self.object = object
        self.indexVertexGroup = indexVertexGroup
        self.lowWallHeight = lowWallHeight
        self.lowWallWidth = lowWallWidth
        self.beginByCrenel = beginByCrenel
        self.inverseSensCreation = inverseSensCreation
        self.crenelLength = crenelLength
        self.merlonLength = merlonLength
        self.merlonHeight = merlonHeight
        listIndexVerticesCreated = self.createLowWall()
        self.createCrenelMerlon(listIndexVerticesCreated)
    
    def createLowWall(self):
        # Select the vertices
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        self.object.vertex_groups.active_index = self.indexVertexGroup
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.mode_set(mode='OBJECT')
        verticesIndex = [vertexSearch.index for vertexSearch in self.object.data.vertices if vertexSearch.select == True]
        
        # Do the low wall
        i = 0
        while i < len(verticesIndex):
            indexVertex = verticesIndex[i]
            
            # Take the vertex reference
            vertexReference = mathutils.Vector((0, 0, 0))
            if indexVertex == 2 and self.indexVertexGroup == 0:
                vertexReference = self.object.data.vertices[3].co
            elif indexVertex == 2 and self.indexVertexGroup == 2:
                vertexReference = self.object.data.vertices[6].co
            elif indexVertex == 3 and self.indexVertexGroup == 1:
                vertexReference = self.object.data.vertices[2].co
            elif indexVertex == 3 and self.indexVertexGroup == 2:
                vertexReference = self.object.data.vertices[7].co
            elif indexVertex == 6 and self.indexVertexGroup == 0:
                vertexReference = self.object.data.vertices[7].co
            elif indexVertex == 6 and self.indexVertexGroup == 3:
                vertexReference = self.object.data.vertices[2].co
            elif indexVertex == 7 and self.indexVertexGroup == 1:
                vertexReference = self.object.data.vertices[6].co
            elif indexVertex == 7 and self.indexVertexGroup == 3:
                vertexReference = self.object.data.vertices[3].co
            
            # Get the vertice of intersection
            verticesObject = intersectionCircleLine(vertexReference, self.object.data.vertices[indexVertex].co, self.lowWallWidth)
            
            if verticesObject[0] != None and verticesObject[1] != None:
                # Get the good vertice
                selectedVertex = getVertexInBox(False, self.object.data.vertices[indexVertex].co, vertexReference, verticesObject[0], verticesObject[1])
                
                if selectedVertex != None:
                    # Extend the vertices and the edges
                    self.object.data.vertices.add(1)
                    self.object.data.edges.add(1)
                    
                    # Add the vertices and edges
                    self.object.data.vertices[-1].co = (selectedVertex.x, selectedVertex.y, selectedVertex.z)
                    self.object.data.edges[-1].vertices = [indexVertex, self.object.data.vertices[-1].index]
            i += 1
        
        # Add an edge
        self.object.data.edges.add(1)
        self.object.data.edges[-1].vertices = [self.object.data.vertices[-1].index, self.object.data.vertices[-2].index]
        
        # Define utils variables
        listVertice = [verticesIndex[1], self.object.data.vertices[-1].index, self.object.data.vertices[-2].index, verticesIndex[0]]
        listIndexVerticesCreated = [self.object.data.vertices[-2].index, self.object.data.vertices[-1].index]
        
        # Do the extrude
        if self.lowWallHeight > 0:
            manualExtrude(self.object, listVertice, mathutils.Vector((0, 0, self.lowWallHeight)))
        
        return listIndexVerticesCreated
    
    def createCrenelMerlon(self, listIndexVerticesLowWall):
        # Select the vertices
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        self.object.vertex_groups.active_index = self.indexVertexGroup
        bpy.ops.object.vertex_group_select()
        bpy.ops.object.mode_set(mode='OBJECT')
        verticesSelected = [vertexSearch for vertexSearch in self.object.data.vertices if vertexSearch.select == True]
        
        # Take the vertices are in the top of the low wall
        vertexTopLowWall = [-1, -1, -1, -1]
        for vertex in self.object.data.vertices:
            if compareTwoCoVertex(vertex.co, (verticesSelected[0].co[0], verticesSelected[0].co[1], verticesSelected[0].co[2] + self.lowWallHeight)):
                vertexTopLowWall[0] = vertex.index
            if compareTwoCoVertex(vertex.co, (verticesSelected[1].co[0], verticesSelected[1].co[1], verticesSelected[1].co[2] + self.lowWallHeight)):
                vertexTopLowWall[1] = vertex.index
            if compareTwoCoVertex(vertex.co, (self.object.data.vertices[listIndexVerticesLowWall[0]].co[0], self.object.data.vertices[listIndexVerticesLowWall[0]].co[1], self.object.data.vertices[listIndexVerticesLowWall[0]].co[2] + self.lowWallHeight)):
                vertexTopLowWall[2] = vertex.index
            if compareTwoCoVertex(vertex.co, (self.object.data.vertices[listIndexVerticesLowWall[1]].co[0], self.object.data.vertices[listIndexVerticesLowWall[1]].co[1], self.object.data.vertices[listIndexVerticesLowWall[1]].co[2] + self.lowWallHeight)):
                vertexTopLowWall[3] = vertex.index
        
        # Define the first and the second length
        if self.beginByCrenel:
            length1 = self.crenelLength
            length2 = self.merlonLength
        else:
            length1 = self.merlonLength
            length2 = self.crenelLength
        
        # Get the first vertices of merlon and crenel
        lastVertice = []
        if self.inverseSensCreation:
            previousFirst = vertexTopLowWall[1]
            lastVertice.append(vertexTopLowWall[0])
            verticesFirst = self.calculateVerticesCrenelMerlon(self.object.data.vertices[vertexTopLowWall[1]].co, self.object.data.vertices[vertexTopLowWall[0]].co, length1 , length2)
        else:
            previousFirst = vertexTopLowWall[0]
            lastVertice.append(vertexTopLowWall[1])
            verticesFirst = self.calculateVerticesCrenelMerlon(self.object.data.vertices[vertexTopLowWall[0]].co, self.object.data.vertices[vertexTopLowWall[1]].co, length1 , length2)
        
        # Define the size of the merlon and crenel for this other side
        coefficient = length2 / length1
        totalSize = sqrt((self.object.data.vertices[vertexTopLowWall[3]].co[0] - self.object.data.vertices[vertexTopLowWall[2]].co[0]) ** 2 + (self.object.data.vertices[vertexTopLowWall[3]].co[1] - self.object.data.vertices[vertexTopLowWall[2]].co[1]) ** 2)
        if len(verticesFirst) % 2 == 0:
            newLength1 = totalSize / (len(verticesFirst) / 2 + len(verticesFirst) * coefficient / 2)
        else:
            newLength1 = totalSize / ((len(verticesFirst) + 1) / 2 + (len(verticesFirst) + 1) * coefficient / 2)
        newLength2 = newLength1 * coefficient
        
        # Get the seconds vertices of merlon and crenel
        if self.inverseSensCreation:
            previousSecond = vertexTopLowWall[3]
            lastVertice.append(vertexTopLowWall[2])
            verticesSecond = self.calculateVerticesCrenelMerlon(self.object.data.vertices[vertexTopLowWall[3]].co, self.object.data.vertices[vertexTopLowWall[2]].co, newLength1 , newLength2)
        else:
            previousSecond = vertexTopLowWall[2]
            lastVertice.append(vertexTopLowWall[3])
            verticesSecond = self.calculateVerticesCrenelMerlon(self.object.data.vertices[vertexTopLowWall[2]].co, self.object.data.vertices[vertexTopLowWall[3]].co, newLength1 , newLength2)
        
        # Creation of merlon and crenel
        index = 0
        while index <= len(verticesSecond):
            # Deselect all the vertices
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Select the previous vertices
            self.object.data.vertices[previousFirst].select = True
            self.object.data.vertices[previousSecond].select = True
            
            if index != len(verticesSecond):
                # Extend the vertices and edges
                self.object.data.vertices.add(2)
                self.object.data.edges.add(3)
                
                # Add the vertices and edges
                self.object.data.vertices[-2].co = (verticesFirst[index].x, verticesFirst[index].y, verticesFirst[index].z)
                self.object.data.vertices[-1].co = (verticesSecond[index].x, verticesSecond[index].y, verticesSecond[index].z)
                self.object.data.edges[-1].vertices = [previousFirst, self.object.data.vertices[-2].index]
                self.object.data.edges[-2].vertices = [self.object.data.vertices[-2].index, self.object.data.vertices[-1].index]
                self.object.data.edges[-3].vertices = [previousSecond, self.object.data.vertices[-1].index]
                listVertice = [previousSecond, self.object.data.vertices[-1].index, self.object.data.vertices[-2].index, previousFirst]
                
                # Add a face
                createFace(self.object, [previousFirst, self.object.data.vertices[-2].index, self.object.data.vertices[-1].index, previousSecond])
                
                # Change the previous vertices
                previousFirst = self.object.data.vertices[-2].index
                previousSecond = self.object.data.vertices[-1].index
            else:
                # Extend the edges
                self.object.data.edges.add(2)
                self.object.data.edges[-1].vertices = [previousFirst, lastVertice[0]]
                self.object.data.edges[-2].vertices = [previousSecond, lastVertice[1]]
                listVertice = [previousSecond, lastVertice[1], lastVertice[0], previousFirst]
                
                # Add a face
                createFace(self.object, [previousFirst, lastVertice[0], lastVertice[1], previousSecond])
            
            # Do the extrude if it's a merlon
            if self.merlonHeight > 0 and ((self.beginByCrenel and index % 2 == 1) or (not (self.beginByCrenel) and index % 2 == 0)):
                manualExtrude(self.object, listVertice, mathutils.Vector((0, 0, self.merlonHeight)))
            
            index += 1
    
    def calculateVerticesCrenelMerlon(self, firstVertex, lastVertex, length1, length2):
        listVertices = []
        previousVertex = firstVertex
        finish = False
        index = 0
        while not (finish):
            # Defines the size
            if index % 2 == 0:
                length = length1
            else:
                length = length2
            
            # Get the vertice of intersection
            verticesObject = intersectionCircleLine(lastVertex, previousVertex, length)
            
            if verticesObject[0] != None and verticesObject[1] != None:
                # Get the good vertice
                selectedVertex = getVertexInBox(True, previousVertex, lastVertex, verticesObject[0], verticesObject[1])
                
                if selectedVertex != None:
                    listVertices.append(selectedVertex)
                    previousVertex = selectedVertex
                else:
                    finish = True
            index += 1
        return listVertices

# Main
#objects = [obj for obj in bpy.context.scene.objects if obj.select]
#WallGenerator(objects[0], objects[1])
#CrenelGenerator(objects[0], 1)
#CrenelGenerator(objects[0], 2)
#CrenelGenerator(objects[0], 3)