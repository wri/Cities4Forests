import numpy as np
import pandas as pd
import os
import geopandas as gpd
import glob

#This script merges regional watershed files to one global file

#Move to working directory
working_dir = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds'
os.chdir(working_dir)

#List all level-5 region files
shapefiles = glob.glob('hydrosheds-level5/*.shp')

#Create empty dataframe
gdf = gpd.GeoDataFrame()
#Loop through region shapefiles
for shapefile in shapefiles:
    print(shapefile)
    #Read file
    region_gdf = gpd.read_file(shapefile)
    #Append to dataframe
    gdf = gpd.GeoDataFrame( pd.concat([gdf,region_gdf], ignore_index=True), crs=region_gdf.crs)

#Save to new file
gdf.to_file('hydrosheds-level5-merged/hydrosheds-level5-merged.shp')