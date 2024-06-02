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

"""
# assign intersection density level
id1 = update(T).values(int_den="low").where(T.c.pts_qt_mi < 1)
id2 = update(T).values(int_den="mod").where(T.c.pts_qt_mi >= 1).where(T.c.pts_qt_mi < 3)
id3 = update(T).values(int_den="high").where(T.c.pts_qt_mi >= 3)
statements = [id1, id2, id3]
for s in statements:
    conn.execute(s)
    conn.commit()

# assign conflict density
cd1 = (
    update(T)
    .values(conf_dens="high")
    .where(T.c.modal_mix == "high")
    .where(T.c.int_den == "high")
)
cd2 = (
    update(T)
    .values(conf_dens="high")
    .where(T.c.modal_mix == "mod")
    .where(T.c.int_den == "high")
)
cd3 = (
    update(T)
    .values(conf_dens="high")
    .where(T.c.modal_mix == "high")
    .where(T.c.int_den == "mod")
)
cd4 = (
    update(T)
    .values(conf_dens="mod")
    .where(T.c.modal_mix == "mod")
    .where(T.c.int_den == "mod")
)
cd5 = (
    update(T)
    .values(conf_dens="mod")
    .where(T.c.modal_mix == "high")
    .where(T.c.int_den == "low")
)
cd6 = (
    update(T)
    .values(conf_dens="mod")
    .where(T.c.modal_mix == "low")
    .where(T.c.int_den == "high")
)
cd7 = (
    update(T)
    .values(conf_dens="low")
    .where(T.c.modal_mix == "low")
    .where(T.c.int_den == "low")
)
cd8 = (
    update(T)
    .values(conf_dens="low")
    .where(T.c.modal_mix == "mod")
    .where(T.c.int_den == "low")
)
cd9 = (
    update(T)
    .values(conf_dens="low")
    .where(T.c.modal_mix == "low")
    .where(T.c.int_den == "mod")
)
statements = [cd1, cd2, cd3, cd4, cd5, cd6, cd7, cd8, cd9]
for s in statements:
    conn.execute(s)
    conn.commit()


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
"""

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

# if a road is in the urban core and is characteriszed as narrow in typologies, default speed should be 20
ucn1 = (
    update(T)
    .values(default_speed=20)
    .where(T.c.uc_overlap != None)
    .where(T.c.TYPOLOGY == "Narrow Neighborhood")
)
ucn2 = (
    update(T)
    .values(default_speed=20)
    .where(T.c.uc_overlap != None)
    .where(T.c.TYPOLOGY == "Narrow Connector")
)
statements = [ucn1, ucn2]
for s in statements:
    conn.execute(s)
    conn.commit()


# exceptionally curvey roads should be 25
c1 = update(T).values(default_speed=25).where(T.c.STREET_NAM == "KELLY DR")
c2 = update(T).values(default_speed=25).where(T.c.STREET_NAM == "LINCOLN DR")
c3 = (
    update(T)
    .values(default_speed=25)
    .where(T.c.STREET_NAM == "MARTIN LUTHER KING JR DR")
)
c4 = update(T).values(default_speed=25).where(T.c.STREET_NAM == "COBBS CREEK PY")
statements = [c1, c2, c3, c4]
for s in statements:
    conn.execute(s)
    conn.commit()


# highway-like roads should be 30
hw1 = update(T).values(default_speed=30).where(T.c.STREET_NAM == "PENROSE AV")
hw2 = update(T).values(default_speed=30).where(T.c.STREET_NAM == "TWENTYSIXTH ST")
hw3 = update(T).values(default_speed=30).where(T.c.STREET_NAM == "ROOSEVELT BL")
# Broad St south of I-76; selected by objectid
hw4 = update(T).values(default_speed=30).where(T.c.objectid == 103769)
hw5 = update(T).values(default_speed=30).where(T.c.objectid == 103770)
hw6 = update(T).values(default_speed=30).where(T.c.objectid == 103771)
hw7 = update(T).values(default_speed=30).where(T.c.objectid == 103772)
hw8 = update(T).values(default_speed=30).where(T.c.objectid == 117415)
hw9 = update(T).values(default_speed=30).where(T.c.objectid == 117416)
statements = [hw1, hw2, hw3, hw4, hw5, hw6, hw7, hw8, hw9]
for s in statements:
    conn.execute(s)
    conn.commit()

# if current posted speed is greater than default speed, defer to posted speed (still only 9 of these)
ps1 = (
    update(T)
    .values(default_speed=T.c.SPD_LIMIT)
    .where(T.c.default_speed > T.c.SPD_LIMIT)
)

conn.execute(ps1)
conn.commit()

# for consistency, overwrite sinle section of 35 mph (to 25 because that is what surrounds it)
z1 = update(T).values(default_speed=25).where(T.c.default_speed == 35)

conn.execute(z1)
conn.commit()

# fill in any nulls (missing due to conflation issues) with 25
n1 = update(T).values(default_speed=25).where(T.c.default_speed == None)

conn.execute(n1)
conn.commit()
