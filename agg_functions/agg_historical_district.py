import pandas as pd
from sqlalchemy import create_engine

def load_historical_district_data(database, boro, percent_flag, net_flag, norm_flag):

    conn = create_engine(database)

    # connect to housing 
    df = pd.read_sql('''
        SELECT 
        SUM(devdb.classa_net) as classa_net,
        ROUND(SUM(pluto.lotarea) / 43560) as total_lot_area,
        typology.typ_2020_03_value as typo_value,
        typology.typ_2020_03_name as typo,
        CASE 
        WHEN ((pluto.histdist IS NULL) AND (pluto.landmark IS NULL)) THEN 'nonhist'
        ELSE 'hist'
        END AS hist_flag

        FROM   dcp_mappluto AS pluto LEFT OUTER JOIN old_export_devdb AS devdb ON pluto.bbl = devdb.bbl 
        LEFT JOIN zoning_typology_map AS typology ON devdb.zoningdist1 = typology.zonedist1

        WHERE 
        devdb.job_inactive IS NULL
        AND 
        pluto.residfar :: NUMERIC > 0
        AND 
        devdb.boro :: NUMERIC IN ({boro})
        AND 
        devdb.job_inactive IS NULL
        AND
        devdb.complete_year::INTEGER >= 2010
        AND
        devdb.bbl :: NUMERIC <>  1000010010  --- hard coded to exclude the Governor Island's bbl
        
        GROUP BY 
        typology.typ_2020_03_value,
        typology.typ_2020_03_name,
        CASE 
        WHEN ((pluto.histdist IS NULL) AND (pluto.landmark IS NULL)) THEN 'nonhist'
        ELSE 'hist'
        END
    '''.format(boro=boro), con = conn)

    df['normalized_units'] = df['classa_net'] / df['total_lot_area']

    df = df.round({'normalized_units': 0})

    df.dropna(axis=0, subset=['typo_value'], inplace=True)

    return df