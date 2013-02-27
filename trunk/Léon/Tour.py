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
	
	return object

def spinObject(lod, radius, z, offset):
	for i in range(lod) :
		# Duplicate
		obj = bpy.context.active_object
		obj.location = (math.cos(math.pi * 2 * (i / lod + offset * 1/lod)) * radius, math.sin(math.pi * 2 * (i / lod + offset * 1/lod)) * radius, z)
		obj.rotation_euler[2] = math.pi * 2 * (i / lod + offset * 1/lod)
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})
	
class Tour :
	object = []
	mesh = []
	def __init__(self):
		lod = 16
		radius = 20
		height = 100
		heightBase = 4
		offsetBase = 2
		heightRempart = 5
		offsetRempart = 5
		
		self.object = createCircle(lod, radius)
		
		scn.objects.active = self.object
		self.object.select = True
		
		bpy.ops.object.editmode_toggle()
		
		# Setp 1
		scaleBase = 0.9
		# scaleBase = (radius + offsetBase) / radius
		bpy.ops.transform.resize(value=\
			(scaleBase, scaleBase, 1))
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightBase * 0.25)})
			
		# scaleBase = (radius + offsetBase * 0.5) / radius
		bpy.ops.transform.resize(value=\
			(scaleBase, scaleBase, 1))
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightBase * 0.75)})
		
		# Step 2
		# scaleBase = (radius * scaleBase) / radius
		bpy.ops.transform.resize(value=\
			(scaleBase, scaleBase, 1))
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, height)})
		
		# Remparts
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightRempart * 0.3)})
			
		# scaleRempart = (radius + offsetRempart) / radius
		scaleRempart = 1.5
		bpy.ops.transform.resize(value=\
			(scaleRempart, scaleRempart, 1))
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightRempart * 0.9)})
			
		# Ground
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 0)})
		bpy.ops.mesh.merge(type='CENTER', uvs=False)
		
		bpy.ops.object.editmode_toggle()
		# bpy.ops.object.shade_smooth()
	
		sommet = self.object.data.vertices[len(self.object.data.vertices) - 1].co.z
		self.object.select = False
		
		# Copy original object Rempart
		scn.objects.active = scn.objects["Rempart"]
		scn.objects["Rempart"].layers[0] = True
		scn.objects["Rempart"].select = True
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})
		scn.objects["Rempart"].select = False
		scn.objects["Rempart"].layers[0] = False
		
		# Construct objects around a circle
		spinObject(lod, radius+1, sommet, 0)
		
		bpy.ops.object.select_all(action='DESELECT')
		
		# Copy original object Planches
		scn.objects.active = scn.objects["Planches"]
		scn.objects["Planches"].layers[0] = True
		scn.objects["Planches"].select = True
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})
		scn.objects["Planches"].select = False
		scn.objects["Planches"].layers[0] = False
		
		# Construct objects around a circle
		spinObject(lod, radius, sommet, 0.5)

tour = Tour()