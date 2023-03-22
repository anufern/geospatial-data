import shapely
import rasterio
from rasterio.features import shapes
from rasterio.plot import show
from rasterio.mask import mask
import numpy as np

input_tiff = "/Users/anushkafernando/code/geospatial-data/data/2015.tif"
input_shp_tiff = "/Users/anushkafernando/code/geospatial-data/data/2020.tif"
src = rasterio.open(input_shp_tiff)
band = src.read(7)
band = band.astype('int32')
result = shapes(band, transform=src.transform, connectivity=8)
l = [shapely.geometry.shape(x[0]) for x in result]
print('l', l)
with rasterio.open(input_tiff) as ras:
  out_image, out_transform = mask(ras, l, crop=True)
  out_meta=ras.meta.copy()
  # Check that after the clip, the image is not empty
  test = out_image[~np.isnan(out_image)]

  if test[test>0].shape[0] == 0:
    passaran = 0
  else:
    passaran = 1

  # convert the zeros into NaN

out_meta.update({
    "driver":"Gtiff",
    "height":out_image.shape[1],
    "width":out_image.shape[2],
    "transform":out_transform
})
              
with rasterio.open('/Users/anushkafernando/code/geospatial-data/outputs/clip.tif','w',**out_meta) as dst:
    dst.write(out_image)

_f = "/Users/anushkafernando/code/geospatial-data/outputs/clip.tif"
img = rasterio.open(_f)
show(img)
