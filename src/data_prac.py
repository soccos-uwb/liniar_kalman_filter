import json
import numpy as np


def log_to_json(input_path, output_path, split_line="1HDIST,1,AN0,5004,1.00,1.00,1.00,"):
    with open(input_path, 'r') as file:
        data = file.read()

        # Разделяем данные по указанной строке и исключаем последние элементы
        data = data.split(split_line)[1:-4]

        # Очищаем данные
        data_clean = {'measurements': [float(i.split("\n")[0]) for i in data][10:-10]}

    # Сохраняем результат в JSON
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data_clean, file, ensure_ascii=False, indent=4)


def json_to_nplist(input_path):
    with open(input_path, 'r') as file:
        data = json.load(file)
        measurements = data["measurements"]
    return measurements


def log_to_nplist(input_path, json_address="../data/uwb_data_json", split_line="1HDIST,1,AN0,5004,1.00,1.00,1.00,"):
    log_to_json(input_path, json_address, split_line=split_line)
    return json_to_nplist(json_address)
