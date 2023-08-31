import dash
from dash import Input, Output, dcc, html, dash_table , State, callback
from dash.dash_table.Format import Format, Scheme, Sign, Symbol
import dash_bootstrap_components as dbc
import plotly.express as px

from load_data import *
from functions import *


layout = html.Div([
                   dbc.Row([
                            dbc.Col([
                                     html.P(["Unauthorized access. Available to Academic and Commercial Users Only"])
                                     ])
                            ])
                   ],className="fullheight")