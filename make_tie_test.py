import json


with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)


tie_pattern = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]


data["patterns"]["size_5_3"] = {
    "input": tie_pattern,
    "expected": "+"
}


with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)


print("동점 테스트 케이스 size_5_3 추가 완료")