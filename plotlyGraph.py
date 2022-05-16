import pandas as pd  # import and analyze data with high performance and productivity
import numpy as np
import chart_studio.plotly as py
import seaborn as sns  # provides beautiful default styles and color palettes to make statistical plots more attractive
import plotly.express as px # Create entire figure / graph at once
import plotly.graph_objects as go


def build_histogram(countryName, articleTitle, positiveWords, negativeWords, neutralWords):
    sentiments = [positiveWords,negativeWords,neutralWords]
    fig = px.histogram(sentiments, title=articleTitle, x="Sentiment of Words", y="Frequency of Words")

    fig.show()


# Creating the Figure instance
fig = px.line(x=[1, 2, 3], y=[1, 2, 3])

# showing the plot
fig.show()