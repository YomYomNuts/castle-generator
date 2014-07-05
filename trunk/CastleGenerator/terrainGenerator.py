import bpy
import os
import random
import math
from utils import *

class TerrainGenerator:
	def __init__(self, numBuissons):
		# Terrain
		bpy.ops.object.select_all(action='DESELECT')
		copyObject("asset.terrain")
		objectTerrain = bpy.context.active_object
		objectTerrain.name = "tmp.terrain"
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")
		buissons = [objectTerrain]
		randomListe = RandomBetween(0, len(objectTerrain.data.vertices) - 1)
		for i in randomListe[:numBuissons]:
			copyObject("asset.buisson")
			objectBuisson = bpy.context.active_object
			objectBuisson.name = "tmp.buisson"
			objectBuisson.location = objectTerrain.data.vertices[i].co
			randomScale = 0.5 + random.random() * 0.5
			objectBuisson.scale[0] = objectBuisson.scale[1] = objectBuisson.scale[2] = randomScale
			objectBuisson.rotation_euler[2] = random.random() * 360
			buissons.append(objectBuisson)
		bpy.context.scene.objects.active = buissons[0]
		for o in buissons:
			o.select = True
		bpy.ops.object.join()