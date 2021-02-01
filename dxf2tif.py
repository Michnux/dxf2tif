import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
# from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
#import wx
# import glob
# import re


import numpy as np
import matplotlib.tri as mtri
import matplotlib.pyplot as plt



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




def convert_dxf2img(name):

	doc = ezdxf.readfile(name)
	msp = doc.modelspace()
	# Recommended: audit & repair DXF document before rendering
	auditor = doc.audit()
	# The auditor.errors attribute stores severe errors,
	# which *may* raise exceptions when rendering.


	dict_vertex3D = {}
	dict_vertex2D = {}
	dict_vertex2Dto3D = {}
	n_vertex = 0


	x = []
	y = []
	z = []
	triangles = []


	for e in msp:

		if(e.dxftype()=='3DFACE'):
			# print_3DFACE(e)
			if e.dxf.vtx0 not in dict_vertex3D:
				dict_vertex3D[e.dxf.vtx0]=n_vertex
				dict_vertex2D[(e.dxf.vtx0[0], e.dxf.vtx0[1])]=n_vertex
				dict_vertex2Dto3D[(e.dxf.vtx0[0], e.dxf.vtx0[1])]=e.dxf.vtx0[2]
				x.append(e.dxf.vtx0[0])
				y.append(e.dxf.vtx0[1])
				z.append(e.dxf.vtx0[2])
				n_vertex += 1

			if e.dxf.vtx1 not in dict_vertex3D:
				dict_vertex3D[e.dxf.vtx1]=n_vertex
				dict_vertex2D[(e.dxf.vtx1[0], e.dxf.vtx1[1])]=n_vertex
				dict_vertex2Dto3D[(e.dxf.vtx1[0], e.dxf.vtx1[1])]=e.dxf.vtx1[2]
				x.append(e.dxf.vtx1[0])
				y.append(e.dxf.vtx1[1])
				z.append(e.dxf.vtx1[2])
				n_vertex += 1

			if e.dxf.vtx2 not in dict_vertex3D:
				dict_vertex3D[e.dxf.vtx2]=n_vertex
				dict_vertex2D[(e.dxf.vtx2[0], e.dxf.vtx2[1])]=n_vertex
				dict_vertex2Dto3D[(e.dxf.vtx2[0], e.dxf.vtx2[1])]=e.dxf.vtx2[2]
				x.append(e.dxf.vtx2[0])
				y.append(e.dxf.vtx2[1])
				z.append(e.dxf.vtx2[2])
				n_vertex += 1


			triangles.append([dict_vertex3D[e.dxf.vtx0], dict_vertex3D[e.dxf.vtx1], dict_vertex3D[e.dxf.vtx2]])




	triang = mtri.Triangulation(x, y, triangles)
	trifinder = triang.get_trifinder()


	xn = np.asarray(x)
	yn = np.asarray(y)
	zn = np.asarray(z)
	Cpoints = xn + 0.5*yn
	xmid = xn[triang.triangles].mean(axis=1)
	ymid = yn[triang.triangles].mean(axis=1)
	Cfaces = 0.5*xmid + ymid

	# plt.tripcolor(triang, Cpoints, edgecolors='k')
	# plt.show()

	interp = mtri.LinearTriInterpolator(triang, z)

	create_geotiff('blah.tif', x, y, interp)




convert_dxf2img('fossetotale_10082038.dxf')

