# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

#my own imports
from joblib import load
slr = load('assets/slr.joblib')
slrf = load('assets/slrf.joblib')
gb = load('assets/gb.joblib')
gbf = load('assets/gbf.joblib')



# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Deliberate Training Focus

            Maybe you've reached the point in your training where more kilos don't come cheap. Maybe you're short on time. Maybe you're just curious.

            Whether it's because your hamstrings can only take so much punishment every week or you have limited time to devote to assistance work,
            knowing where to direct your limited training resources is key to optimizing your progress. Identifying the lifts that need help the most is 
            a good start, and can help you decide whether deficit pulls or pause squats are a better use of those hamstrings right now.

            The Raw Deadlift Predictor uses data from over three decades of global powerlifting meet results to give you a typical raw deadlift number for someone 
            with your other stats. 
            
            If your actual pull is substantially higher, consider helping your squat catch up. 
            If it's substantially lower, it might be time for more pulling volume.
            If it's about the same, congratulations on being proportional. Must be nice. 

            """
        ),
        dcc.Link(dbc.Button('Male Predictor', color='primary'), href='/male_predictor'),
        dcc.Link(dbc.Button('Female Predictor', color='primary'), href='/female_predictor')
    ],
    md=4,
)



column2 = dbc.Col(
    [
        html.Img(src='assets/gymcrop4.jpg')
    ]
)

layout = dbc.Row([column1, column2])