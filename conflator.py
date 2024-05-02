from plan_belt.conflation import conflator

# ensure all geometry fields are called "geom" and objectid fields are lowercase
# conflation results are in postgres schema "rejoined"

conflator(
    "speed_limit",  # name of your database
    "localhost",  # name of your config file in pg_etl config file
    "inrix_2021",  # name of input table (what you want to conflate)
    "inrix",  # what you want the output table to be named
    "objectid",  # uid of conflate layer
    "objectid",  # uid of base layer
    "typologies",  # base layer that you want to conflate to
    "b.REFSPDMEAN, b.REFSPDMIN, b.REFSPDMAX, b.spdwkd, b.spdwkd0610, b.spdwkd1519, b.spdwkd0006, b.spdwkd0607, b.spdwkd0708, b.spdwkd0809, b.spdwkd0910, b.spdwkd1011, b.spdwkd1112, b.spdwkd1213, b.spdwkd1314, b.spdwkd1415, b.spdwkd1516, b.spdwkd1617, b.spdwkd1718, b.spdwkd1819, b.spdwkd1920, b.spdwkd2021, b.spdwkd2122, b.spdwkd2223, b.spdwkd2300",  # columns from conflate layer you want to include. if multiple, just use b. for each. like 'b.line, b.geom'
    5,  # distance threshold in meters. 5 is a good starting point but might need to tune
    70,  # overlap percentage. leave at 70, go smaller if many false negatives, bigger if many false postives
)

print("conflated!")
