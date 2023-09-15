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

inrix_filename = "DVRPCPANJ_INRIXXDgeo22_1_jointraveltime2022"
inrix_year = "2022"
typologies_filename = "_PennDOT_Typologies"


import geopandas as gpd
import pandas as pd
from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
from env_vars import GIS_ENGINE, ENGINE

# read provided shapefiles and write to postgres
inrix = gpd.read_file(rf"{ev.DATA_ROOT}\shapefiles\{inrix_filename}.shp")
inrix.to_postgis(rf"inrix{inrix_year}", con=ENGINE, if_exists="replace")

typologies = gpd.read_file(rf"{ev.DATA_ROOT}\shapefiles\{typologies_filename}.shp")
# rename geometry column
# typologies = typologies.rename_geometry("geom", inplace=True)

typologies.to_postgis("typologies", con=ENGINE, if_exists="replace")

# rename the geometry column to geom so it works with conflation tool
Q_rename = """
    ALTER TABLE typologies
    RENAME COLUMN geometry to geom;
"""
from sqlalchemy import text

with ENGINE.connect() as conn:
    result = conn.execute(text(Q_rename))

# filter inrix to just philadelphia
Q_PhilaInrix = rf"""
    select *, st_transform(geometry, 4326) as geom
    from (
        select *
        from inrix{inrix_year} i
        where i."County" = 'PHILADELPHIA'
    ) foo
"""
phila_inrix = gpd.GeoDataFrame.from_postgis(
    Q_PhilaInrix,
    con=ENGINE,
    geom_col="geom",
)


# write to postgis
phila_inrix.to_postgis(rf"phila_inrix_{inrix_year}", con=ENGINE, if_exists="replace")

# read HIN from GIS database
hin = gpd.GeoDataFrame.from_postgis(
    """SELECT * FROM transportation.philly_highinjurynetwork p""",
    con=GIS_ENGINE,
    geom_col="shape",
)
# write to postgis
hin.to_postgis("hin", con=ENGINE, if_exists="replace")
