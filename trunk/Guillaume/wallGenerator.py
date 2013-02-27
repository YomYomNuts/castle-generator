import bpy
import random
import mathutils
from math import*
from utils import *

# Class WallGenerator
class WallGenerator:
    def __init__(self, positionX=0, positionY=0, distance=20, minimalWallLenght=20, maximalWallLenght=26, widthWall=4, minimalHeightWall=10, maximalHeightWall=15):
        self.positionCenter = mathutils.Vector((positionX, positionY, 0))
        self.distance = distance
        self.minimalWallLenght = minimalWallLenght
        self.maximalWallLenght = maximalWallLenght
        self.widthWall = widthWall
        self.minimalHeightWall = minimalHeightWall
        self.maximalHeightWall = maximalHeightWall
        self.listEdges = []
        self.listFaces = []
        self.positionsExternalWall = []
        self.positionsInternalWall = []
        tempVector = mathutils.Vector((self.positionCenter.x + self.distance, self.positionCenter.y, 0))
        self.createInternalWall(tempVector, random.uniform(0, self.distance * 2))
        self.createExternalWall()
        object = createMesh("Test", (0,0,0), self.positionsInternalWall + self.positionsExternalWall, self.listEdges, self.listFaces)
        self.createWallHeight(object)
    
    # Defines the position of the point internal of the wall
    def createInternalWall(self, initialPosition, lengthWall):
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        if self.positionCenter.y != initialPosition.y:
            # Equation Ax**2 + Bx + C = 0
            N = (lengthWall ** 2 - self.distance ** 2 - initialPosition.x ** 2 + self.positionCenter.x ** 2 - initialPosition.y ** 2 + self.positionCenter.y ** 2) / (2 * (self.positionCenter.y - initialPosition.y))
            H = ((self.positionCenter.x - initialPosition.x) / (self.positionCenter.y - initialPosition.y))
            A = H ** 2 + 1
            B = 2 * self.positionCenter.y * H - 2 * N * H - 2 * self.positionCenter.x
            C = self.positionCenter.x ** 2 + self.positionCenter.y ** 2 + N ** 2 - self.distance ** 2 - 2 * self.positionCenter.y * N
            
            # Determine the delta
            delta = sqrt(B ** 2 - 4 * A * C)
            
            # Get the 2 solutions
            x1 = (- B + delta) / (2 * A)
            y1 = N - x1 * H
            x2 = (- B - delta) / (2 * A)
            y2 = N - x2 * H
        else:
            #Equation Ay**2 + By + C = 0
            x1 = (lengthWall ** 2 - self.distance ** 2 - initialPosition.x ** 2 + self.positionCenter.x ** 2) / (2 * (self.positionCenter.x - initialPosition.x))
            x2 = x1
            A = 1
            B = - 2 * initialPosition.y
            C = initialPosition.x ** 2 + x1 ** 2 - 2 * initialPosition.x * x1 + initialPosition.y ** 2 - lengthWall ** 2
            
            # Determine the delta
            delta = sqrt(B ** 2 - 4 * A * C)
            
            # Get the 2 solutions
            y1 = (- B + delta) / (2 * A)
            y2 = (- B - delta) / (2 * A)
        
        #Get the position
        positionWall = mathutils.Vector((x1, y1, 0))
        
        # Verify if the position is visible by the others points
        if self.visible(positionWall, initialPosition, self.positionCenter) < 0:
            # Change position
            positionWall = mathutils.Vector((x2, y2, 0))
        
        # Add the point
        if len(self.positionsInternalWall) < 3 or not (self.visible(positionWall, self.positionsInternalWall[0], self.positionCenter) > 0 and self.visible(initialPosition, self.positionsInternalWall[0], self.positionCenter) < 0):
            # Do the edges
            if len(self.positionsInternalWall) > 0:
                self.listEdges.append((len(self.positionsInternalWall) - 1, len(self.positionsInternalWall)))
            
            self.positionsInternalWall.append(positionWall)
            self.createInternalWall(positionWall, random.uniform(self.minimalWallLenght, self.maximalWallLenght))
        else:
            self.listEdges.append((len(self.positionsInternalWall) - 1, 0))
    
    # Defines the visibility of a point
    def visible(self, vertex, previousVertex, previousPreviousVertex):
        segmentActuel = mathutils.Vector((previousPreviousVertex.x - previousVertex.x, previousPreviousVertex.y - previousVertex.y, 0))
        segmentPrecedent = mathutils.Vector((vertex.x - previousVertex.x, vertex.y - previousVertex.y, 0))
        
        # Orientation of the polygon, it's everytime positive
        signOrientation = 1
        return signOrientation * (segmentActuel.x * segmentPrecedent.y - segmentActuel.y * segmentPrecedent.x)
    
    # Defines the position of the point internal of the wall
    def createExternalWall(self):
        index = 0
        for pos in self.positionsInternalWall:
            if not (pos.x == self.positionCenter.x and pos.y == self.positionCenter.y):
                H = (pos.x - self.positionCenter.x) ** 2
                x1 = sqrt(((self.distance + self.widthWall) ** 2 * H) / (H + (pos.y - self.positionCenter.y) ** 2))
                y1 = x1 * (pos.y - self.positionCenter.y) / (pos.x - self.positionCenter.x)
                x2 = - x1
                y2 = x2 * (pos.y - self.positionCenter.y) / (pos.x - self.positionCenter.x)
                
                # Do the edges
                # Edges between external vertex
                if len(self.positionsExternalWall) > 0:
                    self.listEdges.append((len(self.positionsInternalWall) + len(self.positionsExternalWall) - 1, len(self.positionsInternalWall) + len(self.positionsExternalWall)))
                # Edges between internal and external vertex
                self.listEdges.append((index, len(self.positionsInternalWall) + len(self.positionsExternalWall)))
                
                # Do the faces
                if len(self.positionsExternalWall) > 0:
                    self.listFaces.append((index - 1, index, len(self.positionsInternalWall) + len(self.positionsExternalWall), len(self.positionsInternalWall) + len(self.positionsExternalWall) - 1))
                
                # Add the new vertex
                if self.positionCenter.x > pos.x:
                    if self.positionCenter.y > pos.y:
                        if self.positionCenter.x > x1 and self.positionCenter.y > y1:
                            self.positionsExternalWall.append(mathutils.Vector((x1, y1, 0)))
                        else:
                            self.positionsExternalWall.append(mathutils.Vector((x2, y2, 0)))
                    elif self.positionCenter.y < pos.y:
                        if self.positionCenter.x > x1 and self.positionCenter.y < y1:
                            self.positionsExternalWall.append(mathutils.Vector((x1, y1, 0)))
                        else:
                            self.positionsExternalWall.append(mathutils.Vector((x2, y2, 0)))
                    else:
                        if self.positionCenter.x > x1:
                            self.positionsExternalWall.append(mathutils.Vector((x1, y1, 0)))
                        else:
                            self.positionsExternalWall.append(mathutils.Vector((x2, y2, 0)))
                elif self.positionCenter.x < pos.x:
                    if self.positionCenter.y > pos.y:
                        if self.positionCenter.x < x1 and self.positionCenter.y > y1:
                            self.positionsExternalWall.append(mathutils.Vector((x1, y1, 0)))
                        else:
                            self.positionsExternalWall.append(mathutils.Vector((x2, y2, 0)))
                    elif self.positionCenter.y < pos.y:
                        if self.positionCenter.x < x1 and self.positionCenter.y < y1:
                            self.positionsExternalWall.append(mathutils.Vector((x1, y1, 0)))
                        else:
                            self.positionsExternalWall.append(mathutils.Vector((x2, y2, 0)))
                    else:
                        if self.positionCenter.x < x1:
                            self.positionsExternalWall.append(mathutils.Vector((x1, y1, 0)))
                        else:
                            self.positionsExternalWall.append(mathutils.Vector((x2, y2, 0)))
                else:
                    if self.positionCenter.y > pos.y:
                        if self.positionCenter.y > y1:
                            self.positionsExternalWall.append(mathutils.Vector((x1, y1, 0)))
                        else:
                            self.positionsExternalWall.append(mathutils.Vector((x2, y2, 0)))
                    else:
                        if self.positionCenter.y < y1:
                            self.positionsExternalWall.append(mathutils.Vector((x1, y1, 0)))
                        else:
                            self.positionsExternalWall.append(mathutils.Vector((x2, y2, 0)))
            index += 1
        
        # Add the last edges
        self.listEdges.append((len(self.positionsInternalWall) + len(self.positionsExternalWall) - 1, index - 1))
        # Add the last faces
        self.listFaces.append((index - 1, 0, index, len(self.positionsInternalWall) + len(self.positionsExternalWall) - 1))
    
    # Create the wall height
    def createWallHeight(self, object):
        # Active the object
        object.select = True
        bpy.context.scene.objects.active = object
        
        # Deselect all vertex
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        index = 0
        for face in self.listFaces:
            # Select the vertex of a face
            for vertex in object.data.polygons[index].vertices:
                bpy.context.active_object.data.vertices[vertex].select = True
            
            # Do the extrude and after deselect the vertex
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, random.uniform(self.minimalHeightWall, self.maximalHeightWall))})
            bpy.ops.mesh.select_all(action = 'DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            index += 1


wall = WallGenerator()