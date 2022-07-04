#%%
#import plotly.express as px
#df = px.data.gapminder().query("year == 2007")
#fig = px.scatter_geo(df, locations="iso_alpha",
#                     size="gdpPercap", # size of markers, "pop" is one of the columns of gapminder
#                     width = 800,
#                     height = 600)
#fig.update_traces(marker_colorbar_borderwidth=1, selector=dict(type='scattergeo'))
#fig.show()

#%%
import pandas as pd
import numpy as np
from cartopy.io import shapereader
import geopandas as gpd
import cartopy.feature as cfeature
import shapely.wkt
import cartopy.crs as crs
import matplotlib.pyplot as plt
from tqdm import tqdm
from shapely.ops import unary_union
import matplotlib.colors as mpl
from colorblind import *

#%%
test_colormaps()
plt.show()
#%%
def rescale_array(array,vmin,vmax):
    arr = array.copy()
    for i in range(len(arr)) :
        if arr[i] > vmax :
            arr[i] = vmax
        elif arr[i] < vmin :
            arr[i] = vmin
    return(arr)
            
def NormalizeData_array(data):
    import numpy as np
    return (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))
#%%
color_dict_un_subregions = {'Australia and New Zealand':'gold', 'Central Asia':'brown', 'China':'red',
       'Eastern Asia':'sienna', 'Eastern Europe':'blueviolet', 'India':'peru',
       'Latin America and the Caribbean':'darkkhaki', 'Melanesia':'mediumvioletred', 'Middle East':'orange',
       'Northern Africa':'yellowgreen', 'Northern America':'lightpink', 'Northern Europe':'darkblue',
       'South-eastern Asia':'fuchsia', 'Southern Asia':'darksalmon', 'Southern Europe':'cornflowerblue',
       'Sub-Saharan Africa':'olive', 'Western Asia':'slategray', 'Western Europe':'blue'}

#%%
centroid_dict = {'Australia and New Zealand':'Australia', 'Central Asia':'Kazakhstan', 'China':'China',
       'Eastern Asia':'Japan', 'Eastern Europe':'Ukraine', 'India':'India',
       'Latin America and the Caribbean':'Brazil', 'Melanesia':'PapuaNewGuinea', 'Middle East':'Kuwait',
       'Northern Africa':'Libya', 'Northern America':'UnitedStates', 'Northern Europe':'Norway',
       'South-eastern Asia':'Singapore', 'Southern Asia':'Pakistan', 'Southern Europe':'Italy',
       'Sub-Saharan Africa':'Congo', 'Western Asia':'Turkey', 'Western Europe':'Luxembourg'}
#%%

resolution = '10m'
category = 'cultural'
name = 'admin_0_countries'

shpfilename = shapereader.natural_earth(resolution, category, name)
countries = gpd.read_file(shpfilename)

all_cities = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA_LAI_NDVI_CORINE_WB_improvement_bool.xlsx",index_col=0,header=0)
#%%
df = pd.DataFrame(index=np.unique(all_cities.loc[:,'Cntry_name'].values),columns=['ISO','Count cities','Count cities >1000 km²','Count cities >300k ppl','Count cities >1M ppl','latitude','longitude','Good cities','Good cities >1000 km²','Good cities >300k ppl','Good cities >1M ppl'])

#%%
countries_centroids = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/countries_centroids.xlsx",index_col=0,header=0)
#%%
drop_list=[]

for country in df.index.values :
    try : 
        lat = countries_centroids.loc[country,'Center_lat']
        lon = countries_centroids.loc[country,'Center_lon']
    except :
        if country == 'FrenchGuiana' or country == 'Guadeloupe' or country == 'Martinique' or country == 'Mayotte' or country == 'Reunion':
            iso_code = 'FRA'
            drop_list.append(country)
        elif country == 'Kosovo':
            iso_code = 'KOS'
        elif country == 'NorthernCyprus' :
            iso_code = 'CYN'
        elif country == 'Palestina':
            iso_code = 'ISR'
            drop_list.append(country)
        elif country == 'SouthSudan':
            iso_code = 'SDS'
        elif country == 'WesternSahara':
            iso_code='SAH'
        else :
            iso_code = all_cities[all_cities['Cntry_name']==country].iloc[0,5]
        df.loc[country,'ISO']=iso_code
        poly = countries.loc[countries['ADM0_A3'] == iso_code]['geometry']
        lat = (poly.bounds.iloc[0,1]+poly.bounds.iloc[0,3])/2
        lon = (poly.bounds.iloc[0,0]+poly.bounds.iloc[0,2])/2
    
    df.loc[country,'latitude']=lat
    df.loc[country,'longitude']=lon
    df.loc[country,'Count cities']=0
    df.loc[country,'Count cities >1000 km²']=0
    df.loc[country,'Count cities >300k ppl']=0
    df.loc[country,'Count cities >1M ppl']=0
    df.loc[country,'Good cities']=0
    df.loc[country,'Good cities >1000 km²']=0
    df.loc[country,'Good cities >300k ppl']=0
    df.loc[country,'Good cities >1M ppl']=0

for idx in all_cities.index.values :
    ctry = all_cities.loc[idx,'Cntry_name']
    if ctry == 'FrenchGuiana' or ctry == 'Guadeloupe' or ctry == 'Martinique' or ctry == 'Mayotte' or ctry == 'Reunion':
        pass
    elif ctry == 'Palestina':
        df.loc['Israel','Count cities']+=1
        df.loc['Israel','Good cities']+=all_cities.loc[idx,'Improve_bool_artificial_area_per_cap']
    else :
        df.loc[ctry,'Count cities']+=1
        df.loc[ctry,'Good cities']+=all_cities.loc[idx,'Improve_bool_artificial_area_per_cap']

big_cities=all_cities[all_cities['FUA_area']>=1000]

for idx in big_cities.index.values :
    ctry = big_cities.loc[idx,'Cntry_name']
    df.loc[ctry,'Count cities >1000 km²']+=1
    df.loc[ctry,'Good cities >1000 km²']+=all_cities.loc[idx,'Improve_bool_artificial_area_per_cap']

big_cities_pop=all_cities[all_cities['Total_pop_2000']>=3e5]

for idx in big_cities_pop.index.values :
    ctry = big_cities_pop.loc[idx,'Cntry_name']
    df.loc[ctry,'Count cities >300k ppl']+=1
    df.loc[ctry,'Good cities >300k ppl']+=all_cities.loc[idx,'Improve_bool_artificial_area_per_cap']

big_cities_pop_2=all_cities[all_cities['Total_pop_2000']>=1e6]

for idx in big_cities_pop_2.index.values :
    ctry = big_cities_pop_2.loc[idx,'Cntry_name']
    df.loc[ctry,'Count cities >1M ppl']+=1
    df.loc[ctry,'Good cities >1M ppl']+=all_cities.loc[idx,'Improve_bool_artificial_area_per_cap']



df = df.drop(drop_list,axis='index')

df['Count cities >1000 km²'] = df['Count cities >1000 km²'].fillna(0)
df['Count cities'] = df['Count cities'].fillna(0)
df['Count cities >300k ppl'] = df['Count cities >1000 km²'].fillna(0)
df['Count cities >1M ppl'] = df['Count cities'].fillna(0)

df['Good cities >1000 km²'] = df['Good cities >1000 km²'].fillna(0)
df['Good cities'] = df['Good cities'].fillna(0)
df['Good cities >300k ppl'] = df['Good cities >1000 km²'].fillna(0)
df['Good cities >1M ppl'] = df['Good cities'].fillna(0)


#%%
filename = "D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/FUA/GHS_FUA_UCDB2015_GLOBE_R2019A_4326_1K_V1_0.gpkg"
shape = gpd.read_file(filename)
#%%

fig = plt.figure(figsize=(48,32))

ax = fig.add_subplot(1,1,1, projection=crs.PlateCarree())

ax.stock_img()
ax.coastlines()
ax.add_feature(cfeature.BORDERS,linewidth=0.7)
#ax.add_feature(cfeature.COASTLINE,linewidth=0.7)

ax.set_extent([-180, 180, -70, 80],
              crs=crs.PlateCarree()) ## Important



#plt.scatter(x=all_cities.City_centroid_lon, y=all_cities.City_centroid_lat,
#            color="orangered",
#            s=100,
#            alpha=0.8,
#            transform=crs.PlateCarree()) ## Important
count=0
dict_col = {1:'green',0:'red'}
for city in tqdm(big_cities_pop_2.index.values) :
    bool_val = big_cities_pop_2.loc[city,'Improve_bool_artificial_area_per_cap']
    #polygon1=shapely.wkt.loads(shape.loc[city,'geometry'])
    polygon1=shape.loc[city,'geometry']
    polygon1 = gpd.GeoSeries(unary_union(polygon1)).values[0]
    try :
        ax.add_geometries([polygon1],crs=crs.PlateCarree(),facecolor = dict_col[bool_val], edgecolor=dict_col[bool_val])
        count+=1
    except :
        pass
        #polygon1 = gpd.GeoSeries(unary_union(polygon1)).values[0]
        #plt.plot(polygon1.exterior.xy)

plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/maps/map_improve_bool_artif.png")
plt.show()

#%% artificalisation
fig = plt.figure(figsize=(48,32))
ax = fig.add_subplot(1,1,1, projection=crs.PlateCarree())
#ax.stock_img()
ax.coastlines()
ax.add_feature(cfeature.BORDERS,linewidth=0.7)
ax.set_extent([-180, 180, -70, 80],
              crs=crs.PlateCarree()) ## Important
mappable = plt.scatter(x=big_cities_pop_2.City_centroid_lon,y=big_cities_pop_2.City_centroid_lat,
            #c=diverging_colormap(NormalizeData_array(rescale_array(np.array(big_cities_pop_2['Improve_artificial_area_per_cap']),vmin=-50,vmax=50))),
            c=NormalizeData_array(rescale_array(np.array(big_cities_pop_2['Improve_artificial_area_per_cap']),vmin=-50,vmax=50)),
            cmap = plt.get_cmap('colorblind_diverging'),
            #edgecolors='white',linewidths=5,
            s=100,
            alpha=1,
            transform=crs.PlateCarree(),zorder=100)
clbr = plt.colorbar(mappable=mappable,orientation = 'horizontal',pad=0.01,aspect=50)
clbr.set_ticks([clbr.vmin, 0.2*(clbr.vmax-clbr.vmin), 0.9*(clbr.vmax+clbr.vmin)/2, 1.1*(clbr.vmax+clbr.vmin)/2, 0.8*(clbr.vmax-clbr.vmin), clbr.vmax ])
clbr.set_ticklabels(['-50%','-30%','-15%','+15%','+30%','+50%'])
mappable.figure.axes[1].tick_params(axis="x", labelsize=25)
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/maps/map_improve_artif_cities.png")
plt.show()

#%% Accès aux transports
fig = plt.figure(figsize=(48,32))
ax = fig.add_subplot(1,1,1, projection=crs.PlateCarree())
#ax.stock_img()
ax.coastlines()
ax.add_feature(cfeature.BORDERS,linewidth=0.7)
ax.set_extent([-180, 180, -70, 80],
              crs=crs.PlateCarree()) ## Important
mappable = plt.scatter(x=big_cities_pop_2.City_centroid_lon,y=big_cities_pop_2.City_centroid_lat,
            #c=diverging_colormap(NormalizeData_array(rescale_array(np.array(big_cities_pop_2['Improve_artificial_area_per_cap']),vmin=-50,vmax=50))),
            c=NormalizeData_array(rescale_array(np.array(big_cities_pop_2['Improve_transport_access_proxy_5k']),vmin=-20,vmax=20)),
            cmap = plt.get_cmap('colorblind_diverging_r'),
            #edgecolors='white',linewidths=5,
            s=100,
            alpha=1,
            transform=crs.PlateCarree(),zorder=100)
clbr = plt.colorbar(mappable=mappable,orientation = 'horizontal',pad=0.01,aspect=50)
clbr.set_ticks([clbr.vmin, 0.2*(clbr.vmax-clbr.vmin), 0.9*(clbr.vmax+clbr.vmin)/2, 1.1*(clbr.vmax+clbr.vmin)/2, 0.8*(clbr.vmax-clbr.vmin), clbr.vmax ])
clbr.set_ticklabels(['-20%','-12%','-6%','+6%','+12%','+20%'])
mappable.figure.axes[1].tick_params(axis="x", labelsize=25)
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/maps/map_improve_transport_5k_cities.png")
plt.show()


#%% Accès à la verdure
fig = plt.figure(figsize=(48,32))
ax = fig.add_subplot(1,1,1, projection=crs.PlateCarree())
#ax.stock_img()
ax.coastlines()
ax.add_feature(cfeature.BORDERS,linewidth=0.7)
ax.set_extent([-180, 180, -70, 80],
              crs=crs.PlateCarree()) ## Important
mappable = plt.scatter(x=big_cities_pop_2.City_centroid_lon,y=big_cities_pop_2.City_centroid_lat,
            #c=diverging_colormap(NormalizeData_array(rescale_array(np.array(big_cities_pop_2['Improve_artificial_area_per_cap']),vmin=-50,vmax=50))),
            c=NormalizeData_array(rescale_array(np.array(big_cities_pop_2['Improve_NDVI_pop_weighted_avg']),vmin=-30,vmax=30)),
            cmap = plt.get_cmap('colorblind_diverging_r'),
            #edgecolors='white',linewidths=5,
            s=100,
            alpha=1,
            transform=crs.PlateCarree(),zorder=100)
clbr = plt.colorbar(mappable=mappable,orientation = 'horizontal',pad=0.01,aspect=50)
clbr.set_ticks([clbr.vmin, 0.2*(clbr.vmax-clbr.vmin), 0.9*(clbr.vmax+clbr.vmin)/2, 1.1*(clbr.vmax+clbr.vmin)/2, 0.8*(clbr.vmax-clbr.vmin), clbr.vmax ])
clbr.set_ticklabels(['-30%','-18%','-9%','+9%','+18%','+30%'])
mappable.figure.axes[1].tick_params(axis="x", labelsize=25)
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/maps/map_improve_ndvi_pop_cities.png")
plt.show()

#%% Là où tout s'est amélioré
from matplotlib.lines import Line2D

fig = plt.figure(figsize=(48,32))
ax = fig.add_subplot(1,1,1, projection=crs.PlateCarree())
#ax.stock_img()
ax.coastlines()
ax.add_feature(cfeature.BORDERS,linewidth=0.7)
ax.set_extent([-180, 180, -70, 80],
              crs=crs.PlateCarree()) ## Important
mappable = plt.scatter(x=big_cities_pop_2.City_centroid_lon,y=big_cities_pop_2.City_centroid_lat,
            c=np.array(big_cities_pop_2['Improve_all_bool_v10']),
            cmap = plt.get_cmap('colorblind_diverging_r'),
            #edgecolors='white',linewidths=5,
            s=100,
            alpha=1,
            transform=crs.PlateCarree(),zorder=100)

legend_elements = [Line2D([0], [0], marker='o', color='w', label='Improved in all 3 criteria',
                          markerfacecolor='#3D52A1', markersize=20),
                   Line2D([0], [0], marker='o', color='w', label='Did not improve in all 3 criteria',
                          markerfacecolor='#AE1C3E', markersize=20)]

ax.legend(handles=legend_elements, loc='best',fontsize=25)
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/maps/map_improve_3_indices_cities.png")
plt.show()
#%%
import difflib
#%%
country_dict ={}
for country in np.unique(all_cities.loc[:,'Cntry_name'].values):
    try :
        country_dict[country]=difflib.get_close_matches(country,countries['ADMIN'].values)[0]
    except :
        pass
country_dict['Macao']='Macao S.A.R'
country_dict['Reunion']='Madagascar'
country_dict['Swaziland']='eSwatini'
country_dict['CotedIvoire']='Ivory Coast'
country_dict['Tanzania']='United Republic of Tanzania'
country_dict['FrenchGuiana']='Brazil'
country_dict['Guadeloupe']='Cuba'
country_dict['Martinique']='Cuba'
country_dict['Mayotte']='Madagascar'
country_dict['TimorLeste']='East Timor'
country_dict['Serbia']='Republic of Serbia'

#%%
fig = plt.figure(figsize=(48,32))

ax = fig.add_subplot(1,1,1, projection=crs.PlateCarree())

ax.stock_img()
ax.coastlines()
ax.set_extent([-180, 180, -70, 80],
              crs=crs.PlateCarree()) ## Important

#plt.scatter(x=all_cities.City_centroid_lon, y=all_cities.City_centroid_lat,
#            color="orangered",
#            s=100,
#            alpha=0.8,
#            transform=crs.PlateCarree()) ## Important

count_list=[]
for sub_reg in np.unique(all_cities.loc[:,'UN_subregion'].values) :
    sub_df = all_cities[all_cities['UN_subregion']==sub_reg]
    count=0
    for country in np.unique(sub_df.loc[:,'Cntry_name'].values):
        #try :
        poly = countries.loc[countries['ADMIN'] == country_dict[country]]['geometry'].values[0]
        #poly = gpd.GeoSeries(unary_union(poly)).values[0]
        if type(poly) == shapely.geometry.polygon.Polygon:
            #simple_poly = df.loc[df['ADMIN'] == country]['geometry'].values[0]
            list_polys = [poly, poly]
            poly = shapely.geometry.MultiPolygon(list_polys)
        ax.add_geometries(poly, crs=crs.PlateCarree(), facecolor=color_dict_un_subregions[sub_reg], edgecolor='none')
        #except :
        #    count+=1
        #    count_list.append(country)
    plt.scatter(x=countries_centroids.loc[centroid_dict[sub_reg],'Center_lon'], y=countries_centroids.loc[centroid_dict[sub_reg],'Center_lat'],
            color='black',edgecolors='white',linewidths=5,
            s=500,
            alpha=0.8,
            transform=crs.PlateCarree(),zorder=100) ## Important
    
poly = countries.loc[countries['ADMIN'] == country_dict['Iran']]['geometry'].values[0]
        #poly = gpd.GeoSeries(unary_union(poly)).values[0]
if type(poly) == shapely.geometry.polygon.Polygon:
    #simple_poly = df.loc[df['ADMIN'] == country]['geometry'].values[0]
    list_polys = [poly, poly]
    poly = shapely.geometry.MultiPolygon(list_polys)
ax.add_geometries(poly, crs=crs.PlateCarree(), facecolor=color_dict_un_subregions['Middle East'], edgecolor='none')

poly = countries.loc[countries['ADMIN'] == country_dict['Serbia']]['geometry'].values[0]
        #poly = gpd.GeoSeries(unary_union(poly)).values[0]
if type(poly) == shapely.geometry.polygon.Polygon:
    #simple_poly = df.loc[df['ADMIN'] == country]['geometry'].values[0]
    list_polys = [poly, poly]
    poly = shapely.geometry.MultiPolygon(list_polys)
ax.add_geometries(poly, crs=crs.PlateCarree(), facecolor=color_dict_un_subregions['Southern Europe'], edgecolor='none')

poly = countries.loc[countries['ADMIN'] == 'Somaliland']['geometry'].values[0]
        #poly = gpd.GeoSeries(unary_union(poly)).values[0]
if type(poly) == shapely.geometry.polygon.Polygon:
    #simple_poly = df.loc[df['ADMIN'] == country]['geometry'].values[0]
    list_polys = [poly, poly]
    poly = shapely.geometry.MultiPolygon(list_polys)
ax.add_geometries(poly, crs=crs.PlateCarree(), facecolor=color_dict_un_subregions['Sub-Saharan Africa'], edgecolor='none')

ax.add_feature(cfeature.BORDERS,linewidth=0.7)

plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/maps/subregions.png")
plt.show()