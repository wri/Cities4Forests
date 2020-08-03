import numpy as np
import pandas as pd
import os
import geopandas as gpd
import glob
from geopandas.tools import overlay

#This script adds the Cities4Forest city properties to the watershed polygons

#Move to working directory
working_dir = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds'
os.chdir(working_dir)

#Load watersheds file
watersheds_file = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds/Cities4Forests-Watersheds-level5-withHonolulu/Cities4Forests-Watersheds-level5-withHonolulu.shp'
watersheds = gpd.read_file(watersheds_file)
#Load cities file
cities_file = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds/Cities4Forests Cities/Cities4Forests Cities.shp'
cities = gpd.read_file(cities_file)

#Spatially join files, which preserves the geometry of the first dataset, while adding the attributes of the right dataset
intersect = gpd.sjoin(watersheds, cities, how='left', op='contains')

#Save to new file
intersect.to_file('/Users/kristine/WRI/Cities4Forests/Defra_Watersheds/Cities4Forests-Watersheds-level5-withCities/Cities4Forests-Watersheds-level5-withCities.shp')

