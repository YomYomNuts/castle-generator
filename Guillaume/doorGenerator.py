import bpy
import math
import mathutils
from utils import *

# Class DoorGenerator
class DoorGenerator:
    def __init__(self, objectInput, heightDoor=2, widthDoor=2, percent=70):
        # Check if a face are select
        bpy.ops.object.mode_set(mode='OBJECT')
        faceSelect = [x for x in objectInput.data.polygons if x.select == True]
        if len(faceSelect) > 0:
            # Get the important points
            verticesIndex = [x for x in faceSelect[0].vertices]
            indexPointA = objectInput.data.vertices[verticesIndex[0]].index
            indexTopPointA = objectInput.data.vertices[verticesIndex[0]].index
            indexPointB = objectInput.data.vertices[verticesIndex[0]].index
            indexPointC = objectInput.data.vertices[verticesIndex[0]].index
            pointA = objectInput.data.vertices[verticesIndex[0]].co.copy()
            pointB = objectInput.data.vertices[verticesIndex[0]].co.copy()
            pointC = objectInput.data.vertices[verticesIndex[0]].co.copy()
            # Find the point A
            for vertexIndex in verticesIndex:
                if pointA.z > objectInput.data.vertices[vertexIndex].co.z:
                    pointA = objectInput.data.vertices[vertexIndex].co.copy()
                    indexPointA = objectInput.data.vertices[vertexIndex].index
                if pointB.z < objectInput.data.vertices[vertexIndex].co.z:
                    pointB = objectInput.data.vertices[vertexIndex].co.copy()
            # Find the point B
            for vertexIndex in verticesIndex:
                if pointB.z > objectInput.data.vertices[vertexIndex].co.z and not pointA.x == objectInput.data.vertices[vertexIndex].co.x and not pointA.y == objectInput.data.vertices[vertexIndex].co.y:
                    pointB = objectInput.data.vertices[vertexIndex].co.copy()
                    indexPointB = objectInput.data.vertices[vertexIndex].index
                if pointA.z < objectInput.data.vertices[vertexIndex].co.z and pointA.x == objectInput.data.vertices[vertexIndex].co.x and pointA.y == objectInput.data.vertices[vertexIndex].co.y:
                    indexTopPointA = objectInput.data.vertices[vertexIndex].index
            # Find the point C
            for edge in objectInput.data.edges:
                if indexPointA in edge.vertices and not indexTopPointA in edge.vertices and not indexPointB in edge.vertices:
                    indexPointC = [x for x in edge.vertices if not x == indexPointA][0]
            pointC = objectInput.data.vertices[indexPointC].co.copy()
            
            pointA = objectInput.matrix_world * pointA
            pointB = objectInput.matrix_world * pointB
            pointC = objectInput.matrix_world * pointC
            
            # Deselect the object
            objectInput.select = False
            
            # Create the door
            object = createMesh("DoorGenerator", (0,0,0), [mathutils.Vector((-widthDoor/2,0,0)), mathutils.Vector((widthDoor/2,0,0))], [(1,0)], [])
            bpy.context.scene.objects.active = object
            object.select = True
            
            # Position the door
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            object.location = mathutils.Vector(((pointA.x + ((pointB.x - pointA.x) * percent) / 100), (pointA.y + ((pointB.y - pointA.y) * percent) / 100), (pointA.z + ((pointB.z - pointA.z) * percent) / 100)))
            bpy.context.scene.cursor_location = object.location.copy()
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Orientation of the door
            vector = pointB - pointA
            angleTheta = math.atan2(math.fabs(vector.y), math.fabs(vector.x)) * math.copysign(1, vector.x * vector.y)
            newVector = mathutils.Matrix.Rotation(-angleTheta, 3, 'Z') * vector
            anglePhi = -math.atan2(math.fabs(newVector.z), math.fabs(newVector.x)) * math.copysign(1, vector.x * vector.z)
            bpy.ops.transform.rotate(value=anglePhi, axis=(0, 1, 0), constraint_axis=(False, True, False), constraint_orientation='GLOBAL')
            bpy.ops.transform.rotate(value=angleTheta, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL')
            bpy.ops.object.transform_apply(rotation=True)
            
            # Finish the door
            # Extend the vertices and edges
            bpy.ops.object.mode_set(mode='OBJECT')
            object.data.vertices.add(5)
            object.data.edges.add(6)
            # Add the vertices and edges
            object.data.vertices[-5].co = object.data.vertices[0].co.copy()
            object.data.vertices[-5].co.z = object.data.vertices[-2].co.z + heightDoor
            object.data.vertices[-4].co = object.data.vertices[1].co.copy()
            object.data.vertices[-4].co.z = object.data.vertices[-1].co.z + heightDoor
            object.data.vertices[-3].co = (object.data.vertices[-5].co + object.data.vertices[-4].co) / 2
            object.data.vertices[-3].co.z = object.data.vertices[-3].co.z + heightDoor * 3/5
            object.data.vertices[-2].co = (object.data.vertices[-5].co + object.data.vertices[-3].co) / 2
            object.data.vertices[-2].co.z = object.data.vertices[-2].co.z + heightDoor * 1/5
            object.data.vertices[-1].co = (object.data.vertices[-3].co + object.data.vertices[-4].co) / 2
            object.data.vertices[-1].co.z = object.data.vertices[-1].co.z + heightDoor * 1/5
            object.data.edges[-1].vertices = [0, 2]
            object.data.edges[-2].vertices = [2, 5]
            object.data.edges[-3].vertices = [5, 4]
            object.data.edges[-4].vertices = [4, 6]
            object.data.edges[-5].vertices = [6, 3]
            object.data.edges[-6].vertices = [3, 1]
            
            # Do the extrude
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(pointC - pointA)*1.02, "constraint_orientation":'GLOBAL'})
            bpy.ops.mesh.normals_make_consistent()
            bpy.ops.object.mode_set(mode='OBJECT')
            translateValue = (pointC - pointA)*-0.01
            translateValue.z = translateValue.z + math.copysign(0.0001,translateValue.z)
            bpy.ops.transform.translate(value=(translateValue.x, translateValue.y, translateValue.z), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=False)
            bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
            
            # Do the difference with boolean modifier
            doDifferenceBooleanModifier(objectInput, object)