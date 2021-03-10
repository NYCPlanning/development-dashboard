import pandas as pd
from sqlalchemy import create_engine

##########################
# Net Effects 
##########################

def load_net_effects_data(database, job_type, x_axis, boro=None, geometry=None, year_start=None, year_end=None):

    conn = create_engine(database)

    if x_axis == 'Citywide':

        if job_type == 'New Building and Demolition':

            job_type_str = "'New Building', 'Demolition'"

        elif job_type == 'Alteration Only':

            job_type_str = "'Alteration'"
        
        else:

            job_type_str = "'New Building', 'Demolition', 'Alteration'"

        df = pd.read_sql('''

        SELECT 
            complete_year AS year,
            SUM(classa_net) as total_classa_net,
            CASE WHEN classa_net::INTEGER < 0 THEN 'units_loss' 
            WHEN classa_net::INTEGER > 0 THEN 'units_gain' 
            END as units_flag
        
        FROM   
            export_devdb

        WHERE
            complete_year::INTEGER >= 2010
            AND
            job_type IN ({job_type})
            AND 
            classa_net::INTEGER <> 0
            AND 
            boro :: INTEGER IN ({boro})

        GROUP BY 
            complete_year,
            CASE WHEN classa_net::INTEGER < 0 THEN 'units_loss' 
            WHEN classa_net::INTEGER > 0 THEN 'units_gain' 
            END 
        
        '''.format(boro=boro, job_type=job_type_str ), con = conn)

        #print(df)

        return df

    else:

        if job_type == 'New Building and Demolition':

            job_type_str = "'New Building', 'Demolition'"

        elif job_type == 'Alteration Only':

            job_type_str = "'Alteration'"
        
        else:

            job_type_str = "'New Building', 'Demolition', 'Alteration'" 

        df = pd.read_sql('''

        SELECT 
            SUM(classa_net) as total_classa_net,
            {geometry} :: varchar AS {geometry},
            CASE WHEN classa_net::INTEGER < 0 THEN 'units_loss' 
            WHEN classa_net::INTEGER > 0 THEN 'units_gain' 
            END as units_flag
        
        FROM   
            export_devdb

        WHERE
            complete_year::INTEGER BETWEEN {year_start} AND {year_end} 
            AND
            job_type IN ({job_type})
            AND 
            classa_net::INTEGER <> 0
            AND 
            (LEFT({geometry} :: varchar, 1) :: INTEGER) = {boro}
            AND 
            job_inactive IS NULL

        GROUP BY 
            {geometry},
            CASE WHEN classa_net::INTEGER < 0 THEN 'units_loss' 
            WHEN classa_net::INTEGER > 0 THEN 'units_gain' 
            END 
        
        '''.format(year_start=year_start, year_end=year_end, boro=boro, job_type=job_type_str, geometry=geometry), con = conn)

        return df 