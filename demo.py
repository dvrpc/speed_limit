from plan_belt.conflation import conflator

conflator(
    "speed_limit",  # name of your database
    "localhost",  # name of your config file in pg_etl config file
    "inrix_2021",  # name of input table (what you want to conflate)
    "inrix",  # what you want the output table to be named
    "objectid",  # uid of conflate layer
    "OBJECTID",  # uid of base layer
    "typologies",  # base layer that you want to conflate to
    "b.REFSPDMEAN, b.REFSPDMIN, b.REFSPDMAX",  # columns from conflate layer you want to include. if multiple, just use b. for each. like 'b.line, b.geom'
    5,  # distance threshold in meters. 5 is a good starting point but might need to tune
    70,  # overlap percentage. leave at 70, go smaller if many false negatives, bigger if many false postives
)

print("conflated!")
