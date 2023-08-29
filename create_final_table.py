import csv
from collections import defaultdict

# Название файла CSV, в который будут записываться данные
TABLE_NAME = 'final_data.csv'

# Функция для создания таблицы с заголовками
def create_table(name, column_names):
    with open(name, 'w', encoding='utf-8-sig', newline='') as file:
        csv.DictWriter(file, delimiter=';', fieldnames=column_names).writeheader()  # Записываем заголовки в колонках

# Функция для записи данных в таблицу
def write_table(filename, data):
    with open(filename, 'a', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, delimiter=';', fieldnames=list(data))
        writer.writerow(data)

# Функция для создания данных для записи в таблицу
def create_data(column_name, product):
    data = dict.fromkeys(column_name)
    art = product[0]
    data['art'] = art
    value_list = product[-1]
    for cn in column_name:
        for item in value_list:
            value = item.get(cn)
            if value:
                data[cn] = value
    write_table(TABLE_NAME, data)
    print('ok')

def main():
    column_name = {}
    column_name['art'] = None
    products = defaultdict(list)  # Создаем словарь с пустыми списками в качестве значений
    with open('final.csv', 'r', encoding='utf-8-sig', newline='') as file:
        for line in csv.DictReader(file, delimiter=';'):
            art = line['art']
            name = line['name']
            value = line['value']
            column_name[name] = value
            parsing_data = {}
            parsing_data[name] = value
            products[art].append(parsing_data)

    column_names = list(column_name)  # Список имен колонок для таблицы
    create_table(TABLE_NAME, column_names)  # Создание таблицы с заголовками

    for product in products.items():
        create_data(column_name, product)  # Создание данных для записи в таблицу

if __name__ == '__main__':
    main()
