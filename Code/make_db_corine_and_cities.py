#%% import modules
#import shapely.wkt
import shapely.vectorized as sv
import numpy as np
import netCDF4 as nc
import shapely
from shapely.ops import unary_union
from shapely.geometry import Polygon
from shapely.geometry import Point
#import cartopy.crs as ccrs
import geopandas as gpd
import pandas as pd
#import pandas as pd
#import matplotlib.pyplot as plt
from tqdm import tqdm
import pycountry_convert as pc
from cartopy.io import shapereader
#from scipy.optimize import curve_fit
#import cartopy.feature as cfeature
#from osgeo import gdal
#from sklearn.metrics import r2_score

#filename = "D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/FUA/GHS_FUA_UCDB2015_GLOBE_R2019A_4326_1K_V1_0.gpkg"
#db_FUA = gpd.read_file(filename)

#%% download country administrative boundaries
resolution = '10m'
category = 'cultural'
name = 'admin_0_countries'
shpfilename = shapereader.natural_earth(resolution, category, name)
df = gpd.read_file(shpfilename)


for year in ['1990','2000','2018'] :
    print(year)
    df_corine = gpd.read_file("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/CORINE/corine_"+year+"_4326.gpkg")
    print('file open')
    if year!='2018' :
        df_corine = df_corine[df_corine['code_'+year[-2:]]=='141'] #keep urban green spaces only
    else :
        df_corine = df_corine[df_corine['Code_'+year[-2:]]=='141'] #keep urban green spaces only
    df_corine['Area_Ha'] = df_corine['Area_Ha']/100 #convert ha to km²
    df_corine.rename(columns = {'Area_Ha':'Area_km2'}, inplace = True)
    df_corine.insert(3,'Country',value=None)
    i=0
    for area in df_corine.loc[:,'geometry'] :
        (lon_min,lat_min,lon_max,lat_max)=df_corine.iloc[i,6].bounds
        mid_lon = (lon_min+lon_max)/2
        mid_lat = (lat_min+lat_max)/2
        i_country = 0
        for country in df.loc[:,'geometry']:
            if country.contains(Point(mid_lon,mid_lat)):
                df_corine.iloc[i,3] = df.loc[i_country,'SOVEREIGNT']
            i_country+=1
        i+=1
    df_corine.to_file('D:/Ubuntu/M2_EEET/Stage_CIRED/Data/CORINE/corine_'+year+'_4326_urban_green.shp',driver ='ESRI Shapefile')