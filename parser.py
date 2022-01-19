from cgitb import reset
from unittest import result
import requests
import json
from bs4 import BeautifulSoup
import os.path as pt
import re


class Parser():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    def sneakerhead(self) -> dict:
        print('snakerhead')
        url = 'https://sneakerhead.ru/sale/shoes/sneakers/'
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'

        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            pagination = soup.find('div', class_='links')
            links = pagination.find_all('a')
            pages = []
            for link in links:
                try:
                    int(link.text)
                    pages.append(link.text)
                except ValueError:
                    k = 1

            finalItems = []
            for page in pages:

                url = f'https://sneakerhead.ru/sale/shoes/sneakers/?PAGEN_1={page}'
                html = requests.get(url, headers=self.headers)
                html.encoding = 'utf-8'

                if html.status_code == 200:
                    soup = BeautifulSoup(html.text, 'lxml')
                    items = soup.find_all('div', class_='product-cards__item')

                    products = []
                    for item in items:
                        itemId = item.find('div', class_='product-card')
                        brand = item.find('meta', itemprop="manufacturer")[
                            'content']
                        model = item.find('meta', itemprop="name")['content']
                        name = brand + ' ' + model
                        price = item.find('meta', itemprop="price")['content']
                        oldPrice = item.find(
                            'span', class_='product-card__price-value product-card__price-value--old')
                        op = ''

                        for i in oldPrice.text:
                            try:
                                int(i)
                                op += str(i)
                            except ValueError:
                                pass
                        imgSrc = item.find('img', itemprop="image")[
                            'src']
                        image = f'https://sneakerhead.ru{imgSrc}'
                        sizeTable = soup.find(
                            'div', class_='product-card__hover')
                        preSize = sizeTable.find_all('dd')
                        sizes = []
                        for size in preSize:
                            sizes.append(size.text)
                        link = item.find(
                            'a', class_='product-card__link')['href']

                        product = {
                            'source': 'sneakerhead',
                            'id': itemId['data-element'],
                            'name': name,
                            'brand': brand,
                            'price': price,
                            'oldPrice': op,
                            'image': image,
                            'sizes': sizes,
                            'link': f'https://sneakerhead.ru{link}'
                        }
                        products.append(product)
                finalItems += products
            result = {
                'success': True,
                'text': '',
                        'items': finalItems
            }

            with open(pt.abspath('sssstest.json'), 'w') as file:
                info = json.dumps(result)
                file.write(info)
            return result
        else:
            result = {
                'success': False,
                'text': 'Ошибка получения данных с сайта',
                'items': []
            }
            return result

    def sneakerstreet(self) -> dict:
        print('sneakerstreet')
        url = 'https://sneaker-street.ru/specials?bfilter=c0%3A127&limit=240'
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'

        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            pagination = soup.find('ul', class_='pagination')
            maxPage = len(pagination) - 1
            counter = 1
            pages = []

            while counter <= maxPage:
                pages.append(counter)
                counter += 1

            finalItems = []
            for page in pages:
                url = f'https://sneaker-street.ru/specials?limit=240&bfilter=c0%3A127&page={page}'
                html = requests.get(url, headers=self.headers)
                html.encoding = 'utf-8'
                soup = BeautifulSoup(html.text, 'lxml')
                items = soup.find_all('div', class_='pli__wrapper')
                products = []
                for item in items:
                    itemId = item.find('a', class_='pli__main')['data-gtm-id']
                    brand = item.find('span', class_='pli__main__brand').text
                    model = item.find('span', class_='pli__main__name').text
                    name = brand + ' ' + model
                    price = item.find(
                        'span', class_='pli__main__price__new').text
                    oldPrice = item.find(
                        'span', class_='pli__main__price__old').text
                    image = item.find('img', class_='i-main')['src']
                    sizes = []
                    sizeTable = item.find_all(
                        'button', class_='pli__options__item')
                    for size in sizeTable:
                        sizes.append(size.text)
                    link = item.find('a', class_='pli__main')['href']

                    product = {
                        'source': 'sneakerstreet',
                        'id': itemId,
                        'name': name,
                        'brand': brand,
                        'price': price,
                        'oldPrice': oldPrice,
                        'image': image,
                        'sizes': sizes,
                        'link': link,
                    }
                    products.append(product)
                finalItems += products
            result = {
                'success': True,
                'text': '',
                'items': finalItems
            }

            with open(pt.abspath('sssstest.json'), 'w') as file:
                info = json.dumps(result)
                file.write(info)
            return result
        else:
            result = {
                'success': False,
                'text': 'Ошибка получения данных с сайта',
                'items': []
            }
            return result

    def superstep(self) -> dict:
        print('superstep')
        # TODO: добавить обработку статусов запросов
        url = 'https://superstep.ru/sale/?arrFilter_29_3839122159=Y&set_filter=Y&arrFilter_29_1536390870=Y&PAGEN_1=100'
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')
        pagination = soup.find_all('a', class_='pagination-item js-pagination')
        for item in pagination:
            pg = int(item.text)
        maxPage = pg + 1
        pagesCount = []
        counter = 1

        while counter <= maxPage:
            pagesCount.append(counter)
            counter += 1

        finalItems = []
        for page in pagesCount:
            url = f'https://superstep.ru/sale/?arrFilter_29_3839122159=Y&set_filter=Y&arrFilter_29_1536390870=Y&PAGEN_1={page}'
            html = requests.get(url, headers=self.headers)
            html.encoding = 'utf-8'
            soup = BeautifulSoup(html.text, 'lxml')
            products = soup.find_all(
                'div', class_='product-item-wrapper js-product-wrapper')

            items = []
            for prod in products:
                try:
                    itemId = prod.find('a', class_='cur_p')
                    model = prod.find('meta', itemprop='name')
                    brand = prod.find('meta', itemprop='brand')
                    name = brand['content'] + ' ' + model['content']
                    price = prod.find('span', class_='product-sale-price').text
                    oldPrice = prod.find(
                        'span', class_='product-list-price').text
                    sizes = []
                    preSizes = prod.find_all(
                        'a', class_='product-sizes-item cur_p td_n')
                    for size in preSizes:
                        sizes.append(size.text)
                    img = prod.find('img', class_='product-item-image')
                    imgIndex = img['src'].rfind('/')
                    imgName = img['src'][imgIndex + 1:]
                    image = f'https://superstep.ru/upload/resize_cache/catalog/800_800_1/{imgName}'
                    preLink = itemId['href']
                    link = f'https://superstep.ru{preLink}'
                except AttributeError:
                    continue

                product = {
                    'source': 'superstep',
                    'id': itemId['data-product-id'],
                    'name': name,
                    'price': price,
                    'oldPrice': oldPrice,
                    'brand': brand['content'],
                    'image': image,
                    'sizes': sizes,
                    'link': link}
                items.append(product)
            finalItems += items
        result = {
            'success': True,
            'text': '',
            'items': finalItems
        }

        with open(pt.abspath('sssstest.json'), 'w') as file:
            info = json.dumps(result)
            file.write(info)
        return result

    def urbanVibes(self) -> dict:
        print('urbanVibes')
        url = 'https://urbanvibes.com/api/catalog/skidki/'
        result = requests.get(url)
        if result.status_code == 200:
            data = json.loads(result.content)
            products = []

            for item in data['items']:
                itemType = str(item['genderCategoryName'])
                if 'кроссовки' in itemType.lower():
                    sizes = []
                    for size in item['sizes']:
                        if size['available'] == True:
                            sizes.append(size['size'])
                        else:
                            continue
                    product = {
                        'source': 'urbanvibes',
                        'id': item['id'],
                        'name': item['name'],
                        'price': item['price'],
                        'oldPrice': item['oldPrice'],
                        'brand': item['brand'],
                        'image': item['image'],
                        'sizes': sizes
                    }
                    products.append(product)
                else:
                    continue
            result = {
                'success': True,
                'text': '',
                'items': products
            }
            with open(pt.abspath('test.json'), 'w') as file:
                info = json.dumps(result)
                file.write(info)
            return result
        else:
            result = {
                'success': False,
                'text': 'Ошибка получения данных с сайта',
                'items': []
            }
            return result

    def start(self) -> dict:
        shops = {
            'urbanVibes': self.urbanVibes(),
            'sneakerhead': self.sneakerhead(),
            'sneakerstreet': self.sneakerstreet(),
            'superstep': self.superstep(),
        }
        result = {
            'success': True,
            'text': 'Получение данных с сайтов прошло успешно'
        }
        print(result)
        return result


k = Parser()
k.startParsing()
