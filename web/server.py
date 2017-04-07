from flask import Flask, render_template
from database import Database
app = Flask(__name__)


DB_NAME = 'twitter-geo'

print('Connection Completed')

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