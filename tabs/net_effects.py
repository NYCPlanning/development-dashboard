import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

def create_net_effects_tab():

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
                                                id="net-effects-mode",
                                                options=[{
                                                    'label': x,
                                                    'value': x
                                                    } for x in ['All Job Types', 'Alteration Only']
                                                ],
                                                value='Alteration Only'
                                            ),
                                        ]
                                    )
                                )
                            ),
                            width={"size": 4}
                        ),
                        # this is the graphics
                        dbc.Col(dcc.Graph(id='net-effects-graphic'))
                    ]
                )
            ]
        ),
        className="mt-3"
    )

    return tab