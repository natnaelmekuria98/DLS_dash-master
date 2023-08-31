import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
import math
# from PIL import Image

from functions import *
from load_data import *

#from pages import Language_Overview_Page 

# ###### DEBUG LOGGER NOT USE ON PROD ######
# import logging

# logger = logging.getLogger(__name__)
# root_logger = logging.getLogger()
# root_logger.setLevel(logging.INFO)
# sh = logging.StreamHandler()
# formatter = logging.Formatter(
#     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# sh.setFormatter(formatter)
# #sh.setFormatter(CsvFormatter())
# root_logger.addHandler(sh)

# ######

# 1) Setup ------------------------------------------------------------------------------------------------------------------------------------------------------------

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# 2) Callbacks ---------------------------------------------------------------------------------------------------------------------------------------------------------

# 2.1) Matrices callbacks -----------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output("dls-dig-ins-matrix","children"),
    Input("dls-dig-ins-area-selected","value")
)
def update_digital_institutional_matrix(area):
    
    year = 2021

    no_x10_DLS = DLS_GLP_EGID_data[DLS_GLP_EGID_data["EGIDS"] != 'x10'].copy()


    mapping = { 'Still' : 'Non-Digital','Emerging':'Digital','Ascending':'Digital','Vital':'Digital' ,  'Thriving' :'Digital' }

    ##DLS_GLP_EGID_data['cluster_mapping'] = DLS_GLP_EGID_data.cluster.map(mapping)
    no_x10_DLS['digital'] = no_x10_DLS.DLS_Level.map(mapping)

    #old_DLS_GLP_EGID_data['cluster_mapping'] = old_DLS_GLP_EGID_data.cluster.map(mapping)

    mapping = { 'x10':'Non-Institutional','9':'Non-Institutional','8b':'Non-Institutional','8a':'Non-Institutional','7':'Non-Institutional' ,
            '6b':'Non-Institutional','6a':'Non-Institutional','5':'Non-Institutional',  
            '4':'Institutional','3':'Institutional','2':'Institutional','1':'Institutional','0':'Institutional' }

    no_x10_DLS['Institutional'] = no_x10_DLS.EGIDS.map(mapping)


    df_long_temp = no_x10_DLS[['ISO_639','digital','Institutional']].drop_duplicates().groupby(['digital','Institutional']).count()['ISO_639']

    df_long_temp = df_long_temp.unstack()

    df_long_temp.fillna(0,inplace= True)

    #no_x10_DLS.groupby(['Institutional','digital','Area']).count()["ISO_639"]

    # Plot setup -----------------------------------------------------------------------------------------------------------------------------------------------------------
    if area == "Global":
        data_filtered = no_x10_DLS
    elif  area in ["Africa","Europe","Americas","Pacific","Asia"] :
        data_filtered = no_x10_DLS[no_x10_DLS["Area"]== area]
    else:
        country_isos = LICs[LICs.Country_Name == area].ISO_639.values

        data_filtered = no_x10_DLS[no_x10_DLS["ISO_639"].isin(country_isos)]


    fig_test_2 = px.density_heatmap(data_filtered,x = 'Institutional',y = "digital",category_orders = {"Institutional":['Non-Institutional', 'Institutional'],
                                                                                                "digital":['Non-Digital','Digital'][::-1]} ,
                                #marginal_x="histogram", marginal_y="histogram",
                                #facet_col='Area', facet_col_wrap=2, 
                                color_continuous_scale='portland',
                                title = "Digital X Institutional, " + area + " - Count",#, text_auto=True
                                labels={"digital": "Language Status classifications",
                                        "Institutional": "Digital Language Support classifications"}
                                )


    fig_test_2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    #fig_test_2.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))


    fig_test_2.update_layout({'coloraxis': {'colorbar': {'title': {'text': 'count'}}}},
                             annotations=[dict(
                                 x=1.15,
                                 y=-.25,
                                 xref='paper',
                                 yref='paper',
                                 text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

                                 showarrow=False
                             )])


    # Annotations hack -----------------------------------------------------------------------------------------------------------------------------------------------------
    #Are you able to improve the 2x2 by adding two things
    #(1) adding Speaker totals into each quadrant;
    # Speakers by quadrant 

    # iso_count_by_quadrant = data_filtered.groupby(['Institutional','digital']).count()[['ISO_639']].reset_index()

    # speakers_by_quadrant = data_filtered.groupby(['Institutional','digital']).sum()[['L1']].reset_index()

    # #(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
    # #that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

    # speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()

    # # Merge groupping sum with counting sum 
    # speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant)
    # speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()

    iso_count_by_quadrant = data_filtered.groupby(['Institutional','digital']).count()[['ISO_639']].reset_index()

    # Testing expand grid to deal with zero count values

    col_expandgrid = expandgrid(no_x10_DLS.Institutional.unique(), no_x10_DLS.digital.unique() )

    col_prior = pd.DataFrame.from_dict(col_expandgrid)
    col_prior.rename(columns = {"Var1":"Institutional","Var2":"digital","Var3":"Area" },inplace = True)
    # 2022
    # data_filtered = data_filtered.astype({'Institutional': int, 'digital': int})
    # speakers_by_quadrant = data_filtered.groupby(['Institutional','digital']).sum()[['L1']].reset_index()
    speakers_by_quadrant = data_filtered.groupby(['Institutional','digital']).sum(numeric_only=True)[['L1']].reset_index()

    # Check data_filtered.L1 for any no float values
    pd.to_numeric(data_filtered['L1'], errors='coerce').isna().any()        
    data_filtered.loc[pd.to_numeric(data_filtered['L1'], errors='coerce').isna(),"L1"]

    speakers_by_quadrant = col_prior.merge(speakers_by_quadrant,on = ['Institutional','digital'],how= "left").fillna(0)

    # 2021
    #speakers_by_quadrant = no_x10_DLS.groupby(['Institutional','digital','Area']).sum()[['L1_Users']].reset_index()

    #(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
    #that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

    # 2022
    speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()
    # 2021
    #speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1_Users'] / speakers_by_quadrant['L1_Users'].sum()

    # Merge groupping sum with counting sum 
    speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant,how="left")
    speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()


    #fig_test_2.update_traces(texttemplate='%{z} <br> 12')

    areas = ["Africa","Europe","Americas","Pacific","Asia"]

    facet_coords = [["x","y5"],["x","y3"],["x","y"],["x2","y5"],["x2","y3"],]

    # x = [0,1] => ["Non-Institutional", "Institutional"] 
    Institutional = ["Non-Institutional", "Institutional"] 

    # y = [0,1] => ["Non-Digital","Digital"]
    digital = ["Non-Digital","Digital"]



    plot_annot_coord = [[0,0],[0,1],[1,0],[1,1]]


    for j in range(4):
            
        dig = speakers_by_quadrant[ (speakers_by_quadrant['Institutional'] == Institutional[ plot_annot_coord[j][0]]) &  # Filter by Institutional value
                                    (speakers_by_quadrant['digital'] == digital[ plot_annot_coord[j][1]])  # Filter by Digital value
                                    ] # Filter by Continent

        # text = str(dig['ISO_639'].values[0]) + ' languages <br>' + '% {:.2f}'.format(dig['lang_count_percentage'].values[0]*100) + ' of total languages<br>L1 Users :' + '{:,}'.format(dig['L1'].values[0]) + "<br>" + '% {:.2f}'.format(dig['L1_percentage'].values[0]*100) + ' of total speakers'

        iso_639 = dig['ISO_639'].values[0]
        lang_count_percentage = dig['lang_count_percentage'].values[0]
        l1 = dig['L1'].values[0]
        l1_percentage = dig['L1_percentage'].values[0]

        # Check if the values are NaN
        if math.isnan(iso_639):
            iso_639 = 0
        if math.isnan(lang_count_percentage):
            lang_count_percentage = 0.0
        if math.isnan(l1):
            l1 = 0
        if math.isnan(l1_percentage):
            l1_percentage = 0

        # text = str(dig['ISO_639'].values[0]) + ' languages <br>' + '% {:.2f}'.format(dig['lang_count_percentage'].values[0]*100) + ' of total languages<br>L1 Users :' + '{:,}'.format(dig['L1'].values[0]) + "<br>" + '% {:.2f}'.format(dig['L1_percentage'].values[0]*100) + ' of total speakers'
        text = f"{str(iso_639)} languages <br>% {lang_count_percentage*100:.2f} of total languages<br>L1 Users :{l1:,}<br>{l1_percentage*100:.2f} of total speakers"


        fig_test_2.add_annotation({
                                    'font': {},
                                    'showarrow': False,
                                    #'bgcolor': 'white',
                                    'font': {'size': 10, 'color': 'white'},
                                    #'text': str(i) + "x: " + str(plot_annot_coord[j][0]) + " y: " + str(plot_annot_coord[j][1]) ,
                                    'text': text,  #  506 languages (7.09% of total languages)
                                    'x': plot_annot_coord[j][0] ,
                                    'xanchor': 'center',
                                    'xref': 'x', 
                                    'y': plot_annot_coord[j][1]-.2,
                                    'yanchor': 'bottom',
                                    'yref': 'y'
                                    })

    return dcc.Graph(figure=fig_test_2,style = {'height': '100%'})

@callback(
    Output("dls-dig-ins-matrix-2","children"),
    Output("dls-dig-ins-matrix-2-title","children"),
    Input("dls-dig-ins-area-selected-2","value")
)
def update_digital_institutional_matrix(area):
    
    year = 2021

    no_x10_DLS = DLS_GLP_EGID_data[DLS_GLP_EGID_data["EGIDS"] != 'x10'].copy()


    mapping = { 'Still' : 'Non-Digital','Emerging':'Digital','Ascending':'Digital','Vital':'Digital' ,  'Thriving' :'Digital' }

    ##DLS_GLP_EGID_data['cluster_mapping'] = DLS_GLP_EGID_data.cluster.map(mapping)
    no_x10_DLS['digital'] = no_x10_DLS.DLS_Level.map(mapping)

    #old_DLS_GLP_EGID_data['cluster_mapping'] = old_DLS_GLP_EGID_data.cluster.map(mapping)

    mapping = { 'x10':'Non-Institutional','9':'Non-Institutional','8b':'Non-Institutional','8a':'Non-Institutional','7':'Non-Institutional' ,
            '6b':'Non-Institutional','6a':'Non-Institutional','5':'Non-Institutional',  
            '4':'Institutional','3':'Institutional','2':'Institutional','1':'Institutional','0':'Institutional' }

    no_x10_DLS['Institutional'] = no_x10_DLS.EGIDS.map(mapping)


    df_long_temp = no_x10_DLS[['ISO_639','digital','Institutional']].drop_duplicates().groupby(['digital','Institutional']).count()['ISO_639']

    df_long_temp = df_long_temp.unstack()

    df_long_temp.fillna(0,inplace= True)

    #no_x10_DLS.groupby(['Institutional','digital','Area']).count()["ISO_639"]

    # Plot setup -----------------------------------------------------------------------------------------------------------------------------------------------------------
    # if area == "Global":
    #     data_filtered = no_x10_DLS
    # elif  area in ["Africa","Europe","Americas","Pacific","Asia"] :
    #     data_filtered = no_x10_DLS[no_x10_DLS["Area"]== area]
    # else:
    country_isos = LICs[LICs.Country_Name == area].ISO_639.values

    data_filtered = no_x10_DLS[no_x10_DLS["ISO_639"].isin(country_isos)]


    fig_test_2 = px.density_heatmap(data_filtered,x = 'Institutional',y = "digital",category_orders = {"Institutional":['Non-Institutional', 'Institutional'],
                                                                                                "digital":['Non-Digital','Digital'][::-1]} ,
                                #marginal_x="histogram", marginal_y="histogram",
                                #facet_col='Area', facet_col_wrap=2, 
                                color_continuous_scale='portland',
                                title = "Digital X Institutional, " + area + " - Count",#, text_auto=True
                                labels={"digital": "Language Status classifications",
                                        "Institutional": "Digital Language Support classifications"}
                                )


    fig_test_2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    #fig_test_2.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))


    fig_test_2.update_layout({'coloraxis': {'colorbar': {'title': {'text': 'count'}}}},
                             annotations=[dict(
                                 x=1.15,
                                 y=-.25,
                                 xref='paper',
                                 yref='paper',
                                 text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

                                 showarrow=False
                             )])


    # Annotations hack -----------------------------------------------------------------------------------------------------------------------------------------------------
    #Are you able to improve the 2x2 by adding two things
    #(1) adding Speaker totals into each quadrant;
    # Speakers by quadrant 

    # iso_count_by_quadrant = data_filtered.groupby(['Institutional','digital']).count()[['ISO_639']].reset_index()

    # speakers_by_quadrant = data_filtered.groupby(['Institutional','digital']).sum()[['L1']].reset_index()

    # #(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
    # #that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

    # speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()

    # # Merge groupping sum with counting sum 
    # speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant)
    # speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()

    iso_count_by_quadrant = data_filtered.groupby(['Institutional','digital']).count()[['ISO_639']].reset_index()

    # Testing expand grid to deal with zero count values

    col_expandgrid = expandgrid(no_x10_DLS.Institutional.unique(), no_x10_DLS.digital.unique() )

    col_prior = pd.DataFrame.from_dict(col_expandgrid)
    col_prior.rename(columns = {"Var1":"Institutional","Var2":"digital","Var3":"Area" },inplace = True)
    # 2022
    speakers_by_quadrant = data_filtered.groupby(['Institutional','digital']).sum(numeric_only=True)[['L1']].reset_index()

    speakers_by_quadrant = col_prior.merge(speakers_by_quadrant,on = ['Institutional','digital'],how= "left").fillna(0)

    # 2021
    #speakers_by_quadrant = no_x10_DLS.groupby(['Institutional','digital','Area']).sum()[['L1_Users']].reset_index()

    #(2) adding % for Languages / Speakers for each quadrant. For example, Digital/Institutional = 506 languages (7.09% of total languages) 
    #that would total N L1 speakers (n% of total L1). Does this make sense? Thank you

    # 2022
    speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1'] / speakers_by_quadrant['L1'].sum()
    # 2021
    #speakers_by_quadrant.loc[:,'L1_percentage'] = speakers_by_quadrant['L1_Users'] / speakers_by_quadrant['L1_Users'].sum()

    # Merge groupping sum with counting sum 
    speakers_by_quadrant = speakers_by_quadrant.merge(iso_count_by_quadrant,how="left")
    speakers_by_quadrant.loc[:,'lang_count_percentage'] = speakers_by_quadrant['ISO_639'] / speakers_by_quadrant['ISO_639'].sum()


    #fig_test_2.update_traces(texttemplate='%{z} <br> 12')

    areas = ["Africa","Europe","Americas","Pacific","Asia"]

    facet_coords = [["x","y5"],["x","y3"],["x","y"],["x2","y5"],["x2","y3"],]

    # x = [0,1] => ["Non-Institutional", "Institutional"] 
    Institutional = ["Non-Institutional", "Institutional"] 

    # y = [0,1] => ["Non-Digital","Digital"]
    digital = ["Non-Digital","Digital"]



    plot_annot_coord = [[0,0],[0,1],[1,0],[1,1]]


    for j in range(4):
            
        dig = speakers_by_quadrant[ (speakers_by_quadrant['Institutional'] == Institutional[ plot_annot_coord[j][0]]) &  # Filter by Institutional value
                                    (speakers_by_quadrant['digital'] == digital[ plot_annot_coord[j][1]])  # Filter by Digital value
                                    ] # Filter by Continent
        
        iso_639 = dig['ISO_639'].values[0]
        lang_count_percentage = dig['lang_count_percentage'].values[0]
        l1 = dig['L1'].values[0]
        l1_percentage = dig['L1_percentage'].values[0]

        # Check if the values are NaN
        if math.isnan(iso_639):
            iso_639 = 0
        if math.isnan(lang_count_percentage):
            lang_count_percentage = 0.0
        if math.isnan(l1):
            l1 = 0
        if math.isnan(l1_percentage):
            l1_percentage = 0

        # text = str(dig['ISO_639'].values[0]) + ' languages <br>' + '% {:.2f}'.format(dig['lang_count_percentage'].values[0]*100) + ' of total languages<br>L1 Users :' + '{:,}'.format(dig['L1'].values[0]) + "<br>" + '% {:.2f}'.format(dig['L1_percentage'].values[0]*100) + ' of total speakers'
        text = f"{str(iso_639)} languages <br>% {lang_count_percentage*100:.2f} of total languages<br>L1 Users :{l1:,}<br>{l1_percentage*100:.2f} of total speakers"

        fig_test_2.add_annotation({
                                    'font': {},
                                    'showarrow': False,
                                    #'bgcolor': 'white',
                                    'font': {'size': 10, 'color': 'white'},
                                    #'text': str(i) + "x: " + str(plot_annot_coord[j][0]) + " y: " + str(plot_annot_coord[j][1]) ,
                                    'text': text,  #  506 languages (7.09% of total languages)
                                    'x': plot_annot_coord[j][0] ,
                                    'xanchor': 'center',
                                    'xref': 'x', 
                                    'y': plot_annot_coord[j][1]-.2,
                                    'yanchor': 'bottom',
                                    'yref': 'y'
                                    })
    area
    return [dcc.Graph(figure=fig_test_2,style = {'height': '100%'}),
            [
                    f'Digital Language Divide matrix For {area}'
                ]]


# 3) Static content -----------------------------------------------------------------------------------------------------------------------------------------------------


# 4) Layouts ------------------------------------------------------------------------------------------------------------------------------------------------------------

## 4.1) Cards -----------------------------------------------------------------------------------------------------------------------------------------------------------

card_icon = {
                "color": "white",
                "textAlign": "center",
                "fontSize": 30,
                "margin": "auto",
            }

## 4.2) Matrix Layout ----------------------------------------------------------------------------------------------------------------------------------------------------

matrix_layout = html.Div([
    # 1 - Row ---------------------------------------------------------------------------------------------------------------------------------------------------------
    dbc.Row([
        # 1.1 - Col -----------------------------------------------------------------------------------------------------------------------------------------------------
        dbc.Col([
            # Card ------------------------------------------------------------------------------------------------------------------------------------------------------
            dbc.Card([
                # Card Header -------------------------------------------------------------------------------------------------------------------------------------------
                dbc.CardHeader([html.H5(["Digital Language Divide matrix by Area",
                                        # html.Span(html.Div(className="fa fa-info-circle"),
                                        #           id='dls_digital_institutional_info',
                                        #           # style={"textDecoration": "underline", "cursor": "pointer"}
                                        #           ),
                                        html.Button('Info', id='dls_digital_institutional_info',
                                                    className="btn btn-theme", n_clicks=0),
                                        dbc.Popover(html.Div(["Digital means whether a language has a DLS level of Emerging or above ( Ascending, Vital, Thriving). Institutional languages have an EGIDS score equal to or above 4."]),
                                                    # className = 'bg-primary',
                                                    # style = {'background-color': 'rgb(120, 100, 225)'},
                                                    target="dls_digital_institutional_info",
                                                    body=True,
                                                    trigger="legacy",
                                                    placement='top'
                                                    )
                                        ], className="card-heading d-flex justify-content-between",
                                       style={'padding': '0px',
                                              'margin': '0px 0',
                                              "align-items": "baseline",
                                            #   'margin-bottom': '24px'
                                              }
                                       )  # need to remove html.P default margin and padding (alterates CardHeader height )
                                ],
                               className="bg-white text-black"),
                # Card Body ---------------------------------------------------------------------------------------------------------------------------------------------
                dbc.CardBody([
                    # Dropdown Menu ---------------------------------------------------------------------------------------------------------------------------------------------
                    dcc.Dropdown(options=[{'label': 'Global', 'value': 'Global'},
                                          {'label': 'Africa',
                                           'value': 'Africa'},
                                          {'label': 'Americas',
                                           'value': 'Americas'},
                                          {'label': 'Europe',
                                           'value': 'Europe'},
                                          {'label': 'Pacific',
                                           'value': 'Pacific'},
                                          #   {'label': 'Countries', 'value': 'Countries'},
                                          ],style={'width': '50%',
                                                   'margin-left': '10px',
                                                   'margin-top': '10px'},
                                 value="Global",
                                 id='dls-dig-ins-area-selected'),
                    # dcc.Dropdown(id = "dls-dig-ins-area-selected-second",value ="Global"),
                    # Loading circle and map plot (id = "datatable-interactivity-map-container" ) -------------------
                    dcc.Loading(children=[
                                # Plot container ------------------------------------------------------------------------------------------------------------------------
                                html.Div(id="dls-dig-ins-matrix")
                                ],
                                type="circle")
                ], style={'min-height': '455px', 'position': 'relative',
                          'padding': '0px'
                          # 'display': 'flex','align-items': 'center',
                          # 'justify-content':'center','position': 'relative'
                          },
                    # id = 'maps-cardbody'

                )
            ],
                style={"padding": "0"}),
        ], className="col-md-6"),
        # 1.2 - Col -----------------------------------------------------------------------------------------------------------------------------------------------------
        dbc.Col([
            # Card ------------------------------------------------------------------------------------------------------------------------------------------------------
            dbc.Card([
                # Card Header -------------------------------------------------------------------------------------------------------------------------------------------
                dbc.CardHeader([html.H5([
                    "Digital Language Divide matrix For "
                ], style={'padding': '6px 0px','margin': '0px 0px','align-items':'baseline'},
                id="dls-dig-ins-matrix-2-title")
                ], className="text-black card-heading d-flex justify-content-between"),
                # Card Body ---------------------------------------------------------------------------------------------------------------------------------------------
                dbc.CardBody([
                    # Dropdown Menu ---------------------------------------------------------------------------------------------------------------------------------------------
                    dcc.Dropdown(options=LICs.Country_Name.unique(),
                                 style={'width': '50%',
                                        'margin-left': '10px',
                                        'margin-top': '10px'},
                                 value="Nigeria",
                                 id='dls-dig-ins-area-selected-2'),
                    # dcc.Dropdown(id = "dls-dig-ins-area-selected-second",value ="Global"),
                    # Loading circle and map plot (id = "datatable-interactivity-map-container" ) -------------------
                    dcc.Loading(children=[
                        # Plot container ------------------------------------------------------------------------------------------------------------------------
                        html.Div(id="dls-dig-ins-matrix-2")
                    ], type="circle")
                ], style={'min-height': '455px', 'position': 'relative',
                          'padding': '0px'
                          # 'display': 'flex','align-items': 'center',
                          # 'justify-content':'center','position': 'relative'
                          },
                    # id = 'maps-cardbody'

                )

            ])
        ], className="col-md-6")
    ])
])
# 5) Page Layout Output ---------------------------------------------------------------------------------------------------------------------------------------------------

section = html.Section([matrix_layout],
                         className="container mt-5")

footer = html.Footer(
    className="mt-100",
    children=[
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="d-md-flex justifyContent-md-between text-center",
                    children=[
                        html.P(
                            className="mb-0",
                            children="Copyright © 2021–2023. Derivation LLC. All Rights Reserved.",
                        ),
                        html.Div(
                            className="mt-2 mt-md-0",
                            children=[
                                html.A(
                                    className="text-white me-3",
                                    href="https://derivation.co/about-us/",
                                    children="About",
                                ),
                                html.A(
                                    className="text-white",
                                    href="https://derivation.co/contact/",
                                    children="Support",
                                ),
                            ]),
                    ]),
            ]),
    ])


layout = html.Div([
    section,
    footer
])
