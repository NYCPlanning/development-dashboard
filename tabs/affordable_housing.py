import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def create_affordable_housing_tab():

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
                                            html.P('Choose to view the charts in units or percentage'),
                                            dcc.RadioItems(
                                                id='affordable-percent-radio',
                                                options=[
                                                    {'label': 'Units', 'value': 'Units'},
                                                    {'label': 'Percentage', 'value': 'Percentage'},
                                                ],
                                                value='Units',
                                                labelStyle={'display': 'inline-block'}
                                            ),
                                            #html.H4('Housing Units Other vs. HNY'),
                                            #html.P('Use radio to select view units for complete or incomplete projects'),
                                            #dcc.RadioItems(
                                            #    id='affordable-status-radio',
                                            #    options=[
                                            #        {'label': 'Complete', 'value': 'Complete'},
                                            #        {'label': 'Incomplete', 'value': 'Incomplete'}
                                            #    ],
                                            #    value='Complete',
                                            #    labelStyle={'display': 'inline-block'}
                                            #),
                                            html.H4('Housing New York Units Characteristics'),
                                            html.P(''),
                                            dcc.RadioItems(
                                                id='affordable-char-radio',
                                                options=[
                                                    {'label': 'Affordable units by income level', 'value': 'Income Level'},
                                                    {'label': 'Affordable units by number of bedrooms', 'value': 'Number of Bedrooms'},
                                                    {'label': 'Affordable units by rental/owner status', 'value': 'Owner Status'}
                                                ],
                                                value='Income Level',
                                                labelStyle={'display': 'inline-block'}
                                            )
                                        ]
                                    )
                                )
                            ),
                            width={"size": 4}
                        ),
                        # this is the graphics
                        dbc.Col(
                            html.Div(
                                    [
                                        dcc.Graph(id='affordable-bar'),
                                        dcc.Graph(id='affordable-bar-hny-char')
                                    ],
                                    style={'width': '100%', 'float': 'Center', 'display': 'inline-block'}
                            )
                        )
                    ]
                )
            ]
        ),
        className="mt-3"
    )

    return tab