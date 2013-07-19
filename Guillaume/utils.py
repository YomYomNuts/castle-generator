import bpy
import mathutils
import math

# Create a mesh
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

# Create a face
def createFace(object, listIndexVertice):
    nbLoops = len(object.data.loops)
    object.data.loops.add(len(listIndexVertice))
    index = 0
    while index < len(listIndexVertice):
        if index == 0:
            object.data.loops[-index].edge_index = [i.index for i in object.data.edges if [j for j in i.vertices] == [listIndexVertice[len(listIndexVertice)-1], listIndexVertice[index]] or [j for j in i.vertices] == [listIndexVertice[index], listIndexVertice[len(listIndexVertice)-1]]][0]
        else:
            object.data.loops[-index].edge_index = [i.index for i in object.data.edges if [j for j in i.vertices] == [listIndexVertice[index-1], listIndexVertice[index]] or [j for j in i.vertices] == [listIndexVertice[index], listIndexVertice[index-1]]][0]
        object.data.loops[-1].vertex_index = listIndexVertice[index]
        index += 1
    
    object.data.polygons.add(1)
    object.data.polygons[-1].loop_start = nbLoops
    object.data.polygons[-1].loop_total = len(listIndexVertice)
    object.data.polygons[-1].vertices = listIndexVertice

# Defines the position of intersection into a circle and a line without Z
def intersectionCircleLineWithoutZ(pointLinePosition, centreCirclePosition, radiusCircle):
    if pointLinePosition.x <= centreCirclePosition.x + 0.0000001 and pointLinePosition.x >= centreCirclePosition.x - 0.0000001:
        x1 = centreCirclePosition.x
        x2 = centreCirclePosition.x
        y1 = centreCirclePosition.y + radiusCircle
        y2 = centreCirclePosition.y - radiusCircle
        z1 = centreCirclePosition.z
        z2 = centreCirclePosition.z
    elif pointLinePosition.y <= centreCirclePosition.y + 0.0000001 and pointLinePosition.y >= centreCirclePosition.y - 0.0000001:
        x1 = centreCirclePosition.x + radiusCircle
        x2 = centreCirclePosition.x - radiusCircle
        y1 = centreCirclePosition.y
        y2 = centreCirclePosition.y
        z1 = centreCirclePosition.z
        z2 = centreCirclePosition.z
    else:
        # y = ax + b
        a = (pointLinePosition.y - centreCirclePosition.y) / (pointLinePosition.x - centreCirclePosition.x)
        b = centreCirclePosition.y - a * centreCirclePosition.x
        
        # Ax**2 + Bx + C = 0
        A = 1 + a ** 2
        B = - 2 * centreCirclePosition.x + 2 * a * b - 2 * a * centreCirclePosition.y
        C = centreCirclePosition.x ** 2 + centreCirclePosition.y ** 2 + b ** 2 - 2 * b * centreCirclePosition.y - radiusCircle ** 2
        
        # Determine the delta
        delta = B ** 2 - 4 * A * C
        
        if delta >= 0:
            # Get the position
            x1 = (- B + math.sqrt(delta)) / (2 * A)
            y1 = a * x1 + b
            x2 = (- B - math.sqrt(delta)) / (2 * A)
            y2 = a * x2 + b
            z1 = centreCirclePosition.z
            z2 = centreCirclePosition.z
        else:
            return (None, None)
        
    return (mathutils.Vector((x1, y1, z1)), mathutils.Vector((x2, y2, z2)))

# Defines the position of intersection into a circle and a line with Z
def intersectionCircleLineWithZ(pointLinePosition, centreCirclePosition, radiusCircle):
    if pointLinePosition.x <= centreCirclePosition.x + 0.0000001 and pointLinePosition.x >= centreCirclePosition.x - 0.0000001:
        x1 = centreCirclePosition.x
        x2 = centreCirclePosition.x
        y1 = centreCirclePosition.y + radiusCircle
        y2 = centreCirclePosition.y - radiusCircle
        z1 = centreCirclePosition.z
        z2 = centreCirclePosition.z
    elif pointLinePosition.y <= centreCirclePosition.y + 0.0000001 and pointLinePosition.y >= centreCirclePosition.y - 0.0000001:
        x1 = centreCirclePosition.x + radiusCircle
        x2 = centreCirclePosition.x - radiusCircle
        y1 = centreCirclePosition.y
        y2 = centreCirclePosition.y
        z1 = centreCirclePosition.z
        z2 = centreCirclePosition.z
    else:
        # y = ax + b
        a = (pointLinePosition.y - centreCirclePosition.y) / (pointLinePosition.x - centreCirclePosition.x)
        b = centreCirclePosition.y - a * centreCirclePosition.x
        
        # Ax**2 + Bx + C = 0
        A = 1 + a ** 2
        B = - 2 * centreCirclePosition.x + 2 * a * b - 2 * a * centreCirclePosition.y
        C = centreCirclePosition.x ** 2 + centreCirclePosition.y ** 2 + b ** 2 - 2 * b * centreCirclePosition.y - radiusCircle ** 2
        
        # Determine the delta
        delta = B ** 2 - 4 * A * C
        
        if delta >= 0:
            # Get the position
            x1 = (- B + math.sqrt(delta)) / (2 * A)
            y1 = a * x1 + b
            x2 = (- B - math.sqrt(delta)) / (2 * A)
            y2 = a * x2 + b
            z1 = centreCirclePosition.z
            z2 = centreCirclePosition.z
        else:
            return (None, None)
    
    # Calculate the correct z
    if centreCirclePosition.z <= pointLinePosition.z - 0.0000001 or centreCirclePosition.z >= pointLinePosition.z + 0.0000001:                
        if centreCirclePosition.y <= pointLinePosition.y - 0.0000001 or centreCirclePosition.y >= pointLinePosition.y + 0.0000001:
            coefficient = (centreCirclePosition.z - pointLinePosition.z) / (centreCirclePosition.y - pointLinePosition.y)
            z1 = y1 * coefficient + centreCirclePosition.z - coefficient * centreCirclePosition.y
            z2 = y2 * coefficient + centreCirclePosition.z - coefficient * centreCirclePosition.y
        elif centreCirclePosition.x <= pointLinePosition.x - 0.0000001 or centreCirclePosition.x >= pointLinePosition.x + 0.0000001:
            coefficient = (centreCirclePosition.z - pointLinePosition.z) / (centreCirclePosition.x - pointLinePosition.x)
            z1 = x1 * coefficient + centreCirclePosition.z - coefficient * centreCirclePosition.x
            z2 = x2 * coefficient + centreCirclePosition.z - coefficient * centreCirclePosition.x
            
    return (mathutils.Vector((x1, y1, z1)), mathutils.Vector((x2, y2, z2)))
    
# Defines the position of intersection into two circles
def intersectionCircleCircle(pointA, radiusA, pointB, radiusB):
    x1 = pointB.x
    y1 = pointB.x
    x2 = pointB.y
    y2 = pointB.y
    z1 = pointB.z
    z2 = pointB.z
    if pointB.y <= pointA.y - 0.0000001 or pointB.y >= pointA.y + 0.0000001:
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
    elif pointB.x <= pointA.x - 0.0000001 or pointB.x >= pointA.x + 0.0000001:
        # Equation Ay**2 + By + C = 0
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
    
    # Calculate the correct z
    if pointB.z <= pointA.z - 0.0000001 or pointB.z >= pointA.z + 0.0000001:                
        if pointB.y <= pointA.y - 0.0000001 or pointB.y >= pointA.y + 0.0000001:
            coefficient = (pointB.z - pointA.z) / (pointB.y - pointA.y)
            z1 = y1 * coefficient + pointB.z - coefficient * pointB.y
            z2 = y2 * coefficient + pointB.z - coefficient * pointB.y
        elif pointB.x <= pointA.x - 0.0000001 or pointB.x >= pointA.x + 0.0000001:
            coefficient = (pointB.z - pointA.z) / (pointB.x - pointA.x)
            z1 = x1 * coefficient + pointB.z - coefficient * pointB.x
            z2 = x2 * coefficient + pointB.z - coefficient * pointB.x
                        
    # Get the position
    return (mathutils.Vector((x1, y1, z1)), mathutils.Vector((x2, y2, z2)))

# Do the rotation around a point "origin" of point "position" an angle "angle"
def getPositionRotationY(origin, position, angle):
    x = math.cos(angle) * position.x - math.sin(angle) * position.y + origin.x - math.cos(angle) * origin.x + math.sin(angle) * origin.y
    y = math.sin(angle) * position.x + math.cos(angle) * position.y + origin.y - math.sin(angle) * origin.x - math.cos(angle) * origin.y
    z = position.z
    
    return mathutils.Vector((x, y, z))

# Defines the visibility of a point
def visible(vertex, previousVertex, previousPreviousVertex):
    segmentActuel = mathutils.Vector((previousPreviousVertex.x - previousVertex.x, previousPreviousVertex.y - previousVertex.y, 0))
    segmentPrecedent = mathutils.Vector((vertex.x - previousVertex.x, vertex.y - previousVertex.y, 0))
    
    # Orientation of the polygon, it's everytime positive
    signOrientation = 1
    return signOrientation * (segmentActuel.x * segmentPrecedent.y - segmentActuel.y * segmentPrecedent.x)

# Get the closest vertex compared to the vertex of reference
def getVertexInBox(purely, vertex, vertexReference, firstVertex, secondVertex):
    selectedVertex = None
    if vertex.x > vertexReference.x:
        if vertex.y > vertexReference.y:
            if vertex.z > vertexReference.z:
                if firstVertex.x >= vertexReference.x and firstVertex.x <= vertex.x and firstVertex.y >= vertexReference.y and firstVertex.y <= vertex.y and firstVertex.z >= vertexReference.z and firstVertex.z <= vertex.z:
                    selectedVertex = firstVertex
                elif secondVertex.x >= vertexReference.x and secondVertex.x <= vertex.x and secondVertex.y >= vertexReference.y and secondVertex.y <= vertex.y and secondVertex.z >= vertexReference.z and secondVertex.z <= vertex.z:
                    selectedVertex = secondVertex
            else:
                if firstVertex.x >= vertexReference.x and firstVertex.x <= vertex.x and firstVertex.y >= vertexReference.y and firstVertex.y <= vertex.y and firstVertex.z <= vertexReference.z and firstVertex.z >= vertex.z:
                    selectedVertex = firstVertex
                elif secondVertex.x >= vertexReference.x and secondVertex.x <= vertex.x and secondVertex.y >= vertexReference.y and secondVertex.y <= vertex.y and secondVertex.z <= vertexReference.z and secondVertex.z >= vertex.z:
                    selectedVertex = secondVertex
        else:
            if vertex.z > vertexReference.z:
                if firstVertex.x >= vertexReference.x and firstVertex.x <= vertex.x and firstVertex.y <= vertexReference.y and firstVertex.y >= vertex.y and firstVertex.z >= vertexReference.z and firstVertex.z <= vertex.z:
                    selectedVertex = firstVertex
                elif secondVertex.x >= vertexReference.x and secondVertex.x <= vertex.x and secondVertex.y <= vertexReference.y and secondVertex.y >= vertex.y and secondVertex.z >= vertexReference.z and secondVertex.z <= vertex.z:
                    selectedVertex = secondVertex
            else:
                if firstVertex.x >= vertexReference.x and firstVertex.x <= vertex.x and firstVertex.y <= vertexReference.y and firstVertex.y >= vertex.y and firstVertex.z <= vertexReference.z and firstVertex.z >= vertex.z:
                    selectedVertex = firstVertex
                elif secondVertex.x >= vertexReference.x and secondVertex.x <= vertex.x and secondVertex.y <= vertexReference.y and secondVertex.y >= vertex.y and secondVertex.z <= vertexReference.z and secondVertex.z >= vertex.z:
                    selectedVertex = secondVertex
    else:
        if vertex.y > vertexReference.y:
            if vertex.z > vertexReference.z:
                if firstVertex.x <= vertexReference.x and firstVertex.x >= vertex.x and firstVertex.y >= vertexReference.y and firstVertex.y <= vertex.y and firstVertex.z >= vertexReference.z and firstVertex.z <= vertex.z:
                    selectedVertex = firstVertex
                elif secondVertex.x <= vertexReference.x and secondVertex.x >= vertex.x and secondVertex.y >= vertexReference.y and secondVertex.y <= vertex.y and secondVertex.z >= vertexReference.z and secondVertex.z <= vertex.z:
                    selectedVertex = secondVertex
            else:
                if firstVertex.x <= vertexReference.x and firstVertex.x >= vertex.x and firstVertex.y >= vertexReference.y and firstVertex.y <= vertex.y and firstVertex.z <= vertexReference.z and firstVertex.z >= vertex.z:
                    selectedVertex = firstVertex
                elif secondVertex.x <= vertexReference.x and secondVertex.x >= vertex.x and secondVertex.y >= vertexReference.y and secondVertex.y <= vertex.y and secondVertex.z <= vertexReference.z and secondVertex.z >= vertex.z:
                    selectedVertex = secondVertex
        else:
            if vertex.z > vertexReference.z:
                if firstVertex.x <= vertexReference.x and firstVertex.x >= vertex.x and firstVertex.y <= vertexReference.y and firstVertex.y >= vertex.y and firstVertex.z >= vertexReference.z and firstVertex.z <= vertex.z:
                    selectedVertex = firstVertex
                elif secondVertex.x <= vertexReference.x and secondVertex.x >= vertex.x and secondVertex.y <= vertexReference.y and secondVertex.y >= vertex.y and secondVertex.z >= vertexReference.z and secondVertex.z <= vertex.z:
                    selectedVertex = secondVertex
            else:
                if firstVertex.x <= vertexReference.x and firstVertex.x >= vertex.x and firstVertex.y <= vertexReference.y and firstVertex.y >= vertex.y and firstVertex.z <= vertexReference.z and firstVertex.z >= vertex.z:
                    selectedVertex = firstVertex
                elif secondVertex.x <= vertexReference.x and secondVertex.x >= vertex.x and secondVertex.y <= vertexReference.y and secondVertex.y >= vertex.y and secondVertex.z <= vertexReference.z and secondVertex.z >= vertex.z:
                    selectedVertex = secondVertex
    
    if purely:
        if selectedVertex != None and selectedVertex.x == vertex.x and selectedVertex.y == vertex.y and selectedVertex.z == vertex.z:
            selectedVertex = None
        if selectedVertex != None and selectedVertex.x == vertexReference.x and selectedVertex.y == vertexReference.y and selectedVertex.z == vertexReference.z:
            selectedVertex = None
    
    return selectedVertex

# Compare two co-vertex
def compareTwoCoVertex(vertex1, vertex2):
    return vertex1[0] + 0.0000001 >= vertex2[0] and vertex1[0] - 0.0000001 <= vertex2[0] and vertex1[1] + 0.0000001 >= vertex2[1] and vertex1[1] - 0.0000001 <= vertex2[1] and vertex1[2] + 0.0000001 >= vertex2[2] and vertex1[2] - 0.0000001 <= vertex2[2]

# Manual extrude
def manualExtrude(object, listIndexVertices, sizeExtrude):
    listNewIndexVertice = []
    index = 0
    while index < len(listIndexVertices):
        # Extend the vertices
        object.data.vertices.add(1)
        object.data.vertices[-1].co = (object.data.vertices[listIndexVertices[index]].co[0] + sizeExtrude.x, object.data.vertices[listIndexVertices[index]].co[1] + sizeExtrude.y, object.data.vertices[listIndexVertices[index]].co[2] + sizeExtrude.z)
        listNewIndexVertice.append(object.data.vertices[-1].index)
        
        # Extend the edges
        if index == 0:
            object.data.edges.add(1)
            object.data.edges[-1].vertices = [listIndexVertices[index], object.data.vertices[-1].index]
        else:
            if index == len(listIndexVertices) - 1:
                object.data.edges.add(3)
                object.data.edges[-3].vertices = [object.data.vertices[-len(listIndexVertices)].index, object.data.vertices[-1].index]
            else:
                object.data.edges.add(2)
            object.data.edges[-2].vertices = [listIndexVertices[index], object.data.vertices[-1].index]
            object.data.edges[-1].vertices = [object.data.vertices[-2].index, object.data.vertices[-1].index]
            
            # Create the faces
            createFace(object, [listIndexVertices[index-1], object.data.vertices[-2].index, object.data.vertices[-1].index, listIndexVertices[index]])
            if index == len(listIndexVertices) - 1:
                createFace(object, [listIndexVertices[index], object.data.vertices[-1].index, object.data.vertices[-len(listIndexVertices)].index, listIndexVertices[0]])
        index += 1
    
    # Create the last face
    listNewIndexVertice.reverse()
    createFace(object, listNewIndexVertice)
    return listNewIndexVertice

# Do the difference with the boolean modifier
def doDifferenceBooleanModifier(objectApply, object):
    modifier = objectApply.modifiers.new('',type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = object
    bpy.context.scene.objects.active = objectApply
    objectApply.select = True
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=modifier.name)