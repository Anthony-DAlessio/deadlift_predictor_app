# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

#my own imports
import pandas as pd
import numpy as np
from joblib import load
slrf = load('assets/slrf.joblib')
gbf = load('assets/gbf.joblib')



# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Your Stats:


            """
        ),
    
    dbc.InputGroup(
        [dbc.InputGroupAddon("Age(years):", addon_type="prepend"), dbc.Input(id="age", type="number", debounce=False, placeholder="Age(years)")],
            size="lg",
    ),
    html.Br(),
    dbc.InputGroup(
        [dbc.InputGroupAddon("Bodyweight(kg):", addon_type="prepend"), dbc.Input(id="bodyweight", type="number", debounce=False, placeholder="BW(kg)")],
            size="lg",
    ),
    html.Br(),
    dbc.InputGroup(
        [dbc.InputGroupAddon("Squat(kg)", addon_type="prepend"), dbc.Input(id="squat", type="number", debounce=False, placeholder="Squat(kg)")],
            size="lg",
    ),
    html.Br(),
    dbc.InputGroup(
        [dbc.InputGroupAddon("Bench(kg)", addon_type="prepend"), dbc.Input(id="bench", type="number", debounce=False, placeholder="Bench(kg)")],
            size="lg",
    ),
    
    

    ],
    md=4, align="center"
)
        
linear_card_content = [
    dbc.CardHeader(html.H4("Linear Regression Model")),
    dbc.CardBody(
        [
            html.H1(html.Div(id='female_linear_prediction')),
            
        ]
    ),
]
gradient_boosting_card_content = [
    dbc.CardHeader(html.H4("Gradient Boosting Model")),
    dbc.CardBody(
        [
            html.H1(html.Div(id='female_gradient_boosting_prediction')),
            
        ]
    ),
]
average_card_content = [
    dbc.CardHeader(html.H4("Average")),
    dbc.CardBody(
        [
            html.H1(html.Div(id='female_average_prediction')),
            
        ]
    ),
]



    
column2 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Your Predicted Deadlift(kg):


            """
        ),
        dbc.Card(linear_card_content, color="secondary"),
        dbc.Card(gradient_boosting_card_content, color="secondary"),
        dbc.Card(average_card_content, color="secondary")
    ],
    align="top", md=6
)
@app.callback(
    Output("female_linear_prediction", "children"),
    [Input("age", "value"), Input("bodyweight", "value"), Input("squat", "value"), Input("bench", "value")],
)
def flpredict(age, bodyweight, squat, bench):
    
    if(age is None):
        age = 1
    if(bodyweight is None):
        bodyweight = 1
    if(squat is None):
        squat = 1
    if(bench is None):
        bench = 1
    

    a = 594.31747775582
    b = -27.23842536447
    c = 0.82112226871
    d = -0.00930733913
    e = 0.00004731582
    f = -0.00000009054

    mswilks = squat * 500 /(a+(b*bodyweight)+(c*bodyweight**2)+(d*bodyweight**3)+(e*bodyweight**4)+(f*bodyweight**5))
    mbwilks = bench * 500 /(a+(b*bodyweight)+(c*bodyweight**2)+(d*bodyweight**3)+(e*bodyweight**4)+(f*bodyweight**5))
    mbbr = bench/bodyweight
    mbsr = bench/squat
    age_class = '24-34'

    if (age>=5)&(age<=12):
        age_class = '5-12'
    elif (age>=13)&(age<=15):
        age_class = '13-15'
    elif (age>=16)&(age<=17):
        age_class = '16-17'
    elif (age>=18)&(age<=19):
        age_class = '18-19'
    elif (age>=20)&(age<=23):
        age_class = '20-23'
    elif (age>=24)&(age<=34):
        age_class = '24-34'
    elif (age>=35)&(age<=39):
        age_class = '35-39'
    elif (age>=40)&(age<=44):
        age_class = '40-44'
    elif (age>=45)&(age<=49):
        age_class = '45-49'
    elif (age>=50)&(age<=54):
        age_class = '50-54'
    elif (age>=55)&(age<=59):
        age_class = '55-59'
    elif (age>=60)&(age<=64):
        age_class = '60-64'
    elif (age>=65)&(age<=69):
        age_class = '65-69'
    elif (age>=70)&(age<=74):
        age_class = '70-74'
    elif (age>=75):
        age_class = '75-79'

    weight_class = '93'
    if bodyweight<=50:
        weight_class = '44'
    elif (bodyweight>50)&(bodyweight<=52):
        weight_class = '52'
    elif (bodyweight>52)&(bodyweight<=63):
        weight_class = '63'
    elif (bodyweight>63)&(bodyweight<=72):
        weight_class = '72'
    elif (bodyweight>72)&(bodyweight<=84):
        weight_class = '84'
    elif (bodyweight>84)&(bodyweight<=90):
        weight_class = '90'
    elif (bodyweight>90)&(bodyweight<=100):
        weight_class = '100'
    elif (bodyweight>100):
        weight_class = '100+'
    
    
    temp = pd.DataFrame(
        columns=['Age', 'AgeClass', 'BodyweightKg', 'WeightClassKg', 'Best3SquatKg', 'Best3BenchKg', 'Squat Wilks', 'Bench Wilks', 'Bench:Bodyweight Ratio', 'Bench:Squat Ratio'], 
        data=[[age, age_class, bodyweight, weight_class, squat, bench, mswilks, mbwilks, mbbr, mbsr]]
    )
    y_pred = slrf.predict(temp)[0]
    return y_pred


@app.callback(
    Output("female_gradient_boosting_prediction", "children"),
    [Input("age", "value"), Input("bodyweight", "value"), Input("squat", "value"), Input("bench", "value")],
)
def gbfpredict(age, bodyweight, squat, bench):
    
    if(age is None):
        age = 1
    if(bodyweight is None):
        bodyweight = 1
    if(squat is None):
        squat = 1
    if(bench is None):
        bench = 1
    

    a = 594.31747775582
    b = -27.23842536447
    c = 0.82112226871
    d = -0.00930733913
    e = 0.00004731582
    f = -0.00000009054

    mswilks = squat * 500 /(a+(b*bodyweight)+(c*bodyweight**2)+(d*bodyweight**3)+(e*bodyweight**4)+(f*bodyweight**5))
    mbwilks = bench * 500 /(a+(b*bodyweight)+(c*bodyweight**2)+(d*bodyweight**3)+(e*bodyweight**4)+(f*bodyweight**5))
    mbbr = bench/bodyweight
    mbsr = bench/squat
    age_class = '24-34'

    if (age>=5)&(age<=12):
        age_class = '5-12'
    elif (age>=13)&(age<=15):
        age_class = '13-15'
    elif (age>=16)&(age<=17):
        age_class = '16-17'
    elif (age>=18)&(age<=19):
        age_class = '18-19'
    elif (age>=20)&(age<=23):
        age_class = '20-23'
    elif (age>=24)&(age<=34):
        age_class = '24-34'
    elif (age>=35)&(age<=39):
        age_class = '35-39'
    elif (age>=40)&(age<=44):
        age_class = '40-44'
    elif (age>=45)&(age<=49):
        age_class = '45-49'
    elif (age>=50)&(age<=54):
        age_class = '50-54'
    elif (age>=55)&(age<=59):
        age_class = '55-59'
    elif (age>=60)&(age<=64):
        age_class = '60-64'
    elif (age>=65)&(age<=69):
        age_class = '65-69'
    elif (age>=70)&(age<=74):
        age_class = '70-74'
    elif (age>=75):
        age_class = '75-79'

    weight_class = '93'
    if bodyweight<=50:
        weight_class = '44'
    elif (bodyweight>50)&(bodyweight<=52):
        weight_class = '52'
    elif (bodyweight>52)&(bodyweight<=63):
        weight_class = '63'
    elif (bodyweight>63)&(bodyweight<=72):
        weight_class = '72'
    elif (bodyweight>72)&(bodyweight<=84):
        weight_class = '84'
    elif (bodyweight>84)&(bodyweight<=90):
        weight_class = '90'
    elif (bodyweight>90)&(bodyweight<=100):
        weight_class = '100'
    elif (bodyweight>100):
        weight_class = '100+'
    
    
    temp = pd.DataFrame(
        columns=['Age', 'AgeClass', 'BodyweightKg', 'WeightClassKg', 'Best3SquatKg', 'Best3BenchKg', 'Squat Wilks', 'Bench Wilks', 'Bench:Bodyweight Ratio', 'Bench:Squat Ratio'], 
        data=[[age, age_class, bodyweight, weight_class, squat, bench, mswilks, mbwilks, mbbr, mbsr]]
    )
    y_pred = gbf.predict(temp)[0]
    return y_pred

@app.callback(
    Output("female_average_prediction", "children"),
    [Input("age", "value"), Input("bodyweight", "value"), Input("squat", "value"), Input("bench", "value")],
)
def avpredict(age, bodyweight, squat, bench):
    
    if(age is None):
        age = 1
    if(bodyweight is None):
        bodyweight = 1
    if(squat is None):
        squat = 1
    if(bench is None):
        bench = 1
    

    a = 594.31747775582
    b = -27.23842536447
    c = 0.82112226871
    d = -0.00930733913
    e = 0.00004731582
    f = -0.00000009054

    mswilks = squat * 500 /(a+(b*bodyweight)+(c*bodyweight**2)+(d*bodyweight**3)+(e*bodyweight**4)+(f*bodyweight**5))
    mbwilks = bench * 500 /(a+(b*bodyweight)+(c*bodyweight**2)+(d*bodyweight**3)+(e*bodyweight**4)+(f*bodyweight**5))
    mbbr = bench/bodyweight
    mbsr = bench/squat
    age_class = '24-34'

    if (age>=5)&(age<=12):
        age_class = '5-12'
    elif (age>=13)&(age<=15):
        age_class = '13-15'
    elif (age>=16)&(age<=17):
        age_class = '16-17'
    elif (age>=18)&(age<=19):
        age_class = '18-19'
    elif (age>=20)&(age<=23):
        age_class = '20-23'
    elif (age>=24)&(age<=34):
        age_class = '24-34'
    elif (age>=35)&(age<=39):
        age_class = '35-39'
    elif (age>=40)&(age<=44):
        age_class = '40-44'
    elif (age>=45)&(age<=49):
        age_class = '45-49'
    elif (age>=50)&(age<=54):
        age_class = '50-54'
    elif (age>=55)&(age<=59):
        age_class = '55-59'
    elif (age>=60)&(age<=64):
        age_class = '60-64'
    elif (age>=65)&(age<=69):
        age_class = '65-69'
    elif (age>=70)&(age<=74):
        age_class = '70-74'
    elif (age>=75):
        age_class = '75-79'

    weight_class = '93'
    if bodyweight<=50:
        weight_class = '44'
    elif (bodyweight>50)&(bodyweight<=52):
        weight_class = '52'
    elif (bodyweight>52)&(bodyweight<=63):
        weight_class = '63'
    elif (bodyweight>63)&(bodyweight<=72):
        weight_class = '72'
    elif (bodyweight>72)&(bodyweight<=84):
        weight_class = '84'
    elif (bodyweight>84)&(bodyweight<=90):
        weight_class = '90'
    elif (bodyweight>90)&(bodyweight<=100):
        weight_class = '100'
    elif (bodyweight>100):
        weight_class = '100+'
    
    
    temp = pd.DataFrame(
        columns=['Age', 'AgeClass', 'BodyweightKg', 'WeightClassKg', 'Best3SquatKg', 'Best3BenchKg', 'Squat Wilks', 'Bench Wilks', 'Bench:Bodyweight Ratio', 'Bench:Squat Ratio'], 
        data=[[age, age_class, bodyweight, weight_class, squat, bench, mswilks, mbwilks, mbbr, mbsr]]
    )
    
    y_pred1 = gbf.predict(temp)[0]
    y_pred2 = slrf.predict(temp)[0]
    y_average = (y_pred1+y_pred2)/2
    return y_average

layout = dbc.Row([column1, column2], align='top')