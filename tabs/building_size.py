import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def create_building_size_tab():

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
                                            html.P('Use radio to select view units for complete or incomplete projects'),
                                            dcc.Dropdown(
                                                id="job-type-dropdown-2",
                                                options=[{
                                                    'label': x,
                                                    'value': x
                                                    } for x in ['New Building', 'Demolition']
                                                ],
                                                value='New Building'
                                            ),
                                        ]
                                    )
                                )
                            ),
                            width={"size": 4}
                        ),
                        # this is the graphics
                        dbc.Col(dcc.Graph(id='building-size-graphic'))
                    ]
                )
            ]
        ),
        className="mt-3"
    )

    return tab