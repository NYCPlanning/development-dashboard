import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from aggregate_data import load_community_district_data
import dash_bootstrap_components as dbc


def create_cumulative_production_tab(app):

    @app.callback(Output('cumulative-control', 'children'), [Input('pp-citywide-dropdown', 'value')])
    def create_cumulative_production_control_panel(citywide_toggle):

        if citywide_toggle == 'Citywide':

            widgets = html.Div(
                        [                              
                            html.P('View by number of jobs or residential units'),
                            dcc.RadioItems(
                                id='pp-citywide-jobs-units-radio',
                                options=[
                                    {'label': 'View by Residential Units', 'value': 'total_classa_net'},
                                    {'label': 'View by Number of Jobs', 'value': 'total_num_jobs'}
                                ],
                                value='total_classa_net'
                            ),
                            html.P('To View Units Normalized Acreage or Unnormalized'),
                            dcc.RadioItems(
                                id='pp-citywide-normalization-radio',
                                options=[
                                    {'label': 'Normalized by Acreage', 'value': 'units_per_acre'},
                                    {'label': 'Unnormalized', 'value': 'total_classa_net'} # this is wrong and need to be a choice between jobs 
                                ],
                                value='units_per_acre'
                            ),
                            html.P('Use the slider to select a year'),
                            dcc.RangeSlider(
                                id='pp-citywide-year-range-slider',
                                min=2010,
                                max=2020,
                                value=[2010, 2020],
                                marks={str(year): str(year) for year in range(2010, 2021)},
                                included=True
                            )
                        ]
            )

        elif citywide_toggle == 'Boroughs':

            #boro_options = ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']

            widgets = html.Div(
                [
                    html.P('Please use the dropdown below to select a borough to view'),
                    dcc.Dropdown(
                        id='pp-cd-boro-dropdown',
                        options=[
                            {'label': 'Manhattan', 'value': 1},
                            {'label': 'Bronx', 'value': 2},
                            {'label': 'Brooklyn', 'value': 3},
                            {'label': 'Queens', 'value': 4},
                            {'label': 'Staten Island', 'value': 5},
                        ],
                        value=1
                    )
                ], 
                style={'width': '70%', 'float': 'Center', 'display': 'inline-block'}
            )

        return widgets

    @app.callback(Output('cumulative-content', 'children'), [Input('pp-citywide-dropdown', 'value')])
    def create_cumulative_content(citywide_toggle):

        if citywide_toggle == 'Citywide':

            content = dcc.Graph(id='pp-citywide-choro')

        else:
            
            content = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='pp-cd-choro')),
                            dbc.Col(dcc.Graph(id='pp-cd-bar'))
                        ]
                    ),
                    dcc.Graph(id='pp-cd-line')
                ]
            )
        
        return content

    tab = dbc.Card(
        dbc.CardBody(
            [   
                dbc.Row(
                    [
                        # this is the control panel 
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    html.Div(
                                        [
                                            html.H2('Control Panel'),
                                            dcc.Dropdown(
                                                id="pp-job-type-dropdown",
                                                options=[
                                                    {'label': 'All Job Types', 'value': "'New Building', 'Demolition', 'Alteration'"},
                                                    {'label': 'New Building', 'value': "'New Building'"},
                                                    {'label': 'Demolition', 'value': "'Demolition'"},
                                                    {'label': 'Alteration', 'value': "'Alteration'"}                          
                                                ],
                                                value="'New Building', 'Demolition', 'Alteration'"
                                            ),
                                            html.P('Choose Citywide view or Borough View'),
                                            dcc.Dropdown(
                                                id="pp-citywide-dropdown",
                                                options=[{
                                                    'label': x,
                                                    'value': x
                                                    } for x in ['Citywide', 'Boroughs']
                                                ],
                                                value='Citywide'
                                            ),
                                            # control panel content depends on the citywide toggle 
                                            html.Div(id='cumulative-control')
                                        ]
                                    )
                                )
                            ),
                            width={"size": 4}
                        ),
                        # this is the graphics
                        dbc.Col(html.Div(id='cumulative-content'))
                    ]
                ),
            ]
        ),
        className="mt-3",
    )

    return tab