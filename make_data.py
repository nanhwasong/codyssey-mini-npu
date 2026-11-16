import json


def make_cross(size):
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    middle = size // 2

    for i in range(size):
        matrix[middle][i] = 1
        matrix[i][middle] = 1

    return matrix


def make_x(size):
    matrix = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        matrix[i][i] = 1
        matrix[i][size - 1 - i] = 1

    return matrix


data = {
    "filters": {},
    "patterns": {}
}

for size in (5, 13, 25):
    cross = make_cross(size)
    x_pattern = make_x(size)

    data["filters"][f"size_{size}"] = {
        "cross": cross,
        "x": x_pattern
    }

    data["patterns"][f"size_{size}_1"] = {
        "input": cross,
        "expected": "+"
    }

    data["patterns"][f"size_{size}_2"] = {
        "input": x_pattern,
        "expected": "x"
    }


with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)


print("data.json 생성 완료")