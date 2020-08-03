from time import sleep
import json
from flask import Flask, request, abort

from os import getenv
import sys
import glob
import zipfile
import os
import numpy as np
import rasterio
import pandas as pd
from rasterstats import zonal_stats
import fiona
from geojson import Point, Feature, FeatureCollection, dump
import geopandas as gpd
import requests
from fiona.crs import from_epsg

#Load watersheds shapefile
watersheds_shapefile = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds/Cities4Forests-Watersheds-level5-withHonolulu/Cities4Forests-Watersheds-level5-withCities-cea.shp'

#Download sequestration estimate geotiffs from AWS
url = 'https://gfw-files.s3.amazonaws.com/ai4e/{}'#.format(geotiff_name)

def download_tif_from_aws(geotiff_name, download_url):
    r = requests.get(download_url, stream=True)
    chunk_size = 20000000
    with open(os.path.join(os.getcwd(),geotiff_name), 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)
            
rate_tif = 'Sequestration_Rate_Map_Griscom_Restoration_Areas.tif'
variance_tif = 'Sequestration_Rate_Map_Griscom_Restoration_Areas_Variance.tif'
belowground_rate_tif = 'Sequestration_Rate_Map_Griscom_Restoration_Areas_BelowGround_Rate.tif'
belowground_variance_tif = 'Sequestration_Rate_Map_Griscom_Restoration_Areas_BelowGround_Variance.tif'
griscom_tif = 'Griscom.tif'

files_to_download = [rate_tif, variance_tif, belowground_rate_tif, belowground_variance_tif]
for file_name in files_to_download:
    download_tif_from_aws(file_name, url.format(file_name))

#Define cylindrical-equal-area projection pixel area in meters and hectares
pixel_size_m = 739.34*739.34 #Pixel area in meters
pixel_size_ha = pixel_size_m*0.0001 #Pixel area in hectares


'''
Calculate Griscom Restoration Area
'''
griscom_stats = zonal_stats(watersheds_shapefile, griscom_tif, stats=['sum'])
griscom_stats = pd.DataFrame(griscom_stats).fillna(0)
for i,row in griscom_stats.iterrows():
    griscom_stats.at[i,'Griscom_Area_Hectares'] = row['sum']*pixel_size_ha
griscom_stats = griscom_stats[['Griscom_Area_Hectares']] 
 
 
'''
Calculate Aboveground Rate Statistics
'''
rate_stats = None
rate_stats = zonal_stats(watersheds_shapefile, rate_tif, stats=['mean','sum','max','min','count'])
rate_stats = pd.DataFrame(rate_stats).fillna(0)
for i,row in rate_stats.iterrows():
    rate_stats.at[i,'Restoration_Area_Sq_Meters'] = row['count']*pixel_size_m
    rate_stats.at[i,'Restoration_Area_Hectares'] = row['count']*pixel_size_ha
    rate_stats.at[i,'AboveGround_Carbon_Accumulation'] = row['sum']*pixel_size_ha

rate_stats = rate_stats.rename(columns={
    "mean": "AboveGround_Sequestration_Rate_Mean", 
    "sum": "AboveGround_Sequestration_Accumulation_Sum", 
    "max": "AboveGround_Sequestration_Rate_Max", 
    "min": "AboveGround_Sequestration_Rate_Min", 
    "count": "Pixel_Count"
})
rate_stats = rate_stats[['Restoration_Area_Sq_Meters','Restoration_Area_Hectares','AboveGround_Sequestration_Rate_Mean',
                        'AboveGround_Sequestration_Accumulation_Sum',
                        'AboveGround_Sequestration_Rate_Max','AboveGround_Sequestration_Rate_Min']]

'''
Calculate Belowground Rate Statistics
'''
belowground_rate_stats = zonal_stats(watersheds_shapefile, belowground_rate_tif, stats=['mean','sum','max','min','count'])
belowground_rate_stats = pd.DataFrame(belowground_rate_stats).fillna(0)
for i,row in belowground_rate_stats.iterrows():
    belowground_rate_stats.at[i,'BelowGround_Carbon_Accumulation'] = row['sum']*pixel_size_ha

belowground_rate_stats = belowground_rate_stats.rename(columns={
    "mean": "BelowGround_Sequestration_Rate_Mean", 
    "sum": "BelowGround_Sequestration_Accumulation_Sum", 
    "max": "BelowGround_Sequestration_Rate_Max", 
    "min": "BelowGround_Sequestration_Rate_Min"
})
belowground_rate_stats = belowground_rate_stats[['BelowGround_Sequestration_Rate_Mean','BelowGround_Sequestration_Accumulation_Sum',
                        'BelowGround_Sequestration_Rate_Max','BelowGround_Sequestration_Rate_Min']]


'''
Calculate Aboveground Variance Statistics
'''                    
variance_stats = zonal_stats(watersheds_shapefile, variance_tif, stats=['sum','count'])
variance_stats = pd.DataFrame(variance_stats).fillna(0)
for i,row in variance_stats.iterrows():
    variance_of_accumulation = row['sum']*pixel_size_ha**2      #variance of accumulation is sum of pixel level variances multiplied by conversion to hectares squared
    if row['count'] !=0:
        variance_of_rate = row['sum']/(row['count']**2)             #variance of rate is sum of pixel level variances, divided by n^2 (n=number of pixels)
    else:
        variance_of_rate = 0

    std_of_accumulation = np.sqrt(variance_of_accumulation)
    std_of_rate = np.sqrt(variance_of_rate)

    variance_stats.at[i,'AboveGround_Carbon_Rate_Variance'] = variance_of_rate
    variance_stats.at[i,'AboveGround_Carbon_Rate_LowerBound'] = rate_stats.at[i,'AboveGround_Sequestration_Rate_Mean']-1.96*std_of_rate
    variance_stats.at[i,'AboveGround_Carbon_Rate_UpperBound'] = rate_stats.at[i,'AboveGround_Sequestration_Rate_Mean']+1.96*std_of_rate

    variance_stats.at[i,'AboveGround_Carbon_Accumulation_Sum_Variance'] = variance_of_accumulation
    variance_stats.at[i,'AboveGround_Carbon_Accumulation_Sum_LowerBound'] = rate_stats.at[i,'AboveGround_Sequestration_Accumulation_Sum']-1.96*std_of_accumulation
    variance_stats.at[i,'AboveGround_Carbon_Accumulation_Sum_UpperBound'] = rate_stats.at[i,'AboveGround_Sequestration_Accumulation_Sum']+1.96*std_of_accumulation

variance_stats = variance_stats[['AboveGround_Carbon_Rate_Variance','AboveGround_Carbon_Rate_LowerBound','AboveGround_Carbon_Rate_UpperBound',
                        'AboveGround_Carbon_Accumulation_Sum_Variance',
                        'AboveGround_Carbon_Accumulation_Sum_LowerBound','AboveGround_Carbon_Accumulation_Sum_UpperBound']]

'''
Calculate Belowground Variance Statistics
'''                        
below_variance_stats = zonal_stats(watersheds_shapefile, belowground_variance_tif, stats=['sum','count'])
below_variance_stats = pd.DataFrame(below_variance_stats).fillna(0)
for i,row in below_variance_stats.iterrows():
    variance_of_accumulation = row['sum']*pixel_size_ha**2      #variance of accumulation is sum of pixel level variances multiplied by conversion to hectares squared
    if row['count'] !=0:
        variance_of_rate = row['sum']/(row['count']**2)             #variance of rate is sum of pixel level variances, divided by n^2 (n=number of pixels)
    else:
        variance_of_rate = 0
        
    std_of_accumulation = np.sqrt(variance_of_accumulation)
    std_of_rate = np.sqrt(variance_of_rate)

    below_variance_stats.at[i,'BelowGround_Carbon_Rate_Variance'] = variance_of_rate
    below_variance_stats.at[i,'BelowGround_Carbon_Rate_LowerBound'] = belowground_rate_stats.at[i,'BelowGround_Sequestration_Rate_Mean']-1.96*std_of_rate
    below_variance_stats.at[i,'BelowGround_Carbon_Rate_UpperBound'] = belowground_rate_stats.at[i,'BelowGround_Sequestration_Rate_Mean']+1.96*std_of_rate

    below_variance_stats.at[i,'BelowGround_Carbon_Accumulation_Sum_Variance'] = variance_of_accumulation
    below_variance_stats.at[i,'BelowGround_Carbon_Accumulation_Sum_LowerBound'] = belowground_rate_stats.at[i,'BelowGround_Sequestration_Accumulation_Sum']-1.96*std_of_accumulation
    below_variance_stats.at[i,'BelowGround_Carbon_Accumulation_Sum_UpperBound'] = belowground_rate_stats.at[i,'BelowGround_Sequestration_Accumulation_Sum']+1.96*std_of_accumulation

below_variance_stats = below_variance_stats[['BelowGround_Carbon_Rate_Variance','BelowGround_Carbon_Rate_LowerBound','BelowGround_Carbon_Rate_UpperBound',
                        'BelowGround_Carbon_Accumulation_Sum_Variance',
                        'BelowGround_Carbon_Accumulation_Sum_LowerBound','BelowGround_Carbon_Accumulation_Sum_UpperBound']]

#Merge dataframes
gdf = gpd.read_file(watersheds_shapefile,encoding='utf-8')
gdf = gdf[[x for x in list(gdf) if x!='geometry']]
stats = pd.concat([gdf,griscom_stats, rate_stats,variance_stats, belowground_rate_stats, below_variance_stats],axis=1)

stat_columns = ['Griscom_Area_Hectares','Restoration_Area_Sq_Meters', 'Restoration_Area_Hectares', 
                'AboveGround_Sequestration_Rate_Mean', 'AboveGround_Carbon_Rate_LowerBound', 'AboveGround_Carbon_Rate_UpperBound', 'AboveGround_Carbon_Rate_Variance',
                'AboveGround_Sequestration_Rate_Max', 'AboveGround_Sequestration_Rate_Min', 'AboveGround_Sequestration_Accumulation_Sum', 
                'AboveGround_Carbon_Accumulation_Sum_LowerBound', 'AboveGround_Carbon_Accumulation_Sum_UpperBound', 'AboveGround_Carbon_Accumulation_Sum_Variance', 
                'BelowGround_Sequestration_Rate_Mean', 'BelowGround_Carbon_Rate_LowerBound','BelowGround_Carbon_Rate_UpperBound', 'BelowGround_Carbon_Rate_Variance', 
                'BelowGround_Sequestration_Rate_Max', 'BelowGround_Sequestration_Rate_Min',  'BelowGround_Sequestration_Accumulation_Sum', 
                'BelowGround_Carbon_Accumulation_Sum_LowerBound', 'BelowGround_Carbon_Accumulation_Sum_UpperBound','BelowGround_Carbon_Accumulation_Sum_Variance']
stats = stats[list(gdf)+stat_columns]

#Save to file
stats.to_csv('RESULTS.csv',index=False)