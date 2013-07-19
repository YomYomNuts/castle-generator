#----------------------------------------------------------
# File texture.py
#----------------------------------------------------------
import bpy, os, random, math

scn = bpy.context.scene

# Copy object on the scene
def copyObject(name):
	bpy.ops.object.select_all(action='DESELECT')
	scn.objects.active = scn.objects[name]
	scn.objects[name].layers[0] = True
	scn.objects[name].select = True	
	bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})
	bpy.context.active_object.show_name = False
	bpy.context.active_object.name = "tower." + name
	scn.objects[name].select = False
	scn.objects[name].layers[0] = False

# Duplicate active object around a circle
def spinObject(lod, radius, position, offset):
	objects = []
	for i in range(lod) :
		obj = bpy.context.active_object
		objects.append(obj)
		obj.location = (position[0] + math.cos(math.pi * 2 * (i / lod)) * radius, 
			position[1] + math.sin(math.pi * 2 * (i / lod )) * radius, 
			position[2] + offset)
		obj.rotation_euler[2] = math.pi * 2 * (i / lod)
		if (i < lod - 1):
			bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0,0,0)})
	for o in objects:
		o.select = True
	bpy.ops.view3d.snap_cursor_to_selected()
	bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
	bpy.ops.object.join()
		
# Duplicate active object around a circle
def spinOneObject(lod, radius, position, offset):
	obj = bpy.context.active_object
	obj.location = (position[0] + math.cos(math.pi * 2 * (offset * 1/lod)) * radius, 
		position[1] + math.sin(math.pi * 2 * (offset * 1/lod)) * radius, 
		position[2])
	obj.rotation_euler[2] = math.pi * 2 * (offset * 1/lod)
	
def spinOneObjectRandom(lod, radius, position, offset):
	i = int(random.random() * lod)
	obj = bpy.context.active_object
	obj.location = (position[0] + math.cos(math.pi * 2 * (i / lod + offset * 1/lod)) * radius, 
		position[1] + math.sin(math.pi * 2 * (i / lod + offset * 1/lod)) * radius, 
		position[2])
	obj.rotation_euler[2] = math.pi * 2 * (i / lod + offset * 1/lod)

class propertiesTowerProps(bpy.types.PropertyGroup):
	positionCenter = bpy.props.FloatVectorProperty(name="Position", description="Tower Position", subtype="XYZ", default=(0.0, 0.0, 0.0))
	numVerts = bpy.props.IntProperty(name="NumVerts", description="Number of vertices of the cylinder", default=24, min=3, max=64)
	radius = bpy.props.FloatProperty(name="Radius", description="Radius of the tower", default=5.0, min=2.0, max=100.0)
	totalHeight = bpy.props.FloatProperty(name="TotalHeight", description="Total Height of the tower", default=20.0, min=5.0, max=100.0)
	crenaux = bpy.props.BoolProperty(name="Crenaux", default=True)
	poteaux = bpy.props.BoolProperty(name="Poteaux", default=False)
	door = bpy.props.BoolProperty(name="Porte", default=False)
	rembarde = bpy.props.BoolProperty(name="Rembarde", default=False)

class TowerPanel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Tower Edition"
	bl_idname = "OBJECT_PT_tower"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	#bl_context = "object"

	def draw(self, context):
		layout = self.layout
		TowerProps = bpy.context.window_manager.TowerProps
		row = layout.row()
		row.operator("tower.build", text="Build!", icon='MESH_CYLINDER')
		row = layout.row()
		box = row.box()
		box.prop(TowerProps, 'positionCenter')
		box.prop(TowerProps, 'numVerts')
		box.prop(TowerProps, 'radius')
		box.prop(TowerProps, 'totalHeight')
		box.prop(TowerProps, 'crenaux')
		box.prop(TowerProps, 'poteaux')
		box.prop(TowerProps, 'door')
		box.prop(TowerProps, 'rembarde')
		
class OBJECT_OT_buildtower(bpy.types.Operator):
	bl_label = "BuildTower"
	bl_idname = "tower.build"
	bl_description = "Build Tower"

	def execute(self, context):
		
		# removeFromCollection(bpy.data.objects, 'Tower')
		# removeFromCollection(bpy.data.meshes, 'Circle')
		
		# bpy.ops.object.add(type='EMPTY')
		# bpy.context.active_object.name = "tmp.empty"
		# bpy.ops.object.mode_set(mode='OBJECT')
		# bpy.ops.object.select_all(action='DESELECT')
				
		# Clean scene
		count = 0
		for o in context.scene.objects:
			tags = o.name.split(".")
			if tags[0] == "tmp":				
				o.select = True
				count += 1
		if (count):
			bpy.ops.object.delete()
		
		# bpy.context.scene.cursor_location.copy()
		# Create Tower
		TowerProps = bpy.context.window_manager.TowerProps
		run(bpy.context.scene.cursor_location.copy(), TowerProps.numVerts, TowerProps.radius,  TowerProps.totalHeight, TowerProps.crenaux,  TowerProps.poteaux,  TowerProps.door,  TowerProps.rembarde)
		
		return{"FINISHED"}
	
def removeFromCollection(collection, name):
	if (collection.__contains__(name)):
		collection[name].user_clear()
		collection.remove(collection[name])

def run(origin, numVerts, rad, totalHeight, crenaux, poteaux, door, rembarde):

	TowerProps = bpy.context.window_manager.TowerProps
	
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
	# removeFromCollection(bpy.data.textures, 'BrickTexture')
	cTex = bpy.data.textures.new('BrickTexture', type = 'IMAGE')
	cTex.image = imgbrick
	# removeFromCollection(bpy.data.materials, 'MaterialCube')
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
	
	# Clean previous Tower object
	# removeFromCollection(bpy.data.objects, 'tower.object')
	# removeFromCollection(bpy.data.meshes, 'tower.mesh')
	
	# bpy.context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'
		
	# Create Tower object
	bpy.context.scene.cursor_location = (0,0,0)
	bpy.ops.mesh.primitive_circle_add(vertices=numVerts, radius=rad)
	object = bpy.context.active_object
	# List of composed objects
	towerObjects = [object]
	# towerObjects.append(object)
	object.name = "tower.object"
	me = object.data
	me.name = "tower.mesh"
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
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude={"type":'EDGES'}, TRANSFORM_OT_translate={"value":(0, 0, step)})
		bpy.ops.transform.resize(value=(ratio, ratio, 1))
		innerRadius = innerRadius * 0.98
	# Base for Crenaux
	crenauxWidth = 1
	crenauxHeight = 1
	ratio = 1 - crenauxWidth / rad
	bpy.ops.mesh.extrude_region_move(MESH_OT_extrude={"type":'EDGES'}, TRANSFORM_OT_translate={"value":(0, 0, 0)})	
	bpy.ops.transform.resize(value=(ratio, ratio, 1))
	
	# Cap
	ratio = 1 - (1 / (rad-1))
	for i in range(int(rad-1)):
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude={"type":'EDGES'}, TRANSFORM_OT_translate={"value":(0, 0, 0)})	
		bpy.ops.transform.resize(value=(ratio, ratio, 1))
	
	# Hole
	bpy.ops.mesh.extrude_region_move(MESH_OT_extrude={"type":'EDGES'}, TRANSFORM_OT_translate={"value":(0, 0, -totalHeight)})	
	
	# Final Cap
	bpy.ops.mesh.extrude_region_move(MESH_OT_extrude={"type":'EDGES'}, TRANSFORM_OT_translate={"value":(0, 0, 0)})	
	bpy.ops.mesh.merge(type='CENTER', uvs=False)
	
	# Crenaux
	if (crenaux):	
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.context.scene.objects.active = towerObjects[0]
		indexes = range(len(bpy.context.active_object.data.faces))
		for i in indexes[numVerts*iterations:numVerts*iterations+numVerts] :
			if (i % 2):
				bpy.context.active_object.data.faces[i].select = True
				
		bpy.context.tool_settings.mesh_select_mode = [False, False, True]
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.extrude_region_move(MESH_OT_extrude={"type":'REGION'}, TRANSFORM_OT_translate={"value":(0, 0, crenauxHeight)})
	
	# UV unwrap
	bpy.ops.uv.smart_project()
	
	# i = 0
	# bpy.ops.object.mode_set(mode='OBJECT')
	# for f in me.faces:
		# if (i < numVerts):
			# f.material_index = 0
		# elif (i < numVerts * 2):
			# f.material_index = 1
		# i += 1
	
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
		
	# Door
	if (door):
		copyObject("asset.door")
		spinOneObject(numVerts, rad, (0,0,origin[2]), 0)
		towerObjects.append(bpy.context.active_object)
		
	# Join everything
	bpy.ops.object.select_all(action='DESELECT')
	for o in towerObjects:
		# print(o.name)
		o.select = True
	if (len(towerObjects) > 1):
		bpy.context.scene.objects.active = towerObjects[0]
		bpy.ops.object.join()
	bpy.context.active_object.location.x = origin.x
	bpy.context.active_object.location.y = origin.y
	bpy.context.active_object.location.z = origin.z
	bpy.context.scene.cursor_location = (0,0,0)
	
	# towerObjects = []
	
	# Add Camera to scene and set to view
	removeFromCollection(bpy.data.cameras, 'Camera')
	bpy.ops.object.camera_add()
	bpy.data.cameras["Camera"].clip_end = 1000.0
	bpy.data.objects["Camera"].name = "tmp.camera"
	bpy.ops.view3d.camera_to_view()
	bpy.data.worlds[0].light_settings.use_ambient_occlusion = True
	bpy.data.worlds[0].light_settings.use_environment_light = True
	bpy.context.scene.render.use_edge_enhance = True
	bpy.ops.render.render()

	return

def register():
	bpy.utils.register_class(TowerPanel)
	bpy.utils.register_class(OBJECT_OT_buildtower)
	bpy.utils.register_class(propertiesTowerProps)
	bpy.types.WindowManager.TowerProps = bpy.props.PointerProperty(type=propertiesTowerProps)


def unregister():
	bpy.utils.unregister_class(TowerPanel)
	bpy.utils.unregister_class(OBJECT_OT_buildtower)
	bpy.utils.unregister_class(propertiesTowerProps)
	del bpy.types.WindowManager.TowerProps

if __name__ == "__main__":
	register()
	#run((0,0,0))