import pandas as pd
from sqlalchemy import create_engine

##########################
# boro level management
##########################

def load_num_dev_res_units_data(db, yr, job_type, year_flag):

    conn = create_engine(db)

    # what are the year 
    df = pd.read_sql('''
    SELECT 
        {0} as year,
        coalesce(COUNT(*), 0) as num_dev,
        job_type, 
        SUM(classa_net :: NUMERIC) as total_res_units_net,
        bct2010 
        
    FROM   final_devdb

    WHERE
        {0} :: INTEGER >= 2010
        AND 
        job_inactive IS NULL

    GROUP  BY
        {0},
        job_type, 
        bct2010
    '''.format(year_flag), con = conn)

    # the dataframe is either aggregated across all years for one job type or simply one year is selected
    if yr == 'All Years':

        ftd_df = df.loc[(df.job_type == job_type)].groupby('bct2010')['total_res_units_net'].agg('sum').reset_index()

    else:

        ftd_df = df.loc[(df.job_type == job_type) & (df.year == int(yr))]

    return ftd_df


##########################
# boro level management
##########################

def load_community_district_data(db, boro, year_flag):

    boro_dict = {'Manhattan': 1, "Bronx": 2, "Brooklyn": 3, "Queens": 4, "Staten Island": 5}

    # connect 
    conn = create_engine(db)
   
    agg_db = pd.read_sql('''
    SELECT 
        {yf} AS year,
        comunitydist AS cd, 
        SUM(classa_net :: INTEGER) as num_net_units
    
    FROM   
        final_devdb

    WHERE
        {yf} :: INTEGER >= 2010
        AND 
        boro::INTEGER = {slct_boro}

    GROUP BY 
        {yf},
        comunitydist
    '''.format(yf=year_flag, slct_boro=boro_dict[boro]), con = conn)


    agg_db.dropna(subset=['num_net_units'], inplace=True)

    agg_db.cd = agg_db.cd.astype(str)

    return agg_db

##########################
# affordable data
##########################

def load_affordable_data(db, status):

    boro_dict = {'1': 'Manhattan', '2': "Bronx", '3': "Brooklyn", '4': "Queens", '5': "Staten Island"}

    conn = create_engine(db)

    # connect 
    agg_db = pd.read_sql('''
    SELECT 
        SUM(classa_net :: NUMERIC) as total_units_net,
        SUM(classa_hnyaff :: NUMERIC) as total_hny_units_net,
        job_status,
        boro

    FROM   final_devdb

    WHERE
        permit_year :: INTEGER >= 2014
        AND job_inactive IS NULL

    GROUP  BY 
        job_status,
        boro
    ''', con = conn)

    agg_db.boro = agg_db.boro.map(boro_dict)

    df_permit = agg_db.loc[agg_db.job_status == '3. Permitted for Construction']

    df_complete = agg_db.loc[agg_db.job_status == '5. Completed Construction']

    return df_permit if status == 'Incomplete' else df_complete

##########################
# building size data 
##########################

def load_building_size_data(db):

    conn = create_engine(db)
   
    agg_db = pd.read_sql('''
    SELECT 
        complete_year AS year,
        SUM(ABS(classa_net)) as net_residential_units,
        job_type,
        CASE WHEN ABS(classa_net) BETWEEN 1 AND 2 THEN '1 to 2 unit buildings'
        WHEN ABS(classa_net) between 3 and 5 THEN '3 to 5' 
        WHEN ABS(classa_net) between 6 and 10 THEN '6 to 10'
        WHEN ABS(classa_net) between 11 and 25 THEN '11 to 25'
        WHEN ABS(classa_net) between 26 and 100 THEN '26 to 100'
        WHEN ABS(classa_net) > 100 THEN '> 100'
        END as units_class
    
    FROM   
        final_devdb

    WHERE
        complete_year::INTEGER >= 2010
        AND
        job_type <> 'Alteration'

    GROUP BY 
        complete_year,
        job_type,
        CASE WHEN ABS(classa_net) BETWEEN 1 AND 2 THEN '1 to 2 unit buildings'
        WHEN ABS(classa_net) between 3 and 5 THEN '3 to 5' 
        WHEN ABS(classa_net) between 6 and 10 THEN '6 to 10'
        WHEN ABS(classa_net) between 11 and 25 THEN '11 to 25'
        WHEN ABS(classa_net) between 26 and 100 THEN '26 to 100'
        WHEN ABS(classa_net) > 100 THEN '> 100'
        END
    ''', con = conn)

    return agg_db

##########################
# Net Effects 
##########################

def load_net_effects_data(db):

    conn = create_engine(db)

    agg_db = pd.read_sql('''
    SELECT 
        complete_year AS year,
        SUM(classa_net) as total_classa_net,
        CASE WHEN classa_net::INTEGER < 0 THEN 'units_loss' 
        WHEN classa_net::INTEGER > 0 THEN 'units_gain' 
        END as units_flag
    
    FROM   
        final_devdb

    WHERE
        complete_year::INTEGER >= 2010
        AND
        job_type = 'Alteration'
        AND 
        classa_net::INTEGER <> 0

    GROUP BY 
        complete_year,
        CASE WHEN classa_net::INTEGER < 0 THEN 'units_loss' 
        WHEN classa_net::INTEGER > 0 THEN 'units_gain' 
        END 
    
    ''', con = conn)

    return agg_db