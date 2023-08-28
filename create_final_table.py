import csv
from collections import defaultdict

TABLE_NAME = 'final_data.csv'

def create_table(name, column_names):
    with open(name, 'w', encoding='utf-8-sig', newline='') as file:
        csv.DictWriter(file, delimiter=';', fieldnames=column_names).writeheader() # записываем заголовки в колонках


def write_table(filename, data):
    with open(filename, 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file,delimiter=';', fieldnames=list(data)).writerow(data)

def create_data(column_name, product):
    data = dict.fromkeys(column_name)
    art = product[0]
    data['art'] = art
    value_list = product[-1]
    for cn in column_name:
        for item in value_list:
            value = item.get(cn)
            if value:
                data[cn]= value
    write_table(TABLE_NAME, data)
    print('ok')



def main():

    column_name = {}
    column_name['art'] = None
    products = defaultdict(list) # создает ключи если их не было
    with open('final.csv', 'r', encoding='utf-8-sig', newline='') as file:
        for line in csv.DictReader(file, delimiter=';'):  # берем в качестве ключа первое значение в таблице(заголовок)
            art = line['art']
            name = line['name']
            value = line['value']
            column_name[name] = value
            parsing_data = {}
            parsing_data[name] = value
            products[art].append(parsing_data)


    column_names = list(column_name)
    create_table(TABLE_NAME, column_names)


    for product in products.items():
        create_data(column_name,product)





if __name__ == '__main__':
    main()