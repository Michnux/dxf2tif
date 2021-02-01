import rasterio as rio
# from rasterio.warp import transform
from rasterio.transform import Affine

from matplotlib import pyplot

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm

from tqdm import tqdm
# def LonLat2uv(Lon, Lat, dataset):


# 	# #coord map
# 	# x, y = transform({'init': 'EPSG:4326'}, dataset.crs,  [Lon] , [Lat])
# 	# #coord image
# 	pixel_y, pixel_x = ~dataset.transform*(x[0], y[0]) #le transpose ici n'est pas super clean
# 	# pixel_y, pixel_x = ~dataset.transform*(Lon, Lat) #le transpose ici n'est pas super clean

# 	return pixel_x, pixel_y


def create_geotiff(raster_name, x, y, interp):


	x_min = min(x)
	x_max = max(x)
	y_min = min(y)
	y_max = max(y)


	print(x_min, x_max, y_min, y_max)


	resolution = 4 #m
	new_ds_width = int((x_max-x_min)/resolution)
	new_ds_height = int((y_max-y_min)/resolution)



	print('frame size', new_ds_width, new_ds_height)

	crs = {'init': 'EPSG:27563'}
	xy2pix = rio.transform.from_bounds(x_min, y_min, x_max, y_max, new_ds_width, new_ds_height)

	# xy2pix = Affine.translation(x_max, y_min) * Affine.scale(  (x_max-x_min)/new_ds_width, (y_max-y_min)/new_ds_height)


	#DSM like raster
	new_dataset = rio.open('./'+raster_name, 'w', driver='GTiff',
									nodata = 0,
									height=new_ds_height, width=new_ds_width,
									count=1, dtype=rio.float32,
									crs=crs, transform=xy2pix)

	DSM = np.zeros((new_ds_height, new_ds_width, 1), dtype=np.float32)
	mask = np.zeros((new_ds_height, new_ds_width, 1), dtype=np.uint8)

	for u in tqdm(range(new_ds_width)):
		for v in range(new_ds_height):

			x, y = xy2pix*(u, v)
			z = interp(x, y)
			if not z.mask:
				DSM[v, u] = z
				mask[v, u] = 255


	new_dataset.write_mask(mask[:,:,0])
	new_dataset.write(DSM[:,:,0], 1)
	new_dataset.close()


	plt.imshow(DSM)
	plt.show()


if __name__ == "__main__":

	pass
    # scatter_geotiff('gsp.tif', data['longitude'].tolist(), data['latitude'].tolist(), data['gear'].tolist(), radius = 2)
