import plotly.express as px
import requests
import pandas as pd
from pandas import json_normalize
import plotly.graph_objects as go


def zoning_district_chart(df, norm_flag):

    boroughs = ['', 'Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']

    bar_units = go.Figure()

    bar_land_area = go.Figure()

    for flag in df.units_flag.unique():

        if norm_flag:

            bar_units.add_trace(
                go.Bar(
                    x=df.loc[df.units_flag == flag].typo,
                    y=df.loc[df.units_flag == flag].normalized_units,
                    text=df.loc[df.units_flag == flag].normalized_units, 
                    name=flag,
                    textposition='outside',
                    hoverinfo='skip'
                )
            )

        else:

            bar_units.add_trace(
                go.Bar(
                    x=df.loc[df.units_flag == flag].typo,
                    y=df.loc[df.units_flag == flag].net_units,
                    text=df.loc[df.units_flag == flag].net_units, 
                    name=flag,
                    textposition='outside',
                    hoverinfo='skip'
                )
            )

        net_table_zd = df.groupby('typo').net_units.sum().reset_index()

        bar_units.add_trace(
            go.Scatter(
                x=net_table_zd.typo, 
                y=net_table_zd.net_units, 
                mode='markers', 
                name='net units outcome', 
                textposition='top center',
                hovertemplate='<br><b> %{x} </b><br>' + '<i>Net Units</i>: %{y} <extra></extra>'
            )
        )

        bar_units.update_layout(title='Net Effects by Zoning District Typology ', 
            barmode='relative', xaxis_tickangle=-45)

        bar_land_area.add_trace(
            go.Bar(
                x=df.loc[df.units_flag == flag].typo,
                y=df.loc[df.units_flag == flag].total_lot_area,
                text=df.loc[df.units_flag == flag].total_lot_area, 
                name=flag,
                textposition='outside',
                hoverinfo='skip'
            )
        )


    return bar_units, bar_land_area