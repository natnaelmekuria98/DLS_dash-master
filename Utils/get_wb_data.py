# Get World bank data
# 	Gross capital formation (constant 2015 US$)(NE.GDI.TOTL.KD) - Saved as: Gross_Capital_Formation_const_2015usd
#   Gross capital formation (annual % growth)(NE.GDI.TOTL.KD.ZG) - Saved as: Gross_Capital_Formation_annual_growth
#   Gross fixed capital formation (constant 2015 US$)(NE.GDI.FTOT.KD) - Save as: Gross_Fixed_Capital_Formation_const_2015usd
#   Gross fixed capital formation (% of GDP)(NE.GDI.FTOT.ZS) - Saved as: Gross_Fixed_Capital_Formation_annual_growth
#	Households and NPISHs Final consumption expenditure (current US$)(NE.CON.PRVT.CD) - Saved as: Household_consumption

import pandas as pd
import wbdata

# Functions ##

## Saves World bank data to csv, given indicator code ###

def saves_wb_data(code,data_name):
    #pdb.set_trace()
    if ( data_name == None):
        data_name = wbdata.get_indicator(code)[0]['name']

    # Get the data
    data = wbdata.get_dataframe({code:data_name})

    # Index name to column ( data and country name )
    data.reset_index(inplace=True)

    # Get countries ISO codes 
    ## World bank data country names 
    wbd_country_names = data['country'].unique()

    # Creating a dataframe with world bank dict for Country_Name to ISO

    ## Empty list to append the data
    wbd_country_ids = []

    ## Iterates between names in the data
    for country_name in wbd_country_names:
        # Try get the name ISO, if not then says 'no data'
        try:
            country_id = wbdata.search_countries(country_name)[0]['id']
        except:
            country_id = 'no data'
        # append the data collected
        wbd_country_ids.append([country_name,country_id ])

    # Creates the dataframe with name to iso map
    df_wbd_country_ids = pd.DataFrame(wbd_country_ids, columns=['Country_Name', 'Country_ISO'])

    # Delete rows with 'no data'
    df_wbd_country_ids = df_wbd_country_ids[df_wbd_country_ids["Country_ISO"] != 'no data']

     # Merge the ISO dict with the household consumption data 
    data = data.merge(df_wbd_country_ids, left_on = "country",right_on = "Country_Name",how = "inner" ).drop(columns = ['Country_Name'])

    # drop duplicate column
    data.drop(columns = ['country'],inplace = True)

    #Transforms crazy package datatype to pd 
    data = pd.DataFrame(data.to_dict('records'))

    data.to_csv("./data/WorldBank/" + data_name +".csv", index = False)

    return( print('done') )

## Saves World bank data in bulk to csv, given list of indicators ####


def saves_wb_data_bulk(list_variables):

    # Get the data
    data = wbdata.get_dataframe(list_variables)

    # Index name to column ( data and country name )
    data.reset_index(inplace=True)

    # Get countries ISO codes 
    ## World bank data country names 
    wbd_country_names = data['country'].unique()

    # Creating a dataframe with world bank dict for Country_Name to ISO

    ## Empty list to append the data
    wbd_country_ids = []

    ## Iterates between names in the data
    for country_name in wbd_country_names:
        # Try get the name ISO, if not then says 'no data'
        try:
            country_id = wbdata.search_countries(country_name)[0]['id']
        except:
            country_id = 'no data'
        # append the data collected
        wbd_country_ids.append([country_name,country_id ])

    # Creates the dataframe with name to iso map
    df_wbd_country_ids = pd.DataFrame(wbd_country_ids, columns=['Country_Name', 'Country_ISO'])

    # Delete rows with 'no data'
    df_wbd_country_ids = df_wbd_country_ids[df_wbd_country_ids["Country_ISO"] != 'no data']

    # Merge the ISO dict with the household consumption data 
    data = data.merge(df_wbd_country_ids, left_on = "country",right_on = "Country_Name",how = "inner" ).drop(columns = ['Country_Name'])

    # drop duplicate column
    data.drop(columns = ['country'],inplace = True)

    #Transforms crazy package datatype to pd 
    data = pd.DataFrame(data.to_dict('records'))

    data.to_csv("./data/WorldBank/worldbankbulk.csv", index = False)

    return( print('done') )


####

# List of variables ####

list_variables = { "NE.GDI.TOTL.KD": "Gross_Capital_Formation_const_2015usd",
                   "NE.GDI.TOTL.KD.ZG": "Gross_Capital_Formation_annual_growth",
                   "NE.GDI.FTOT.KD": "Gross_Fixed_Capital_Formation_const_2015usd",
                   "NE.GDI.FTOT.ZS": "Gross_Fixed_Capital_Formation_annual_growth",
                   "NE.CON.PRVT.CD": "household_consu"
                   }
        
   

#wbdata.search_indicators("obstacle")

#wbdata.get_indicator("IC.FRM.CRM.CRIME2_C")

## Get the data
#households_consumption = wbdata.get_dataframe({"NE.CON.PRVT.CD":"household_consu"})

## Index name to column ( data and country name )
#households_consumption.reset_index(inplace=True)

## Get countries ISO codes 
### World bank data country names 
#wbd_country_names = households_consumption['country'].unique()

## Creating a dataframe with world bank dict for Country_Name to ISO

### Empty list to append the data
#wbd_country_ids = []

### Iterates between names in the data
#for country_name in wbd_country_names:
#    # Try get the name ISO, if not then says 'no data'
#    try:
#        country_id = wbdata.search_countries(country_name)[0]['id']
#    except:
#        country_id = 'no data'
#    # append the data collected
#    wbd_country_ids.append([country_name,country_id ])

## Creates the dataframe with name to iso map
#df_wbd_country_ids = pd.DataFrame(wbd_country_ids, columns=['Country_Name', 'Country_ISO'])

## Delete rows with 'no data'
#df_wbd_country_ids = df_wbd_country_ids[df_wbd_country_ids["Country_ISO"] != 'no data']

# # Merge the ISO dict with the household consumption data 
#households_consumption = households_consumption.merge(df_wbd_country_ids, left_on = "country",right_on = "Country_Name",how = "inner" ).drop(columns = ['Country_Name'])

## drop duplicate column
#households_consumption.drop(columns = ['Country_Name'],inplace = True)

# Transforms crazy package datatype to pd 
# households_consumption = pd.DataFrame(households_consumption.to_dict('records'))

#households_consumption.to_csv("./data/WorldBank/households_consumption.csv")
