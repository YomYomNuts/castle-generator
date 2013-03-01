
		
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
		spinObject(lod, radius, sommet, 0.5)
		
		
		
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
			
		
		
		
		# Select last vertex
		# self.object.data.vertices[len(self.object.data.vertices) - 1].select = True
		

		# Translate all vertex with random proportion
		# bpy.ops.object.mode_set(mode='EDIT')
		# bpy.ops.transform.translate(value=(0.6, 0.6, 0.6), constraint_axis=(True, True, True), constraint_orientation='GLOBAL', mirror=False, proportional='ENABLED', proportional_edit_falloff='RANDOM', proportional_size=207.965, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=True)
		


		# prevVert = self.object.data.vertices[0]
		# for vertex in self.object.data.vertices :
			# if (vertex.co.z == prevVert.co.z) :
				# vertex.select = True
			# prev
			
# #######################################

		
		# bpy.ops.object.mode_set(mode='OBJECT')
		# bpy.ops.mesh.select_all(action = 'DESELECT')
		
		# print(dir(scn.objects))
		
		# print(type(helper))
		# print(dir(helper))
		
		# BOTTOM #
		
		# Scale
		# scaleBase = 0.9
		# bpy.ops.transform.resize(value=(scaleBase, scaleBase, 1))
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, heightBase * 0.25)})
		# Scale
		# bpy.ops.transform.resize(value=(scaleBase, scaleBase, 1))
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, heightBase * 0.75)})
		
		# OFFSET TOP #
		
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, heightRempart * 0.3)})
		# Scale
		# scaleRempart = (radius + offsetRempart) / radius
		# bpy.ops.transform.resize(value=(scaleRempart, scaleRempart, 1))
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, heightRempart * 0.9)})
			
		# GROUND #
		
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, 0)})
		# Scale
		# bpy.ops.transform.resize(value=(0.5, 0.5, 1))
		# Refresh object
		# bpy.ops.object.editmode_toggle()
		# bpy.ops.object.editmode_toggle()
		# Get positionGround from last vertex
		# positionGround = self.object.data.vertices[len(self.object.data.vertices) - 1].co.xyz
		# positionGround.x = position[0]
		# positionGround.y = position[1]
		
		# bpy.ops.object.vertex_group_add()
		# print(dir(self.object.data.vertices[0]))
		
		# WALLS #
		
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, heightWall)})
			
		# ROOF #
		
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, 0)})
		# Scale
		# bpy.ops.transform.resize(value=(0.7, 0.7, 1))
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, 6)})
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, 0)})
		# Scale
		# bpy.ops.transform.resize(value=(1.2, 1.2, 1))
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, 1)})
		# Extrude
		# bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":\
			# (0, 0, 5)})
		# Colapse vertices
		# bpy.ops.mesh.merge(type='CENTER', uvs=False)
		
		# BEVELS Operations #
		# bevelCircle(subdivision + 6, lod)
		# bevelCircle(subdivision + 5, lod)
		# bevelCircle(subdivision + 4, lod)
		# bevelCircle(subdivision + 3, lod)
		# bevelCircle(subdivision + 2, lod)
		
		# Setup context
		# self.object.select = False
		
		# REMPART #
		# copyObject("Rempart")
		# remparts = []
		# remparts = spinObject(lod, radius + offsetRempart * 0.5 - 1, positionGround, 0)
		
		# Setup context
		# bpy.ops.object.select_all(action='DESELECT')
		
		# PLANCHES #
		# copyObject("Planches")
		# planches = []
		# planches = spinObject(lod, radius + offsetRempart * 0.5 - 1, positionGround, 0.5)
		
		# DOOR #
		# copyObject("Door")
		# offset = 1
		# obj = bpy.context.active_object
		# Position
		# obj.location = \
			# (positionGround.x + math.cos(math.pi * 2 * (3 / lod)) * (radius * 0.5 + offset), \
			# positionGround.y + math.sin(math.pi * 2 * (3 / lod)) * (radius * 0.5 + offset), \
			# positionGround.z)
		# Orientation
		# obj.rotation_euler[2] = math.pi * 2 * (3 / lod)
		
		# JOIN Everything
		# for ob in remparts :
			# ob.select = True
		# for ob in planches :
			# ob.select = True
		# self.object.select = True
			
		# bpy.ops.object.join()