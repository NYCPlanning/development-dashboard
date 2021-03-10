import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def create_zoning_district_tab():        

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
                                                html.P('Select the job types '),
                                                dcc.Dropdown(
                                                    id="zoning-district-job-type-dropdown",
                                                    options=[{
                                                        'label': x,
                                                        'value': x
                                                        } for x in ['All Job Types', 'Alteration Only', 'New Building and Demolition']
                                                    ],
                                                    value='Alteration Only'
                                                ),
                                                html.P('View Citywide or by Boroughs'),
                                                dcc.RadioItems(
                                                    id='zoning-district-boro-radio',
                                                    options=[
                                                        {'label': 'Citywide', 'value': '1, 2, 3, 4, 5'},
                                                        {'label': 'Manhattan', 'value': 1},
                                                        {'label': 'Bronx', 'value': 2},
                                                        {'label': 'Brooklyn', 'value': 3},
                                                        {'label': 'Queens', 'value': 4},
                                                        {'label': 'Staten Island', 'value': 5},
                                                    ],
                                                    value='1, 2, 3, 4, 5',
                                                    labelStyle={'display': 'block'}
                                                ),
                                                html.P('View the data through units or percentage breakdown'),
                                                dcc.RadioItems(
                                                    id='zoning-district-percent-radio',
                                                    options=[
                                                        {'label': 'Units', 'value': 'Units'},
                                                        {'label': 'Percentage', 'value': 'Percentage'},
                                                    ],
                                                    value='Units',
                                                    labelStyle={'display': 'block'}
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
                                                    id='zoning-district-net-only-radio',
                                                    options=[
                                                        {'label': 'Net Only', 'value': 0},
                                                        {'label': 'By Parts', 'value': 1},
                                                    ],
                                                    value=0,
                                                    labelStyle={'display': 'block'}
                                                ),
                                                html.P('Data Normalization'),
                                                dcc.RadioItems(
                                                    id='zoning-district-normalization-radio',
                                                    options=[
                                                        {'label': 'Units', 'value': 0},
                                                        {'label': 'Units per acre', 'value': 1},
                                                    ],
                                                    value=0,
                                                    labelStyle={'display': 'block'}
                                                ),
                                            ]
                                        )
                                    )
                                )
                            ],
                            width={"size": 3}
                        ),
                        # referece map first
                        dbc.Col(
                            #html.P('Place holder for reference map'),#add the new reference map)
                            #dcc.Graph(id='zoning-district-reference-map')
                            #ref_map = <iframe width="100%" height="520" frameborder="0" src="https://nycplanning.carto.com/u/dcpbuilder/builder/cb8f558f-f0e2-464a-862f-f8afa9b2bb53/embed" allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen></iframe>
                            html.Iframe(src="https://nycplanning.carto.com/u/dcpbuilder/builder/cb8f558f-f0e2-464a-862f-f8afa9b2bb53/embed", 
                                style={"height": "80%", "width": "100%", "frameborder" : "0"})
                        ),
                        # this is the main graphics panel
                        dbc.Col(
                            [
                                dbc.Row(dbc.Spinner(dcc.Graph(id='zoning-district-units-bar'))),
                                dbc.Row(dbc.Spinner(dcc.Graph(id='zoning-district-land-area-bar')))
                            ]
                        ),
                    ]
                )
            ]
        ),
        className="mt-3"
    )

    return tab