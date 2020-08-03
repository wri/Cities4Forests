import numpy as np
import pandas as pd
import os
import geopy
import geopandas as gpd
from  geopy.geocoders import Nominatim

#This script finds the coordinates for each Cities4Forest city

#Move to working directory
working_dir = '/Users/kristine/WRI/Cities4Forests/Defra_Watersheds'
os.chdir(working_dir)

#Load cities
csv_file = 'Cities4Forests Watersheds.csv'
df = pd.read_csv(csv_file)

#Loop through cities
for i,row in df.iterrows():
    #Find city and country names
    city = row['City Simplified'].replace(',','')
    country = row['Country'].replace(',','')
    
    #Get coordinates using geopy.geocoders
    geolocator = Nominatim(user_agent='cities4forests')
    loc = geolocator.geocode(city+','+ country)
    df.at[i,'Latitude'] = loc.latitude
    df.at[i,'Longitude'] = loc.longitude

#Save to new file    
df.to_csv(csv_file,index=False,encoding='utf-8')
