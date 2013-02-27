import bpy
import math
from utils import *

scn = bpy.context.scene

def createCircle(lod, radius):

	verts = []
	edges = []
	faces = []

	# verts = [(0,0,0)]
	for i in range(lod) :
		verts.append((math.cos(math.pi * 2 * (i / lod)) * radius, math.sin(math.pi * 2 * (i / lod)) * radius, 0))
		if (i + 2 > lod) :
			edges.append((i, 0))
		else :
			edges.append((i, i + 1))
    
	object = createMesh("Tour", (0,0,0), verts, edges, faces)
	scn.objects.active = object
	object.select = True
	
	return object

def spinObject(lod, radius):
	obj = bpy.context.active_object
	for i in range(lod) :
		# Duplicate
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})
		obj = bpy.context.active_object
		obj.location = (math.cos(math.pi * 2 * (i / lod)) * radius, math.sin(math.pi * 2 * (i / lod)) * radius, 0)
	
class Tour :
	object = []
	mesh = []
	def __init__(self):
		lod = 16
		radius = 10
		height = 50
		heightBase = 4
		offsetBase = 2
		heightRempart = 10
		offsetRempart = 5
		
		self.object = createCircle(lod, radius)
		
		bpy.ops.object.editmode_toggle()
		
		# Setp 1
		scaleBase = (radius - offsetBase) / radius
		bpy.ops.transform.resize(value=\
			(scaleBase, scaleBase, 1))
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightBase * 0.25)})
			
		scaleBase = (radius - offsetBase * 0.5) / radius
		bpy.ops.transform.resize(value=\
			(scaleBase, scaleBase, 1))
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightBase * 0.75)})
		
		# Step 2
		scaleBase = (radius * scaleBase) / radius
		bpy.ops.transform.resize(value=\
			(scaleBase, scaleBase, 1))
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, height)})
		
		# Remparts
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightRempart * 0.1)})
		scaleRempart = (radius + offsetRempart) / radius
		bpy.ops.transform.resize(value=\
			(scaleRempart, scaleRempart, 1))
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightRempart * 0.9)})
		
		bpy.ops.object.editmode_toggle()
		bpy.ops.object.shade_smooth()
		
		# for v in self.object.data.vertices :
			# if ( v.co.z > self.totalHeight ) :
				# self.totalHeight = v.co.z

tour = Tour()

spinObject(12, 20)