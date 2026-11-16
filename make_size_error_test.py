import json


with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)


wrong_pattern = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]


data["patterns"]["size_5_3"] = {
    "input": wrong_pattern,
    "expected": "x"
}


with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)


print("크기 오류 테스트 케이스 size_5_3 추가 완료")