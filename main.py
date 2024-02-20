import json
import os
import sys
import datetime
from json import JSONDecodeError


# python main.py help - Информация о том, как работать с приложением


def open_json() -> dict:
    if not os.path.exists('notes.json'):
        file = open("notes.json", "w+")
        file.write("{}")
        file.close()

    with open("notes.json", "r", encoding='UTF-8') as file_stream:
        try:
            python_data = json.load(file_stream)
        except JSONDecodeError:
            with open("notes.json", "w", encoding='UTF-8') as file:
                file.write("{}")
                python_data = {}

    return python_data


def dump_json(data: dict):
    with open("notes.json", "w", encoding='UTF-8') as file_stream:
        json.dump(data, file_stream, ensure_ascii=False, indent=4)
        file_stream.write('\n')


def add(title: str, body: str):
    data = open_json()
    key = str(max(map(int, data.keys())) + 1) if data != {} else '1'

    data[key] = {
        'title': title,
        'body': body,
        'time_create': str(datetime.datetime.now()),
        'time_update': str(datetime.datetime.now())
    }
    dump_json(data)


def delete(id: str):
    data = open_json()
    try:
        del data[id]
    except KeyError:
        print("\033[91mЗаписи с данным ID не существует\033[37m")
        print("Существующие id: ", *data.keys())
        return
    dump_json(data)


def print_notes_data(data, key):
    print('\033[1mID: ', key)
    print('Заголовок: ', data[key]['title'])
    print('Тело заметки: ', data[key]['body'])
    print('Время создания: ', data[key]['time_create'])
    print('Время последнего изменения: ', data[key]['time_update'], '\n\033[0m')


def read(id: str = None, date: str = None):
    data = open_json()

    if date is None:
        if id is not None:
            try:
                data = {id: open_json()[id]}
            except KeyError:
                print("\033[91mЗаписи с данным ID не существует\033[37m")
                print("Существующие id: ", *data.keys())
                return

        for key in data.keys():
            print_notes_data(data, key)
    else:
        try:
            date = datetime.datetime.strptime(date, '%d.%m.%Y').date()
        except ValueError:
            print("\033[91mВведите Дату в формате dd.mm.yyyy\033[37m")
            return
        for id_note in data.keys():
            date_note = datetime.datetime.strptime(data[id_note]['time_create'], '%Y-%m-%d %H:%M:%S.%f').date()
            if date_note == date:
                print_notes_data(data, id_note)


def update(id: str, title: str = None, body: str = None):
    data = open_json()

    if title:
        data[id]['title'] = title
        data[id]['time_update'] = str(datetime.datetime.now())
    if body:
        data[id]['body'] = body
        data[id]['time_update'] = str(datetime.datetime.now())
    else:
        print("\033[91mВведите данные которые нужно изменить\033[37m")

    dump_json(data)


def help():
    print('\033[34m\033[1mИнформация о работе приложения: \033[37m\033[0m')
    print('\033[34mДобавить заметку: python main.py add --title "Значение" --body "Значение" \033[37m')
    print('\033[34mУдалить заметку: python main.py delete --id "Значение" \033[37m')
    print('\033[34mЧитать заметку: python main.py read --id "Значение" or --date dd.mm.yyyy \033[37m')
    print('\033[34mИзменить заметку: python main.py update *--title "Значение" *--body "Значение" \033[37m')
    print('\033[34m* - Необязательно, но должен присутствовать хотя бы один аргумент\033[37m')


if __name__ == '__main__':
    args = sys.argv[1:]
    kwargs = {}

    for i in range(len(args)):
        if args[i][:2] == '--':
            kwargs[args[i][2:]] = args[i + 1]
    try:
        globals()[sys.argv[1]](**kwargs)
    except TypeError:
        print("\033[91mВведите параметры для функции\033[37m")
    except KeyError:
        print("\033[91mНеверное имя функции\033[37m")
        help()
