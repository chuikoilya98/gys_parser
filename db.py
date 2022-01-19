import sqlite3
from datetime import datetime
import os.path as pt
import json

#conn = sqlite3.connect(pt.abspath("database.db"))

#cursor = conn.cursor()

"""CREATE TABLE sneakers
source text, id text, name text, brand text, price text, oldprice text, image text, sizes text, link text , executed text, dateexecuted text, dateadd text)
"""


class Database():

    def createItemsFromDict(self, items: dict) -> None:
        conn = sqlite3.connect(pt.abspath("database.db"))
        cursor = conn.cursor()
        for item in items['items']:
            dateAdd = str(datetime.now())
            query = f"""
         INSERT INTO sneakers
         VALUES ('{item['source']}', {item['id']}, {item['name']}, {item['brand']}, {item['price']}, {item['oldPrice']}, {item['image']}, {item['sizes']}, 1, N , 0 , {dateAdd})
         """
            cursor.execute(query)
            conn.commit()

    def getNonExecutedItems(self):
        conn = sqlite3.connect(pt.abspath("database.db"))
        cursor = conn.cursor()
        query = """
        SELECT * FROM sneakers 
        """
        cursor.execute(query)
        print(cursor.fetchall())


k = Database()

with open(pt.abspath('test.json'), 'r') as file:
    data = json.load(file)
    k.createItemsFromDict(items=data)
    k.getNonExecutedItems()
