import geopandas as gpd
import pandas as pd
from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
from env_vars import ENGINE
from sqlalchemy import text

# join conflated attributes

# joined = gpd.GeoDataFrame.from_postgis(
#     """
#         select t.*, ta."type", tb."sw_ratio"
#         from public.typologies t
#         left join rejoined.typologies_a ta
#         on t.objectid = ta.objectid
#         left join rejoined.typologies_b tb
#         on t.objectid  = tb.objectid;
#         """,
#     con=ENGINE,
#     geom_col="shape",
# )

with ENGINE.connect() as conn:
    conn.execute(
        text(
            """
        DROP TABLE IF EXISTS typologies_joined;
        COMMIT;
        CREATE TABLE typologies_joined AS
        select t.*, ta."type", tb."sw_ratio", tc."circuit"
        from public.typologies t 
        left join rejoined.typologies_a ta
        on t.objectid = ta.objectid 
        left join rejoined.typologies_b tb
        on t.objectid  = tb.objectid
        left join rejoined.typologies_c tc
        on t.objectid  = tc.objectid;
        COMMIT;
        """
        )
    )


# assign modal mixing


# overlay urban core


# assign activity levels


# calculate intersection density
# buffer


# assign conflict density

# assign default speed limit
