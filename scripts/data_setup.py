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
    - road intersections (created in QGIS)

"""

import geopandas as gpd
import pandas as pd
from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
from env_vars import GIS_ENGINE, ENGINE
from sqlalchemy import text

typologies_filename = "_PennDOT_Typologies"

# list of tables to rename geometry column to geom from shape
s_list = [
    "circuittrails",
    "pa_centerline",
    "philly_bike_network",
    "ped_network_gaps",
    "hin",
]

# list of tables to rename geometry column from geometry to geom and lowercase object id
g_list = ["typologies", "urbancore"]


# read typologies from shapefile
typologies = gpd.read_file(rf"{ev.DATA_ROOT}\shapefiles\{typologies_filename}.shp")
typologies = typologies.to_crs(26918)
typologies.to_postgis("typologies", con=ENGINE, if_exists="replace")

# read urban core from geojson
urbancore = gpd.read_file(rf"{ev.DATA_ROOT}\urban_core.geojson")
urbancore = urbancore.to_crs(26918)
urbancore.to_postgis("urbancore", con=ENGINE, if_exists="replace")

# read road intersections from geojson
road_intersections = gpd.read_file(rf"{ev.DATA_ROOT}\road_intersections.geojson")
road_intersections = road_intersections.to_crs(26918)
road_intersections.to_postgis("road_intersections", con=ENGINE, if_exists="replace")

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
    """SELECT p.*
    FROM transportation.pa_centerline p,
        (select cb.*
        from boundaries.countyboundaries cb
        where co_name = 'Philadelphia') a
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

# read sidewalk gaps from GIS database
png = gpd.GeoDataFrame.from_postgis(
    """SELECT p.*
    FROM (select p.objectid, p.hwy_tag, p.sw_ratio, st_transform(p.shape, 26918) as shape from transportation.pedestriannetwork_gaps p) p,
        (select cb.*
        from boundaries.countyboundaries cb
        where co_name = 'Philadelphia') a
    where st_intersects(p.shape, a.shape)""",
    con=GIS_ENGINE,
    geom_col="shape",
)
# write to postgis
png.to_postgis("ped_network_gaps", con=ENGINE, if_exists="replace")


# rename columns so they work with conflation tool
def geometry_rename(g_tbl):
    with ENGINE.connect() as conn:
        conn.execute(
            text(
                rf"""
            ALTER TABLE {g_tbl}
            RENAME COLUMN geometry to geom;
            ALTER TABLE {g_tbl}
            RENAME COLUMN "OBJECTID" to objectid;
            COMMIT;
        """
            )
        )


def shape_rename(s_tbl):
    with ENGINE.connect() as conn:
        conn.execute(
            text(
                rf"""
        ALTER TABLE {s_tbl}
        RENAME COLUMN shape to geom;
        COMMIT;
    """
            )
        )


# run renaming functions on each table in previously defined lists
for g_tbl in g_list:
    geometry_rename(g_tbl)

for s_tbl in s_list:
    shape_rename(s_tbl)
