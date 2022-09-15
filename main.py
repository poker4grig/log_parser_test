import re
import datetime
from pprint import pprint

total_dict = {}
# Открываю файл start.log и построчно читаю. При этом, выделяю главные элементы
# строк: DocId (по нему будет происходить сопоставление с ответами.)
with open('start.log', 'r', encoding='utf-8') as start_file:
    # Создаю временный словарь
    temporary_dict = {}
    log_start = start_file.readlines()

    for log in log_start:
        # Разбиваю строку на список по пробелу
        log_list = log.split(" ")
        # С помощью рег.выражения достаю число DocId - идентификатор одного запрос-ответа
        log_doc_id = re.findall("\d+", log_list[-1])[0]
        # Перевожу время начала запроса в формат Datetime, для того, чтобы потом найти разницу во времени
        log_date_time_raw = log_list[0] + " " + log_list[1]
        log_date_time = datetime.datetime.strptime(log_date_time_raw, "%Y-%m-%d %H:%M:%S.%f")
        # Достаю поле типа запроса
        is_request = log_list[4].split("_")[1]
        # Вношу данные во временный словарь
        temporary_dict["start_date_time"] = log_date_time
        temporary_dict.update({"is_request": is_request})
        # В главном словаре создаю словарь с ключем, равным docId для возможности его поиска
        total_dict[log_doc_id] = temporary_dict
        temporary_dict = {}

# Открываю файл stop.log и построчно читаю. При этом, выделяю главные элементы
# строк: DocId (по нему будет происходить сопоставление с ответами.)
with open('stop.log', 'r', encoding='utf-8') as stop_file:
    temporary_dict = {}
    log_stop = stop_file.readlines()
    # Действия аналогичные со start.log
    for _log in log_stop:
        log_list = _log.split(" ")
        log_doc_id = re.findall("\d+", log_list[-1])[0]

        # Время ответа
        log_date_time_raw = log_list[0] + " " + log_list[1]
        log_date_time = datetime.datetime.strptime(log_date_time_raw,
                                                   "%Y-%m-%d %H:%M:%S.%f")

        is_response = log_list[4].split("_")[1]

        temporary_dict["stop_date_time"] = log_date_time
        temporary_dict.update({"is_response": is_response})
        # Нахожу в главном словаре нужный словарь по docId и расширяю его данными со stop.log
        total_dict[log_doc_id].update(temporary_dict)
        # Добавляю в этот словарь разницу по времени между запросами в одном docId
        total_dict[log_doc_id]['average_duration'] = log_date_time - total_dict[log_doc_id]["start_date_time"]
        temporary_dict = {}

# Открываю файл itog.txt на запись построчно
with open("itog.txt", "w", encoding="utf-8") as write_file:
    # В главном словаре перебираю все словари по docId, собираю в них необходимую информацию
    #и записываю в файл itog.txt
    for elem in total_dict:
        str = f'{total_dict[elem]["start_date_time"]}, {total_dict[elem]["is_request"]}, {total_dict[elem]["is_response"]}, {total_dict[elem]["average_duration"]}\n'
        write_file.writelines(str)

pprint(total_dict)
