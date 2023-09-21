# import geopandas as gpd
import pandas as pd

# from sqlalchemy_utils import database_exists, create_database
import env_vars as ev
from env_vars import ENGINE
import matplotlib.pyplot as plot


def tod_avg_speed():
    df = pd.read_sql_query(
        rf"""select "SPD_LIMIT",
                avg(dif0610) as adif0610,
                avg(dif1519) as adif1519,
                avg(dif0006) as adif0006,
                avg(dif0607) as adif0607,
                avg(dif0708) as adif0708,
                avg(dif0809) as adif0809,
                avg(dif0910) as adif0910,
                avg(dif1011) as adif1011,
                avg(dif1112) as adif1112,
                avg(dif1213) as adif1213,
                avg(dif1314) as adif1314,
                avg(dif1415) as adif1415,
                avg(dif1516) as adif1516,
                avg(dif1617) as adif1617,
                avg(dif1718) as adif1718,
                avg(dif1819) as adif1819,
                avg(dif1920) as adif1920,
                avg(dif2021) as adif2021,
                avg(dif2122) as adif2122,
                avg(dif2223) as adif2223,
                avg(dif2300) as adif2300
            from(
                select i."SPD_LIMIT",
                    (i.spdwkd0610 - i."SPD_LIMIT") as dif0610,
                    (i.spdwkd1519 - i."SPD_LIMIT") as dif1519, 
                    (i.spdwkd0006 - i."SPD_LIMIT") as dif0006, 
                    (i.spdwkd0607 - i."SPD_LIMIT") as dif0607, 
                    (i.spdwkd0708 - i."SPD_LIMIT") as dif0708, 
                    (i.spdwkd0809 - i."SPD_LIMIT") as dif0809, 
                    (i.spdwkd0910 - i."SPD_LIMIT") as dif0910, 
                    (i.spdwkd1011 - i."SPD_LIMIT") as dif1011, 
                    (i.spdwkd1112 - i."SPD_LIMIT") as dif1112, 
                    (i.spdwkd1213 - i."SPD_LIMIT") as dif1213, 
                    (i.spdwkd1314 - i."SPD_LIMIT") as dif1314, 
                    (i.spdwkd1415 - i."SPD_LIMIT") as dif1415, 
                    (i.spdwkd1516 - i."SPD_LIMIT") as dif1516, 
                    (i.spdwkd1617 - i."SPD_LIMIT") as dif1617, 
                    (i.spdwkd1718 - i."SPD_LIMIT") as dif1718, 
                    (i.spdwkd1819 - i."SPD_LIMIT") as dif1819, 
                    (i.spdwkd1920 - i."SPD_LIMIT") as dif1920, 
                    (i.spdwkd2021 - i."SPD_LIMIT") as dif2021, 
                    (i.spdwkd2122 - i."SPD_LIMIT") as dif2122, 
                    (i.spdwkd2223 - i."SPD_LIMIT") as dif2223, 
                    (i.spdwkd2300 - i."SPD_LIMIT") as dif2300 
                from rejoined.inrix i
                ) as foo
            group by "SPD_LIMIT"
            order by "SPD_LIMIT" asc
            """,
        con=ENGINE,
    )

    return df


def top5perc_speed(spd):
    df = pd.read_sql_query(
        rf"""select i."SPD_LIMIT",
                    (i.spdwkd0610 - i."SPD_LIMIT") as dif0610,
                    (i.spdwkd1519 - i."SPD_LIMIT") as dif1519, 
                    (i.spdwkd0006 - i."SPD_LIMIT") as dif0006, 
                    (i.spdwkd0607 - i."SPD_LIMIT") as dif0607, 
                    (i.spdwkd0708 - i."SPD_LIMIT") as dif0708, 
                    (i.spdwkd0809 - i."SPD_LIMIT") as dif0809, 
                    (i.spdwkd0910 - i."SPD_LIMIT") as dif0910, 
                    (i.spdwkd1011 - i."SPD_LIMIT") as dif1011, 
                    (i.spdwkd1112 - i."SPD_LIMIT") as dif1112, 
                    (i.spdwkd1213 - i."SPD_LIMIT") as dif1213, 
                    (i.spdwkd1314 - i."SPD_LIMIT") as dif1314, 
                    (i.spdwkd1415 - i."SPD_LIMIT") as dif1415, 
                    (i.spdwkd1516 - i."SPD_LIMIT") as dif1516, 
                    (i.spdwkd1617 - i."SPD_LIMIT") as dif1617, 
                    (i.spdwkd1718 - i."SPD_LIMIT") as dif1718, 
                    (i.spdwkd1819 - i."SPD_LIMIT") as dif1819, 
                    (i.spdwkd1920 - i."SPD_LIMIT") as dif1920, 
                    (i.spdwkd2021 - i."SPD_LIMIT") as dif2021, 
                    (i.spdwkd2122 - i."SPD_LIMIT") as dif2122, 
                    (i.spdwkd2223 - i."SPD_LIMIT") as dif2223, 
                    (i.spdwkd2300 - i."SPD_LIMIT") as dif2300 
                from rejoined.inrix i
                where i."SPD_LIMIT" = {spd}
            """,
        con=ENGINE,
    )

    return df


def create_bar_chart(df, spd, title):
    spds = [25, 30, 35, 40, 45, 50]
    x = spds.index(spd)

    data = []
    for i in range(4, 22):
        data.append(df.iloc[x][i])
    times = [
        "6AM-7AM",
        "7AM-8AM",
        "8AM-9AM",
        "9AM-10AM",
        "10AM-11AM",
        "11AM-12PM",
        "12PM-1PM",
        "1PM-2PM",
        "2PM-3PM",
        "3PM-4PM",
        "4PM-5PM",
        "5PM-6PM",
        "6PM-7PM",
        "7PM-8PM",
        "8PM-9PM",
        "9PM-10PM",
        "10PM-11PM",
        "11PM-12AM",
    ]

    plot.figure(figsize=(10, 6))
    plot.bar(times, data)
    plot.title(f"{title}: {spd}mph Roads")
    plot.xlabel("Time of Day")
    plot.ylabel("Difference from Posted Speed")
    plot.xticks(rotation=65)
    # plot.show()
    plot.savefig(f"{ev.DATA_ROOT}/{title}+{spd}+.png")


def quantile_bar_chart(df, spd, title):
    spds = [25, 30, 35, 40, 45, 50]
    x = spds.index(spd)

    l = df.quantile(0.95)
    data = []
    for i in range(4, 22):
        data.append(l[i])
    times = [
        "6AM-7AM",
        "7AM-8AM",
        "8AM-9AM",
        "9AM-10AM",
        "10AM-11AM",
        "11AM-12PM",
        "12PM-1PM",
        "1PM-2PM",
        "2PM-3PM",
        "3PM-4PM",
        "4PM-5PM",
        "5PM-6PM",
        "6PM-7PM",
        "7PM-8PM",
        "8PM-9PM",
        "9PM-10PM",
        "10PM-11PM",
        "11PM-12AM",
    ]

    plot.figure(figsize=(10, 6))
    plot.bar(times, data)
    plot.title(f"{title}: {spd}mph Roads")
    plot.xlabel("Time of Day")
    plot.ylabel("Difference from Posted Speed")
    plot.xticks(rotation=65)
    # plot.show()
    plot.savefig(f"{ev.DATA_ROOT}/{title}{spd}.png")


spds = [25, 30, 35, 40, 45, 50]
for s in spds:
    create_bar_chart(tod_avg_speed(), s, "Average Travel Speed vs Posted Speed by TOD")
    quantile_bar_chart(top5perc_speed(s), s, "Top 5 Percent Speeds by TOD")
