#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import scipy.stats
#%%
oecd_data = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/Vervabatz/mrt_access.xlsx")
#my_data_GUB = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_data_threshold_100.xlsx",index_col=0)
my_data_FUA = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA.xlsx",index_col=0)
#%%
list_cities = oecd_data['City'].values
#my_data_GUB = my_data_GUB.query("City in @list_cities")
my_data_FUA = my_data_FUA.query("eFUA_name in @list_cities")
#oecd_data_GUB_ordered = pd.DataFrame(data=None, columns=oecd_data.columns,index=my_data_GUB.index)
oecd_data_FUA_ordered = pd.DataFrame(data=None, columns=oecd_data.columns,index=my_data_FUA.index)

#idx=0
#for city in my_data_GUB.City.values :
#    oecd_data_GUB_ordered.iloc[idx,:]=oecd_data[oecd_data['City']==city]
#    idx+=1
    
idx=0
for city in my_data_FUA.eFUA_name.values :
    oecd_data_FUA_ordered.iloc[idx,:]=oecd_data[oecd_data['City']==city]
    idx+=1
   
#%%
colors = dict(mcol.BASE_COLORS, **mcol.CSS4_COLORS)
colors2 = {'Argentina':'cyan', 'Australia':'gold', 'Brazil':'darkgreen',
'Canada':'lightcoral', 'Belgium':'red', 'Norway':'sienna','France' : 'mediumblue',
'Greece':'olivedrab', 'Portugal':'darkkhaki', 'Hungary':'teal', 'Italy':'blue', 'Sweden':'yellow',
'Netherlands':'orange', 'United States':'slategray', 'Mexico':'lime', 'Lithuania':'firebrick', 'Ireland':'olive',
'Finland':'cadetblue', 'Spain':'crimson', 'Czech Republic':'peru', 'United Kingdom':'midnightblue',
'Poland':'orangered','Switzerland':'turquoise','Austria':'tan','Chile':'purple','Germany':'black'}
color_dict={}
for ctry in colors2:
    color_dict[ctry] = colors[colors2[ctry]]
#%%
def linear_law(x, a, b):
    return a*x+b
for indicator in ['Rate_pop_transport_access_threshold_3k_2015',
 'Rate_pop_transport_access_threshold_5k_2015', 'Rate_pop_transport_access_threshold_10k_2015'] :
    for threshold in ['500','1000','1500'] :
        #plot for FUA
        print('FUA')
        PNT_array = np.array(oecd_data_FUA_ordered.loc[:,threshold+'m'])
        access = np.array(my_data_FUA.loc[:,indicator])
        country_list=oecd_data_FUA_ordered.loc[:,'Country']
        color=[colors2.get(x) for x in country_list]
        pars, cov = curve_fit(f=linear_law, xdata=PNT_array, ydata=access, p0=[0, 0], bounds=(-np.inf, np.inf))
        #print(r2_score(access, linear_law(np.array(PNT_array),*pars)))
        print(scipy.stats.pearsonr(access,PNT_array))
        #plt.plot(np.sort(PNT_array),linear_law(np.sort(PNT_array), *pars),'blue')
        plt.plot([0,100],[0,100],'b')
        plt.scatter(access,PNT_array)#,c=['slategray']*94)#[color])
        plt.ylabel('OECD People Near Transit '+threshold+' m')
        plt.xlabel(indicator)
        plt.xlim([0,100])
        plt.ylim([0,100])
        plt.grid()
        plt.tight_layout()
        plt.show()