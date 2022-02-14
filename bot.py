import requests
import json

class Bot():

    TOKEN = '1981681842:AAGa8DKSFXsTaxe4_3DqcVdb02HtSW5c6Y0'
    URL = 'https://api.telegram.org/bot'
    CHAT = '@getyoursneakers'
    ADMIN = '331392389'

    def sendItemToChannel(self, item: dict) -> bool:
        methodName = '/sendPhoto'

        text = f"""
       🔥<b>{item['name']}</b>🔥

{item['oldPrice']} → {item['price']}

{item['sizes']}

Найдено на {item['source']}

<a href='{item['link']}'>Купить</a>
       """
        reply = json.dumps({'inline_keyboard': [[{'text': 'Купить', 'url': item['link']}]]})
        params = {
            'chat_id': self.CHAT,
            'photo': item['image'],
            'caption': text,
            'parse_mode': 'HTML',
            'reply_markup' : reply
        }
        url = self.URL + self.TOKEN + methodName
        req = requests.get(url, params=params)
        print(req.content)

        return True

    def sendAdminMessage(self, text: str) -> bool:

        methodName = '/sendMessage'
        params = {
            'chat_id': self.ADMIN,
            'text': text
        }
        url = self.URL + self.TOKEN + methodName
        req = requests.get(url, params=params)
        return True

k = Bot()

