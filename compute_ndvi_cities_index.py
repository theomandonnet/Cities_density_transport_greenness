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
nc_file_pop_2015 = nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/GHS_POP_2015_4326_30ss_reproj.nc", mode='r')
#file is lat x lon
lat=nc_file_pop_2015.variables['lat'][:]
lon=nc_file_pop_2015.variables['lon'][:]

dict_year_file_pop = {'2000' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/GHS_POP_2000_4326_30ss_reproj.nc", mode='r'),
'2015' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/GHS_POP_2015_4326_30ss_reproj.nc", mode='r')}
dict_year_file_ndvi = {'2000' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/NDVI_2000/max_ndvi_2000.nc", mode='r'),
'2015' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/NDVI_2015/max_ndvi_2015.nc", mode='r')}
dict_year_file_lai = {'2000' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/LAI_2000/max_lai_2000.nc", mode='r'),
'2015' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/LAI_2015/max_lai_2015.nc", mode='r')}
dict_year_file_fcover = {'2000' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/FCOVER/2000/max_fcover_2000.nc", mode='r'),
'2015' : nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Copernicus/FCOVER/2015/max_fcover_2015.nc", mode='r')}
#%% Shapefile with urban area from Globan Urban Boundaries, keep only biggest areas
filename = "D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA.xlsx"
shape = pd.read_excel(filename,index_col=0)
filename = "D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/FUA/GHS_FUA_UCDB2015_GLOBE_R2019A_4326_1K_V1_0.gpkg"
fuas_gpkg = gpd.read_file(filename)
#threshold = 100
#shape = shape[shape['UC_area']>=threshold]

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

shape['NDVI_index_threshold_0.0_2000']=None
shape['NDVI_index_threshold_0.0_2015']=None
shape['NDVI_index_threshold_0.1_2000']=None
shape['NDVI_index_threshold_0.1_2015']=None
shape['NDVI_index_threshold_0.2_2000']=None
shape['NDVI_index_threshold_0.2_2015']=None
shape['NDVI_index_threshold_0.3_2000']=None
shape['NDVI_index_threshold_0.3_2015']=None
shape['NDVI_index_threshold_0.4_2000']=None
shape['NDVI_index_threshold_0.4_2015']=None
shape['NDVI_index_threshold_0.5_2000']=None
shape['NDVI_index_threshold_0.5_2015']=None
shape['NDVI_index_threshold_0.6_2000']=None
shape['NDVI_index_threshold_0.6_2015']=None
shape['NDVI_index_threshold_0.7_2000']=None
shape['NDVI_index_threshold_0.7_2015']=None
shape['NDVI_index_threshold_0.8_2000']=None
shape['NDVI_index_threshold_0.8_2015']=None
shape['NDVI_index_threshold_0.9_2000']=None
shape['NDVI_index_threshold_0.9_2015']=None
shape['NDVI_index_avg_2000']=None
shape['NDVI_index_avg_2015']=None
shape['NDVI_index_pop_weighted_avg_2000']=None
shape['NDVI_index_pop_weighted_avg_2015']=None
shape['LAI_index_2000']=None
shape['LAI_index_2015']=None
shape['LAI_avg_index_2000']=None
shape['LAI_avg_index_2015']=None
shape['FCOVER_pop_weighted_avg_2000']=None
shape['FCOVER_pop_weighted_avg_2015']=None
shape['FCOVER_avg_2000']=None
shape['FCOVER_avg_2015']=None

for urb_ID in tqdm(shape.index.values) :
    urban_area = fuas_gpkg.loc[urb_ID,'geometry'] #read geometry from string
    (lon_min,lat_min,lon_max,lat_max)=urban_area.bounds
    y_lon_min = find_closest(lon,lon_min)[0]
    y_lon_max = find_closest(lon,lon_max)[0]
    x_lat_max = find_closest(lat,lat_min)[0]
    x_lat_min = find_closest(lat,lat_max)[0]
    
    nc_data_pop = nc_file_pop_2015.variables['Band1'][x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]

    cell_area_table = [cell_area[x_lat_min-1:x_lat_max+2]]*np.shape(nc_data_pop)[1]
    cell_area_table = np.reshape(cell_area_table,np.shape(nc_data_pop))

    xy = np.meshgrid(lon[y_lon_min-1:y_lon_max+2],lat[x_lat_min-1:x_lat_max+2])
    xy = np.reshape(xy,(2,-1))
    bool_array = sv.contains(urban_area, x=xy[0,:], y=xy[1,:])
    bool_array = np.reshape(bool_array,np.shape(nc_data_pop)) #ensemble des points qui appartiennent à l'aire urbaine = True, sinon False
    ndvi_threshold = 0.5
    for year in ['2000','2015'] :
        nc_data_lai = dict_year_file_lai[year].variables['lai'][0,x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
        nc_data_ndvi = dict_year_file_ndvi[year].variables['ndvi'][0,x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
        nc_data_pop = dict_year_file_pop[year].variables['Band1'][x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
        nc_data_fcover = dict_year_file_fcover[year].variables['fcover'][0,x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
        shape.loc[urb_ID,'NDVI_index_threshold_0.0_'+year]=100*np.sum(nc_data_pop*(nc_data_ndvi>0.0))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'NDVI_index_threshold_0.1_'+year]=100*np.sum(nc_data_pop*(nc_data_ndvi>0.1))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'NDVI_index_threshold_0.2_'+year]=100*np.sum(nc_data_pop*(nc_data_ndvi>0.2))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'NDVI_index_threshold_0.3_'+year]=100*np.sum(nc_data_pop*(nc_data_ndvi>0.3))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'NDVI_index_threshold_0.4_'+year]=100*np.sum(nc_data_pop*(nc_data_ndvi>0.4))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'NDVI_index_threshold_0.5_'+year]=100*np.sum(nc_data_pop*(nc_data_ndvi>0.5))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'NDVI_index_threshold_0.6_'+year]=100*np.sum(nc_data_pop*(nc_data_ndvi>0.6))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'NDVI_index_threshold_0.7_'+year]=100*np.sum(nc_data_pop*(nc_data_ndvi>0.7))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'NDVI_index_threshold_0.8_'+year]=100*np.sum(nc_data_pop*(nc_data_ndvi>0.8))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'NDVI_index_threshold_0.9_'+year]=100*np.sum(nc_data_pop*(nc_data_ndvi>0.9))/np.sum(nc_data_pop)
        shape.loc[urb_ID,'LAI_index_'+year]=np.sum(nc_data_pop*nc_data_lai)/np.sum(nc_data_pop)
        shape.loc[urb_ID,'LAI_avg_index_'+year]=np.sum(cell_area_table*nc_data_lai)/np.sum(cell_area_table)
        shape.loc[urb_ID,'NDVI_index_avg_'+year]=np.sum(cell_area_table*nc_data_ndvi)/np.sum(cell_area_table)
        shape.loc[urb_ID,'NDVI_index_pop_weighted_avg_'+year]=np.sum(nc_data_pop*nc_data_ndvi)/np.sum(nc_data_pop)
        shape.loc[urb_ID,'FCOVER_pop_weighted_avg_'+year]=np.sum(nc_data_pop*nc_data_fcover)/np.sum(nc_data_pop)
        shape.loc[urb_ID,'FCOVER_avg_'+year]=np.sum(cell_area_table*nc_data_fcover)/np.sum(cell_area_table)

#%%
for year in ['2000','2015'] :
    dict_year_file_lai[year].close()
    dict_year_file_pop[year].close()
    dict_year_file_ndvi[year].close()
#%% Save database
shape.to_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA_LAI_NDVI.xlsx")
