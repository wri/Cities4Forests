import numpy as np
import pandas as pd
import os
import geopandas as gpd

#This script appends information on the ADM1 region that contains each Cities4Forest city and saves it to a new file.

#Change to directory
working_dir = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds'
os.chdir(working_dir)

#Load city locations
city_locations_file = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds/Cities4Forests Watersheds/Cities4Forests Watersheds.shp'
city_locations = gpd.read_file(city_locations_file)

#Load adm1 polygons
adm1_file = '/Users/kristine/WRI/gadm36_levels_shp/gadm36_1.shp'
adm1 = gpd.read_file(adm1_file)

#Spatially join files, which preserves the geometry of the first dataset, while adding the attributes of the right dataset
merged_files = gpd.sjoin(city_locations, adm1[['NAME_0','NAME_1', 'geometry']], how='left', op='intersects')

#Select desired columns
merged_files = merged_files[['City', 'City Simpl', 'Country', 'Watersheds', 'Latitude', 'Longitude', 'Tree Cover', 'Biomass Lo', 
    'Restoratio', 'Carbon Seq', 'Aqueduct W', 'Overlaps w', 'Watershed','NAME_0', 'NAME_1']]

#Save to a CSV file
merged_files.to_csv('Cities4Forests Watersheds with ADM1.csv',index=False)

