import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def create_historical_district_tab():        

    tab = dbc.Card(
        dbc.CardBody(
            [   
                dbc.Row(
                    [
                        # this is the control panel 
                        dbc.Col(
                            [
                                dbc.Card(
                                    dbc.CardBody(
                                        html.Div(
                                            [
                                                html.H2('Control Panel'),
                                                html.P('View Citywide or by Boroughs'),
                                                dcc.RadioItems(
                                                    id='historical-district-boro-radio',
                                                    options=[
                                                        {'label': 'Citywide', 'value': '1, 2, 3, 4, 5'},
                                                        {'label': 'Manhattan', 'value': 1},
                                                        {'label': 'Bronx', 'value': 2},
                                                        {'label': 'Brooklyn', 'value': 3},
                                                        {'label': 'Queens', 'value': 4},
                                                        {'label': 'Staten Island', 'value': 5},
                                                    ],
                                                    value='1, 2, 3, 4, 5',
                                                    labelStyle={'display': 'inline-block'}
                                                ),
                                                dcc.RadioItems(
                                                    id='historical-district-percent-radio',
                                                    options=[
                                                        {'label': 'Units', 'value': 'Units'},
                                                        {'label': 'Stacked Percentage', 'value': 'Percentage'},
                                                    ],
                                                    value='Units',
                                                    labelStyle={'display': 'inline-block'}
                                                ),
                                            ]
                                        )
                                    )
                                ),
                                dbc.Card(
                                    dbc.CardBody(
                                        html.Div(
                                            [
                                                html.H2(''),
                                                html.P('Summary Type'),
                                                dcc.RadioItems(
                                                    id='historical-district-net-only-radio',
                                                    options=[
                                                        {'label': 'Net Only', 'value': 0},
                                                        {'label': 'By Parts', 'value': 1},
                                                    ],
                                                    value=0,
                                                    labelStyle={'display': 'inline-block'}
                                                ),
                                                html.P('Data Normalization'),
                                                dcc.RadioItems(
                                                    id='historical-district-normalization-radio',
                                                    options=[
                                                        {'label': 'Units', 'value': 0},
                                                        {'label': 'Units per acre', 'value': 1},
                                                    ],
                                                    value=0,
                                                    labelStyle={'display': 'inline-block'}
                                                ),
                                            ]
                                        )
                                    )
                                )
                            ],
                            width={"size": 3}
                        ),
                        # this is the main graphics panel
                        dbc.Col(
                            [
                                dbc.Row(
                                    dcc.Graph(id='historical-units-bar')
                                ),
                                dbc.Row(
                                    dcc.Graph(id='historical-land-area-bar')
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        className="mt-3"
    )

    return tab