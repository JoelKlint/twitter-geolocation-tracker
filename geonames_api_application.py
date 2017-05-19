import requests
import time
from database.database import Database

def make_search_request(query):
    base_payload = {'username': 'Svenskjefel', 'order_by': 'relevance'}
    base_url = "http://api.geonames.org/searchJSON"
    base_payload['q'] = query
    r = requests.get(base_url, base_payload)
    return r.json()

#Not used
def split_on_common_characters(query):
    result = []
    if '/' in query:
        result = query.split('/')
    elif '|' in query:
        result = query.split('|')
    elif ';' in query:
        result = query.split(';')
    elif ':' in query:
        result = query.split(':')
    elif '-' in query:
        result = query.split('-')
    elif '.' in query:
        result = query.split('.')

    return result

def split_to_words(query):
    if " " in query:
        return query.split(" ")
    listify = []
    listify.append(query)
    return listify

def lookup(db, location, throttle_count=0, no_result_count=0):
    throttle_count += 1

    if throttle_count == 1950:
        time.sleep(3650)

    user_id = location[0]
    user_location = location[1]
    preprocessed_data = db.select_preprocessed_data_from_user_id(user_id)
    preprocessed_location = preprocessed_data[0]
    preprocessed_rest = None
    if len(preprocessed_data) > 1:
        preprocessed_rest = preprocessed_data[1]

    #Check given user location
    query = user_location
    result = make_search_request(query)
    total_results = result['totalResultsCount']

    if total_results > 0:
        id = result['geonames'][0]['geonameId']
        country_name = result['geonames'][0].get('countryName', None)
        db.insert_into_identified_via_geonames(user_id, id, country_name)
    else:
        # Check our preprocessed locations
        query = preprocessed_location
        result = make_search_request(query)
        if result['totalResultsCount'] > 0:
            id = result['geonames'][0]['geonameId']
            country_name = result['geonames'][0].get('countryName', None)
            db.insert_into_identified_via_geonames(user_id, id, country_name)
        else:
            # Check our preprocessed preprocessed rest
            if (preprocessed_rest):
                query = preprocessed_rest
                result = make_search_request(query)
                if (result['totalResultsCount'] > 0):
                    id = result['geonames'][0]['geonameId']
                    country_name = result['geonames'][0].get('countryName', None)
                    db.insert_into_identified_via_geonames(user_id, id, country_name)
            else:
                #CHECKING EACH INDIVIDUAL WORD
                list_words = split_to_words(preprocessed_location)
                if (preprocessed_rest):
                    list_words += split_to_words(preprocessed_rest)
                for word in list_words:
                    query = word
                    result = make_search_request(query)
                    if result['totalResultsCount'] > 0:
                        id = result['geonames'][0]['geonameId']
                        country_name = result['geonames'][0].get('countryName', None)
                        db.insert_into_identified_via_geonames(user_id, id, country_name)
                        break
                    else:
                        no_result_count += 1


def run_location_lookup_on_all_users():
    db = Database("twitter-geo")
    some_user_locations_with_ids = db.select_user_locations()
    no_result_count = 0
    for location in some_user_locations_with_ids:
        throttle_count = 0
        lookup(db, location, throttle_count, no_result_count)

def run_location_lookup_on_a_user(user_id):
    db = Database("twitter-geo")
    user_location = db.select_locations_based_on_user_id(user_id)
    if len(user_location) > 0:
        lookup(db, user_location[0])
