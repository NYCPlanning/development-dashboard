import plotly.express as px
import requests
import pandas as pd
from pandas import json_normalize
import plotly.graph_objects as go


def net_effects_chart(df, mapbox_token, job_type, x_axis, boro, df_zd=None, geometry=None):

    boroughs = ['', 'Manhattan', 'Bronx', 'Brooklyn', 'Queens', 'Staten Island']

    if x_axis == 'Citywide':

        bar = go.Figure()

        for flag in df.units_flag.unique():

            bar.add_trace(
                go.Bar(
                    x=df.loc[df.units_flag == flag].year, 
                    y=df.loc[df.units_flag == flag].total_classa_net, 
                    name=flag.replace('_', ' '),
                    text=df.loc[df.units_flag == flag].total_classa_net, 
                    textposition='outside')
            )

        net_table = df.groupby('year').total_classa_net.sum().reset_index()

        bar.add_trace(
            go.Scatter(
                x=net_table.year, 
                y=net_table.total_classa_net, 
                mode='markers', 
                name='net units outcome', 
                textposition='top center')
        )

        bar.update_layout(title='Net Effects on Residential Units ' + job_type, 
            barmode='relative', xaxis_tickangle=-45)

        # zoning district net effects
        zd_bar = go.Figure()

        for flag in df.units_flag.unique():

            zd_bar.add_trace(
                go.Bar(
                    x=df_zd.loc[df_zd.units_flag == flag].typo,
                    y=df_zd.loc[df_zd.units_flag == flag].net_units,
                    name=flag.replace('_', ' '),
                    text=df_zd.loc[df_zd.units_flag == flag].net_units, 
                    textposition='outside',
                    hoverinfo='skip'
                )
            )

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

        return bar, zd_bar
    
    else:

        bar = go.Figure()

        for flag in df.units_flag.unique():

            bar.add_trace(
                go.Bar(
                    x=df.loc[df.units_flag == flag].total_classa_net, 
                    y=df.loc[df.units_flag == flag][geometry], 
                    orientation='h', 
                    name=flag.replace('_', ' '),
                    text=df.loc[df.units_flag == flag].total_classa_net,
                    textposition='outside',
                    hoverinfo='skip'
                )
            )

        net_table = df.groupby(geometry).total_classa_net.sum().reset_index()

        #print(net_table)

        bar.add_trace(
            go.Scatter(
                x=net_table.total_classa_net, 
                y=net_table[geometry], 
                mode='markers', 
                name='net units outcome',
                text=net_table.total_classa_net,
                hovertemplate='<br><b>Community District %{y} </b><br>' + '<i>Net Units</i>: %{text}<extra></extra>'
            )
        )

        bar.update_layout(
            title='Net Effects on Residential Units ' + job_type, 
            barmode='relative', 
            xaxis_tickangle=-45
        )

        bar.update_yaxes(type='category')
        
        # choropleth
        if geometry == 'comunitydist':
            
            response = requests.get('https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Community_Districts/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson')

            featureidkey = "properties.BoroCD"

        else:

            response = requests.get('https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Census_Tracts_for_2010_US_Census/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson')

            featureidkey = "properties.BoroCT2010"
            
        geojson = response.json()

        # aggregate by community district 
        cd_choro = df.groupby(geometry)['total_classa_net'].sum().reset_index()

        fig_choro = go.Figure(
            go.Choroplethmapbox(
                geojson=geojson, 
                locations=cd_choro.iloc[:, 0], 
                z=cd_choro.total_classa_net,
                colorscale='Greens',
                marker_opacity=1.0, 
                marker_line_width=0, 
                featureidkey=featureidkey
            )
        )

        # lat long for different borough  
        center_dict = {
            1: (40.7831, -73.9712), 
            2: (40.8448, -73.8648), 
            3: (40.6782, -73.9442), 
            4: (40.7282, -73.7949), 
            5: (40.5795, -74.1502)
        }

        fig_choro.update_layout(
            title_text=boroughs[boro] + ' Net Effects ' + job_type + ' Jobs',
            mapbox_accesstoken=mapbox_token, 
            mapbox_style="carto-positron",
            mapbox_zoom=10, 
            mapbox_center = {"lat": center_dict[boro][0], "lon": center_dict[boro][1]},
            margin={"r":0,"t":0,"l":0,"b":0}
        )

        return bar, fig_choro