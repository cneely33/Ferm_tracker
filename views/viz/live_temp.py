
from dash.dependencies import Output, Input
# import dash_bootstrap_components as dbcs
import dash_core_components as dcc
import dash_html_components as html
# import plotly
# import random
# import plotly.graph_objs as go
import plotly.express as px
# from collections import deque

from app import app, no_data_fig
from data.gsheets_data import google_sheets_data
import functions


## create callback id prefex generator
id_gen = functions.id_factory('live_feed')

layout = html.Div(
    [
    dcc.Interval(id=id_gen('graph_update'),
       interval=300*1000,
       n_intervals=0
       ),
    
    # html.Div(id=id_gen("print_n"), style={"text-align": "center"}),
    
    dcc.Graph(id=id_gen('graph_temp'), figure={}),
    dcc.Graph(id=id_gen('graph_humidity'), figure={}),
    ]
)

# @app.callback(Output(id_gen('print_n'), 'children'),
#               [Input(id_gen('graph_update'), 'n_intervals')])
# def return_n(n):
#     try:
#         n_count = 'interval count ' + str(n)
#     except Exception as e:
#         print(e)
#     return n_count

@app.callback(Output(id_gen('graph_temp'), 'figure'),
              [Input(id_gen('graph_update'), 'n_intervals')])
def update_graph_scatter_temp(n):
    try:
        df_copy = google_sheets_data()
        df_copy = df_copy.head(20)
        fig = px.line(df_copy, x='timestamp', 
                      y='temperature', 
                      # color='country',
                      markers=True)
        fig = functions.remove_figure_background(fig)

    except Exception as e:
        print(e)
        fig = no_data_fig
    return fig


@app.callback(Output(id_gen('graph_humidity'), 'figure'),
               [Input(id_gen('graph_update'), 'n_intervals')]
              )
def update_graph_scatter_humid(n):
    try:
        df_copy = google_sheets_data()
        df_copy = df_copy.head(20)
        fig = px.line(df_copy, x='timestamp', 
                      y='humidity', 
                      # color='country',
                      markers=True)
        fig = functions.remove_figure_background(fig)

    except Exception as e:
        print(e)
        fig = no_data_fig
    return fig


