from datetime import datetime


def parse_timestamp(line: str) -> datetime:
    timestamp_str = line.split("[")[1].split("]")[0]  # Extract timestamp string
    return datetime.strptime(timestamp_str.replace(",", ""), "%H:%M:%S.%f")


def parse_dist(line: str) -> float:
    return float(line[:-1])


def parse_data(file_path: str):
    with open(file_path) as f:
        data = f.readlines()

    parsed_data = []
    for line in data:
        if "distance from" in line:
            splitted = line.strip().split()
            distance_idx = splitted.index("distance")

            timestamp = parse_timestamp(splitted[distance_idx - 3])
            id1, id2 = splitted[distance_idx + 2], splitted[distance_idx + 4]
            dist = parse_dist(splitted[distance_idx + 6])

            # фильтруем выбросы
            if dist < 10:
                parsed_data.append((timestamp, id2, dist))

    start_timestamp = parsed_data[0][0]
    parsed_data = [
        (timestamp - start_timestamp, int(id2) % 10, dist) for timestamp, id2, dist in parsed_data
    ][5:-5]

    return parsed_data
