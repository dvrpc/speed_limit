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


# # assign intersection density level
# id1 = update(T).values(int_den="low").where(T.c.pts_qt_mi < 1)
# id2 = update(T).values(int_den="mod").where(T.c.pts_qt_mi >= 1).where(T.c.pts_qt_mi < 3)
# id3 = update(T).values(int_den="high").where(T.c.pts_qt_mi >= 3)
# statements = [id1, id2, id3]
# for s in statements:
#     conn.execute(s)
#     conn.commit()

# # assign conflict density
# cd1 = (
#     update(T)
#     .values(conf_dens="high")
#     .where(T.c.modal_mix == "high")
#     .where(T.c.int_den == "high")
# )
# cd2 = (
#     update(T)
#     .values(conf_dens="high")
#     .where(T.c.modal_mix == "mod")
#     .where(T.c.int_den == "high")
# )
# cd3 = (
#     update(T)
#     .values(conf_dens="high")
#     .where(T.c.modal_mix == "high")
#     .where(T.c.int_den == "mod")
# )
# cd4 = (
#     update(T)
#     .values(conf_dens="mod")
#     .where(T.c.modal_mix == "mod")
#     .where(T.c.int_den == "mod")
# )
# cd5 = (
#     update(T)
#     .values(conf_dens="mod")
#     .where(T.c.modal_mix == "high")
#     .where(T.c.int_den == "low")
# )
# cd6 = (
#     update(T)
#     .values(conf_dens="mod")
#     .where(T.c.modal_mix == "low")
#     .where(T.c.int_den == "high")
# )
# cd7 = (
#     update(T)
#     .values(conf_dens="low")
#     .where(T.c.modal_mix == "low")
#     .where(T.c.int_den == "low")
# )
# cd8 = (
#     update(T)
#     .values(conf_dens="low")
#     .where(T.c.modal_mix == "mod")
#     .where(T.c.int_den == "low")
# )
# cd9 = (
#     update(T)
#     .values(conf_dens="low")
#     .where(T.c.modal_mix == "low")
#     .where(T.c.int_den == "mod")
# )
# statements = [cd1, cd2, cd3, cd4, cd5, cd6, cd7, cd8, cd9]
# for s in statements:
#     conn.execute(s)
#     conn.commit()


# assign default speed limit
ds1 = (
    update(T)
    .values(default_speed=20)
    .where(T.c.conf_dens == "high")
    .where(T.c.activ_level == "high")
)
ds2 = (
    update(T)
    .values(default_speed=25)
    .where(T.c.conf_dens == "mod")
    .where(T.c.activ_level == "high")
)
ds3 = (
    update(T)
    .values(default_speed=25)
    .where(T.c.conf_dens == "high")
    .where(T.c.activ_level == "mod")
)
ds4 = (
    update(T)
    .values(default_speed=25)
    .where(T.c.conf_dens == "mod")
    .where(T.c.activ_level == "mod")
)
ds5 = (
    update(T)
    .values(default_speed=25)
    .where(T.c.conf_dens == "high")
    .where(T.c.activ_level == "low")
)
ds6 = (
    update(T)
    .values(default_speed=25)
    .where(T.c.conf_dens == "low")
    .where(T.c.activ_level == "high")
)
ds7 = (
    update(T)
    .values(default_speed=35)
    .where(T.c.conf_dens == "low")
    .where(T.c.activ_level == "low")
)
ds8 = (
    update(T)
    .values(default_speed=25)
    .where(T.c.conf_dens == "mod")
    .where(T.c.activ_level == "low")
)
ds9 = (
    update(T)
    .values(default_speed=30)
    .where(T.c.conf_dens == "low")
    .where(T.c.activ_level == "mod")
)
statements = [ds1, ds2, ds3, ds4, ds5, ds6, ds7, ds8, ds9]
for s in statements:
    conn.execute(s)
    conn.commit()


##### overwrites #####
# if there is more than 1 lane in each direction, 25 should be the minimum
l1 = (
    update(T)
    .values(default_speed=25)
    .where(T.c.DIR_IND == "B")
    .where(T.c.LANE_CNT > 2)
    .where(T.c.default_speed < 25)
)
l2 = (
    update(T)
    .values(default_speed=25)
    .where(T.c.DIR_IND != "B")
    .where(T.c.LANE_CNT > 1)
    .where(T.c.default_speed < 25)
)
statements = [l1, l2]
for s in statements:
    conn.execute(s)
    conn.commit()


# exceptionally curvey roads should be 25
c1 = update(T).values(default_speed=25).where(STREET_NAM="KELLY DR")
c2 = update(T).values(default_speed=25).where(STREET_NAM="LINCOLN DR")
c3 = update(T).values(default_speed=25).where(STREET_NAM="MARTIN LUTHER KING JR DR")
statements = [c1, c2, c3]
for s in statements:
    conn.execute(s)
    conn.commit()


# if current posted speed is greater than default speed, defer to posted speed
# ps1 = update(T).values(default_speed=SPD_LIMIT).where(default_speed > SPD_LIMIT)
