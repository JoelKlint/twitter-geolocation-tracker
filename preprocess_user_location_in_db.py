import psycopg2

conn = psycopg2.connect('dbname={}'.format("twitter-geo"))

def get_all_users_with_location():
    cur = conn.cursor()

    statement = """
        SELECT user_id, user_location
        FROM users
        WHERE user_location IS NOT NULL
    """

    cur.execute(statement)
    conn.commit()
    result_tuple = cur.fetchall()
    cur.close()

    return result_tuple

all_users = get_all_users_with_location()

for user in all_users:
    index = user[1].find(",")
    if(index > -1):
        location = user[1][0:index]
        rest = user[1][index:]
        user = (user[0],) + (location, rest,)

    # Save in DB
    # ALTER TABLE IN DB