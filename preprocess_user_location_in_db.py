import psycopg2
from database.database import Database

db = Database("twitter-geo")

print("Starts the preprocess, This takes about an hour. Consider loading a dump instead.")

all_users = db.get_all_users_with_location()

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
        db.insert_into_preprocessed(location, user[0], rest)
    else:
        db.insert_into_preprocessed(user[1], user[0])
    i+= 1

    if (i%10000 == 0):
        print('We have completed: ', i)

print ("Done preprocessing")