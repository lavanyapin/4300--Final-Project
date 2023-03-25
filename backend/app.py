import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "gan4646"
MYSQL_PORT = 3306
MYSQL_DATABASE = "yelp"

mysql_engine = MySQLDatabaseHandler(MYSQL_USER,MYSQL_USER_PASSWORD,MYSQL_PORT,MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded, 
# but if you decide to use SQLAlchemy ORM framework, 
# there's a much better and cleaner way to do this
# Dictionary ={1:'Welcome', 2:'to',
#             3:'Geeks', 4:'for',
#             5:'Geeks'}
def sql_search(query):
    query_sql_city = f"""SELECT * FROM businesses WHERE LOWER( city ) LIKE '%%{query.split()[0].lower()}%%'"""
    query_sql_review = f"""SELECT rev_text FROM reviews JOIN (businesses) ON (businesses.bus_id = reviews.bus_id)"""
    # query_sql_city = f"""SELECT rev_text FROM reviews JOIN (SELECT * FROM businesses WHERE LOWER( city ) LIKE '%%{query.split()[0].lower()}%%') ON (businesses.bus_id = reviews.bus_id) WHERE LOWER(rev_text) like '%%{query.split()[1].lower()}%%'"""
    keys = ["id","business_name","city", "us_state"]
    data = mysql_engine.query_selector(query_sql_city)
    return json.dumps([dict(zip(keys,i)) for i in data])
    # json_string = json.dumps(Dictionary)

@app.route("/")
def home():
    return render_template('base.html',title="sample html")

@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)

app.run(debug=True)