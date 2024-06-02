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

# read mismatches from postgis query and create dataframe with results


# itterate over mismatches with same sequence number
# select +1 and -!
