import pandas as pd
from sqlalchemy import create_engine

def load_zoning_district_data(database, boro, percent_flag, net_flag, norm_flag):

    conn = create_engine(database)

    df = pd.read_sql('''

    SELECT 
        SUM(devdb.classa_net) as net_units,
        ROUND(SUM(pluto.lotarea) / 43560) as total_lot_area,
        typology.typo_wwl_value as typo_value,
        typology.typo_wwl as typo,
        CASE 
        WHEN devdb.classa_net::INTEGER < 0 THEN 'units_loss' 
        WHEN devdb.classa_net::INTEGER > 0 THEN 'units_gain' 
        END as units_flag


        FROM   dcp_mappluto AS pluto LEFT OUTER JOIN old_export_devdb AS devdb ON pluto.bbl = devdb.bbl 
        LEFT JOIN zoning_typology_map AS typology ON devdb.zoningdist1 = typology.zonedist1

    WHERE 
        job_inactive IS NULL
        AND 
        boro :: NUMERIC IN ({boro})
        AND 
        complete_year :: NUMERIC >= 2010

    GROUP BY
        typology.typo_wwl_value,
        typology.typo_wwl,
        CASE WHEN classa_net::INTEGER < 0 THEN 'units_loss' 
        WHEN classa_net::INTEGER > 0 THEN 'units_gain' 
        END

    '''.format(boro=boro), con = conn)

    sql = '''

    SELECT 
    pluto.bbl,
    pluto.zonedist1,
    pluto.residfar,
    typology.typo_wwl as typo,
    pluto.wkb_geometry

    FROM   dcp_mappluto AS pluto LEFT JOIN zoning_typology_map AS typology ON pluto.zonedist1 = typology.zonedist1
    '''

    #df_rm = gpd.GeoDataFrame.from_postgis(sql, conn, geom_col='wkb_geometry')


    return df#, df_rm