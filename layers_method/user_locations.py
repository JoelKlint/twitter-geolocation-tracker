import psycopg2

def create_bounding_box(coordinates):
    return [float(coordinates[0])-1, float(coordinates[1])-1,
            float(coordinates[0])+1, float(coordinates[1])+1]


def get_bounding_box_of_user():
    conn = psycopg2.connect('dbname={}'.format('twitter-geo'))
    cur = conn.cursor()

    statment = '''
    select longitude, latitude
    from geonames natural join identified_via_geonames natural join users
    where longitude <> 0 and latitude <> 0
    limit 1;
    '''

    cur.execute(statment)
    coordinates = cur.fetchone()
    cur.close()
    conn.close()
    return create_bounding_box(coordinates)