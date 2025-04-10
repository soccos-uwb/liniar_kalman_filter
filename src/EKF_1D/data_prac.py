import json
import numpy as np
import re


def log_to_json(input_path: str, output_path: str, split_line: str = "1HDIST,1,AN0,5004,1.00,1.00,1.00,") -> None:
    with open(input_path, 'r') as file:
        data = file.read()
        data = data.split(split_line)[1:-4]
        data_clean = {'measurements': [float(i.split("\n")[0]) for i in data][10:-10]}

    # Сохраняем результат в JSON
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data_clean, file, ensure_ascii=False, indent=4)


def json_to_nplist(input_path: str) -> np.ndarray:
    with open(input_path, 'r') as file:
        data = json.load(file)
        measurements = np.array(data["measurements"], dtype=float)
    return measurements


def log_to_nplist(
        input_path: str,
        json_address: str = "../data/uwb_data_json",
        split_line: str = "1HDIST,1,AN0,5004,1.00,1.00,1.00,") -> np.ndarray:
    log_to_json(input_path, json_address, split_line=split_line)
    return json_to_nplist(json_address)


def parse_logs_to_array(file_path):
    data = []
    pattern = re.compile(r'\[(\d+:\d+:\d+\.\d+),\d+] .*? distance from (\d+) to (\d+) is ([\d.]+)m')

    with open(file_path, "r") as file:
        for line in file:
            match = pattern.search(line)
            if match:
                time_str, addr_from, addr_to, distance = match.groups()
                time_parts = list(map(float, re.split('[:.]', time_str)))  # Разделяем часы, минуты, секунды
                time_sec = time_parts[0] * 3600 + time_parts[1] * 60 + time_parts[2] + time_parts[3] / 1000  # Переводим в секунды
                data.append([time_sec, int(addr_from), float(distance)])

    return np.array(data).T  # Транспонируем в 3 x n
