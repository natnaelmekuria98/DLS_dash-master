import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dash_table, dcc, html
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
# from numpy import column_stack
from PIL import Image
import lang_pyramid

from functions import *
from load_data import *

# 1) Setup --------------------------------------------------------------------------------------------------------------------------------------------------------------

card_icon = {
                "color": "white",
                "textAlign": "center",
                "fontSize": 30,
                "margin": "auto",
            }

className = "shadow"        

DLS_level_table_data = DLS_GLP_EGID_data.groupby("DLS_Level").agg(Lang_Count=('Reference_Name', 'count'))

DLS_level_table_data.reset_index(inplace=True)

# define the order of DLS levels
dls_levels_order = ['Still', 'Emerging', 'Ascending', 'Vital', 'Thriving']

# create a categorical data type with the above order
dls_level_cat_dtype = pd.api.types.CategoricalDtype(categories=dls_levels_order, ordered=True)

# convert the 'DLS_Level' column to categorical data type with the above order
DLS_level_table_data['DLS_Level'] = DLS_level_table_data['DLS_Level'].astype(dls_level_cat_dtype)

# sort the DataFrame based on the ordered 'DLS_Level' column
DLS_level_table_data = DLS_level_table_data.sort_values(by='DLS_Level', ascending=False)

DLS_level_table = dash_table.DataTable(
                                       columns=[
                                           # {"name": i, "id": i, "deletable": True, "selectable": True} for i in dls_mapped_data_by_ft2.columns
                                           {"name": i, "id": i, "filter_options" : {"case":"insensitive"}} for i in DLS_level_table_data.columns
                                       ],
                                       style_header={'whiteSpace': 'normal',
                                                     'height': 'auto', "font-family": "sans-serif",
                                                     'border': '1px solid black', "border-width": " 1px 0px"},
                                       style_cell={'border': '1px solid grey',
                                                   "font-family": "sans-serif",
                                                   "border-width": " 1px"},
                                       style_data={'whiteSpace': 'normal', 'height': 'auto',
                                                   'border': '1px solid black', "border-width": " 1px 0px", "font-family": "sans-serif"},
                                       # data=dls_mapped_data_by_ft.to_dict('records'),
                                       data=DLS_level_table_data.to_dict(
                                           'records'),
                                       style_as_list_view=True,
                                    #    filter_action="native",
                                    #    sort_action="native",
                                    #    sort_mode="multi",
                                    #    column_selectable="single",
                                    #    row_selectable="multi",
                                    #    # row_deletable=True,
                                    #    selected_columns=[],
                                    #    selected_rows=[],
                                    #    page_action="native",
                                    #    page_current=0,
                                    #    page_size=9,
                                       export_format='xlsx',
                                       export_headers='display',
                                       )


# 2) Callbacks ----------------------------------------------------------------------------------------------------------------------------------------------------------

## 2.1) interactive figure --------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns'),
)
def update_styles(selected_columns):
    """
    update_styles(selected_columns)
    -------------------------------

    Used to color select columns on data datable.
    OBS.: Not sure if needed might delete this later.

    """
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


## 2.2) Plot Callback --------------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"),
    Input('dropdown_menu', "value"), prevent_initial_call=True)
def update_graphs(rows, derived_virtual_selected_rows,value):
    """
    update_graphs(rows, derived_virtual_selected_rows,value)
    --------------------------------------------------------

    Return plotly bar plot. This graph uses code that make it interactive,
    is possible to select a row and see the row on the graph. 

    When the table is first rendered, `derived_virtual_data` and
    `derived_virtual_selected_rows` will be `None`. This is due to an
    idiosyncrasy in Dash (unsupplied properties are always None and Dash
    calls the dependent callbacks when the component is first rendered).
    So, if `rows` is `None`, then the component was just rendered
    and its value will be the same as the component's dataframe.
    Instead of setting `None` in here, you could also set
    `derived_virtual_data=df.to_rows('dict')` when you initialize
    the component.

    OBS.: Don't know if the interactivity is desired. Leaving it here
    in case it is used. Might remove it later.

    Parameters
    ----------
    rows: list
        Rows from table. This is need in case any of the row
        is deleted.
    derived_virtual_selected_rows: list
        Selected rows from table (id = datatable-interactivity, see update_data).
        Used to color the data in the plot
    value:str
        Dropdown menu value, used to change the data being displayed

    Returns
    -------
    dash.dcc.Graph.Graph
        Returns a barplot about some DLS counting by scope.

    
    """
    
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    #DLS_all_features
    y_legend_dict = {"Feature_Name":-.85,"Reference_Name":-1,"Support_Category":-.2}
    #dff = dls_mapped_data_by_ft if rows is None else pd.DataFrame(rows)

    dff = DLS_all_features if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#FD841F'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff[value],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 370,
                    "margin": {"t": 10,"b": 100, "l": 10, "r": 10},
                    # "images":[dict(
                    #     #source="assets/images/logo/derivation-logo.png",#\assets\images\logo
                    #     source=Image.open("assets/images/logo/derivation-logo.png"),
                    #     xref="paper", yref="paper",
                    #     x=0.98, y=0.765,
                    #     sizex=0.2, sizey=0.2,
                    #     xanchor="right", yanchor="bottom"
                    # )],
                    "annotations" : [dict(
                        x=1,
                        y=y_legend_dict[value],
                        xref='paper',
                        yref='paper',
                        text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

                        showarrow = False
                    )]
                },
            },config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'],'displaylogo': False}
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["counts"] if column in dff
    ]


## 2.3) Table callback --------------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output('dropdown_menu_selection', 'children'),
    Input('dropdown_menu', 'value'))
def update_data(dropdown_menu):
    """
    update_data(dropdown_menu)
    --------------------------

    Given a selected scope this callback returns a datatable with the
    selected grouping. For example, if Count of language supported by feature 
    is selected the table will show the count by Feature_Name.

    Parameters
    ----------
    dropdown_menu: str
        Name of the column for the data groupping.

    Returns
    -------
    dash.dash_table.DataTable.DataTable
        A table with the data.

    """

    #dls_mapped_data_by_ft2 =  dls_mapped_data.groupby(dropdown_menu).count().iloc[:,0].reset_index(name='counts').sort_values("counts",ascending = False)
    dls_mapped_data_by_ft2 =  DLS_features_by_lang.groupby(dropdown_menu).count().iloc[:,0].reset_index(name='counts').sort_values("counts",ascending = False)


    #columns =  [{"name": i, "id": i,} for i in (dls_mapped_data_by_ft2.columns)]

    return [
        dash_table.DataTable(id='datatable-interactivity',
                             columns=[
                                 #{"name": i, "id": i, "deletable": True, "selectable": True} for i in dls_mapped_data_by_ft2.columns
                                 {"name": i, "id": i,"filter_options" : {"case":"insensitive"}} for i in dls_mapped_data_by_ft2.columns
                             ],
                             style_header={'whiteSpace': 'normal',
                                           'height': 'auto', "font-family": "sans-serif",
                                           'border': '1px solid black', "border-width": " 1px 0px"},
                             style_cell={'border': '1px solid grey',
                                         "font-family": "sans-serif",
                                         "border-width": " 1px"},
                             style_data={'whiteSpace': 'normal', 'height': 'auto',
                                         'border': '1px solid black', "border-width": " 1px 0px", "font-family": "sans-serif"},
                             #data=dls_mapped_data_by_ft.to_dict('records'),
                             data=dls_mapped_data_by_ft2.to_dict('records'),
                             style_as_list_view=True,
                             filter_action="native",
                             sort_action="native",
                             sort_mode="multi",
                             column_selectable="single",
                             row_selectable="multi",
                             #row_deletable=True,
                             selected_columns=[],
                             selected_rows=[],
                             page_action="native",
                             page_current=0,
                             page_size=9,
                             export_format='xlsx',
                             export_headers='display',
                             )
    ]

## 2.4) Bulk data download -----------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output("download-databulk-csv", "data"),
    Input("btn_bulk_csv", "n_clicks"),
    prevent_initial_call=True,
)
def download_dls_bulk(n_clicks):
    """
    func(n_clicks)
    --------------

    Callback to operate button for downloading bulk DLS data.

    Parameters
    ----------
    n_clicks: int
        counts number of clicks, only used to trigger the callback

    Returns
    -------
    dict
        Dash function to download data on browsers

    """
    #return dcc.send_data_frame(DLS_scores_by_lang.to_csv, "DLS_all_scores.csv")
    return dcc.send_file("./data/DLS_2021/DLS_2021.zip")

## 2.5) DLS level Pie charts ---------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output("dls-level-piecharts","children"),
    Input("dropdown-menu-dls-level","value")
)
def update_dls_lvl_charts_table(scope):
    """
    update_dls_lvl_charts_table(scope)
    ----------------------------------

    Update pie chart given a selected scope (DLS Level langugage count (Lang_Count) or
    DLS level population count (L1_Users) ).

    Parameters
    ----------
    scope: str
        Scope to define the data analysed. Two possible values (DLS Level langugage count (Lang_Count) or
        DLS level population count (L1_Users) )

    Returns
    -------
    dbc._components.Tabs.Tabs
        dbc tabs with two tabs where one is a pie chart and the second is a table with the data from the chart.

    """

    DLS_level_dist = DLS_GLP_EGID_data.groupby("DLS_Level").agg(L1_Users=('L1', 'sum'), Lang_Count=('Reference_Name', 'count'))

    DLS_level_dist = DLS_level_dist.reset_index()

    fig_pie = px.pie(DLS_level_dist,values=scope,names="DLS_Level",color = "DLS_Level",
                    # color_discrete_map={'Still':'orange',
                    #                     'Emerging':'purple',
                    #                     'Ascending':'green',
                    #                     'Vital':'red',
                    #                     'Thriving':'blue'}
                                        )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label+value')
    fig_pie.update_layout(
        #title_text=users_dd,
        # images=[dict(
        #     #source="assets/images/logo/derivation-logo.png",#\assets\images\logo
        #     source=Image.open("assets/images/logo/derivation-logo.png"),
        #     xref="paper", yref="paper",
        #     x=1.2, y=0.065,
        #     sizex=0.2, sizey=0.2,
        #     xanchor="right", yanchor="bottom"
        #     )],
        annotations = [dict(
            x=1.2,
            y=0,
            xref='paper',
            yref='paper',
            text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

            showarrow = False
        )],
        margin=dict(b=20, t=20, r=5, l=5),
        )

    # Table -------------------
    
    table = dash_table.DataTable(  # id='datatable-interactivity',
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
            {"name": i.replace("_", " "), "id": i,"filter_options" : {"case":"insensitive"}} for i in DLS_level_dist.columns
        ],

        #data=dls_mapped_data_by_ft.to_dict('records'),
        data=DLS_level_dist.to_dict('records'),
        style_as_list_view=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        export_format='xlsx',
        export_headers='display',
    )
    return [
     dbc.Tabs([
            dbc.Tab([
                dcc.Graph(figure=fig_pie,style = {'height': '370px'},
                    config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'],'displaylogo': False})
                    ],label="Figure"), 
            dbc.Tab([table],label="Table")
                        ],active_tab = "tab-0") 
    ]

## 2.6) Modal handler ------------------------------------------------------------------------------------------------------------------------------------------------------
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

callback(
    Output("modal-dls-info-3", "is_open"),
    [Input("open_dls_info-3", "n_clicks"), Input("close-body-scroll-dls", "n_clicks")],
    State("modal-dls-info-3", "is_open"),
)(toggle_modal)

# 3) Static content -----------------------------------------------------------------------------------------------------------------------------------------------------

## 3.1) Map -------------------------------------------------------------------------------------------------------------------------------------------------------------

# Code for world map with DLS by contry.
# No Callback is need.

LICs_temp = LICs[["Country_Code","iso_3","Country_Name","Area",
                  "Language_Name","ISO_639","L1_percentage_of_country_L1"]]

LICs_DLS = LICs_temp.merge(DLS_scores_by_lang[["ISO_639","Adjusted_Score"]],
                           how = "left", on ="ISO_639")

LICs_DLS['L1_weighted_score'] = LICs_DLS['L1_percentage_of_country_L1'] * LICs_DLS["Adjusted_Score"]

temp = LICs_DLS.groupby(["iso_3","Country_Name"]).sum(numeric_only=True)[['L1_weighted_score']]
temp.reset_index(inplace=True)

fig = go.Figure(data=go.Choropleth(
    locations=temp['iso_3'],
    z=temp['L1_weighted_score'],
    text=temp['Country_Name'],
    #colorscale = 'Viridis',
    colorscale=[[0, 'rgb(204, 0, 102)'],
                [.5, 'rgb(255, 255, 153)'],
                [1, 'rgb(0, 153, 51)']],
    autocolorscale=False,
    #reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,

    colorbar_title='DLS by country',
    colorbar_orientation='h',
    colorbar_thickness=10,
    colorbar_xpad=30,
    colorbar_y=-.12
))

fig.update_layout(
    #title_text=users_dd,
    # images=[dict(
    #     #source="assets/images/logo/derivation-logo.png",#\assets\images\logo
    #     source=Image.open("assets/images/logo/derivation-logo.png"),
    #     xref="paper", yref="paper",
    #     x=0.98, y=0.065,
    #     sizex=0.2, sizey=0.2,
    #     xanchor="right", yanchor="bottom"
    #   )],
    annotations=[dict(
        x=1,
        y=0,
        xref='paper',
        yref='paper',
        text='Source:© 2022, all rights reserved, <a href="https://derivation.co/">Derivation.co</a>',

        showarrow=False
    )],

    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),


    margin=dict(b=0, t=0, r=5, l=5),
    mapbox=dict(
        style="carto-positron",
        zoom=1,
        center_lat=0,
        center_lon=0,
    ),
)
# fig.data[0].colorbar.y=-0.2
# fig.show()
# save svg fig.write_image("DLS_world_map_v2.svg",width = 900, height = 400)

temp["Rank"] = temp["L1_weighted_score"].rank(ascending=False,method="min")

columns = [
    {'name': 'iso 3', 'id': 'iso_3'},
    {'name': 'Country Name', 'id': 'Country_Name',"filter_options" : {"case":"insensitive"}},
    {'name': 'L1 weighted score', 'id': 'L1_weighted_score',"type":'numeric', 'format':Format(precision=2, scheme=Scheme.fixed),
     "filter_options" : {"case":"insensitive"}}
    ]


country_table = dash_table.DataTable(  id='datatable-dls-countries-rank',
    # columns=[
    #     #{"name": i, "id": i, "deletable": True, "selectable": True} for i in dls_mapped_data_by_ft2.columns
    #     {"name": i, "id": i, "deletable": False, "selectable": False} for i in temp.columns
    # ],
    columns = columns,
    #data=dls_mapped_data_by_ft.to_dict('records'),
    data=temp.sort_values(by=['L1_weighted_score'],
                          ascending=False).to_dict('records'),
    style_header={'whiteSpace': 'normal',
                  'height': 'auto', "font-family": "sans-serif",
                  'border': '1px solid black', "border-width": " 1px 0px"},
    style_cell={'border': '1px solid grey',
                "font-family": "sans-serif",
                "border-width": " 1px"},
    style_data={'whiteSpace': 'normal', 'height': 'auto',
                'border': '1px solid black', "border-width": " 1px 0px", "font-family": "sans-serif"},
    filter_action="native",
    filter_options= {
        'case': 'insensitive'
    },
    sort_action="native",
    sort_mode="multi",
    style_as_list_view=True,
    column_selectable="single",
    page_action="native",
    page_current=0,
    page_size=10,
    export_format='xlsx',
    export_headers='display',
)

## 3.2) S-Curve ---------------------------------------------------------------------------------------------------------------------------------------------------------

# DLS_scores_by_lang[['Proportional_Score','Rank','DLS_Level']]

# DLS_scores_by_lang = pd.read_csv('DLS_scores_by_lang.csv')

# Transform Rank column
x = 1 - np.log(DLS_scores_by_lang['Rank'])

# Normalize x
x_norm = (x - x.min()) / (x.max() - x.min())

# Define logistic function
# def logistic_func(x, L, k, x0):
#     return L / (1 + np.exp(-k * (x - x0)))
# from scipy.optimize import curve_fit
# # Fit logistic curve regression
# popt, pcov = curve_fit(logistic_func, x_norm, DLS_scores_by_lang['Proportional_Score'])

# Create plot
fig_SCurve = px.scatter(DLS_scores_by_lang, x=x_norm, 
                        y='Proportional_Score',
                        color='DLS_Level',
                        labels={'x': '1 - log(Rank)', 'Proportional_Score': 'Proportional Rank'})
fig_SCurve.update_layout(xaxis_range=[0, 1], 
                         legend=dict(x=0.5, y=0.04, bgcolor='rgba(0,0,0,0)',                                     
                                    font=dict(size=12),title="DLS Level"),
                         margin=dict(r=0,l=0,t=0,b=0))
# fig.add_trace(px.line(x=np.linspace(0, 1, 100), y=logistic_func(np.linspace(0, 1, 100), *popt)).data[0])

# # Sample data
# df = pd.DataFrame({'Proportional_Score': np.random.rand(100),
#                    'Rank': np.arange(1, 101),
#                    'DLS_Level': np.random.choice(['Still', 'Emerging', 'Ascending', 'Vital', 'Thriving'], 100)})

# # Create the scatter plot
# fig = px.scatter(DLS_scores_by_lang[['Proportional_Score','Rank','DLS_Level']], x=1-np.log(DLS_scores_by_lang[['Proportional_Score','Rank','DLS_Level']]['Rank']), y='Proportional_Score', color='DLS_Level')

# # Update the x-axis title
# fig.update_xaxes(title='1 - log(Rank)')

# Show the plot


# 4) Layouts ------------------------------------------------------------------------------------------------------------------------------------------------------------
## 4.1) Cards --------------------------------------------------------------------------------------------------------------------------------------------------------------

card_DLS_stats = dbc.CardGroup([
    dbc.Card(
            dbc.CardBody(
                [
                    html.H5("DLS Stats", className="card-title",
                            style={'font-size': '1em'}),
                    html.Li([len(DLS_scores_by_lang.ISO_639.unique()), " Languages Scores"]),
                    html.Li([str(len(DLS_all_features.Feature_Name)), " Digital Features"]),
                    #html.Li(["Seven possible classifications based on hierarchical linguistic functions"])

                ], style={'padding': '1.25rem', "minHeight": '7rem'}
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
        style={'border-radius': '5px',
            #'padding-top': '20px',
            'width': '100%',
            "min-height": "112px"}
    )

card_DLS_planned_features = dbc.CardGroup([
    dbc.Card(
        dbc.CardBody(
            [
                html.H5("Planned DLS features", className="card-title",
                        style={'font-size': '1em'}),
                html.Li(
                    ["Addition of ~400 new digital features"]),
                html.Li(
                    ["Weekly DLS update"]),

            ], style={'padding': '1.25rem', "minHeight": '7rem'}
        )
    ),
    dbc.Card(
        html.Div(
            className="fa fa-search-plus", style=card_icon),
        className="bg-primary",
        style={"maxWidth": 75},
    ),
],
    #className=className,
    style={'border-radius': '5px',
           'padding-top': '20px',
           'width': '100%',
           "min-height": "145px"}
)

## 4.2) Modal --------------------------------------------------------------------------------------------------------------------------------------------------------------

span_style={"textDecoration": "underline", "cursor": "pointer", "color": "#0a58ca"}

modal_dls_info_text = html.Div([
    # a) First Paragraph -------------------------------------------------------------------------------------------------------------------
    # html.P(["Digital language support (DLS) is a scale that ranks each language's level of support by digital technologies.\
    #          Briefly, the DLS is calculated by accounting for the number of digital technologies that support each \
    #          language. After collecting this data, we conduct a Mokken scale analysis ",
    #         html.Span("Mokken Scale analysis",
    #                   id="mokken_info", style=span_style),
    #         ". Abbey Thomas and Gary Simons from ",
    #         html.A("SIL international",
    #                href='https://www.sil.org/', target="_blank"),
    #         " developed this method for DLS settings."
    #         ], style={'text-indent': '40px'}),


    html.P(["Digital language support (DLS) serves as a valuable tool for evaluating and comparing the level of digital support provided to each language, ultimately contributing to a more inclusive and accessible digital landscape worldwide. Essentially, this assessment is based on a comprehensive analysis that takes into account the multitude of digital resources available for each language. By quantifying the number of digital technologies catering to specific languages, the DLS is then able to provide an objective measure of the digital support available. This development in the field of Linguistics is the pioneering work of Abbey Thomas and Gary Simons from ",
    html.A("SIL International", href='https://www.sil.org/', target="_blank"),
    ". This is then followed by a Mokken scale analysis ",
    html.Span("Mokken Scale analysis", id="mokken_info", style=span_style),
    "."
    ], style={'text-indent': '40px'}),

    # a.1) Mokken popover ------------------------------------------------------------------------------------------------------------------
    dbc.Popover(
        html.Div(["\"Mokken scaling techniques are a useful tool for researchers who wish to construct\
                   unidimensional tests or use questionnaires that comprise multiple binary or polytomous items. \
                   The stochastic cumulative scaling model offered by this approach is ideally suited when the \
                   intention is to score an underlying latent trait by simple addition of the item response values.\" ",
                  html.A("Stoch, Jones, Croudace (2012)",
                         href='https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-12-74',
                         target="_blank"),
                  ], style={"text-align": "justify"}),
        #style = { "inset": "-24px auto auto 268px !important"},
        #offset="200,200",
        id="mokken_dls_info_popover",
        target="mokken_info",
        body=True,
        trigger="hover",
        placement='right'
    ),
    # b) Second paragraph ------------------------------------------------------------------------------------------------------------------
    # html.P(["The current version takes into account 143 unique digital technologies. The procedure for creating the\
    #          scale divides these technologies into seven categories, These constructed classes represent different linguistic functions (",
    #         html.Span("encoding", id="Encoding_info",  style=span_style), ", ",
    #         html.Span("content", id="Content_info",  style=span_style), ", ",
    #         html.Span("surface", id="Surface_info",  style=span_style), ", ",
    #         html.Span("localized", id="Localized_info",
    #                   style=span_style), ", ",
    #         html.Span("meaning", id="Meaning_info",  style=span_style), ", ",
    #         html.Span("speech", id="Speech_info",  style=span_style), ", ",
    #         html.Span("assistant", id="Assistant_info",
    #                   style=span_style), ".",

    #         # Attemp to make the Span above automatic, like the popoover below... failed :( ... Test it later
    #         #html.Div([make_span_dls_class(classification)[0] for classification in dls_class_descr["class"].to_list() ]),".",

    #         "). These types have four levels, each representing a different count of softwares supports in the category ( See ",
    #         html.Span('Table', id="threshold_info", style=span_style), "). The level of support in a category ( 1,2,3,4 ) is the category's language score."],
    #        style={'text-indent': '40px'}),
    html.P([
        "The Digital Language Support Scale (DLS) encompasses an extensive range of 143 distinct digital technologies. "
        "It incorporates a refined procedure that classifies these technologies into seven distinct categories, each representing specific linguistic functions, namely; ",
        html.Span("encoding", id="Encoding_info", style=span_style), ", ",
        html.Span("content", id="Content_info", style=span_style), ", ",
        html.Span("surface", id="Surface_info", style=span_style), ", ",
        html.Span("localized", id="Localized_info", style=span_style), ", ",
        html.Span("meaning", id="Meaning_info", style=span_style), ", ",
        html.Span("speech", id="Speech_info", style=span_style), ", and ",
        html.Span("assistant", id="Assistant_info", style=span_style), "). "
        "Within each category, the DLS further distinguishes between four levels of support, denoting different counts of software support available (See ",
        html.Span('Table', id="threshold_info", style=span_style), "). "
        "The level of support in a category ( 1,2,3,4 ) is the category's language score."
    ], style={'text-indent': '40px'}),

    # b.1) Classes popover and table -------------------------------------------------------------------------------------------------------

    ## b.1.1)Creates each class popover
    html.Div([make_popover_dls_class(classification)[
        0] for classification in dls_class_descr["class"].to_list()]),

    ## b.1.2)Table popover  - table classification_count_thresholds
    html.Div([
        dbc.Popover([
            dcc.Markdown("""
                     ### Digital Tecnhologies Category Count Threshold
                         
                     &nbsp Here is the table showing how is the partition of individual categories. 
                     Each category has four bins, representing different quantiles (25%, 50%, 75%, 100%) 
                     of how much technologies support a given language. For example, 
                     If a language has five speech software supports, this language has the support of speech level 2.
                         
                     """),
            dbc.Tabs([make_table_dls_thresholds(name)[0] for name in list(dls_class_threshold.support_level.unique())],
                     id="card-dls-threshold-table2",
                     )
        ], style={'max-width': '400px'},
            target='threshold_info', body=True, trigger="hover")]),

    # c) Third paragraph -------------------------------------------------------------------------------------------------------------------
    # html.P(["In Mokken analysis, these items need some attributes to ensure a proper Mokken scale. These properties are ",
    #         html.Span('Homogeneity', id="homogeneity_info",
    #                   style=span_style), ', ',
    #         html.Span('Monotonicity', id="monotonicity_info",
    #                   style=span_style), ', ',
    #         html.Span('Stochastic independence',
    #                   id="stoch_ind_info", style=span_style),
    #         ". Therefore, it is necessary to check these assumptions in the data constructed ( Content 1,\
    #                                      Content 2, etc.) ( See each property tooltip above)."],
    #        style={'text-indent': '40px'}),
    html.P([
        "In the realm of Mokken analysis, the construction of a reliable and valid Mokken scale necessitates the consideration of specific attributes associated with the items under investigation. These attributes, namely ",
        html.Span('Homogeneity', id="homogeneity_info", style=span_style),
        ", ",
        html.Span('Monotonicity', id="monotonicity_info", style=span_style),
        ", and ",
        html.Span('Locally Stochastic Independence',
                  id="stoch_ind_info", style=span_style),
        ", play a pivotal role in ensuring the accuracy and integrity of the scale. Therefore, it is essential to assess these assumptions within the data being examined, specifically the items labeled as Content 1, Content 2, and so forth (See each property tooltip above)."
    ], style={'text-indent': '40px'}),
    html.Br(),
    # c.1) Data Suppositions Popover -------------------------------------------------------------------------------------------------------

    ## c.1.1) Homogeneity ------------------------------------------------------------------------------------------------------------------

    dbc.Popover([
        dcc.Markdown("""
                     ### Homogeneity
                     ( -- this needs changes --)
                     &nbsp This desired quality of the data guarantees that the items' difficulty can order the **DLS scale** 
                     (**Encoding 1**, **Encoding 2**, etc.). For example, suppose English has "**Encoding 4**" (i.e., more than four 
                     encoding digital support ( see Table ). With that, it is expected that this language has more probability 
                     of having a higher **DLS score** than those that do not have this encoding level. The test that assesses 
                     this quality is **Loevinger's Coefficient of Homogeneity**. Below we see the results for each category. 
                     **H** values **above  0.5** indicate a robust scale.
                       
                     """, style={"text-align": "justify"}),
        dash_table.DataTable([{"category": "assistant",
                               "Hi": 0.987},
                              {"category": "speech",
                               "Hi": 0.942},
                              {"category": "meaning",
                               "Hi": 0.920},
                              {"category": "localized",
                               "Hi": 0.924},
                              {"category": "surface",
                               "Hi": 0.885}, 
                              {"category": "encoding",
                               "Hi": 0.707},
                              {"category": "content",
                               "Hi": 0.685},
                              ],

                             columns=[{"name": "category", "id": "category"},
                                      {"name": "Hi", "id": "Hi", "type": "numeric", "format": Format(precision=2, scheme=Scheme.fixed)}],
                             style_as_list_view=True,
                             
            style_header={'whiteSpace': 'normal',
                          'height': 'auto', "font-family": "sans-serif",
                          'border': '1px solid black', "border-width": " 1px 0px"},
            style_cell={'border': '1px solid grey',
                        "font-family": "sans-serif",
                        "border-width": " 1px"},
            style_data={'whiteSpace': 'normal', 'height': 'auto',
                        'border': '1px solid black', "border-width": " 1px 0px", "font-family": "sans-serif"},
                             export_format='xlsx',
                             export_headers='display',)

    ],
        #style = {'background-color': 'rgb(120, 100, 225)'},
        target="homogeneity_info",
        body=True,
        trigger="hover"
    ),

    ## c.1.2) Monotonicity -----------------------------------------------------------------------------------------------------------------

    dbc.Popover([
        dbc.Row([
            # First Col --------------------------------------------------------------------------------------------------
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(
                        dcc.Markdown("""
                                     ### Monotonicity

                                     &nbsp The Mokken analysis assesses an unobserved subject trait (Language's digital support). The caveat is that
                                     the evaluation is based on the response of the observed ones (the item classifications). Because we are estimating 
                                     a unidimensional **ordered** variable from a binary one, it is required to verify that the probability of having 
                                     one item increases when the language has all the other traits. This is needed to guarantee that our scale is always 
                                     crescent with a positive answer in a given item. For example, suppose the Chinese language is level 3 on the surface,
                                     then we should expect that Spanish, that is, surface 4, has a higher total score.
                                     """, style={"text-align": "justify"}),
                        label="1", tab_id="1"),
                    dbc.Tab(
                        dcc.Markdown("""
                                     &nbsp So we need an estimation for an item adjusted score ( -- add definition -- ) given a Restscore ( Sum of all 
                                     language scores subtracting less the score of the evaluated item ). The estimation process fits a logistic regression 
                                     where restcore would explain an item response. If the result is a non-decreasing curve, one can check the monotonicity
                                     of the data. The keyword here is probability. There are individual cases where this monotonicity does not hold, we can 
                                     see this on the plots, but they are too far between to influence our logistic fit.
                                     
                                     &nbsp On the x-axis is the overall score of a
                                     given language. The y-axis is an item's adjusted score ( -- add definition -- ).
                                     """, style={"text-align": "justify"}),
                        label="2", tab_id="2")
                ],
                    id="card-dls-threshold-table-monotonicity",
                    active_tab="1",
                )
            ]),

            # IRF plot ---------------------------------------------------------------------------------------------------
            dbc.Col([
                # Radio buttons group ------------------------------------------------------------------------------

                dbc.RadioItems(
                    id="irf_radio_info",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": "encoding",
                         "value": "encoding"},
                        {"label": "content",
                         "value": "content"},
                        {"label": "localized",
                         "value": "localized"},
                        {"label": "surface",
                         "value": "surface"},
                        {"label": "meaning",
                         "value": "meaning"},
                        {"label": "speech",
                         "value": "speech"},
                        {"label": "assistant",
                         "value": "assistant"}
                    ],
                    value="encoding",
                ),

                # Item response function curves --------------------------------------------------------------------
                #html.Div(id="output_irf")
                ### Loading circle and map plot (id = "datatable-interactivity-map-container" ) --------------------
                dcc.Loading(children=[html.Div(id="output_irf")],
                            type="circle", style={'padding': '2'})
            ])
            #make_irf_plot("encoding")[0]
        ], style={"display": "grid", "grid-template-columns": "300px 800px"})

    ],
        id="monotonicity_popover",
        style={'max-width': '1100px'},
        target="monotonicity_info",
        body=True,
        trigger="hover"
    ),

    ## c.1.3) Stochastic independece -------------------------------------------------------------------------------------------------------

    dbc.Popover([
        #dbc.Row([
        # First paragraph --------------------------------------------------------------------------------------------
        dcc.Markdown("""
                     ###  Locally independence              
 
                     Local independence in Mokken analysis refers to the assumption that item responses are independent of each other,\
                     conditional on the underlying latent trait being measured. It implies that once the latent trait is considered, there \
                     should be no systematic relationship or correlation between item responses. Assessing local independence helps ensure \
                     that the items in the scale are measuring distinct aspects of the construct without any unwanted dependencies.

                     """, style={"text-align": "justify"}),


        ## IRF plot ---------------------------------------------------------------------------------------------------
        #dbc.Col([

        #          # Item response function curves --------------------------------------------------------------------
        #          #html.Div(id="output_irf")
        #          ### Loading circle and map plot (id = "datatable-interactivity-map-container" ) --------------------
        #          dcc.Loading(children=[html.Div(id="output_irf")],
        #                      type="circle",style={'padding': '2'})
        #         ])
        ##make_irf_plot("encoding")[0]
        #], style = {"display":"grid" , "grid-template-columns": "300px 800px"})

    ],
        id="stoch_ind_popover",
        #style = {'max-width': '1100px'},
        target="stoch_ind_info",
        body=True,
        trigger="hover"
    ),

    # d) Fourth Paragraph ------------------------------------------------------------------------------------------------------------------
    # html.H4("Final Score"),
    # #html.Br(),
    # html.P(["Once these constructed items are tested, further processing needs to be done on the data. (--bad line--) Although\
    #                                      we already measured the level of support a language has, using the sum of the individual score could be problematic. (--bad line--)"],
    #        style={"text-indent": "40px"}),

    # html.P(["To illustrate that, let's suppose that the English language has an assistant level of 4 (i.e., three content technologies\
    #          support, see table ) but has level one in all other support. With that, the English language has a rest score equal to 6. Suppose\
    #          that it is uncommon for a language to have a rest score (-- insert definition --) of 6 and an assistant level of 4. Due to the\
    #          monotonicity (-- insert definition --), we can treat this as a statistical fluke. And with that, we can weigh an item value by \
    #          the ratio of languages with the same rest score and item response. "],
    #        style={"text-indent": "40px"}),
    # #html.Br(),
    # # e) Fifth Paragraph -------------------------------------------------------------------------------------------------------------------
    # html.P(["So if only one in 100 ( number of languages with an assistant level of 3 ) languages has an \
    #          assistant level of 3 and 0 rest score, its adjusted item score would be 3 x (1 / 100). \
    #          Thus, the sum gives us the adjusted score of a language."], style={"text-indent": "40px"}),
    html.H4("Final Score"),
    html.P(
        [
            "Once the constructed items have undergone testing, additional data processing steps are required. "
            "However, it is important to address certain considerations to ensure accurate interpretation and avoid potential issues. "
            "In particular, the conventional approach of summing individual scores to measure the level of support for a language "
            "can be problematic and may require careful handling."
        ],
        style={"text-indent": "40px"},
    ),
    html.P(
        [
            "To exemplify this point, let's consider the English language as an example. "
            "Suppose that the English language has an assistant level of 4, indicating strong support in three content technologies "
            "(as indicated in the table). Consequently, the English language obtains a rest score of 6, which is calculated "
            "based on the sum of individual scores. It is worth noting that a rest score of 6 combined with an assistant level of 4 "
            "is an uncommon combination. Such an occurrence is statistically unusual and can be considered a statistical anomaly "
            "due to the property of monotonicity, which asserts that the likelihood of endorsing an item positively should increase "
            "with the underlying trait being measured. To address this issue, one approach is to assign a weighted value to each item "
            "based on the ratio of languages that share the same rest score and item response."
        ],
        style={"text-indent": "40px"},
    ),
    html.P(
        [
            "To further illustrate this concept, let's consider a scenario where only one out of 100 languages has an assistant level of 3 "
            "and a rest score of 0. In this case, we can calculate the adjusted item score for this particular combination as "
            "3 multiplied by the ratio of languages with the same rest score and item response, which is 1 divided by 100. "
            "Therefore, the adjusted item score would be 3 x (1 / 100). By applying this adjustment to each relevant combination, "
            "we can obtain the adjusted scores for different languages. Summing up these adjusted scores provides us with the overall "
            "adjusted score of a language. This approach allows us to account for the rarity of certain combinations and ensure "
            "a more accurate representation of the level of support for a given language."
        ],
        style={"text-indent": "40px"},
    ),
    
    html.Br(),
    # f) Sixth Paragraph -------------------------------------------------------------------------------------------------------------------
    html.H4("Clustering"),
    #html.Br(),
    # html.P(["The adjusted score is the final measure of the support level. There is some further handling\
    #          to make it to a more intuitive scale."], style={"text-indent": "40px"})

    html.P(["The adjusted score serves as the final measure of the support level, indicating the overall level of assistance provided by a language. ",
            "However, to enhance its interpretability and ensure a more intuitive scale, additional adjustments can be applied. ",
            "By refining the scale, the adjusted score becomes more intuitive, enabling users to readily comprehend and compare the levels of support provided by various languages. ",
            "This additional handling ensures that the measure is more user-friendly and effectively conveys the relative differences in support levels."
            ],style={"text-indent": "40px"}),
],style = {"text-align": "justify"})

# 5) Page Layout Output -------------------------------------------------------------------------------------------------------------------------------------------------

## 5.1) First row (navbar) ----------------------------------------------------------------------------------------------------------------------------------------------
first_row = html.Div([
    # 1 - Row -----------------------------------------------------------------------------------------------
    html.Div([
        # 1.1 - Col -----------------------------------------------------------------------------------------
        html.Div([
            # 1.1.1 Row -------------------------------------------------------------------------------------
            html.Div([
                # 1.1.1.1 Col -------------------------------------------------------------------------------
                html.Div([
                    html.Div([
                        html.H2("7829"),
                        html.H5("Languages Scores")
                    ], className="banner-info")
                ], className="col-6 border-end"),
                # 1.1.1.2 Col -------------------------------------------------------------------------------
                html.Div([
                    html.Div([
                        html.H2("143"),
                        html.H5("Digital Features")
                    ], className="banner-info")
                ], className="col-6")
            ], className="row mb-2 text-center"),
            # Button ----------------------------------------------------------------------------------------
            html.Button([
                html.H4([html.I(
                    className="fa-solid fa-download me-2")
                ], className="mb-0 d-inline-block"),
                "DLS Bulk Data CSV",
                html.Img(src="/assets/images/csv-file.png",
                             className="img-fluid",
                             alt="csv icon")
            ], id="btn_bulk_csv",
                className="btn btn-hero mt-4 d-block mx-auto"),
            dcc.Download(id="download-databulk-csv"),
        ], className="col-md-5 order-1 order-md-0 mt-5 mt-md-0"),
        # 1.2 - Col -----------------------------------------------------------------------------------------
        html.Div([
            # Card ------------------------------------------------------------------------------------------
            html.Div(
                # Card Title ---------------------------------------------------------------------------------
                [html.H5(["About Digital Language Support"],
                         className="fw-semibold mb-4"),
                 # Card Text ---------------------------------------------------------------------------------
                 html.P(["Digital language support (DLS) is a scale that ranks each \
                        language's level of support by digital technologies. Briefly, \
                        the DLS is calculated by accounting for the number of digital \
                        technologies that support each language. After collecting this \
                        data, we conduct a Mokken scale analysis Mokken Scale analysis. \
                        Abbey Thomas and Gary Simons from SIL international developed \
                        this method for DLS settings."],
                        className="modal-text mb-0"),
                 # Card Button -------------------------------------------------------------------------------
                 html.Button(className="btn btn-theme mt-4",
                             children="Read More",
                             id="open_dls_info-3"),

                 # Modal ----------------------------------------------------------------------------------------------------------------------------

                 dbc.Modal([
                     dbc.ModalHeader(dbc.ModalTitle(
                         "Digital Language Support Info")),
                     dbc.ModalBody(
                         modal_dls_info_text),
                     dbc.ModalFooter(
                         dbc.Button("Close",
                                    id="close-body-scroll-dls",
                                    className="ms-auto",
                                    n_clicks=0)
                     ),
                 ], id="modal-dls-info-3",
                    size='lg',
                    scrollable=True,
                    is_open=False)

                 ],
                className="about-lang-card")
        ], className="col-md-7 order-0 order-md-1")
    ], className="row align-items-center")
],className="container mt-5 pt-md-3")

## 5.2) Page body -------------------------------------------------------------------------------------------------------------------------------------------------------

### 5.2.1) First row ----------------------------------------------------------------------------------------------------------------------------------------------------
card1 = html.Div([
    html.Div([
        html.Div([
            html.H5(
                "Digital Language Support by Country ",
                className="mb-0 fw-semibold",
            ),
            html.Button('Info', id='info-dls-country',
                              className="btn btn-theme", n_clicks=0),
            # html.I(
            #     className="fa-solid fa-circle-info text-muted",id='dls_country_popup',
            # ),
            # html.Span(html.Div(className="fa fa-info-circle"),
            #           id='dls_country_popup',
            #           # style={"textDecoration": "underline", "cursor": "pointer"}
            #           ),
            dbc.Popover(
                html.Div(
                    ["The Digital Support Language by Country is a weighted average of the DLS of the\
                    languages spoken in that Country. The weight used is the percentage of L1 speakers \
                    of a given language in that Country."]),
                className='bg-white',
                style={'background-color': 'rgb(255, 255, 225)'},
                target="info-dls-country",
                body=True,
                trigger="legacy",
                placement='top'
            ),
        ], className="card-heading d-flex justify-content-between mb-4"),
        # html.Img(
        #     src="/assets/images/digitalLang.png",
        #     className="img-fluid w-100",
        #     alt="digtal language",
        # ),
        dcc.Loading(children=[dcc.Graph(figure=fig, style={
            # 'width': '100% !important',
            'height': '100%'
        }, config={'modeBarButtonsToRemove': ['lasso2d', 'select2d'], 'displaylogo': False})],
            type="circle")
    ], className="card-body"),
], className="card")

### 5.2.2) Second row ---------------------------------------------------------------------------------------------------------------------------------------------------
card2 = html.Div(
    className="card",
    children=[
        html.Div(
            className="card-body",
            children=[
                html.Div(
                    className="card-heading d-md-flex justify-content-between align-items-center mb-4",
                    children=[
                        html.H5(className="mb-0 fw-semibold", children="Digital Language Support Countries Rank"),
                        # html.Button(className="btn btn-theme mt-3 d-block ms-auto", 
                        #             children="View All", id="dlsCountry", n_clicks=0, **{'data-bs-toggle': 'modal', 'data-bs-target': '#dlsCountry'})
                    ]
                ),
                dcc.Loading(children=[html.Div([country_table])],
                                type="circle")
            ]
        )
    ]
)

### 5.2.3) Third row ----------------------------------------------------------------------------------------------------------------------------------------------------
card3 = html.Div(
    className="card",
    children=[
        html.Div(
            className="card-body",
            children=[
                dbc.Row([
                    html.Div(
                        className="card-heading d-md-flex justify-content-between align-items-center mb-4",
                        children=[
                            html.H5(className="mb-0 fw-semibold", children="Digital Language Support By Scope"),
                            dcc.Dropdown(options=[{'label': 'Count of language supported by feature', 'value': 'Feature_Name'},
                                            {'label': 'Count of feature support by language','value': 'Reference_Name'},
                                            {'label': 'Features count by Support Category', 'value': 'Support_Category'}],
                                                value="Support_Category",style={"width": "336px"},
                                                id='dropdown_menu')
                        ])
                ]),
                dbc.Row([
                    dbc.Col([dcc.Loading(children=[
                                html.Div(id='datatable-interactivity-container')
                                ],type="circle")]),
                    dbc.Col([html.Div(id='dropdown_menu_selection')])
                ])
            ])
    ])

### 5.2.4) Fourth row ---------------------------------------------------------------------------------------------------------------------------------------------------
card4 = dbc.Card([
    dbc.CardBody([
        # dbc.CardHeader(
        #     dbc.Row([
        #             dbc.Col(
        #                 html.H5("Digital Language Support Level", className="mb-0 fw-semibold")),
        #         ],align="center",
        #         justify="between")
        #         ),
        
        html.Div([html.H5(className="mb-0 fw-semibold",
                          children="Digital Language Support Level"),
                  html.Button('Info', id='template',
                              className="btn btn-theme", n_clicks=0),
                  # Tooltip ----------------------------------------------------------------------------------------------------------------------------
                  dbc.Tooltip([
                      dbc.Row([
                          dbc.Col([
                              html.P([html.A("Simons et al. (2022)", href="https://arxiv.org/pdf/2209.13515.pdf", target="_blank"),
                                      " describe a way to categorize different languages\
                                     based on their growth and success. They use an S-shaped curve to visualize\
                                     this growth, which is common when studying innovation.\
                                     They look at the shape of this curve and use it to put each language into\
                                     one of five categories:"], style={"text-align": "justify",
                                                                       "color": "black"}),
                              html.Li(["Still — a score of 0"], style={"text-align": "justify",
                                                                       "color": "black"}),
                              html.Li(["Emerging — at the bottom, where the slope is primarily horizontal"],
                                      style={"text-align": "justify",
                                             "color": "black"}),
                              html.Li(["Ascending — below the midpoint where the slope is mostly vertical"],
                                      style={"text-align": "justify",
                                             "color": "black"}),
                              html.Li(["Vital — above the midpoint where the slope is mostly vertical"],
                                      style={"text-align": "justify",
                                             "color": "black"}),
                              html.Li(["Thriving — at the top where the slope is mostly horizontal"],
                                      style={"text-align": "justify",
                                             "color": "black"}),
                          ],className="col-md-6"),
                          dbc.Col([
                              dcc.Graph(figure=fig_SCurve, style={
                                #   'width': '600px !important',
                                  'height': '100%'},
                                config={'modeBarButtonsToRemove': [
                                        'lasso2d', 'select2d'],
                                        'displaylogo': False,
                                        'staticPlot' : True},
                              )],className="col-md-5",
                              style={"padding": "0"})
                      ], style={"width": "inherit"})
                  ],
                style={"background-color": "white",
                    "color": "black",
                    "width":"600px",
                    "border-radius": "5px",
                    "border": "2px solid black"},
                target="template",
                trigger="legacy")
            ], className="card-heading d-flex justify-content-between mb-4",
            style={"align-items": "baseline"}),
        html.Div([
            dbc.Row([
                # First Col --------------------------------------------------------------------------------------------------------------------------------
                dbc.Col(
                    ## Table with data ##
                    # [DLS_level_table],
                    [
                        # Dropdown menu ----------------------------------------------------------------------------------------------
                        dcc.Dropdown(options=[{'label': 'DLS level language count', 'value': 'Lang_Count'},
                                              {'label': 'DLS level population count', 'value': 'L1_Users'}],
                                     value="Lang_Count",
                                     id='dropdown-menu-dls-level'),
                        # Loading circle and map plot (id = "datatable-interactivity-map-container" ) --------------------
                        dcc.Loading(children=[html.Div(id="dls-level-piecharts")],
                                    type="circle")
                    ],
                    width=6),
                # Second Col -------------------------------------------------------------------------------------------------------------------------------
                dbc.Col(                    
                    [lang_pyramid.LangPyramid(
                        id='input',
                    )],
                    width=6,
                    className="mt-5 mt-lg-0",
                ),
            ]),
        ]),
    ]),
])

page_body = html.Section([card1, card2, card3,card4], className="container mt-100")

### 5.3) Footer ---------------------------------------------------------------------------------------------------------------------------------------------------------
footer = html.Footer([
    html.Div([
        html.Div([html.P(className="mb-0",
                         children="Copyright © 2021–2023. Derivation LLC. All Rights Reserved."),
                  html.Div([html.A(className="text-white me-3",
                                   href="https://derivation.co/about-us/",
                                   children="About"),
                            html.A(className="text-white",
                                   href="https://derivation.co/contact/",
                                   children="Support"),
                            ], className="mt-2 mt-md-0"),
                  ], className="d-md-flex justify-content-md-between text-center"),
    ], className="container"),
], className="mt-100")


layout = html.Div([
  #first_row,
  page_body,
  footer  
])