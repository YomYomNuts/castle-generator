import bpy
import math
from utils import *

scn = bpy.context.scene

def createCircle(position, lod, radius):
	# lod = Level of Detail
	verts = []
	edges = []
	faces = []
	for i in range(lod) :
		# Vertices
		verts.append((math.cos(math.pi * 2 * (i / lod)) * radius, math.sin(math.pi * 2 * (i / lod)) * radius, 0))
		# Edges
		if (i + 2 > lod) :
			edges.append((i, 0))
		else :
			edges.append((i, i + 1))
	# Create object
	object = createMesh("Tour", position, verts, edges, faces)
	return object
	
# Copy object on the scene
def copyObject(name):
	scn.objects.active = scn.objects[name]
	scn.objects[name].layers[0] = True
	scn.objects[name].select = True	
	bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})
	bpy.context.active_object.show_name = False
	scn.objects[name].select = False
	scn.objects[name].layers[0] = False

# Duplicate active object around a circle
def spinObject(lod, radius, position, offset):
	for i in range(lod) :
		# Refresh
		obj = bpy.context.active_object
		# Position
		obj.location = \
			(position.x + math.cos(math.pi * 2 * (i / lod + offset * 1/lod)) * radius, \
			position.y + math.sin(math.pi * 2 * (i / lod + offset * 1/lod)) * radius, \
			position.z)
		# Orientation
		obj.rotation_euler[2] = math.pi * 2 * (i / lod + offset * 1/lod)
		# Duplicate
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})

# Bevel edges where 'n' is the index of a vertices and 'lod' the vertices length of a circle
def bevelCircle(n, lod):
        # Setup context
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_all(action = 'DESELECT')
		bpy.ops.object.mode_set(mode='OBJECT')
		ob = bpy.context.active_object
		
		# Select circle
		for offset in range(lod) :
			ob.data.vertices[n * lod + offset].select = True
			
		# Bevel operation
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.bevel(offset=1, segments=1, vertex_only=False)
		
        # Deselect all vertex
		bpy.ops.mesh.select_all(action = 'DESELECT')
		bpy.ops.object.mode_set(mode='OBJECT')
	
class Tour :
	object = []
	mesh = []
	
	def __init__(self, position, lod=16, radius=20, heightBody=100, heightBase=4, offsetBase=2, heightWall = 20, heightRempart = 50, offsetRempart = 30, subdivision = 6):
		
		# Create first circle
		self.object = createCircle(position, lod, radius)
		
		# Setup context
		scn.objects.active = self.object
		self.object.select = True
		bpy.ops.object.editmode_toggle()
		bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
		
		# BOTTOM #
		
		# Scale
		scaleBase = 0.9
		bpy.ops.transform.resize(value=(scaleBase, scaleBase, 1))
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightBase * 0.25)})
		# Scale
		bpy.ops.transform.resize(value=(scaleBase, scaleBase, 1))
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightBase * 0.75)})
		
		# BODY #
		
		# Scale
		bpy.ops.transform.resize(value=(scaleBase, scaleBase, 1))
		# Subdivise body
		for sub in range(subdivision) :
			bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
				(0, 0, heightBody / subdivision)})
		
		# OFFSET TOP #
		
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightRempart * 0.3)})
		# Scale
		scaleRempart = (radius + offsetRempart) / radius
		bpy.ops.transform.resize(value=(scaleRempart, scaleRempart, 1))
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightRempart * 0.9)})
			
		# GROUND #
		
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 0)})
		# Scale
		bpy.ops.transform.resize(value=(0.5, 0.5, 1))
		# Refresh object
		bpy.ops.object.editmode_toggle()
		bpy.ops.object.editmode_toggle()
		# Get positionGround from last vertex
		positionGround = self.object.data.vertices[len(self.object.data.vertices) - 1].co.xyz
		positionGround.x = position[0]
		positionGround.y = position[1]
		
		# WALLS #
		
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, heightWall)})
			
		# ROOF #
		
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 0)})
		# Scale
		bpy.ops.transform.resize(value=(0.7, 0.7, 1))
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 6)})
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 0)})
		# Scale
		bpy.ops.transform.resize(value=(1.2, 1.2, 1))
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 1)})
		# Extrude
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			(0, 0, 5)})
		# Colapse vertices
		bpy.ops.mesh.merge(type='CENTER', uvs=False)
		
		# BEVELS Operations #
		bevelCircle(subdivision + 6, lod)
		bevelCircle(subdivision + 5, lod)
		bevelCircle(subdivision + 4, lod)
		bevelCircle(subdivision + 3, lod)
		bevelCircle(subdivision + 2, lod)
		
		# Setup context
		self.object.select = False
		bpy.ops.object.mode_set(mode='OBJECT')
		
		# REMPART #
		copyObject("Rempart")
		spinObject(lod, radius + offsetRempart * 0.5 - 1, positionGround, 0)
		
		# Setup context
		bpy.ops.object.select_all(action='DESELECT')
		
		# PLANCHES #
		copyObject("Planches")
		spinObject(lod, radius + offsetRempart * 0.5 - 1, positionGround, 0.5)
		
		# DOOR #
		copyObject("Door")
		offset = 1
		obj = bpy.context.active_object
		# Position
		obj.location = \
			(positionGround.x + math.cos(math.pi * 2 * (3 / lod)) * (radius * 0.5 + offset), \
			positionGround.y + math.sin(math.pi * 2 * (3 / lod)) * (radius * 0.5 + offset), \
			positionGround.z)
		# Orientation
		obj.rotation_euler[2] = math.pi * 2 * (3 / lod)
		
# Main
tour = Tour((5,5,0))