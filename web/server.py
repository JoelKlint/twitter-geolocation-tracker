from flask import Flask, render_template
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


    return render_template('statistics.html', 
        tweet_count=tweet_count,
        clean_retweet_count=clean_retweet_count, 
        commented_retweet_count=commented_retweet_count,
        reply_tweet_count=reply_tweet_count,
        total_mention_count=total_mention_count)


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


@app.route("/test")
def test():
    db = Database(DB_NAME)
    db.nbrOfUsersWithLocation()



app.run(debug=True)