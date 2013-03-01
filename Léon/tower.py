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
	objects = []
	for i in range(lod) :
		# Refresh
		obj = bpy.context.active_object
		objects.append(obj)
		# Position
		obj.location = \
			(position.x + math.cos(math.pi * 2 * (i / lod + offset * 1/lod)) * radius, \
			position.y + math.sin(math.pi * 2 * (i / lod + offset * 1/lod)) * radius, \
			position.z)
		# Orientation
		obj.rotation_euler[2] = math.pi * 2 * (i / lod + offset * 1/lod)
		# Duplicate
		bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})
	return objects
	
def selectVertices(object, indexes):
	# Select object
	scn.objects.active = object
	# Setup context
	bpy.ops.object.mode_set(mode='EDIT')
	bpy.ops.mesh.select_all(action = 'DESELECT')
	bpy.ops.object.mode_set(mode='OBJECT')
	# Select vertices
	for i in range(len(indexes)) :
		object.data.vertices[indexes[i]].select = True

def getCircle(index, length):
	circle = []
	for i in range(length) :
		circle.append(index * length + i)
	return circle

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

def scrollVertices(helper, object, indexes):
	for i in range(len(indexes)) :
		object.data.vertices[indexes[i]].co.z = helper.location.z
		
def scaleVertices(helper, object, indexes, radius):
	long = len(indexes)
	for i in range(long) :
		print("poin")
		object.data.vertices[indexes[i]].co.x = math.cos(math.pi * 2 * (i / long)) * radius
		object.data.vertices[indexes[i]].co.y = math.sin(math.pi * 2 * (i / long)) * radius

def refresh(object, lod=16):
		
		# Refresh
		bpy.ops.object.editmode_toggle()
		bpy.ops.object.editmode_toggle()
		
		# Select
		# selectVertices(getCircle(2))
		selectVertices(object, getCircle(2, lod))
		
		# Scroll
		scrollVertices(scn.objects["HelperRemparts"], object, getCircle(2, lod))
		
		verts = scn.objects["HelperRemparts"].data.vertices
		demi = 16
		radius = math.fabs(scn.objects["HelperRemparts"].data.vertices[0].co.y) + math.fabs(scn.objects["HelperRemparts"].data.vertices[demi].co.y)
		radius *= 0.4
		
		# Scale
		scaleVertices(scn.objects["HelperRemparts"], object, getCircle(2, lod), radius)	


class Tower :
	object = []
	mesh = []
	
	def __init__(self, position=(0,0,0), lod=16, radius=20, heightBody=100, heightBase=4, offsetBase=2, heightWall = 20, heightRempart = 50, offsetRempart = 30):
		
		subdivision = 4
		
		old = scn.objects.get("Tour")
		if (old != None) :
			old.select = True
			scn.objects.active = old
			bpy.ops.object.delete(use_global=False)
		
		# Create first circle
		self.object = createCircle(position, lod, radius)
		
		# Setup context
		scn.objects.active = self.object
		self.object.select = True
		bpy.ops.object.editmode_toggle()
		bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
		
		# BODY #
		
		# Scale
		# bpy.ops.transform.resize(value=(scaleBase, scaleBase, 1))
		# Subdivise body
		for sub in range(subdivision) :
			bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
				(0, 0, heightBody / subdivision)})
		bpy.ops.object.mode_set(mode='OBJECT')
		
	def refresh(self, lod):
		
		# Refresh
		bpy.ops.object.editmode_toggle()
		bpy.ops.object.editmode_toggle()
		
		# Select
		# selectVertices(getCircle(2))
		selectVertices(self.object, getCircle(2, lod))
		
		# Scroll
		scrollVertices(scn.objects["HelperRemparts"], self.object, getCircle(2, lod))
		
		verts = scn.objects["HelperRemparts"].data.vertices
		demi = 16
		radius = math.fabs(scn.objects["HelperRemparts"].data.vertices[0].co.y) + math.fabs(scn.objects["HelperRemparts"].data.vertices[demi].co.y)
		radius *= 0.4
		
		# Scale
		scaleVertices(scn.objects["HelperRemparts"], self.object, getCircle(2, lod), radius)
		# print(scn.objects["HelperRemparts"].location.z)
		