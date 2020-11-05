import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from aggregate_data import load_community_district_data
import dash_bootstrap_components as dbc


def create_pipeline_tab(app):

    @app.callback(Output('pipeline-control', 'children'), [Input('citywide-dropdown', 'value')])
    def create_pipeline_control_panel(citywide_toggle):

        if citywide_toggle == 'Citywide':

            widgets = html.Div(
                        [
                            html.P('Please use the options to select one job type to view'),                                
                            dcc.Dropdown(
                                id="job-type-dropdown",
                                options=[{
                                    'label': x,
                                    'value': x
                                    } for x in ['New Building', 'Demolition', 'Alteration']
                                ],
                                value='New Building'
                            ),
                            html.P('Use the slider to select a year'),
                            dcc.Slider(
                                id='year-slider',
                                min=2010,
                                max=2020,
                                value=2010,
                                marks={str(year): str(year) for year in range(2010, 2021)},
                                included=False
                            )
                        ]
            )

        elif citywide_toggle == 'Boroughs':

            boro_options = ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']

            widgets = html.Div(
                [
                    html.P('Please use the dropdown below to select a borough to view'),
                    dcc.Dropdown(
                        id='boro-dropdown',
                        options=[{'label': k, 'value': k} for k in boro_options],
                        value='Manhattan'
                    )
                ], 
                style={'width': '70%', 'float': 'Center', 'display': 'inline-block'}
            )

        return widgets

    @app.callback(Output('pipeline-content', 'children'), [Input('citywide-dropdown', 'value')])
    def create_pipeline_content(citywide_toggle):

        if citywide_toggle == 'Citywide':

            content = dcc.Graph(id='choro-graphic')

        else:
            
            content = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Graph(id='cd-choro-graphic')),
                            dbc.Col(dcc.Graph(id='cd-bar-chart'))
                        ]
                    ),
                    dcc.Graph(id='cd-line-chart')
                    #dbc.Row(
                        #[
                        #    dcc.Graph(id='cd-line-chart')
                        #]
                    #)
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
                                            html.P('Choose Citywide view or Borough View'),
                                            dcc.Dropdown(
                                                id="citywide-dropdown",
                                                options=[{
                                                    'label': x,
                                                    'value': x
                                                    } for x in ['Citywide', 'Boroughs']
                                                ],
                                                value='Citywide'
                                            ),
                                            # control panel content depends on the citywide toggle 
                                            html.Div(id='pipeline-control')
                                        ]
                                    )
                                )
                            ),
                            width={"size": 4}
                        ),
                        # this is the graphics
                        dbc.Col(html.Div(id='pipeline-content'))
                    ]
                ),
            ]
        ),
        className="mt-3",
    )

    return tab