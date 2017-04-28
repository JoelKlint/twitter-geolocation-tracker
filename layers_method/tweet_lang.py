from country_bounding_boxes import (
    country_subunits_containing_point,
    country_subunits_by_iso_code
)
import os

ISO_CODE_INDEX = 0
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


def get_country_codes_speaking_lang(tweet_lang):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '../data/geonames/countryInfo.txt')
    country_languages = open(filename, 'r', encoding="utf-8")

    res = []

    for line in country_languages:
        # Skip comments
        if(line[0] == '#'):
            continue
        
        splitted_line = line.split('\t')

        # Get all langs in a list
        langs = splitted_line[LANG_INDEX].split(',')
        langs = list(map(convert_lang, langs))
        langs = list(filter(None, langs))
        
        # Figure out if language is used by country
        country_uses_lang = any([x == tweet_lang for x in langs])
        if(country_uses_lang):
            res.append(splitted_line[ISO_CODE_INDEX])

    return res

# Returns a list of bounding boxes
def get_potential_bounding_boxes_for_tweet_lang(tweet_lang):
    countries = get_country_codes_speaking_lang(tweet_lang)
    bboxes = list(map(get_bounding_boxes_for_country, countries))
    print(countries)
    print(bboxes)
