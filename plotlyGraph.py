import os.path
import pandas as pd  # import and analyze data with high performance and productivity
import numpy as np
import chart_studio.plotly as py
import seaborn as sns  # provides beautiful default styles and color palettes to make statistical plots more attractive
import plotly.express as px  # Create entire figure / graph at once
import plotly.graph_objects as go


def buil_csv_file(country, positiveFreq, negativeFreq, neutralFreuq):
    fileName = ""
    if country == 'Malaysia':
        fileName = 'MY'
    elif country == 'United State':
        fileName = 'US'
    elif country == 'Singapore':
        fileName = 'SG'
    elif country == 'Taiwan':
        fileName = 'TW'
    else:
        fileName = 'JP'
    Sentiment = ["Positive", "Negative", "Neutral"]
    Frequency = [positiveFreq, negativeFreq, neutralFreuq]
    dictionary = {'Sentiment': Sentiment, 'Frequency': Frequency}
    df = pd.DataFrame(dictionary)
    fileName = fileName+".csv"
    #  Only want to create the file one time
    if not os.path.exists("graphAnalysis\\" + fileName):
        df.to_csv("graphAnalysis\\"+fileName, index=False)


df = pd.read_csv("graphAnalysis\\SG.csv")  # Use pandas to read our data file
#  Build "df" dataFrame to build the histogram
#  The title of the histogram = "Overview for Singapore"
#  Use values of "Sentiment" column as index in x-axis (x = 'Sentiment')
#  Use values of "Frequency" column as y-axis values (x = 'Frequency')
#  text_auto=True allows us to display the value on the histogram
fig = px.histogram(df, title="Overview for Singapore", x='Sentiment', y='Frequency', text_auto=True)
#  Define the gap between each bar
fig.update_layout(bargap=0.3, yaxis_title="Frequency")
fig.show()
