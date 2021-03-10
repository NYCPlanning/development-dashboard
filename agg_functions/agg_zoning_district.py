import pandas as pd
from sqlalchemy import create_engine

def load_zoning_district_data(database, boro, percent_flag, net_flag, norm_flag):

    conn = create_engine(database)

    df = pd.read_sql('''

    SELECT 
        SUM(devdb.classa_net) as net_units,
        ROUND(SUM(pluto.lotarea) / 43560) as total_lot_area,
        typology.typ_2020_03_value as typo_value,
        typology.typ_2020_03_name as typo,
        CASE 
        WHEN devdb.classa_net::INTEGER < 0 THEN 'units_loss' 
        WHEN devdb.classa_net::INTEGER > 0 THEN 'units_gain' 
        END as units_flag


        FROM   dcp_mappluto AS pluto LEFT OUTER JOIN export_devdb AS devdb ON pluto.bbl = devdb.bbl 
        LEFT JOIN zoning_typology_map AS typology ON devdb.zoningdist1 = typology.zonedist1

    WHERE 
        job_inactive IS NULL
        AND 
        boro :: NUMERIC IN ({boro})
        AND 
        complete_year :: NUMERIC >= 2010

    GROUP BY
        typology.typ_2020_03_value,
        typology.typ_2020_03_name,
        CASE WHEN classa_net::INTEGER < 0 THEN 'units_loss' 
        WHEN classa_net::INTEGER > 0 THEN 'units_gain' 
        END

    '''.format(boro=boro), con = conn)

    sql = '''

    SELECT 
    pluto.bbl,
    pluto.zonedist1,
    pluto.residfar,
    typology.typ_2020_03_name as typo,
    pluto.wkb_geometry

    FROM   dcp_mappluto AS pluto LEFT JOIN zoning_typology_map AS typology ON pluto.zonedist1 = typology.zonedist1
    '''

    #df_rm = gpd.GeoDataFrame.from_postgis(sql, conn, geom_col='wkb_geometry')


    return df#, df_rm