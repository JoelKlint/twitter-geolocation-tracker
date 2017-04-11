import requests
import time
from database.database import Database

def make_search_request(query):
    base_payload = {'username': 'Svenskjefel', 'order_by': 'relevance'}
    base_url = "http://api.geonames.org/searchJSON"
    base_payload['q'] = query
    r = requests.get(base_url, base_payload)
    return r.json()

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

db = Database("twitter-geo")

# Must be less then 2000 an hour
some_user_locations = db.select_user_locations()


throttle_count = 0

no_result_count = 0

for location in some_user_locations:
    throttle_count += 1

    if throttle_count == 1950:
        time.sleep(60)

    user_id = location[0]
    user_location = location[1]
    preprocessed_data = db.select_preprocessed_data_from_user_id(user_id)
    preprocessed_location = preprocessed_data[0]
    preprocessed_rest = None
    if len(preprocessed_data) > 1:
        preprocessed_rest = preprocessed_data[1]

    #Check given user location
    query = user_location
    print ("Sending query for: ", query)
    result = make_search_request(query)
    print (result)
    total_results = result['totalResultsCount']

    if total_results > 0:
        print("FOUND RESULT")
        id = result['geonames'][0]['geonameId']
        country_name = result['geonames'][0].get('countryName', None)
        db.insert_into_identified_via_geonames(user_id, id, country_name)
    else:
        # Check our preprocessed locations
        print ("Failed.... Checking Preprocessed locations")
        query = preprocessed_location
        print ("Sending query for: ", query)
        result = make_search_request(query)
        if result['totalResultsCount'] > 0:
            print ("FOUND RESULT")
            id = result['geonames'][0]['geonameId']
            country_name = result['geonames'][0].get('countryName', None)
            db.insert_into_identified_via_geonames(user_id, id, country_name)
        else:
            # Check our preprocessed preprocessed rest
            print('Failed.... Checking Rest of preprocess if exists')
            if (preprocessed_rest):
                query = preprocessed_rest
                result = make_search_request(query)
                print ("Sending query for: ", query)
                if (result['totalResultsCount'] > 0):
                    id = result['geonames'][0]['geonameId']
                    country_name = result['geonames'][0].get('countryName', None)
                    db.insert_into_identified_via_geonames(user_id, id, country_name)
            else:
                #CHECKING EACH INDIVIDUAL WORD
                print('Failed.... Checking Every Word')
                list_words = split_to_words(preprocessed_location)
                if (preprocessed_rest):
                    list_words += split_to_words(preprocessed_rest)
                for word in list_words:
                    query = word
                    print ("Sending query for: ", word)
                    result = make_search_request(query)
                    if result['totalResultsCount'] > 0:
                        id = result['geonames'][0]['geonameId']
                        country_name = result['geonames'][0].get('countryName', None)
                        db.insert_into_identified_via_geonames(user_id, id, country_name)
                        break
                    else:
                        print ("Still no result")
                        no_result_count += 1

                # MAYBE DO A FALLOVER TO LOCATIONS IN DBPEDIA SPOTLIGHT?
                # Seems hard since its politics, though might be possible with locations



print('No result for: ', no_result_count, " queries")