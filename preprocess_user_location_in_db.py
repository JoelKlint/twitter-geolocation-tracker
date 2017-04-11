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

def insert_into_preprocessed(location, user_id, rest=None):
    cur = conn.cursor()
    if rest != None:
        statement = """
            UPDATE users
            SET preprocessed_location = %s,
                preprocessed_rest = %s
            WHERE user_id = %s
        """
        cur.execute(statement, (location, rest, user_id))
    else:
        statement = """
            UPDATE users
            SET preprocessed_location = %s,
                preprocessed_rest = DEFAULT
            WHERE user_id = %s
        """
        cur.execute(statement, (location, user_id))
    conn.commit()
    cur.close()

all_users = get_all_users_with_location()

i = 0

for user in all_users:
    index = user[1].find(",")
    if(index > -1):
        location = user[1][0:index]
        rest = user[1][index:]
        user = (user[0],) + (location, rest,)
        rest_split = user[2].split(',')
        if (len(rest_split) > 1 and len(rest_split) < 3 and not(rest_split[1] == "") and rest_split[1][0] == " "):
            rest = rest_split[1][1:]
        else:
            rest = ",".join(rest_split)
        insert_into_preprocessed(location, user[0], rest)
    else:
        insert_into_preprocessed(user[1], user[0])
    i+= 1

    if (i%10000 == 0):
        print('We have completed: ', i)
    #print(location)
    #print (rest)
    #print(user[0])
    #



    # Save in DB
    # ALTER TABLE IN DB