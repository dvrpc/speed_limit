"""
data_setup.py
________________
This script filters and imports the required datasets from provided shapefiles and the DVRPC GIS database.

    - PennDOT/Philadelphia Typologies
    - Philadelphia High Injury Network
    - ped network gaps
    - philadelphia bike network
    - urban core (from typologies work)
    - PA Centerline
    - circuit trails
    - county boundaries


"""

typologies_filename = "_PennDOT_Typologies"

# list of tables to rename geometry column to geom from shape
s_list = [
    "circuittrails",
    "pa_centerline",
    "philly_bike_network",
    "pedestriannetwork_gaps",
]

# list of tables to rename geometry column from geometry to geom and lowercase object id
g_list = ["typologies", "urbancore"]


import geopandas as gpd
import pandas as pd
from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
from env_vars import GIS_ENGINE, ENGINE


# read typologies from shapefile
typologies = gpd.read_file(rf"{ev.DATA_ROOT}\shapefiles\{typologies_filename}.shp")
typologies = typologies.to_crs(26918)
typologies.to_postgis("typologies", con=ENGINE, if_exists="replace")

# read urban core from geojson
urbancore = gpd.read_file(rf"{ev.DATA_ROOT}\urban_core.geojson")
urbancore = typologies.to_crs(26918)
urbancore.to_postgis("urbancore", con=ENGINE, if_exists="replace")


# read HIN from GIS database
hin = gpd.GeoDataFrame.from_postgis(
    """SELECT * FROM transportation.philly_highinjurynetwork p""",
    con=GIS_ENGINE,
    geom_col="shape",
)
# write to postgis
hin.to_postgis("hin", con=ENGINE, if_exists="replace")


# read pa_centerline from GIS database
# will need to be clipped to county boundary
pac = gpd.GeoDataFrame.from_postgis(
    """SELECT * 
    FROM transportation.pa_centerline p, 
        (select cb.*
        from boundaries.countyboundaries cb
        where co_name = 'Philadelphia) a
    where st_intersects(p.shape, a.shape)""",
    con=GIS_ENGINE,
    geom_col="shape",
)
# write to postgis
pac.to_postgis("pa_centerline", con=ENGINE, if_exists="replace")

# read circuit trails from GIS database
ct = gpd.GeoDataFrame.from_postgis(
    """SELECT * FROM transportation.circuittrails c""",
    con=GIS_ENGINE,
    geom_col="shape",
)
# write to postgis
ct.to_postgis("circuittrails", con=ENGINE, if_exists="replace")

# read philly bike network from GIS database
pbn = gpd.GeoDataFrame.from_postgis(
    """SELECT * FROM transportation.philly_bike_network p""",
    con=GIS_ENGINE,
    geom_col="shape",
)
# write to postgis
pbn.to_postgis("philly_bike_network", con=ENGINE, if_exists="replace")

# read sidewalk gaps from GIS database and clip to philadelphia
png = gpd.GeoDataFrame.from_postgis(
    """SELECT * 
    FROM transportation.pedestriannetwork_gaps p,
        (select cb.*
        from boundaries.countyboundaries cb
        where co_name = 'Philadelphia) a
    where st_intersects(p.shape, a.shape)""",
    con=GIS_ENGINE,
    geom_col="shape",
)
# write to postgis
png.to_postgis("ped_network_gaps", con=ENGINE, if_exists="replace")


# rename columns so they work with conflation tool
Q_rename_g = rf"""
    ALTER TABLE {g_tbl}
    RENAME COLUMN geometry to geom;
    ALTER TABLE {g_tbl}
    RENAME COLUMN "OBJECTID" to objectid;
    COMMIT;
"""

Q_rename_s = rf"""
    ALTER TABLE {s_tbl}
    RENAME COLUMN shape to geom;
    COMMIT;
"""
from sqlalchemy import text

for g_tbl in g_list:
    with ENGINE.connect() as conn:
        result = conn.execute(text(Q_rename_g), g_tbl)
for s_tbl in s_list:
    with ENGINE.connect() as conn:
        result = conn.execute(text(Q_rename_s), s_tbl)

'''
#IGNORE: saving for future reference if needed

# read inrix from GIS database
inrix = gpd.GeoDataFrame.from_postgis(
    """select objectid, segid, roadname, county, startlat, startlong, endlat, endlong, refspdmean, refspdmin, refspdmax, 
    spdwkd, spdwkd0610, spdwkd1519, spdwkd0006, spdwkd0607, spdwkd0708, spdwkd0809, spdwkd0910, spdwkd1011, spdwkd1112, spdwkd1213, 
    spdwkd1314, spdwkd1415, spdwkd1516, spdwkd1617, spdwkd1718, spdwkd1819, spdwkd1920, spdwkd2021, spdwkd2122, spdwkd2223, spdwkd2300, shape as geom
from transportation.cmp2021_inrix_traveltimedata cit
where cit.county = 'PHILADELPHIA' """,
    con=GIS_ENGINE,
    geom_col="geom",
)
# write to postgis
inrix.to_postgis("inrix_2021", con=ENGINE, if_exists="replace")
'''
