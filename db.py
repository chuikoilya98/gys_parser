import sqlite3
from datetime import datetime
import os.path as pt
import json
from unittest import result

#conn = sqlite3.connect(pt.abspath("database.db"))

#cursor = conn.cursor()

"""CREATE TABLE sneakers
source text, id text, name text, brand text, price text, oldprice text, image text, sizes text, link text , executed text, dateexecuted text, dateadd text)
"""


class Database():

    def createItemsFromDict(self, items: dict) -> None:
        conn = sqlite3.connect(pt.abspath("database.db"))
        # TODO: есть проблема с наличием символа ' в названии -это вызывает ошибку
        cursor = conn.cursor()
        actualIds = []
        query = """
        SELECT * FROM sneakers
        """
        cursor.execute(query)
        ids = cursor.fetchall()
        for item in ids:
            actualIds.append(item[1])

        for item in items['items']:
            if item['id'] in actualIds:
                continue
            else:
                dateAdd = str(datetime.now())
                sizes = ''
                for size in item['sizes']:
                    sizes += size
                    sizes += ', '
                query = f"""
            INSERT INTO sneakers
            VALUES ('{item['source']}', '{item['id']}', '{item['name']}', '{item['brand']}', '{item['price']}', '{item['oldPrice']}', '{item['image']}', '{sizes}', '1', 'N' , '0' , '{dateAdd}')
            """
                cursor.execute(query)
                conn.commit()

    def getNonExecutedItems(self, count=10, brand=None) -> dict:
        conn = sqlite3.connect(pt.abspath("database.db"))
        cursor = conn.cursor()
        query = """
        SELECT * FROM sneakers WHERE executed = 'N'
        """
        cursor.execute(query)
        data = cursor.fetchall()
        result = []

        for i in range(count):
            result.append(data[i])
        print(result)


k = Database()

with open(pt.abspath('test.json'), 'r') as file:
    data = json.load(file)
    # k.createItemsFromDict(items=data)
    k.getNonExecutedItems()
