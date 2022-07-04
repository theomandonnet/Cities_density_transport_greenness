#%% import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import scipy.stats
#%% Open database if starting from here
##################################################
#                   TOUTES VILLES                #
##################################################
threshold = 1e6 #1M ppl threshold
shape = pd.read_excel("D:/Ubuntu/M2_EEET/Stage_CIRED/Data/GHS/Urban_areas_from_FUA_LAI_NDVI_CORINE_WB_improvement_bool_continuous.xlsx",index_col=0)
shape = shape[shape['Total_pop_2000']>=1e6]

#%%
shape=shape.drop([6398,7166],axis='index')
#%% Plot cities evolution
from matplotlib.lines import Line2D
import matplotlib.colors as mcol
color_dict = {'Australia and New Zealand':'gold', 'Central Asia':'maroon', 'China':'red',
       'Eastern Asia':'chocolate', 'Eastern Europe':'blueviolet', 'India':'peru',
       'Latin America and the Caribbean':'darkkhaki', 'Melanesia':'orchid', 'Middle East':'orange',
       'Northern Africa':'yellowgreen', 'Northern America':'lightpink', 'Northern Europe':'darkblue',
       'South-eastern Asia':'fuchsia', 'Southern Asia':'darksalmon', 'Southern Europe':'cornflowerblue',
       'Sub-Saharan Africa':'olive', 'Western Asia':'slategray', 'Western Europe':'blue'}

#{'Argentina':'cyan', 'Australia':'gold', 'Brazil':'darkgreen',
#'Canada':'lightcoral', 'China':'red', 'Egypt':'sienna','France' : 'mediumblue',
#'Ghana':'olivedrab', 'India':'darkkhaki', 'Indonesia':'teal', 'Italy':'blue', 'Japan':'yellow',
#'Jordan':'orange', 'Malaysia':'slategray', 'Mexico':'lime', 'Russia':'firebrick', 'South Africa':'olive',
#'South Korea':'cadetblue', 'Spain':'crimson', 'Thailand':'peru', 'United Kingdom':'midnightblue',
#'United States of America':'lightpink'}
#%%
from matplotlib.lines import Line2D
import matplotlib.colors as mcol
col_dct = mcol.CSS4_COLORS.copy()
#print(len(col_dct))
for item in ['lavender','honeydew','whitesmoke','white','snow','seashell','linen'
,'floralwhite','ivory','mintcream','azure','aliceblue','lightcyan','beige','lightgoldenrodyellow',
'ghostwhite','lavenderblush','oldlace','lightyellow','lightgray','lightslategrey','lightslategray']:
    col_dct.pop(item)
col_dct=[k for k,v in col_dct.items()]
#print(len(col_dct))  
color_dict={}
i_ctry = 0
for country in np.unique(shape.loc[:,'Country']):
    color_dict[country]=col_dct[i_ctry]
    i_ctry+=1
#%% Plot more than 1M ppl cities
#Artificialisation per capita vs transport access proxy :

fig, axs = plt.subplots(nrows=6, ncols=3,figsize=(20,16))
i=-1
for sub_reg in np.unique(shape.loc[:,'UN_subregion'].values):
    i+=1
    df=shape[shape['UN_subregion']==sub_reg]
    var1 = df.loc[:,'Improve_artificial_area_per_cap']
    var2 = df.loc[:,'Improve_transport_access_proxy_5k']
    legend_elements = []
    for region in color_dict :
        legend_elements.append(Line2D([0], [0], color=color_dict[region], lw=4,label=region))

    #ax = axs[i//3,i%3]
    axs[i//3,i%3].axhline(y=0, lw=0.8, color='k')
    axs[i//3,i%3].axvline(x=0, lw=0.8, color='k')
    axs[i//3,i%3].scatter(var1,var2,c=color_dict[sub_reg])
    axs[i//3,i%3].set_title(sub_reg,size=14)
    axs[i//3,i%3].set_xlim([-75,150])
    axs[i//3,i%3].set_ylim([-30,70])
    #plt.legend(handles=legend_elements,loc='best')
    axs[i//3,i%3].grid()
fig.delaxes(axs.flatten()[17])
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axes
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.grid(False)
plt.xlabel('Artificial area per cap relative variation 2000-2015',size=20)
plt.ylabel('Transport access proxy (5k) variation 2000-2015',size=20)
plt.tight_layout()
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/scatter_artif_vs_acess_5k_subregions.png")
#plt.show()
    
#%%
reg_list=shape.loc[:,'UN_subregion']
color_list=[]
for reg in reg_list :
    color_list.append(color_dict[reg])

var1 = shape.loc[:,'Improve_artificial_area_per_cap']
var2 = shape.loc[:,'Improve_transport_access_proxy_5k']

legend_elements = []
for region in color_dict :
    legend_elements.append(Line2D([0], [0], color=color_dict[region], lw=4,label=region))

plt.scatter(var1,var2,c=color_list)
plt.xlabel("Artificial area per cap relative variation 2000-2015")
plt.ylabel("Transport access proxy (5k) variation 2000-2015")
#plt.xlim([-50,50])
#plt.ylim([-50,50])
#plt.legend(handles=legend_elements,loc='best')
plt.grid()
plt.tight_layout()
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/scatter_artif_vs_acess_5k.png")
print(scipy.stats.pearsonr(var1,var2))
plt.show()

#%% Artificialisation per capita vs average greenness :

fig, axs = plt.subplots(nrows=2, ncols=2,figsize=(12,8))
i=-1
for income_class in np.unique(shape.loc[:,'Country_income_class_2000'].values)[1:]:
    i+=1
    df=shape[shape['Country_income_class_2000']==income_class]

    var1 = df.loc[:,'Improve_artificial_area_per_cap']
    var2 = df.loc[:,'Improve_NDVI_pop_weighted_avg']

    legend_elements = []
    for region in color_dict :
        legend_elements.append(Line2D([0], [0], color=color_dict[region], lw=4,label=region))

    #ax = axs[i//3,i%3]
    axs[i//2,i%2].axhline(y=0, lw=0.8, color='k')
    axs[i//2,i%2].axvline(x=0, lw=0.8, color='k')
    axs[i//2,i%2].scatter(var1,var2)#,c=color_dict[sub_reg])
    axs[i//2,i%2].set_title(income_class,size=14)
    axs[i//2,i%2].set_xlim([-75,180])
    axs[i//2,i%2].set_ylim([-35,40])
    #plt.legend(handles=legend_elements,loc='best')
    axs[i//2,i%2].grid()
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axes
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.grid(False)
plt.xlabel("Artificial area per cap relative variation 2000-2015",size=17)
plt.ylabel("Mean pop-weighted greenness relative variation 2000-2015",size=17)
plt.tight_layout()
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/scatter_artif_vs_ndvi_pop_income_class.png")
#plt.show()



#%%
fig, axs = plt.subplots(nrows=6, ncols=3,figsize=(20,16))
i=-1
for sub_reg in np.unique(shape.loc[:,'UN_subregion'].values):
    i+=1
    df=shape[shape['UN_subregion']==sub_reg]

    var1 = df.loc[:,'Improve_artificial_area_per_cap']
    var2 = df.loc[:,'Improve_NDVI_pop_weighted_avg']

    legend_elements = []
    for region in color_dict :
        legend_elements.append(Line2D([0], [0], color=color_dict[region], lw=4,label=region))

    axs[i//3,i%3].axhline(y=0, lw=0.8, color='k')
    axs[i//3,i%3].axvline(x=0, lw=0.8, color='k')
    axs[i//3,i%3].scatter(var1,var2,c=color_dict[sub_reg])
    axs[i//3,i%3].set_title(sub_reg,size=14)
    axs[i//3,i%3].set_xlim([-75,180])
    axs[i//3,i%3].set_ylim([-35,40])
    #plt.legend(handles=legend_elements,loc='best')
    axs[i//3,i%3].grid()
fig.delaxes(axs.flatten()[17])
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axes
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.grid(False)
plt.xlabel("Artificial area per cap relative variation 2000-2015",size=20)
plt.ylabel("Mean pop-weighted greenness relative variation 2000-2015",size=20)
plt.tight_layout()
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/scatter_artif_vs_ndvi_pop_subregions.png")
#plt.show()


#%%
reg_list=shape.loc[:,'UN_subregion']
color_list=[]
for reg in reg_list :
    color_list.append(color_dict[reg])

var1 = shape.loc[:,'Improve_artificial_area_per_cap']
var2 = shape.loc[:,'Improve_NDVI_pop_weighted_avg']

legend_elements = []
for region in color_dict :
    legend_elements.append(Line2D([0], [0], color=color_dict[region], lw=4,label=region))

plt.scatter(var1,var2,c=color_list)
plt.xlabel("Artificial area per cap relative variation 2000-2015")
plt.ylabel("Mean pop-weighted greenness relative variation 2000-2015")
#plt.xlim([-50,50])
#plt.ylim([-50,50])
#plt.legend(handles=legend_elements,loc='best')
plt.grid()
plt.tight_layout()
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/scatter_artif_vs_ndvi_pop.png")
print(scipy.stats.pearsonr(var1,var2))
plt.show()

#%
#%%Transport acess vs average greenness
#%
reg_list=shape.loc[:,'UN_subregion']
color_list=[]
for reg in reg_list :
    color_list.append(color_dict[reg])

var1 = shape.loc[:,'Improve_transport_access_proxy_5k']
var2 = shape.loc[:,'Improve_NDVI_pop_weighted_avg']

legend_elements = []
for region in color_dict :
    legend_elements.append(Line2D([0], [0], color=color_dict[region], lw=4,label=region))

plt.scatter(var1,var2,c=color_list)
plt.xlabel("Transport access proxy (5k) variation 2000-2015")
plt.ylabel("Mean pop-weighted greenness relative variation 2000-2015")
#plt.xlim([-50,50])
#plt.ylim([-50,50])
#plt.legend(handles=legend_elements,loc='best')
plt.grid()
plt.tight_layout()
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/scatter_transport_5k_vs_ndvi_pop.png")
print(scipy.stats.pearsonr(var1,var2))
plt.show()

plt.legend(handles=legend_elements,loc='best')
plt.show()
#%% Transport acess vs average greenness region by region
fig, axs = plt.subplots(nrows=6, ncols=3,figsize=(20,16))
i=-1
for sub_reg in np.unique(shape.loc[:,'UN_subregion'].values):
    i+=1
    df=shape[shape['UN_subregion']==sub_reg]

    var1 = df.loc[:,'Improve_transport_access_proxy_5k']
    var2 = df.loc[:,'Improve_NDVI_pop_weighted_avg']

    legend_elements = []
    for region in color_dict :
        legend_elements.append(Line2D([0], [0], color=color_dict[region], lw=4,label=region))

    axs[i//3,i%3].axhline(y=0, lw=0.8, color='k')
    axs[i//3,i%3].axvline(x=0, lw=0.8, color='k')
    axs[i//3,i%3].scatter(var1,var2,c=color_dict[sub_reg])
    axs[i//3,i%3].set_title(sub_reg,size=14)
    axs[i//3,i%3].set_xlim([-30,70])
    axs[i//3,i%3].set_ylim([-35,45])
    #plt.legend(handles=legend_elements,loc='best')
    axs[i//3,i%3].grid()
fig.delaxes(axs.flatten()[17])
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axes
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.grid(False)
plt.xlabel("Transport access proxy (5k) variation 2000-2015",size=20)
plt.ylabel("Mean pop-weighted greenness relative variation 2000-2015",size=20)
plt.tight_layout()
plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/figs/scatter_transport_5k_vs_ndvi_pop_subregions.png")
#plt.show()

#%%
##################################################
#     Densité moyenne de population calculée     #
#                    à partir                    #
#                du modèle urbain                #
#                      VS                        # 
# % de la ville (km²) ayant accès aux transports #
##################################################

#%% Scatter plots for all cities
def log_law(x, a, b):
    return a*np.log(x)+b
def linear_law(x, a, b):
    return a*x+b
def power_law(x, a, b):
    return a*np.power(x, b)
year_beg = '2000'
year_end = '2015'
for access_threshold in [3000, 5000, 10000] :
    print('access_threshold',access_threshold)
    for choice in [year_beg,year_end,'delta'] :
        if choice =='delta' :
            access = np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+year_end]) - np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+year_beg])
            density = np.array(shape.loc[:,'Avg_pop_density_'+year_end]) - np.array(shape.loc[:,'Avg_pop_density_'+year_beg])
        else :
            access = np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+choice])
            density = np.array(shape.loc[:,'Avg_pop_density_'+choice])
        country_list=shape.loc[:,'Country']
        color=[color_dict.get(x) for x in country_list]
        plt.scatter(density,access,c=color,marker='o')
        #legend_elements = []
        #for country in df.columns :
        #    legend_elements.append(Line2D([0], [0], color=color_dict[country], lw=4,label=country))
        plt.xlabel('Density '+choice)
        plt.ylabel('Transport access '+choice)
        #plt.legend([country for country in color_dict.keys()],[color for color in color_dict.values()])
        if choice == 'delta' :
            density_no_nans=list(density)
            access_no_nans=list(access)
            nb_cut=0
            for idx in np.argwhere(np.isnan(density)):
                density_no_nans.pop(*idx-nb_cut)
                access_no_nans.pop(*idx-nb_cut)
                nb_cut+=1
            pars, cov = curve_fit(f=linear_law, xdata=density_no_nans, ydata=access_no_nans, p0=[0, 0], bounds=(-np.inf, np.inf))
            plt.plot(np.sort(density_no_nans),linear_law(np.sort(density_no_nans), *pars),'blue')
            print(r2_score(access_no_nans, linear_law(np.array(density_no_nans),*pars)))
        
        plt.tight_layout()
        #plt.legend(handles=legend_elements,loc='best')
        plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/Code/figures_GHS_"+str(threshold)+"/scatter_density_transport_"+choice+"_threshold_"+str(access_threshold)+".jpg")
        plt.grid()
        plt.show()
#%% Plot evolution of 2 indicators for each city
for access_threshold in [3000, 5000, 10000] :
    print('access_threshold',access_threshold)
    for idx in tqdm(shape.index) :
        density = np.array(shape[['Avg_pop_density_1975','Avg_pop_density_1990','Avg_pop_density_2000','Avg_pop_density_2015']].loc[idx])
        access = np.array(shape[['Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_1975','Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_1990',
        'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_2000','Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_2015']].loc[idx])
        fig, ax1 = plt.subplots() 
    
        ax1.set_xlabel('Time') 
        ax1.set_ylabel('Average density', color = 'red') 
        ax1.plot([1975,1990,2000,2015], density, color = 'red') 
        ax1.tick_params(axis ='y', labelcolor = 'red') 
        
        ax2 = ax1.twinx() 

        ax2.set_ylabel('Transport accessibility', color = 'blue') 
        ax2.plot([1975,1990,2000,2015], access, color = 'blue') 
        ax2.tick_params(axis ='y', labelcolor = 'blue') 
        
        #plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/Code/figures_GHS_"+str(threshold)+"/fig_cities_density_transit_access_SMOD_"+str(threshold)+"/density_transit_access_"+str(shape.loc[idx,'ORIG_FID'])+"_threshold_"+str(access_threshold)+".jpg")
        #plt.show()
        plt.close()
        #break
#%%
##################################################
#     Densité moyenne de population calculée     #
#       à partir de l'artificialisation et       #
#             non du modèle urbain               #
#                      VS                        # 
# % de la population ayant accès aux transports  #
##################################################
#%% Scatter plots for all cities
year_beg = '2000'
year_end = '2015'
for access_threshold in [3000, 5000, 10000] :
    print('access_threshold',access_threshold)
    for choice in [year_beg,year_end,'delta'] :
        if choice =='delta' :
            access = np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+year_end]) - np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+year_beg])
            density = np.array(shape.loc[:,'Avg_pop_density_'+year_end]) - np.array(shape.loc[:,'Avg_pop_density_'+year_beg])
        else :
            access = np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+choice])
            density = np.array(shape.loc[:,'Avg_pop_density_'+choice])
        country_list=shape.loc[:,'Country']
        color=[color_dict.get(x) for x in country_list]
        plt.scatter(density,access,c=color,marker='o')
        #legend_elements = []
        #for country in df.columns :
        #    legend_elements.append(Line2D([0], [0], color=color_dict[country], lw=4,label=country))
        plt.xlabel('Density '+choice)
        plt.ylabel('Transport access '+choice)
        #plt.legend([country for country in color_dict.keys()],[color for color in color_dict.values()])
        if choice == 'delta':
            density_no_nans=list(density)
            access_no_nans=list(access)
            nb_cut=0
            for idx in np.argwhere(np.isnan(density)):
                density_no_nans.pop(*idx-nb_cut)
                access_no_nans.pop(*idx-nb_cut)
                nb_cut+=1
            pars, cov = curve_fit(f=linear_law, xdata=density_no_nans, ydata=access_no_nans, p0=[0, 0], bounds=(-np.inf, np.inf))
            plt.plot(np.sort(density_no_nans),linear_law(np.sort(density_no_nans), *pars),'blue')
            print(r2_score(access_no_nans, linear_law(np.array(density_no_nans),*pars)))
        plt.tight_layout()
        #plt.legend(handles=legend_elements,loc='best')
        plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/Code/figures_GHS_"+str(threshold)+"/scatter_density_transport_"+choice+"_threshold_"+str(access_threshold)+".jpg")
        plt.grid()
        plt.show()
#%% Plot evolution of 2 indicators for each city
for access_threshold in [3000, 5000, 10000] :
    print('access_threshold',access_threshold)
    for idx in tqdm(shape.index) :
        density = np.array(shape[['Avg_pop_density_metric_artificial_area_1975','Avg_pop_density_metric_artificial_area_1990','Avg_pop_density_metric_artificial_area_2000','Avg_pop_density_metric_artificial_area_2015']].loc[idx])
        access = np.array(shape[['Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_1975','Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_1990',
        'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_2000','Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_2015']].loc[idx])
        fig, ax1 = plt.subplots() 
    
        ax1.set_xlabel('Time') 
        ax1.set_ylabel('Average density', color = 'red') 
        ax1.plot([1975,1990,2000,2015], density, color = 'red') 
        ax1.tick_params(axis ='y', labelcolor = 'red') 
        
        ax2 = ax1.twinx() 

        ax2.set_ylabel('Transport accessibility', color = 'blue') 
        ax2.plot([1975,1990,2000,2015], access, color = 'blue') 
        ax2.tick_params(axis ='y', labelcolor = 'blue') 
        
        #plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/Code/figures_GHS_"+str(threshold)+"/fig_cities_density_transit_access_BUILT_"+str(threshold)+"/density_transit_access_"+str(shape.loc[idx,'ORIG_FID'])+"_threshold_"+str(access_threshold)+".jpg")
        #plt.show()
        plt.close()
        #break

#%%
##################################################
#            Artificialisation/habitants         #
#                      VS                        # 
# % de la population ayant accès aux transports  #
##################################################
#%% Scatter plots for all cities
def exponential(x, a, b):
    return a*np.exp(b*x)
def power_law(x, a, b):
    return a*np.power(x, b)
year_beg = '2000'
year_end = '2015'
for access_threshold in [3000, 5000, 10000] :
    print('access_threshold',access_threshold)
    for choice in [year_beg,year_end,'delta'] :
        #plt.figure(figsize=(16,12))
        if choice =='delta' :
            access = (np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+year_end]) - np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+year_beg]))#/np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_1975'])
            artif_per_hab = (np.array(shape.loc[:,'Artificial_area_'+year_end]/shape.loc[:,'Total_pop_'+year_end]) - np.array(shape.loc[:,'Artificial_area_'+year_beg]/shape.loc[:,'Total_pop_'+year_beg]))/np.array(shape.loc[:,'Artificial_area_'+year_beg])#/shape.loc[:,'Total_pop_1975'])
        else :
            access = np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+choice])
            artif_per_hab = np.array(shape.loc[:,'Artificial_area_'+choice]/shape.loc[:,'Total_pop_'+choice])
        country_list=shape.loc[:,'Country']
        color=[color_dict.get(x) for x in country_list]
        plt.scatter(artif_per_hab,access,c=color,marker='o')
        #legend_elements = []
        #for country in df.columns :
        #    legend_elements.append(Line2D([0], [0], color=color_dict[country], lw=4,label=country))
        plt.xlabel('Artificial area per capita '+choice)
        plt.ylabel('Population fraction transport access '+choice)
        #plt.legend([country for country in color_dict.keys()],[color for color in color_dict.values()])
        if choice == 'delta':
            artif_per_hab_no_nans=list(artif_per_hab)
            access_no_nans=list(access)
            nb_cut=0
            for idx in np.argwhere(np.isnan(artif_per_hab)):
                artif_per_hab_no_nans.pop(*idx-nb_cut)
                access_no_nans.pop(*idx-nb_cut)
                nb_cut+=1
            for idx in np.argwhere(np.isnan(access)):
                artif_per_hab_no_nans.pop(*idx-nb_cut)
                access_no_nans.pop(*idx-nb_cut)
                nb_cut+=1
            pars, cov = curve_fit(f=linear_law, xdata=artif_per_hab_no_nans, ydata=access_no_nans, p0=[0, 0], bounds=(-np.inf, np.inf))
            plt.plot(np.sort(artif_per_hab_no_nans),linear_law(np.sort(artif_per_hab_no_nans), *pars),'blue')
            print(r2_score(access_no_nans, linear_law(np.array(artif_per_hab_no_nans),*pars)))
        plt.tight_layout()
        #plt.legend(handles=legend_elements,loc='best')
        #pars, cov = curve_fit(f=exponential, xdata=artif_per_hab, ydata=access, p0=[0, 0], bounds=(-np.inf, np.inf))
        #if choice != 'delta':
        #    pars, cov = curve_fit(f=power_law, xdata=artif_per_hab, ydata=access, p0=[0, 0], bounds=(-np.inf, np.inf))
        #    plt.plot(np.sort(artif_per_hab),power_law(np.sort(artif_per_hab), *pars),'black')
        plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/Code/figures_GHS_"+str(threshold)+"/scatter_density_transport_"+choice+"_threshold_"+str(access_threshold)+".jpg")
        plt.grid()
        plt.show()
    break


#%% Scatter plots for all cities
def exponential(x, a, b):
    return a*np.exp(b*x)
def power_law(x, a, b):
    return a*np.power(x, b)
year_beg = '1975'
year_end = '2015'
for access_threshold in [3000, 5000, 10000] :
    print('access_threshold',access_threshold)
    for choice in [year_beg,year_end,'delta'] :
        #plt.figure(figsize=(16,12))
        if choice =='delta' :
            access = (np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+year_end]) - np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+year_beg]))#/np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_1975'])
            artif_per_hab = (np.array(shape.loc[:,'Artificial_area_'+year_end]/shape.loc[:,'Total_pop_'+year_end]) - np.array(shape.loc[:,'Artificial_area_'+year_beg]/shape.loc[:,'Total_pop_'+year_beg]))/np.array(shape.loc[:,'Artificial_area_'+year_beg])#/shape.loc[:,'Total_pop_1975'])
        else :
            access = np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+choice])
            artif_per_hab = np.array(shape.loc[:,'Artificial_area_'+choice]/shape.loc[:,'Total_pop_'+choice])
        country_list=shape.loc[:,'Country']
        color=[color_dict.get(x) for x in country_list]
        plt.scatter(artif_per_hab,access,c=color,marker='o')
        #legend_elements = []
        #for country in df.columns :
        #    legend_elements.append(Line2D([0], [0], color=color_dict[country], lw=4,label=country))
        plt.xlabel('Artificial area per capita '+choice)
        plt.ylabel('Population fraction transport access '+choice)
        #plt.legend([country for country in color_dict.keys()],[color for color in color_dict.values()])
        plt.tight_layout()
        #plt.legend(handles=legend_elements,loc='best')
        pars, cov = curve_fit(f=exponential, xdata=artif_per_hab, ydata=access, p0=[0, 0], bounds=(-np.inf, np.inf))
        #plt.plot(np.sort(artif_per_hab),exponential(np.sort(artif_per_hab), *pars),'blue')
        if choice != 'delta':
            pars, cov = curve_fit(f=power_law, xdata=artif_per_hab, ydata=access, p0=[0, 0], bounds=(-np.inf, np.inf))
            plt.plot(np.sort(artif_per_hab),power_law(np.sort(artif_per_hab), *pars),'black')
        plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/Code/figures_GHS_"+str(threshold)+"/scatter_density_transport_"+choice+"_threshold_"+str(access_threshold)+".jpg")
        plt.grid()
        #residuals = power_law(np.sort(artif_per_hab))- power_law(np.sort(artif_per_hab), *pars)
        #ss_res = np.sum(residuals**2)
        #ss_tot = np.sum((power_law(np.sort(artif_per_hab)-np.mean(power_law(np.sort(artif_per_hab)))**2)
        #r_squared = 1 - (ss_res / ss_tot)
        #print(r_squared)
        plt.show()
        #break

#%%
##################################################
#                Etalement marginal              #
#                       VS                       #
#    variation marginale d'accès au transport    #
##################################################
#%%Scatter lot de l'étalement marginal vs la variation marginale d'accès au transport
year_beg = '1975'
year_end = '2015'
for access_threshold in [3000, 5000, 10000] :
    print('access_threshold',access_threshold)
    #plt.figure(figsize=(16,12))

    delta_pop = np.array(shape.loc[:,'Urban_pop_'+year_end]) - np.array(shape.loc[:,'Urban_pop_'+year_beg])
    margin_access = (np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+year_end]) - np.array(shape.loc[:,'Rate_area_transport_access_threshold_'+str(access_threshold)[:-3]+'k_'+year_beg]))/delta_pop
    margin_sprawl = (np.array(shape.loc[:,'Artificial_area_'+year_end]) - np.array(shape.loc[:,'Artificial_area_'+year_beg]))/delta_pop

    country_list=shape.loc[:,'Country']
    color=[color_dict.get(x) for x in country_list]
    nb_cut=0
    for idx in np.argwhere(np.isnan(margin_access)) :
        margin_access = np.delete(margin_access,*idx-nb_cut)
        margin_sprawl = np.delete(margin_sprawl,*idx-nb_cut)
        color.pop(*idx-nb_cut)
        nb_cut+=1
    color.pop(np.argmin(margin_access))
    margin_sprawl = np.delete(margin_sprawl,np.argmin(margin_access))
    margin_access = np.delete(margin_access,np.argmin(margin_access))
    plt.scatter(margin_access,margin_sprawl,c=color,marker='o')
    #legend_elements = []
    #for country in df.columns :
    #    legend_elements.append(Line2D([0], [0], color=color_dict[country], lw=4,label=country)    
    plt.xlabel('Marginal transport access between '+year_beg+' and '+year_end)
    plt.ylabel('Marginal sprawl between '+year_beg+' and '+year_end)
    #plt.legend([country for country in color_dict.keys()],[color for color in color_dict.values()])
    plt.tight_layout()
    #plt.legend(handles=legend_elements,loc='best')
    #pars, cov = curve_fit(f=exponential, xdata=artif_per_hab, ydata=access, p0=[0, 0], bounds=(-np.inf, np.inf))
    #plt.plot(np.sort(artif_per_hab),exponential(np.sort(artif_per_hab), *pars),'blue')
    #pars, cov = curve_fit(f=power_law, xdata=artif_per_hab, ydata=access, p0=[0, 0], bounds=(-np.inf, np.inf))
    #plt.plot(np.sort(artif_per_hab),power_law(np.sort(artif_per_hab), *pars),'black')
    plt.savefig("D:/Ubuntu/M2_EEET/Stage_CIRED/Code/figures_GHS_"+str(threshold)+"/scatter_density_transport_"+choice+"_threshold_"+str(access_threshold)+".jpg")
    plt.grid()
    #residuals = power_law(np.sort(artif_per_hab))- power_law(np.sort(artif_per_hab), *pars)
    #ss_res = np.sum(residuals**2)
    #ss_tot = np.sum((power_law(np.sort(artif_per_hab)-np.mean(power_law(np.sort(artif_per_hab)))**2)
    #r_squared = 1 - (ss_res / ss_tot)
    #print(r_squared)
    plt.show()
    #break
