import geopandas as gpd
import pandas as pd
from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
from env_vars import ENGINE
from sqlalchemy import text

# ### join conflated attributes
# with ENGINE.connect() as conn:
#     conn.execute(
#         text(
#             """
#         DROP TABLE IF EXISTS typologies_joined;
#         COMMIT;
#         CREATE TABLE typologies_joined AS
#         select t.*, ta."type", tb."sw_ratio", tc."circuit"
#         from public.typologies t
#         left join rejoined.typologies_a ta
#         on t.objectid = ta.objectid
#         left join rejoined.typologies_b tb
#         on t.objectid  = tb.objectid
#         left join rejoined.typologies_c tc
#         on t.objectid  = tc.objectid;
#         COMMIT;
#         """
#         )
#     )

# ### assign modal mixing
# # add columns for bike, ped, and overall modal mixing
# with ENGINE.connect() as conn:
#     conn.execute(
#         text(
#             """
#             alter table typologies_joined add column if not exists bike_mix text;
#             alter table typologies_joined add column if not exists ped_mix text;
#             alter table typologies_joined add column if not exists modal_mix text;
#             COMMIT;
#             """
#         )
#     )


from sqlalchemy import update, MetaData
from geoalchemy2 import Geometry

## get table in sqlalchemy
conn = ENGINE.connect()
meta = MetaData()
meta.reflect(bind=ENGINE)
T = meta.tables["typologies_joined"]
## update queries
# bike mix
b1 = update(T).values(bike_mix="high").where(T.c.type == "Bus Bike Lane")
b2 = update(T).values(bike_mix="high").where(T.c.type == "Sharrow")
b3 = update(T).values(bike_mix="high").where(T.c.type == None)

b4 = update(T).values(bike_mix="mod").where(T.c.type == "Conventional w Sharrows")
b5 = update(T).values(bike_mix="mod").where(T.c.type == "Conventional")
b6 = update(T).values(bike_mix="mod").where(T.c.type == "Paint Buffered")
b7 = (
    update(T)
    .values(bike_mix="mod")
    .where(T.c.type == "Two Way Unprotected Bicycle Lane")
)

b8 = (
    update(T).values(bike_mix="low").where(T.c.type == "One Way Protected Bicycle Lane")
)

statements = [b1, b2, b3, b4, b5, b6, b7, b8]
for s in statements:
    conn.execute(s)
    conn.commit()

# ped mix
s1 = update(T).values(ped_mix="high").where(T.c.sw_ratio < 0.45)
s2 = (
    update(T)
    .values(ped_mix="mod")
    .where(T.c.sw_ratio >= 0.45)
    .where(T.c.sw_ratio <= 0.82)
)
s3 = update(T).values(ped_mix="low").where(T.c.sw_ratio > 0.82)

statements = [s1, s2, s3]
for s in statements:
    conn.execute(s)
    conn.commit()


# circuit overwrite: if roadway is adjacent to circuit trail, bike/ped measures are overwritten to low/low mixing
c1 = update(T).values(bike_mix="low").where(T.c.circuit == "Existing")
c2 = update(T).values(ped_mix="low").where(T.c.circuit == "Existing")
statements = [c1, c2]
for s in statements:
    conn.execute(s)
    conn.commit()

# overall modal mix
m1 = (
    update(T)
    .values(modal_mix="high")
    .where(T.c.bike_mix == "high")
    .where(T.c.ped_mix == "high")
)
m2 = (
    update(T)
    .values(modal_mix="high")
    .where(T.c.bike_mix == "mod")
    .where(T.c.ped_mix == "high")
)
m3 = (
    update(T)
    .values(modal_mix="high")
    .where(T.c.bike_mix == "high")
    .where(T.c.ped_mix == "mod")
)
m4 = (
    update(T)
    .values(modal_mix="mod")
    .where(T.c.bike_mix == "mod")
    .where(T.c.ped_mix == "mod")
)
m5 = (
    update(T)
    .values(modal_mix="mod")
    .where(T.c.bike_mix == "high")
    .where(T.c.ped_mix == "low")
)
m6 = (
    update(T)
    .values(modal_mix="mod")
    .where(T.c.bike_mix == "low")
    .where(T.c.ped_mix == "high")
)
m7 = (
    update(T)
    .values(modal_mix="low")
    .where(T.c.bike_mix == "low")
    .where(T.c.ped_mix == "low")
)
m8 = (
    update(T)
    .values(modal_mix="low")
    .where(T.c.bike_mix == "mod")
    .where(T.c.ped_mix == "low")
)
m9 = (
    update(T)
    .values(modal_mix="low")
    .where(T.c.bike_mix == "low")
    .where(T.c.ped_mix == "mod")
)
statements = [m1, m2, m3, m4, m5, m6, m7, m8, m9]
for s in statements:
    conn.execute(s)
    conn.commit()

### overlay urban core
# read from db
tbl = gpd.GeoDataFrame.from_postgis(
    """select tj.*, st_intersects(tj.geom, u.geom ) as uc_overlap
        from typologies_joined tj, urbancore u""",
    con=ENGINE,
    geom_col="geom",
)
# put results back in db
tbl.to_postgis("typologies_joined", con=ENGINE, if_exists="replace")

### assign activity levels
a1 = update(T).values(activity_level="low").where(T.c.TYPOLOGY == "Narrow Neighborhood")
a2 = update(T).values(activity_level="low").where(T.c.TYPOLOGY == "Wide Neighborhood")
a3 = update(T).values(activity_level="mod").where(T.c.TYPOLOGY == "Narrow Connector")
a4 = update(T).values(activity_level="mod").where(T.c.TYPOLOGY == "Wide Connector")
a5 = update(T).values(activity_level="high").where(T.c.uc_overlap == True)
statements = [a1, a2, a3, a4, a5]
for s in statements:
    conn.execute(s)
    conn.commit()

### calculate intersection density
# intersection points created in QGIS using the process outlined here: https://www.qgistutorials.com/en/docs/3/calculating_intersection_density.html
# buffer typology segments

# count how many intersections points are within the buffer

# divide by mileage and then by 4 to get avg intersections per quarter mile


# assign conflict density

# assign default speed limit
