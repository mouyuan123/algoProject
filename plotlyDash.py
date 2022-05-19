"""
A simple app demonstrating how to dynamically render tab content containing
dcc.Graph components to ensure graphs get sized correctly. We also show how
dcc.Store can be used to cache the results of an expensive graph generation
process so that switching tabs is fast.
"""
import os
import time

import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
import pandas as pd
from dash import Input, Output, dcc, html

dataFrame = {}  # Store the dictionary to be used in DataFrame
sentimentList = ["Positive", "Negative", "Neutral"]


# Create .csv file of positive, negative and neutral words for each country using pandas
def build_csv_file(countryDict):
    fileName = "data.csv"
    # Each column name is equivalent to "country name"
    for i, j in countryDict.items():
        dataFrame[i] = {sentimentList[0]: j[0], sentimentList[1]: j[1], sentimentList[2]: j[2], 'Length of words': j[3]}
    df = pd.DataFrame(dataFrame)
    #  Only want to create the file one time
    if not os.path.exists("graphAnalysis\\" + fileName):
        df.to_csv("graphAnalysis\\" + fileName, index=False)


def updateLayout(figure):
    figure.update_layout(xaxis_title="Sentiment",
                         yaxis_title="Frequency of Words",
                         # Define the position of the title of the graph
                         title_x=0.5,
                         title_y=0.95,
                         # Define the font size and type of title of graph
                         title_font=dict(family="Arial", size=30),
                         # Define the font type and size of the text in the graph (excluding title)
                         font=dict(family='Balto', size=16),
                         # Define how the hover text looks like when the mouse hover over the bar chart
                         hoverlabel=dict(
                             bgcolor="white",
                             font_size=16,
                             font_family="Rockwell"
                         ))
    return figure


# ======================== Setting the margins
layout = go.Layout(
    margin=go.layout.Margin(
        l=40,  # left margin
        r=40,  # right margin
        b=10,  # bottom margin
        t=35  # top margin
    )
)


# ======================== Plotly Graphs
def get_bar_chart(analysis):
    barChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Bar(x=analysis['country'],
                                                                          y=analysis['differences'],
                                                                          marker=dict(color='#351e15'))).update_layout(
        title='Differences of Word Frequency', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '70vh', 'display': 'inline-block'})
    return barChart


def get_line_chart(analysis):
    lineChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Scatter(x=analysis['country'],
                                                                               y=analysis['length of words'],
                                                                               marker=dict(
                                                                               color='#351e15'))).update_layout(
        title='Total Number of Words', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '70vh', 'display': 'inline-block'})
    return lineChart


def build():
    tabs_styles = {
        'height': '44px',
        'align-items': 'center'
    }
    tab_style = {
        'borderBottom': '1px solid #d6d6d6',
        'padding': '6px',
        'fontWeight': 'bold',
        'border-radius': '15px',
        'background-color': '#F2F2F2',
        'box-shadow': '4px 4px 4px 4px lightgrey',

    }

    tab_selected_style = {
        'borderTop': '1px solid #d6d6d6',
        'borderBottom': '1px solid #d6d6d6',
        'backgroundColor': '#119DFF',
        'color': 'white',
        'padding': '6px',
        'border-radius': '15px',
    }
    app = dash.Dash(__name__)
    # Create the DataFrame object using the dictionary defined above
    dFrame = pd.DataFrame(dataFrame)
    app.layout = html.Div((
        html.Div([
            html.Div([
                dcc.Tabs(id="tabs-styled-with-inline", value='Overview', children=[
                    dcc.Tab(label='Overview', value='Overview', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Comparison', value='Comparison', style=tab_style, selected_style=tab_selected_style),
                ], style=tabs_styles),
                html.Div(id='tabs-content-inline')
            ], className="create_container3 eight columns", ),
        ], className="row flex-display")
    ))

    #  Run the graph on the website
    @app.callback(Output('bar-graph', 'figure'), Input('countryName', 'value'))
    def get_graph(country):
        if country is None:
            return go.Figure()
        elif country == 'All':
            d = go.Figure()
            d.add_trace(go.Bar(x=sentimentList,
                               y=dFrame['Malaysia'],
                               name='Malaysia'))
            d.add_trace(go.Bar(x=sentimentList,
                               y=dFrame['Singapore'],
                               name='Singapore'))
            d.add_trace(go.Bar(x=sentimentList,
                               y=dFrame['United State'],
                               name='United State'))
            d.add_trace(go.Bar(x=sentimentList,
                               y=dFrame['Japan'],
                               name='Japan'))
            d.add_trace(go.Bar(x=sentimentList,
                               y=dFrame["Taiwan"],
                               name='Taiwan'))
            return updateLayout(d)
        else:
            figure = go.Figure().add_trace(go.Bar(x=sentimentList,
                                                  y=dFrame[country],
                                                  name=country,
                                                  marker=dict(color="#F4BFBF")
                                                  ))
        return updateLayout(figure)

    @app.callback(Output('tabs-content-inline', 'children'), Input('tabs-styled-with-inline', 'value'))
    def render_content(tab):
        if tab == 'Overview':
            return html.Div([
                # Set the heading of this page using HTML component, h1
                html.H1('Overview of the Word Frequency of Each Country',
                        id='title',
                        style={'color': '#351e15',
                               'text-align': 'center',
                               'margin-top': '20px'}),
                dcc.Dropdown(
                    id='countryName',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Malaysia', 'value': 'Malaysia'},
                        {'label': 'Singapore', 'value': 'Singapore'},
                        {'label': 'United State', 'value': 'United State'},
                        {'label': 'Japan', 'value': 'Japan'},
                        {'label': 'Taiwan', 'value': 'Taiwan'}
                    ],
                    value='All',
                    style={'width': '50%',
                           'margin': '20px auto 0px auto'}
                ),
                # Define th core component which is used to display any type of graph within it
                dcc.Graph(id='bar-graph',
                          style={'height': '500px'})
            ])
        elif tab == 'Comparison':
            analysis = pd.DataFrame(
                {'country': ['Malaysia', 'Singapore', 'United State', 'Japan', 'Taiwan'],
                 'length of words': [dataFrame['Malaysia']['Length of words'],
                                     dataFrame['Singapore']['Length of words'],
                                     dataFrame['United State']['Length of words'],
                                     dataFrame['Japan']['Length of words'],
                                     dataFrame['Taiwan']['Length of words']],
                 "differences": [dataFrame['Malaysia'][sentimentList[0]] - dataFrame['Malaysia'][sentimentList[1]],
                                 dataFrame['Singapore'][sentimentList[0]] - dataFrame['Singapore'][sentimentList[1]],
                                 dataFrame['United State'][sentimentList[0]] - dataFrame['United State'][sentimentList[1]],
                                 dataFrame['Japan'][sentimentList[0]] - dataFrame['Japan'][sentimentList[1]],
                                 dataFrame['Taiwan'][sentimentList[0]] - dataFrame['Taiwan'][sentimentList[1]]]
                 })
            return html.Div([
                html.H1('Comparison among countries', style={'text-align': 'center', 'background-color': '#ede9e8'}),
                get_line_chart(analysis),
                get_bar_chart(analysis)
            ])

    app.run_server()
