import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table

def create_net_effects_tab(app):

    @app.callback(Output('net-effects-control', 'children'), [Input('net-effects-x-dropdown', 'value')])
    def create_net_effects_control_panel(x_dropdown):

        if x_dropdown == 'By Borough':

            widgets = html.Div(
                        [
                            html.P('Please use the options to select a borough to view its community district data'),                                
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
                            html.P('Please select the geometries to join the'),
                            dcc.Dropdown(
                                id='net-effects-geometries',
                                options=[
                                    {'label': 'Community District', 'value': 'comunitydist'},
                                    {'label': 'Census Tract', 'value': 'bct2010'}
                                ],
                                value='comunitydist'
                            ),
                            html.P('Use the slider to select a year or the range of years'),
                            dcc.RangeSlider(
                                id='net-effects-year-slider',
                                min=2010,
                                max=2020,
                                value=[2010, 2020],
                                marks={str(year): str(year) for year in range(2010, 2021)},
                                included=True
                            )
                        ]
            )

        else:

            widgets = html.Div(
                [
                    html.P('Choose a borough if want to see only the data for one borough'), 
                    dcc.RadioItems(
                        id='net-effects-citywide-boro-radio',
                        options=[
                            {'label': 'All Boroughs', 'value': '1, 2, 3, 4, 5'},
                            {'label': 'Manhattan', 'value': 1},
                            {'label': 'Bronx', 'value': 2},
                            {'label': 'Brooklyn', 'value': 3},
                            {'label': 'Queens', 'value': 4},
                            {'label': 'Staten Island', 'value': 5},
                            
                        ],
                        value='1, 2, 3, 4, 5',
                        #labelStyle={'display': 'inline-block'}
                    )
                ]
            )


        return widgets

    @app.callback(Output('net-effects-content', 'children'), [Input('net-effects-x-dropdown', 'value')])
    def create_net_effects_content(x_dropdown):

        if x_dropdown == 'Citywide':

            content = html.Div(
                [
                    dcc.Graph(id='net-effects-citywide-bar'),
                    #dcc.Graph(id='net-effects-zd-bar')
                ]
            )
            

        else:

            boro_options = ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']

            content = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(id='net-effects-boro-choro')
                            ),
                            #dbc.Col(
                            #    dcc.Graph(id='net-effects-boro-bar')
                            #)
                        ]
                    ),
                    dbc.Row(
                        dcc.Graph(id='net-effects-boro-bar')
                    ),
                    dbc.Row(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div(id='net-effects-boro-datatable')
                                ]
                            )
                        )
                    )
                ], 
                style={'width': '100%', 'float': 'Center', 'display': 'inline-block'}
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
                                            html.P('Use dropdown to select view units for complete or incomplete projects'),
                                            dcc.Dropdown(
                                                id="net-effects-job-type-dropdown",
                                                options=[{
                                                    'label': x,
                                                    'value': x
                                                    } for x in ['All Job Types', 'Alteration Only', 'New Building and Demolition']
                                                ],
                                                value='Alteration Only'
                                            ),
                                            html.P('View Citywide or by Boroughs'),
                                            dcc.Dropdown(
                                                id='net-effects-x-dropdown',
                                                options=[{
                                                    'label': x,
                                                    'value': x
                                                    } for x in ['Citywide', 'By Borough']
                                                ],
                                                value='Citywide'
                                            ),
                                            html.Div(id='net-effects-control')
                                        ]
                                    )
                                )
                            ),
                            width={"size": 3}
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