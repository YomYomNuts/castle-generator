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
		
def bevelCircle(n, lod):
        # Deselect all vertex
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_all(action = 'DESELECT')
		bpy.ops.object.mode_set(mode='OBJECT')
		ob = bpy.context.active_object
		
		# Select circle above remparts
		for offset in range(lod) :
			ob.data.vertices[n * lod + offset].select = True
		# BEVEL
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.bevel(offset=1, segments=1, vertex_only=False)
		
        # Deselect all vertex
		bpy.ops.mesh.select_all(action = 'DESELECT')
		bpy.ops.object.mode_set(mode='OBJECT')
	
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
		heightWall = 20
		
		self.object = createCircle(lod, radius)
		
		scn.objects.active = self.object
		self.object.select = True
		
		bpy.ops.object.editmode_toggle()
		bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')

		
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
		
		subdivision = 6
		for sub in range(subdivision) :
			bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
				(0, 0, height / subdivision)})
		
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
		bpy.ops.transform.resize(value=\
			(0.5, 0.5, 1))
		
		bpy.ops.object.editmode_toggle()
		bpy.ops.object.editmode_toggle()
		sommet = self.object.data.vertices[len(self.object.data.vertices) - 1].co.z
		
		# Walls
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightWall)})
			
		# Roof
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 0)})
		bpy.ops.transform.resize(value=\
			(0.7, 0.7, 1))
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 6)})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 0)})
		bpy.ops.transform.resize(value=\
			(1.2, 1.2, 1))
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 1)})
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 5)})
		# Colapse vertices
		bpy.ops.mesh.merge(type='CENTER', uvs=False)
		
		# EDGE MODE
		# bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE', action='TOGGLE')
		# prevEdge = self.object.data.edges[0]
		# for edge in self.object.data.edges :
			# print(dir(edge))
			# if (self.object.data.vertices[edge.vertices[0]].co.z == self.object.data.vertices[edge.vertices[1]].co.z) :
				# print("poin")
				# edge.select = True
				# print(edge.select)
		# Update mesh with new data
		# self.object.data.update(calc_edges=True)
		# self.object = bpy.context.active_object
		
		bevelCircle(subdivision + 6, lod)
		bevelCircle(subdivision + 5, lod)
		bevelCircle(subdivision + 4, lod)
		bevelCircle(subdivision + 3, lod)
		bevelCircle(subdivision + 2, lod)
			
		
		
		
		# Select last vertex
		# self.object.data.vertices[len(self.object.data.vertices) - 1].select = True
		

		# Translate all vertex with random proportion
		# bpy.ops.object.mode_set(mode='EDIT')
		# bpy.ops.transform.translate(value=(0.6, 0.6, 0.6), constraint_axis=(True, True, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='RANDOM', proportional_size=207.965, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=True)
		
		# bpy.ops.object.shade_smooth()
		bpy.ops.object.mode_set(mode='OBJECT')


		# prevVert = self.object.data.vertices[0]
		# for vertex in self.object.data.vertices :
			# if (vertex.co.z == prevVert.co.z) :
				# vertex.select = True
			# prev
			
		self.object.select = False
		
		# Copy original object Rempart
		scn.objects.active = scn.objects["Rempart"]
		scn.objects["Rempart"].layers[0] = True
		scn.objects["Rempart"].select = True	
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})
		scn.objects["Rempart"].select = False
		scn.objects["Rempart"].layers[0] = False
		
		# REMPART
		spinObject(lod, radius, sommet, 0)
		
		bpy.ops.object.select_all(action='DESELECT')
		
		# Copy original object Planches
		scn.objects.active = scn.objects["Planches"]
		scn.objects["Planches"].layers[0] = True
		scn.objects["Planches"].select = True
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})
		scn.objects["Planches"].select = False
		scn.objects["Planches"].layers[0] = False
		
		# PLANCHES
		spinObject(lod, radius - 1, sommet, 0.5)

tour = Tour()