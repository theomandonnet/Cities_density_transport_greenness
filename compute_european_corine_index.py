#%% import modules
import shapely.wkt
import shapely.vectorized as sv
import numpy as np
import netCDF4 as nc
import shapely
from shapely.ops import unary_union
#from shapely.geometry import Polygon
#from shapely.geometry import Point
#from cartopy.io import shapereader
#import cartopy.crs as ccrs
import geopandas as gpd
import pandas as pd
#import pandas as pd
#import matplotlib.pyplot as plt
from tqdm import tqdm
import pycountry_convert as pc
import numpy.ma as ma
#from scipy.optimize import curve_fit
#import cartopy.feature as cfeature
#from osgeo import gdal
#from sklearn.metrics import r2_score
#%%open files
nc_file_pop_2015 = nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/GHS_POP_2015_4326_30ss_extract_europe.nc", mode='r')
#file is lat x lon
lat=nc_file_pop_2015.variables['lat'][:]
lon=nc_file_pop_2015.variables['lon'][:]

dict_year_file_pop = {'2000' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/GHS_POP_2000_4326_30ss_extract_europe.nc", mode='r'),
'2015' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/GHS_POP_2015_4326_30ss_extract_europe.nc", mode='r')}
dict_year_file_cor_200 = {'2000' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/CORINE/area_2000_200m.nc", mode='r'),
'2015' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/CORINE/area_2018_200m.nc", mode='r')}
dict_year_file_cor_300 = {'2000' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/CORINE/area_2000_300m.nc", mode='r'),
'2015' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/CORINE/area_2018_300m.nc", mode='r')}
dict_year_file_cor_500 = {'2000' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/CORINE/area_2000_500m.nc", mode='r'),
'2015' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/CORINE/area_2018_500m.nc", mode='r')}
#%% Shapefile with urban area from Globan Urban Boundaries, keep only biggest areas
filename = "D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA_LAI_NDVI.xlsx"
shape = pd.read_excel(filename)
filename = "D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/FUA/GHS_FUA_UCDB2015_GLOBE_R2019A_4326_1K_V1_0.gpkg"
fuas_gpkg = gpd.read_file(filename)
#threshold = 100
#fuas_gpkg = fuas_gpkg[fuas_gpkg['Continent']>='Europe']
#shape = shape[shape['Continent']>='Europe']

#%% Function to find closest element of given value in a list
def find_closest(lst, K):
    lst = np.asarray(lst)
    idx = (np.abs(lst - K)).argmin()
    return idx,lst[idx]
#%% Cell area depending on latitude
cell_area = np.array([6371**2*np.cos(np.pi*lat/180)*0.008928571482636*np.pi/180*0.008928571324300*np.pi/180]).T # the area in km² of each cell, depending on the latitude
#Mettre à jour la résolution
##############
##### || #####
###   ||   ###
##    ||    ##
#     ()     #
##############

#%%

shape['CORINE_rate_pop_200m_2000']=None
shape['CORINE_rate_pop_200m_2015']=None
shape['CORINE_rate_pop_300m_2000']=None
shape['CORINE_rate_pop_300m_2015']=None
shape['CORINE_rate_pop_500m_2000']=None
shape['CORINE_rate_pop_500m_2015']=None

for urb_ID in tqdm(shape[shape['Continent']>='Europe'].index.values) :
    urban_area = fuas_gpkg.loc[urb_ID,'geometry'] #read geometry from string
    (lon_min,lat_min,lon_max,lat_max)=urban_area.bounds
    y_lon_min = find_closest(lon,lon_min)[0]
    y_lon_max = find_closest(lon,lon_max)[0]
    x_lat_max = find_closest(lat,lat_min)[0]
    x_lat_min = find_closest(lat,lat_max)[0]
    
    nc_data_pop = nc_file_pop_2015.variables['pop'][x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]

    cell_area_table = [cell_area[x_lat_min-1:x_lat_max+2]]*np.shape(nc_data_pop)[1]
    cell_area_table = np.reshape(cell_area_table,np.shape(nc_data_pop))

    xy = np.meshgrid(lon[y_lon_min-1:y_lon_max+2],lat[x_lat_min-1:x_lat_max+2])
    xy = np.reshape(xy,(2,-1))
    bool_array = sv.contains(urban_area, x=xy[0,:], y=xy[1,:])
    bool_array = np.reshape(bool_array,np.shape(nc_data_pop)) #ensemble des points qui appartiennent à l'aire urbaine = True, sinon False

    for year in ['2000','2015'] :
        nc_data_pop = dict_year_file_pop[year].variables['pop'][x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
        nc_data_corine_200m = dict_year_file_cor_200[year].variables['Band1'][::-1,:]#latitude is reversed
        nc_data_corine_200m = nc_data_corine_200m[x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
        nc_data_corine_300m = dict_year_file_cor_300[year].variables['Band1'][::-1,:]#latitude is reversed
        nc_data_corine_300m = nc_data_corine_300m[x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
        nc_data_corine_500m = dict_year_file_cor_500[year].variables['Band1'][::-1,:]#latitude is reversed
        nc_data_corine_500m = nc_data_corine_500m[x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
        shape.loc[urb_ID,'CORINE_rate_pop_200m_'+year]=100*np.sum(nc_data_pop*nc_data_corine_200m/(cell_area_table*1e6))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'CORINE_rate_pop_300m_'+year]=100*np.sum(nc_data_pop*nc_data_corine_300m/(cell_area_table*1e6))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'CORINE_rate_pop_500m_'+year]=100*np.sum(nc_data_pop*nc_data_corine_500m/(cell_area_table*1e6))/np.sum(nc_data_pop)

#%%
for year in ['2000','2015'] :
    dict_year_file_cor_200[year].close()
    dict_year_file_cor_300[year].close()
    dict_year_file_cor_500[year].close()
    dict_year_file_pop[year].close()

#%% Save database
shape.to_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA_LAI_NDVI_CORINE.xlsx")
