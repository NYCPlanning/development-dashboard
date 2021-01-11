import pandas as pd
from sqlalchemy import create_engine

##########################
# affordable data
##########################

def load_affordable_data(db, percent_flag, char_flag):

    boro_dict = {'1': 'Manhattan', '2': "Bronx", '3': "Brooklyn", '4': "Queens", '5': "Staten Island"}

    conn = create_engine(db)

    # connect to housing 
    hny_units = pd.read_sql('''
    SELECT 
        SUM(classa_hnyaff :: NUMERIC) as hny_units,
        (SUM(classa_net :: NUMERIC)  - SUM(classa_hnyaff :: NUMERIC)) as other_units,
        job_status,
        boro :: VARCHAR

    FROM   export_devdb

    WHERE
        permit_year :: INTEGER >= 2014
        AND job_inactive IS NULL

    GROUP BY 
        job_status,
        boro
    ''', con = conn)

    hny_units.boro = hny_units.boro.map(boro_dict)

    df_permit = hny_units.loc[hny_units.job_status == '3. Permitted for Construction']

    df_complete = hny_units.loc[hny_units.job_status == '5. Completed Construction']

    # charateristics of housing new york units to compile
    if char_flag == 'Income Level':

        attr_ls = ['extremely_low_income_units',
                    'very_low_income_units',
                    'low_income_units',
                    'moderate_income_units',
                    'middle_income_units',
                    'other_income_units'
                ]

        df_char = pd.read_sql('''

        SELECT 
            SUM({0} :: INTEGER) as "Extremely_Low_Income_Units",
            SUM({1} :: INTEGER) as "Very_Low_Income_Units", 
            SUM({2} :: INTEGER) as "Low_Income_Units",
            SUM({3} :: INTEGER) as "Moderate_Income_Units",
            SUM({4} :: INTEGER) as "Middle_Income_Units",
            SUM({5} :: INTEGER) as "Other_Income_Units",
            borough 

        FROM hpd_hny_units_by_building

        WHERE
        RIGHT(project_completion_date :: varchar, 4) :: NUMERIC >= 2015 
        AND 
        reporting_construction_type = 'New Construction'

        GROUP BY
            borough
        '''.format(attr_ls[0], attr_ls[1], attr_ls[2], attr_ls[3], attr_ls[4], attr_ls[5]), con= conn)

    elif char_flag == 'Number of Bedrooms':

        attr_ls = ['studio_units',
                    '1_br_units',
                    '2_br_units',
                    '3_br_units',
                    '4_br_units',
                    '5_br_units',
                    '6_br+_units',
                    'unknown_br_units'
                    ]

        df_char = pd.read_sql('''

        SELECT 
            SUM({0} :: INTEGER) as "Studio_Units",
            SUM("{1}" :: INTEGER) as "1-Bedroom_Units", 
            SUM("{2}" :: INTEGER) as "2-Bedroom_Units",
            SUM("{3}" :: INTEGER) as "3-Bedroom_Units",
            SUM("{4}" :: INTEGER) as "4-Bedroom_Units",
            SUM("{5}" :: INTEGER) as "5-Bedroom_Units",
            SUM("{6}" :: INTEGER) as "Unknown",
            borough 

        FROM hpd_hny_units_by_building

        WHERE
        RIGHT(project_completion_date :: varchar, 4) :: NUMERIC >= 2015 
        AND 
        reporting_construction_type = 'New Construction'

        GROUP BY
            borough
        '''.format(attr_ls[0], attr_ls[1], attr_ls[2], attr_ls[3], attr_ls[4], attr_ls[5], attr_ls[6]), con=conn)

    else:

        attr_ls = ['counted_rental_units', 'counted_homeownership_units']

        df_char = pd.read_sql('''

        SELECT 
            SUM({0} :: INTEGER) as "Rental_Units",
            SUM({1} :: INTEGER) as "Homeownership_Units", 
            borough 

        FROM hpd_hny_units_by_building

        WHERE
        RIGHT(project_completion_date :: varchar, 4) :: NUMERIC >= 2015
        AND 
        reporting_construction_type = 'New Construction'

        GROUP BY
            borough
        '''.format(attr_ls[0], attr_ls[1]), con= conn)
    
    if percent_flag == 'Percentage':
        
        df_char.loc[5] = list(df_char.iloc[:, :-1].sum(axis=0)) + ['Citywide']

        df_complete.loc[5] = list(df_complete.iloc[:, :-1].sum(axis=0)) + ['Citywide']

        for i in range(6):

            df_char.iloc[i, :-1] = (df_char.iloc[i, :-1] / df_char.iloc[i, :-1].sum())

            df_complete.iloc[i, :-2] = (df_complete.iloc[i, :-2] / df_complete.iloc[i, :-2].sum())

    return df_complete, df_char