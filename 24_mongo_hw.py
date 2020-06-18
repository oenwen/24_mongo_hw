import csv
import re
from pprint import pprint
from pymongo import MongoClient

client = MongoClient()
concerts_db = client['concerts_db']

def read_data(scv_file, db):
    concerts_collection = db['concerts_collection']
    '''импорт данных из csv файла'''
    with open(scv_file, encoding='utf8') as artists_csv:
        reader = csv.DictReader(artists_csv)
        artists_list = [] # получаем список словарей \
        # [{'Исполнитель': 'T-Fest', 'Цена': '1200', 'Место': 'Adrenaline Stadium', 'Дата': '22.11'},{}........
        for line in reader:
            price = line.get('Цена')
            line['Цена'] = int(price)
            artists_list.append(line)

        concerts_collection.insert_many(artists_list)

    return db


def find_cheapest(db):
    '''сортировка билетов из базы по возрастанию цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/

    https://stackoverflow.com/questions/10242149/using-sort-with-pymongo
    '''

    concerts_collection = db['concerts_collection']
    sorted_by_price = list(concerts_collection.find().sort([('Цена', 1)]))
    pprint(sorted_by_price)

    return sorted_by_price


def find_by_name(db):
    '''
    поиск билетов по исполнителю (имя исполнителя может быть задано не полностью),
     возврат по возрастанию цены
    '''

    name = input('Введите строку поиска исполнителя ')
    pattern = re.compile((f'\w?{name}\w?'), re.I)
    search = db['concerts_collection'].find({'Исполнитель': pattern}).sort([('Цена', 1)])
    pprint(list(search))

    return search

if __name__ == '__main__':
    read_data('artists.csv', concerts_db)
    find_cheapest(concerts_db)
    find_by_name(concerts_db)

