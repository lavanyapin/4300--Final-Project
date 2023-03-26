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
    city = query.split()[0]
    dict_list = []
    keywords = query.split()[1:]
    for x in range(len(keywords)):
        word = keywords[x]
        query_sql_city = f"""SELECT DISTINCT business_filtered.bus_name, business_filtered.city,business_filtered.us_state FROM reviews JOIN (SELECT * FROM businesses WHERE LOWER(city) LIKE '%%{city.lower()}%%') business_filtered ON (business_filtered.bus_id = reviews.bus_id) WHERE LOWER(rev_text) LIKE '%%{word.lower()}%%'"""
        keys = ["bus_name","city","us_state"]
        # breaking here on 2nd iteration      
        data = mysql_engine.query_selector(query_sql_city)
        this_list = [dict(zip(keys,i)) for i in data]
        dict_list.extend(this_list)
    dedup_list = [i for n, i in enumerate(dict_list) if i not in dict_list[n + 1:]]
    return json.dumps(dict_list)

@app.route("/")
def home():
    return render_template('base.html',title="sample html")

@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    return sql_search(text)

app.run(debug=True)