import bpy
import math
import mathutils

sizeDoor = 3
lengthDoor = 2
widthDoor = 6
pointA = mathutils.Vector((0, 0, 0))
pointB = mathutils.Vector((5, 10, 10))
percent = 50
sizeCircleBase = 2

# Create the door
bpy.ops.mesh.primitive_circle_add()

# Deselect all the vertices
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')

# Delete the bottom vertices
object = createMesh("DoorGenerator", (0,0,0), [(-lengthDoor/2,0,0), (lengthDoor/2,0,0)], [1,2], [])
object = bpy.context.active_object
object.name = "DoorGenerator"
nbVertices = int(len(object.data.vertices)/2)
verticesDelete = [x for x in object.data.vertices if x.index != 0 and x.index > len(object.data.vertices)/2]
for vertex in verticesDelete:
    vertex.select = True
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.delete()
bpy.ops.mesh.select_all(action = 'SELECT')
bpy.ops.transform.rotate(value=math.radians(90.0), axis=(0.0, 1.0, 0.0))
bpy.ops.transform.translate(value=(0.5 - widthDoor / 2, 0, 0.5 + sizeDoor))
bpy.ops.object.mode_set(mode='OBJECT')
nbVertices = len(object.data.vertices) - 1

# Extend the vertices and edges
object.data.vertices.add(2)
object.data.edges.add(3)

# Add the vertices and edges
object.data.vertices[-2].co = object.data.vertices[0].co.copy()
object.data.vertices[-2].co.z = 0
object.data.vertices[-1].co = object.data.vertices[nbVertices].co.copy()
object.data.vertices[-1].co.z = 0
object.data.edges[-1].vertices = [object.data.vertices[0].index, object.data.vertices[-2].index]
object.data.edges[-2].vertices = [object.data.vertices[-2].index, object.data.vertices[-1].index]
object.data.edges[-3].vertices = [object.data.vertices[-1].index, object.data.vertices[nbVertices].index]

# Do the extrude
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action = 'SELECT')
#bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(widthDoor, 0, 0)})
#bpy.ops.mesh.select_all(action = 'DESELECT')
#bpy.ops.mesh.normals_make_consistent()
bpy.ops.object.mode_set(mode='OBJECT')
#if object.data.polygons[11].normal.x < 0:
#    bpy.ops.object.mode_set(mode='EDIT')
#    bpy.ops.mesh.flip_normals()
#    bpy.ops.object.mode_set(mode='OBJECT')

# Position the door
#bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action = 'SELECT')
locationObject = ((pointA.x + ((pointB.x - pointA.x) * percent) / 100), (pointA.y + ((pointB.y - pointA.y) * percent) / 100), (pointA.z + ((pointB.z - pointA.z) * percent) / 100))
#bpy.ops.transform.translate(value=(locationObject))
object.location = locationObject
#bpy.context.scene.cursor_location = locationObject
bpy.ops.object.mode_set(mode='OBJECT')

# Orientation of the door
vector = pointB - pointA
angleTheta = -math.atan2(math.fabs(vector.x), math.fabs(vector.y)) * math.copysign(1, vector.x * vector.y)
newVector = mathutils.Matrix.Rotation(-angleTheta, 3, 'Z').transposed() * vector
anglePhi = math.atan2(math.fabs(newVector.x), math.fabs(newVector.z)) * math.copysign(1, vector.y * vector.z)
bpy.ops.transform.rotate(value=anglePhi, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL')
bpy.ops.transform.rotate(value=angleTheta, axis=(0, 0, 1), constraint_axis=(False, False, True), constraint_orientation='GLOBAL')
bpy.ops.object.transform_apply(rotation=True)