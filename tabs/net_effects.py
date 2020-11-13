import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def create_net_effects_tab(app):

    @app.callback(Output('net-effects-content', 'children'), [Input('net-effects-x-dropdown', 'value')])
    def create_net_effects_content(x_dropdown):

        if x_dropdown == 'By Year':

            content = dcc.Graph(id='net-effects-graphic')

        else:

            boro_options = ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']

            content = html.Div(
                [
                    # boro selection 
                    dcc.RadioItems(
                        id='net-effects-boro-radio',
                        options=[
                            {'label': 'Manhattan', 'value': 1},
                            {'label': 'Bronx', 'value': 2},
                            {'label': 'Brooklyn', 'value': 3},
                            {'label': 'Queens', 'value': 4},
                            {'label': 'Staten Island', 'value': 5},
                        ],
                        value=1,
                        labelStyle={'display': 'inline-block'}
                    ),  
                    # the bar chart 
                    dcc.Graph(id='net-effects-choro'),
                    # also add a map
                    dcc.Graph(id='net-effects-bar'),
                    dcc.Slider(
                        id='net-effects-year-slider',
                        min=2010,
                        max=2020,
                        value=2010,
                        marks={str(year): str(year) for year in range(2010, 2021)},
                        included=False
                    ),
                    html.P(""),
                    """
                    dbc.ButtonGroup(
                        id='borough-option-button',
                        children=[
                            #dbc.Button("All", id='borough-button-all'), 
                            dbc.Button("Manhattan", id='manhattan-button'), 
                            dbc.Button("Bronx", id='bronx-button'),
                            dbc.Button("Queen", id='queen-button'),
                            dbc.Button("Booklyn", id='brooklyn-button'),
                            dbc.Button("Staten Island", id='staten-island-button')
                        ],
                        loading_state={'is_loading': True, 'component_name':'borough-button-all'},
                        style={'width': '70%', 'float': 'Center', 'display': 'inline-block'}
                    )
                    """
                ], 
                style={'width': '70%', 'float': 'Center', 'display': 'inline-block'}
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
                                            html.P('Use radio to select view units for complete or incomplete projects'),
                                            dcc.Dropdown(
                                                id="net-effects-job-type-dropdown",
                                                options=[{
                                                    'label': x,
                                                    'value': x
                                                    } for x in ['All Job Types', 'Alteration Only', 'New Building and Demolition']
                                                ],
                                                value='Alteration Only'
                                            ),
                                            html.P('View by Year or by Boroughs'),
                                            dcc.Dropdown(
                                                id='net-effects-x-dropdown',
                                                options=[{
                                                    'label': x,
                                                    'value': x
                                                    } for x in ['By Year', 'By Borough']
                                                ],
                                                value='By Borough'
                                            ),
                                        ]
                                    )
                                )
                            ),
                            width={"size": 4}
                        ),
                        # this is the main graphics panel
                        dbc.Col(html.Div(id='net-effects-content'))
                    ]
                )
            ]
        ),
        className="mt-3"
    )

    return tab