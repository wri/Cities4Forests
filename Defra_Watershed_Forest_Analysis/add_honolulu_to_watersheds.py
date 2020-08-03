import numpy as np
import pandas as pd
import os
import geopandas as gpd
import glob

#This script adds the island of Honolulu to our Cities4Forests Watersheds

#Move to working directory
working_dir = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds'
os.chdir(working_dir)

#Load watersheds
watershed_file = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds/Cities4Forests-Watersheds-level5/Cities4Forests-Watersheds-level5.shp'
watersheds = gpd.read_file(watershed_file)

#Load Honolulu island, this was taken from GADM Boundaries (version 3.6) (https://gadm.org/index.html)
honolulu = gpd.read_file(honolulu_file)
honolulu_file = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds/honolulu'

#Save only geometry from Honolulu
honolulu = honolulu[['geometry']]
#Select columns from watersheds
watersheds_columns = ['HYBAS_ID', 'NEXT_DOWN', 'NEXT_SINK', 'MAIN_BAS', 'DIST_SINK', 'DIST_MAIN', 'SUB_AREA', 
                        'UP_AREA', 'PFAF_ID', 'ENDO', 'COAST', 'ORDER', 'SORT']
#Set watershed properties for Honolulu to be a unique ID, not present in the watersheds data
for column in watersheds_columns:
    honolulu[column] = -9999

#Create merged dataframe by concating watersheds and Honolulu dataframe
gdf = gpd.GeoDataFrame( pd.concat([watersheds,honolulu], ignore_index=True), crs=watersheds.crs)
#Select desired columns
gdf = gdf[['HYBAS_ID','MAIN_BAS','PFAF_ID','geometry']]
#Save to file
gdf.to_file('/Users/kristine/WRI/Cities4Forests/Defra_Watersheds/Cities4Forests-Watersheds-level5/Cities4Forests-Watersheds-level5-withHonolulu/Cities4Forests-Watersheds-level5-withHonolulu.shp')