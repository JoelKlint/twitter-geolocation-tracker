#This file compares the "places" table with "geonames" table with plain old contains.
from database.database import Database
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


db = Database("twitter-geo")

user_locations = db.select_user_locations()
db_locations = db.select_database_locations()
found_locations = []
for user_location in user_locations:
    print ("Parsing: ", user_location)
    max = 0
    max_geoid = 0
    has_been_inserted = False
    for db_location in db_locations:
        if not(db_location[1] == None):
            ratio = similar(user_location[1], db_location[1])
            if ratio == 1:
                db.set_filtered_location(user_location[0], db_location[0], ratio)
                has_been_inserted = True
                break
            elif ratio > max:
                max = ratio
                max_geoid = db_location[0]

        elif not(db_location[2] == None):
            ratio = similar(user_location[1], db_location[2])
            if ratio == 1:
                db.set_filtered_location(user_location[0], db_location[0], ratio)
                has_been_inserted = True
                break
            elif ratio > max:
                max = ratio
                max_geoid = db_location[0]

    if (max_geoid != 0 and not(has_been_inserted)):
        db.set_filtered_location(user_location[0], max_geoid, max)

print ("WE ARE DONE")