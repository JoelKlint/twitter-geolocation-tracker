from country_bounding_boxes import (
    country_subunits_containing_point,
    country_subunits_by_iso_code
)
import os
import json

COUNTRY_INDEX = 0
LANG_INDEX = 15

# Recieves a lang string and converts it so it can be used with langs for tweets in our db
def convert_lang(lang):
    if(len(lang) == 2):
        return lang
    elif(len(lang) == 3):
        return None
    elif(len(lang) == 5):
        return lang[:2]
    else:
        return None

# Returns bounding boxes for a country.
# The country MUST be specified in two letter ISO format
def get_bounding_boxes_for_country(country_code):
    return [c.bbox for c in country_subunits_by_iso_code(country_code)]

# Get all country codes that speak a language
def get_country_codes_speaking_lang(tweet_lang):

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'map_lang_to_countries.json')
    if(not os.path.isfile(filename)):
        preprocess_lang_file()
    
    res = []
    with open(filename, 'r') as data_file:    
        data = json.load(data_file)
        return data.get(tweet_lang)

# The entry point for this layer
def get_bboxes(tweet_lang):
    countries = get_country_codes_speaking_lang(tweet_lang)
    if(countries != None):
        bboxes = list(map(get_bounding_boxes_for_country, countries))
        return bboxes

# This can be run to 
def preprocess_lang_file():
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../data/geonames/countryInfo.txt')
    country_languages = open(filename, 'r', encoding="utf-8")

    res = {}

    for line in country_languages:
        # Skip comments
        if(line[0] == '#'):
            continue
        
        splitted_line = line.split('\t')

        # Get country
        country = splitted_line[COUNTRY_INDEX]

        # Get all langs in a list
        langs = splitted_line[LANG_INDEX].split(',')
        langs = list(map(convert_lang, langs))
        langs = list(filter(None, langs))

        for lang in langs:
            if(res.get(lang) == None):
                res[lang] = []
            res[lang].append(country)

    file = open('map_lang_to_countries.json', 'w') 
    file.write(json.dumps(res, sort_keys=True, indent=4, separators=(',', ': ')))
    file.close() 
    print('Saved preprocessed file in map_lang_to_countries.json')