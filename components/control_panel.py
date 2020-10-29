import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_ui as dui


def create_control_panel():

    controlpanel = dui.ControlPanel(_id="controlpanel")

    boro_options = [
    'Manhattan',
    'Bronx',
    'Brooklyn',
    'Queens',
   'Staten Island'
    ]

    # 
    controlpanel.create_section(
        section='FirstSection',
        section_title='First Section'
    )

    controlpanel.create_group(
        group="OnlyGroup",
        group_title="Only Group"
    )

    toggle = dcc.Dropdown(
        id="quick-dropdown",
        options=[{
            'label': x,
            'value': x
            } for x in ['First Look', 'Second Look']
        ],
        value='First Look'
    )

    controlpanel.add_element(toggle, 'OnlyGroup')

    controlpanel.add_groups_to_section('FirstSection', ['OnlyGroup'])


    # what is the 
    controlpanel.create_section(
        section='ExtentSection',
        section_title='Citywide Section'
    )

    # what is group 
    controlpanel.create_group(
        group="CitywideOptions",
        group_title="Citywide Options Selections"
    )


    # create the elements for citywide group then add the appropriate elements to the groups
    job_type_select = dcc.Dropdown(
        id="job-type-dropdown",
        options=[{
            'label': x,
            'value': x
            } for x in ['New Building', 'Demolition', 'Alteration']
        ],
        value='New Building'
    )

    cum_seg_select = dcc.RadioItems(
        id='cum-seg-radio',
        options=[
            {'label': 'Cumulative', 'value': 0},
            {'label': 'Segregate', 'value': 1},
        ],
        value=1,
        labelStyle={'display': 'inline-block'}
    )  

    permit_complete = dbc.DropdownMenu(
        label="permit/completion",
        children=[
            dbc.DropdownMenuItem("completion date"),
            dbc.DropdownMenuItem("permit date"),
        ],
    )

    controlpanel.add_element(job_type_select, "CitywideOptions")

    controlpanel.add_element(cum_seg_select, "CitywideOptions")

    controlpanel.add_element(permit_complete, 'CitywideOptions')

    # add groups to the first sections
    controlpanel.add_groups_to_section('ExtentSection', ['CitywideOptions'])

    #controlpanel.add_groups_to_section('SecondSection', ['City'])

    # testing for second sections
    controlpanel.create_section(
        section='SecondSection',
        section_title='Community District Section'
    )

    controlpanel.create_group(
        group='CommunityDistrictOptions',
        group_title='Community District Options'
    )

    boro_slct = dcc.Dropdown(
            id='boro-dropdown',
            options=[{'label': k, 'value': k} for k in boro_options],
            value='Manhattan'
        )
    
    controlpanel.add_element(boro_slct, 'CommunityDistrictOptions')

    controlpanel.add_groups_to_section('SecondSection', ['CommunityDistrictOptions'])

    return controlpanel

