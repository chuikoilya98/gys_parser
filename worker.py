from bot import Bot
from db import Database


def start():
    db = Database()
    bot = Bot()

    items = db.getNonExecutedItems()
    bot.sendItemToChannel(item=items['items'][0])


if __name__ == '__main__':
    start()
