import time
import numpy as np
import rasterio
from rasterio import Affine as A
from rasterio.warp import calculate_default_transform, reproject, Resampling
import uuid
import os
import math

# PART 1
#
# folder_path = 'C:/Users/ATSmi/OneDrive/Documents/CITA/7A/GIS/DATA/DTM_617_72_TIF_UTM32-ETRS89'
# file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
# file_paths = [os.path.join(folder_path, file) for file in file_list]
# path = 'C:/Users/ATSmi/OneDrive/Documents/CITA/7A/GIS/DATA/DTM_617_72_TIF_UTM32-ETRS89/DTM_1km_6170_720.tif'
# dataset = rasterio.open(path)
# print('Reprojecting Images...')
# src_crs = dataset.crs # original CRS
# dst_crs = 'EPSG:3857' # desired CRS
# # loop through all GeoTiffs in a directory
# for filepath in file_paths:
#     with rasterio.open(filepath) as src:
#         transform, width, height = calculate_default_transform(src.crs, dst_crs, src.width, src.height, *src.bounds)
#         kwargs = src.meta.copy()
#         kwargs.update({
#             'crs': dst_crs,
#             'transform': transform,
#             'width': width,
#             'height': height
#         })

#         # write the reprojected GeoTiff to a new file
#         with rasterio.open(f'{filepath}_reprojected.tif', 'w', **kwargs) as dst:
#             reproject(
#                 source=rasterio.band(src, 1),
#                 destination=rasterio.band(dst, 1),
#                 src_transform=src.transform,
#                 src_crs=src.crs,
#                 dst_transform=transform,
#                 dst_crs=dst_crs,
#                 resampling=Resampling.nearest
#             )                
# print('Done!')

# PART 2
#
# Maps a float32 number from a source domain to a target domain where values represent height in m.
# Mapbox supports elevations between 0-10000m, but source data only exists between -10 and 190m so we map the data
def map_domain(value):
    if(value < -10):
        value = -10
    if(value > 190):
        value = 190
    source_min = -10
    source_max = 190
    target_min = 0
    target_max = 200
    mapped_value = (value - source_min) * (target_max - target_min) / (source_max - source_min) + target_min
    return mapped_value


def calculate_R(height):
    R = int(10 * (height + 10000) // 256 // 256 % 256)
    return R

# Solves for G 
def calculate_G(height):
    G = int(10 * (height + 10000) // 256 % 256)
    return G

# Solves for B
def calculate_B(height):
    B = int(10 * (height + 10000) % 256)
    return B

def terrarium_R(height):
    height += 32768
    return int(math.floor(height/256))

def terrarium_G(height):
    height += 32768
    return int(math.floor(height % 256))

def terrarium_B(height):
    height += 32768
    return math.floor((height - math.floor(height)) * 256)


# Maps a float32 elevation within the domain [-10.0,190.0] to unsigned int8 R Channel [0,255]
# Useful for HDR tonemapping float32 greyscale image to 8bit RGB
def float32_to_r(f32):
    #f32_mapped = map_domain(f32)
    r = terrarium_R(f32)
    return r

def float32_to_g(f32):
    #f32_mapped = map_domain(f32)
    g = terrarium_G(f32)
    return g

def float32_to_b(f32):
    #f32_mapped = map_domain(f32)
    b = terrarium_B(f32)
    return b

def float32_to_a(f32):
    return int(f32 != -9999.0) * 255

folder_path = 'C:/Users/ATSmi/OneDrive/Documents/CITA/7A/GIS/DATA/DTM_617_72_TIF_UTM32-ETRS89_reprojected'
file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
file_paths = [os.path.join(folder_path, file) for file in file_list]
print('Tonemapping Images...')
for filepath in file_paths:
    with rasterio.open(filepath) as dst:
        kwargs = dst.meta.copy()
        kwargs.update({
            'nodata' : 0,
            'dtype' : rasterio.uint8,
            'count' : 4
        })

        datafloat = dst.read(1)
        data_r = np.vectorize(float32_to_r)(datafloat)
        data_g = np.vectorize(float32_to_g)(datafloat)
        data_b = np.vectorize(float32_to_b)(datafloat)
        data_a = np.vectorize(float32_to_a)(datafloat)

        # write the tonemapped GeoTiff to a new file
        with rasterio.open(f'{filepath}_tonemapped5.tif', 'w', **kwargs) as tmp:
            tmp.write(data_r, 1)
            tmp.write(data_g, 2)
            tmp.write(data_b, 3)
            tmp.write(data_a, 4)
        print('Finished Image....')

print('Finished all Images!')


































































































