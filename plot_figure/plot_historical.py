import plotly.express as px
import requests
import pandas as pd
from pandas import json_normalize
import plotly.graph_objects as go



def historical_chart(df, norm_flag):

    boroughs = ['', 'Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']

    bar_units = go.Figure()

    bar_land_area = go.Figure()

    for flag in df.hist_flag.unique():

        if norm_flag:

            bar_units.add_trace(
                go.Bar(
                    x=df.loc[df.hist_flag == flag].typo,
                    y=df.loc[df.hist_flag == flag].normalized_units,
                    text=df.loc[df.hist_flag == flag].normalized_units, 
                    name=flag,
                    textposition='outside',
                    hoverinfo='skip'
                )
            )

        else:

            bar_units.add_trace(
                go.Bar(
                    x=df.loc[df.hist_flag == flag].typo,
                    y=df.loc[df.hist_flag == flag].classa_net,
                    text=df.loc[df.hist_flag == flag].classa_net, 
                    name=flag,
                    textposition='outside',
                    hoverinfo='skip'
                )
            )

        bar_land_area.add_trace(
            go.Bar(
                x=df.loc[df.hist_flag == flag].typo,
                y=df.loc[df.hist_flag == flag].total_lot_area,
                text=df.loc[df.hist_flag == flag].total_lot_area, 
                name=flag,
                textposition='outside',
                hoverinfo='skip'
            )
        )

    return bar_units, bar_land_area

    """
    net_table_zd = df_zd.groupby('typo').net_units.sum().reset_index()

    zd_bar.add_trace(
        go.Scatter(
            x=net_table_zd.typo, 
            y=net_table_zd.net_units, 
            mode='markers', 
            name='net units outcome', 
            textposition='top center',
            hovertemplate='<br><b> %{x} </b><br>' + '<i>Net Units</i>: %{y} <extra></extra>'
        )
    )

    zd_bar.update_layout(title='Net Effects by Zoning District Typology ' + job_type, 
        barmode='relative', xaxis_tickangle=-45)
    """