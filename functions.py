# 
import plotly.graph_objects as go
import numpy as np
from load_data import *
import textwrap 
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc, html,dash_table
import itertools

# functions

# E --------------------------------------------------------------------------------------------------------------------------------------------------------------------

def expandgrid(*itrs):
   product = list(itertools.product(*itrs))
   return {'Var{}'.format(i+1):[x[i] for x in product] for i in range(len(itrs))}

# G --------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Get country data for GCF/GFCF table in language economics ------------------------------------------------------------------------------------------------------------

def get_data_for_country(country_name,selected_language_worldbank_data):
            
            # Filter the data for the selected country
            df_temp = selected_language_worldbank_data[selected_language_worldbank_data['Country_Name'] == country_name ]

            number_of_nans = df_temp.isna().sum()["Gross_Capital_Formation_const_2015usd"]

            # Check if there is any observation
            if (number_of_nans == len(df_temp) ):
                return html.Tr([
                            html.Th(country_name),
                            html.Th("-"),
                            html.Th("-"),
                            html.Th("-"), # Return value in Millions
                            html.Th("-")
                            ],style = {"border-width": "0px 0px .9px 0px" , "border-style": "solid solid solid solid"})

            # Get most recent year of observation
            last_year = max(df_temp[['date','Gross_Capital_Formation_const_2015usd']].dropna()['date'])

            # Make plot 
            fig = px.line(df_temp, x="date", y="Gross_Capital_Formation_const_2015usd")

            # Plot layout options 
            fig.update_layout(xaxis=dict(showline=False,showgrid=False,zeroline=False,showticklabels=False,title = dict( text =''),ticks=""),
                              yaxis=dict(showgrid=False,zeroline=False,showline=False,showticklabels=False,title = dict( text =''),ticks=""),
                              autosize=False,margin=dict(autoexpand=False,l=0,r=0,t=0,b=0),showlegend=False,
                              paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',width=100,height= 50
                              )            

            # Static image
            config={'staticPlot': True}


            # Get most recent value
            last_value = df_temp[df_temp['date'] == last_year ] 

            # Check if growth is nan 
            if ( np.isnan(last_value.Gross_Capital_Formation_annual_growth.values[0]) ):
                return html.Tr([
                            html.Th(country_name),
                            html.Th(last_year),
                            html.Th("-"),
                            html.Th("{:,.2f} M".format(last_value.Gross_Capital_Formation_const_2015usd.values[0]/1000000)), # Return value in Millions
                            html.Th(dcc.Graph(figure=fig,config=config))
                            ],style = {"border-width": "0px 0px .9px 0px" , "border-style": "solid solid solid solid"})

            
            # Make html version of indicator 
            growth = float(last_value.Gross_Capital_Formation_annual_growth/100 )

            # Check variation direction and format the number accordinly
            if (last_value.Gross_Capital_Formation_annual_growth.values[0] > 0):
                # Green upward arrow for growth
                growth_indicator = html.P(["\u2BC5 ", "{:.2%}".format(growth)],style = {"color":"#00c88a", "margin":0})                     
            elif (last_value.Gross_Capital_Formation_annual_growth.values[0] < 0):
                # Red upward arrow for decline
                growth_indicator = html.P(["\u2BC6 ", "{:.2%}".format(growth)],style = {"color":"#ff415f", "margin":0})
            else:
                # Square if zero
                growth_indicator = html.P(["\u2BC0 ", "{:.2%}".format(growth)],style = { "margin":0})
                
            
                        
            return html.Tr([
                            html.Th(country_name),
                            html.Th(last_year),
                            html.Th(growth_indicator),
                            html.Th("{:,.2f} M".format(last_value.Gross_Capital_Formation_const_2015usd.values[0]/1000000)), # Return value in Millions
                            html.Th(dcc.Graph(figure=fig,config=config))
                            ],style = {"border-width": "0px 0px .9px 0px" , "border-style": "solid solid solid solid"})
       
# Get GME Coefficient by sector or industry ----------------------------------------------------------------------------------------------------------------------------

def get_gme_coefficients(by_sector_or_industry,id):

    variables = ['cl','norm_log_t_index','iso_hhi.y']

    if (by_sector_or_industry == 'sector'):

        temp = gme_by_sector[(gme_by_sector['model'] == 'TSFE_all') |  (gme_by_sector['model'] == 'fast_ppmlModel_FEVD_all') ]

        temp = temp[ (temp['sector_industry'] == id) & (temp['rowname'].isin(variables)) & (temp['log_t_index'] == True) ] 
        
        return temp

    else:

        temp = gme_by_industry[(gme_by_industry['model'] == 'TSFE_all') |  (gme_by_industry['model'] == 'fast_ppmlModel_FEVD_all') ]        

        temp = temp[ (temp['sector_industry'] == id) & (temp['rowname'].isin(variables)) & (temp['log_t_index'] == True) ] 
        
        return temp        


# Group sunburst subgroups for language consumptions by country --------------------------------------------------------------------------------------------------------
# continent_or_regional = { "Area" , "Region_Name" }
## TODO: If more grouping of minority is need, tweek this function

def group_lang_sunburst(df_hh_consumption,continent_or_regional="Area"):
    
    total_proportional_consumption_by_continent = df_hh_consumption.groupby(continent_or_regional)["household_consu_L1_proportional"].sum() / df_hh_consumption["household_consu_L1_proportional"].sum() 

    # Pandas series to dataframe 
    total_proportional_consumption_by_continent = total_proportional_consumption_by_continent.to_frame()
    
    # rowname to column 
    total_proportional_consumption_by_continent.reset_index(inplace=True)


    # Ordering data frame to get cumulative percentage 
    continent_less_than_five_percent = total_proportional_consumption_by_continent.sort_values('household_consu_L1_proportional')
    
    # rowname to column 
    continent_less_than_five_percent.reset_index(drop = True,inplace = True)

    
    # Cumulative sum
    ## continent
    continent_less_than_five_percent['cumsum'] = continent_less_than_five_percent['household_consu_L1_proportional'].cumsum()

    # Continent to be grouped index
    continent_to_be_group = continent_less_than_five_percent[continent_less_than_five_percent['cumsum'] < .05 ].index.to_list()

    #
    continent_to_be_group.append(max(continent_to_be_group)+1)

    # Lists continents with less than 2.5% of total proportional consumption 

    grouped_continets = continent_less_than_five_percent.loc[continent_to_be_group][continent_or_regional]
    # Group minority continents 

    df_hh_consumption.loc[df_hh_consumption['Area'].isin(grouped_continets),'Area'] = ", ".join(grouped_continets.to_list())

    return df_hh_consumption


# Row iterator parser used in the iterator object called to make the HHI subtable rows  --------------------------------------------------------------------------------  

def get_sub_row_given_Scope_and_Users(row2_temp):
                      
    return html.Tr([
                    html.Td(row2_temp[1]["Country_Name"]),
                    html.Td("{:,}".format(row2_temp[1]["All_Users"])),
                    html.Td("{:,}".format(row2_temp[1]["L1_Users"])),
                    html.Td("{:,}".format(row2_temp[1]["L2_Users"]))
                    ],style = {"border-width": "0px 0px .9px 0px" , "border-style": "solid solid solid solid"})


## Gets bbox for geoJSON feature collection 

# OBS.: Not working, the features sometimes has more than "coordinates"  ( polygon) 

#def get_bbox_from_features(poly):

#i = 0 
#for f in poly:
#    if len( f["geometry"]["coordinates"][0]) == 1:
#        c = f["geometry"]["coordinates"][0][0]
#    else:
#        c = f["geometry"]["coordinates"][0]

#    c1 = [x[0] for x in c]
#    c2 = [x[1] for x in c]
#    # appends previews bbox calculated
#    if (i != 0):
#        [ c1.append(bbox[j][0]) for j in range(4) ]
#        [ c2.append(bbox[j][1]) for j in range(4) ]

#    bbox = [[min(c1),min(c2)],[min(c1),max(c2)],[max(c1),max(c2)],[max(c1),min(c2)],[min(c1),min(c2)]]
#    #f["geometry"]["coordinates"] = [bbox]
#    i += 1

#        return(bbox)    

# I  -------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Insert break line ----------------------------------------------------------------------------------------------------------------------------------------------------

#def insert_dash(string, index=100):
    
#    return textwrap.fill(string, index).replace("\n","<br>")

#    #if ( len(string) > 12):
#    #    return string[:index] + '<br>' + string[index:]
#    #else:
#    #    return string

# Interest rate bar plot -----------------------------------------------------------------------------------------------------------------------------------------------

def interest_rate_bar_plot(melted_selected_language_interest_rate_IMF,date = 2020):
    
    test = melted_selected_language_interest_rate_IMF[melted_selected_language_interest_rate_IMF['date'] == date ]

    # X labels 
    x_labels = test.label.unique()

    # Empty graph to set X order 
    fig = go.Figure(data=[
        go.Bar(name='', x =  x_labels,
               y = len(test.label.unique())*[0],
              showlegend=False)
    ])

    # Adding all bars
    for country in test.Country_Name.unique():

        fig.add_bar(name=country, x = test[test['Country_Name']==country].label,
                   y = test[test['Country_Name']==country].value/100,
                   #hovertext = test[test['Country_Name']==country].value/100 
                   hovertemplate="<br>".join(["Country:"+country,
                                              #"Rate: %{y:.2%}" ,
                                              "Rate: %{y:.2%}" ,
                                              ])
                   )

    fig.update_layout(barmode='group')
    #fig.update_traces(width=.02,
    #                  bargap=.2)

    test0 = test.groupby('label').mean()

    # Add each mean
    i = 0
    for code in test.label.unique():
        # Add horizontal line for each rate mean
        fig.add_shape(type="line",
                        name = code,
                        x0=-0.5+i, y0=test0['value'][code]/100, x1=.5+i, y1=test0['value'][code]/100,
                        line=dict(color="black",
                                  width=3,
                                  dash="dashdot")
                       )
        # Add rate mean text to the plot
        fig.add_trace(go.Scatter(showlegend=False,
                                 x=[code],
                                 y=[test0['value'][code]/100+.003],
                                 text="{:.2%}".format(test0['value'][code]/100),
                                 mode="text",
                                ))

        i += 1

    return fig


# H  -------------------------------------------------------------------------------------------------------------------------------------------------------------------

## HHI concentration index ---------------------------------------------------------------------------------------------------------------------------------------------

def HHI(iso,users="L1_Users"):
    
    # LIC filtered by iso and na droped
    lic_temp = LICs.loc[LICs['ISO_639'] == iso  ].dropna(subset = [users])

    # Gets percentual population of the selected language in regard the total 
    lic_temp['per_of_total'] = (lic_temp[users] /  lic_temp[users].sum())**2

    # HHI 

    df_hhi = pd.DataFrame([ [lic_temp[users].sum(), lic_temp['per_of_total'].sum(), lic_temp['per_of_total'].count()]], columns = [users, "ISO_HHI","count"])

    df_hhi.index = ["All countries"]

    return df_hhi
    #return  lic_temp['per_of_total'].sum()

## HHI by cladistic distance -------------------------------------------------------------------------------------------------------------------------------------------

def HHI_by_LP(iso,deepness,users = "L1_Users"):

    # get cladistic distances
    df_lp = language_proximity_all(iso,users)

    # LIC filtered by iso and na droped 
    # Old is >= 
    lic_temp = df_lp.loc[df_lp['distance'] >= deepness  ].dropna(subset = [users])
    
    # get family branch 

    family_len = [ len(string.split(',')) for string in lic_temp.parent_family_branch.unique() ]

    parent_family = lic_temp.parent_family_branch.unique()[np.argmin(family_len)]

    # Set parent family to all languages if no parent is return
    if (parent_family == ''):
        parent_family = "All Languages"
        
    # Gets percentual population of the selected language in regard the total 
    lic_temp['per_of_total'] = (lic_temp[users] /  lic_temp[users].sum())**2

    # HHI 

    #return  lic_temp['per_of_total'].sum()

    return pd.DataFrame( data = {  "HHI" : lic_temp['per_of_total'].sum() , "Family Group" : parent_family }, index=[0])


## HHI by geo scope  ---------------------------------------------------------------------------------------------------------------------------------------------------

## HHI concentration index by geographic denomination 

## IDEA : Make clickable map ( choose the custom geo location to calculate)

# geo = 'Region_Name' or 'Area' or 'global'

def HHI_geo(iso,users="L1_Users", geo = 'Region_Name' ):
   
    if (geo == 'global'):
        
        lic_temp = HHI(iso,users)

        lic_temp['Scope'] = lic_temp.index

        return lic_temp
    
    else: 

        lic_temp = LICs.loc[ (LICs['ISO_639'] == iso)  ].dropna(subset = [users])[['ISO_639',geo,users]]

        # Sum by group 
        lic_temp['Total_users'] = lic_temp[users].groupby(lic_temp[geo]).transform('sum')
    
        # Get the squared percentual for the HHI
        lic_temp['sq_per_of_total'] = (lic_temp[users]/lic_temp['Total_users'])**2

        # LIC filtered by iso and na droped
        lic_temp = pd.concat( [lic_temp.groupby([geo])[[users,'sq_per_of_total']].sum().rename(columns={'sq_per_of_total': 'ISO_HHI'}),
                                  lic_temp.groupby([geo])[['sq_per_of_total']].count().rename(columns={'sq_per_of_total': 'count'}) ], axis=1)
       

        lic_temp['Scope'] = lic_temp.index
        # HHI 

       # return  lic_temp.rename_axis("region").reset_index()
        return  lic_temp


## HHI by country ------------------------------------------------------------------------------------------------------------------------------------------------------

def HHI_country(iso,users="L1_Users", geo = 'Country_Name' ):
    
    if ( iso == 'nan'):
        iso == 'na'

    lic_temp = LICs.loc[ (LICs['Country_Code'] == iso)  ].dropna(subset = [users])[['ISO_639',geo,users]]

    # Sum by group 
    lic_temp['Total_users'] = lic_temp[users].groupby(lic_temp[geo]).transform('sum')
    
    # Get the squared percentual for the HHI
    lic_temp['sq_per_of_total'] = (lic_temp[users]/lic_temp['Total_users'])**2

    # LIC filtered by iso and na droped
    lic_temp = pd.concat( [lic_temp.groupby([geo])[[users,'sq_per_of_total']].sum().rename(columns={'sq_per_of_total': 'ISO_HHI'}),
                              lic_temp.groupby([geo])[['sq_per_of_total']].count().rename(columns={'sq_per_of_total': 'count'}) ], axis=1)
       

    # HHI 

    return  lic_temp


## human_format --------------------------------------------------------------------------------------------------------------------------------------------------------
# Transforms exp numbers to letters format 1 M , 1 k  ... https://stackoverflow.com/questions/579310/formatting-long-numbers-as-strings-in-python

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])


# L  -------------------------------------------------------------------------------------------------------------------------------------------------------------------


## get language proximity pairwise, one language versus anoter ( distance in the tree ) --------------------------------------------------------------------------------

def language_proximity(iso_1,iso_2) :

    # 1) Merge LICs with TOLs to get language classification in LICs data

    # Select columns that are not already in LICs
    
    cols_to_use = TOLs.columns.difference(LICs.columns)
      
    # Append ISO 
    cols_to_use = cols_to_use.append(pd.Index(["ISO_639"]) )
    
    # Join LICs table with TOLs table to get Classification ( Tree family)
    LICs_wclassification = pd.merge(LICs, TOLs[cols_to_use],
                          on = 'ISO_639', how="inner")[["ISO_639","Family","Country_Code",
                                                        "Language_Name","All_Users","L1_Users",
                                                        "L2_Users","Classification"]]

    # 2) Get classification of each language and split the word by ","

    iso_1_classification = LICs_wclassification.loc[LICs_wclassification['ISO_639']==iso_1]["Classification"].iloc[0]

    iso_1_classification = iso_1_classification.split(',')

    iso_2_classification = LICs_wclassification.loc[LICs_wclassification['ISO_639']==iso_2]["Classification"].iloc[0]

    iso_2_classification = iso_2_classification.split(',')

    ## get which is the min len

    isos_len = [len(iso_1_classification),len(iso_2_classification)]

    which_is_smaller = np.argmin(isos_len)

    ## Create a list for the comparison... dont need, just to be cleaner to read

    comparing_classification = [iso_1_classification[:isos_len[which_is_smaller]] , 
                                iso_2_classification[:isos_len[which_is_smaller]]]

    # Element wise comparison result
    comparing_classification_result = [ comparing_classification[0][i] == comparing_classification[1][i] for i in range(isos_len[which_is_smaller]) ]

    # index Distance of the language 
    # Old distance
    #distance_index = 1 - sum(comparing_classification_result)/isos_len[which_is_smaller]
    # Gurevich et al (2021) ( inspired from Laitin (2000) and Fearon (2003) )
    distance_index = sum(comparing_classification_result)/ np.mean(isos_len)


    return distance_index


## get language proximity, one language vs all classifications ( distance in the tree ) --------------------------------------------------------------------------------

def language_proximity_all(iso_1,users) :

    # 1) Merge LICs with TOLs to get language classification in LICs data

    # Select columns that are not already in LICs
    
    cols_to_use = TOLs.columns.difference(LICs.columns)
      
    # Append ISO 
    cols_to_use = cols_to_use.append(pd.Index(["ISO_639"]) )
    
    # Join LICs table with TOLs table to get Classification ( Tree family)
    LICs_wclassification = pd.merge(LICs.dropna(subset = [users]), TOLs[cols_to_use],
                          on = 'ISO_639', how="inner")[["ISO_639","Family","Country_Code",
                                                        "Language_Name","All_Users","L1_Users",
                                                        "L2_Users","Classification"]]

    # 2) Get classification of each language and split the word by ","

    iso_1_classification = LICs_wclassification.loc[LICs_wclassification['ISO_639']==iso_1]["Classification"].unique()[0]

    iso_1_classification = iso_1_classification.split(',')

    iso_2_classification = LICs_wclassification["Classification"].unique()

    iso_2_classification = [ class_name.split(',') for class_name in iso_2_classification ]

    ## get which is the min len

    isos_min_len =  [  min([len(iso_1_classification),len(iso_2_class)])  for iso_2_class in iso_2_classification  ]

    ## Get len mean
    isos_mean_len =  [  np.mean([len(iso_1_classification),len(iso_2_class)])  for iso_2_class in iso_2_classification  ]

    ## Create a list for the comparison... dont need, just to be cleaner to read

    comparing_classification = [ [iso_1_classification[:isos_min_len[i]] , 
                                  iso_2_classification[i][:isos_min_len[i]]] for i  in range(len(iso_2_classification)) ]

    # Element wise comparison result

    comparing_classification_result = [ [ iso_classes[0][i] == iso_classes[1][i] for i in range(len(iso_classes[0])) ]  for iso_classes in comparing_classification ]

    # get family branch

    family_branch = [ [ iso_classes[0][i] if (iso_classes[0][i] == iso_classes[1][i]) else None  for i in range(len(iso_classes[0])) ]  for iso_classes in comparing_classification ]


    family_branch_strings =  [ ",".join(filter(None,names)) for names in family_branch ]
    
    # index Distance of the language
    # Old distance 
    #distance_index = [ 1 - sum(comparing_classification_result[i])/isos_min_len[i] for i in range(len(comparing_classification_result)) ] 
    # Gurevich et al (2021) ( inspired from Laitin (2000) and Fearon (2003) )
    distance_index = [ sum(comparing_classification_result[i])/np.mean(isos_mean_len[i]) for i in range(len(comparing_classification_result)) ] 

    # Save distance dataframe 
    df_distance = pd.DataFrame( data = {  "Classification" : LICs_wclassification["Classification"].unique() , "distance" : distance_index, "parent_family_branch" : family_branch_strings  })

    # Get merge with LICs_wclassification to get ISOs
    LICs_wclassification = pd.merge(LICs_wclassification, df_distance,
                          on = 'Classification', how="inner")[["ISO_639","Family","Country_Code",
                                                        "Language_Name","All_Users","L1_Users",
                                                        "L2_Users","Classification","parent_family_branch","distance"]]

    return  LICs_wclassification


## get language proximity, one language vs all classifications ( distance in the tree ) --------------------------------------------------------------------------------

def language_proximity_all_tols(iso_1) :

    # 1) Merge LICs with TOLs to get language classification in LICs data

    # Select columns that are not already in LICs
    TOLs_wclassification = TOLs[["ISO_639","Family","Country_Code","Language_Name","All_Users","L1_Users","Classification"]]

    # 2) Get classification of each language and split the word by ","

    iso_1_classification = TOLs_wclassification.loc[TOLs_wclassification['ISO_639']==iso_1]["Classification"].unique()[0]

    iso_1_classification = iso_1_classification.split(',')

    iso_2_classification = TOLs_wclassification["Classification"].unique()

    iso_2_classification = [ class_name.split(',') for class_name in iso_2_classification ]

    ## get which is the min len

    isos_min_len =  [  min([len(iso_1_classification),len(iso_2_class)])  for iso_2_class in iso_2_classification  ]

    ## Get len mean
    isos_mean_len =  [  np.mean([len(iso_1_classification),len(iso_2_class)])  for iso_2_class in iso_2_classification  ]

    ## Create a list for the comparison... dont need, just to be cleaner to read

    comparing_classification = [ [iso_1_classification[:isos_min_len[i]] , 
                                  iso_2_classification[i][:isos_min_len[i]]] for i  in range(len(iso_2_classification)) ]

    # Element wise comparison result

    comparing_classification_result = [ [ iso_classes[0][i] == iso_classes[1][i] for i in range(len(iso_classes[0])) ]  for iso_classes in comparing_classification ]

    # get family branch

    family_branch = [ [ iso_classes[0][i] if (iso_classes[0][i] == iso_classes[1][i]) else None  for i in range(len(iso_classes[0])) ]  for iso_classes in comparing_classification ]


    family_branch_strings =  [ ",".join(filter(None,names)) for names in family_branch ]
    
    # index Distance of the language
    # Old distance 
    #distance_index = [ 1 - sum(comparing_classification_result[i])/isos_min_len[i] for i in range(len(comparing_classification_result)) ] 
    # Gurevich et al (2021) ( inspired from Laitin (2000) and Fearon (2003) )
    distance_index = [ sum(comparing_classification_result[i])/np.mean(isos_mean_len[i]) for i in range(len(comparing_classification_result)) ] 

    # Save distance dataframe 
    df_distance = pd.DataFrame( data = {  "Classification" : TOLs_wclassification["Classification"].unique() , "distance" : distance_index, "parent_family_branch" : family_branch_strings  })

    # Get merge with TOLs_wclassification to get ISOs
    TOLs_wclassification = pd.merge(TOLs_wclassification, df_distance,
                          on = 'Classification', how="inner")[["ISO_639","Family","Country_Code",
                                                                "Language_Name","All_Users","L1_Users",
                                                                "Classification","parent_family_branch","distance"]]

    return  TOLs_wclassification


# M  -------------------------------------------------------------------------------------------------------------------------------------------------------------------


## Make popover dls classification data --------------------------------------------------------------------------------------------------------------------------------

def make_popover_dls_class(name):

    description = dls_class_descr[dls_class_descr['class']==name]["description"].values[0]

    examples = dls_class_descr[dls_class_descr['class']==name]["examples"].values[0]

    temp = [f"* {i}" for i in examples.split(";") ]

    temp = "\n".join(temp)

    markdown_string = f"\n## {name}\n"+f"&nbsp {description} ;\n"+ f"{temp}"

    return [dbc.Popover( dcc.Markdown(markdown_string),
                       target=f"{name}_info",body=True,trigger="hover",placement='top') ]


## Make Span for dls classification data --- NOT USING -----------------------------------------------------------------------------------------------------------------

#def make_span_dls_class(name):
    
#    return [html.Span(f"{name}, ",id = f"{name}_info",  style={"textDecoration": "underline", "cursor": "pointer", "color":"#0a58ca"} )]


## Make table of dls thresholds ----------------------------------------------------------------------------------------------------------------------------------------

def make_table_dls_thresholds(name):

    data_temp = dls_class_threshold.loc[dls_class_threshold['support_level'] == name]

    data_temp = data_temp.rename(columns = {'class':'classification','lower_limit':'Lower limit','upper_limit':'Upper limit'})

    data_temp['classification'] = data_temp.support_level.map(str) + " " + data_temp.classification.map(str)

    data_temp.drop(['support_level'],axis=1,inplace = True)

    classification_count_thresholds = dash_table.DataTable(data_temp.to_dict('records'), [{"name": i, "id": i} for i in data_temp.columns],
                                                                style_as_list_view=True,
                                                                style_cell={'padding': '5px', 'font-family':'sans-serif'},
                                                                style_header={'backgroundColor': 'white','fontWeight': 'bold'},
                                                                style_data={'whiteSpace': 'normal','height': 'auto','textAlign': 'center'})

    

    return[ dbc.Tab(classification_count_thresholds,label=f"{name}",
                    tab_id=f"{name}_dls_modal_threshold_table",
                    tab_style={'border-color': '#dee2e6','border-radius': '0.35rem','padding':'1px'}) ]


## Make Item Response Function Plot ------------------------------------------------------------------------------------------------------------------------------------

def make_irf_plot(category):

    # Get the data 
    dls_item_adjusted_score_curve = pd.read_csv("./data/dls/item_adjusted_score_curve.csv", encoding = 'ISO8859-1')

    ## Getting the data 
    #fig_irf = px.scatter(dls_item_adjusted_score_curve, x = 'adjusted_total',y ='adjusted_score', 
    #                     color = 'cluster',facet_col = 'ItemStep',facet_row = 'level',opacity = .2,custom_data= ["ISO_639","cluster","level","ItemStep"],
    #                     category_orders = {"level": ["encoding", "content", "localized", "surface","meaning","speech","assistant"],
    #                                        "ItemStep": [1,2,3,4] },
    #                     #labels={
    #                     #        "adjusted_score": '$p( x_{i} = 1 )$'
    #                     #        }
    #                     )

    fig_irf = px.scatter(dls_item_adjusted_score_curve[dls_item_adjusted_score_curve['level']==category], x = 'adjusted_total',y ='adjusted_score', 
                         color = 'cluster',facet_col = 'ItemStep',facet_col_wrap=2,opacity = .2,#custom_data= ["ISO_639","cluster","level","ItemStep"],
                         category_orders = {"ItemStep": [1,2,3,4] }

                         #labels={
                         #        "adjusted_score": '$p( x_{i} = 1 )$'
                         #        }
                         )


    # Remove Labels from facet columns 
    fig_irf.for_each_annotation(lambda a: a.update(text= category + " " + a.text.split("=")[1]))
    #fig_irf.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))

    # y axis tick angle 
    #for annotation in fig_irf['layout']['annotations']: 
    #    if (annotation['textangle'] == 90):
    #        annotation['textangle'] = 60
    
    # Remove labels 
    fig_irf.update_yaxes(title='')
    fig_irf.update_xaxes(title='')

    # Add "label" to y axis
    fig_irf.add_annotation(x=-0.1,y=0.5,showarrow=False,
                            #text='$p( x_{i} = 1 )$',
                            text='P(x = 1)',
                            textangle=-90,
                            xref="paper", yref="paper")
    # Add "label" to x axis
    fig_irf.add_annotation(x=0.5,y=-.1,showarrow=False,
                   text='Total Adjusted Score', textangle=0,
                    xref="paper", yref="paper")


    # Add label to the middle 
    #fig_irf.update_layout(yaxis13=dict(title='$p( x_{i} = 1 )$'))
    #fig_irf.update_layout(yaxis13=dict(title='P(x = 1)'))

    fig_line = px.line(dls_item_adjusted_score_curve[dls_item_adjusted_score_curve['level']==category].sort_values(by = ["adjusted_total"]),
                      x = 'adjusted_total',y ='fitted_y',facet_col = 'ItemStep',facet_col_wrap=2,
                                   category_orders = {"ItemStep": [1,2,3,4]})

    fig_line.update_traces(line_color='#000000')

    for i in range(len(fig_line.data)):
        
        fig_irf.add_trace( fig_line.data[i] )
    
    # Padding formatting
    fig_irf.update_layout(margin=dict(l=20,
                                       r=25,
                                       b=30,
                                       t=30,
                                       pad=4
                                       )
                                )
    #return fig_irf.show()
    return [ dcc.Graph(id = 'irf_scatter_info',figure = fig_irf) ]


## Makes subrow for HHI subtable --------------------------------------------------------------------------------------------------------------------------------------- 

def make_row_with_subtable_HHI(row_temp,iso_dd,scope_dd,users_dd):
        
        # 1) Check whether the scope is set to global to get All the langugages or separate by the scope ( Continents or Regions )
        if (scope_dd == "global"):

            df_lics = LICs.loc[(LICs['Language_Name'] == iso_dd) ].dropna(subset = [users_dd])[['Country_Name','All_Users','L1_Users','L2_Users']]
        else:

            df_lics = LICs.loc[(LICs['Language_Name'] == iso_dd) & (LICs[scope_dd] == row_temp["Scope"]) ].dropna(subset = [users_dd])[['Country_Name','All_Users','L1_Users','L2_Users']]

        # 2) Creates a row with the subtable 
        row_with_subtable = [
                             # Make the root row of the table ( subtable is a child of this )
                             html.Tr([
                                     html.Td([html.Button(["+"],className= 'btn open',
                                                          **{"data-text-swap":"-","data-text-original":"+"})]),
                                     html.Td([row_temp['Scope']]),
                                     html.Td(["{:,}".format(row_temp[users_dd]) ]),
                                     html.Td(["{:.2f}".format(row_temp['ISO_HHI'])]),
                                     html.Td([row_temp['count']])
                                     ]),
                             # Create the a row that stays hidden and contais the subtable.
                             # NOTE: It is unhide by a javascript called in subtable_collapse.js
                             html.Tr([
                                     html.Td(),
                                     html.Td([ html.Div([
                                                         html.Table([
                                                                     # Header ------------------------------------------------------------------------------------------
                                                                     html.Thead([
                                                                                 html.Tr([   
                                                                                         html.Th("Country",className="order alphaNumericOrdering",**{"data-sortable":"true"}),
                                                                                         html.Th("All Users",className="order",**{"data-sortable":"true", "data-field": "Scope","data-sorter": "numericOnly"}),
                                                                                         html.Th("L1 Users",className="order",**{"data-sortable":"true", "data-field": users_dd, "data-sorter": "numericOnly"}),
                                                                                         html.Th("L2 Users",className="order",**{"data-sortable":"true", "data-field": "ISO_HHI", "data-sorter": "sortVariationWithTriangleOnly"}),
                                                                                         ],style = {"border-width": "2px 0px 1px 0px" , "border-style": "solid solid solid solid"})
                                                                                 ]),
                                                                     # body --------------------------------------------------------------------------------------------
                                                                     html.Tbody(
                                                                                 [get_sub_row_given_Scope_and_Users(row2) for row2 in df_lics.iterrows()],
                                                                                 className="subTableTbody"
                                                                                 )
                                                                     
                                                                     ],className= "subtableHHI",style={"width": "100%"})
                                                         ],className="scrollable", style = {"max-height": "400px", "width": "100%", "overflow": "auto"})
                                               ] ,colSpan = 4)
                                     ], id="hideLine", style = {"display": "none"})]

        return row_with_subtable


## Calculates market expansion metric ----------------------------------------------------------------------------------------------------------------------------------
# NOTES: Uses t-index, HHI and ICL in a perfect substitute type utility function to define the best choice.
# IDEA!: Where the biggest variation of imports happens ( low or high HHI countries, low or high DICL countries, low or high T-index Countries)
# IDEA: expand language filtering by LP 
# IDEA: t-index calculus where is not internet users that determine the cut in the wealth distribuition, but make it customable
# IDEA: add entropy ( -sum{p(x)*log(p(x)) ) and Simpson Index ( sum{p(x)^a} ^ (1/(1-a)) where a = 2 for Simpson index) https://stats.stackexchange.com/questions/460564/how-is-the-herfindahl-hirschman-index-different-from-entropy
# IDEA: Less entropic/concentrated language are better for trade?
# IDEA: HHI for country, which is better a country in high or low HHI

def market_expansion_metric(country_iso3,iso_639,year= 2018):

    # 0) Setup 

    ## gets iso 2 and contry name from iso3

    country_iso2 = pycountry.countries.get(alpha_3 = country_iso3).alpha_2
    country = pycountry.countries.get(alpha_3 = country_iso3).name


    # Save t-index of countries with english speakers
    t_index_selection = t_index_by_language_with_countries[ (t_index_by_language_with_countries['ISO_639']== iso_639) & (t_index_by_language_with_countries["year"] == year) &
                                                        (t_index_by_language_with_countries['iso2c']!= country_iso2)].copy()


    # normalize the t-index
    #t_index_selection.loc[:,'norm_t_index'] =  (t_index_selection.loc[:,'t_index'] - min(t_index_selection.loc[:,'t_index'] )) / (max(t_index_selection.loc[:,'t_index'] ) - min(t_index_selection.loc[:,'t_index'] ))

    # IDEA: add entropy ( -sum{p(x)*log(p(x)) ) and Simpson Index ( sum{p(x)^a} ^ (1/(1-a)) where a = 2 for Simpson index) https://stats.stackexchange.com/questions/460564/how-is-the-herfindahl-hirschman-index-different-from-entropy
    # IDEA: Less entropic/concentrated language are better for trade?
    # IDEA: HHI for country, which is better a country in high or low HHI

    # Save HHI by country

    t_index_selection.loc[:,'HHI_by_country'] = [ HHI_country(selected_country)['ISO_HHI'].to_list()[0] for selected_country in t_index_selection['iso2c'] ]


    # Save iso3 of each country

    t_index_selection.loc[:,'iso3'] = [ gets_iso3_from_iso2(selected_country) for selected_country in t_index_selection['iso2c'] ]

    # DICL ----------------------------------

    def icl(iso,iso2):
        dicl.loc[(dicl["ISO3"]==iso) & (dicl['ISO3_2']==iso2) ]

        return dicl.loc[(dicl["ISO3"]==iso) & (dicl["ISO3_2"]==iso2) ][['col','cnl','lp','cl']].mean(axis=1).values[0]

    t_index_selection.loc[:,'ICL'] = [ icl(country_iso3,selected_country) for selected_country in t_index_selection['iso3'] ]

    # Utility function
    t_index_selection.loc[:,'U'] = t_index_selection[['norm_log_t_index','HHI_by_country','ICL']].apply(lambda x: (x[0]+x[1]+x[2])/3 , axis=1)


    return t_index_selection


# Market Expansion Metric By cladistic distance ------------------------------------------------------------------------------------------------------------------------

def market_expansion_metric_by_LP(country_iso3,iso_639,deepness,year= 2018):


    # 1) gets iso 2 and contry name from iso3 --------------------------------------------------------------------------------------------------------------------------

    country_iso2 = pycountry.countries.get(alpha_3 = country_iso3).alpha_2
    country = pycountry.countries.get(alpha_3 = country_iso3).name

     
    # 1) get language by LP deepness -----------------------------------------------------------------------------------------------------------------------------------

    users= "L1_Users"

    # get cladistic distances
    df_lp = language_proximity_all(iso_639,users)

    # LIC filtered by iso and na droped 
    # Old is >= 
    lic_temp = df_lp.loc[df_lp['distance'] >= deepness  ].dropna(subset = [users])
    
    # get family branch 

    family_len = [ len(string.split(',')) for string in lic_temp.parent_family_branch.unique() ]

    parent_family = lic_temp.parent_family_branch.unique()[np.argmin(family_len)]

    # Set parent family to all languages if no parent is return
    if (parent_family == ''):
        parent_family = "All Languages"

    # List of filtered languages by deepness

    list_lang_deep = lic_temp["ISO_639"].unique()

    # 2) Save t-index of countries with english speakers ---------------------------------------------------------------------------------------------------------------

    t_index_selection = t_index_by_language_with_countries[ (t_index_by_language_with_countries['ISO_639'].isin(list_lang_deep)) & (t_index_by_language_with_countries["year"] == year) &
                                                        (t_index_by_language_with_countries['iso2c']!= country_iso2)].copy()


    # normalize the t-index
    #t_index_selection.loc[:,'norm_t_index'] =  (t_index_selection.loc[:,'t_index'] - min(t_index_selection.loc[:,'t_index'] )) / (max(t_index_selection.loc[:,'t_index'] ) - min(t_index_selection.loc[:,'t_index'] ))

    # IDEA: add entropy ( -sum{p(x)*log(p(x)) ) and Simpson Index ( sum{p(x)^a} ^ (1/(1-a)) where a = 2 for Simpson index) https://stats.stackexchange.com/questions/460564/how-is-the-herfindahl-hirschman-index-different-from-entropy
    # IDEA: Less entropic/concentrated language are better for trade?
    # IDEA: HHI for country, which is better a country in high or low HHI

    # Save HHI by country

    t_index_selection.loc[:,'HHI_by_country'] = [ HHI_country(selected_country)['ISO_HHI'].to_list()[0] for selected_country in t_index_selection['iso2c'] ]


    # Save iso3 of each country

    t_index_selection.loc[:,'iso3'] = [ gets_iso3_from_iso2(selected_country) for selected_country in t_index_selection['iso2c'] ]

    # DICL ----------------------------------

    def icl(iso,iso2):
        dicl.loc[(dicl["ISO3"]==iso) & (dicl['ISO3_2']==iso2) ]

        return dicl.loc[(dicl["ISO3"]==iso) & (dicl["ISO3_2"]==iso2) ][['col','cnl','lp','cl']].mean(axis=1).values[0]

    t_index_selection.loc[:,'ICL'] = [ icl(country_iso3,selected_country) for selected_country in t_index_selection['iso3'] ]

    # Separating the GME model coefficients for the index calculation
    cl_coef, t_coef, hhi_coef = get_gme_coefficients("sector","all")['Estimate'].values.tolist()

    # Calculates the index using the GME coefficient as weights.
    # NOTE: To make a easy normalization. the HHI is inverted so that the HHI coefficient is positive. Now I can get the ponderate mean
    t_index_selection['U'] = (t_coef*t_index_selection.loc[:,'norm_log_t_index'] - hhi_coef*(1 - t_index_selection.loc[:,'HHI_by_country']) + cl_coef*t_index_selection.loc[:,'ICL'])/\
                             (cl_coef + t_coef - hhi_coef)


    # Utility function
    #t_index_selection.loc[:,'U'] = t_index_selection[['norm_log_t_index','HHI_by_country','ICL']].apply(lambda x: (t_coef*x[0]-hhi_coef*(1-x[1])+ cl_coef*x[2])/(cl_coef + t_coef - hhi_coef) , axis=1)


    return t_index_selection



# S  -------------------------------------------------------------------------------------------------------------------------------------------------------------------


## Choose the respective measure for percapita plot --------------------------------------------------------------------------------------------------------------------

def switch_select_percapita_measure(argument):
    switcher = {
        'GLP_vanila': "GLP_vanila_per_cap",
        'w_GDP_lang_kummu': "w_GDP_lang_kummu_per_cap",
        'w_GDP_lang_GHS_kummu': "w_GDP_lang_GHS_kummu_per_cap"
    }
    return(switcher.get(argument, "Invalid measure"))

