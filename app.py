from flask import Flask, g, jsonify, got_request_exception
from flask_restful import Resource, Api
from resources.Item import Item, ItemList
from flask_cors import CORS
import psycopg2
from psycopg2 import pool
import logging, traceback
from config import config

# def get_db():
#     print ('GETTING CONN')
#     if 'db' not in g:
#         g.db = app.config['postgreSQL_pool'].getconn()
#     return g.db

app = Flask(__name__)
CORS(app)
# app.config['postgreSQL_pool'] = psycopg2.pool.SimpleConnectionPool(1, 20,user = USER,
#                                                   password = PASSWORD,
#                                                   host = HOST,
#                                                   port = PORT,
#                                                   database = DATABASE)

logger = logging.getLogger('root')
database_cred = config["postgres_creds"]

app.config['postgreSQL_pool'] = psycopg2.pool.ThreadedConnectionPool(2, 20,user = database_cred["user"],
                                                  password = database_cred["password"],
                                                  host = database_cred["host"],
                                                  port = database_cred["port"],
                                                  database = database_cred["database"])

def log_exception(sender, exception, **extra):
    logger.error(traceback.format_exc())

@app.before_request
def set_connection():
    print('Setting a db connection to app_context g')
    g.db = app.config['postgreSQL_pool'].getconn()

@app.teardown_appcontext
# @app.teardown_request
def close_conn(e):
    print('releasing a db connection to app_context g')
    db = g.pop('db', None)
    if db is not None:
        app.config['postgreSQL_pool'].putconn(db)

@app.route('/getConversationCount')
def index():
  
    cursor = g.db.cursor()
    cursor.execute("SELECT COUNT(*) FROM CONVERSATIONS;")
    result = cursor.fetchall()
    logger.info(result)

    cursor.close()
    return jsonify(result)

api = Api(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == "__main__":
    app.run(port=5000, debug= True)
    got_request_exception(log_exception, app)


