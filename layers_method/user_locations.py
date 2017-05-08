import psycopg2
import geonames_api_application as geo_api

def create_bounding_box(coordinates, padding):
    return [float(coordinates[0])-padding, float(coordinates[1])-padding,
            float(coordinates[0])+padding, float(coordinates[1])+padding]


def execute_query_for_identified_location(user_screen_name):
    conn = psycopg2.connect('dbname={}'.format('twitter-geo'))
    cur = conn.cursor()

    statment = '''
    select user_id, longitude, latitude
    from geonames natural join identified_via_geonames natural join users
    where longitude <> 0 and latitude <> 0 and user_screen_name = %s;
    '''

    cur.execute(statment, (user_screen_name,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def find_user_id(user_screen_name):
    conn = psycopg2.connect('dbname={}'.format('twitter-geo'))
    cur = conn.cursor()

    statment = '''
        select user_id
        from  users
        where user_screen_name = %s;
        '''

    cur.execute(statment, (user_screen_name,))
    user_id = cur.fetchone()
    cur.close()
    conn.close()
    return user_id

def get_bbox(user_screen_name):
    padding = 1
    print ('user_screen_name is:',user_screen_name)
    user_id_and_coordinates = execute_query_for_identified_location(user_screen_name)

    #Eiter the user has not given a user locations, or it has not yet been handled
    if user_id_and_coordinates == None:
        print('Got Null in database check!')
        #Try a lookup in geonames and try to get a new location
        #print ('Doing Extra lookup!')
        user_id = find_user_id(user_screen_name)
        geo_api.run_location_lookup_on_a_user(user_id)
        user_id_and_coordinates = execute_query_for_identified_location(user_screen_name)
        #New user location found
        if user_id_and_coordinates != None:
            print ('Got Null in geonames check')
            #print ('New Lookup location found location!')
            coordinates = [user_id_and_coordinates[1], user_id_and_coordinates[2]]
            return create_bounding_box(coordinates, padding)

        return None
    #print ("Ordinary location found")
    coordinates = [user_id_and_coordinates[1], user_id_and_coordinates[2]]
    # Padding the bb with 1 degree
    return create_bounding_box(coordinates, padding)