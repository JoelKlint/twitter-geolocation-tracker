from flask import Flask, render_template, jsonify
from database_text_searcher import Database
app = Flask(__name__)


DB_NAME = 'twitter-geo'

print('Connection Completed')


@app.route("/statistics", methods=['GET'])
def statistics():
    db = Database(DB_NAME)

    tweet_count = db.get_total_tweet_count()
    clean_retweet_count = db.get_total_clean_retweet_count()
    commented_retweet_count = db.get_total_commented_retweet_count()
    reply_tweet_count = db.get_total_reply_count()
    total_mention_count = db.get_total_mention_count()
    original_tweets_count = db.get_original_tweets_count()


    return render_template('statistics.html', 
        tweet_count=tweet_count,
        clean_retweet_count=clean_retweet_count, 
        commented_retweet_count=commented_retweet_count,
        reply_tweet_count=reply_tweet_count,
        total_mention_count=total_mention_count,
        original_tweets_count=original_tweets_count
    )


@app.route("/", methods=['GET'])
def index():
    db = Database(DB_NAME)
    nbrOfUsers = db.selectNumberOfUsers()
    return render_template('base.html', nbrOfUsers=nbrOfUsers)

@app.route("/search/", methods=['GET'])
@app.route("/search/<table>", methods=['GET'])
def searchTemplate(table='users'):
    db = Database(DB_NAME)
    tables = db.selectAllTables()
    if (table):
        data = db.generateTableData(table)
    return render_template('search.html', tables=tables, data=data)

@app.route("/cluster_data", methods=['GET'])
def cluster():
    return render_template('cluster_data.html')

# @app.route("/cluster_data/get_data", methods=['GET'])
# def get_data():
#     db = Database(DB_NAME)
#     data = db.select_users_with_predicted_coordinates()
#     list_data = []
#     for dp in data:
#         lat = float(dp[1])
#         long = float(dp[2])
#         list_data.append([lat, long])
#     result = list_data
#     return jsonify(result)


# This is just a mock. Fill it will real data
@app.route('/locations', methods=['GET'])
def get_locations():
    locations = [
        {'lat': -31.563910, 'lng': 147.154312},
        {'lat': -33.718234, 'lng': 150.363181},
        {'lat': -33.727111, 'lng': 150.371124},
        {'lat': -33.848588, 'lng': 151.209834},
        {'lat': -33.851702, 'lng': 151.216968},
        {'lat': -34.671264, 'lng': 150.863657},
        {'lat': -35.304724, 'lng': 148.662905},
        {'lat': -36.817685, 'lng': 175.699196},
        {'lat': -36.828611, 'lng': 175.790222},
        {'lat': -37.750000, 'lng': 145.116667},
        {'lat': -37.759859, 'lng': 145.128708},
        {'lat': -37.765015, 'lng': 145.133858},
        {'lat': -37.770104, 'lng': 145.143299},
        {'lat': -37.773700, 'lng': 145.145187},
        {'lat': -37.774785, 'lng': 145.137978},
        {'lat': -37.819616, 'lng': 144.968119},
        {'lat': -38.330766, 'lng': 144.695692},
        {'lat': -39.927193, 'lng': 175.053218},
        {'lat': -41.330162, 'lng': 174.865694},
        {'lat': -42.734358, 'lng': 147.439506},
        {'lat': -42.734358, 'lng': 147.501315},
        {'lat': -42.735258, 'lng': 147.438000},
        {'lat': -43.999792, 'lng': 170.463352}
    ]

    db = Database(DB_NAME)
    data = db.select_users_with_predicted_coordinates()

    return jsonify(data)

    # {
    #     user_id: user_id,
    #     lat: predicted_lat,
    #     lng: predicted_long,
    #     value: max_value,
    # }


app.run(debug=True)