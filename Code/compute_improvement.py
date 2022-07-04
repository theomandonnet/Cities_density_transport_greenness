#%%
import pandas as pd
import numpy as np

from tqdm import tqdm

df = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA_LAI_NDVI_CORINE_WB.xlsx",index_col=0)
#%%
# Var explicatives :
#df['Total_pop_2000']
#df['Urban_area_2000']
#df['City_pop_relative_var_2000_2015']
#df['Cntry_name']
#df['Continent']
#df['Country_GDP_2000']
#df['Country_GDP_relative_var_2000_2015']
#df['Country_GDP_growth_2000']
#df['Country_GDP_growth_avg_2000_2015']
#df['Country_GDP_cap_2000']
#df['Country_GDP_cap_relative_var_2000_2015']
#df['Country_GDP_cap_growth_2000']
#df['Country_GDP_cap_growth_avg_2000_2015']
#df['Country_income_class_2000']

# Var à expliquer :
#df['Improve_artificial_area_per_cap']

#df['Improve_transport_access_proxy_3k']
#df['Improve_transport_access_proxy_5k']
#df['Improve_transport_access_proxy_10k']
#df.loc[idx,'Improve_Pop_close_to_MRT_500m'] #Vervabatz
#df.loc[idx,'Improve_Pop_close_to_MRT_1000m'] #Vervabatz
#df.loc[idx,'Improve_Pop_close_to_MRT_1500m'] #Vervabatz

#df['Improve_NDVI_pop_weighted_avg']
#df['Improve_LAI']
#df['Improve_NDVI_avg']
#df['Improve_LAI_avg']
#df['Improve_CORINE_200m']
#df['Improve_CORINE_300m']
#df['Improve_CORINE_500m']

df['Improve_idx_v1']=None
df['Improve_idx_v2']=None
df['Improve_idx_v3']=None
df['Improve_idx_v4']=None
df['Improve_idx_v5']=None
df['Improve_idx_v6']=None
df['Improve_idx_v7']=None
df['Improve_idx_v8']=None
df['Improve_idx_v9']=None
df['Improve_idx_v10']=None
df['Improve_idx_v11']=None
df['Improve_idx_v12']=None
df['Improve_idx_v13']=None
df['Improve_idx_v14']=None
df['Improve_idx_v15']=None
df['Improve_idx_v16']=None

df['Improve_idx_v17']=None
df['Improve_idx_v18']=None
df['Improve_idx_v19']=None
df['Improve_idx_v20']=None
df['Improve_idx_v21']=None
df['Improve_idx_v22']=None
df['Improve_idx_v23']=None
df['Improve_idx_v24']=None
df['Improve_idx_v25']=None
df['Improve_idx_v26']=None
df['Improve_idx_v27']=None
df['Improve_idx_v28']=None
df['Improve_idx_v29']=None
df['Improve_idx_v30']=None
df['Improve_idx_v31']=None

df['Improve_idx_v32']=None
df['Improve_idx_v33']=None
df['Improve_idx_v34']=None
df['Improve_idx_v35']=None
df['Improve_idx_v36']=None
df['Improve_idx_v37']=None
df['Improve_idx_v38']=None
df['Improve_idx_v39']=None
df['Improve_idx_v40']=None
df['Improve_idx_v41']=None
df['Improve_idx_v42']=None
df['Improve_idx_v43']=None
df['Improve_idx_v44']=None
df['Improve_idx_v45']=None
df['Improve_idx_v46']=None
df['Improve_idx_v47']=None
df['Improve_idx_v48']=None
df['Improve_idx_v49']=None
df['Improve_idx_v50']=None
df['Improve_idx_v51']=None
df['Improve_idx_v52']=None
df['Improve_idx_v53']=None
df['Improve_idx_v54']=None
df['Improve_idx_v55']=None
df['Improve_idx_v56']=None
df['Improve_idx_v57']=None
df['Improve_idx_v58']=None
df['Improve_idx_v59']=None
df['Improve_idx_v60']=None
df['Improve_idx_v61']=None
df['Improve_idx_v62']=None
df['Improve_idx_v63']=None
df['Improve_idx_v64']=None
df['Improve_idx_v65']=None
df['Improve_idx_v66']=None
df['Improve_idx_v67']=None
df['Improve_idx_v68']=None
df['Improve_idx_v69']=None
df['Improve_idx_v70']=None
df['Improve_idx_v71']=None
df['Improve_idx_v72']=None
df['Improve_idx_v73']=None
df['Improve_idx_v74']=None
df['Improve_idx_v75']=None
df['Improve_idx_v76']=None
df['Improve_idx_v77']=None
df['Improve_idx_v78']=None
df['Improve_idx_v79']=None
df['Improve_idx_v80']=None
df['Improve_idx_v81']=None
df['Improve_idx_v82']=None
df['Improve_idx_v83']=None
df['Improve_idx_v84']=None
df['Improve_idx_v85']=None

for idx in tqdm(df.index.values):
    df.loc[idx,'Improve_idx_v1'] = df.loc[idx,'Improve_artificial_area_per_cap']
    df.loc[idx,'Improve_idx_v2'] = df.loc[idx,'Improve_transport_access_proxy_3k']
    df.loc[idx,'Improve_idx_v3'] = df.loc[idx,'Improve_transport_access_proxy_5k']
    df.loc[idx,'Improve_idx_v4'] = df.loc[idx,'Improve_transport_access_proxy_10k']
    df.loc[idx,'Improve_idx_v5'] = df.loc[idx,'Improve_Pop_close_to_MRT_500m']
    df.loc[idx,'Improve_idx_v6'] = df.loc[idx,'Improve_Pop_close_to_MRT_1000m']
    df.loc[idx,'Improve_idx_v7'] = df.loc[idx,'Improve_Pop_close_to_MRT_1500m']
    df.loc[idx,'Improve_idx_v8'] = df.loc[idx,'Improve_NDVI_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v9'] = df.loc[idx,'Improve_LAI']
    df.loc[idx,'Improve_idx_v10']= df.loc[idx,'Improve_NDVI_avg']
    df.loc[idx,'Improve_idx_v11']= df.loc[idx,'Improve_LAI_avg']
    df.loc[idx,'Improve_idx_v12']= df.loc[idx,'Improve_CORINE_200m']
    df.loc[idx,'Improve_idx_v13']= df.loc[idx,'Improve_CORINE_300m']
    df.loc[idx,'Improve_idx_v14']= df.loc[idx,'Improve_CORINE_500m']
    df.loc[idx,'Improve_idx_v15']= df.loc[idx,'Improve_FCOVER_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v16']= df.loc[idx,'Improve_FCOVER_avg']
    
    df.loc[idx,'Improve_idx_v17']=df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_transport_access_proxy_3k']
    df.loc[idx,'Improve_idx_v18']=df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_transport_access_proxy_5k']
    df.loc[idx,'Improve_idx_v19']=df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_transport_access_proxy_10k']
    df.loc[idx,'Improve_idx_v20']=df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_Pop_close_to_MRT_500m']
    df.loc[idx,'Improve_idx_v21']=df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_Pop_close_to_MRT_1000m']
    df.loc[idx,'Improve_idx_v22']=df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_Pop_close_to_MRT_1500m']
    
    df.loc[idx,'Improve_idx_v23']=df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_NDVI_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v24']= df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_LAI']
    df.loc[idx,'Improve_idx_v25']= df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_NDVI_avg']
    df.loc[idx,'Improve_idx_v26']= df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_LAI_avg']
    df.loc[idx,'Improve_idx_v27']= df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_CORINE_200m']
    df.loc[idx,'Improve_idx_v28']= df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_CORINE_300m']
    df.loc[idx,'Improve_idx_v29']= df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_CORINE_500m']
    df.loc[idx,'Improve_idx_v30']= df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_FCOVER_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v31']=df.loc[idx,'Improve_artificial_area_per_cap']/df.loc[idx,'Improve_FCOVER_avg']
    
    df.loc[idx,'Improve_idx_v32']=df.loc[idx,'Improve_transport_access_proxy_3k']/df.loc[idx,'Improve_NDVI_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v33']=df.loc[idx,'Improve_transport_access_proxy_3k']/df.loc[idx,'Improve_LAI']
    df.loc[idx,'Improve_idx_v34']=df.loc[idx,'Improve_transport_access_proxy_3k']/df.loc[idx,'Improve_NDVI_avg']
    df.loc[idx,'Improve_idx_v35']=df.loc[idx,'Improve_transport_access_proxy_3k']/df.loc[idx,'Improve_LAI_avg']
    df.loc[idx,'Improve_idx_v36']=df.loc[idx,'Improve_transport_access_proxy_3k']/df.loc[idx,'Improve_CORINE_200m']
    df.loc[idx,'Improve_idx_v37']=df.loc[idx,'Improve_transport_access_proxy_3k']/df.loc[idx,'Improve_CORINE_300m']
    df.loc[idx,'Improve_idx_v38']=df.loc[idx,'Improve_transport_access_proxy_3k']/df.loc[idx,'Improve_CORINE_500m']
    df.loc[idx,'Improve_idx_v39']=df.loc[idx,'Improve_transport_access_proxy_3k']/df.loc[idx,'Improve_FCOVER_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v40']=df.loc[idx,'Improve_transport_access_proxy_3k']/df.loc[idx,'Improve_FCOVER_avg']
    
    df.loc[idx,'Improve_idx_v41']=df.loc[idx,'Improve_transport_access_proxy_5k']/df.loc[idx,'Improve_NDVI_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v42']=df.loc[idx,'Improve_transport_access_proxy_5k']/df.loc[idx,'Improve_LAI']
    df.loc[idx,'Improve_idx_v43']=df.loc[idx,'Improve_transport_access_proxy_5k']/df.loc[idx,'Improve_NDVI_avg']
    df.loc[idx,'Improve_idx_v44']=df.loc[idx,'Improve_transport_access_proxy_5k']/df.loc[idx,'Improve_LAI_avg']
    df.loc[idx,'Improve_idx_v45']=df.loc[idx,'Improve_transport_access_proxy_5k']/df.loc[idx,'Improve_CORINE_200m']
    df.loc[idx,'Improve_idx_v46']=df.loc[idx,'Improve_transport_access_proxy_5k']/df.loc[idx,'Improve_CORINE_300m']
    df.loc[idx,'Improve_idx_v47']=df.loc[idx,'Improve_transport_access_proxy_5k']/df.loc[idx,'Improve_CORINE_500m']
    df.loc[idx,'Improve_idx_v48']=df.loc[idx,'Improve_transport_access_proxy_5k']/df.loc[idx,'Improve_FCOVER_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v49']=df.loc[idx,'Improve_transport_access_proxy_5k']/df.loc[idx,'Improve_FCOVER_avg']
    
    df.loc[idx,'Improve_idx_v50']=df.loc[idx,'Improve_transport_access_proxy_10k']/df.loc[idx,'Improve_NDVI_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v51']=df.loc[idx,'Improve_transport_access_proxy_10k']/df.loc[idx,'Improve_LAI']
    df.loc[idx,'Improve_idx_v52']=df.loc[idx,'Improve_transport_access_proxy_10k']/df.loc[idx,'Improve_NDVI_avg']
    df.loc[idx,'Improve_idx_v53']=df.loc[idx,'Improve_transport_access_proxy_10k']/df.loc[idx,'Improve_LAI_avg']
    df.loc[idx,'Improve_idx_v54']=df.loc[idx,'Improve_transport_access_proxy_10k']/df.loc[idx,'Improve_CORINE_200m']
    df.loc[idx,'Improve_idx_v55']=df.loc[idx,'Improve_transport_access_proxy_10k']/df.loc[idx,'Improve_CORINE_300m']
    df.loc[idx,'Improve_idx_v56']=df.loc[idx,'Improve_transport_access_proxy_10k']/df.loc[idx,'Improve_CORINE_500m']
    df.loc[idx,'Improve_idx_v57']=df.loc[idx,'Improve_transport_access_proxy_10k']/df.loc[idx,'Improve_FCOVER_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v58']=df.loc[idx,'Improve_transport_access_proxy_10k']/df.loc[idx,'Improve_FCOVER_avg']
    
    df.loc[idx,'Improve_idx_v59']=df.loc[idx,'Improve_Pop_close_to_MRT_500m']/df.loc[idx,'Improve_NDVI_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v60']=df.loc[idx,'Improve_Pop_close_to_MRT_500m']/df.loc[idx,'Improve_LAI']
    df.loc[idx,'Improve_idx_v61']=df.loc[idx,'Improve_Pop_close_to_MRT_500m']/df.loc[idx,'Improve_NDVI_avg']
    df.loc[idx,'Improve_idx_v62']=df.loc[idx,'Improve_Pop_close_to_MRT_500m']/df.loc[idx,'Improve_LAI_avg']
    df.loc[idx,'Improve_idx_v63']=df.loc[idx,'Improve_Pop_close_to_MRT_500m']/df.loc[idx,'Improve_CORINE_200m']
    df.loc[idx,'Improve_idx_v64']=df.loc[idx,'Improve_Pop_close_to_MRT_500m']/df.loc[idx,'Improve_CORINE_300m']
    df.loc[idx,'Improve_idx_v65']=df.loc[idx,'Improve_Pop_close_to_MRT_500m']/df.loc[idx,'Improve_CORINE_500m']
    df.loc[idx,'Improve_idx_v66']=df.loc[idx,'Improve_Pop_close_to_MRT_500m']/df.loc[idx,'Improve_FCOVER_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v67']=df.loc[idx,'Improve_Pop_close_to_MRT_500m']/df.loc[idx,'Improve_FCOVER_avg']
    
    df.loc[idx,'Improve_idx_v68']=df.loc[idx,'Improve_Pop_close_to_MRT_1000m']/df.loc[idx,'Improve_NDVI_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v69']=df.loc[idx,'Improve_Pop_close_to_MRT_1000m']/df.loc[idx,'Improve_LAI']
    df.loc[idx,'Improve_idx_v70']=df.loc[idx,'Improve_Pop_close_to_MRT_1000m']/df.loc[idx,'Improve_NDVI_avg']
    df.loc[idx,'Improve_idx_v71']=df.loc[idx,'Improve_Pop_close_to_MRT_1000m']/df.loc[idx,'Improve_LAI_avg']
    df.loc[idx,'Improve_idx_v72']=df.loc[idx,'Improve_Pop_close_to_MRT_1000m']/df.loc[idx,'Improve_CORINE_200m']
    df.loc[idx,'Improve_idx_v73']=df.loc[idx,'Improve_Pop_close_to_MRT_1000m']/df.loc[idx,'Improve_CORINE_300m']
    df.loc[idx,'Improve_idx_v74']=df.loc[idx,'Improve_Pop_close_to_MRT_1000m']/df.loc[idx,'Improve_CORINE_500m']
    df.loc[idx,'Improve_idx_v75']=df.loc[idx,'Improve_Pop_close_to_MRT_1000m']/df.loc[idx,'Improve_FCOVER_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v76']=df.loc[idx,'Improve_Pop_close_to_MRT_1000m']/df.loc[idx,'Improve_FCOVER_avg']
    
    df.loc[idx,'Improve_idx_v77']=df.loc[idx,'Improve_Pop_close_to_MRT_1500m']/df.loc[idx,'Improve_NDVI_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v78']=df.loc[idx,'Improve_Pop_close_to_MRT_1500m']/df.loc[idx,'Improve_LAI']
    df.loc[idx,'Improve_idx_v79']=df.loc[idx,'Improve_Pop_close_to_MRT_1500m']/df.loc[idx,'Improve_NDVI_avg']
    df.loc[idx,'Improve_idx_v80']=df.loc[idx,'Improve_Pop_close_to_MRT_1500m']/df.loc[idx,'Improve_LAI_avg']
    df.loc[idx,'Improve_idx_v81']=df.loc[idx,'Improve_Pop_close_to_MRT_1500m']/df.loc[idx,'Improve_CORINE_200m']
    df.loc[idx,'Improve_idx_v82']=df.loc[idx,'Improve_Pop_close_to_MRT_1500m']/df.loc[idx,'Improve_CORINE_300m']
    df.loc[idx,'Improve_idx_v83']=df.loc[idx,'Improve_Pop_close_to_MRT_1500m']/df.loc[idx,'Improve_CORINE_500m']
    df.loc[idx,'Improve_idx_v84']=df.loc[idx,'Improve_Pop_close_to_MRT_1500m']/df.loc[idx,'Improve_FCOVER_pop_weighted_avg']
    df.loc[idx,'Improve_idx_v85']=df.loc[idx,'Improve_Pop_close_to_MRT_1500m']/df.loc[idx,'Improve_FCOVER_avg']

#%%
df.to_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA_LAI_NDVI_CORINE_WB_improvement_bool_continuous.xlsx")
#%%

ar1 = [['All Cities','All Cities','All Cities','All Cities', '>1000 km²','>1000 km²','>1000 km²','>1000 km²','>300k ppl cities','>300k ppl cities','>300k ppl cities','>300k ppl cities','>1M ppl cities','>1M ppl cities','>1M ppl cities','>1M ppl cities','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition','Improve_idx definition'],['Nb of good cities','Proportion of good cities','R-squared','Adj. R-squared','Nb of good cities','Proportion of good cities','R-squared','Adj. R-squared','Nb of good cities','Proportion of good cities','R-squared','Adj. R-squared','Nb of good cities','Proportion of good cities','R-squared','Adj. R-squared','Improve_artificial_area_per_cap','Improve_transport_access_proxy_3k','Improve_transport_access_proxy_5k','Improve_transport_access_proxy_10k','Improve_Pop_close_to_MRT_500m','Improve_Pop_close_to_MRT_1000m','Improve_Pop_close_to_MRT_1500m','Improve_NDVI_pop_weighted_avg','Improve_LAI','Improve_NDVI_avg','Improve_LAI_avg','Improve_CORINE_200m','Improve_CORINE_300m','Improve_CORINE_500m','Improve_NDVI_pop_weighted_avg','Improve_NDVI_avg'],]
col_index = pd.MultiIndex.from_tuples(list(zip(*ar1)),names=['1','2'])
df2 = pd.DataFrame(index = df.columns.values[-85:],columns = col_index)
sub_df = df[df['FUA_area']>=1000]
sub_df3 = df[df['Total_pop_2000']>=3e5]
sub_df4 = df[df['Total_pop_2000']>=1e6]
#%%

for i in df2.index.values :
    df2.loc[i,('All Cities','Nb of good cities')]=np.shape(df[df[i]>0])[0]
    df2.loc[i,('All Cities','Proportion of good cities')]=round(100*np.shape(df[df[i]>0])[0]/(np.shape(df[df[i]<=0])[0]+np.shape(df[df[i]>0])[0]),2)
    df2.loc[i,('>1000 km²','Nb of good cities')]=np.shape(sub_df[sub_df[i]>0])[0]
    df2.loc[i,('>1000 km²','Proportion of good cities')]=round(100*np.shape(sub_df[sub_df[i]>0])[0]/(np.shape(sub_df[sub_df[i]<=0])[0]+np.shape(sub_df[sub_df[i]>0])[0]),2)
    df2.loc[i,('>300k ppl cities','Nb of good cities')]=np.shape(sub_df3[sub_df3[i]>0])[0]
    df2.loc[i,('>300k ppl cities','Proportion of good cities')]=round(100*np.shape(sub_df3[sub_df3[i]>0])[0]/(np.shape(sub_df3[sub_df3[i]<=0])[0]+np.shape(sub_df3[sub_df3[i]>0])[0]),2)
    df2.loc[i,('>1M ppl cities','Nb of good cities')]=np.shape(sub_df4[sub_df4[i]>0])[0]
    df2.loc[i,('>1M ppl cities','Proportion of good cities')]=round(100*np.shape(sub_df4[sub_df4[i]>0])[0]/(np.shape(sub_df4[sub_df4[i]<=0])[0]+np.shape(sub_df4[sub_df4[i]>0])[0]),2)

df2.to_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/lm_regression.xlsx")

#%%
exit()
#%%
import matplotlib.pyplot as plt
import scipy.stats
print(scipy.stats.pearsonr(df2.loc[:,('All Cities','Proportion of good cities')],df2.loc[:,('>1000 km²','Proportion of good cities')]))
plt.scatter(df2.loc[:,('All Cities','Proportion of good cities')],df2.loc[:,('>1000 km²','Proportion of good cities')])
plt.plot(np.linspace(0,100,2),np.linspace(0,100,2))
plt.xlim([0,100])
plt.ylim([0,100])
plt.xlabel('Percentage of good cities among all cities')
plt.ylabel('Percentage of good cities among large cities')
plt.grid()
plt.show()