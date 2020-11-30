from flask import request, g
from flask_restful import Resource
import psycopg2
import psycopg2.extras
import logging


item_list = []

logger = logging.getLogger(__file__)

class Item(Resource):

    
    def get(self, name):
        item = next(filter(lambda x: x['name']== name, item_list), None)
        count = 0
        try:
            with g.db.cursor() as db_cursor:
                db_cursor.execute('SELECT COUNT(*) FROM CONVERSATIONS')
                row = db_cursor.fetchone()
                logger.info('information retried from database')
                if row and row[0]:
                    count = row[0]
                else:
                    count = 0
            logger.info('Successful execution of data retrieval')
        except:
            print('exception happened')
        finally:
            pass

        item['price'] = count

        return {'item': item}, 200 if item else 404

    def post(self, name):

        if next(filter(lambda x: x['name'] == name, item_list), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        item = { 'name' : name, 'price': data['price']}
        item_list.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': item_list}