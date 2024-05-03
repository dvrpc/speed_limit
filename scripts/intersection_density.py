"""
This script calcualtes average intersection density per 
quarter mile along existing typologies segments using 
the PA_Centerline dataset.

"""

import geopandas as gpd
import pandas as pd
import env_vars as ev
from env_vars import GIS_ENGINE, ENGINE
from sqlalchemy import text


# read pa centerline from database
pc = gpd.GeoDataFrame.from_postgis(
    """SELECT * FROM pa_centerline p""",
    con=ENGINE,
    geom_col="geom",
)

# dissolve to avoid getting points at verticies that are not intersections
pc = pc.dissolve()

# explode dissolved multilines to single part linestrings
sp = pc.explode()

# write to db
sp.to_postgis("roads_exploded", con=ENGINE, if_exists="replace")

# # explode dissolved multiline to single part linestrings
# with ENGINE.connect() as conn:
#     conn.execute(
#         text(
#             """CREATE TABLE roads_singlepart AS
#         SELECT (ST_DUMP(rd.geom)).geom::geometry(LineString, 26918) AS geom
#         FROM roads_dissolved rd;
#         COMMIT;
#             """
#         )
#     )

# read single part linestrings from db
rs = gpd.GeoDataFrame.from_postgis(
    """SELECT * FROM roads_exploded rs""",
    con=ENGINE,
    geom_col="geom",
)

# find intersections, create points, and eliminate duplicates
gdf = gpd.overlay(rs, rs, how="intersection", keep_geom_type=False)
gdf = gdf[gdf.geom_type == "Point"]
gdf.drop_duplicates("geometry", inplace=True)

# write to postgis
gdf.to_postgis("road_intersections", con=ENGINE, if_exists="replace")
