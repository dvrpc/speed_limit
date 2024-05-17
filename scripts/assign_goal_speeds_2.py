# ### calculate intersection density --- run each query individually in dbever until this is fixed
# # intersection points created in QGIS using the process outlined here: https://www.qgistutorials.com/en/docs/3/calculating_intersection_density.html

import geopandas as gpd
import pandas as pd
from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
from env_vars import ENGINE
from sqlalchemy import text
from sqlalchemy import update, MetaData
from geoalchemy2 import Geometry

## get table in sqlalchemy
conn = ENGINE.connect()
meta = MetaData()
meta.reflect(bind=ENGINE)
T = meta.tables["typologies_joined"]


# # buffer typology segments
# ### these queries create individual tables due to memory load and to save substantial processing time
# conn.execute(
#     """
#     create table if not exists typologies_buffer5 as
#     select tj.objectid, st_buffer(tj.geom, 5) as buff_5
#     from typologies_joined tj;"""
# )
# # join intesrsection points to buffer
# conn.execute(
#     """
#     create table if not exists buff_pts_join as
#     SELECT tb.objectid, ri.geom AS pts
#     FROM typologies_buffer5 tb
#     LEFT JOIN road_intersections ri ON st_contains(tb.buff_5,ri.geom);"""
# )
# # count number of points joined to each buffer
# conn.execute(
#     """
#     create table if not exists pts_in_buff as
#     select b.objectid, count (*) as pts_in_buff
#     from buff_pts_join b
#     group by objectid;"""
# )
# # join count of pts to typologies
# # divide to convert ft to miles, divide pts by mileage and then by 4 to get avg intersections per quarter mile
# conn.execute(
#     """
#     update typologies_joined tj
#     set pts_qt_mi = ((p.pts_in_buff/(tj."Geo_Ft"/5280))/4)
#     from pts_in_buff p
#     where tj.objectid = p.objectid;"""
# )
