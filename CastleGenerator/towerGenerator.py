import bpy
import os
import random
import math
from utils import *

# Class TowerGenerator
class TowerGenerator:
	def __init__(self, origin, numVerts, rad, totalHeight, crenaux, poteaux, door, rembarde, roof, etendard, stairs):			
		# Create Tower object
		bpy.context.scene.cursor_location = (0,0,0)
		bpy.ops.mesh.primitive_circle_add(vertices=numVerts, radius=rad)
		object = bpy.context.active_object
		# List of composed objects
		towerObjects = [object]
		object.name = "TowerGenerator"
		me = object.data
		me.name = "TowerGenerator"
		me.materials.append(bpy.data.materials['Brick'])
		
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
		bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0)})	
		bpy.ops.transform.resize(value=(ratio, ratio, 1))
		if (stairs == False):
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
			copyObject("asset.stick")
			spinObject(int(numVerts * 0.5), innerRadius - crenauxWidth * 0.5, (0,0,0), offset)
			objectPoteaux = bpy.context.active_object
			towerObjects.append(objectPoteaux)
			objectPoteaux.rotation_euler[2] = - math.pi * (1 / numVerts)
			
			if (rembarde):
				copyObject("asset.planks")
				spinObject(int(numVerts * 0.5), innerRadius - crenauxWidth * 0.5, (0,0,0), offset)
				objectRembarde = bpy.context.active_object
				towerObjects.append(objectRembarde)
				objectRembarde.rotation_euler[2] = math.pi * (1 / numVerts)
		
		# Stairs
		if (stairs):
			innerRadius = innerRadius * ratio
			radian = math.pi * 2 * (1/numVerts)
			stairWidthOut = radian * rad
			stairWidthIn = radian 
			stairHeight = 0.25
			lenStairs = int(totalHeight/stairHeight) - 1
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
			spinOneObjectRandom(numVerts, rad, (0,0,0), 0)
			towerObjects.append(bpy.context.active_object)
			
		# Roof
		if (roof):
			# Object
			bpy.context.scene.cursor_location = (0,0,0)
			bpy.ops.mesh.primitive_circle_add(vertices=numVerts, radius=rad)
			objectRoof = bpy.context.active_object
			towerObjects.append(objectRoof)
			me = objectRoof.data
			me.materials.append(bpy.data.materials['Roof'])
			bpy.context.tool_settings.mesh_select_mode = [False, True, False]
			# Edit Mode
			bpy.ops.object.mode_set(mode='EDIT')
			roofHeight = 5
			bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, roofHeight)})
			bpy.ops.mesh.merge(type='CENTER', uvs=False)
			# Final position
			bpy.ops.object.mode_set(mode='OBJECT')
			positionRoof = totalHeight
			if (crenaux):
				positionRoof += crenauxHeight
			if (poteaux):
				positionRoof += 2
			objectRoof.location.z = positionRoof
			
		# Etendard
		if (etendard):
			copyObject("asset.etendard")
			spinOneObjectRandom(numVerts, (rad + innerRadius) * 0.5, (0,0,totalHeight - 1), 0)
			towerObjects.append(bpy.context.active_object)
			
		# Join everything
		bpy.ops.object.select_all(action='DESELECT')
		bpy.context.scene.objects.active = towerObjects[0]
		for o in towerObjects:
			o.select = True
		if (len(towerObjects) > 1):	
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