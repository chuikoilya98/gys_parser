import sqlite3
from datetime import datetime
import os.path as pt
import json
from unittest import result

#conn = sqlite3.connect(pt.abspath("database.db"))

#cursor = conn.cursor()

#cursor.execute("""CREATE TABLE sneakers (source text, id text, name text, brand text, price text, oldprice text, image text, sizes text, link text , executed text, dateexecuted text, dateadd text)""")


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
                name = item['name'].remove("'")
                sizes = ''
                for size in item['sizes']:
                    sizes += size
                    sizes += ' '
                query = f"""
            INSERT INTO sneakers
            VALUES ('{item['source']}', '{item['id']}', '{name}', '{item['brand']}', '{item['price']}', '{item['oldPrice']}', '{item['image']}', '{sizes}', '{item['link']}', 'N' , '0' , '{dateAdd}')
            """
                cursor.execute(query)
                conn.commit()

    def getNonExecutedItems(self, count=1, brand=None) -> dict:
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
        products = []
        for item in result:
            product = {
                'source': item[0],
                'id': item[1],
                'name': item[2],
                'brand': item[3],
                'price': item[4],
                'oldPrice': item[5],
                'image': item[6],
                'sizes': item[7],
                'link': item[8],
            }
            products.append(product)
            conn = sqlite3.connect(pt.abspath("database.db"))
            cursor = conn.cursor()
            sql = f"""UPDATE sneakers
            SET executed = 'Y', dateexecuted = '{str(datetime.now())}'
            WHERE id = '{item[1]}'
            """
            cursor.execute(sql)
            conn.commit()

        final = {
            'success': True,
            'count': count,
            'items': products
        }

        return final
