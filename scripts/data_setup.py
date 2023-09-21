"""
data_setup.py
________________
This script filtered and imports the required datasets from provided shapefiles and the DVRPC GIS database.

    - 2022 INRIX data clipped to the City of Philadelphia
    - PennDOT/Philadelphia Typologies
    - Philadelphia High Injury Network

Working on:
    - Crash data
    - Posted speed limit data for non-arterials (collectors and local roads)
"""

# inrix_filename = "DVRPCPANJ_INRIXXDgeo22_1_jointraveltime2022"
# inrix_year = "2022"
typologies_filename = "_PennDOT_Typologies"


import geopandas as gpd
import pandas as pd
from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
from env_vars import GIS_ENGINE, ENGINE


typologies = gpd.read_file(rf"{ev.DATA_ROOT}\shapefiles\{typologies_filename}.shp")
typologies = typologies.to_crs(26918)
typologies.to_postgis("typologies", con=ENGINE, if_exists="replace")

# rename the geometry column to geom so it works with conflation tool
Q_rename = """
    ALTER TABLE typologies
    RENAME COLUMN geometry to geom;
    ALTER TABLE typologies
    RENAME COLUMN "OBJECTID" to objectid;
    COMMIT;
"""
from sqlalchemy import text

with ENGINE.connect() as conn:
    result = conn.execute(text(Q_rename))

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


# read HIN from GIS database
hin = gpd.GeoDataFrame.from_postgis(
    """SELECT * FROM transportation.philly_highinjurynetwork p""",
    con=GIS_ENGINE,
    geom_col="shape",
)
# write to postgis
hin.to_postgis("hin", con=ENGINE, if_exists="replace")
