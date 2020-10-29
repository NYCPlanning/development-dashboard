import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from aggregate_data import load_community_district_data
import dash_bootstrap_components as dbc


def create_pipeline_tab():

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
                                            html.P('Select one job type to view...'),
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
                                )
                            ),
                            width={"size": 5}
                        ),
                        # this is the graphics
                        dbc.Col(
                            html.Div(
                                [

                                    dcc.Graph(id='choro-graphic'),

                                    dcc.Graph(id='bar-chart')
                                ]
                            )
                        )
                    ]
                ),
            ]
        ),
        className="mt-3",
    )

    return tab