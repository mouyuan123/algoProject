import os
import dash
import plotly.graph_objs as go
import pandas as pd
from dash import Input, Output, dcc, html
from plotly.subplots import make_subplots

dataFrame = {}  # Store the dictionary to be used in DataFrame
sentimentList = ["Positive", "Negative", "Neutral"]


# Create .csv file of positive, negative and neutral words for each country using pandas
def build_dataFrame(countryDict):
    for i, j in countryDict.items():
        dataFrame[i] = {sentimentList[0]: j[0], sentimentList[1]: j[1], sentimentList[2]: j[2], 'Length of words': j[3]}


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
                                                                          marker=dict(color='#2F8F9D'))).update_layout(
        title='Differences of Word Frequency', plot_bgcolor='rgba(0,0,0,0)'),
        style={'width': '50%', 'height': '70vh', 'display': 'inline-block'})
    return barChart


def get_line_chart(analysis):
    lineChart = dcc.Graph(figure=go.Figure(layout=layout).add_trace(go.Scatter(x=analysis['country'],
                                                                               y=analysis['length of words'],
                                                                               marker=dict(
                                                                               color='#2F8F9D'))).update_layout(
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
        'box-shadow': '4px 4px 4px 4px lightgrey'
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
        elif country == 'All (Group Bar Chart)':
            d = go.Figure()
            d.add_trace(go.Bar(x=sentimentList,
                               y=dFrame['Malaysia'],
                               name='Malaysia'))
            d.add_trace(go.Bar(x=sentimentList,
                               y=dFrame['Singapore'],
                               name='Singapore'))
            d.add_trace(go.Bar(x=sentimentList,
                               y=dFrame['United States'],
                               name='United States'))
            d.add_trace(go.Bar(x=sentimentList,
                               y=dFrame['Japan'],
                               name='Japan'))
            d.add_trace(go.Bar(x=sentimentList,
                               y=dFrame["Taiwan"],
                               name='Taiwan'))
            return updateLayout(d)
        elif country == 'All (Pie Chart)':
            positiveWords = dataFrame['Malaysia'][sentimentList[0]] + dataFrame['Singapore'][sentimentList[0]] + dataFrame['United States'][sentimentList[0]] + dataFrame['Japan'][sentimentList[0]] + dataFrame['Taiwan'][sentimentList[0]]
            negativeWords = dataFrame['Malaysia'][sentimentList[1]] + dataFrame['Singapore'][sentimentList[1]] + dataFrame['United States'][sentimentList[1]] + dataFrame['Japan'][sentimentList[1]] + dataFrame['Taiwan'][sentimentList[1]]
            neutralWords = dataFrame['Malaysia'][sentimentList[2]] + dataFrame['Singapore'][sentimentList[2]] + dataFrame['United States'][sentimentList[2]] + dataFrame['Japan'][sentimentList[2]] + dataFrame['Taiwan'][sentimentList[2]]
            pie = pd.DataFrame(
                {"countryName": ['Malaysia', 'Singapore', 'United Statess', 'Japan', 'Taiwan'],
                    "value1": [dataFrame['Malaysia'][sentimentList[0]],
                                     dataFrame['Singapore'][sentimentList[0]],
                                     dataFrame['United States'][sentimentList[0]],
                                     dataFrame['Japan'][sentimentList[0]],
                                     dataFrame['Taiwan'][sentimentList[0]]],
                    "value2": [dataFrame['Malaysia'][sentimentList[1]],
                                    dataFrame['Singapore'][sentimentList[1]],
                                    dataFrame['United States'][sentimentList[1]],
                                    dataFrame['Japan'][sentimentList[1]],
                                    dataFrame['Taiwan'][sentimentList[1]]],
                    "value3": [dataFrame['Malaysia'][sentimentList[2]],
                                dataFrame['Singapore'][sentimentList[2]],
                                dataFrame['United States'][sentimentList[2]],
                                dataFrame['Japan'][sentimentList[2]],
                                dataFrame['Taiwan'][sentimentList[2]]]
                 })
            fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
            fig = fig.add_trace(go.Pie(labels=pie.countryName, values=pie.value1, textinfo='label+percent', insidetextorientation='radial'), 1, 1)
            fig.add_trace(go.Pie(labels=pie.countryName, values=pie.value2, textinfo='label+percent', insidetextorientation='radial'), 1, 2)
            fig.add_trace(go.Pie(labels=pie.countryName, values=pie.value3, textinfo='label+percent', insidetextorientation='radial'), 1, 3)

            # Create donut pie chart using 'hole'
            fig.update_traces(hole=.4, hoverinfo="label+value")

            fig.update_layout(
                title_text="Percentage of Positive Words ("+str(positiveWords)+"), Negative Words ("+str(negativeWords)+"), and Neutral Words ("+str(neutralWords)+") For Each Country",
                # Add title in the center of the donut pies.
                annotations=[dict(text='Positive words', x=0.10, y=0.5, font_size=15, showarrow=False),
                             dict(text='Negative words', x=0.50, y=0.5, font_size=15, showarrow=False),
                             dict(text='Neutral words', x=0.90, y=0.5, font_size=15, showarrow=False)])
            return fig
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
                        {'label': 'All (Group Bar Chart)', 'value': 'All (Group Bar Chart)'},
                        {'label': 'All (Pie Chart)', 'value': 'All (Pie Chart)'},
                        {'label': 'Malaysia', 'value': 'Malaysia'},
                        {'label': 'Singapore', 'value': 'Singapore'},
                        {'label': 'United States', 'value': 'United States'},
                        {'label': 'Japan', 'value': 'Japan'},
                        {'label': 'Taiwan', 'value': 'Taiwan'}
                    ],
                    value='All (Group Bar Chart)',
                    style={'width': '50%',
                           'margin': '20px auto 0px auto'}
                ),
                # Define th core component which is used to display any type of graph within it
                dcc.Graph(id='bar-graph',
                          style={'height': '500px'})
            ])
        elif tab == 'Comparison':
            analysis = pd.DataFrame(
                {'country': ['Malaysia', 'Singapore', 'United States', 'Japan', 'Taiwan'],
                 'length of words': [dataFrame['Malaysia']['Length of words'],
                                     dataFrame['Singapore']['Length of words'],
                                     dataFrame['United States']['Length of words'],
                                     dataFrame['Japan']['Length of words'],
                                     dataFrame['Taiwan']['Length of words']],
                 "differences": [dataFrame['Malaysia'][sentimentList[0]] - dataFrame['Malaysia'][sentimentList[1]],
                                 dataFrame['Singapore'][sentimentList[0]] - dataFrame['Singapore'][sentimentList[1]],
                                 dataFrame['United States'][sentimentList[0]] - dataFrame['United States'][sentimentList[1]],
                                 dataFrame['Japan'][sentimentList[0]] - dataFrame['Japan'][sentimentList[1]],
                                 dataFrame['Taiwan'][sentimentList[0]] - dataFrame['Taiwan'][sentimentList[1]]]
                 })
            return html.Div([
                html.H1('Comparison among countries', style={'text-align': 'center', 'background-color': '#ede9e8'}),
                get_line_chart(analysis),
                get_bar_chart(analysis)
            ])

    app.run_server()


