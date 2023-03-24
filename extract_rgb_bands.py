import rasterio
from rasterio.plot import show

import numpy

def normalize(x, lower, upper):
    """Normalize an array to a given bound interval"""

    x_max = numpy.max(x)
    x_min = numpy.min(x)

    m = (upper - lower) / (x_max - x_min)
    x_norm = (m * (x - x_min)) + lower

    return x_norm

# Normalize each band separately


#to display RGB
dataset = rasterio.open('/Users/anushkafernando/code/geospatial-data/data/2020.tif')
data = dataset.read([4,3,2])
data_norm = numpy.array([normalize(data[i,:,:], 0, 255) for i in range(data.shape[0])])
data_rgb = data_norm.astype("uint8")

with rasterio.open(
    '/Users/anushkafernando/code/geospatial-data/outputs/2020_true_color_clipped.tif',
    'w',
    driver='GTiff',
    height=data_rgb.shape[1],
    width=data_rgb.shape[2],
    count=data_rgb.shape[0],
    dtype=data_rgb.dtype,
    crs=dataset.crs,
    transform=dataset.transform
) as dst:
    dst.write(data_rgb)