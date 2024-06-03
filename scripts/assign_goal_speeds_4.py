import pandas as pd
import geopandas as gpd
import os
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import update, MetaData
import env_vars as ev
from env_vars import ENGINE, DATA_ROOT
import numpy as np
from psycopg2.extensions import register_adapter, AsIs

register_adapter(np.int64, AsIs)

distinct_mismatches = pd.read_sql(
    """select distinct ("ST_RT_NO", "SEQ_NO")
        from (
            select "ST_RT_NO","SEQ_NO" , default_speed, count(*) as cnt
            from typologies_joined tj 
            where "DIV_RDWY" = 1
            group by "ST_RT_NO", "SEQ_NO", default_speed
            having count(*) = 1
            ) foo""",
    con=ENGINE,
)

# convert DF to list and get rid of SRs that start with "G"
list = []
for i in range(0, len(distinct_mismatches)):
    sr = distinct_mismatches["row"][i][1:5]
    seq = distinct_mismatches["row"][i][6:-1]
    if sr.startswith("G"):
        pass
    else:
        list.append((sr, seq))


# create function that finds the appropriate speed to use based on the most common default speed on the adjacent road segments
def find_speed(sr, seq):
    df = pd.read_sql(
        f"""select default_speed, count(*) cnt
        from (
            select objectid, "ST_RT_NO" , "SEQ_NO" , default_speed 
            from typologies_joined tj 
            where ("SEQ_NO" = '{seq}'
            or "SEQ_NO" = CAST('{seq}' as INTEGER)+ 100
            or "SEQ_NO" = CAST('{seq}' as INTEGER)- 100)
            and "ST_RT_NO" = '{sr}') foo
        group by default_speed
        order by cnt desc""",
        con=ENGINE,
    )
    if len(df) > 1:
        if df["cnt"].iloc[0] > df["cnt"].iloc[1]:
            speeds.append((sr, seq, df["default_speed"].iloc[0]))
        else:
            # speed = 'Check'
            check.append((sr, seq))
        # print(sr, seq, speed)
    else:
        # print('skipped')
        pass


# iterate through the list to find the associated default speeds to use
check = []
speeds = []
for i in range(0, len(list)):
    find_speed(list[i][0], list[i][1])
print("Mismatches to check manually:", len(check))

# export list of sr/seq_no pairs to check manually
check_df = pd.DataFrame(check)
check_df.columns = ["SR", "SEQ_NO"]
check_df.to_csv(f"{DATA_ROOT}/manual_checks.csv")

# set up speed df to be joined
speed_df = pd.DataFrame(speeds)
speed_df.columns = ["ST_RT_NO", "SEQ_NO", "SpeedToUse"]
speed_df["SEQ_NO"] = speed_df["SEQ_NO"].astype(str).astype(int)
# speed_df.head()

# read from table with objectid to be able to update appropriate fields
oid = pd.read_sql(
    """select t.objectid, foo.*
    from(
        select "ST_RT_NO","SEQ_NO" , default_speed, count(*) as cnt
        from typologies_joined tj 
        where "DIV_RDWY" = 1
        group by "ST_RT_NO", "SEQ_NO", default_speed
        having count(*) = 1
        ) foo
    inner join typologies_joined t
    on t."ST_RT_NO" = foo."ST_RT_NO"
    and t."SEQ_NO" = foo."SEQ_NO"
    and t.default_speed = foo.default_speed""",
    con=ENGINE,
)

join = pd.merge(speed_df, oid, how="left", on=["ST_RT_NO", "SEQ_NO"])

# read table from postgres into sqlalchemy to update
conn = ENGINE.connect()
meta = MetaData()
meta.reflect(bind=ENGINE)
T = meta.tables["typologies_joined"]

# run update query to assign new speed to mismatched pair using objectid?
for i in range(0, len(join["objectid"])):
    oid = join["objectid"][i]
    spd = join["SpeedToUse"][i]
    q = update(T).values(default_speed=spd).where(T.c.objectid == oid)
    conn.execute(q)
    conn.commit()

# Need to do some manual updateson "Check" list that was exported to CSV
