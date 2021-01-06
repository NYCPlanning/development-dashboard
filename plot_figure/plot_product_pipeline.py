import plotly.express as px
import requests
import pandas as pd
from pandas import json_normalize
import plotly.graph_objects as go

def citywide_choropleth(df, mapbox_token, job_type, job_units, normalization):

    # get the geojson needed for the mapping 
    response = requests.get('https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Census_Tracts_for_2010_US_Census/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson')
    #response = requests.get('https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Census_Tracts_for_2010_US_Census_Water_Included/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson')

    geojson = response.json()

    geofeatures = json_normalize(geojson["features"])

    geofeatures['acreage'] = geofeatures['properties.Shape__Area'].astype(float) / 43560.

    merged = df.merge(geofeatures[['properties.BoroCT2010', 'acreage']], left_on='bct2010', right_on='properties.BoroCT2010', how='inner')

    # this step normalizes jobs/units to be by acre
    merged['units_per_acre'] = merged[job_units] / merged.acreage

    # if the normalization specifies then 
    if normalization == 'units_per_acre':

        params = {
            'max': merged[normalization].max(),
            'min': merged[normalization].min(),
            'job_type': job_type
        }

    else:
        # if the unormalized, then it should be raw count of units or number of jobs 
        params = {
            'max': merged[job_units].max(),
            'min': merged[job_units].min(),
            'job_type': job_type
        }

    if params['job_type'] == "'Demolition'":
        cs = 'Reds'
        rs = True
    elif params['job_type'] == "'New Building'":
        cs = 'Blues'
        rs = False
    else:
        cs = 'Bluered'
        rs = None

    fig = go.Figure(go.Choroplethmapbox(geojson=geojson, locations=merged.bct2010, z=merged[normalization],
                                    colorscale=cs, reversescale=rs, zmin=params['min'], zmax=params['max'],
                                    marker_opacity=1.0, marker_line_width=0, featureidkey="properties.BoroCT2010"))

    fig.update_layout(mapbox_accesstoken=mapbox_token, mapbox_style="carto-positron",
                    mapbox_zoom=9, mapbox_center = {"lat": 40.730610, "lon": -73.935242}, margin={"r":0,"t":0,"l":0,"b":0})

    return fig


def community_district_choropleth(agg_db, job_type, boro, mapbox_token):

    response = requests.get('https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Community_Districts/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson')
    
    geojson = response.json()

    # aggregate by community district 
    cd_choro = agg_db.groupby('cd')['num_net_units'].sum().reset_index()

    # params
    if job_type == "'Demolition'":
        cs = 'Reds'
        rs = True
    elif job_type == "'New Building'":
        cs = 'Blues'
        rs = False
    else:
        cs = 'Bluered'
        rs = None

    fig_choro = go.Figure(go.Choroplethmapbox(geojson=geojson, locations=cd_choro.cd, z=cd_choro.num_net_units, 
                                colorscale=cs, reversescale=rs,
                                marker_opacity=1.0, marker_line_width=0, featureidkey="properties.BoroCD"))

    # lat long for different borough  
    center_dict = {
        1: (40.7831, -73.9712), 
        2: (40.8448, -73.8648), 
        3: (40.6782, -73.9442), 
        4: (40.7282, -73.7949), 
        5: (40.5795, -74.1502)
    }


    fig_choro.update_layout(
        mapbox_accesstoken=mapbox_token, 
        mapbox_style="carto-positron",
        mapbox_zoom=10, 
        mapbox_center = {"lat": center_dict[boro][0], "lon": center_dict[boro][1]}
    )

    fig_choro.update_geos(fitbounds="locations", visible=False)
    fig_choro.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
 
    # the bar chart graphic
    fig_bar = px.bar(agg_db, x='cd', y='num_net_units', color='year', barmode='stack', 
        title='Number Units by Year and Community District')

    fig_bar.update_layout(xaxis={"type":"category"})

    # create a line chart for different number of units in community districts over years 
    fig_line = px.line(agg_db, x='year', y='num_net_units', color='cd', title='Number of Units Between 2010 and Now')

    return fig_choro, fig_bar, fig_line
