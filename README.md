Description of the Analytic:

A symplistic approach to generate a PlantHeight format from a .las file

PlantHeight is a raster format (.tif) with 1 band (DSM like), where the elevation at point (x,y) is the heigth of the vegetation from the ground.
The mothod to generate a PlantHeight is the following:
- generate a raster from the .las taking the maximum value of the point cloud at each point of the grid (supposedly the top of the trees)
- generate a raster from the .las taking the minimum value of the point cloud at each point of the grid (supposedly the ground level)
- differentiate both to obtain the PlandHeight


Usage

The PlantHeight format is needed for algos such as Tree counting.
Hence this analytic can be part of a workflow from .las to tree counting.


Parameters:

The analytic the .las file as input



