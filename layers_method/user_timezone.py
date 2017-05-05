# 
# This file translates time zones to bounding boxes by coordinates
# 

from country_bounding_boxes import (
    country_subunits_containing_point,
    country_subunits_by_iso_code
)
import psycopg2
import os
dir = os.path.dirname(__file__)
filename = os.path.join(dir, '../data/tzdb-2017b/zone.tab')

def get_countries_using_time_zone(db_time_zone):
    # This file contains which countries that use a specific time zone
    # timezones = open('../data/tzdb-2017b/zone1970.tab', 'r', encoding="utf-8")
    timezones = open(filename, 'r', encoding="utf-8")

    for line in timezones:
        # Skip garbage
        if(line[0] == '#'):
            continue
        # Match names of time zones
        splitted_line = line.split('\t')
        if db_time_zone in splitted_line[2]:
            # Getch ISO 2 letter country codes
            return splitted_line[0].split(',')

    return None

def get_special_bbox_special_treatment(db_time_zone):
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

def get_time_zone_from_db_for_user(user_screen_name):
    # Fetch all time_zones from db
    conn = psycopg2.connect('dbname={}'.format('twitter-geo'))
    cur = conn.cursor()
    statement = """
        SELECT user_time_zone
        FROM users
        WHERE user_screen_name = %s
        LIMIT 1
    """
    cur.execute(statement, (user_screen_name,))
    conn.commit()
    db_time_zone = cur.fetchall()
    cur.close()
    return db_time_zone[0][0]


def get_bboxes_from_db_time_zone(db_time_zone):
    # Make the strings match
    time_zone = db_time_zone.replace(' ', '_')

    # We got a hit
    country_codes = get_countries_using_time_zone(time_zone)
    bbox = None
    if country_codes != None: # Look in tz database
        for country_code in country_codes:
            bboxes = [c.bbox for c in country_subunits_by_iso_code(country_code)]
            return bboxes
            # for coords in bboxes:
            #     # We have a bounding box
            #     bbox = coords
    elif get_special_bbox_special_treatment(time_zone) != None: # Look in special treatments
        # We have a bounding box
        bbox = get_special_bbox_special_treatment(time_zone)
        return [bbox]
    else:
        # We could not find a bounding box
        return None


# The main entry point for this script
def get_bboxes(time_zone):
    bboxes = get_bboxes_from_db_time_zone(time_zone)
    return bboxes