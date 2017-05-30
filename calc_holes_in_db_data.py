import psycopg2
import functools
import datetime

# Connect to the db
conn = psycopg2.connect("dbname=twitter-geo")


# Fetch stuff from db
cur = conn.cursor()
cur.execute('select distinct(created_at) from tweets;')
result = cur.fetchall()
cur.close()
# Get rid of tuples
result = list(map(lambda a: a[0], result))
# Work on a minute level 
result = list(map(lambda a: a.replace(second=0, microsecond=0), result))
# Remove duplicates
result = set(result)
# Convert to list
result = list(result)
# Sort
result = sorted(result)

# Find non aligned values
for i in range(len(result)):
    # Convert to seconds
    if(i == 0):
        continue

    # Get the two values
    start = result[i-1]
    end = result[i]

    # Convert to seconds
    a = start.timestamp()
    b = end.timestamp()

    # Print non aligned values
    if(b-a != 60):
        print("FOUND HOLE")
        print("Last insert time: {}".format(start))
        print("First insert time: {}".format(end))
        print("")