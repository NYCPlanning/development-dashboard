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
                                                id="building-size-job-type-dropdown",
                                                options=[{
                                                    'label': x,
                                                    'value': x
                                                    } for x in ['New Building', 'Demolition']
                                                ],
                                                value='New Building'
                                            ),
                                            html.P('Choose to view the charts in units or percentage'),
                                            dcc.RadioItems(
                                                id='building-size-percent-radio',
                                                options=[
                                                    {'label': 'Units', 'value': 'Units'},
                                                    {'label': 'Percentage', 'value': 'Percentage'},
                                                ],
                                                value='Units',
                                                labelStyle={'display': 'inline-block'}
                                            ),
                                        ]
                                    )
                                )
                            ),
                            width={"size": 4}
                        ),
                        # this is the summary statistics and graphics
                        dbc.Col(
                            [                            
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Card(
                                                dbc.CardBody(
                                                    [
                                                        html.H2(id='building-size-median', className='card-title'),
                                                        html.P('Median Number of Units Per Building', className='card-text')
                                                    ]
                                                ),
                                                color='success', inverse=True
                                            ),
                                            width='auto'
                                        ),
                                        dbc.Col(
                                            dbc.Card(
                                                dbc.CardBody(
                                                    [                                                    
                                                        html.H2(id='building-size-mean', className='card-title'),
                                                        html.P('Average Number of Units Per Building', className='card-text')
                                                    ]
                                                ),
                                                color='success', inverse=True
                                            ),
                                            width='auto'
                                        ),
                                        dbc.Col(
                                            #dbc.Card(
                                                #dbc.CardBody(
                                                    #[                                                    
                                                        #html.H2('Something else', className='card-title'),
                                                        #html.P('something else', className='card-text')
                                                    #]
                                                #),
                                                #color='success', inverse=True
                                            #),
                                            #width='auto'
                                        )
                                    ]
                                ),
                                dbc.Row(
                                    dbc.Col(
                                        dcc.Graph(id='building-size-graphic'),
                                    )
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