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
