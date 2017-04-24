# 
# This file translates time zones to bounding boxes by coordinates
# 

from country_bounding_boxes import (
    country_subunits_containing_point,
    country_subunits_by_iso_code
)
import psycopg2
import sys

def get_countries_using_time_zone(db_time_zone):

    # timezones = open('../data/tzdb-2017b/zone1970.tab', 'r', encoding="utf-8")
    timezones = open('../data/tzdb-2017b/zone.tab', 'r', encoding="utf-8")
    for line in timezones:

        # Skip garbage
        if(line[0] == '#'):
            continue

        # Match names of time zones
        splitted_line = line.split('\t')
        if db_time_zone in splitted_line[2]:
            # Getch ISO 2 letter country codes
            return splitted_line[0].split(',')

    # Handle cases that could not be found
    special_cases = {
        'Central_Time_(US_&_Canada)': (-109.34, 10.7, -85.41, 82.44),
        'Pacific_Time_(US_&_Canada)': (-141.3, 26.6, -114.3, 78.0),
        'Eastern_Time_(US_&_Canada)': (-90.18, 1.45, -64.78, 83.13),
        'Mountain_Time_(US_&_Canada)': (-134.3, 17.9, -101.9, 79.3),
        'Arizona': (-114.8166, 31.3322, -109.0452, 37.0043),
        'Quito': (-80.86, -5.01, -75.19, 2.3),
        'Atlantic_Time_(Canada)': (-69.61, 43.48, -54.49, 60.31),
        'Hawaii': (-178.4, 18.9, -154.8 ,28.5),
        'Alaska': (172.35, 51.18, -129.98, 71.44),
        'New_Delhi': (68.1, 6.5 ,97.4, 35.5),
        'Chennai': (68.1, 6.5 ,97.4, 35.5),
        'Brasilia': (-74.0, -34.1, -28.7, 5.3),
        'Indiana_(East)': (-88.1, 37.77, -84.78, 41.76),
        'Greenland': (-73.8, 58.3, -8.3, 84.0),
        'Bern': (5.96, 45.82, 10.49, 47.81),
        'Central_America': (-92.27, 5.5, -77.16, 18.5),
        'Beijing': (73.5, 18.0, 134.77, 53.56),
        'Edinburgh': (-14.02, 49.67, 2.09, 61.06),
        'Pretoria': (16.28, -35.14, 38.22, -22.13),
    }

    special_case = special_cases.get(db_time_zone, None)
    if special_case != None:
        return special_case
        
    return None
        
        

# Fetch all time_zones from db
conn = psycopg2.connect('dbname={}'.format('twitter-geo'))
cur = conn.cursor()
# statement = """
#     SELECT user_time_zone, count(*) as c
#     FROM users
#     WHERE user_time_zone IS NOT NULL
#     GROUP BY user_time_zone
#     ORDER BY c DESC;
# """
statement = """
    SELECT user_time_zone
    FROM users
    WHERE user_time_zone IS NOT NULL
    LIMIT 1;
"""
cur.execute(statement)
conn.commit()
time_zones_from_db = cur.fetchall()
cur.close()

# This file contains which countries that use a specific time zone

for current_time_zone in time_zones_from_db:
    # Make the strings match
    time_zone = current_time_zone[0].replace(' ', '_')

    # We got a hit
    if get_countries_using_time_zone(time_zone) != None:
        



# for country in countries:
#     bboxes = [c.bbox for c in country_subunits_by_iso_code(country)]
#     for bbox in bboxes:
#         print()
#         print(country)
#         print(bbox)
#         min_long = bbox[0]
#         min_lat = bbox[1]
#         max_long = bbox[2]
#         max_lat = bbox[3]
#         print('{0}, {1}, {2}, {3}'.format(min_long, min_lat, max_long, max_lat))
