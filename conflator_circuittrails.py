from plan_belt.conflation import conflator

# ensure all geometry fields are called "geom" and objectid fields are lowercase
# conflation results are in postgres schema "rejoined"

conflator(
    "speed_limit",  # name of your database
    "localhost",  # name of your config file in pg_etl config file
    "circuittrails",  # name of input table (what you want to conflate)
    "typologies_c",  # what you want the output table to be named
    "objectid",  # uid of conflate layer
    "objectid",  # uid of base layer
    "typologies",  # base layer that you want to conflate to
    "b.circuit",  # columns from conflate layer you want to include. if multiple, just use b. for each. like 'b.line, b.geom'
    20,  # distance threshold in meters. 5 is a good starting point but might need to tune
    85,  # overlap percentage. leave at 70, go smaller if many false negatives, bigger if many false postives
)

print("conflated!")
