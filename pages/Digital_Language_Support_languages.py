import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
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

## 2.1) 3D box - DLS-GLP-EGIDS -----------------------------------------------------------------------------------------------------------------------------------------

@callback(Output('3D_box_dls_glp_egids','children'),
          #Output('3D_hover_Data','children'),
          Input('3D_box_color','value'),
          Input('selected_language', 'value'),
          Input("z_axis","value"),
          Input("3D_box_xaxis","value")
          #State('3D_box_dls_glp_egids','clickData'), prevent_initial_call=True
          )
def updated_3d_box(color,Language_selected,z_axis,x_axis):
    """
    updated_3d_box(color,Language_selected,z_axis,x_axis)
    -----------------------------------------------------

    Update 3D box given selected language and axis and color change.

    Parameters
    ----------

    color: str
        Select 3D box group by colors. Three possible values: Area, Region_Name, Family.
    Language_selected: list
        Select one or more language from SIL database to display.
    z_axis: str
        Select different DLS measures for the z axis. Possible values: 
        Assistant, Speech, Meaning, Localized, Surface, Content, Encoding
    x_axis:
        Select users type for the x axis. Possible values: All, L1, L2

    Returns
    -------
    dash.dcc.Graph.Graph
        A 3D scatterplot.

    """
    x_axis_label = {"All": "All Users", "L1": "L1 Users", "L2": "L2 Users"}

    # a) Make 3D box ---------------------------------------------------------------------------------------------------------------------------------------------------
    # Obs.: Custom data os used to get ISO data for clickevent and Area for hover
    fig_3dbox = px.scatter_3d(DLS_GLP_EGID_data, x=x_axis, y='EGIDS', z=z_axis,
                              color=color, log_x=True, hover_name = "Language_Name", custom_data = ["ISO_639","Area"],
                              category_orders = {"EGIDS":pd.CategoricalIndex(DLS_GLP_EGID_data["EGIDS"]).categories}, height=500,
                              labels={
                                           x_axis: x_axis_label[x_axis],
                                           "EGIDS": "EGIDS",
                                           "Adjusted_Score": "Digital Language Support Score"
                                       }, opacity=0.5,
                                template = "plotly_white"
                              )

    # Set 3D box hover 
    fig_3dbox.update_traces(hovertemplate='<b>%{hovertext}</b><br><br>Area = %{customdata[1]}<br>L1 Users = %{x}<br>EGIDS = %{y}<br>Digital Language<br>Support Score = %{z}<extra></extra>',
        marker = {"size" : 4.7}
    )
    # fig2 = px.imshow(Image.open("assets/images/logo/derivation-logo.png"))
    # fig_3dbox.add_trace(fig2.data[0])

    # Set click mode
    fig_3dbox.update_layout(clickmode='event+select')

    # b) 3D box formating ---------------------------------------------------------------------------------------------------------------------------------------------------
    # Camera initial position
    #camera = dict(
    #    eye=dict(x=1.7702700919608734, y=-2.5555325887349833, z=0.6990227175556791)
    #)
    camera = {"center": {
                          "x": -0.043639136922750205,
                          "y": -0.11818211100672854,
                          "z": -0.18322483647692656
                        },
                        "eye": {
                          "x": 1.215874617277591,
                          "y": -1.5033885706975556,
                          "z": 0.4102674678509134
                        }}




    # Padding formatting
    fig_3dbox.update_layout(
        margin=dict(l=20,
                    r=25,
                    b=30,
                    t=30,
                    pad=4
                    ),
        scene_camera=camera,
        # images=[dict(
        #     #source="assets/images/logo/derivation-logo.png",#\assets\images\logo
        #     source=Image.open("assets/images/logo/derivation-logo.png"),
        #     xref="paper", yref="paper",
        #     x=1.2, y=0.065,
        #     sizex=0.2, sizey=0.2,
        #     xanchor="right", yanchor="bottom"
        #     )],
        
        annotations = [dict(
            x=1.3,
            y=0,
            xref='paper',
            yref='paper',
            text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

            showarrow = False
        )]
        )

    # c) Adding Language ---------------------------------------------------------------------------------------------------------------------------------------------------

    if Language_selected == None: 
        iso = 'eng'
        Language_selected = "English"
    # else:    
    #     #return str(Language_selected[0]['props']['children'][0])
    #     Language_selected = Language_selected[0]['props']['children'][0]

    # getting iso from selected language 
    # iso = LICs.loc[LICs['Language_Name'] == Language_selected ]['ISO_639'].unique()[0]


    # If no data is clicked pass english as default
    #if clickData == None: 
    #    iso = 'eng'
    #    seletect_language = "English"
    #else:
    #    # Get ISO from clicked point
    #    iso = clickData["points"][0]["customdata"][0]
    #    seletect_language = clickData["points"][0]["hovertext"]

    if type(Language_selected) == str:
        Language_selected = [Language_selected]

    for lang in Language_selected:
        #selected_lang_data = DLS_GLP_EGID_data[DLS_GLP_EGID_data['ISO_639'] == iso]
        
        selected_lang_data = DLS_GLP_EGID_data[DLS_GLP_EGID_data['Reference_Name'] == lang]
        
        #x_axis: x_axis_label[x_axis],
        fig_3dbox.add_scatter3d( x= selected_lang_data[x_axis],y= selected_lang_data.EGIDS, z= selected_lang_data[z_axis],
                                mode = 'markers', 
                                        hovertemplate = ('<b>'+ selected_lang_data['Language_Name'].values[0] +'</b><br><br>Area = '+selected_lang_data['Area'].values[0] +'\
                                                            <br>'+x_axis_label[x_axis]+' = '+str(selected_lang_data[x_axis].values[0]) +'<br>EGIDS = '+selected_lang_data['EGIDS'].values[0] +'\
                                                            <br>Digital Language<br>Support Score = '+ str(selected_lang_data['Adjusted_Score'].values[0]) +'<extra></extra>'
                                                        ),
                                        hovertext = selected_lang_data['Language_Name'], 
                                        name = "Selected Language",
                                        marker=dict(
                                                        color='black',
                                                        symbol = 'x',   #['circle', 'circle-open', 'cross', 'diamond','diamond-open', 'square', 'square-open', 'x']
                                                        size=3,
                                                        line=dict(
                                                            color='black',
                                                            width=2
                                                                )
                                                    )
                                        )
        
    annotations = [dict(x=np.log10(DLS_GLP_EGID_data[DLS_GLP_EGID_data['Reference_Name'] == lang][x_axis]).values[0],
                        y=DLS_GLP_EGID_data[DLS_GLP_EGID_data['Reference_Name']
                                            == lang].EGIDS.cat.codes.values[0],
                        z=DLS_GLP_EGID_data[DLS_GLP_EGID_data['Reference_Name']
                                            == lang][z_axis].values[0],
                        ax=-30, ay=-30, arrowsize=2, arrowwidth=1, showarrow=True,
                        arrowhead=1,
                        font=dict(
        color="black",
        size=12
    ),
        text=f"<b>{lang}</b>", xanchor="left", yanchor="bottom") for lang in Language_selected]

    # fig_3dbox.update_layout(
    #     scene=dict(
    #         annotations=[
    #             dict(
    #                 showarrow=True,
    #                 x=0,
    #                 y=0,
    #                 z=0,
    #                 ax=50,
    #                 ay=0,
    #                 text="Point 3",
    #                 arrowhead=1,
    #                 xanchor="left",
    #                 yanchor="bottom")]
    #     ),
    # )
    fig_3dbox.update_layout(
        scene=dict(
            annotations=annotations
        ),
    )


    hover_data = { "points": [ { "x": 94909056.8994485, "y": "3", "z": 5.3089, "curveNumber": 5, "pointNumber": 0, "hovertext": "Tuvaluan", "bbox": { "x0": 228.97723098492847, "x1": 228.97723098492847, "y0": 200.2765065567537, "y1": 200.2765065567537 } } ] }
    
    return dcc.Graph(id = 'DLS_GLP_EGIDs_3d',
                    hoverData = { "points": [ { "x": 94909056.8994485, "y": "3", "z": 5.3089, "curveNumber": 5, "pointNumber": 0, "hovertext": "Tuvaluan", "bbox": { "x0": 228.97723098492847, "x1": 228.97723098492847, "y0": 200.2765065567537, "y1": 200.2765065567537 } } ] },
                     figure = fig_3dbox,config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'],'displaylogo': False})

## 2.2) Right panel with features by type -----------------------------------------------------------------------------------------------------------------------------

@callback(Output('features_count_by_type_plot','children'),
          Output('features_count_by_type_table','children'),
          #Output('selected_language','children'),
          Output('Language_DLS_score_plot','children'),
          Output('Language_DLS_score_table','children'),
        #   Output('Language_L1_map','children'),
          Output('selected_language_modal','options'),
          #Input('DLS_GLP_EGIDs_3d','clickData'),
          Input('selected_language','value'))
def update_features_by_type(selected_language):
    """
    update_features_by_type(selected_language)
    ------------------------------------------

    Update both bar plots which DLS scores, Features count and Language maps.

    Parameters
    ----------
    selected_language: str

    Returns
    -------
    list
        list of dash objectes. First is a dbc.Tabs with a feature count by type barplot and a table.
        The second is a dbc.Tabs with the dls score by category barplot and a table

    """
    # Setup -------------------------------------------------------------------------------------------------------------------------------------------------------------
    # if ( selected_language == None ) | (clickData != None) :
    #     # If no data is clicked pass english as default
    if selected_language == None: 
        iso = 'eng'
        selected_language = "English"

    if type(selected_language) == str:
        selected_language = [selected_language]    
    #     else:
    #         # Get ISO from clicked point
    #         iso = clickData["points"][0]["customdata"][0]
    #         seletect_language = clickData["points"][0]["hovertext"]
    # else:
    #     seletect_language = seletect_language[0]['props']['children'][0]

    # getting iso from selected language 
    #iso = LICs.loc[LICs['Language_Name'] == selected_language ]['ISO_639'].unique()[0]
    #selected_lang_data = DLS_GLP_EGID_data[DLS_GLP_EGID_data['Reference_Name'] == selected_language]
    
    ## a) Feature count data -------------------------------------------------------------------------------------------------------------------------------------------
    # Count features by support type
    #features_by_support = dls_mapped_data[dls_mapped_data["ISO_639"]==iso].groupby('support_level')['feature_name'].count()
    #features_by_support = DLS_features_by_lang[DLS_features_by_lang["ISO_639"]==iso].groupby('Support_Category')['Feature_Name'].count()
    #features_by_support = DLS_features_by_lang[DLS_features_by_lang["Reference_Name"]==selected_language].groupby('Support_Category')['Feature_Name'].count()
    
    
    #features_by_support = DLS_features_by_lang[DLS_features_by_lang['Reference_Name'].isin(selected_language)].groupby('Support_Category')['Feature_Name'].count()
    #features_by_support = DLS_features_by_lang[DLS_features_by_lang['Reference_Name'].isin(selected_language)].groupby(['Reference_Name','Support_Category'])['Feature_Name'].count()
    features_by_support = DLS_features_by_lang.groupby([pd.Categorical(DLS_features_by_lang.Reference_Name),'Support_Category'])['Feature_Name'].count().fillna(0)
    
    #features_by_support["English"]
    # df = DLS_features_by_lang[DLS_features_by_lang['Reference_Name'].isin(selected_language)]
    # features_by_support = df.groupby([pd.Categorical(DLS_features_by_lang.Support_Category),'Reference_Name']).count()
    # df.groupby([pd.Categorical(df.Reference_Name),'Support_Category']).count().fillna(0)
    
    # Transforms count from series to data frame
    features_by_support = features_by_support.to_frame()

    # rowname to index 
    features_by_support.reset_index(inplace=True)

    

    # premade data to make bar plot all look the same
    #fetures_template = pd.DataFrame.from_dict({'Support_Category': ['Assistant','Speech','Meaning','Localized','Surface','Encoding','Content']})

    #features_by_support = fetures_template.merge(features_by_support,how = 'left').fillna(0)

    features_by_support = features_by_support[features_by_support["level_0"].isin(selected_language)]

    # OBS.: This bit is necessary because in pandas 1.5.0 or plotly 5.10 the filtered values stays hiding. This issue makes the px.bar broke.
    # px.bar uses a function get_group that returns all the groups from before ther filter (go figure). Because of this
    # it is need some way to unlink this. This is done by creating a completed unrelated dataframe. I only manage to do this
    # by transforming the dataframe into a dict and them into a dataframe again.
    features_by_support = features_by_support.query(f"level_0 == {selected_language}").to_dict("records")
    
    features_by_support = pd.DataFrame(features_by_support)
    

    features_by_support.rename(columns={'level_0': 'Reference_Name'}, inplace=True)

    #del(fetures_template)

    # Bar plot ---------------------------------------------------------------------------------------------------------------------------------------------------------
    fig_bar = px.bar(features_by_support.loc[::-1], x="Feature_Name", y="Support_Category",
                     color = "Reference_Name", barmode="group", orientation='h',height=393,
                     template = "plotly_white")
    
    # set range
    #max_feature_count = dls_mapped_data.groupby(['ISO_639','support_level'])['feature_name'].count().max()
    max_feature_count = DLS_features_by_lang.groupby(['ISO_639','Support_Category'])['Feature_Name'].count().max()
    fig_bar.update_xaxes(range=[0, max_feature_count ],autorange="reversed")
    fig_bar.update_yaxes(side='right')

    # Category Order 
    category_orders = {'index': ['Content','Encoding','Surface','Localized','Meaning','Speech','Assistant']}

    # Padding formatting
    fig_bar.update_layout(
        yaxis=dict(categoryorder='array', categoryarray=category_orders['index']),
        #paper_bgcolor="LightSteelBlue",
        margin=dict(l=20,
            r=25,
            #b=120,
            t=30,
            pad=4
            ),
        # images=[dict(
        #     #source="assets/images/logo/derivation-logo.png",#\assets\images\logo
        #     source=Image.open("assets/images/logo/derivation-logo.png"),
        #     xref="paper", yref="paper",
        #     x=1.1, y=-0.35,
        #     sizex=0.2, sizey=0.2,
        #     xanchor="right", yanchor="bottom"
        #     )],
        annotations = [dict(
            x=1.1,
            y=-0.25,
            xref='paper',
            yref='paper',
            text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

            showarrow = False
        )],
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
        )

    ## b) DLS score by support -----------------------------------------------------------------------------------------------------------------------------------------
    
    # Bar plot ---------------------------------------------------------------------------------------------------------------------------------------------------------

    # Get language DLS scores and transpose it 
    #dls_scores = DLS.loc[DLS['ISO_639']==iso,'encoding':'assistant'].T
    #dls_scores = DLS_scores_by_lang.loc[DLS_scores_by_lang['ISO_639']==iso,'Content':'Assistant'].T

    
    # dls_scores = DLS_scores_by_lang.loc[DLS_scores_by_lang['Reference_Name']==selected_language,'Content':'Assistant'].T
    #dls_scores = DLS_scores_by_lang.loc[DLS_features_by_lang['Reference_Name'].isin(selected_language),'Content':'Assistant'].T
    
    df = DLS_scores_by_lang.loc[DLS_scores_by_lang['Reference_Name'].isin(selected_language)]
    dls_scores = pd.melt(df,id_vars = 'Reference_Name',value_vars = ['Content','Encoding','Surface','Localized','Meaning','Speech','Assistant'])

    # Se column name
    #dls_scores.set_axis(['DLS Scores'], axis=1, inplace=True)
    dls_scores = dls_scores.set_axis(['Reference_Name','index','DLS Scores'], axis=1)

    # Rowname to column
    #dls_scores.reset_index(inplace=True)

    # Make figure
    fig_column = px.bar(dls_scores, x="index", y="DLS Scores",orientation = 'v', color = "Reference_Name", barmode="group",
                        category_orders = {'index': ['Content','Encoding','Surface','Localized','Meaning','Speech','Assistant']},height=400,
                     template = "plotly_white")
    
    # Set y range and changes y label side 
    fig_column.update_yaxes(range=[0, 4 ],side='right')
    
    # Padding formatting
    fig_column.update_layout(
        #paper_bgcolor="LightSteelBlue",
        margin=dict(l=20,
            r=120,
            #b=120,
            t=30,
            pad=4
            ),
        # images=[dict(
        #     #source="assets/images/logo/derivation-logo.png",#\assets\images\logo
        #     source=Image.open("assets/images/logo/derivation-logo.png"),
        #     xref="paper", yref="paper",
        #     x=1.3, y=-0.37,
        #     sizex=0.2, sizey=0.2,
        #     xanchor="right", yanchor="bottom"
        #     )],
        annotations = [dict(
            x=1.3,
            y=-.25,
            xref='paper',
            yref='paper',
            text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

            showarrow = False
        )],
        legend=dict(
            #yanchor="top",
            y=0.99,
            #xanchor="left",
            x=1.1
        )
        )

    fig_column.update_xaxes(title_text=None)
    # Tables for tab ----------------------------------------------------------------------------------------------------------------------------------------------------

    ## Score table
    dls_score_table = dls_scores.pivot_table(index=["index"], columns = ['Reference_Name'],
                                             values=['DLS Scores'], aggfunc='first').fillna(0)

    #bottom_col_row = dls_score_table.columns.get_level_values(1)  #------------
    dls_score_table.columns =  dls_score_table.columns.droplevel(0)

    dls_score_table = dls_score_table.reset_index()

    dls_score_table = dash_table.DataTable(  # id='datatable-interactivity',
        style_header={'whiteSpace': 'normal',
            'height': 'auto',"font-family": "sans-serif",
            'border': '1px solid black',"border-width":" 1px 0px"},
        style_cell={ 'border': '1px solid grey',
                    "font-family": "sans-serif",
                    "border-width":" 1px" },
        style_data={ 'whiteSpace': 'normal','height': 'auto',
                    'border': '1px solid black',"border-width":" 1px 0px","font-family": "sans-serif"},
        columns=[
            #{"name": i, "id": i, "deletable": True, "selectable": True} for i in dls_mapped_data_by_ft2.columns
            {"name": i.replace("_", " "), "id": i,"filter_options" : {"case":"insensitive"}} for i in dls_score_table.columns

        ],
        style_as_list_view=True,
        #data=dls_mapped_data_by_ft.to_dict('records'),
        data=dls_score_table.to_dict('records'),
        editable=True,
        sort_action="native",
        sort_mode="multi",
        #row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        export_format='xlsx',
        export_headers='display',
    )

    ## Feat count table
    dls_feat_count = features_by_support.pivot_table(index=["Support_Category"], columns = ['Reference_Name'],
                                             values=['Feature_Name'], aggfunc='first').fillna(0)

    dls_feat_count.columns = dls_feat_count.columns.droplevel(0)

    dls_feat_count = dls_feat_count.reset_index()

    dls_feat_count = dash_table.DataTable(  # id='datatable-interactivity',
        style_header={'whiteSpace': 'normal',
            'height': 'auto',"font-family": "sans-serif",
            'border': '1px solid black',"border-width":" 1px 0px"},
        style_cell={ 'border': '1px solid grey',
                    "font-family": "sans-serif",
                    "border-width":" 1px" },
        style_data={ 'whiteSpace': 'normal','height': 'auto',
                    'border': '1px solid black',"border-width":" 1px 0px","font-family": "sans-serif"},
        columns=[
            #{"name": i, "id": i, "deletable": True, "selectable": True} for i in dls_mapped_data_by_ft2.columns
            {"name": i.replace("_", " "), "id": i,"filter_options" : {"case":"insensitive"}} for i in dls_feat_count.columns

        ],
        style_as_list_view=True,
        #data=dls_mapped_data_by_ft.to_dict('records'),
        data=dls_feat_count.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        #row_deletable=True,
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        export_format='xlsx',
        export_headers='display',
    )


    # Language Maps ------------------------------------------------------------------------------------------------------------------------------------------------------
    #filtered_data = LICs[ LICs.Uninverted_Name == selected_language]
    filtered_data = LICs[ LICs.Uninverted_Name.isin(selected_language)]
    ## 1) L1 Users
    fig = go.Figure(data=go.Choropleth(
                        locations = filtered_data['iso_3'],
                        z = filtered_data["L1_Users"],
                        text = filtered_data['Country_Name'],
                        colorscale = 'Viridis',
                        autocolorscale=False,
                        #reversescale=True,
                        marker_line_color='darkgray',
                        marker_line_width=0.5,
    
                        colorbar_title = "L1_Users" + '<br>Millions',
                    ))

    fig.update_layout(
            #title_text=users_dd,

            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),

            
            margin=dict(b=0, t=0, r=5, l=5),
            mapbox=dict(
                style="carto-positron",
                zoom=1, 
                center_lat = 0,
                center_lon = 0,
                ),
            annotations=[dict(
                                 x=.99,
                                 y=0.01,
                                 xref='paper',
                                 yref='paper',
                                 text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

                                 showarrow=False
                             )]
        )                    
    
    ## 2) Legal status map

    fig_legal = px.choropleth(data_frame= filtered_data.fillna('no data'),
                               locations= 'iso_3', 
                               locationmode="ISO-3",
                               color= 'Function_Label',
                               color_discrete_map={'no data':'grey'},
                               hover_name= "Country_Name",
                               hover_data= ["Function_Label","L1_Users"]
                               #,
                               #                    'Moderate':'Yellow',
                               #                    'Low':'Green'}
                               #scope="usa"
                               )

    fig_legal.update_layout(
            #title_text=users_dd,

            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),

            
            margin=dict(b=0, t=0, r=5, l=5),
            mapbox=dict(
                style="carto-positron",
                zoom=1, 
                center_lat = 0,
                center_lon = 0,
                ),
            annotations=[dict(
                                 x=.99,
                                 y=0.01,
                                 xref='paper',
                                 yref='paper',
                                 text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

                                 showarrow=False
                             )]
        )                    
    
    ## 3) EGIDs by country

    ## Filtering LICs by ISO_639
    #LICs_egid_ordered =  LICs[ LICs.Uninverted_Name == selected_language]

    ## Ordering LICs by egids, to make the legends in order
    LICs_egid_ordered = filtered_data.sort_values("EGIDS")

    # OBS.: This bit is necessary because in pandas 1.5.0 or plotly 5.10 the filtered values stays hiding. This issue makes the px broke.
    # px.bar uses a function get_group that returns all the groups from before ther filter (go figure). Because of this
    # it is need some way to unlink this. This is done by creating a completed unrelated dataframe. I only manage to do this
    # by transforming the dataframe into a dict and them into a dataframe again.
    LICs_egid_ordered = LICs_egid_ordered.to_dict("records")
    
    LICs_egid_ordered = pd.DataFrame(LICs_egid_ordered)

    fig_egids = px.choropleth(data_frame= LICs_egid_ordered.fillna('no data'),
                               locations= 'iso_3', 
                               locationmode="ISO-3",
                               color= 'EGIDS',
                               color_discrete_map={'no data':'grey'},
                               hover_name= "Country_Name",
                               hover_data= ["Function_Label","L1_Users"]
                               #,
                               #                    'Moderate':'Yellow',
                               #                    'Low':'Green'}
                               #scope="usa"
                               )

    fig_egids.update_layout(
            #title_text=users_dd,

            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),

            
            margin=dict(b=0, t=0, r=5, l=5),
            mapbox=dict(
                style="carto-positron",
                zoom=1, 
                center_lat = 0,
                center_lon = 0,
                ),
            annotations=[dict(
                                 x=1,
                                 y=0.01,
                                 xref='paper',
                                 yref='paper',
                                 text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

                                 showarrow=False
                             )]
        )                    
    
    # Tab with 3 maps 
    maps_modal_lang_info = dbc.Tabs([dbc.Tab([dcc.Graph(figure = fig,
                                                        config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                                                                'displaylogo': False}
                                                        )],
                                             label="L1 Users"),
                                     dbc.Tab([dcc.Graph(figure = fig_legal,
                                                        config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                                                                'displaylogo': False}
                                                        )], label="Legal Status"),
                                     dbc.Tab([dcc.Graph(figure = fig_egids,
                                                        config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                                                                'displaylogo': False}
                                                        )], label="EGIDS"),

                                    ])

    # Tables for modal --------------------------------------------------------------------------------------------------------------------------------------------------

    table_data = filtered_data[['ISO_639', 'Language_Name','Country_Name','Area','All_Users', 'L1_Users','L2_Users','Function_Label','EGIDS']]

    table_modal = dash_table.DataTable(  # id='datatable-interactivity',
        style_header={'whiteSpace': 'normal',
            'height': 'auto',"font-family": "sans-serif",
            'border': '1px solid black',"border-width":" 1px 0px"},
        style_cell={ 'border': '1px solid grey',
                    "font-family": "sans-serif",
                    "border-width":" 1px" },
        style_data={ 'whiteSpace': 'normal','height': 'auto',
                    'border': '1px solid black',"border-width":" 1px 0px","font-family": "sans-serif"},
        columns=[
            #{"name": i, "id": i, "deletable": True, "selectable": True} for i in dls_mapped_data_by_ft2.columns
            {"name": i.replace("_", " "), "id": i,"filter_options" : {"case":"insensitive"}} for i in table_data.columns
        ],
        style_as_list_view=True,
        #data=dls_mapped_data_by_ft.to_dict('records'),
        data=table_data.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        export_format='xlsx',
        export_headers='display',
    )

    # Dropdown menu -----------------------------------------------------------------------------------------------------------------------------------------------------
    
    menu_options = [{'label': lang, 'value': lang} for lang in selected_language ]
        
    # Save svg of fig_bar
    # fig_bar.update_layout(height=400,width=600)
    # fig_bar.write_image("assets/images/home/column.svg")


    # Output -----------------------------------------------------------------------------------------------------------------------------------------------------------
    
    return [[dcc.Graph(id='features_count_type',
                            figure=fig_bar,
                            config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'], 'displaylogo': False}
                            )], \
            [dls_feat_count], \
            [dcc.Graph(id='features_count_type', figure=fig_column,
                                           config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'], 'displaylogo': False})
                                           ], \
            [dls_score_table], \
            # [dbc.Tabs([
            #             dbc.Tab([dcc.Graph(id='features_count_type', figure=fig_column,
            #                                config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'], 'displaylogo': False})
            #                     ], label="Figure"),
            #             dbc.Tab([dls_score_table], label="Table")
            #             ], active_tab="tab-0")], \
            # [maps_modal_lang_info, table_modal] \
            menu_options
           ]

## 2.3) DLS cards -------------------------------------------------------------------------------------------------------------------------------------------------------

@callback([Output("dls_cat_card","children"),
          Output("dls_lvl_card","children")],
          Input('selected_language','value'))
def update_dls_cards(selected_language):
    """
    update_dls_cards(selected_language)
    -----------------------------------

    Callback used to update cards displaying each language rank and dls level.
    
    Parameters
    ----------
    selected_language: str

    Returns
    -------
    list
        Two list of html.P used to feel dls cards

    """
    if type(selected_language) == str:
        selected_language = [selected_language]   

    # dls_selected_lang = DLS_scores_by_lang[DLS_scores_by_lang['Reference_Name']==selected_language ]
    dls_selected_lang = DLS_scores_by_lang[DLS_scores_by_lang['Reference_Name'].isin(selected_language) ]
    
    dls_cat = [html.P(row[1]["Reference_Name"] + " DLS Level: " + row[1]["DLS_Level"],style = {"margin":"0px"}) for row in dls_selected_lang.iterrows() ]
    dls_lvl = [ html.P(row[1]["Reference_Name"] + " DLS rank position is " + str(int(row[1]["Rank"]))+ "º" ,style = {"margin":"0px"}) for row in dls_selected_lang.iterrows() ]
    
    # return [html.P(dls_selected_lang["Reference_Name"] + " DLS Level: " + dls_selected_lang["DLS_Level"]),
    #         html.P(dls_selected_lang["Reference_Name"] + " DLS rank position is " + str(int(dls_selected_lang["Rank"].values[0])))
    #        ]
    return [dls_cat,
            dls_lvl
           ]

## 2.4) Retrieve datatable -----------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output('dropdown_menu_selection_lang_feat', 'children'),
    Input('selected_language', 'value'))
def update_data(selected_language):
    """
    update_data(selected_language)
    ------------------------------

    Update table with seleted language(s) supported Digital Features

    Parameters
    ----------
    selected_language: str

    Returns
    -------
    dash.dash_table.DataTable.DataTable
        A table with the data.

    """

    #iso = TOLs[['Language_Name','ISO_639']][TOLs['Language_Name'] == selected_language]['ISO_639'].values[0]
    #dls_mapped_data_by_ft2 =  dls_mapped_data.groupby(dropdown_menu).count().iloc[:,0].reset_index(name='counts').sort_values("counts",ascending = False)
    #dls_mapped_data_by_ft2 =  DLS_features_by_lang.groupby(dropdown_menu).count().iloc[:,0].reset_index(name='counts').sort_values("counts",ascending = False)
    #dls_mapped_data_by_ft2 =   DLS_features_by_lang[DLS_features_by_lang['Reference_Name']==selected_language]
    if type(selected_language) == str:
        selected_language = [selected_language]
    
    dls_mapped_data_by_ft2 =   DLS_features_by_lang[DLS_features_by_lang['Reference_Name'].isin(selected_language)]
    
    #columns =  [{"name": i, "id": i,} for i in (dls_mapped_data_by_ft2.columns)]

    return [
        dash_table.DataTable(  # id='datatable-interactivity',
            style_header={'whiteSpace': 'normal',
                          'height': 'auto', "font-family": "sans-serif",
                          'border': '1px solid black', "border-width": " 1px 0px"},
            style_cell={'border': '1px solid grey',
                        "font-family": "sans-serif",
                        "border-width": " 1px"},
            style_data={'whiteSpace': 'normal', 'height': 'auto',
                        'border': '1px solid black', "border-width": " 1px 0px", "font-family": "sans-serif"},
            columns=[
                #{"name": i, "id": i, "deletable": True, "selectable": True} for i in dls_mapped_data_by_ft2.columns
                {"name": i.replace("_", " "), "id": i,"filter_options" : {"case":"insensitive"}} for i in dls_mapped_data_by_ft2.columns
            ],
            style_as_list_view=True,
            data=dls_mapped_data_by_ft2.to_dict('records'),
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            page_action="native",
            page_current=0,
            page_size=10,
            export_format='xlsx',
            export_headers='display',
        )


    ]

## 2.5) Modal handler ----------------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output("modal_lang_info", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal_lang_info", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    """
    toggle_modal(n1, n2, is_open)
    -----------------------------

    Parameters
    ----------
    n1: int
        Numbers of clicks in button. Used to open the modal.
    n2: int
        Numbers of clicks in button. Used to close the modal.
    is_open: bool
        Returns if modal is open.

    Returns
    -------
    bool
        Set modal status

    """
    if n1 or n2:
        return not is_open
    return is_open

 # DEBUGER 

# @callback(
#    Output('hover_test', 'children'),
#    Input('DLS_GLP_EGIDs_3d', 'hoverData'))
# def display_click_data(clickData):
#    return json.dumps(clickData, indent=2)

## 2.7) Language Maps Modal handler -------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output("Language_L1_map", "children"),
    Input("selected_language_modal", "value"),
    prevent_initial_call=True
)
def update_modal_lang_info(selected_language):


    # Map ---------------------------------------------------------------------------------------------------------------------------------------------------------------
    #filtered_data = LICs[ LICs.Uninverted_Name == selected_language]
    filtered_data = LICs[ LICs.Uninverted_Name == selected_language]
    ## 1) L1 Users
    fig = go.Figure(data=go.Choropleth(
                        locations = filtered_data['iso_3'],
                        z = filtered_data["L1_Users"],
                        text = filtered_data['Country_Name'],
                        colorscale = 'Viridis',
                        autocolorscale=False,
                        #reversescale=True,
                        marker_line_color='darkgray',
                        marker_line_width=0.5,
    
                        colorbar_title = "L1_Users" + '<br>Millions',
                    ))

    fig.update_layout(
            #title_text=users_dd,

            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),

            
            margin=dict(b=0, t=0, r=5, l=5),
            mapbox=dict(
                style="carto-positron",
                zoom=1, 
                center_lat = 0,
                center_lon = 0,
                ),
            annotations=[dict(
                                 x=.99,
                                 y=0.01,
                                 xref='paper',
                                 yref='paper',
                                 text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

                                 showarrow=False
                             )]
        )                    
    
    ## 2) Legal status map

    fig_legal = px.choropleth(data_frame= filtered_data.fillna('no data'),
                               locations= 'iso_3', 
                               locationmode="ISO-3",
                               color= 'Function_Label',
                               color_discrete_map={'no data':'grey'},
                               hover_name= "Country_Name",
                               hover_data= ["Function_Label","L1_Users"]
                               #,
                               #                    'Moderate':'Yellow',
                               #                    'Low':'Green'}
                               #scope="usa"
                               )

    fig_legal.update_layout(
            #title_text=users_dd,

            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),

            
            margin=dict(b=0, t=0, r=5, l=5),
            mapbox=dict(
                style="carto-positron",
                zoom=1, 
                center_lat = 0,
                center_lon = 0,
                ),
            annotations=[dict(
                                 x=.99,
                                 y=0.01,
                                 xref='paper',
                                 yref='paper',
                                 text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

                                 showarrow=False
                             )]
        )                    
    
    ## 3) EGIDs by country

    ## Filtering LICs by ISO_639
    #LICs_egid_ordered =  LICs[ LICs.Uninverted_Name == selected_language]

    ## Ordering LICs by egids, to make the legends in order
    LICs_egid_ordered = filtered_data.sort_values("EGIDS")

    # OBS.: This bit is necessary because in pandas 1.5.0 or plotly 5.10 the filtered values stays hiding. This issue makes the px broke.
    # px.bar uses a function get_group that returns all the groups from before ther filter (go figure). Because of this
    # it is need some way to unlink this. This is done by creating a completed unrelated dataframe. I only manage to do this
    # by transforming the dataframe into a dict and them into a dataframe again.
    LICs_egid_ordered = LICs_egid_ordered.to_dict("records")
    
    LICs_egid_ordered = pd.DataFrame(LICs_egid_ordered)

    fig_egids = px.choropleth(data_frame= LICs_egid_ordered.fillna('no data'),
                               locations= 'iso_3', 
                               locationmode="ISO-3",
                               color= 'EGIDS',
                               color_discrete_map={'no data':'grey'},
                               hover_name= "Country_Name",
                               hover_data= ["Function_Label","L1_Users"]
                               #,
                               #                    'Moderate':'Yellow',
                               #                    'Low':'Green'}
                               #scope="usa"
                               )

    fig_egids.update_layout(
            #title_text=users_dd,

            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),

            
            margin=dict(b=0, t=0, r=5, l=5),
            mapbox=dict(
                style="carto-positron",
                zoom=1, 
                center_lat = 0,
                center_lon = 0,
                ),
            annotations=[dict(
                                 x=1,
                                 y=0.01,
                                 xref='paper',
                                 yref='paper',
                                 text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

                                 showarrow=False
                             )]
        )                    
    
    # Tab with 3 maps 
    maps_modal_lang_info = dbc.Tabs([dbc.Tab([dcc.Graph(figure = fig,
                                                        config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                                                                'displaylogo': False}
                                                        )],
                                             label="L1 Users"),
                                     dbc.Tab([dcc.Graph(figure = fig_legal,
                                                        config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                                                                'displaylogo': False}
                                                        )], label="Legal Status"),
                                     dbc.Tab([dcc.Graph(figure = fig_egids,
                                                        config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                                                                'displaylogo': False}
                                                        )], label="EGIDS"),

                                    ],active_tab="tab-0")

    # Tables for modal --------------------------------------------------------------------------------------------------------------------------------------------------

    table_data = filtered_data[['ISO_639', 'Language_Name','Country_Name','Area','All_Users', 'L1_Users','L2_Users','Function_Label','EGIDS']]

    table_modal = dash_table.DataTable(  # id='datatable-interactivity',
        style_header={'whiteSpace': 'normal',
            'height': 'auto',"font-family": "sans-serif",
            'border': '1px solid black',"border-width":" 1px 0px"},
        style_cell={ 'border': '1px solid grey',
                    "font-family": "sans-serif",
                    "border-width":" 1px" },
        style_data={ 'whiteSpace': 'normal','height': 'auto',
                    'border': '1px solid black',"border-width":" 1px 0px","font-family": "sans-serif"},
        columns=[
            #{"name": i, "id": i, "deletable": True, "selectable": True} for i in dls_mapped_data_by_ft2.columns
            {"name": i.replace("_", " "), "id": i,"filter_options" : {"case":"insensitive"}} for i in table_data.columns
        ],
        style_as_list_view=True,
        #data=dls_mapped_data_by_ft.to_dict('records'),
        data=table_data.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        export_format='xlsx',
        export_headers='display',
    )

    return [maps_modal_lang_info, table_modal]


# 3) Static content -----------------------------------------------------------------------------------------------------------------------------------------------------

## 3.1) 3D box different selections -------------------------------------------------------------------------------------------------------------------------------------

fig_3dbox = go.Figure()

dcc.Graph(id = 'box_3d_test',
                     figure = fig_3dbox,config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'],'displaylogo': False})

# 4) Layouts ------------------------------------------------------------------------------------------------------------------------------------------------------------

## 4.1) Cards -----------------------------------------------------------------------------------------------------------------------------------------------------------

card_icon = {
                "color": "white",
                "textAlign": "center",
                "fontSize": 30,
                "margin": "auto",
            }

## 4.2) DLS Category ----------------------------------------------------------------------------------------------------------------------------------------------------
card_DLS_category = dbc.CardGroup([
    dbc.Card(

        dbc.CardBody(
            [
                html.H5("DLS Category", className="card-title",
                        style={'font-size': '1em'}),
                html.Div(
                    id="dls_cat_card"),
                #html.Li(["Total of ", str(len(DLS_all_features.Feature_Name)), " Digital Features Accounted"]),
                #html.Li(["Seven possible classifications based on hierarchical linguistic functions"])

            ], style={'padding': '1.25rem',"max-height":"112px", "minHeight": '7rem',
                      "overflow": "auto"}
        )
    ),
    dbc.Card(
        html.Div(className="fa fa-list",
                 style=card_icon),
        className="bg-primary",
        style={"maxWidth": 75},
    ),
],
    #className=className,
    style={'borderRadius': '5px',
           #'padding-top': '20px',
           'width': '100%',
           "minHeight": "112px"}
)

## 4.3) DLS Rank --------------------------------------------------------------------------------------------------------------------------------------------------------

card_DLS_rank = dbc.CardGroup([
    dbc.Card(

        dbc.CardBody(
            [
                html.H5("DLS Stats", className="card-title",
                        style={'font-size': '1em'}),
                html.Div(id="dls_lvl_card"),
                #html.Li(["Total of ", str(len(DLS_all_features.Feature_Name)), " Digital Features Accounted"]),
                #html.Li(["Seven possible classifications based on hierarchical linguistic functions"])

            ], style={'padding': '1.25rem', "minHeight": '7rem',
                      "overflow": "auto","max-height":"112px"}
        )
    ),
    dbc.Card(
        html.Div(className="fa fa-list-ol",
                 style=card_icon),
        className="bg-primary",
        style={"maxWidth": 75},
    ),
],
    #className=className,
    style={'borderRadius': '5px',
           #'padding-top': '20px',
           'width': '100%',
           "minHeight": "112px"}
)

## 4.4) Modal -----------------------------------------------------------------------------------------------------------------------------------------------------------

modal_lang_info = dbc.Modal([
                            dbc.ModalHeader([
                                dbc.ModalTitle("Language Maps"),
                                dcc.Dropdown(id="selected_language_modal",
                                             style={"width": "250px",
                                                    "padding-left": "10px"})
                                            ]),
                            dbc.ModalBody(html.Div([
                                dbc.Row([
                                    dbc.Col(
                                        [html.Div("Select a Language",id="Language_L1_map")]),
                                    #dbc.Col([html.P("teste")]),
                                ])
                            ])
                            ),
                            dbc.ModalFooter(dbc.Button(
                                "Close", id="close", className="ms-auto", n_clicks=0)),
                            ], id="modal_lang_info", is_open=False, scrollable=True,)

# 5) Page Layout Output ---------------------------------------------------------------------------------------------------------------------------------------------------

first_row = html.Div([
    html.Div(className='row', children=[
        # Search bar
        # html.Div(className='col-md-5 order-1 order-md-0 mt-5 mt-md-0', children=[
        #     html.Div(
        #         className="form-group",
        #         children=[
        #             html.Label("Select Language(s)", className="form-label"),
        #             dcc.Dropdown(options=# [{'label': i, 'value': i } for i in TOLs.Language_Name.unique()  ]
        #                          [{'label': i, 'value': i} for i in DLS_features_by_lang.Reference_Name.unique(
        #                          )],
        #                          value=['Portuguese','Krio'],
        #                          id="selected_language",
        #                          multi=True,
        #                          #clearable= False,
        #                          #disabled= False,
        #                          #className = "mx=2",
        #                          style={
        #                              "width": "250px", "color": "black"}
        #                          ),
        #         ])
        # ]),
        # Second line 
        html.Div(className='row', children=[
            # Two first cards
            html.Div(className='col-lg-9', children=[
                html.Div(className='row', children=[
                    html.Div(className='col-lg-6 col-md-6', children=[
                        dbc.Card(className='mb-3', children=[
                            dbc.CardBody([
                                html.H4(className='fw-semibold mb-4 text-theme', children='DLS Category'),
                                html.Div(id="dls_cat_card"),
                            ]),
                        ]),
                    ]),
                    html.Div(className='col-lg-6 col-md-6', children=[
                        dbc.Card(className='mb-3', children=[
                            dbc.CardBody([
                                html.H4(className='fw-semibold mb-4 text-theme', children='DLS Stats'),
                                html.Div(id="dls_lvl_card"),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
            # Button for modal 
            html.Div(className='col-lg-3 col-md-12',
                     children=[
                         dbc.Button(className='btn btn-hero mt-4 mt-md-0  d-block mx-auto', children=[
                             html.H4(className='mb-0 d-inline-block', children=[
                                 html.I(className='fa-regular fa-eye')
                             ]),
                             "View Language Map",
                             html.Img(src="/assets/images/btn-map.png",
                                      className="img-fluid", alt="csv icon"),
                         ], id="open", n_clicks=0, size="lg", color="primary", outline=True
                         ),
                     ]),
            modal_lang_info,
        ]),
    ]),
], 
className='container pt-md-3'
)

dls_CountryRank = html.Section([
        html.Div(className="card container", children=[
            html.Div(className="card-body", children=[
                # Card title --------------------------------------------------------------------------------------------------------------------------------------------
                dbc.Row([
                    # First Col -----------------------------------------------------------------------------------------------------------------------------------------
                    dbc.Col(className="card-heading d-flex justifyContent-between mb-4 col-md-6",
                            style={"display": "flex","align-items": "center",
                                   "justify-content": "space-between"}, children=[
                        html.H5(className="mb-0 fw-semibold", children=[
                            "Digital Language Support Countries Rank ",
                            # html.I(className="fa-solid fa-circle-info text-muted"),
                            # html.Span(html.Div(className="fa-solid fa-circle-info text-muted"),                            
                        ], style={"margin-left": "12px"}),                        
                        # DropDown Menu -------------------------------------------------------------------------
                        dbc.DropdownMenu([
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.H6("Change axis"),
                                    ],style={"display": "flex","align-items": "center"}),
                                    dbc.Col([
                                        html.Span(html.Div("info", className="export"),
                                                  id='dls_3dbox_popup',
                                                  # style={"textDecoration": "underline", "cursor": "pointer"}
                                                  ),
                                    ],style={"display": "flex","justify-content": "flex-end",
                                             "align-items": "baseline"}),
                                ]),
                                html.Hr(),
                                # Card dropdown menu --------------------------------------------------------------
                                dbc.Row([dbc.Col([html.P("Select x-axis:", style={"margin": "0px"})]),
                                        dbc.Col([dcc.Dropdown(options=[{'label': 'All Users', 'value': 'All'},
                                                                        {'label': 'L1 Users',
                                                                        'value': 'L1'},
                                                                        {'label': 'L2 Users',
                                                                        'value': 'L2'},
                                                                        ],
                                                            value='L1',
                                                            id="3D_box_xaxis",
                                                            multi=False,
                                                            clearable=False,
                                                            disabled=False,
                                                            className="mx=2",
                                                            style={"width": "150px", "color": "black",
                                                                    'display': 'inline', 'float': 'right'})
                                                ])
                                        ], style={"inline": "flex", "align-items": "center", "margin-bottom": "5px"}),
                                # Card dropdown menu 2 --------------------------------------------------------------
                                # GLP, Pop , L1 , L2 , Internet Users, t-index in X
                                dbc.Row([
                                    dbc.Col([html.P("Select z-axis:", style={"margin": "0px"})
                                            ], className="col-lm-6"),
                                    dbc.Col([dcc.Dropdown(options=[{'label': 'DLS total Score', 'value': 'Adjusted_Score'},
                                                                {'label': 'DLS assistant',
                                                                    'value': 'Assistant'},
                                        {'label': 'DLS speech',
                                        'value': "Speech"},
                                        {'label': 'DLS meaning',
                                        'value': 'Meaning'},
                                        {'label': 'DLS localized',
                                        'value': 'Localized'},
                                        {'label': 'DLS surface',
                                        'value': 'Surface'},
                                        {'label': 'DLS content',
                                        'value': 'Content'},
                                        {'label': 'DLS encoding',
                                        'value': 'Encoding'},
                                    ],
                                        value='Adjusted_Score',
                                        id="z_axis",
                                        multi=False,
                                        clearable=False,
                                        disabled=False,
                                        className="mx=2",
                                        style={
                                        "width": "150px", "color": "black", 'display': 'inline', 'float': 'right'}
                                    )], className="col-lm-6"),
                                ], style={"inline": "flex", "align-items": "center", "margin-bottom": "5px"}),
                                # Card dropdown menu 3 ---------------------------------------------------------------
                                dbc.Row([dbc.Col([html.P("Select Colors:", style={"margin": "0px"})]),
                                        dbc.Col([dcc.Dropdown(options=[{'label': 'Continent', 'value': 'Area'},
                                                                        {'label': 'Region',
                                                                        'value': 'Region_Name'},
                                                                        {'label': 'Family',
                                                                        'value': 'Family'},
                                                                        # {'label': 'cluster','value':'cluster'},
                                                                        # {'label':'Latitude','value':'Latitude'},
                                                                        # {'label':'Longitude','value':'Longitude'},
                                                                        # {'label': 'cluster 3x3 testing','value':'cluster_mapping'},
                                                                        # {'label': 'EGIDS 3x3 testing','value':'EGIDS_mapping'}
                                                                        ],
                                                            value='Area',
                                                            id="3D_box_color",
                                                            multi=False,
                                                            clearable=False,
                                                            disabled=False,
                                                            className="mx=2",
                                                            style={"width": "150px", "color": "black", 'display': 'inline', 'float': 'right'})
                                                ])
                                        ], style={"inline": "flex", "align-items": "center", "margin-bottom": "5px"}),                                
                            ], style={"padding": "10px", "width": "330px"})
                        ], label='...', align_end=True,
                            # style={'display': 'inline', 'float': 'right'},
                            style={'display': 'flex','align-items': 'center',
                                    'justify-content': 'space-around' , 'float': 'right'},
                            toggle_class_name="btn btn-theme export",
                            toggle_style={"width": "44px", "borderRadius": "5px",
                                          "display": "flex","align-items": "center",
                                          "justify-content": "space-around"})

                    ]),
                    # Second Col ----------------------------------------------------------------------------------------------------------------------------------------
                    dbc.Col(className='col-md-6 order-1 order-md-0 mt-5 mt-md-0',
                            children=[
                                html.Div(
                                    className="form-group",
                                    children=[
                                        dbc.Row([
                                            dbc.Col([
                                                html.Label("Select Language(s)",
                                                        className="form-label"),
                                            ], className="col-lm-6",
                                                style={"text-align-last": "right"}),
                                            dbc.Col([dcc.Dropdown(options=  # [{'label': i, 'value': i } for i in TOLs.Language_Name.unique()  ]
                                                                [{'label': i, 'value': i} for i in DLS_features_by_lang.Reference_Name.unique(
                                                                )],
                                                                value=[
                                                                    'Portuguese', 'Krio'],
                                                                id="selected_language",
                                                                multi=True,
                                                                # clearable= False,
                                                                # disabled= False,
                                                                # className = "mx=2",
                                                                style={
                                                                    "width": "350px", "color": "black"}
                                                                ),
                                                    ], className="col-lm-6"),
                                        ], style={"margin-top": "0px",
                                                "align-items": "baseline"}),
                                    ])
                            ])
                ]),
                # Card body --------------------------------------------------------------------------------------------------------------------------------------------
                dbc.Row([
                    # 3D plot container -----------------------------------------------------------------------------
                    dbc.Col([                        
                        # 3D plot -----------------------------------------------------------------------------------

                        dcc.Loading(children=[
                            html.Div(id="3D_box_dls_glp_egids",
                                    style={'height': '100%'}),
                            # html.H5(["Selected Language Supported Digital Features"]),
                        ],
                            type="circle",
                            parent_style={'minHeight': 'fit-content', 'display': 'block', 'alignItems': 'center',
                                        'justifyContent': 'center', 'position': 'relative'})
                    ], className="col-lg-6"),
                    # Table -----------------------------------------------------------------------------------------
                    dbc.Col([
                        html.Div(id='dropdown_menu_selection_lang_feat',
                                style={"overflow": "auto"})
                    ], className="col-lg-6")

                ], className="gx-5"),
                dbc.Popover(
                    html.Div(["This graphic contains and 3D scatter plot, where the axis are the DLS score,\
                                                                EGIDS score and the Gross language Product (GLP).",
                            html.Li(["The EGIDS consists of 13 levels with each higher \
                                                                number on the scale representing a greater level of disruption to the \
                                                                intergenerational transmission of the language."]),
                            #   html.Li([ "GLP is an aggregation of the Gross Domestic Product by language. This measure \
                            #   estimates the wealth produced by all L1 speakers of a given language."])
                            html.Li(
                                ["L1 users refer to the number of people using a language as their first language."])
                            ]),
                    # className = 'bg-primary',
                    # style = {'background-color': 'rgb(120, 100, 225)'},
                    target="dls_3dbox_popup",
                    body=True,
                    trigger="hover",
                    placement='top'
                )
            ])
        ])
    ], className="container")

num_DigitalSupportCountry = html.Div(
    className="card",
    children=[
        html.Div(
            className="card-body",
            children=[                
                html.Div(
                    className="row gx-5",
                    children=[
                        
                        dbc.Col([
                            # Title
                            html.Div(
                                className="card-heading d-flex justifyContent-between alignItems-center mb-4",
                                children=[
                                    html.H5(className="mb-0 fw-semibold",
                                            children="Number of Digital Support by Category")
                                ]
                            ),
                            # Plot 
                            dcc.Loading([html.Div(id="features_count_by_type_plot",
                                                  style={'height': '100%'})
                                         ],
                                        type="circle",
                                        parent_style={'minHeight': '400px', 'display': 'block', 'alignItems': 'center',
                                                      'justifyContent': 'center', 'position': 'relative'}
                                        )], className="col-lg-6"),
                        
                        dbc.Col([dcc.Loading(children=[html.Div(id="features_count_by_type_table",
                                                   style={'height': '100%'})
                                          ],
                                type="circle",
                                parent_style={'minHeight': '400px', 'display': 'block', 'alignItems': 'center',
                                              'justifyContent': 'center', 'position': 'relative'}
                                )],className="col-lg-6"),
                    ])
            ])
    ])

dls_ScoreCategory = html.Div(
    className="card",
    children=[
        html.Div(
            className="card-body",
            children=[                
                dbc.Row([
                    dbc.Col([
                        # Title
                        html.Div(
                            className="card-heading d-flex justifyContent-between alignItems-center mb-4",
                            children=[
                                html.H5(className="mb-0 fw-semibold",
                                        children="Adjusted DLS Score by Category")
                            ]
                        ),
                        # Plot 
                        dcc.Loading([html.Div(id="Language_DLS_score_plot",
                                              style={'height': '100%'})
                                     ],
                                    type="circle",
                                    parent_style={'minHeight': '400px', 'display': 'block', 'alignItems': 'center',
                                                  'justifyContent': 'center', 'position': 'relative'}
                                    )], className="col-lg-6"),

                    dbc.Col([dcc.Loading(children=[html.Div(id="Language_DLS_score_table",
                                                            style={'height': '100%'})
                                                   ],
                             type="circle",
                             parent_style={'minHeight': '400px', 'display': 'block', 'alignItems': 'center',
                                           'justifyContent': 'center', 'position': 'relative'}
                                         )], className="col-lg-6")
                ])
            ])
    ])

section2 = html.Section([first_row, num_DigitalSupportCountry, dls_ScoreCategory],
                         className="container")

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
    section2,
    footer
])
