import pandas as pd
from sqlalchemy import create_engine

def load_zoning_district_data(database, boro, percent_flag, net_flag, norm_flag):

    conn = create_engine(database)

    df = pd.read_sql('''

    SELECT 
        complete_year AS year,
        SUM(classa_net) as total_classa_net,
        job_type,
        nta2010 as nta, 
        CASE WHEN classa_net::INTEGER < 0 THEN 'units_loss' 
        WHEN classa_net::INTEGER > 0 THEN 'units_gain' 
        END as units_flag
    
    FROM   
        old_export_devdb

    WHERE
        complete_year::INTEGER >= 2010
        AND 
        classa_net::INTEGER <> 0
        AND 
        boro :: INTEGER IN ({boro})

    GROUP BY 
        complete_year,
        job_type,
        CASE WHEN classa_net::INTEGER < 0 THEN 'units_loss' 
        WHEN classa_net::INTEGER > 0 THEN 'units_gain' 
        END 
    
    '''.format(boro=boro, job_type=job_type_str ), con = conn)

    #print(df)

    return df
