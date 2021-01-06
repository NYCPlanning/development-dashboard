import plotly.express as px
import requests
import pandas as pd
from pandas import json_normalize
import plotly.graph_objects as go

##########################
# building size tab
##########################
def building_size_bar(df, job_type, percent_flag):

    # percentage or units count 
    if percent_flag == 'Percentage':

        hover_temp = '<br><b> %{text} </b><br>' + '<i>Percentage</i>: %{y:.1%}<extra></extra>'

    else:

        hover_temp = '<br><b> %{text} </b><br>' + '<i>Units Count</i>: %{y}<extra></extra>'


    # set the figure 
    fig = go.Figure()

    print(df.units_class.unique())

    uclass = ['1 to 2 unit buildings', '3 to 5','6 to 10','11 to 25' , '26 to 100', '> 100' , None]

    uclass.reverse()

    for uc in uclass:

        fig.add_trace(
            go.Bar(
                x=df.loc[df.units_class == uc].year, 
                y=df.loc[df.units_class == uc].net_residential_units, 
                name=uc, 
                text=[uc for i in range(11)],
                hovertemplate=hover_temp
            )
        )
    
    fig.update_layout(
        title=job_type + ' Completed Residential Units by Number of Units in Buildings', 
        #legend_traceorder=['1 to 2 unit buildings', '3 to 5', '6 to 10', '11 to 25', '26 to 100', '> 100'],
        # https://community.plotly.com/t/customizing-the-order-of-legends/12668 no ability to sort the at the moment
        barmode='stack', 
        xaxis_tickangle=-45,
        # this could only works with keywords such as group/reverse/
        #legend={'traceorder': }
    )

    return fig
