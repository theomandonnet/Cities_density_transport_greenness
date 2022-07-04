#%% import modules
#import shapely.wkt
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
nc_file_pop_2015 = nc.Dataset("E:/Stage_CIRED/Data/GHS/GHS-POP/ghs_pop_2015_9ss_4326.nc", mode='r')
nc_file_smod_2015 = nc.Dataset("E:/Stage_CIRED/Data/GHS/SMOD/ghs_smod_2015_9ss_4326.nc", mode='r')
nc_file_built_2015 = nc.Dataset("E:/Stage_CIRED/Data/GHS/BUILT/ghs_built_2014_9ss_4326.nc", mode='r')
#file is lat x lon
lat=nc_file_pop_2015.variables['lat'][:]
lon=nc_file_pop_2015.variables['lon'][:]
#%%
dict_year_file_pop = {'1975':nc.Dataset("E:/Stage_CIRED/Data/GHS/GHS-POP/ghs_pop_1975_9ss_4326.nc", mode='r'),
'1990' : nc.Dataset("E:/Stage_CIRED/Data/GHS/GHS-POP/ghs_pop_1990_9ss_4326.nc", mode='r'),
'2000' : nc.Dataset("E:/Stage_CIRED/Data/GHS/GHS-POP/ghs_pop_2000_9ss_4326.nc", mode='r'),
'2015' : nc.Dataset("E:/Stage_CIRED/Data/GHS/GHS-POP/ghs_pop_2015_9ss_4326.nc", mode='r')}
dict_year_file_smod = {'1975':nc.Dataset("E:/Stage_CIRED/Data/GHS/SMOD/ghs_smod_1975_9ss_4326.nc", mode='r'),
'1990' : nc.Dataset("E:/Stage_CIRED/Data/GHS/SMOD/ghs_smod_1990_9ss_4326.nc", mode='r'),
'2000' : nc.Dataset("E:/Stage_CIRED/Data/GHS/SMOD/ghs_smod_2000_9ss_4326.nc", mode='r'),
'2015' : nc.Dataset("E:/Stage_CIRED/Data/GHS/SMOD/ghs_smod_2015_9ss_4326.nc", mode='r')}
dict_year_file_built = {'1975':nc.Dataset("E:/Stage_CIRED/Data/GHS/BUILT/ghs_built_1975_9ss_4326.nc", mode='r'),
'1990' : nc.Dataset("E:/Stage_CIRED/Data/GHS/BUILT/ghs_built_1990_9ss_4326.nc", mode='r'),
'2000' : nc.Dataset("E:/Stage_CIRED/Data/GHS/BUILT/ghs_built_2000_9ss_4326.nc", mode='r'),
'2015' : nc.Dataset("E:/Stage_CIRED/Data/GHS/BUILT/ghs_built_2014_9ss_4326.nc", mode='r')}
#%%
climate_regions_file = nc.Dataset("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Beck_KG_V1/climate_zone_present_4326.nc")
climate_regions_lon = climate_regions_file.variables['lon'][:]
climate_regions_lat = climate_regions_file.variables['lat'][:]
climate_regions_var = climate_regions_file.variables['Band1'][:]
#%%
mrt_access = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Vervabatz/mrt_access.xlsx")
#%% Shapefile with urban area from Globan Urban Boundaries, keep only biggest areas
#filename = "D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/FUA/GHS_FUA_UCDB2015_GLOBE_R2019A_54009_1K_V1_0.gpkg"
filename = "D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/FUA/GHS_FUA_UCDB2015_GLOBE_R2019A_4326_1K_V1_0.gpkg"
shape = gpd.read_file(filename)
threshold = 100
#shape = shape[shape['UC_area']>=threshold]
#%%
un_subregions = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/UN_regions/UNSD_Methodology.xlsx",index_col=1)
#%%
shape.insert(7,'Continent',value=None)
#%%
def country_to_continent(country_name):
    if country_name == 'BurkinaFaso':
        country_name = 'Burkina Faso'
    elif country_name == 'BosniaandHerzegovina':
        country_name = 'Bosnia and Herzegovina'
    elif country_name == 'CapeVerde':
        country_name = 'Cape Verde'
    elif country_name == 'CentralAfricanRepublic':
        country_name = 'Central African Republic'
    elif country_name == 'CostaRica':
        country_name = 'Costa Rica'
    elif country_name == 'Curacao':
        country_name = 'Curaçao'
    elif country_name == 'CzechRepublic':
        country_name = 'Czech Republic'
    elif country_name == 'CotedIvoire':
        country_name = "Côte d'Ivoire"
    elif country_name == 'DemocraticRepublicoftheCongo':
        country_name = "Democratic Republic of the Congo"
    elif country_name == 'DominicanRepublic':
        country_name = "Dominican Republic"
    elif country_name == 'ElSalvador':
        country_name = "El Salvador"
    elif country_name == 'EquatorialGuinea':
        country_name = "Equatorial Guinea"
    elif country_name == 'FrenchGuiana':
        country_name = "French Guiana"
    elif country_name == 'GuineaBissau':
        country_name = "Guinea-Bissau"
    elif country_name == 'HongKong':
        country_name = "Hong Kong"
    elif country_name == 'Kosovo':
        return('Europe')
    elif country_name == 'NewCaledonia':
        country_name = "New Caledonia"
    elif country_name == 'NewZealand':
        country_name = "New Zealand"
    elif country_name == 'NorthKorea':
        country_name = "North Korea"
    elif country_name == 'NorthernCyprus':
        country_name = "Cyprus"
    elif country_name == 'Palestina':
        country_name = "Israel"
    elif country_name == 'PapuaNewGuinea':
        country_name = "Papua New Guinea"
    elif country_name == 'PuertoRico':
        country_name = "Puerto Rico"
    elif country_name == 'RepublicofCongo':
        country_name = "Congo"
    elif country_name == 'Reunion':
        country_name = "Réunion"
    elif country_name == 'SaudiArabia':
        country_name = "Saudi Arabia"
    elif country_name == 'SierraLeone':
        country_name = "Sierra Leone"
    elif country_name == 'SolomonIslands':
        country_name = "Solomon Islands"
    elif country_name == 'SouthAfrica':
        country_name = "South Africa"
    elif country_name == 'SouthKorea':
        country_name = "South Korea"
    elif country_name == 'SouthSudan':
        country_name = "South Sudan"
    elif country_name == 'SriLanka':
        country_name = "Sri Lanka"
    elif country_name == 'SaoTomeandPrincipe':
        country_name = "Sao Tome and Principe"
    elif country_name == 'TimorLeste':
        return('Oceania')
    elif country_name == 'TrinidadandTobago':
        country_name = "Trinidad and Tobago"
    elif country_name == 'UnitedArabEmirates':
        country_name = "United Arab Emirates"
    elif country_name == 'UnitedKingdom':
        country_name = "United Kingdom"
    elif country_name == 'UnitedStates':
        country_name = "United States"
    elif country_name == 'UnitedStates':
        country_name = "United States"
    elif country_name == 'WesternSahara':
        country_name = "Morocco"
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name
for idx in range(np.shape(shape)[0]):
    shape.iloc[idx,7]=country_to_continent(shape.iloc[idx,6])
#%% Function to find closest element of given value in a list
def find_closest(lst, K):
    lst = np.asarray(lst)
    idx = (np.abs(lst - K)).argmin()
    return idx,lst[idx]
#%% Cell area depending on latitude
cell_area = np.array([6371**2*np.cos(np.pi*lat/180)*0.00249043*np.pi/180*0.00249043*np.pi/180]).T # the area in km² of each cell, depending on the latitude
#%% Compute database ~10min
#shape['Climate_region']=None
#shape['UN_subregion']=None
#shape['City_centroid_lat']=None
#shape['City_centroid_lon']=None
# shape['Total_pop_1975']=None
# shape['Total_pop_1990']=None
# shape['Total_pop_2000']=None
# shape['Total_pop_2015']=None

# shape['Urban_pop_1975']=None
# shape['Urban_pop_1990']=None
# shape['Urban_pop_2000']=None
# shape['Urban_pop_2015']=None

# shape['Urban_area_1975']=None
# shape['Urban_area_1990']=None
# shape['Urban_area_2000']=None
# shape['Urban_area_2015']=None

# shape['Avg_pop_density_1975']=None
# shape['Avg_pop_density_1990']=None
# shape['Avg_pop_density_2000']=None
# shape['Avg_pop_density_2015']=None

shape['Rate_pop_low_density_1.5k_1975']=None
shape['Rate_pop_low_density_1.5k_1990']=None
shape['Rate_pop_low_density_1.5k_2000']=None
shape['Rate_pop_low_density_1.5k_2015']=None

shape['Rate_pop_transport_access_threshold_2.5k_1975']=None
shape['Rate_pop_transport_access_threshold_2.5k_1990']=None
shape['Rate_pop_transport_access_threshold_2.5k_2000']=None
shape['Rate_pop_transport_access_threshold_2.5k_2015']=None

shape['Rate_pop_transport_access_threshold_3.5k_1975']=None
shape['Rate_pop_transport_access_threshold_3.5k_1990']=None
shape['Rate_pop_transport_access_threshold_3.5k_2000']=None
shape['Rate_pop_transport_access_threshold_3.5k_2015']=None

# shape['Avg_pop_density_metric_artificial_area_1975']=None
# shape['Avg_pop_density_metric_artificial_area_1990']=None
# shape['Avg_pop_density_metric_artificial_area_2000']=None
# shape['Avg_pop_density_metric_artificial_area_2015']=None

# shape['Rate_urban_inhab_1975']=None
# shape['Rate_urban_inhab_1990']=None
# shape['Rate_urban_inhab_2000']=None
# shape['Rate_urban_inhab_2015']=None

# shape['Density_gradient_1975']=None
# shape['Density_gradient_1990']=None
# shape['Density_gradient_2000']=None
# shape['Density_gradient_2015']=None

# shape['Artificial_area_1975']=None
# shape['Artificial_area_1990']=None
# shape['Artificial_area_2000']=None
# shape['Artificial_area_2015']=None

# shape['Rate_area_transport_access_threshold_3k_1975']=None
# shape['Rate_area_transport_access_threshold_3k_1990']=None
# shape['Rate_area_transport_access_threshold_3k_2000']=None
# shape['Rate_area_transport_access_threshold_3k_2015']=None

# shape['Rate_area_transport_access_threshold_5k_1975']=None
# shape['Rate_area_transport_access_threshold_5k_1990']=None
# shape['Rate_area_transport_access_threshold_5k_2000']=None
# shape['Rate_area_transport_access_threshold_5k_2015']=None

# shape['Rate_area_transport_access_threshold_10k_1975']=None
# shape['Rate_area_transport_access_threshold_10k_1990']=None
# shape['Rate_area_transport_access_threshold_10k_2000']=None
# shape['Rate_area_transport_access_threshold_10k_2015']=None

# shape['Rate_pop_transport_access_threshold_3k_1975']=None
# shape['Rate_pop_transport_access_threshold_3k_1990']=None
# shape['Rate_pop_transport_access_threshold_3k_2000']=None
# shape['Rate_pop_transport_access_threshold_3k_2015']=None

# shape['Rate_pop_transport_access_threshold_5k_1975']=None
# shape['Rate_pop_transport_access_threshold_5k_1990']=None
# shape['Rate_pop_transport_access_threshold_5k_2000']=None
# shape['Rate_pop_transport_access_threshold_5k_2015']=None

# shape['Rate_pop_transport_access_threshold_10k_1975']=None
# shape['Rate_pop_transport_access_threshold_10k_1990']=None
# shape['Rate_pop_transport_access_threshold_10k_2000']=None
# shape['Rate_pop_transport_access_threshold_10k_2015']=None

# shape['Pop_close_to_MRT_500m_1975']=None
# shape['Pop_close_to_MRT_500m_1990']=None
# shape['Pop_close_to_MRT_500m_2000']=None
# shape['Pop_close_to_MRT_500m_2015']=None

# shape['Avg_pop_density_close_to_MRT_500m_1975']=None
# shape['Avg_pop_density_close_to_MRT_500m_1990']=None
# shape['Avg_pop_density_close_to_MRT_500m_2000']=None
# shape['Avg_pop_density_close_to_MRT_500m_2015']=None

# shape['Min_pop_density_close_to_MRT_500m_1975']=None
# shape['Min_pop_density_close_to_MRT_500m_1990']=None
# shape['Min_pop_density_close_to_MRT_500m_2000']=None
# shape['Min_pop_density_close_to_MRT_500m_2015']=None

# shape['Pop_close_to_MRT_1000m_1975']=None
# shape['Pop_close_to_MRT_1000m_1990']=None
# shape['Pop_close_to_MRT_1000m_2000']=None
# shape['Pop_close_to_MRT_1000m_2015']=None

# shape['Avg_pop_density_close_to_MRT_1000m_1975']=None
# shape['Avg_pop_density_close_to_MRT_1000m_1990']=None
# shape['Avg_pop_density_close_to_MRT_1000m_2000']=None
# shape['Avg_pop_density_close_to_MRT_1000m_2015']=None

# shape['Min_pop_density_close_to_MRT_1000m_1975']=None
# shape['Min_pop_density_close_to_MRT_1000m_1990']=None
# shape['Min_pop_density_close_to_MRT_1000m_2000']=None
# shape['Min_pop_density_close_to_MRT_1000m_2015']=None

# shape['Pop_close_to_MRT_1500m_1975']=None
# shape['Pop_close_to_MRT_1500m_1990']=None
# shape['Pop_close_to_MRT_1500m_2000']=None
# shape['Pop_close_to_MRT_1500m_2015']=None

# shape['Avg_pop_density_close_to_MRT_1500m_1975']=None
# shape['Avg_pop_density_close_to_MRT_1500m_1990']=None
# shape['Avg_pop_density_close_to_MRT_1500m_2000']=None
# shape['Avg_pop_density_close_to_MRT_1500m_2015']=None

# shape['Min_pop_density_close_to_MRT_1500m_1975']=None
# shape['Min_pop_density_close_to_MRT_1500m_1990']=None
# shape['Min_pop_density_close_to_MRT_1500m_2000']=None
# shape['Min_pop_density_close_to_MRT_1500m_2015']=None

# shape['PNT_2015_500m']=None
# shape['PNT_2015_1000m']=None
# shape['PNT_2015_1500m']=None

for urb_ID in tqdm(shape.index.values) :
    #try :
    #    shape.loc[urb_ID,'UN_subregion']=un_subregions.loc[shape.loc[urb_ID,'Cntry_name'],'Mahtta_nomenclature']
    #except :
    #    if shape.loc[urb_ID,'Cntry_name'] == 'NorthernCyprus':
    #        shape.loc[urb_ID,'UN_subregion']=un_subregions.loc['Cyprus','Mahtta_nomenclature']
    #    elif shape.loc[urb_ID,'Cntry_name'] == 'Taiwan':
    #        shape.loc[urb_ID,'UN_subregion']=un_subregions.loc['China','Mahtta_nomenclature']
    urban_area = shape.loc[urb_ID,'geometry']
    (lon_min,lat_min,lon_max,lat_max)=shape.loc[urb_ID,'geometry'].bounds
    y_lon_min = find_closest(lon,lon_min)[0]
    y_lon_max = find_closest(lon,lon_max)[0]
    x_lat_min = find_closest(lat,lat_min)[0]
    x_lat_max = find_closest(lat,lat_max)[0]
    
    nc_data_pop = nc_file_pop_2015.variables['Band1'][x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]

    cell_area_table = [cell_area[x_lat_min-1:x_lat_max+2]]*np.shape(nc_data_pop)[1]
    cell_area_table = np.reshape(cell_area_table,np.shape(nc_data_pop))

    xy = np.meshgrid(lon[y_lon_min-1:y_lon_max+2],lat[x_lat_min-1:x_lat_max+2])
    xy = np.reshape(xy,(2,-1))
    bool_array = sv.contains(urban_area, x=xy[0,:], y=xy[1,:])
    bool_array = np.reshape(bool_array,np.shape(nc_data_pop)) #ensemble des points qui appartiennent à l'aire urbaine = True, sinon False

    #centroid_lat = (lat_max+lat_min)/2
    #centroid_lon = (lon_max+lon_min)/2
    #shape.loc[urb_ID,'City_centroid_lat']=centroid_lat
    #shape.loc[urb_ID,'City_centroid_lon']=centroid_lon
    #climate_x_lat = find_closest(climate_regions_lat,centroid_lat)[0]
    #climate_x_lon = find_closest(climate_regions_lon,centroid_lon)[0]
    #shape.loc[urb_ID,'Climate_region']=str(climate_regions_var[climate_x_lat,climate_x_lon])

    for year in ['1975','1990','2000','2015'] :
        nc_data_smod = dict_year_file_smod[year].variables['Band1'][x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
        nc_data_pop = dict_year_file_pop[year].variables['Band1'][x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
        nc_data_built = dict_year_file_built[year].variables['Band1'][x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]/100*bool_array
        shape.loc[urb_ID,'Urban_pop_'+year] = np.sum(nc_data_pop*(nc_data_smod>20))
        shape.loc[urb_ID,'Rate_pop_low_density_1.5k_'+year] = 100*np.sum((nc_data_smod>20)*nc_data_pop*((nc_data_pop/cell_area_table)<1500))/shape.loc[urb_ID,'Urban_pop_'+year]
        shape.loc[urb_ID,'Rate_pop_transport_access_threshold_2.5k_'+year] = 100*np.sum((nc_data_smod>20)*nc_data_pop*((nc_data_pop/cell_area_table)>2500))/shape.loc[urb_ID,'Urban_pop_'+year]
        shape.loc[urb_ID,'Rate_pop_transport_access_threshold_3.5k_'+year] = 100*np.sum((nc_data_smod>20)*nc_data_pop*((nc_data_pop/cell_area_table)>3500))/shape.loc[urb_ID,'Urban_pop_'+year]
    #     shape.loc[urb_ID,'Total_pop_'+year] = np.sum(nc_data_pop)
    #     shape.loc[urb_ID,'Urban_area_'+year] = np.sum((nc_data_smod>20)*cell_area_table)
    #     shape.loc[urb_ID,'Rate_urban_inhab_'+year] = 100*np.sum(nc_data_pop*(nc_data_smod==30))/shape.loc[urb_ID,'Total_pop_'+year]
    #     shape.loc[urb_ID,'Density_gradient_'+year] = 0
    #     shape.loc[urb_ID,'Rate_area_transport_access_threshold_3k_'+year] = 100*np.sum((nc_data_smod>20)*cell_area_table*((nc_data_pop/cell_area_table)>3000))/shape.loc[urb_ID,'Urban_area_'+year]
    #     shape.loc[urb_ID,'Rate_area_transport_access_threshold_5k_'+year] = 100*np.sum((nc_data_smod>20)*cell_area_table*((nc_data_pop/cell_area_table)>5000))/shape.loc[urb_ID,'Urban_area_'+year]
    #     shape.loc[urb_ID,'Rate_area_transport_access_threshold_10k_'+year] = 100*np.sum((nc_data_smod>20)*cell_area_table*((nc_data_pop/cell_area_table)>10000))/shape.loc[urb_ID,'Urban_area_'+year]
    #     shape.loc[urb_ID,'Rate_pop_transport_access_threshold_3k_'+year] = 100*np.sum((nc_data_smod>20)*nc_data_pop*((nc_data_pop/cell_area_table)>3000))/shape.loc[urb_ID,'Urban_pop_'+year]
    #     shape.loc[urb_ID,'Rate_pop_transport_access_threshold_5k_'+year] = 100*np.sum((nc_data_smod>20)*nc_data_pop*((nc_data_pop/cell_area_table)>5000))/shape.loc[urb_ID,'Urban_pop_'+year]
    #     shape.loc[urb_ID,'Rate_pop_transport_access_threshold_10k_'+year] = 100*np.sum((nc_data_smod>20)*nc_data_pop*((nc_data_pop/cell_area_table)>10000))/shape.loc[urb_ID,'Urban_pop_'+year]
    #     shape.loc[urb_ID,'Artificial_area_'+year] = np.sum(nc_data_built*cell_area_table)
    #     shape.loc[urb_ID,'Avg_pop_density_'+year] = shape.loc[urb_ID,'Urban_pop_'+year]/shape.loc[urb_ID,'Urban_area_'+year]
    #     shape.loc[urb_ID,'Avg_pop_density_metric_artificial_area_'+year] = shape.loc[urb_ID,'Total_pop_'+year]/shape.loc[urb_ID,'Artificial_area_'+year]
    # if shape.loc[urb_ID,'eFUA_name'] in mrt_access['City'].values and shape.loc[urb_ID,'eFUA_name']!='Winnipeg' and shape.loc[urb_ID,'Cntry_name']==mrt_access[mrt_access['City']==shape.loc[urb_ID,'eFUA_name']]['Country'].values[0]:
    #     shape.loc[urb_ID,'PNT_2015_500m']= mrt_access[mrt_access['City']==shape.loc[urb_ID,'eFUA_name']]['500m'].values[0]
    #     shape.loc[urb_ID,'PNT_2015_1000m']=mrt_access[mrt_access['City']==shape.loc[urb_ID,'eFUA_name']]['1000m'].values[0]
    #     shape.loc[urb_ID,'PNT_2015_1500m']=mrt_access[mrt_access['City']==shape.loc[urb_ID,'eFUA_name']]['1500m'].values[0]
    #     df_500m  = gpd.read_file("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Vervabatz/pops_close_to_MRT/cities_shapefiles/500_"+shape.loc[urb_ID,'eFUA_name']+".shp")
    #     df_500m  = df_500m.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})
    #     #df_500m  = shapely.geometry.MultiPolygon(df_500m.loc[:,'geometry'].values)
    #     df_500m = gpd.GeoSeries(unary_union(df_500m.loc[:,'geometry'].values)).values[0]
        
    #     df_1000m = gpd.read_file("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Vervabatz/pops_close_to_MRT/cities_shapefiles/1000_"+shape.loc[urb_ID,'eFUA_name']+".shp")
    #     df_1000m = df_1000m.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})
    #     #df_1000m = shapely.geometry.MultiPolygon(df_1000m.loc[:,'geometry'].values)
    #     df_1000m = gpd.GeoSeries(unary_union(df_1000m.loc[:,'geometry'].values)).values[0]
        
    #     df_1500m = gpd.read_file("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Vervabatz/pops_close_to_MRT/cities_shapefiles/1500_"+shape.loc[urb_ID,'eFUA_name']+".shp")
    #     df_1500m = df_1500m.to_crs({'proj':'longlat', 'ellps':'WGS84', 'datum':'WGS84'})
    #     #df_1500m = shapely.geometry.MultiPolygon(df_1500m.loc[:,'geometry'].values)
    #     df_1500m = gpd.GeoSeries(unary_union(df_1500m.loc[:,'geometry'].values)).values[0]
        
    #     bool_array_500m = sv.contains(df_500m, x=xy[0,:], y=xy[1,:])
    #     bool_array_500m = np.reshape(bool_array_500m,np.shape(nc_data_pop))
    #     bool_array_500m = bool_array_500m*bool_array
        
    #     bool_array_1000m = sv.contains(df_1000m, x=xy[0,:], y=xy[1,:])
    #     bool_array_1000m = np.reshape(bool_array_1000m,np.shape(nc_data_pop))
    #     bool_array_1000m = bool_array_1000m*bool_array
        
    #     bool_array_1500m = sv.contains(df_1500m, x=xy[0,:], y=xy[1,:])
    #     bool_array_1500m = np.reshape(bool_array_1500m,np.shape(nc_data_pop))
    #     bool_array_1500m = bool_array_1500m*bool_array
        
    #     for year in ['1975','1990','2000','2015'] :
    #         nc_data_pop = dict_year_file_pop[year].variables['Band1'][x_lat_min-1:x_lat_max+2,y_lon_min-1:y_lon_max+2]*bool_array
    #         shape.loc[urb_ID,'Pop_close_to_MRT_500m_'+year] =100*np.sum(bool_array_500m*nc_data_pop)/np.sum(nc_data_pop)
    #         shape.loc[urb_ID,'Pop_close_to_MRT_1000m_'+year]=100*np.sum(bool_array_1000m*nc_data_pop)/np.sum(nc_data_pop)
    #         shape.loc[urb_ID,'Pop_close_to_MRT_1500m_'+year]=100*np.sum(bool_array_1500m*nc_data_pop)/np.sum(nc_data_pop)
    #         # shape.loc[urb_ID,'Avg_pop_density_close_to_MRT_500m_'+year] =np.mean(ma.array(nc_data_pop/cell_area_table,mask=np.invert(bool_array_500m)))
    #         # shape.loc[urb_ID,'Min_pop_density_close_to_MRT_500m_'+year] = np.min(ma.array(nc_data_pop/cell_area_table,mask=np.invert(bool_array_500m)))
    #         # shape.loc[urb_ID,'Avg_pop_density_close_to_MRT_1000m_'+year]=np.mean(ma.array(nc_data_pop/cell_area_table,mask=np.invert(bool_array_1000m)))
    #         # shape.loc[urb_ID,'Min_pop_density_close_to_MRT_1000m_'+year]= np.min(ma.array(nc_data_pop/cell_area_table,mask=np.invert(bool_array_1000m)))
    #         # shape.loc[urb_ID,'Avg_pop_density_close_to_MRT_1500m_'+year]=np.mean(ma.array(nc_data_pop/cell_area_table,mask=np.invert(bool_array_1500m)))
    #         # shape.loc[urb_ID,'Min_pop_density_close_to_MRT_1500m_'+year]= np.min(ma.array(nc_data_pop/cell_area_table,mask=np.invert(bool_array_1500m)))
        
        #break
#%% Close files
for year in ['1975','1990','2000','2015'] :
    dict_year_file_smod[year].close()
    dict_year_file_pop[year].close()
    dict_year_file_built[year].close()
#%% Save database
#P = shapely.wkt.loads('POLYGON ((51.0 3.0, 51.3 3.61, 51.3 3.0, 51.0 3.0))') #read geometry from string
#shape.to_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA.xlsx")
shape.to_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA_V2.xlsx")