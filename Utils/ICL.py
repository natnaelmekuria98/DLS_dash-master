# ICL

# 1) COL - Common Offial Language

## 1.1) Setup ----------------------------------------------------------------------------------------------------------------------------------------------------------

## filtering by function label 
LICs_institutional = LICs[LICs["Institutional"]==1].dropna(subset = ['Function_Label'])

## Funtion Labels filter. Gurevich et. al (one_nation_one_language) whether national or provincial, statutory or de facto
function_labels = ['De facto language of provincial identity',
                   'Statutory provincial language',
                   'De facto national working language',
                   #'Recognized language',
                   'Statutory national language',
                   #'Language of recognized nationality',
                   'De facto language of national identity',
                   'Statutory language of provincial identity',
                   'De facto national language',
                   'Statutory national working language',
                   'Provincially recognized language', 
                   'De facto provincial language',
                   'Statutory provincial working language',
                   'Statutory language of national identity',
                   'De facto provincial working language']

## Official languages
LICs_institutional = LICs_institutional[LICs_institutional["Function_Label"].isin(function_labels)]

## List of countries
Country_list = LICs_institutional[["Country_Name","Country_Code","iso_3"]].drop_duplicates()

## 1.2) Function get the COL for a given country
# NOTE: Try saving a list if the loop is too slow
def Get_Country_Common_Official_Language_With_All_Countries(iso_country):

    #iso_country = "USA"

    # Get Country's Officials Languages
    country_official_languages = LICs_institutional[LICs_institutional['iso_3']==iso_country]["ISO_639"].values

    # Prepare output df
    df_lics_temp = LICs_institutional[["Country_Code","iso_3","ISO_639"]].groupby("iso_3")['ISO_639'].apply(list).reset_index()

    # Function to check selected country official languages with a given list 
    def check_list_with_list(iso3_list):
        return any( iso3 in country_official_languages  for iso3 in iso3_list ) 

    # Iterate the function above with all the countries to check whether it they have a Common Official Language
    df_lics_temp.loc[:,'COL'] = [ check_list_with_list(iso3_list) for iso3_list in df_lics_temp["ISO_639"] ]

    # Map boolean
    df_lics_temp.loc[:,'COL'] = df_lics_temp.loc[:,'COL'].map({True:1,False:0})
    
    # Save country name
    df_lics_temp.loc[:,'iso'] = iso_country

    df_lics_temp = df_lics_temp[["iso","iso_3","COL"]]

    df_lics_temp.rename(columns = {'iso':'ISO3', 'iso_3':'ISO3_2'}, inplace = True)

    return df_lics_temp

## 1.3) Calculate the COL for all countries
## NOTE: "NEVER grow a DataFrame!" https://stackoverflow.com/questions/13784192/creating-an-empty-pandas-dataframe-then-filling-it
COL_list = []

# Loop for append the list
 
for iso_country in  Country_list["iso_3"]:

    COL_list.extend(Get_Country_Common_Official_Language_With_All_Countries(iso_country)[["ISO3","ISO3_2","COL"]].to_dict('records'))

## 1.4) Transforming the List into a dataframe
df_COL = pd.DataFrame(COL_list)


# 2) CNL - Common National Language ------------------------------------------------------------------------------------------------------------------------------------

# CNL_{i,j} = sum{ l_{j,k} * l_{l,k} } where l is the percentage of speakers of language k in common withing country j,l

## Sperating the L1 percentage per country data
df_cnl_temp = LICs[["Country_Code","iso_3","ISO_639","L1_percentage_of_country_L1"]]

# Loop for append the list
CNL_list = [] 
for iso_country in  Country_list["iso_3"]:

    for iso_country_2 in Country_list["iso_3"]:

        # Get the data for country 1
        lang_country_1 = df_cnl_temp[df_cnl_temp["iso_3"]==iso_country]
        
        # Get the data for country 2
        lang_country_2 = df_cnl_temp[df_cnl_temp["iso_3"]==iso_country_2]

        # Get the intersection between the two language group
        lang_intersection = lang_country_1[["ISO_639","L1_percentage_of_country_L1"]].merge(lang_country_2[["ISO_639","L1_percentage_of_country_L1"]], how='inner',left_on = 'ISO_639',right_on = 'ISO_639')

        # CNL calculus
        CNL_1_2 = sum((lang_intersection["L1_percentage_of_country_L1_x"] * lang_intersection["L1_percentage_of_country_L1_y"]).dropna())

        # Saving as a dict records
        CNL_temp = { "ISO3": iso_country, "ISO3_2": iso_country_2 , "CNL": CNL_1_2 }

        # Appending the data
        CNL_list.append(CNL_temp)


## Transforming the List into a dataframe
df_CNL = pd.DataFrame(CNL_list)




# 3) LP - Language Proximity -------------------------------------------------------------------------------------------------------------------------------------------

all_lp_data = pd.read_pickle("./data/all_lp_data")
 
import time

# Saving LP data for countries
all_countries = []

start_time = time.perf_counter()

# Loop for Country 1
# NOTE: The loop is too slow 
for iso_country in Country_list["iso_3"]:

    print("ISO3 : " + iso_country)
    
    country_lp = []

    # Clock
    loop_start_time = time.perf_counter()

    # Loop for Country 2
    for iso_country_2 in Country_list["iso_3"]:

        # Get the data for country 1
        lang_country_1 = df_cnl_temp[df_cnl_temp["iso_3"]==iso_country].dropna()
        
        # Get the data for country 2
        lang_country_2 = df_cnl_temp[df_cnl_temp["iso_3"]==iso_country_2].dropna()

        #language_proximity(iso_lang_1,iso_lang_2)
        iso_1_lp = []

        # Clock
        inner_loop_start_time = time.perf_counter()

        # Loop for languages of country 1
        for iso_1 in lang_country_1.ISO_639:
            
            ## Clock
            #inner_loop_start_time = time.perf_counter()

            # Get LP from iso 1
            #LP_for_lang_1 = language_proximity_all(iso_1, "L1_Users") # TOO SLOW !!!
            LP_for_lang_1 = pd.DataFrame(all_lp_data[all_lp_data['ISO3']== iso_1 ]['ISO_639'].tolist()[0]) # This is uses a precaculated dataframe with all LPs
            
            ## Clock
            #inner_loop_start_time1 = time.perf_counter() 
            #print("1) ",iso_1," time: ",inner_loop_start_time1 - inner_loop_start_time, "seconds")
            
            # Get All LP from country to iso1
            all_lang2_LPs = lang_country_2.merge(LP_for_lang_1[["ISO_639","distance"]].drop_duplicates(),how='inner',left_on="ISO_639",right_on="ISO_639")
            
            ## Clock
            #inner_loop_start_time2 = time.perf_counter() 
            #print("2) ",iso_1," time: ",inner_loop_start_time2 - inner_loop_start_time1, "seconds")
            
            # Append sum{ LP_{iso_1, country_2}} where country_2 is the set of all languages in that country
            iso_1_lp.append( sum(all_lang2_LPs["L1_percentage_of_country_L1"] * all_lang2_LPs["distance"]) )
            
            ## Clock
            #inner_loop_start_time3 = time.perf_counter() 
            #print("3) ",iso_1," time: ",inner_loop_start_time3 - inner_loop_start_time2, "seconds")
        
        # Save sum{ LP_{iso_1, country_2}} for all iso_1 in country_1
        lang_country_1['distance'] = iso_1_lp


         # Clock
        loop_time = time.perf_counter() 
        print("ISO3: ", iso_country ," loop time: ", loop_time - inner_loop_start_time )

        df_LP_1_2 = {"ISO3": iso_country, "ISO3_2": iso_country_2,
                     "LP":sum(lang_country_1["L1_percentage_of_country_L1"] * lang_country_1["distance"]) }
        
        
        country_lp.append(df_LP_1_2)

        # Clock
        inner_loop_time = time.perf_counter() 
        print("ISO3: ", iso_country , " ISO3_2: " , iso_country_2 , " Inner Loop time: ", inner_loop_time - loop_time , "seconds")
        
    
    # Clock
    loop_time = time.perf_counter() 
    print("ISO3: ", iso_country ," loop time: ", loop_time - loop_start_time )

    #df_LP_1_2 = { country_lp  }

    all_countries.extend(country_lp)

#Country_list['LP'] = country_lp

df_LP =  pd.DataFrame(all_countries)



print("Total time: ", time.perf_counter() - start_time)


# Saving the data
df_LP.to_pickle("./data/DICL/df_LP")

df_CNL.to_pickle("./data/DICL/df_CNL")

df_COL.to_pickle("./data/DICL/df_COL")

# Merging all the ICL factors
df_ICL = df_COL.merge(df_CNL).merge(df_LP)

# Calculating the ICL. Mean of the three columns
df_ICL['cl'] = df_ICL[['COL','CNL','LP']].mean(axis=1)

df_ICL.to_pickle("./data/custom_icl")




# Calculating all LP #### DO NOT RUN ! ####

def lp_to_list(x):

   temp = language_proximity_all_tols(x)[["ISO_639","distance"]].to_dict('records')

   return temp

# Clock
start_time = time.perf_counter() 

# Apply language_proximity_all_tols to all languages and save the result in list inside a pandas series
all_lp_data = TOLs.loc[:,'ISO_639'].apply(lp_to_list )

# transforms pandas series to dataframe
all_lp_data = all_lp_data.to_frame()

# Save columns with each row ISO 639
all_lp_data['ISO3'] = TOLs.loc[:,'ISO_639']

print(time.perf_counter() -start_time)


# Saving All_LPs calculated 1 GB file :/
all_lp_data.to_pickle("./data/all_lp_data")





#### Comparing both ICL ####

comparing_icls = dicl.merge(df_ICL, left_on= ["ISO3","ISO3_2"],right_on = ["ISO3","ISO3_2"])


fig = px.scatter(comparing_icls, x="cl_x", y="cl_y", trendline="ols",custom_data= comparing_icls )

fig.update_traces(hovertemplate='ISO3: %{customdata[0]} <br>ISO3 2: %{customdata[1]} <br>\
                                        <b>Paper data \
                                        <br> COL: %{customdata[2]}<br> CNL: %{customdata[3]}<br> LP: %{customdata[4]}<br>\
                                        CL: %{x} <br>\
                                        <b>Calculated data \
                                        <br> COL: %{customdata[6]}<br> CNL: %{customdata[7]}<br> LP: %{customdata[8]}<br>\
                                        CL: %{y}'
                                        )

fig.show()



comparing_icls[(comparing_icls["ISO3"] == "PCN" ) & (comparing_icls["ISO3_2"] == "NFK" ) ]


df_ICL[(df_ICL["ISO3"] == "PCN" ) & (df_ICL["ISO3_2"] == "NFK" ) ]


import statsmodels.api as sm

Y = comparing_icls['cl_x']
X = comparing_icls['cl_y']
np.corrcoef(X, Y)

model = sm.OLS(Y,X)
results = model.fit()


# Mean Absolute Percentage Difference bigger than .1
sum(abs((Y - X)/X) > .1 ) / len(Y)

