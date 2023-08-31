import dash
from dash import Input, Output, dcc, html, dash_table , State, callback
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
import dash_bootstrap_components as dbc
import plotly.express as px

from load_data import *
from functions import *

# 1) Callbacks ----------------------------------------------------------------------------------------------------------------------------------------------------------

@callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(DLS_scores_by_lang[['ISO_639','Reference_Name','Adjusted_Score']].to_csv, "DLS_scores.csv")


# 2) Layout -------------------------------------------------------------------------------------------------------------------------------------------------------------

layout = html.Div([
                   dbc.Row([
                            dbc.Col([
                                     dash_table.DataTable(DLS_scores_by_lang[['ISO_639','Reference_Name','Adjusted_Score']].to_dict('records'),
                                                         [{"name": i, "id": i} for i in DLS_scores_by_lang[['ISO_639','Reference_Name','Adjusted_Score']].columns])

                                     ]),
                            dbc.Col([
                                     html.Button("Download CSV", id = "btn_csv"),
                                     dcc.Download(id="download-dataframe-csv"),
                                     ])
                            ])
                   ])