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

### assign modal mixing
# add columns for bike, ped, and overall modal mixing
with ENGINE.connect() as conn:
    conn.execute(
        text(
            """
            alter table typologies_joined add column if not exists bike_mix text;
            alter table typologies_joined add column if not exists ped_mix text;
            alter table typologies_joined add column if not exists modal_mix text;
            COMMIT;
            """
        )
    )
## update columns based on value ranges
# bike mix
with ENGINE.connect() as conn:
    conn.execute(
        text(
            """
            update table typologies_joined
            set bike_mix = 'high'
            where "type" = 'Bus Bike Lane'
            or "type" = 'Sharrow'
            or "type" IS NULL;

            update table typologies_joined
            set bike_mix = 'mod'
            where or "type" = 'Conventional w Sharrows'
            or "type" = 'Conventional'
            or "type" = 'Paint Buffered'
            or "type" = 'Two Way Unprotected Bicycle Lane';

            update table typologies_joined
            set bike_mix = 'low'
            where "type" = 'One Way Protected Bicycle Lane';
            
            COMMIT;
            """
        )
    )

# ped mix
with ENGINE.connect() as conn:
    conn.execute(
        text(
            """
            update table typologies_joined
            set ped_mix = 'high'
            where sw_ratio < 0.45;

            update table typologies_joined
            set ped_mix = 'mod'
            where sw_ratio >= 0.45
            and sw_ratio <= 0.82;

            update table typologies_joined
            set ped_mix = 'low'
            where sw_ratio > 0.82;
            
            COMMIT;
            """
        )
    )

# circuit overwrite: if roadway is adjacent to circuit trail, bike/ped measures are overwritten to low/low mixing
with ENGINE.connect() as conn:
    conn.execute(
        text(
            """
            update table typologies_joined
            set bike_mix = 'low'
            where circuit = 'Existing';

            update table typologies_joined
            set ped_mix = 'low'
            where circuit = 'Existing';
            
            COMMIT;
            """
        )
    )
# overall modal mix
with ENGINE.connect() as conn:
    conn.execute(
        text(
            """
            update table typologies_joined
            set modal_mix = 'high'
            where bike_mix = 'high'
            and ped_mix = 'high';

            update table typologies_joined
            set modal_mix = 'high'
            where bike_mix = 'high'
            and ped_mix = 'mod';

            update table typologies_joined
            set modal_mix = 'high'
            where bike_mix = 'mod'
            and ped_mix = 'high';

            update table typologies_joined
            set modal_mix = 'mod'
            where bike_mix = 'mod'
            and ped_mix = 'mod';

            update table typologies_joined
            set modal_mix = 'mod'
            where bike_mix = 'high'
            and ped_mix = 'low';

            update table typologies_joined
            set modal_mix = 'mod'
            where bike_mix = 'low'
            and ped_mix = 'high';

            update table typologies_joined
            set modal_mix = 'low'
            where bike_mix = 'low'
            and ped_mix = 'low';

            update table typologies_joined
            set modal_mix = 'low'
            where bike_mix = 'mod'
            and ped_mix = 'low';

            update table typologies_joined
            set modal_mix = 'low'
            where bike_mix = 'low'
            and ped_mix = 'mod';
            
            COMMIT;
            """
        )
    )

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
with ENGINE.connect() as conn:
    conn.execute(
        text(
            """
            alter table typologies_joined add column if not exists activity_level text;
           
            update table typologies_joined
            set activity_level = 'low'
            where "TYPOLOGY" = 'Narrow Neighborhood'
            or "TYPOLOGY" = 'Wide Neighborhood';

            update table typologies_joined
            set activity_level = 'mod'
            where "TYPOLOGY" = 'Narrow Connector'
            or "TYPOLOGY" = 'Wide Connector';

            update table typologies_joined
            set activity_level = 'high'
            where uc_overlap = TRUE;

            COMMIT;
            """
        )
    )


### calculate intersection density
# intersection points created in QGIS using the process outlined here: https://www.qgistutorials.com/en/docs/3/calculating_intersection_density.html
# buffer typology segments

# count how many intersections points are within the buffer

# divide by mileage and then by 4 to get avg intersections per quarter mile


# assign conflict density

# assign default speed limit
