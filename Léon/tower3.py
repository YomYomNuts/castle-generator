import bpy
from utils import *

scn = bpy.context.scene

# Level of Detail
lod = 16
radius = 32
width = 8
height = 96
position = (0,0,0)
subdivision = 2

circle1 = createCircle(position, lod, radius)
circle2 = createCircle(position, lod, radius - width)
scn.objects.active = circle1
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action = 'SELECT')
bpy.ops.object.join()
# bpy.ops.mesh.bridge_edge_loops(inside=False, use_merge=False, merge_factor=0.5)

# BODY #

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
bpy.ops.mesh.select_all(action = 'SELECT')
# Subdivise body
for sub in range(subdivision) :
	bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
		(0, 0, height / subdivision)})
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action = 'DESELECT')

# STAIRS #


stairWidthIn = 4
stairWidthOut = 10
stairHeight = 4
lenStairs = 16

# INNER CIRCLE #
stairCylindreWidth = 4
circleInner = createCircle(position, lod, stairCylindreWidth)
scn.objects.active = circleInner
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')
bpy.ops.mesh.select_all(action = 'SELECT')
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
	(0, 0, height)})
bpy.ops.object.mode_set(mode='OBJECT')


# CUBES #
verts = [	((-radius + width), stairWidthOut * -0.5, 0),\
			((-radius + width), (stairWidthOut * 0.5), 0),\
			(0, (stairWidthIn * 0.5), 0),\
			(0, (stairWidthIn * -0.5), 0)]
edges = []
faces = [[0,1,2,3]]

stair = createMesh("Stairs", position, verts, edges, faces)
stair.show_name = False
scn.objects.active = stair
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
	(0, 0, stairHeight)})
bpy.ops.object.mode_set(mode='OBJECT')

stair.select = True
scn.objects.active = stair
bpy.context.active_object.rotation_euler[2] = math.pi * 2 * (-0.5/lenStairs)

# SPIN
for s in range(lenStairs) :
	# Duplicate
	bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, stairHeight), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "texture_space":False, "release_confirm":False})
	bpy.context.active_object.rotation_euler[2] = math.pi * 2 * (s / lenStairs + 0.5/lenStairs)

