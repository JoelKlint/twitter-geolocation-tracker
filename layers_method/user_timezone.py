# 
# This file translates time zones to bounding boxes by coordinates
# 

from country_bounding_boxes import (
    country_subunits_containing_point,
    country_subunits_by_iso_code
)
import psycopg2
import os
import json

def get_countries_using_time_zone(timezone):

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'map_timezone_to_country.json')
    if(not os.path.isfile(filename)):
        preprocess_timezone_file()
    
    res = []
    with open(filename, 'r') as data_file:    
        data = json.load(data_file)
        return data.get(timezone.strip('\n'))

def get_bbox_special_treatment(db_time_zone):
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

    return special_cases.get(db_time_zone, None)


def get_bboxes_from_time_zone(db_time_zone):
    # Make the strings match
    time_zone = db_time_zone.replace(' ', '_')

    # We got a hit
    country_code = get_countries_using_time_zone(time_zone)
    bboxes = []
    if country_code != None: # Look in tz database
        return [c.bbox for c in country_subunits_by_iso_code(country_code)]

    elif get_bbox_special_treatment(time_zone) != None: # Look in special treatments
        # We have a bounding box
        return [get_bbox_special_treatment(time_zone)]
    else:
        # We could not find a bounding box
        return None

# The main entry point for this script
def get_bboxes(timezone):
    bboxes = get_bboxes_from_time_zone(timezone)
    return bboxes

def preprocess_timezone_file():
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../data/tzdb-2017b/zone.tab')
    timezones = open(filename, 'r', encoding="utf-8")

    res = {}
    for line in timezones:
        # Skip garbage
        if(line[0] == '#'):
            continue

        
        # Match names of time zones
        splitted_line = line.split('\t')
        country = splitted_line[0]
        timezone = splitted_line[2].strip('\n')
        res[timezone] = country

    file = open('map_timezone_to_country.json', 'w') 
    file.write(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))
    file.close() 
    print('Saved preprocessed file in map_timezones_to_country.json')