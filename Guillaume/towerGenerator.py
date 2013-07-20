import bpy
import os
import random
import math
from utils import *

# Class TowerGenerator
class TowerGenerator:
    def __init__(self, origin, numVerts, rad, totalHeight, crenaux, poteaux, door, rembarde):
        uvSizeCubeWood = 20.0
        uvSizeRoof = 20.0
        uvSizeTube = 20.0
        uvSizeCube = 0.4
        
        brick = os.path.join(os.path.dirname(bpy.data.filepath), 'BrickOldSharp0264_23_S.jpg')
        realpathbrick = os.path.expanduser(brick)
        try:
        	imgbrick = bpy.data.images.load(realpathbrick)
        except:
        	raise NameError("Cannot load image %s" % realpathbrick)
        
        # Create image texture from image
        cTex = bpy.data.textures.new('BrickTexture', type = 'IMAGE')
        cTex.image = imgbrick
        matCube = bpy.data.materials.new('MaterialCube')
        
        # Add texture slot for color texture
        mtex = matCube.texture_slots.add()
        mtex.texture = cTex
        mtex.texture_coords = 'GLOBAL'
        mtex.mapping = 'CUBE'
        mtex.use_map_color_diffuse = True 
        mtex.use_map_color_emission = True 
        mtex.emission_color_factor = 0.5
        mtex.use_map_density = True 
        mtex.scale = (uvSizeCube, uvSizeCube, uvSizeCube)
        	
        # Create Tower object
        bpy.context.scene.cursor_location = (0,0,0)
        bpy.ops.mesh.primitive_circle_add(vertices=numVerts, radius=rad)
        object = bpy.context.active_object
        # List of composed objects
        towerObjects = [object]
        object.name = "TowerGenerator"
        me = object.data
        me.name = "TowerGenerator"
        me.materials.append(matCube)
        
        # Set Edge Edit Mode
        bpy.context.tool_settings.mesh_select_mode = [False, True, False]
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Main cylinder
        iterations = 10
        step = totalHeight/iterations
        ratio = 0.98
        innerRadius = rad
        for cercle in range(iterations):
        	bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, step)})
        	bpy.ops.transform.resize(value=(ratio, ratio, 1))
        	innerRadius = innerRadius * 0.98
        # Base for Crenaux
        crenauxWidth = 1
        crenauxHeight = 1
        ratio = 1 - crenauxWidth / rad
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0)})	
        bpy.ops.transform.resize(value=(ratio, ratio, 1))
        
        # Cap
        ratio = 1 - (1 / (rad-1))
        for i in range(int(rad-1)):
        	bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0)})	
        	bpy.ops.transform.resize(value=(ratio, ratio, 1))
        
        # Hole
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, -totalHeight)})	
        
        # Final Cap
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0)})	
        bpy.ops.mesh.merge(type='CENTER', uvs=False)
        
        # Crenaux
        if (crenaux):	
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.scene.objects.active = towerObjects[0]
            indexes = range(len(bpy.context.active_object.data.polygons))
            
            listIndexPolygons = [i for i in indexes[(numVerts*iterations):(numVerts*iterations+numVerts)]]
            bpy.context.active_object.data.polygons[listIndexPolygons[0]].select = True
            polygonsDone = [0]
            verticesToFind = set(bpy.context.active_object.data.polygons[listIndexPolygons[0]].vertices)
            while len(polygonsDone) < len(listIndexPolygons):
                neighboursPolygons = [x for x in listIndexPolygons if not verticesToFind & set(bpy.context.active_object.data.polygons[x].vertices) == set() and not x in polygonsDone]
                polygonsDone.append(neighboursPolygons[0])
                verticesToFind = set(bpy.context.active_object.data.polygons[neighboursPolygons[0]].vertices)
                if len(polygonsDone) % 2 == 0:
                    bpy.context.active_object.data.polygons[neighboursPolygons[0]].select = True
            
            bpy.context.tool_settings.mesh_select_mode = [False, False, True]
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, crenauxHeight)})
        
        # UV unwrap
        bpy.ops.uv.smart_project()
        
        # Erosion
        factorErosion = 0.2
        bpy.ops.object.mode_set(mode='OBJECT')
        object = bpy.context.active_object
        for v in object.data.vertices:
        	v.co.x += random.random() * factorErosion
        	v.co.y += random.random() * factorErosion
        	v.co.z += random.random() * factorErosion
        	
        # Poteaux
        if (poteaux):
        	offset = totalHeight
        	# Extra height if crenaux
        	if (crenaux):
        		offset += crenauxHeight
        	copyObject("asset.stick")
        	spinObject(int(numVerts * 0.5), innerRadius - crenauxWidth * 0.5, (0,0,origin[2]), offset)
        	objectPoteaux = bpy.context.active_object
        	towerObjects.append(objectPoteaux)
        	objectPoteaux.rotation_euler[2] = - math.pi * (1 / numVerts)
        	
        	if (rembarde):
        		copyObject("asset.planks")
        		spinObject(int(numVerts * 0.5), innerRadius - crenauxWidth * 0.5, (0,0,origin[2]), offset)
        		objectRembarde = bpy.context.active_object
        		towerObjects.append(objectRembarde)
        		objectRembarde.rotation_euler[2] = math.pi * (1 / numVerts)
        
        # Stairs
        innerRadius = innerRadius * ratio
        radian = math.pi * 2 * (1/numVerts)
        stairWidthOut = radian * rad
        stairWidthIn = radian 
        stairHeight = 0.25
        lenStairs = int(totalHeight/stairHeight)
        width = 0
        verts = [(-innerRadius, stairWidthOut * -0.5, 0), (-innerRadius, (stairWidthOut * 0.5), 0), (0, 0, 0), (0, 0, 0)] 
        edges = []
        faces = [[0,1,2,3]]
        stair = createMesh("Stairs", (0,0,0), verts, edges, faces)
        stair.show_name = False
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.scene.objects.active = stair
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, stairHeight)})
        bpy.ops.object.mode_set(mode='OBJECT')
        stair.select = True
        bpy.context.scene.objects.active = stair
        bpy.context.active_object.rotation_euler[2] = math.pi * 2 * (-0.5/numVerts)
        objectStair = [stair]
        for s in range(lenStairs) :
        	bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, stairHeight)})
        	bpy.context.active_object.rotation_euler[2] = math.pi * 2 * (s / numVerts + 0.5/numVerts)
        	objectStair.append(bpy.context.active_object)
        	
        for o in objectStair:
        	o.select = True
        
        bpy.context.scene.objects.active = stair
        bpy.ops.object.join()
        towerObjects.append(bpy.context.active_object)
        	
        # Door
        if (door):
        	copyObject("asset.door")
        	spinOneObject(numVerts, rad, (0,0,origin[2]), 0)
        	towerObjects.append(bpy.context.active_object)
        	
        # Join everything
        bpy.ops.object.select_all(action='DESELECT')
        for o in towerObjects:
        	o.select = True
        if (len(towerObjects) > 1):
        	bpy.context.scene.objects.active = towerObjects[0]
        	bpy.ops.object.join()
        bpy.context.active_object.location.x = origin.x
        bpy.context.active_object.location.y = origin.y
        bpy.context.active_object.location.z = origin.z
        bpy.context.scene.cursor_location = (0,0,0)
        
        # Calculate the normals
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.normals_make_consistent()
        bpy.ops.object.mode_set(mode='OBJECT')