#Copenhagen Ecology Urban Model
#Data Retrieval
#R 4.2.1
# 1 - Install necessary packages:
from logging import lastResort
import os as o
from pyexpat.errors import XML_ERROR_INCOMPLETE_PE
import geopandas as gpd
from matplotlib.hatch import NorthEastHatch
import pandas as pd
import numpy as np
import pathlib as pl
import shapely.geometry as sg 
from pyproj import crs
import overpy
import requests as rq
import ee
import datetime
import geemap
import pygbif as gb

# Trigger the authentication flow and initialize the library.
#ee.Authenticate() #run once a week?
ee.Initialize()
print('EE Initialized...')

# 2 - Define Functions:
def bbox_from_geopts(pt_a, pt_b):
    if (pt_a[0] < pt_b[0]):
        xmin = pt_a[0]
        xmax = pt_b[0]
    else:
        xmin = pt_b[0]
        xmax = pt_a[0]
    if (pt_a[1] < pt_b[1]):
        ymin = pt_a[1]
        ymax = pt_b[1]
    else:
        ymin = pt_b[1]
        ymax = pt_a[1]
    bb_poly = sg.Polygon([(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)])
    return bb_poly

def getEVI(ee_image):
    EVI = ee_image.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))', {
            'NIR': ee_image.select('B8').divide(10000),
            'RED': ee_image.select('B4').divide(10000),
            'BLUE': ee_image.select('B2').divide(10000)
        }
    ).rename("EVI")
    ee_image = ee_image.addBands(EVI)
    return(ee_image)

# 3 - Set Working Directory:
o.chdir("C:/Users/ATSmi/OneDrive/Documents/CITA/7A/GIS")
o.getcwd()

# 4 - Define Data Retrieval BoundingBox:
a_geopt: tuple = (55.666103, 12.549321)
b_geopt: tuple = (55.698544, 12.630742)
bbox_polygon: sg.Polygon = bbox_from_geopts(a_geopt, b_geopt)
bbox_df: pd.DataFrame = {'geometry': [bbox_polygon]}
bbox_gdf: gpd.GeoDataFrame = gpd.GeoDataFrame(bbox_df, crs="EPSG:4326")
bbox_bnd: pd.DataFrame = bbox_gdf.bounds
north: float = bbox_bnd.iat[0,2]
south: float = bbox_bnd.iat[0,0]
east: float = bbox_bnd.iat[0,3]
west: float = bbox_bnd.iat[0,1]
print('BBox Initialized...')

# 5 - Get OSM. Query Open Street Maps (OSM) via Overpass API:
# headers = {
#     'Connection': 'keep-alive',
#     'sec-ch-ua': '"Google Chrome 80"',
#     'Accept': '*/*',
#     'Sec-Fetch-Dest': 'empty',
#     'User-Agent': 'EcologyGIS_DataRetrievl / atsmithpb @ github',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Origin': 'https://overpass-turbo.eu',
#     'Sec-Fetch-Site': 'cross-site',
#     'Sec-Fetch-Mode': 'cors',
#     'Referer': 'https://overpass-turbo.eu/',
#     'Accept-Language': '',
#     'dnt': '1',
# }
# query = f"""nwr({south},{west},{north},{east});out;"""
# data = {'data': query}
# print('Sending Query to Overpass...')
# response = rq.post('https://overpass-api.de/api/interpreter', headers=headers, data=data)
# print(f'Response: {response}')
# with open('myquery.osm', 'w', encoding ='utf-8') as f:
#     f.write(response.text)

# 6 - Retrieve Google EE Data within the BoundingBox as ee.Image objects
ee_date_start: ee.Date = ee.Date('2022-11-01')
ee_date_end: ee.Date = ee.Date('2022-11-16')
ee_bbox: ee.Geometry = ee.Geometry.BBox(west, south, east, north)
ee_bbox_poly: ee.Geometry = ee.Geometry.Polygon(ee_bbox._coordinates)
ee_bbox_rect: ee.Geometry = ee.Geometry.Rectangle(south, west, north, east)
ee_filter_dw: ee.Filter = ee.Filter.And(ee.Filter.bounds(ee_bbox),ee.Filter.date(ee_date_start, ee_date_end))
ee_filter_s2 = ee.Filter.And(ee.Filter.bounds(ee_bbox),ee.Filter.date(ee_date_start, ee_date_end), ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 35))
ee_ic_dw = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1').filter(ee_filter_dw)\
    .select('label')
ee_ic_s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filter(ee_filter_s2)\
    .select('B4', 'B3', 'B2', 'B8')
ee_i_dw: ee.Image = ee.Image(ee_ic_dw.first())
ee_i_s2: ee.Image = ee.Image(ee_ic_s2.first())
print('EE Data Recieved...')

# Calculate NDVI from S2 Red and NIR bands
ee_i_ndvi = ee_i_s2.normalizedDifference(['B8', 'B4'])

# Define color palettes
ee_palette_dw: list = [
    '419BDF', '397D49', '88B053', '7A87C6',
    'E49635', 'DFC35A', 'C4281B', 'A59B8F',
    'B39FE1']

# Define color palettes
ee_palette_ndvi: list = [
    '#d73027', '#f46d43', '#fdae61', '#fee08b',
    '#d9ef8b', '#a6d96a', '#66bd63', '#1a9850']

# Create RGB images based on visualization parameters
ee_i_dwviz = ee_i_dw.visualize(**{'bands': 'label','min': 0, 'max': 8, 'palette': ee_palette_dw})
ee_i_s2viz = ee_i_s2.visualize(**{'bands': ['B4', 'B3', 'B2'],'min': 0, 'max': 4000})
ee_i_ndviviz = ee_i_ndvi.visualize(**{'min': -1, 'max': 1, 'palette': ee_palette_ndvi})

#Get the most likely class probability.
# top1Prob = ee_i_dw.select(CLASS_NAMES).reduce(ee.Reducer.max())

#Create a hillshade of the most likely class probability on [0, 1];
#top1ProbHillshade = ee.Terrain.hillshade(top1Prob.multiply(100)).divide(255)

#Combine the RGB image with the hillshade.
#dwRgbHillshade = dwRgb.multiply(top1ProbHillshade)

print('EE Data Ready...')
ee_task_dw = ee.batch.Export.image.toDrive(image = ee_i_dwviz,  # an ee.Image object.
                                     region = ee_bbox_poly,  # an ee.Geometry object.
                                     description = 'EarthEngine_DyanmicWorld_CRS25832',
                                     folder = 'Data',
                                     fileNamePrefix = 'EE_DW_25832',
                                     scale = 10,
                                     crs = 'EPSG:25832')

ee_task_s2 = ee.batch.Export.image.toDrive(image = ee_i_s2viz,  # an ee.Image object.
                                     region = ee_bbox_poly,  # an ee.Geometry object.
                                     description = 'EarthEngine_Sentinal2_SurfaceReflect_CRS25832',
                                     folder = 'Data',
                                     fileNamePrefix = 'EE_S2SR_25832',
                                     scale = 10,
                                     crs = 'EPSG:25832')

ee_task_ndvi = ee.batch.Export.image.toDrive(image = ee_i_ndviviz,  # an ee.Image object.
                                     region = ee_bbox_poly,  # an ee.Geometry object.
                                     description = 'EarthEngine_Normalized-Difference-Vegitation-Index_CRS25832',
                                     folder = 'Data',
                                     fileNamePrefix = 'EE_NDVI_25832',
                                     scale = 10,
                                     crs = 'EPSG:25832')

ee_task_ndvi.start()
ee_task_dw.start()
ee_task_s2.start()
print('Images Exported Successfully...')

#api = overpy.Overpass()
#results = api.parse_xml(response.text)

#gdf_buildings = gpd.read_file("DATA/1084_SHAPE_UTM32-EUREF89/FOT/BYGNINGER/BYGNING.shp")
#print("Buildings .shp Loaded...")
#gdf_treeloc = gpd.read_file("DATA/1084_SHAPE_UTM32-EUREF89/FOT/NATUR/TRAE.shp")
#print("Tree Locations .shp Loaded...")
#gdf_treebasis = gpd.read_file("DATA/trae_basis/trae_basis.shp")
#print("Tree Basis .shp Loaded...")
#gdf_greenarea = gpd.read_file("DATA/park_groent_omr_oversigtskort/park_groent_omr_oversigtskort.shp")
#print("Green Areas .shp Loaded...")
#gdf_garden = gpd.read_file("DATA/storbyhaver/storbyhaver.shp")
#print("Gardens .shp Loaded...")
#gdf_gardenloc = gpd.read_file("DATA/1084_SHAPE_UTM32-EUREF89/FOT/NATUR/GARTNERI.shp")
#print("Garden Locations .shp Loaded...")
#gdf_uselimits = gpd.read_file("DATA/1084_SHAPE_UTM32-EUREF89/FOT/NATUR/BRUGSGRAENSE.shp")
#print("Use Limits .shp Loaded...")



#    test
# Landsat8 = ee.Image('LANDSAT/LC08/C01/T1_TOA/LC08_170052_20170108')\
#     .select('B4', 'B3', 'B2')
# region = ee.Geometry.Rectangle(37.07, 11.50, 37.39, 11.82)
# task = ee.batch.Export.image.toDrive(**{
#     'image': Landsat8,
#     'description' : 'imageToDrive',
#     'folder': 'Example_Folder',
#     'scale': 30,
#     'region': region.getInfo()['coordinates']
# })
# task.start()

