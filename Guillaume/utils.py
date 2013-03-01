import bpy
import mathutils
import math

def createMesh(name, origin, verts, edges, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True
    # Link object to scene
    bpy.context.scene.objects.link(ob)
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, edges, faces)
    # Update mesh with new data
    me.update(calc_edges=True)
    return ob

# Defines the position of intersection into a circle and a line
def intersectionCircleLine(initialPosition, destinationPosition, widthWall):
    if initialPosition.x <= destinationPosition.x + 0.0000001 and initialPosition.x >= destinationPosition.x - 0.0000001:
        x = destinationPosition.x
        y1 = destinationPosition.y + widthWall
        y2 = destinationPosition.y - widthWall
        z = destinationPosition.z
        return (mathutils.Vector((x, y1, z)), mathutils.Vector((x, y2, z)))
    elif initialPosition.y <= destinationPosition.y + 0.0000001 and initialPosition.y >= destinationPosition.y - 0.0000001:
        x1 = destinationPosition.x + widthWall
        x2 = destinationPosition.x - widthWall
        y = destinationPosition.y
        z = destinationPosition.z
        return (mathutils.Vector((x1, y, z)), mathutils.Vector((x2, y, z)))
    else:
        # y = ax + b
        a = (initialPosition.y - destinationPosition.y) / (initialPosition.x - destinationPosition.x)
        b = destinationPosition.y - a * destinationPosition.x
        
        # Ax**2 + Bx + C = 0
        A = 1 + a ** 2
        B = - 2 * destinationPosition.x + 2 * a * b - 2 * a * destinationPosition.y
        C = destinationPosition.x ** 2 + destinationPosition.y ** 2 + b ** 2 - 2 * b * destinationPosition.y - widthWall ** 2
        
        #Determine the delta
        delta = B ** 2 - 4 * A * C
        
        if delta >= 0:
            #Get the position
            x1 = (- B + math.sqrt(delta)) / (2 * A)
            y1 = a * x1 + b
            x2 = (- B - math.sqrt(delta)) / (2 * A)
            y2 = a * x2 + b
            z = destinationPosition.z
            
            return (mathutils.Vector((x1, y1, z)), mathutils.Vector((x2, y2, z)))
    return (None, None)
    
# Defines the position of intersection into two circles
def intersectionCircleCircle(pointA, radiusA, pointB, radiusB):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    z = pointB.z
    if pointA.y != pointB.y:
        # Equation Ax**2 + Bx + C = 0
        N = (radiusB ** 2 - radiusA ** 2 - pointB.x ** 2 + pointA.x ** 2 - pointB.y ** 2 + pointA.y ** 2) / (2 * (pointA.y - pointB.y))
        H = ((pointA.x - pointB.x) / (pointA.y - pointB.y))
        A = H ** 2 + 1
        B = 2 * pointA.y * H - 2 * N * H - 2 * pointA.x
        C = pointA.x ** 2 + pointA.y ** 2 + N ** 2 - radiusA ** 2 - 2 * pointA.y * N
        
        # Determine the delta
        delta = sqrt(B ** 2 - 4 * A * C)
        
        # Get the 2 solutions
        x1 = (- B + delta) / (2 * A)
        y1 = N - x1 * H
        x2 = (- B - delta) / (2 * A)
        y2 = N - x2 * H
    else:
        #Equation Ay**2 + By + C = 0
        x1 = (radiusB ** 2 - radiusA ** 2 - pointB.x ** 2 + pointA.x ** 2) / (2 * (pointA.x - pointB.x))
        x2 = x1
        A = 1
        B = - 2 * pointB.y
        C = pointB.x ** 2 + x1 ** 2 - 2 * pointB.x * x1 + pointB.y ** 2 - radiusB ** 2
        
        # Determine the delta
        delta = sqrt(B ** 2 - 4 * A * C)
        
        # Get the 2 solutions
        y1 = (- B + delta) / (2 * A)
        y2 = (- B - delta) / (2 * A)
    
    #Get the position
    return (mathutils.Vector((x1, y1, z)), mathutils.Vector((x2, y2, z)))

# Do the rotation around a point "origin" of point "position" an angle "angle"
def getPositionRotationY(origin, position, angle):
    x = math.cos(angle) * position.x - math.sin(angle) * position.y + origin.x - math.cos(angle) * origin.x + math.sin(angle) * origin.y
    y = math.sin(angle) * position.x + math.cos(angle) * position.y + origin.y - math.sin(angle) * origin.x - math.cos(angle) * origin.y
    z = position.z
    
    return mathutils.Vector((x, y, z))

# Defines the visibility of a point
def visible(self, vertex, previousVertex, previousPreviousVertex):
    segmentActuel = mathutils.Vector((previousPreviousVertex.x - previousVertex.x, previousPreviousVertex.y - previousVertex.y, 0))
    segmentPrecedent = mathutils.Vector((vertex.x - previousVertex.x, vertex.y - previousVertex.y, 0))
    
    # Orientation of the polygon, it's everytime positive
    signOrientation = 1
    return signOrientation * (segmentActuel.x * segmentPrecedent.y - segmentActuel.y * segmentPrecedent.x)