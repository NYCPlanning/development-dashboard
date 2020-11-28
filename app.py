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
from aggregate_data import load_citywide_data
from aggregate_data import load_net_effects_data


from plot_figure import citywide_choropleth
from plot_figure import community_district_choropleth
from plot_figure import building_size_bar
from plot_figure import hny_chart
from plot_figure import net_effects_chart


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

#headers = create_headers()

######################
# Call the Tabs Functions to create tabs
########################
cumulative_tab = create_cumulative_production_tab(app)

pipeline_tab = create_pipeline_tab(app)

affordable_tab = create_affordable_housing_tab()

building_size_tab = create_building_size_tab()

net_effects_tab = create_net_effects_tab(app)

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
    #headers,
    dcc.Tabs(id="tab-selection", value='tab-cumulative', children=[
        dcc.Tab(label='Cumulative Production', value='tab-cumulative', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Pipeline', value='tab-pipeline', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Affordable Housing', value='tab-affordable', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Building Size', value='tab-size', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Net Effects', value='tab-net-effects', style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles),
    html.Div(id='tab-content')
])


###########################
# production and pipelines
###########################
@app.callback(Output('tab-content', 'children'), [Input('tab-selection', 'value')])
def render_content(tab):
    if tab == 'tab-cumulative':
        return cumulative_tab
    elif tab == 'tab-pipeline':
        return pipeline_tab
    elif tab == 'tab-affordable':
        return affordable_tab
    elif tab == 'tab-size':
        return building_size_tab
    elif tab == 'tab-net-effects':
        return net_effects_tab


@app.callback(
    Output('pp-citywide-choro', 'figure'),
    [
        Input('tab-selection', 'value'),
        Input('pp-citywide-job-type-dropdown', 'value'), 
        Input('pp-citywide-year-range-slider', 'value'),
        Input('pp-citywide-jobs-units-radio', 'value'),
        Input('pp-citywide-normalization-radio', 'value')
    ]
)
def update_citywide_graphic(tab_select, job_type, year, job_units, normalization):

    year_flag = 'complete_year' if tab_select == 'tab-cumulative' else 'permit_year'
    
    df = load_citywide_data(database, job_type, year_flag, year[0], year[1])

    fig = citywide_choropleth(df, mapbox_token, job_type, job_units, normalization)

    return fig

@app.callback(
    [
        Output('pp-cd-choro', 'figure'),
        Output('pp-cd-bar', 'figure'),
        Output('pp-cd-line', 'figure')
    ],
    [
        Input('tab-selection', 'value'),
        Input('pp-cd-boro-dropdown', 'value')
    ]
)
def update_community_district_graphic(tab_select, boro):

    year_flag = 'complete_year' if tab_select == 'tab-cumulative' else 'permit_year'

    df = load_community_district_data(database, boro, year_flag)

    choro, bar, line = community_district_choropleth(df, mapbox_token)

    return choro, bar, line

###############################
# affordable
###############################
@app.callback(
    [
        Output('affordable-bar', 'figure'), 
        Output('affordable-bar-hny-charct', 'figure')
    ],
    [
        Input('affordable-percent-radio', 'value'),
        Input('affordable-status-radio', 'value'),
        Input('affordable-charct-radio', 'value')
    ]
)
def update_affordable_graphic(percent_flag, status, charct_flag):

    df, df_charct = load_affordable_data(database, percent_flag, status, charct_flag)

    bar, hny_bar = hny_chart(df, df_charct, percent_flag, status)

    return bar, hny_bar

###############################
# building size
###############################
@app.callback(Output('building-size-graphic', 'figure'), [Input('job-type-dropdown-2', 'value')])
def update_building_size_graphic(job_type):

    df = load_building_size_data(database)

    fig = building_size_bar(df, job_type)

    return fig


###############################
# net effects
###############################
@app.callback(
    [
        Output('net-effects-boro-bar', 'figure'),
        Output('net-effects-boro-choro', 'figure')
    ],
    [
        Input('net-effects-job-type-dropdown', 'value'),
        Input('net-effects-x-dropdown', 'value'),
        Input('net-effects-boro-radio', 'value'),
        Input('net-effects-year-slider', 'value')
    ]
)
def update_net_effects_boro_graphic(job_type, x_axis, boro, year):

    df = load_net_effects_data(database, job_type, x_axis, boro, year[0], year[1])

    bar, choro = net_effects_chart(df, mapbox_token, job_type, x_axis)

    return bar, choro

@app.callback(Output('net-effects-year-bar', 'figure'),
    [
        Input('net-effects-job-type-dropdown', 'value'),
        Input('net-effects-x-dropdown', 'value'),
        Input('net-effects-year-boro-radio', 'value')
    ]
)
def update_net_effects_year_graphic(job_type, x_axis, boro):

    df = load_net_effects_data(database, job_type, x_axis, boro)
    
    bar = net_effects_chart(df, mapbox_token, job_type, x_axis)

    return bar



if __name__ == '__main__':

    app.run_server(debug=True)

