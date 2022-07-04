#%%
import pandas as pd
import numpy as np
import difflib
from tqdm import tqdm

gdp = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/WorldBank/gdp_data.xlsx",sheet_name='Data',index_col=0)
gdp_growth = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/WorldBank/gdp_growth_data.xlsx",sheet_name='Data',index_col=0)
gdp_cap = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/WorldBank/gdp_cap_data.xlsx",sheet_name='Data',index_col=0)
gdp_cap_growth = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/WorldBank/gdp_cap_growth_data.xlsx",sheet_name='Data',index_col=0)
income_class = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/WorldBank/OGHIST.xlsx",sheet_name='Country Analytical History',index_col=1)
pop_data = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/WorldBank/pop_data.xlsx",sheet_name='Data',index_col=0)

gdp_growth_sub_data = gdp_growth[['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
gdp_growth_sub_data = gdp_growth_sub_data.mean(axis=1)
gdp_cap_growth_sub_data = gdp_cap_growth[['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
gdp_cap_growth_sub_data = gdp_cap_growth_sub_data.mean(axis=1)

AllCities= pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Wu_et_al/AllCities.xlsx",index_col=0)

df = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA_LAI_NDVI_CORINE.xlsx",index_col=0)

#%%

country_dict_FUA_to_WB={}
for country in np.unique(df.loc[:,'Cntry_name'].values):
    try :
        country_dict_FUA_to_WB[country]=difflib.get_close_matches(country,gdp.index.values)[0]
    except :
        country_dict_FUA_to_WB[country]=None

country_dict_FUA_to_WB['Gambia']='Gambia, The'        
country_dict_FUA_to_WB['DemocraticRepublicoftheCongo']='Congo, Dem. Rep.'
country_dict_FUA_to_WB['Egypt']='Egypt, Arab Rep.'
country_dict_FUA_to_WB['HongKong']='Hong Kong SAR, China'
country_dict_FUA_to_WB['RepublicofCongo']='Congo, Rep.'
country_dict_FUA_to_WB['Guadeloupe']='France'
country_dict_FUA_to_WB['Mayotte']='France'
country_dict_FUA_to_WB['Reunion']='France'
country_dict_FUA_to_WB['Martinique']='France'
country_dict_FUA_to_WB['FrenchGuiana']='France'
country_dict_FUA_to_WB['Swaziland']='Eswatini'
country_dict_FUA_to_WB['Brunei']='Brunei Darussalam'
country_dict_FUA_to_WB['Kyrgyzstan']='Kyrgyz Republic'
country_dict_FUA_to_WB['Macao']='Macao SAR, China'
country_dict_FUA_to_WB['Russia']='Russian Federation'
country_dict_FUA_to_WB['Slovakia']='Slovak Republic'
country_dict_FUA_to_WB['NorthKorea']="Korea, Dem. People's Rep."
country_dict_FUA_to_WB['SouthKorea']='Korea, Rep.'
country_dict_FUA_to_WB['Syria']='Syrian Arab Republic'
country_dict_FUA_to_WB['Taiwan']='China'
country_dict_FUA_to_WB['Iran']='Iran, Islamic Rep.'

#%%

city_dict_FUA_to_AllCities={}
for city in AllCities.index.values :
    try :
        city_dict_FUA_to_AllCities[city]=difflib.get_close_matches(city,np.unique(df.loc[:,'eFUA_name'].values))[0]
    except :
        city_dict_FUA_to_AllCities[city]=None

city_dict_FUA_to_AllCities['Shenzhen']=None
city_dict_FUA_to_AllCities['Riverside']=None
city_dict_FUA_to_AllCities['Minneapolis']='Minneapolis'
city_dict_FUA_to_AllCities['Brasilia']=None
city_dict_FUA_to_AllCities['San Diego']=None
city_dict_FUA_to_AllCities['Guarulhos']=None
city_dict_FUA_to_AllCities['Ottawa_Gatineau']='Ottawa'
city_dict_FUA_to_AllCities['Canberra']=None
city_dict_FUA_to_AllCities.pop('Darwin')
city_dict_FUA_to_AllCities.pop('Shenzhen')
city_dict_FUA_to_AllCities.pop('Riverside')
city_dict_FUA_to_AllCities.pop('Brasilia')
city_dict_FUA_to_AllCities.pop('San Diego')
city_dict_FUA_to_AllCities.pop('Guarulhos')
city_dict_FUA_to_AllCities.pop('Canberra')
city_dict_FUA_to_AllCities.pop('Duque de Caxias')

city_dict_FUA_to_AllCities = {v: k for k, v in city_dict_FUA_to_AllCities.items()}

#%%

df['Country_GDP_2000']=None
df['Country_GDP_relative_var_2000_2015']=None
df['Country_GDP_growth_2000']=None
df['Country_GDP_growth_avg_2000_2015']=None
df['Country_GDP_cap_2000']=None
df['Country_GDP_cap_relative_var_2000_2015']=None
df['Country_GDP_cap_growth_2000']=None
df['Country_GDP_cap_growth_avg_2000_2015']=None
df['Country_income_class_2000']=None
df['Country_pop_2000']=None
df['Country_pop_2015']=None
df['Country_pop_relative_var_2000_2015']=None

df['City_pop_relative_var_2000_2015']=None
df['Artificial_area_per_cap_2000']=None
df['Artificial_area_per_cap_2015']=None

df['Jobs_access_transit_Wu_et_al']=None

df['Improve_artificial_area_per_cap']=None
df['Improve_transport_access_proxy_3k']=None
df['Improve_transport_access_proxy_5k']=None
df['Improve_transport_access_proxy_10k']=None
df['Improve_NDVI_pop_weighted_avg']=None
df['Improve_LAI']=None
df['Improve_NDVI_avg']=None
df['Improve_LAI_avg']=None
df['Improve_FCOVER_pop_weighted_avg']=None
df['Improve_FCOVER_avg']=None
df['Improve_CORINE_200m']=None
df['Improve_CORINE_300m']=None
df['Improve_CORINE_500m']=None

df['Improve_Pop_close_to_MRT_500m']=None
df['Improve_Pop_close_to_MRT_1000m']=None
df['Improve_Pop_close_to_MRT_1500m']=None

df['Improve_bool_artificial_area_per_cap']=None
df['Improve_bool_transport_access_proxy_3k']=None
df['Improve_bool_transport_access_proxy_5k']=None
df['Improve_bool_transport_access_proxy_10k']=None
df['Improve_bool_NDVI_pop_weighted_avg']=None
df['Improve_bool_LAI']=None
df['Improve_bool_NDVI_avg']=None
df['Improve_bool_LAI_avg']=None
df['Improve_bool_FCOVER_pop_weighted_avg']=None
df['Improve_bool_FCOVER_avg']=None
df['Improve_bool_CORINE_200m']=None
df['Improve_bool_CORINE_300m']=None
df['Improve_bool_CORINE_500m']=None

df['Improve_bool_Pop_close_to_MRT_500m']=None
df['Improve_bool_Pop_close_to_MRT_1000m']=None
df['Improve_bool_Pop_close_to_MRT_1500m']=None

df.loc[:,'Artificial_area_per_cap_2000']=df.loc[:,'Artificial_area_2000']/df.loc[:,'Total_pop_2000']
df.loc[:,'Artificial_area_per_cap_2015']=df.loc[:,'Artificial_area_2015']/df.loc[:,'Total_pop_2015']
df.loc[:,'City_pop_relative_var_2000_2015']=100*(df.loc[:,'Total_pop_2015']-df.loc[:,'Total_pop_2000'])/df.loc[:,'Total_pop_2000']
#%%
for idx in tqdm(df.index.values) :
    #print(df.loc[idx,'eFUA_name'])
    if df.loc[idx,'Cntry_name'] not in ['Jersey','Laos','Palestina','WesternSahara'] :
        df.loc[idx,'Country_GDP_2000']=gdp.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2000']
        df.loc[idx,'Country_GDP_relative_var_2000_2015']=100*(gdp.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2015']-gdp.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2000'])/gdp.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2000']
        df.loc[idx,'Country_GDP_growth_2000']=gdp_growth.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2000']
        df.loc[idx,'Country_GDP_growth_avg_2000_2015']=gdp_growth_sub_data.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']]]
        
        df.loc[idx,'Country_GDP_cap_2000']=gdp_cap.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2000']
        df.loc[idx,'Country_GDP_cap_relative_var_2000_2015']=100*(gdp_cap.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2015']-gdp_cap.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2000'])/gdp_cap.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2000']
        df.loc[idx,'Country_GDP_cap_growth_2000']=gdp_cap_growth.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2000']
        df.loc[idx,'Country_GDP_cap_growth_avg_2000_2015']=gdp_cap_growth_sub_data.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']]]
        
        df.loc[idx,'Country_income_class_2000'] = income_class.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],2000]
        
        df.loc[idx,'Country_pop_2000']=pop_data.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2000']
        df.loc[idx,'Country_pop_2015']=pop_data.loc[country_dict_FUA_to_WB[df.loc[idx,'Cntry_name']],'2015']
        
        df.loc[idx,'Improve_bool_artificial_area_per_cap']=(df.loc[idx,'Artificial_area_per_cap_2015']<df.loc[idx,'Artificial_area_per_cap_2000'])
        df.loc[idx,'Improve_bool_transport_access_proxy_3k']= (df.loc[idx,'Rate_pop_transport_access_threshold_3k_2015']>df.loc[idx,'Rate_pop_transport_access_threshold_3k_2000'])
        df.loc[idx,'Improve_bool_transport_access_proxy_5k']= (df.loc[idx,'Rate_pop_transport_access_threshold_5k_2015']>df.loc[idx,'Rate_pop_transport_access_threshold_5k_2000'])
        df.loc[idx,'Improve_bool_transport_access_proxy_10k']=(df.loc[idx,'Rate_pop_transport_access_threshold_10k_2015']>df.loc[idx,'Rate_pop_transport_access_threshold_10k_2000'])
        
        df.loc[idx,'Improve_artificial_area_per_cap']=100*(df.loc[idx,'Artificial_area_per_cap_2015']-df.loc[idx,'Artificial_area_per_cap_2000'])/df.loc[idx,'Artificial_area_per_cap_2000']
        df.loc[idx,'Improve_transport_access_proxy_3k']= (df.loc[idx,'Rate_pop_transport_access_threshold_3k_2015']-df.loc[idx,'Rate_pop_transport_access_threshold_3k_2000'])
        df.loc[idx,'Improve_transport_access_proxy_5k']= (df.loc[idx,'Rate_pop_transport_access_threshold_5k_2015']-df.loc[idx,'Rate_pop_transport_access_threshold_5k_2000'])
        df.loc[idx,'Improve_transport_access_proxy_10k']=(df.loc[idx,'Rate_pop_transport_access_threshold_10k_2015']-df.loc[idx,'Rate_pop_transport_access_threshold_10k_2000'])
        
        if not np.isnan(df.loc[idx,'Pop_close_to_MRT_500m_2015']) :
            df.loc[idx,'Improve_bool_Pop_close_to_MRT_500m']=(df.loc[idx,'Pop_close_to_MRT_500m_2015']>df.loc[idx,'Pop_close_to_MRT_500m_2000']) 
            df.loc[idx,'Improve_Pop_close_to_MRT_500m']=(df.loc[idx,'Pop_close_to_MRT_500m_2015']-df.loc[idx,'Pop_close_to_MRT_500m_2000'])
        else :
            df.loc[idx,'Improve_bool_Pop_close_to_MRT_500m']=np.nan
            df.loc[idx,'Improve_Pop_close_to_MRT_500m']=np.nan
            
        if not np.isnan(df.loc[idx,'Pop_close_to_MRT_1000m_2015']) :
            df.loc[idx,'Improve_bool_Pop_close_to_MRT_1000m']=(df.loc[idx,'Pop_close_to_MRT_1000m_2015']>df.loc[idx,'Pop_close_to_MRT_1000m_2000'])
            df.loc[idx,'Improve_Pop_close_to_MRT_1000m']=(df.loc[idx,'Pop_close_to_MRT_1000m_2015']-df.loc[idx,'Pop_close_to_MRT_1000m_2000'])
        else : 
            df.loc[idx,'Improve_bool_Pop_close_to_MRT_1000m']=np.nan
            df.loc[idx,'Improve_Pop_close_to_MRT_1000m']=np.nan
        if not np.isnan(df.loc[idx,'Pop_close_to_MRT_1500m_2015']) :
            df.loc[idx,'Improve_bool_Pop_close_to_MRT_1500m']=(df.loc[idx,'Pop_close_to_MRT_1500m_2015']>df.loc[idx,'Pop_close_to_MRT_1500m_2000'])
            df.loc[idx,'Improve_Pop_close_to_MRT_1500m']=(df.loc[idx,'Pop_close_to_MRT_1500m_2015']-df.loc[idx,'Pop_close_to_MRT_1500m_2000'])
        else : 
            df.loc[idx,'Improve_bool_Pop_close_to_MRT_1500m']=np.nan
            df.loc[idx,'Improve_Pop_close_to_MRT_1500m']=np.nan
        try :
            df.loc[idx,'Improve_bool_NDVI_pop_weighted_avg']=(df.loc[idx,'NDVI_index_pop_weighted_avg_2015']>df.loc[idx,'NDVI_index_pop_weighted_avg_2000'])
            df.loc[idx,'Improve_NDVI_pop_weighted_avg']=100*(df.loc[idx,'NDVI_index_pop_weighted_avg_2015']-df.loc[idx,'NDVI_index_pop_weighted_avg_2000'])/df.loc[idx,'NDVI_index_pop_weighted_avg_2000']
        except : pass
        try :
            df.loc[idx,'Improve_bool_LAI']=(df.loc[idx,'LAI_index_2015']>df.loc[idx,'LAI_index_2000'])
            df.loc[idx,'Improve_LAI']=100*(df.loc[idx,'LAI_index_2015']-df.loc[idx,'LAI_index_2000'])/df.loc[idx,'LAI_index_2000']
        except : pass
        try :
            df.loc[idx,'Improve_bool_NDVI_avg']=(df.loc[idx,'NDVI_index_avg_2015']>df.loc[idx,'NDVI_index_avg_2000'])
            df.loc[idx,'Improve_NDVI_avg']=100*(df.loc[idx,'NDVI_index_avg_2015']-df.loc[idx,'NDVI_index_avg_2000'])/df.loc[idx,'NDVI_index_avg_2000']
        except : pass
        try :
            df.loc[idx,'Improve_bool_LAI_avg']=(df.loc[idx,'LAI_avg_index_2015']>df.loc[idx,'LAI_avg_index_2000'])
            df.loc[idx,'Improve_LAI_avg']=100*(df.loc[idx,'LAI_avg_index_2015']-df.loc[idx,'LAI_avg_index_2000'])/df.loc[idx,'LAI_avg_index_2000']
        except : pass
        try :
            df.loc[idx,'Improve_bool_FCOVER_pop_weighted_avg']=(df.loc[idx,'FCOVER_pop_weighted_avg_2015']>df.loc[idx,'FCOVER_pop_weighted_avg_2000'])
            df.loc[idx,'Improve_FCOVER_pop_weighted_avg']=100*(df.loc[idx,'FCOVER_pop_weighted_avg_2015']-df.loc[idx,'FCOVER_pop_weighted_avg_2000'])/df.loc[idx,'FCOVER_pop_weighted_avg_2000']
        except : pass
        try :
            df.loc[idx,'Improve_bool_FCOVER_avg']=(df.loc[idx,'FCOVER_avg_2015']>df.loc[idx,'FCOVER_avg_2000'])
            df.loc[idx,'Improve_FCOVER_avg']=100*(df.loc[idx,'FCOVER_avg_2015']-df.loc[idx,'FCOVER_avg_2000'])/df.loc[idx,'FCOVER_avg_2000']
        except : pass
        try :
            if not np.isnan(df.loc[idx,'CORINE_rate_pop_500m_2015']):
                df.loc[idx,'Improve_bool_CORINE_200m']=(df.loc[idx,'CORINE_rate_pop_200m_2015']>df.loc[idx,'CORINE_rate_pop_200m_2000'])
                df.loc[idx,'Improve_bool_CORINE_300m']=(df.loc[idx,'CORINE_rate_pop_300m_2015']>df.loc[idx,'CORINE_rate_pop_300m_2000'])
                df.loc[idx,'Improve_bool_CORINE_500m']=(df.loc[idx,'CORINE_rate_pop_500m_2015']>df.loc[idx,'CORINE_rate_pop_500m_2000'])
                df.loc[idx,'Improve_CORINE_200m']=(df.loc[idx,'CORINE_rate_pop_200m_2015']-df.loc[idx,'CORINE_rate_pop_200m_2000'])
                df.loc[idx,'Improve_CORINE_300m']=(df.loc[idx,'CORINE_rate_pop_300m_2015']-df.loc[idx,'CORINE_rate_pop_300m_2000'])
                df.loc[idx,'Improve_CORINE_500m']=(df.loc[idx,'CORINE_rate_pop_500m_2015']-df.loc[idx,'CORINE_rate_pop_500m_2000'])
            else :
                df.loc[idx,'Improve_bool_CORINE_200m']=np.nan
                df.loc[idx,'Improve_bool_CORINE_300m']=np.nan
                df.loc[idx,'Improve_bool_CORINE_500m']=np.nan
                df.loc[idx,'Improve_CORINE_200m']=np.nan
                df.loc[idx,'Improve_CORINE_300m']=np.nan
                df.loc[idx,'Improve_CORINE_500m']=np.nan
        except :
            if df.loc[idx,'CORINE_rate_pop_500m_2015'] != '--':
                df.loc[idx,'Improve_bool_CORINE_200m']=(df.loc[idx,'CORINE_rate_pop_200m_2015']>df.loc[idx,'CORINE_rate_pop_200m_2000'])
                df.loc[idx,'Improve_bool_CORINE_300m']=(df.loc[idx,'CORINE_rate_pop_300m_2015']>df.loc[idx,'CORINE_rate_pop_300m_2000'])
                df.loc[idx,'Improve_bool_CORINE_500m']=(df.loc[idx,'CORINE_rate_pop_500m_2015']>df.loc[idx,'CORINE_rate_pop_500m_2000'])
                df.loc[idx,'Improve_CORINE_200m']=(df.loc[idx,'CORINE_rate_pop_200m_2015']-df.loc[idx,'CORINE_rate_pop_200m_2000'])
                df.loc[idx,'Improve_CORINE_300m']=(df.loc[idx,'CORINE_rate_pop_300m_2015']-df.loc[idx,'CORINE_rate_pop_300m_2000'])
                df.loc[idx,'Improve_CORINE_500m']=(df.loc[idx,'CORINE_rate_pop_500m_2015']-df.loc[idx,'CORINE_rate_pop_500m_2000'])
            else :
                df.loc[idx,'Improve_bool_CORINE_200m']=np.nan
                df.loc[idx,'Improve_bool_CORINE_300m']=np.nan
                df.loc[idx,'Improve_bool_CORINE_500m']=np.nan
                df.loc[idx,'Improve_CORINE_200m']=np.nan
                df.loc[idx,'Improve_CORINE_300m']=np.nan
                df.loc[idx,'Improve_CORINE_500m']=np.nan
    if df.loc[idx,'eFUA_name'] in city_dict_FUA_to_AllCities:
        #print(df.loc[idx,'eFUA_name'])
        try :
            df.loc[idx,'Jobs_access_transit_Wu_et_al']=AllCities.loc[city_dict_FUA_to_AllCities[df.loc[idx,'eFUA_name']],'Transit']
        except : pass
        
df.loc[:,'Country_pop_relative_var_2000_2015']=100*(df['Country_pop_2015']-df['Country_pop_2000'])/df['Country_pop_2000']

df.to_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA_LAI_NDVI_CORINE_WB.xlsx")