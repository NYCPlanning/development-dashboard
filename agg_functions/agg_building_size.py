import pandas as pd
from sqlalchemy import create_engine

##########################
# building size data 
##########################

def load_building_size_data(db, job_type, percent_flag):

    conn = create_engine(db)

    stats = pd.read_sql('''
    SELECT 
        classa_net

    FROM 
        export_devdb

    WHERE
        complete_year::INTEGER >= 2010
        AND
        job_type = '{job_type}'
    '''.format(job_type=job_type), con=conn)

   
    df = pd.read_sql('''
    SELECT 
        complete_year AS year,
        SUM(ABS(classa_net)) as net_residential_units,
        --- job_type,
        CASE WHEN ABS(classa_net) BETWEEN 1 AND 2 THEN '1 to 2 units'
        WHEN ABS(classa_net) between 3 and 5 THEN '3 to 5 units' 
        WHEN ABS(classa_net) between 6 and 10 THEN '6 to 10 units'
        WHEN ABS(classa_net) between 11 and 25 THEN '11 to 25 units'
        WHEN ABS(classa_net) between 26 and 100 THEN '26 to 100 units'
        WHEN ABS(classa_net) > 100 THEN '> 100 units'
        END as units_class
    
    FROM   
        export_devdb

    WHERE
        complete_year::INTEGER >= 2010
        AND
        job_type = '{job_type}'

    GROUP BY 
        complete_year,
        --- job_type,
        CASE WHEN ABS(classa_net) BETWEEN 1 AND 2 THEN '1 to 2 units'
        WHEN ABS(classa_net) between 3 and 5 THEN '3 to 5 units' 
        WHEN ABS(classa_net) between 6 and 10 THEN '6 to 10 units'
        WHEN ABS(classa_net) between 11 and 25 THEN '11 to 25 units'
        WHEN ABS(classa_net) between 26 and 100 THEN '26 to 100 units'
        WHEN ABS(classa_net) > 100 THEN '> 100 units'
        END
    '''.format(job_type=job_type), con = conn)

    if percent_flag == 'Percentage':

        df_gb = df.groupby(['year', 'units_class']).agg({'net_residential_units': 'sum'})

        df = df_gb.groupby(level=0).apply(lambda x: x / float(x.sum()))

        df.reset_index(inplace=True)

    return df, stats
