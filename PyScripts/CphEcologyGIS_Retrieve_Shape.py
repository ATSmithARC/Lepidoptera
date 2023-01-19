#Copenhagen Ecology Urban Model
#Data Retrieval - Shape
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