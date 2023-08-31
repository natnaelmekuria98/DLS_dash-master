# Read data 

import pandas as pd
import os
# import shapefile
import json
#import matplotlib.pyplot as plt
import pycountry
import numpy as np

# Set options to view more column 

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 20)
pd.set_option('display.float_format', lambda x: '%.3f' % x)


#import plotly.express as px

# x) DLS 2021 data -----------------------------------------------------------------------------------------------------------------------------------------------------

# Similar to dls_mapped_data
DLS_features_by_lang = pd.read_csv("./data/DLS_2021/DLS features for all languages.csv", encoding = 'UTF-8')

# Similar to DLS
DLS_scores_by_lang = pd.read_csv("./data/DLS_2021/DLS scores for all languages.csv", encoding = 'UTF-8')

DLS_scores_by_lang['Rank'] = DLS_scores_by_lang["Adjusted_Score"].rank(ascending=False,method="min")

DLS_scores_by_lang['DLS_Level'] = pd.Categorical(DLS_scores_by_lang['DLS_Level'],
                                                 ordered=True,
                                                 categories=['Still', 'Emerging', 'Ascending',
                                                             "Vital","Thriving"] )

# similar to dls_mapped_data_by_ft
DLS_all_features = pd.read_csv("./data/DLS_2021/List of all DLS features.csv", encoding = 'UTF-8')


# Transforms EGIDs variable into a categorical variable
# DLS_GLP_EGID_data["EGIDS"] = pd.Categorical(DLS_GLP_EGID_data["EGIDS"],['x10','9','8b','8a','7','6b','6a','5','4','3','2','1','0'], ordered = True)

# #old_DLS_GLP_EGID_data["EGIDS"] = pd.Categorical(old_DLS_GLP_EGID_data["EGIDS"],['x10','9','8b','8a','7','6b','6a','5','4','3','2','1','0'], ordered = True)

# # Transform cluster variable into a categorical variable
# DLS_GLP_EGID_data["cluster"] = pd.Categorical(DLS_GLP_EGID_data["cluster"],['still','emerging',  'ascending', 'vital', 'thriving'], ordered = True)




# 1) GLPs (Vanilla and Polygon weighted ) ------------------------------------------------------------------------------------------------------------------------------ 

# TODO: Calculate Russia an United States Polygon Weighted GLPs

GLPs = pd.read_csv("./data/GLPs.csv", encoding = 'ISO8859-1')

# Drop incomplete columns of ISO-3
GLPs.drop(columns = ['ISO3'],inplace=True)

# 2) Languages of the world - TOLs--------------------------------------------------------------------------------------------------------------------------------------

TOLs = pd.read_table("./data/Table_of_Languages.tab",encoding = "UTF-8")

# Corrects for ISO that are nan (Chinese nan) to 'nan'

null_isos_tols = TOLs['ISO_639'].isnull()

TOLs.loc[null_isos_tols,'ISO_639'] = str('nan')

# 3) Loads Digital Language Score , Gross Language Product and EGIDs data... ( "placeholder" I need to update the data ) - DLS_GLP_EGID_data ---------------------------

## a) Merging GLP,TOLs with new dls data 

#DLS_GLP_EGID_data = DLS[["ISO_639","cluster","adjusted_total"]].merge(TOLs, on = "ISO_639")
DLS_GLP_EGID_data = DLS_scores_by_lang[["ISO_639","Reference_Name","DLS_Level","Adjusted_Score","Assistant","Speech",
                                        "Meaning","Localized","Surface","Encoding","Content"]].merge(TOLs, on = "ISO_639")

#old_DLS_GLP_EGID_data = old_DLS[["ISO_639","cluster","adjusted_total"]].merge(TOLs, on = "ISO_639")

# Sum GLPs by language
GLPs_grouped = GLPs.groupby("ISO_639").sum(numeric_only=True)[["GLP_vanila","GLP_All_users","w_GDP_lang_kummu","w_GDP_lang_GHS_kummu"]]

# indext to column
GLPs_grouped = GLPs_grouped.reset_index()

# Merge DLS data with GLPs grouped by ISO 
DLS_GLP_EGID_data = DLS_GLP_EGID_data.merge(GLPs_grouped, on = "ISO_639",how = "left")

# Cleaning
del(GLPs_grouped)

# Transforms EGIDs variable into a categorical variable
DLS_GLP_EGID_data["EGIDS"] = pd.Categorical(DLS_GLP_EGID_data["EGIDS"],['x10','9','8b','8a','7','6b','6a','5','4','3','2','1','0'], ordered = True)

#old_DLS_GLP_EGID_data["EGIDS"] = pd.Categorical(old_DLS_GLP_EGID_data["EGIDS"],['x10','9','8b','8a','7','6b','6a','5','4','3','2','1','0'], ordered = True)

# Transform cluster variable into a categorical variable
#DLS_GLP_EGID_data["cluster"] = pd.Categorical(DLS_GLP_EGID_data["cluster"],['still','emerging',  'ascending', 'vital', 'thriving'], ordered = True)

DLS_GLP_EGID_data["DLS_Level"] = pd.Categorical(DLS_GLP_EGID_data["DLS_Level"],['Still','Emerging',  'Ascending', 'Vital', 'Thriving'], ordered = True)

#old_DLS_GLP_EGID_data["cluster"] = pd.Categorical(old_DLS_GLP_EGID_data["cluster"],['still','emerging',  'ascending', 'vital', 'thriving'], ordered = True)

#new_DLS_GLP_EGID_data[(new_DLS_GLP_EGID_data["EGIDS"] > "x10") & (new_DLS_GLP_EGID_data["GLP_vanila"] > "x10")]


## b) Mapping cluster and EGIDS scores ---------------------------------------------------------------------------------------------------------------------------------

# Make groupping  for 3x3 matrix 

mapping = { 'still' : 'Dormant','emerging':'Ascending','ascending':'Ascending','vital':'Ascending' ,  'thriving' :'Developed' }

#DLS_GLP_EGID_data['cluster_mapping'] = DLS_GLP_EGID_data.cluster.map(mapping)
DLS_GLP_EGID_data['cluster_mapping'] = DLS_GLP_EGID_data.DLS_Level.map(mapping)

#old_DLS_GLP_EGID_data['cluster_mapping'] = old_DLS_GLP_EGID_data.cluster.map(mapping)

mapping = { 'x10':'Endangered','9':'Endangered','8b':'Endangered','8a':'Endangered','7':'Endangered' ,
           '6b':'Vulnerable','6a':'Vulnerable','5':'Vulnerable',  
           '4':'Institutional','3':'Institutional','2':'Institutional','1':'Institutional','0':'Institutional' }

#DLS_GLP_EGID_data['EGIDS_mapping'] = DLS_GLP_EGID_data.EGIDS.map(mapping)
DLS_GLP_EGID_data['EGIDS_mapping'] = DLS_GLP_EGID_data.EGIDS.map(mapping)

#old_DLS_GLP_EGID_data['EGIDS_mapping'] = old_DLS_GLP_EGID_data.EGIDS.map(mapping)

DLS_GLP_EGID_data.rename(columns={'GLP_vanila': 'GLP', 'L1_Users': 'L1','All_Users':'All'}, inplace=True)

# L2 calculation for TOLs 
DLS_GLP_EGID_data['L2'] = DLS_GLP_EGID_data["All"].fillna(0) - DLS_GLP_EGID_data["L1"].fillna(0)


# 4) Languages by country - LICs ---------------------------------------------------------------------------------------------------------------------------------------

#LICs = pd.read_csv("./data/LICs.csv",encoding = "ISO8859-1")
LICs = pd.read_table("./data/Table_of_LICs.tab",encoding = "UTF-8")


# Corrects for ISO that are nan (Chinese nan) to 'nan'

null_isos = LICs['ISO_639'].isnull()

LICs.loc[null_isos,'ISO_639'] = str('nan')

# set na as 'no data'
null_isos = LICs['EGIDS'].isnull()

LICs.loc[null_isos,'EGIDS'] = str('no data')

# Transforms EGIDs variable into a categorical variable
LICs["EGIDS"] = pd.Categorical(LICs["EGIDS"],["no data",'x10','9','8b','8a','7','6b','6a','5','4','3','2','1','0'], ordered = True)


# Transforms NaN from Namibia to NA

LICs.loc[LICs["Country_Name"]=='Namibia','Country_Code'] = str('NA')

# Creates column with ISO 3 data 

def gets_iso3_from_iso2(country):
    
    #print(country)
    #if ( type(country) != type(str()) ):
    #    country = "NA"

    return(pycountry.countries.get(alpha_2 = country).alpha_3)

LICs['iso_3'] = LICs['Country_Code'].map(gets_iso3_from_iso2)

# Language percentage of the total pop of country

LICs["L1_percentage_of_country_L1"] = LICs["L1_Users"] / LICs.groupby("Country_Code")["L1_Users"].transform('sum')

# 5) HHI rank - hhi_rank -----------------------------------------------------------------------------------------------------------------------------------------------

## OBS.: Used to calculate the rank, only used one time, the result is saved in ./data/hhi_rank.csv ####################################################################

#def HHI_ranker(iso):

#    df_temp = HHI(iso,users="L1_Users")

#    df_temp['ISO_639'] = iso

#    return(df_temp)

## Calculates HHI 
#hhi_rank = [HHI_ranker(iso) for iso in LICs['ISO_639'].unique() ]

## concat list into df
#hhi_rank = pd.concat(hhi_rank)

## Removes languages without L1_Users
#hhi_rank = hhi_rank[hhi_rank["L1_Users"] != 0 ]

## Save HHI rank
#hhi_rank["hhi_rank"] = hhi_rank["ISO_HHI"].rank(method = 'min', ascending = True)

#hhi_rank.to_csv("./data/hhi_rank.csv")

#########################################################################################################################################################################

hhi_rank = pd.read_csv("./data/hhi_rank.csv", encoding = "ISO8859-1")

# Get HHI rank percentile

hhi_rank['Percentile'] = np.argsort(np.argsort(hhi_rank['ISO_HHI'])) * 100. / (len(hhi_rank['ISO_HHI']) - 1)

# 6) T-index - t_index_by_language , t_index_by_language_with_countries ------------------------------------------------------------------------------------------------

# a) t-index by language
t_index_by_language = pd.read_csv("./data/t_index_by_lang.csv", encoding = 'ISO8859-1')

t_index_by_language = t_index_by_language.merge(TOLs[["ISO_639","Language_Name"]],how="left")

# b) t-index by language with country data
t_index_by_language_with_countries = pd.read_csv("./data/t_index_by_lang_with_country_data.csv", encoding = 'ISO8859-1')

#t_index_by_language_with_countries['internet_penetration'] = t_index_by_language_with_countries['internet_users_by_lang']/t_index_by_language_with_countries['SP.POP.TOTL']

#t_index_by_language[(t_index['Language_Name'] == 'English') & (t_index['year'] == 2017) ]

t_index_by_language_with_countries.loc[t_index_by_language_with_countries['country'] == 'Namibia',"iso2c"] = str("NA")

# Log transformation of the t-index ( makes the data more normalized than the Standart transformation )
t_index_by_language_with_countries['log_t_index'] = np.log(t_index_by_language_with_countries["t_index"])

# Normalized log t-index ( set the data between 0 and 1)
# NOTE: did not worked as I though. In USA with Spanish selected, Spain is not better than Colombia as in the T-index
t_index_by_language_with_countries['norm_log_t_index'] =  (t_index_by_language_with_countries["log_t_index"] - min(t_index_by_language_with_countries["log_t_index"]))/\
                                                          (max(t_index_by_language_with_countries["log_t_index"]) - min(t_index_by_language_with_countries["log_t_index"]) )

# Making the rank for the t-index
t_index_by_language_with_countries['rank_t_index'] = t_index_by_language_with_countries['t_index'].rank(pct=True)


# 7) World Bank data --------------------------------------------------------------------------------------------------------------------------------------------------

worldbank_data = pd.read_csv("./data/WorldBank/worldbankbulk.csv", encoding = 'ISO8859-1')

worldbank_data = worldbank_data[worldbank_data["date"]>1999]

worldbank_data = worldbank_data.astype({"date": int})

# 8) Currency data ----------------------------------------------------------------------------------------------------------------------------------------------------
# From babel 
#currency_by_country = pd.read_csv("./data/currencies_by_country.csv", encoding = 'ISO8859-1')
currency_by_country = pd.read_csv("./data/currencies_by_country.csv", encoding = 'UTF-8')

# 9) Legal status definition table ------------------------------------------------------------------------------------------------------------------------------------

legal_status_def_table = pd.read_csv("./data/dls/legal_status.csv", encoding = 'ISO8859-1',sep=';')

# 10) EGIDS definition table -------------------------------------------------------------------------------------------------------------------------------------------

egids_def_table = pd.read_csv("./data/dls/EGIDS.csv", encoding = 'ISO8859-1',sep=';')

# 11) DLS classification description -----------------------------------------------------------------------------------------------------------------------------------

dls_class_descr = pd.read_csv("./data/DLS_2021/classifications_description.csv", encoding = 'ISO8859-1',sep=';')

# 12) DLS classification count threshold
# OBS.: The thresholds are get the quartile (.25,.5,.75,1.0 ) of the number of each category. 
#       If two adjacent quartiles have the same upper limit, 1 is added to tue upper limit of the higher quartile 
dls_class_threshold = pd.read_csv("./data/DLS_2021/level_quarts.csv", encoding = 'ISO8859-1')

# 13) DLS adjustesd score by classification ----------------------------------------------------------------------------------------------------------------------------
# TODO: REMOVE WRONG COLLECTED ISO 
# dls_adjusted_score = pd.read_csv('./data/dls/all_numeric_adjusted_results.csv')

# 14) ICL temp ---------------------------------------------------------------------------------------------------------------------------------------------------------

# Gurovich paper data
#dicl = pd.read_csv("./data/dicl.csv", encoding = 'ISO8859-1')

# NOTE: There are some differences between the data calculated and the one offered by the paper, e.g. Ukraine and Latvia having Common Official Language in their data,
# Falkland not having english as offical language. 

# Data calculated by Marco
dicl = pd.read_pickle("./data/custom_icl")

dicl.rename(columns = {'COL':'col', 'CNL':'cnl','LP': 'lp'}, inplace = True)

# 15) Gravity Model (GME) Coefficients ---------------------------------------------------------------------------------------------------------------------------------------

# Gravity model coefficients used for market expansion index
# All models:
#['fast_ppmlModel_all_sample', 'fast_ppmlModel_only_international',
#       'fast_ppmlModel_FEVD_all', 'fast_ppmlModel_FEVD',
#       'model_step_2_all', 'model_step_2', 'model_pesaran_all',
#       'model_pesaran', 'TSFE_all', 'TSFE',
#       'fast_ppmlModel_wo_importer_all', 'fast_ppmlModel_wo_importer']


## Get GME coefficients  
gme_by_sector = pd.read_csv('./data/Gravity_Models/coef_by_sector_cl.csv')

gme_by_industry = pd.read_csv('./data/Gravity_Models/coef_by_industry_cl.csv')

# Models to use ( best theoretically )
# fast_ppmlModel_FEVD_all - For the GME coefficients
# TSFE_all - For the fixed effects coefficients 
 
## All sectors
#gme_by_sector['sector_industry'].unique()
## All industries
#gme_by_industry[['industry_descr','sector_industry']].drop_duplicates()


# count = 1
# for result in results_folder:
#     print(result)
#     path_dls = "../../../Data/Ethnologue/DLS_data/DLS Datasets/"
#     path_dls = path_dls + result
#     if count == 1:
#     DLS = pd.read_csv(path_dls + "/DLS scores for all languages.csv")
#     DLS['year'] = result[:4]
#     else:
#     DLS_temp = pd.read_csv(path_dls + "/DLS scores for all languages.csv")
#     DLS_temp['year'] = result[:4]
#     DLS = pd.concat([DLS, DLS_temp])
#     count = count + 1