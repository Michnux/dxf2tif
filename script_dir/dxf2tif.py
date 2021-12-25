import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
import json

import numpy as np
import matplotlib.tri as mtri
import matplotlib.pyplot as plt

import os


from CreateTiff import *




def print_entity(e):
	print("LINE on layer: %s\n" % e.dxf.layer)
	print("start point: %s\n" % e.dxf.start)
	print("end point: %s\n" % e.dxf.end)


def print_3DFACE(e):
	print("3DFACE on layer: %s\n" % e.dxf.layer)
	print("vtx0: %s\n" % e.dxf.vtx0)
	print("vtx1: %s\n" % e.dxf.vtx1)
	print("vtx2: %s\n" % e.dxf.vtx2)
	print("vtx3: %s\n" % e.dxf.vtx3)




def dxf2tif(file_path, grid_size, WORKING_DIR):


	x = []
	y = []
	z = []
	triangles = []
	crs = None

	file_path_str = str(file_path)

	if file_path_str.split('.')[-1]=='dxf':

		doc = ezdxf.readfile(file_path)
		msp = doc.modelspace()
		# Recommended: audit & repair DXF document before rendering
		auditor = doc.audit()
		# The auditor.errors attribute stores severe errors,
		# which *may* raise exceptions when rendering.

		dict_vertex3D = {}
		# dict_vertex2D = {}
		# dict_vertex2Dto3D = {}
		n_vertex = 0

		for e in msp:

			# print(e.dxftype())
			if(e.dxftype()=='3DFACE'):
				# print_3DFACE(e)
				if e.dxf.vtx0 not in dict_vertex3D:
					dict_vertex3D[e.dxf.vtx0]=n_vertex
					# dict_vertex2D[(e.dxf.vtx0[0], e.dxf.vtx0[1])]=n_vertex
					# dict_vertex2Dto3D[(e.dxf.vtx0[0], e.dxf.vtx0[1])]=e.dxf.vtx0[2]
					x.append(e.dxf.vtx0[0])
					y.append(e.dxf.vtx0[1])
					z.append(e.dxf.vtx0[2])
					n_vertex += 1

				if e.dxf.vtx1 not in dict_vertex3D:
					dict_vertex3D[e.dxf.vtx1]=n_vertex
					# dict_vertex2D[(e.dxf.vtx1[0], e.dxf.vtx1[1])]=n_vertex
					# dict_vertex2Dto3D[(e.dxf.vtx1[0], e.dxf.vtx1[1])]=e.dxf.vtx1[2]
					x.append(e.dxf.vtx1[0])
					y.append(e.dxf.vtx1[1])
					z.append(e.dxf.vtx1[2])
					n_vertex += 1

				if e.dxf.vtx2 not in dict_vertex3D:
					dict_vertex3D[e.dxf.vtx2]=n_vertex
					# dict_vertex2D[(e.dxf.vtx2[0], e.dxf.vtx2[1])]=n_vertex
					# dict_vertex2Dto3D[(e.dxf.vtx2[0], e.dxf.vtx2[1])]=e.dxf.vtx2[2]
					x.append(e.dxf.vtx2[0])
					y.append(e.dxf.vtx2[1])
					z.append(e.dxf.vtx2[2])
					n_vertex += 1


				triangles.append([dict_vertex3D[e.dxf.vtx0], dict_vertex3D[e.dxf.vtx1], dict_vertex3D[e.dxf.vtx2]])



	elif file_path_str.split('.')[-1]=='json':
		
		alteia_converted_dxf = None
		with open(file_path) as f:
			alteia_converted_dxf = json.load(f)

		dict_vertex3D = {}
		n_vertex = 0

		for feat in alteia_converted_dxf["features"]:

			#check: features are triangles
			if feat["geometry"]["type"]=="Polygon" and len(feat["geometry"]["coordinates"][0])==4:

				p=[]

				for k in range(3):
					#if we haven't seen the vertex before, let's add it to the list
					p.append((tuple(feat["geometry"]["coordinates"][0][k][0:3])))

					if p[k] not in dict_vertex3D:
						dict_vertex3D[p[k]]=n_vertex
						x.append(p[k][0])
						y.append(p[k][1])
						z.append(p[k][2])
						n_vertex+=1

				triangles.append([dict_vertex3D[p[0]], dict_vertex3D[p[1]], dict_vertex3D[p[2]]])
				# print(triangles)

		crs_json = alteia_converted_dxf.get("crs")

		if "CRS84" in crs_json['properties']['name']:
			crs = {'init': 'EPSG:4326'}



	triang = mtri.Triangulation(x, y, triangles)
	# trifinder = triang.get_trifinder()
	# xn = np.asarray(x)
	# yn = np.asarray(y)
	# zn = np.asarray(z)
	# Cpoints = xn + 0.5*yn
	# xmid = xn[triang.triangles].mean(axis=1)
	# ymid = yn[triang.triangles].mean(axis=1)
	# Cfaces = 0.5*xmid + ymid

	# plt.tripcolor(triang, Cpoints, edgecolors='k')
	# plt.show()

	interp = mtri.LinearTriInterpolator(triang, z)

	create_geotiff(WORKING_DIR / 'output.tif', x, y, interp, grid_size, crs)





if __name__ == "__main__":

	from pathlib import Path
	WORKING_DIR = Path('../work_dir').resolve()
	# dxf2tif('../work_dir/fossetotale_10082038.dxf', 1, WORKING_DIR)
	dxf2tif(WORKING_DIR / 'fossetotale_10082038.json', 1, WORKING_DIR)

