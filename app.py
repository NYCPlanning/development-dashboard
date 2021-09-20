import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
import plotly.express as px
import requests
import pandas as pd
import dash_bootstrap_components as dbc
#import dash_ui as dui 
from components.headers import create_headers
import os
# for local testing with .env file
from dotenv import load_dotenv, find_dotenv


from aggregate_data import load_community_district_data
from agg_functions.agg_affordable import load_affordable_data
from agg_functions.agg_building_size import load_building_size_data
from aggregate_data import load_citywide_data
#from aggregate_data import load_net_effects_data
from agg_functions.agg_zoning_district import load_zoning_district_data
from agg_functions.agg_historical_district import load_historical_district_data
from agg_functions.agg_net_effects import load_net_effects_data


from plot_figure.plot_product_pipeline import citywide_choropleth
from plot_figure.plot_product_pipeline import community_district_choropleth
from plot_figure.plot_building_size import building_size_bar
from plot_figure.plot_affordable import affordable_chart
from plot_figure.plot_net_effects import net_effects_chart, net_effects_table
from plot_figure.plot_historical import historical_chart
from plot_figure.plot_zoning_district import zoning_district_chart


from tabs.cumulative_production import create_cumulative_production_tab
from tabs.affordable_housing import create_affordable_housing_tab
from tabs.building_size import create_building_size_tab
from tabs.net_effects import create_net_effects_tab
from tabs.pipeline import create_pipeline_tab
from tabs.zoning_district import create_zoning_district_tab
from tabs.historical_district import create_historical_district_tab

# get the enviromental variable in local testing 
load_dotenv(find_dotenv())

database = os.getenv('BUILD_ENGINE')

mapbox_token = os.getenv('MAPBOX_TOKEN')

# use this when load environment variables from server
#database = os.environ.get("BUILD_ENGINE", "")

#mapbox_token = os.environ.get("MAPBOX_TOKEN", "")

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

zoning_tab = create_zoning_district_tab()

historical_tab = create_historical_district_tab()

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
        dcc.Tab(label='Net Effects', value='tab-net-effects', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Zoning District', value='tab-zoning-district', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Historical District', value='tab-historical-district', style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles),
    html.Div(id='tab-content')
])

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
    elif tab == 'tab-zoning-district':
        return zoning_tab
    elif tab == 'tab-historical-district':
        return historical_tab

##########################################
# production and pipelines
##########################################

@app.callback(
    Output('pp-citywide-choro', 'figure'),
    [
        Input('tab-selection', 'value'),
        Input('pp-job-type-dropdown', 'value'), 
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
        Input('pp-job-type-dropdown', 'value'), 
        Input('pp-cd-boro-dropdown', 'value')
    ]
)
def update_community_district_graphic(tab_select, job_type, boro):

    year_flag = 'complete_year' if tab_select == 'tab-cumulative' else 'permit_year'

    df = load_community_district_data(database, job_type, boro, year_flag)

    choro, bar, line = community_district_choropleth(df, job_type, boro, mapbox_token)

    return choro, bar, line

###############################
# affordable
###############################

@app.callback(
    [
        Output('affordable-bar', 'figure'), 
        Output('affordable-bar-hny-char', 'figure')
    ],
    [
        Input('affordable-percent-radio', 'value'),
        #Input('affordable-status-radio', 'value'),
        Input('affordable-char-radio', 'value')
    ]
)
def update_affordable_graphic(percent_flag, char_flag):

    df_aff, df_char = load_affordable_data(database, percent_flag, char_flag)

    aff_bar, hny_bar = affordable_chart(df_aff, df_char, percent_flag, char_flag)

    return aff_bar, hny_bar

###############################
# building size
###############################


@app.callback(
[
    Output('building-size-median', 'children'),
    Output('building-size-mean', 'children'),
    Output('building-size-graphic', 'figure')
],     
[
    Input('building-size-job-type-dropdown', 'value'),
    Input('building-size-percent-radio', 'value')
]
)
def update_building_size_graphic(job_type, percent_flag):

    df, stats = load_building_size_data(database, job_type, percent_flag)

    median = stats.classa_net.median()

    mean = stats.classa_net.mean()

    fig = building_size_bar(df, job_type, percent_flag)

    return median, mean, fig


###############################
# net effects
###############################
# year option
@app.callback(
        Output('net-effects-citywide-bar', 'figure'),
        #Output('net-effects-zd-bar', 'figure')
    [
        Input('net-effects-job-type-dropdown', 'value'),
        Input('net-effects-x-dropdown', 'value'),
        Input('net-effects-citywide-boro-radio', 'value')
    ]
)
def update_net_effects_citywide_graphic(job_type, x_axis, boro):

    df = load_net_effects_data(database, job_type, x_axis, boro)
    
    boro_bar = net_effects_chart(df, mapbox_token, job_type, x_axis, boro)

    return boro_bar

@app.callback(
    [
        Output('net-effects-boro-bar', 'figure'),
        Output('net-effects-boro-choro', 'figure'),
        Output('net-effects-boro-datatable', 'children')
    ],
    [
        Input('net-effects-job-type-dropdown', 'value'),
        Input('net-effects-x-dropdown', 'value'),
        Input('net-effects-boro-radio', 'value'),
        Input('net-effects-geometries', 'value'),
        Input('net-effects-year-slider', 'value')
    ]
)
def update_net_effects_boro_graphic(job_type, x_axis, boro, geometry, year):

    df = load_net_effects_data(database, job_type, x_axis, boro, geometry, year[0], year[1])

    bar, choro = net_effects_chart(df, mapbox_token, job_type, x_axis, boro, geometry=geometry)

    dt = net_effects_table(df)

    return bar, choro, dt

@app.callback(
    Output('net-effects-census-pie', 'figure'),
    [Input('net-effects-boro-choro', 'selected-value')]
)
def update_net_effects_boro_graphic(select_geom):

    pie = census_chart(select_geom)

    return pie

#####################
# zoning district 
######################

@app.callback(
    [
        Output('zoning-district-units-bar', 'figure'),
        Output('zoning-district-land-area-bar', 'figure'),
        #Output('zoning-district-reference-map', 'figure')
    ],
    [
        Input('zoning-district-boro-radio', 'value'),
        Input('zoning-district-percent-radio', 'value'),
        Input('zoning-district-net-only-radio', 'value'),
        Input('zoning-district-normalization-radio', 'value')
    ]
)
def update_zoning_district_graphic(boro, percent_flag, net_flag, norm_flag):

    df = load_zoning_district_data(database, boro, percent_flag, net_flag, norm_flag)

    #print(df)
    
    bar_units, bar_land_area = zoning_district_chart(df, norm_flag)

    return bar_units, bar_land_area#, ref_map, 

#####################
# historical district
######################


@app.callback(
    [
        Output('historical-units-bar', 'figure'),
        Output('historical-land-area-bar', 'figure')
    ],
    [
        Input('historical-district-boro-radio', 'value'),
        Input('historical-district-percent-radio', 'value'),
        Input('historical-district-net-only-radio', 'value'),
        Input('historical-district-normalization-radio', 'value')
    ]
)
def update_historical_district_graphic(boro, percent_flag, net_flag, norm_flag):

    df = load_historical_district_data(database, boro, percent_flag, net_flag, norm_flag)

    #print(df)
    
    bar_units, bar_land_area = historical_chart(df, norm_flag)

    return bar_units, bar_land_area


if __name__ == '__main__':
    
    #app.run_server(host='0.0.0.0', port=5000, debug=False) 

    # use this for local development and debugging
    app.run_server(debug=True)

