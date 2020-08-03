# Forest Loss and Restoration Potential in Cities4Forest City Watershed Areas
## This folder contains code used to calculate statistics on forest loss, biomass loss, restoration potential, and potential carbon sequestration in watersheds near cities in the Cities4Forests Program.
The analysis was done in three steps:
1. Watershed Preprocessing
2. Forest Loss and Biomass Loss Calculation
3. Restoration and Carbon Sequestration Potential Calculation


## Watershed Preprocessing
- Our source of watershed areas was taken from [HydroSHEDS](https://www.hydrosheds.org/page/overview) (Hydrological data and maps based on SHuttle Elevation Derivatives at multiple Scales). HydroSHEDS provides hydrographic information in a consistent and comprehensive format for regional and global-scale applications. HydroSHEDS offers a suite of geo-referenced data sets in raster and vector format, including stream networks, watershed boundaries, drainage directions, and ancillary data layers such as flow accumulations, distances, and river topology information. 
- We utilized the HydroBASINS dataset within HydroSHEDS. HydroBASINS was created by the data providers using the HydroSHEDS database at 15 arc-second resolution, watersheds were delineated in a consistent manner at different scales, and a hierarchical sub-basin breakdown was created following the topological concept of the Pfafstetter coding system. The resulting polygon layers are termed HydroBASINS and represent a subset of the HydroSHEDS database.
- We utilized the level-5 layer from HydroBASINS as a proxy for city watershed boundaries. 
- HydroSHEDS data was downloaded from https://www.hydrosheds.org/downloads by following HydroBASINS -> Standard (Without Lakes) -> Region -> Level 5
- There were no HydroSHEDS watersheds for the islands of Hawaii, so the island of Honolulu was taken from [GADM Version 3.6](https://gadm.org/index.html) from the Administrative Level 3 dataset.
- Administrative Level 0 (countries) and 1 (states/provinces) information was also added to the Cities4Forest cities using [GADM Version 3.6](https://gadm.org/index.html)
- The preprocessing was done in X steps:
1. Adding latitude and longitude to the Cities4Forests cities, done using [get_city_coordinates.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/get_city_coordinates.py)
2. Adding Administrative level 0 and 1 information to the Cities4Forests cities, done using [add_adm1_information.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/add_adm1_information.py)
3. Downloading watershed datasets for each region (Africa, South America, North America, etc.) from HydroBASINS from https://www.hydrosheds.org/downloads by following HydroBASINS -> Standard (Without Lakes) -> Region -> Level 5.
4. Merging Level 5 watersheds from regional datasets to one global dataset using [merge_watersheds.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/merge_watersheds.py)
5. Selected watersheds that contained Cities4Forests cities using QGIS's "Select by Location" command."
6. Adding the island of Honolulu to the global watersheds layer using [add_honolulu_to_watersheds.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/add_honolulu_to_watersheds.py)
7. Added Cities4Forests city attributes to each intersecting watershed using [intersect_city_and_watershed_properties.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/intersect_city_and_watershed_properties.py)
