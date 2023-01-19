# Copenhagen Ecology Urban Environment Model
# Data Retrieval - GeoTiff / CSV

# Install necessary packages:
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
import pygbif as gbif
import sqlite3 as sql

# Authenticate & Initialize Google Earth Engine
#ee.Authenticate() #run once a week?
ee.Initialize()
print('EE Initialized...')

# 1 - Functions:
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

def addCoord(feature):
    point:ee.Geometry = ee.Geometry.Point(coords=[feature.get(property='x'),feature.get(property='y')])
    return feature.setGeometry(geometry=point)

def projCoord(feature):
    point:ee.Geometry = feature.geometry().transform(proj="EPSG:25832")
    return feature.setGeometry(geometry=point)

def dictfromfeature(feature, previousresult):
    previousresult = [].append(previousresult)
    jsonfeature: str = feature.getInfo()
    attr = jsonfeature['properties']
    attr['geometry'] = feature['geometry']  # GeoJSON Feature!
    return previousresult.append(attr)

def dffromfc(fc):
    # Convert a FeatureCollection into a pandas DataFrame
    dictarr = fc.iterate(dictfromfeature)
    df = gpd.GeoDataFrame(dictarr)
    return df

#2 - Create Sqlite Database
conn = sql.connect('lepidoptera.db')
c = conn.cursor()

# 3 - Set Working Directory:
o.chdir("C:/Users/ATSmi/OneDrive/Documents/CITA/7A/GIS")
o.getcwd()

# 4 - Define Data Retrieval GeoBoundingBox:
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
bbox_gdf_crs: gpd.GeoDataFrame = bbox_gdf.to_crs(crs="EPSG:25832")
bbox_bnd_crs: pd.DataFrame = bbox_gdf_crs.bounds
north_crs: float = bbox_bnd_crs.iat[0,2]
south_crs: float = bbox_bnd_crs.iat[0,0]
east_crs: float = bbox_bnd_crs.iat[0,3]
west_crs: float = bbox_bnd_crs.iat[0,1]
print('BBox Initialized...')

#5 - Retrieve OSM Data. Query Open Street Maps (OSM) via Overpass API:
headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Google Chrome 80"',
    'Accept': '*/*',
    'Sec-Fetch-Dest': 'empty',
    'User-Agent': 'EcologyGIS_DataRetrievl / atsmithpb @ github',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://overpass-turbo.eu',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://overpass-turbo.eu/',
    'Accept-Language': '',
    'dnt': '1',
}
query = f"""nwr({south},{west},{north},{east});out;"""
data = {'data': query}
print('Sending Query to Overpass...')
response = rq.post('https://overpass-api.de/api/interpreter', headers=headers, data=data)
print(f'Response: {response}')
with open('myquery.csv', 'w', encoding ='utf-8') as f:
    f.write(response.text)

# 6 - Retrieve Google EarthEngine Data within the BoundingBox as ee.Image objects
print('Downloading Earth Engine Data...')
ee_date_start: ee.Date = ee.Date('2022-08-01')
ee_date_end: ee.Date = ee.Date('2022-08-30')
ee_bbox: ee.Geometry = ee.Geometry.BBox(west, south, east, north)
ee_bbox_poly: ee.Geometry = ee.Geometry.Polygon(ee_bbox._coordinates)
ee_bbox_poly_crs: ee.Geometry = ee.Geometry.Polygon(ee_bbox._coordinates, proj='EPSG:25832')
ee_filter_s2:ee.Filter = ee.Filter.And(ee.Filter.bounds(ee_bbox),ee.Filter.date(ee_date_start, ee_date_end), ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 35)) 
ee_imgc_s2: ee.ImageCollection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filter(ee_filter_s2)\
    .select(['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B9','B11','B12','AOT','WVP','SCL','TCI_R','TCI_G','TCI_B'])
ee_img_s2: ee.Image = ee.Image(ee_imgc_s2.first())
ee_img_s2_index = ee_img_s2.get('system:index')
ee_filter_dw: ee.Filter = ee.Filter.eq('system:index', ee_img_s2_index)
ee_imgc_dw: ee.ImageCollection = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1').filter(ee_filter_dw)
ee_img_dw: ee.Image = ee.Image(ee_imgc_dw.first())
ee_img_compile_1: ee.Image = ee_img_s2.addBands(srcImg=ee_img_dw, overwrite=False)
ee_img_evi: ee.Image = getEVI(ee_img_s2).select('EVI')
ee_img_normdiff: ee.Image = ee_img_s2.normalizedDifference(['B8','B4'])
ee_img_ndvi: ee.Image = ee_img_normdiff.rename(['NDVI'])
ee_img_compile_2: ee.Image = ee_img_compile_1.addBands(srcImg=ee_img_evi,overwrite=True)
ee_img_compile_3: ee.Image = ee_img_compile_2.addBands(srcImg=ee_img_ndvi,overwrite=False)
ee_img_coords: ee.Image = ee_img_compile_3.pixelCoordinates('EPSG:25832')
ee_img_compile_4: ee.Image = ee_img_compile_3.addBands(srcImg=ee_img_coords,overwrite=False)
ee_fc_compile: ee.FeatureCollection = ee_img_compile_4.sample(region=ee_bbox_poly,scale=10,projection='EPSG:25832',geometries=True)
ee_fc_compile_coords: ee.FeatureCollection = ee_fc_compile.map(projCoord)
ee_df: gpd.GeoDataFrame = dffromfc(ee_fc_compile_coords)
print(ee_df)
# Export CSV to Google Drive 
ee_gdf: gpd.GeoDataFrame = dffromfc(ee_fc_compile_coords)
ee_img_compile_4_viz = ee_img_compile_4.visualize(**{'bands': ['B4', 'B3', 'B2'],'min': 0, 'max': 4000})
ee_task_exportcsv = ee.batch.Export.table.toDrive(collection=ee_fc_compile_coords,description='EE_TabletoShp',folder='Data',fileNamePrefix='DATA_25832', fileFormat='CSV')
ee_task_exportcsv.start()
print('Earth Engine Data Exported to Google Drive')

# 7 - Retrieve GBIF Data as GeoDataFrame
gbif_bbox_poly: str = f'POLYGON(({west} {south}, {east} {south}, {east} {north}, {west} {north}, {west} {south}))'
gbif_fields = [
                            'key',
                            'kingdom',
                            'genus',
                            'species',
                            'genericName',
                            'iuncRedListCategory',
                            'decimalLongitude',
                            'decimalLatitude',
                            'coordinateUncertaintyInMeters',
                            'year',
                            'month',
                            ''
                            'habitat']
print('Downloading GBIF Data...')
current_offset: int = 0
current_limit: int = 300
gbif_loop: int = 0
gbif_dflist_occ_pages: list = []
while gbif_loop < 5:
    print(f"GBIF: Downloading Page {gbif_loop}...")
    gbif_dict_occ_page: dict = gbif.occurrences.search(geometry=gbif_bbox_poly, limit=current_limit, offset=current_offset)
    print("GBIF: Adding Page to Dataframe... ")
    gbif_df_occ_page: pd.DataFrame = pd.DataFrame.from_dict(gbif_dict_occ_page['results'], orient='columns')
    print("GBIF: Filtering Dataframe... ")
    gbif_df_occ_page_filt: pd.DataFrame = gbif_df_occ_page.filter(items=gbif_fields)  
    print("GBIF: Adding Dataframe to List... ")
    gbif_dflist_occ_pages.append(gbif_df_occ_page_filt)
    current_offset += current_limit
    gbif_loop += 1
print("GBIF: Formatting Dataframe")
gbif_df_occ: pd.DataFrame = pd.concat(gbif_dflist_occ_pages)
gbif_strlist_wkt: list = "POINT (" + gbif_df_occ.decimalLatitude.map(str) + " " + gbif_df_occ.decimalLongitude.map(str) + ")"
del gbif_df_occ['decimalLatitude']
del gbif_df_occ['decimalLongitude']
gbif_gs_geo: gpd.GeoSeries = gpd.GeoSeries.from_wkt(data=gbif_strlist_wkt, crs='EPSG:4326')
gbif_gs_geo_tocrs: gpd.GeoSeries = gbif_gs_geo.to_crs("EPSG:25832")
gbif_gdf: gpd.GeoDataFrame = gpd.GeoDataFrame(data=gbif_df_occ, geometry=gbif_gs_geo_tocrs, crs="EPSG:25832")
gbif_gdf['modelID']= 1
gbif_gdf.to_csv(path_or_buf='C:/Users/ATSmi/Desktop/gbif_gdf.csv', index=False)
gbif_gdf.to_postgis()

#8a - Retrieve DTM and DSM Data from Copenhagen Minicipality WCS API (Size Limit of 9000x9000 pixels)
#Example URL: 'https://api.dataforsyningen.dk/dhm_wcs_DAF?SERVICE=WCS&REQUEST=GetCoverage&COVERAGE=dhm_terraen&CRS=EPSG:25832&BBOX=723216.1577610369,6174630.958749102,728145.165522719,6178503.884337852&WIDTH=4929&HEIGHT=3873&FORMAT=GTiff&token=643fd60fada7605aa34679b7d9650c08'
wcs_source: str = 'https://api.dataforsyningen.dk/dhm_wcs_DAF?SERVICE=WCS&REQUEST=GetCoverage'
wcs_dtm_coverage: str = '&COVERAGE=dhm_terraen'
wcs_dsm_coverage: str = '&COVERAGE=dhm_overflade'
wcs_crs:str = '&CRS=EPSG:25832'
wcs_bbox:str = f'&BBOX=723216.1577610369,6174630.958749102,728145.165522719,6178503.884337852'
wcs_width:str = '&WIDTH=4929'
wcs_height:str = '&HEIGHT=3873'
wcs_format:str = '&FORMAT=GTiff'
wcs_token:str = '&token=643fd60fada7605aa34679b7d9650c08'
wcs_dtm_url: str = f'{wcs_source}{wcs_dtm_coverage}{wcs_crs}{wcs_bbox}{wcs_width}{wcs_height}{wcs_token}'
dtm = rq.get()

#8b - Retrieve DTM and DSM Data from Geotiff Collection
#C:\Users\ATSmi\OneDrive\Documents\CITA\7A\GIS\DATA\DSM_617_72_TIF_UTM32-ETRS89
#C:\Users\ATSmi\OneDrive\Documents\CITA\7A\GIS\DATA\DTM_617_72_TIF_UTM32-ETRS89