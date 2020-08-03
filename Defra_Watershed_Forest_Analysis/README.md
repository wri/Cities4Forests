# Forest Loss and Restoration Potential in Cities4Forest City Watershed Areas
## This folder contains code used to calculate statistics on forest loss, biomass loss, restoration potential, and potential carbon sequestration in watersheds near cities in the Cities4Forests Program.
Kristine Lister, James Anderson, Michael Chen, John-Rob Pool
The analysis was done in three steps:
1. Watershed Preprocessing
2. Forest Loss, Biomass Loss, and Population Calculation
3. Restoration and Carbon Sequestration Potential Calculation


## Watershed Preprocessing
- Our source of watershed areas was taken from [HydroSHEDS](https://www.hydrosheds.org/page/overview) (Hydrological data and maps based on SHuttle Elevation Derivatives at multiple Scales). HydroSHEDS provides hydrographic information in a consistent and comprehensive format for regional and global-scale applications. HydroSHEDS offers a suite of geo-referenced data sets in raster and vector format, including stream networks, watershed boundaries, drainage directions, and ancillary data layers such as flow accumulations, distances, and river topology information. 
- We utilized the HydroBASINS dataset within HydroSHEDS. HydroBASINS was created by the data providers using the HydroSHEDS database at 15 arc-second resolution, watersheds were delineated in a consistent manner at different scales, and a hierarchical sub-basin breakdown was created following the topological concept of the Pfafstetter coding system. The resulting polygon layers are termed HydroBASINS and represent a subset of the HydroSHEDS database.
- We utilized the level-5 layer from HydroBASINS as a proxy for city watershed boundaries. 
- HydroSHEDS data was downloaded from https://www.hydrosheds.org/downloads by following HydroBASINS -> Standard (Without Lakes) -> Region -> Level 5
- There were no HydroSHEDS watersheds for the islands of Hawaii, so the island of Honolulu was taken from [GADM Version 3.6](https://gadm.org/index.html) from the Administrative Level 3 dataset.
- Administrative Level 0 (countries) and 1 (states/provinces) information was also added to the Cities4Forest cities using [GADM Version 3.6](https://gadm.org/index.html)

The watershed preprocessing was done in 7 steps:
1. Adding latitude and longitude to the Cities4Forests cities, done using [get_city_coordinates.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/get_city_coordinates.py)
2. Adding Administrative level 0 and 1 information to the Cities4Forests cities, done using [add_adm1_information.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/add_adm1_information.py)
3. Downloading watershed datasets for each region (Africa, South America, North America, etc.) from HydroBASINS from https://www.hydrosheds.org/downloads by following HydroBASINS -> Standard (Without Lakes) -> Region -> Level 5.
4. Merging Level 5 watersheds from regional datasets to one global dataset using [merge_watersheds.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/merge_watersheds.py)
5. Selected watersheds that contained Cities4Forests cities using QGIS's "Select by Location" command.
6. Adding the island of Honolulu to the global watersheds layer using [add_honolulu_to_watersheds.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/add_honolulu_to_watersheds.py)
7. Added Cities4Forests city attributes to each intersecting watershed using [intersect_city_and_watershed_properties.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/intersect_city_and_watershed_properties.py)

## Forest Loss, Biomass Loss, and Population Calculation
- For each Cities4Forest city watershed area, we calculated the area of forest loss from 2001 through 2019, the amount of biomass loss from 2001 through 2019, and the population in the watershed area. To do this we used Google Earth Engine, Google Earth Engine Python SDK, and jupyter notebooks.
- The forest loss data comes from Hansen et al 2013, which contains at 30-meter resolution, tree cover density as of 2000 and a binary loss mask for pixels that experienced loss from 2001 through 2019.
- The biomass data comes from an unpublished dataset produced by the Woods Hole Research Center that estimates the above ground biomass density at 30-meter resolution. The data can be viewed on [Global Forest Watch](http://www.globalforestwatch.org/map/global/?analysis=eyJzaG93RHJhdyI6ZmFsc2V9&areaOfInterestModal=eyJvcGVuIjpmYWxzZSwiYWN0aXZlQXJlYUlkIjpudWxsfQ%3D%3D&location=WyJnbG9iYWwiXQ%3D%3D&mainMap=eyJoaWRlUGFuZWxzIjpmYWxzZSwiaGlkZUxlZ2VuZCI6ZmFsc2UsInNob3dCYXNlbWFwcyI6ZmFsc2UsInNob3dSZWNlbnRJbWFnZXJ5IjpmYWxzZSwic2hvd0FuYWx5c2lzIjpmYWxzZX0%3D&map=eyJjZW50ZXIiOnsibGF0IjozNi44MTU3Njc3NzczMzEzMSwibG5nIjoyOC43Njk0MzEwNTAzNTc2Nzh9LCJ6b29tIjoyLjA2MTk1MTk0MjgzNTcwMTYsImJlYXJpbmciOjAsInBpdGNoIjowLCJtaW5ab29tIjoyLCJtYXhab29tIjoxOSwiYmFzZW1hcCI6eyJ2YWx1ZSI6ImRlZmF1bHQifSwibGFiZWxzIjp0cnVlLCJyb2FkcyI6ZmFsc2UsImJib3giOltdLCJjYW5Cb3VuZCI6dHJ1ZSwiZHJhd2luZyI6ZmFsc2UsImRhdGFzZXRzIjpbeyJkYXRhc2V0IjoiNTg3Yjk5NTEtNTRhYS00Y2Q1LTg5MjktOGFhY2Q1NzQzZTE1Iiwib3BhY2l0eSI6MSwidmlzaWJpbGl0eSI6dHJ1ZSwibGF5ZXJzIjpbIjFhMTE5OWUyLTg5NmItNDA1MS05NDE5LWViNGY2N2M1NTRhNyJdfSx7ImRhdGFzZXQiOiIwYjAyMDhiNi1iNDI0LTRiNTctOTg0Zi1jYWRkZmEyNWJhMjIiLCJsYXllcnMiOlsiY2MzNTQzMmQtMzhkNy00YTAzLTg3MmUtM2E3MWEyZjU1NWZjIiwiYjQ1MzUwZTMtNWE3Ni00NGNkLWIwYTktNTAzOGEwZDhiZmFlIl0sIm9wYWNpdHkiOjEsInZpc2liaWxpdHkiOnRydWV9XX0%3D&mapMenu=eyJtZW51U2VjdGlvbiI6ImRhdGFzZXRzIiwiZGF0YXNldENhdGVnb3J5IjoiY2xpbWF0ZSIsImV4cGxvcmVUeXBlIjoidG9waWNzIiwic2VhcmNoVHlwZSI6ImRhdGFzZXQiLCJwdHdUeXBlIjoiYWxsIiwic2VhcmNoIjoiIiwic2VsZWN0ZWRDb3VudHJpZXMiOltdfQ%3D%3D&mapPrompts=eyJvcGVuIjpmYWxzZSwic3RlcEluZGV4IjowLCJzdGVwc0tleSI6IiJ9&modalMeta=aboveground_biomass&recentImagery=eyJzZWxlY3RlZCI6bnVsbCwic2VsZWN0ZWRJbmRleCI6MCwiZGF0ZSI6bnVsbCwid2Vla3MiOjEzLCJjbG91ZHMiOjI1LCJiYW5kcyI6MH0%3D).
- The population data comes from [Gridded Population of the World (GPW), v4](https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-count-rev11), using the population count dataset of GPW. The GPW is produced by the Center for International Earth Science Information Network (CIESIN) at Columbia University.
- The calculation was done using the jupyter notebook [Cities4Forests_Calculate_Loss_Biomass_and_Population.ipynb](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/Cities4Forests_Calculate_Loss_Biomass_and_Population.ipynb)

## Forest Loss, Biomass Loss, and Population Calculation
- For each Cities4Forests city, we calculated the area of restoration potential and potential carbon sequestration in those restoartion areas.
- The area of restoration potential comes from [Griscom et al. 2017](https://www.pnas.org/content/114/44/11645) which defines areas of restoration opportunity at approximately 1-kilometer resolution.
- The estimates of potential carbon sequestration comes from ""Mapping carbon accumulation potential from global natural forest regrowth" soon to be published. It estimates the potential rate of carbon sequestration in Mg C/ha/year for young, naturally regenerating forests for the first 30 years of forest growth. The map is available at approximately 1-kilometer resolution. 
- The analysis for calculating the restoration potential area from Griscom and the potential sequestration potential was done using [sequestration_zonal_stats.py](https://github.com/wri/Cities4Forests/blob/master/Defra_Watershed_Forest_Analysis/sequestration_zonal_stats.py)



Citations:
- Center for International Earth Science Information Network - CIESIN - Columbia University. 2018. Gridded Population of the World, Version 4 (GPWv4): Population Count, Revision 11. Palisades, NY: NASA Socioeconomic Data and Applications Center (SEDAC). https://doi.org/10.7927/H4JW8BX5. Accessed 03/08/2020.
- Griscom, Bronson W. et al. "Natural Climate Solutions". Proceedings Of The National Academy Of Sciences, vol 114, no. 44, 2017, pp. 11645-11650. Proceedings Of The National Academy Of Sciences, doi:10.1073/pnas.1710465114. Accessed 3 Aug 2020.
- Hansen, Potapov, Moore, Hancher et al. “High-resolution global maps of 21st-century forest cover change.” Science 342.6160 (2013): 850-853.
- Woods Hole Research Center. Unpublished data. Accessed through Global Forest Watch Climate on 03/08/2020. climate.globalforestwatch.org
