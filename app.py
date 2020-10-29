import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
import plotly.express as px
import requests
import pandas as pd
import dash_bootstrap_components as dbc
import dash_ui as dui 
from components.headers import create_headers
import os
# for local testing with .env file
from dotenv import load_dotenv, find_dotenv

from aggregate_data import load_community_district_data
from aggregate_data import load_affordable_data


from plot_figure import citywide_choropleth
from plot_figure import community_district_choropleth
from plot_figure import building_size_bar
from plot_figure import hny_bar_chart


from aggregate_data import load_bar_units_agg
from aggregate_data import load_num_dev_res_units_data


from tabs.cumulative_production import create_cumulative_production_tab
from tabs.affordable_housing import create_affordable_housing_tab
from tabs.building_size import create_building_size_tab

# get the enviromental variable in local testing 
load_dotenv(find_dotenv())

database = os.getenv('BUILD_ENGINE')

mapbox_token = os.getenv('MAPBOX_TOKEN')

# app dash 
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config['suppress_callback_exceptions'] = True

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

boro_options = [
'Manhattan',
'Bronx',
'Brooklyn',
'Queens',
'Staten Island'
]
####################
# components 
####################

headers = create_headers()

######################
# Tabs 
########################
citywide_content = create_cumulative_production_tab()

borough_content = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    dcc.Dropdown(
                        id='boro-dropdown',
                        options=[{'label': k, 'value': k} for k in boro_options],
                        value='Manhattan'
                    ),
                    dcc.Graph(id='cd-choro-graphic'),
                    dcc.Slider(
                        id='cd-year-slider',
                        min=2010,
                        max=2020,
                        value=2010,
                        marks={str(year): str(year) for year in range(2010, 2020)},
                        included=False
                    ),
                ], 
                style={'width': '70%', 'float': 'Center', 'display': 'inline-block'}
            ),
            html.Div(
                [
                    dcc.Graph(id='cd-bar-chart')
                ],
                style={'width': '70%', 'float': 'Center', 'display': 'inline-block'}
            )
        ]
    ),
    className="mt-3",
)

affordable_content = create_affordable_housing_tab()

building_size_content = create_building_size_tab()

######### 
# dcc tabs 
#########

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
    html.H1('Housing Dashboard'),
    headers,
    dcc.Tabs(id="tabs-main", value='tab-cumulative', children=[
        dcc.Tab(label='Cumulative Production', value='tab-cumulative', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Pipeline', value='tab-pipeline', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Affordable Housing', value='tab-affordable', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Building Size', value='tab-size', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Alteration Effects', value='tab-alteration', style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs-main', 'value')])
def render_content(tab):
    if tab == 'tab-cumulative':
        return citywide_content
    elif tab == 'tab-pipeline':
        return borough_content
    elif tab == 'tab-affordable':
        return affordable_content
    elif tab == 'tab-size':
        return building_size_content
    elif tab == 'tab-alteration':
        return html.Div([
            html.H3('Tab content alteration')
        ])


@app.callback(
    Output('choro-graphic', 'figure'),
    [Input('job-type-dropdown', 'value'),
    Input('year-slider', 'value')]
)
def update_citywide_graphic(job_type, year):
    
    df = load_num_dev_res_units_data(database, year, job_type)

    fig = citywide_choropleth(df, job_type, mapbox_token)

    return fig

@app.callback(
    [Output('cd-choro-graphic', 'figure'),
    Output('cd-bar-chart', 'figure')],
    [Input('boro-dropdown', 'value'),
    Input('cd-year-slider', 'value')]
)
def update_community_district_graphic(boro, year):

    df = load_community_district_data(boro, database)

    choro, bar = community_district_choropleth(df, mapbox_token)

    return choro, bar


@app.callback(
    Output('affordable-graphic', 'figure'),
    [Input('status-radio', 'value')]
)
def update_affordable_graphic(status):

    df = load_affordable_data(database, status)

    fig = hny_bar_chart(df, status)

    return fig

@app.callback(
    Output('building-size-graphic', 'figure'),
    [Input('job-type-dropdown-2', 'value')]
)
def update_building_size_graphic(job_type):

    df = load_bar_units_agg(database)

    fig = building_size_bar(df, job_type)

    return fig

if __name__ == '__main__':

    app.run_server(debug=True)

