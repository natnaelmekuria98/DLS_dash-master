import dash
from dash import Input, Output, dcc, html, dash_table , State, callback
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
import dash_bootstrap_components as dbc
import plotly.express as px

from load_data import *
from functions import *

# Dropdown Options ------------------------------------------------------------------------------------------------------------------------------------------------------

# drop_menu = {"Global": ["Global"], "Africa": ["Africa"], "Americas": ["Americas"],
#              "Europe": ["Europe"], "Pacific": ["Pacific"], "Countries": [LICs.Country_Name.unique()]}

# names = list(drop_menu.keys())
# nestedOptions = drop_menu[names[0]]

# 1) Callbacks ----------------------------------------------------------------------------------------------------------------------------------------------------------

# 1.1) Main plot --------------------------------------------------------------------------------------------------------------------------------------------------------

# @callback(
#     Output("dls-dig-ins-matrix","children"),
#     Input("dls-dig-ins-area-selected","value")
# )
# def update_digital_institutional_matrix(area):
    
#     year = 2021

#     no_x10_DLS = DLS_GLP_EGID_data[DLS_GLP_EGID_data["EGIDS"] != 'x10'].copy()


#     mapping = { 'Still' : 'Non-Digital','Emerging':'Digital','Ascending':'Digital','Vital':'Digital' ,  'Thriving' :'Digital' }

#     ##DLS_GLP_EGID_data['cluster_mapping'] = DLS_GLP_EGID_data.cluster.map(mapping)
#     no_x10_DLS['digital'] = no_x10_DLS.DLS_Level.map(mapping)

#     #old_DLS_GLP_EGID_data['cluster_mapping'] = old_DLS_GLP_EGID_data.cluster.map(mapping)

#     mapping = { 'x10':'Non-Institutional','9':'Non-Institutional','8b':'Non-Institutional','8a':'Non-Institutional','7':'Non-Institutional' ,
#             '6b':'Non-Institutional','6a':'Non-Institutional','5':'Non-Institutional',  
#             '4':'Institutional','3':'Institutional','2':'Institutional','1':'Institutional','0':'Institutional' }

#     no_x10_DLS['Institutional'] = no_x10_DLS.EGIDS.map(mapping)


#     df_long_temp = no_x10_DLS[['ISO_639','digital','Institutional']].drop_duplicates().groupby(['digital','Institutional']).count()['ISO_639']

#     df_long_temp = df_long_temp.unstack()

#     df_long_temp.fillna(0,inplace= True)

#     #no_x10_DLS.groupby(['Institutional','digital','Area']).count()["ISO_639"]

#     # Plot setup -----------------------------------------------------------------------------------------------------------------------------------------------------------
#     if area == "Global":
#         data_filtered = no_x10_DLS
#     elif  area in ["Africa","Europe","Americas","Pacific","Asia"] :
#         data_filtered = no_x10_DLS[no_x10_DLS["Area"]== area]
#     else:
#         country_isos = LICs[LICs.Country_Name == area].ISO_639.values

#         data_filtered = no_x10_DLS[no_x10_DLS["ISO_639"].isin(country_isos)]


#     fig_test_2 = px.density_heatmap(data_filtered,x = 'Institutional',y = "digital",category_orders = {"Institutional":['Non-Institutional', 'Institutional'],
#                                                                                                 "digital":['Non-Digital','Digital'][::-1]} ,
#                                 #marginal_x="histogram", marginal_y="histogram",
#                                 #facet_col='Area', facet_col_wrap=2, 
#                                 color_continuous_scale='portland',
#                                 title = "Digital X Institutional, " + area + " - Count",#, text_auto=True
#                                 labels={"digital": "Digital"}
#                                 )


#     fig_test_2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
#     #fig_test_2.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))


#     fig_test_2.update_layout({'coloraxis': {'colorbar': {'title': {'text': 'count'}}}})


#     # Annotations hack -----------------------------------------------------------------------------------------------------------------------------------------------------
#     #Are you able to improve the 2x2 by adding two things
#     #(1) adding Speaker totals into each quadrant;
#     # Speakers by quadrant 

#     # iso_count_by_quadrant = data_filtered.groupby(['Institutional','digital']).count()[['ISO_639']].reset_index()

#     # speakers_by_quadrant = data_filtered.groupby(['Institutional','digital']).sum()[['L1']].reset_index()

#     # #(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
#     # #that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

#     # speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()

#     # # Merge groupping sum with counting sum 
#     # speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant)
#     # speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()

#     iso_count_by_quadrant = data_filtered.groupby(['Institutional','digital']).count()[['ISO_639']].reset_index()

#     # Testing expand grid to deal with zero count values

#     col_expandgrid = expandgrid(no_x10_DLS.Institutional.unique(), no_x10_DLS.digital.unique() )

#     col_prior = pd.DataFrame.from_dict(col_expandgrid)
#     col_prior.rename(columns = {"Var1":"Institutional","Var2":"digital","Var3":"Area" },inplace = True)
#     # 2022
#     # data_filtered = data_filtered.astype({'Institutional': int, 'digital': int})
#     # speakers_by_quadrant = data_filtered.groupby(['Institutional','digital']).sum()[['L1']].reset_index()
#     speakers_by_quadrant = data_filtered.groupby(['Institutional','digital']).sum(numeric_only=True)[['L1']].reset_index()

#     # Check data_filtered.L1 for any no float values
#     pd.to_numeric(data_filtered['L1'], errors='coerce').isna().any()        
#     data_filtered.loc[pd.to_numeric(data_filtered['L1'], errors='coerce').isna(),"L1"]

#     speakers_by_quadrant = col_prior.merge(speakers_by_quadrant,on = ['Institutional','digital'],how= "left").fillna(0)

#     # 2021
#     #speakers_by_quadrant = no_x10_DLS.groupby(['Institutional','digital','Area']).sum()[['L1_Users']].reset_index()

#     #(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
#     #that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

#     # 2022
#     speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()
#     # 2021
#     #speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1_Users'] / speakers_by_quadrant['L1_Users'].sum()

#     # Merge groupping sum with counting sum 
#     speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant,how="left")
#     speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()


#     #fig_test_2.update_traces(texttemplate='%{z} <br> 12')

#     areas = ["Africa","Europe","Americas","Pacific","Asia"]

#     facet_coords = [["x","y5"],["x","y3"],["x","y"],["x2","y5"],["x2","y3"],]

#     # x = [0,1] => ["Non-Institutional", "Institutional"] 
#     Institutional = ["Non-Institutional", "Institutional"] 

#     # y = [0,1] => ["Non-Digital","Digital"]
#     digital = ["Non-Digital","Digital"]



#     plot_annot_coord = [[0,0],[0,1],[1,0],[1,1]]


#     for j in range(4):
            
#         dig = speakers_by_quadrant[ (speakers_by_quadrant['Institutional'] == Institutional[ plot_annot_coord[j][0]]) &  # Filter by Institutional value
#                                     (speakers_by_quadrant['digital'] == digital[ plot_annot_coord[j][1]])  # Filter by Digital value
#                                     ] # Filter by Continent

#         text = str(dig['ISO_639'].values[0]) + ' languages <br>' + '% {:.2f}'.format(dig['lang_count_percentage'].values[0]*100) + ' of total languages<br>L1 Users :' + '{:,}'.format(dig['L1'].values[0]) + "<br>" + '% {:.2f}'.format(dig['L1_percentage'].values[0]*100) + ' of total speakers'

#         fig_test_2.add_annotation({
#                                     'font': {},
#                                     'showarrow': False,
#                                     #'bgcolor': 'white',
#                                     'font': {'size': 10, 'color': 'white'},
#                                     #'text': str(i) + "x: " + str(plot_annot_coord[j][0]) + " y: " + str(plot_annot_coord[j][1]) ,
#                                     'text': text,  #  506 languages (7.09% of total languages)
#                                     'x': plot_annot_coord[j][0] ,
#                                     'xanchor': 'center',
#                                     'xref': 'x', 
#                                     'y': plot_annot_coord[j][1]-.2,
#                                     'yanchor': 'bottom',
#                                     'yref': 'y'
#                                     })

#     return dcc.Graph(figure=fig_test_2,style = {'height': '100%'})

# @callback(
#     Output("dls-dig-ins-matrix-2","children"),
#     Input("dls-dig-ins-area-selected-2","value")
# )
# def update_digital_institutional_matrix(area):
    
#     year = 2021

#     no_x10_DLS = DLS_GLP_EGID_data[DLS_GLP_EGID_data["EGIDS"] != 'x10'].copy()


#     mapping = { 'Still' : 'Non-Digital','Emerging':'Digital','Ascending':'Digital','Vital':'Digital' ,  'Thriving' :'Digital' }

#     ##DLS_GLP_EGID_data['cluster_mapping'] = DLS_GLP_EGID_data.cluster.map(mapping)
#     no_x10_DLS['digital'] = no_x10_DLS.DLS_Level.map(mapping)

#     #old_DLS_GLP_EGID_data['cluster_mapping'] = old_DLS_GLP_EGID_data.cluster.map(mapping)

#     mapping = { 'x10':'Non-Institutional','9':'Non-Institutional','8b':'Non-Institutional','8a':'Non-Institutional','7':'Non-Institutional' ,
#             '6b':'Non-Institutional','6a':'Non-Institutional','5':'Non-Institutional',  
#             '4':'Institutional','3':'Institutional','2':'Institutional','1':'Institutional','0':'Institutional' }

#     no_x10_DLS['Institutional'] = no_x10_DLS.EGIDS.map(mapping)


#     df_long_temp = no_x10_DLS[['ISO_639','digital','Institutional']].drop_duplicates().groupby(['digital','Institutional']).count()['ISO_639']

#     df_long_temp = df_long_temp.unstack()

#     df_long_temp.fillna(0,inplace= True)

#     #no_x10_DLS.groupby(['Institutional','digital','Area']).count()["ISO_639"]

#     # Plot setup -----------------------------------------------------------------------------------------------------------------------------------------------------------
#     # if area == "Global":
#     #     data_filtered = no_x10_DLS
#     # elif  area in ["Africa","Europe","Americas","Pacific","Asia"] :
#     #     data_filtered = no_x10_DLS[no_x10_DLS["Area"]== area]
#     # else:
#     country_isos = LICs[LICs.Country_Name == area].ISO_639.values

#     data_filtered = no_x10_DLS[no_x10_DLS["ISO_639"].isin(country_isos)]


#     fig_test_2 = px.density_heatmap(data_filtered,x = 'Institutional',y = "digital",category_orders = {"Institutional":['Non-Institutional', 'Institutional'],
#                                                                                                 "digital":['Non-Digital','Digital'][::-1]} ,
#                                 #marginal_x="histogram", marginal_y="histogram",
#                                 #facet_col='Area', facet_col_wrap=2, 
#                                 color_continuous_scale='portland',
#                                 title = "Digital X Institutional, " + area + " - Count",#, text_auto=True
#                                 labels={"digital": "Digital"}
#                                 )


#     fig_test_2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
#     #fig_test_2.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))


#     fig_test_2.update_layout({'coloraxis': {'colorbar': {'title': {'text': 'count'}}}})


#     # Annotations hack -----------------------------------------------------------------------------------------------------------------------------------------------------
#     #Are you able to improve the 2x2 by adding two things
#     #(1) adding Speaker totals into each quadrant;
#     # Speakers by quadrant 

#     # iso_count_by_quadrant = data_filtered.groupby(['Institutional','digital']).count()[['ISO_639']].reset_index()

#     # speakers_by_quadrant = data_filtered.groupby(['Institutional','digital']).sum()[['L1']].reset_index()

#     # #(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
#     # #that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

#     # speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()

#     # # Merge groupping sum with counting sum 
#     # speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant)
#     # speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()

#     iso_count_by_quadrant = data_filtered.groupby(['Institutional','digital']).count()[['ISO_639']].reset_index()

#     # Testing expand grid to deal with zero count values

#     col_expandgrid = expandgrid(no_x10_DLS.Institutional.unique(), no_x10_DLS.digital.unique() )

#     col_prior = pd.DataFrame.from_dict(col_expandgrid)
#     col_prior.rename(columns = {"Var1":"Institutional","Var2":"digital","Var3":"Area" },inplace = True)
#     # 2022
#     speakers_by_quadrant = data_filtered.groupby(['Institutional','digital']).sum(numeric_only=True)[['L1']].reset_index()

#     speakers_by_quadrant = col_prior.merge(speakers_by_quadrant,on = ['Institutional','digital'],how= "left").fillna(0)

#     # 2021
#     #speakers_by_quadrant = no_x10_DLS.groupby(['Institutional','digital','Area']).sum()[['L1_Users']].reset_index()

#     #(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
#     #that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

#     # 2022
#     speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()
#     # 2021
#     #speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1_Users'] / speakers_by_quadrant['L1_Users'].sum()

#     # Merge groupping sum with counting sum 
#     speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant,how="left")
#     speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()


#     #fig_test_2.update_traces(texttemplate='%{z} <br> 12')

#     areas = ["Africa","Europe","Americas","Pacific","Asia"]

#     facet_coords = [["x","y5"],["x","y3"],["x","y"],["x2","y5"],["x2","y3"],]

#     # x = [0,1] => ["Non-Institutional", "Institutional"] 
#     Institutional = ["Non-Institutional", "Institutional"] 

#     # y = [0,1] => ["Non-Digital","Digital"]
#     digital = ["Non-Digital","Digital"]



#     plot_annot_coord = [[0,0],[0,1],[1,0],[1,1]]


#     for j in range(4):
            
#         dig = speakers_by_quadrant[ (speakers_by_quadrant['Institutional'] == Institutional[ plot_annot_coord[j][0]]) &  # Filter by Institutional value
#                                     (speakers_by_quadrant['digital'] == digital[ plot_annot_coord[j][1]])  # Filter by Digital value
#                                     ] # Filter by Continent

#         text = str(dig['ISO_639'].values[0]) + ' languages <br>' + '% {:.2f}'.format(dig['lang_count_percentage'].values[0]*100) + ' of total languages<br>L1 Users :' + '{:,}'.format(dig['L1'].values[0]) + "<br>" + '% {:.2f}'.format(dig['L1_percentage'].values[0]*100) + ' of total speakers'

#         fig_test_2.add_annotation({
#                                     'font': {},
#                                     'showarrow': False,
#                                     #'bgcolor': 'white',
#                                     'font': {'size': 10, 'color': 'white'},
#                                     #'text': str(i) + "x: " + str(plot_annot_coord[j][0]) + " y: " + str(plot_annot_coord[j][1]) ,
#                                     'text': text,  #  506 languages (7.09% of total languages)
#                                     'x': plot_annot_coord[j][0] ,
#                                     'xanchor': 'center',
#                                     'xref': 'x', 
#                                     'y': plot_annot_coord[j][1]-.2,
#                                     'yanchor': 'bottom',
#                                     'yref': 'y'
#                                     })

#     return dcc.Graph(figure=fig_test_2,style = {'height': '100%'})

# 1.2) Generate country options -----------------------------------------------------------------------------------------------------------------------------------------

# @callback(
#     Output('dls-dig-ins-area-selected-second', 'options'),
#     Input('dls-dig-ins-area-selected', 'value')
# )
# def update_date_dropdown(name):
#     return [{'label': i, 'value': i} for i in drop_menu[name]]

# @callback(
#     dash.dependencies.Output('dls-dig-ins-area-selected-second', 'value'),
#     [dash.dependencies.Input('dls-dig-ins-area-selected-second', 'options')])
# def set_cities_value(available_options):
#     return available_options[0]['value']


# Layout ----------------------------------------------------------------------------------------------------------------------------------------------------------------

layout = html.Div([
    # 1 - Row ---------------------------------------------------------------------------------------------------------------------------------------------------------
    dbc.Row([
        # 1.1 - Col -----------------------------------------------------------------------------------------------------------------------------------------------------
        dbc.Col([
            # Card ------------------------------------------------------------------------------------------------------------------------------------------------------
            dbc.Card([  
                # Card Header -------------------------------------------------------------------------------------------------------------------------------------------
                dbc.CardHeader([ html.P(["Digital Language Support Matrix (Digital x Institutional) ",
                                        html.Span(html.Div(className="fa fa-info-circle"),
                                                            id = 'dls_digital_institutional_info' ,
                                                            #style={"textDecoration": "underline", "cursor": "pointer"}
                                                            ),
                                        dbc.Popover(html.Div(["Digital means whether a language has a DLS level of Emerging or above ( Ascending, Vital, Thriving). Institutional languages have an EGIDS score equal to or above 4."])
                                                    ,
                                                    #className = 'bg-primary',
                                                    #style = {'background-color': 'rgb(120, 100, 225)'},
                                                    target="dls_digital_institutional_info",
                                                    body=True,
                                                    trigger="hover",
                                                    placement='top'
                                                    )
                                        ],
                                        style = {'padding': '0px','margin': '0px 0'}
                                        ) # need to remove html.P default margin and padding (alterates CardHeader height )
                                ],
                            className="bg-primary text-white"),
                # Card Body ---------------------------------------------------------------------------------------------------------------------------------------------
                dbc.CardBody([
                            # Dropdown Menu ---------------------------------------------------------------------------------------------------------------------------------------------
                            dcc.Dropdown(options=[{'label': 'Global', 'value': 'Global'},
                                                  {'label': 'Africa', 'value': 'Africa'},
                                                  {'label': 'Americas', 'value': 'Americas'},
                                                  {'label': 'Europe', 'value': 'Europe'},
                                                  {'label': 'Pacific', 'value': 'Pacific'},
                                                #   {'label': 'Countries', 'value': 'Countries'},
                                                  ],
                                                value = "Global",
                                                id='dls-dig-ins-area-selected'),
                            #dcc.Dropdown(id = "dls-dig-ins-area-selected-second",value ="Global"),                    
                            ### Loading circle and map plot (id = "datatable-interactivity-map-container" ) -------------------
                            dcc.Loading(children=[
                                # Plot container ------------------------------------------------------------------------------------------------------------------------
                                html.Div(id="dls-dig-ins-matrix")
                            ],
                                        type="circle")                                                                        
                            ],style = { 'min-height': '455px','position': 'relative',
                                        #'display': 'flex','align-items': 'center',
                                        #'justify-content':'center','position': 'relative'
                                        },
                            #id = 'maps-cardbody'
                                    
                            )
                ],
                style = {"padding": "0"}),            
        ],className="col-md-6"),
        # 1.2 - Col -----------------------------------------------------------------------------------------------------------------------------------------------------
        dbc.Col([
            # Card ------------------------------------------------------------------------------------------------------------------------------------------------------
            dbc.Card([  
                # Card Header -------------------------------------------------------------------------------------------------------------------------------------------
                dbc.CardHeader([ html.P([
                    "Digital Language Support Matrix (Digital x Institutional) - By Country "
                    ],style = {'padding': '0px','margin': '0px 0'})
                    ],className="bg-primary text-white"),
                # Card Body ---------------------------------------------------------------------------------------------------------------------------------------------
                dbc.CardBody([
                    # Dropdown Menu ---------------------------------------------------------------------------------------------------------------------------------------------
                    dcc.Dropdown(options=LICs.Country_Name.unique(),
                                        value = "Nigeria",
                                        id='dls-dig-ins-area-selected-2'),
                    #dcc.Dropdown(id = "dls-dig-ins-area-selected-second",value ="Global"),                    
                    ### Loading circle and map plot (id = "datatable-interactivity-map-container" ) -------------------
                    dcc.Loading(children=[
                        # Plot container ------------------------------------------------------------------------------------------------------------------------
                        html.Div(id="dls-dig-ins-matrix-2")
                        ],type="circle")
                    ],style = { 'min-height': '455px','position': 'relative',
                                #'display': 'flex','align-items': 'center',
                                #'justify-content':'center','position': 'relative'
                                },
                    #id = 'maps-cardbody'
                            
                    )

        ])
    ],className="col-md-6")
])
])