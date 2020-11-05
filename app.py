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
from aggregate_data import load_building_size_data
from aggregate_data import load_num_dev_res_units_data
from aggregate_data import load_net_effects_data


from plot_figure import citywide_choropleth
from plot_figure import community_district_choropleth
from plot_figure import building_size_bar
from plot_figure import hny_bar_chart
from plot_figure import net_bar_chart


from tabs.cumulative_production import create_cumulative_production_tab
from tabs.affordable_housing import create_affordable_housing_tab
from tabs.building_size import create_building_size_tab
from tabs.net_effects import create_net_effects_tab
from tabs.pipeline import create_pipeline_tab

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

####################
# components 
####################

headers = create_headers()

######################
# Call the Tabs Functions to create tabs
########################
cumulative_content = create_cumulative_production_tab(app)

pipeline_content = create_pipeline_tab(app)

affordable_content = create_affordable_housing_tab()

building_size_content = create_building_size_tab()

net_effects_content = create_net_effects_tab()
#################### 
# dcc tabs 
####################

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
    dcc.Tabs(id="tab-selection", value='tab-cumulative', children=[
        dcc.Tab(label='Cumulative Production', value='tab-cumulative', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Pipeline', value='tab-pipeline', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Affordable Housing', value='tab-affordable', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Building Size', value='tab-size', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Net Effects', value='tab-net-effects', style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles),
    html.Div(id='tab-content')
])

@app.callback(Output('tab-content', 'children'), [Input('tab-selection', 'value')])
def render_content(tab):
    if tab == 'tab-cumulative':
        return cumulative_content
    elif tab == 'tab-pipeline':
        return pipeline_content
    elif tab == 'tab-affordable':
        return affordable_content
    elif tab == 'tab-size':
        return building_size_content
    elif tab == 'tab-net-effects':
        return net_effects_content


@app.callback(Output('choro-graphic', 'figure'),
    [Input('job-type-dropdown', 'value'), 
    Input('year-slider', 'value'),
    Input('tab-selection', 'value')])
def update_citywide_graphic(job_type, year, tab_select):

    year_flag = 'complete_year' if tab_select == 'tab-cumulative' else 'permit_year'
    
    df = load_num_dev_res_units_data(database, year, job_type, year_flag)

    fig = citywide_choropleth(df, job_type, mapbox_token)

    return fig

@app.callback(
    [Output('cd-choro-graphic', 'figure'),
    Output('cd-bar-chart', 'figure'),
    Output('cd-line-chart', 'figure')],
    [Input('boro-dropdown', 'value'),
    Input('tab-selection', 'value')]
)
def update_community_district_graphic(boro, tab_select):

    year_flag = 'complete_year' if tab_select == 'tab-cumulative' else 'permit_year'

    df = load_community_district_data(database, boro, year_flag)

    choro, bar, line = community_district_choropleth(df, mapbox_token)

    return choro, bar, line


@app.callback(Output('affordable-graphic', 'figure'), [Input('status-radio', 'value')])
def update_affordable_graphic(status):

    df = load_affordable_data(database, status)

    fig = hny_bar_chart(df, status)

    return fig

@app.callback(Output('building-size-graphic', 'figure'), [Input('job-type-dropdown-2', 'value')])
def update_building_size_graphic(job_type):

    df = load_building_size_data(database)

    fig = building_size_bar(df, job_type)

    return fig

@app.callback(Output('net-effects-graphic', 'figure'), [Input('net-effects-mode', 'value')])
def update_net_effects_graphic(mode):

    df = load_net_effects_data(database)

    fig = net_bar_chart(df)

    return fig

if __name__ == '__main__':

    app.run_server(debug=True)

