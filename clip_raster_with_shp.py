import fiona
import rasterio
import rasterio.mask
from rasterio import features
import numpy as np


src_raster_path = r'/Users/anushkafernando/code/geospatial-data/data/2015.tif'

shp_file_path = '/Users/anushkafernando/code/geospatial-data/data/AOI/AOI.shp'

output_raster_path = '/Users/anushkafernando/code/geospatial-data/outputs/clipped_raster_new.tif'

with fiona.open(shp_file_path, "r") as shapefile:

    shapes = [feature["geometry"] for feature in shapefile]
    print(features.is_valid_geom(shapes[0]))

input = rasterio.open(src_raster_path) 
# use nodata = .. so that the contents of the graph are only inside the boundary.
out_image, out_transform = rasterio.mask.mask(input, shapes, nodata=np.nan, crop=True)
out_meta = input.meta.copy()

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 }) #"transform": out_transform


with rasterio.open(output_raster_path, "w", **out_meta) as dest:
    dest.write(out_image)