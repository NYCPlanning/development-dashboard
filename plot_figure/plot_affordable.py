import plotly.express as px
import requests
import pandas as pd
from pandas import json_normalize
import plotly.graph_objects as go

##########################
# affordable tab
##########################

def affordable_chart(df, df_char, percent_flag, char_flag):

    if percent_flag == 'Percentage':

        hover_temp = '<br><b> %{text} </b><br>' + '<i>Percentage</i>: %{y:.1%}<extra></extra>'

        n = 6

    else:

        hover_temp = '<br><b> %{text} </b><br>' + '<i>Units Count</i>: %{y}<extra></extra>'

        n = 5

    bar = go.Figure()

    bar.add_trace(
        go.Bar(
            x=df.boro, 
            y=df.other_units, 
            name='Non-HNY Units',
            text=['Non-HNY Units' for i in range(n)],
            hovertemplate=hover_temp
        )
    )

    bar.add_trace(
        go.Bar(
            x=df.boro,
            y=df.hny_units, 
            name='HNY Units',
            text=['HNY Units' for i in range(n)],
            hovertemplate=hover_temp
        )
    )

    bar.update_layout(title='Residential Units and HNY Units in 2015 or Later Projects', 
        barmode='stack', xaxis_tickangle=-45)

    # hny characteristics graphics starts here
    hny_bar = go.Figure()

    #charct_ls = df_char.columns[:-1]

    #print(charct_ls)


    #df_char = ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']
    for col in df_char.columns[:-1]:

        hny_bar.add_trace(
            go.Bar(
                x=df_char.borough, 
                y=df_char[col], 
                name=col.replace('_', ' '),
                text=[col.replace('_', ' ') for i in range(n)],
                hovertemplate=hover_temp
            )
        )

    hny_bar.update_layout(title='HNY Characteristics: Affordable Units by ' + char_flag, 
        hoverlabel_align = 'right',
        barmode='stack', xaxis_tickangle=-45)

    hny_bar.update_xaxes(categoryorder='array', categoryarray= ['Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island'])

    return bar, hny_bar