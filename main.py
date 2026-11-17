import json
import re
from time import perf_counter

EPSILON = 1e-9
REPEATS = 10
LABEL_MAP = {
    "+": "Cross",
    "cross": "Cross",
    "x": "X"
}


def read_matrix(name, size=3):
    """사용자에게 size x size 숫자 배열을 입력받는다."""
    print(f"\n{name}을 입력하세요.")

    matrix = []

    while len(matrix) < size:
        row_number = len(matrix) + 1
        user_input = input(f"{row_number}행: ").strip()

        parts = user_input.split()

        if len(parts) != size:
            print(
                f"입력 형식 오류: 각 줄에 {size}개의 숫자를 "
                "공백으로 구분해 입력하세요."
            )
            continue

        try:
            row = [float(value) for value in parts]
        except ValueError:
            print("입력 형식 오류: 숫자만 입력하세요.")
            continue

        matrix.append(row)

    return matrix


def mac(pattern, filter_matrix):
    """같은 위치의 값을 곱하고 모두 더해서 MAC 점수를 계산한다."""
    score = 0.0

    for row in range(len(pattern)):
        for column in range(len(pattern[row])):
            score += pattern[row][column] * filter_matrix[row][column]

    return score


def measure_mac_time(pattern, filter_matrix):
    """MAC 연산만 10회 실행한 평균 시간을 ms로 반환한다."""
    start = perf_counter()

    for _ in range(REPEATS):
        mac(pattern, filter_matrix)

    end = perf_counter()

    average_seconds = (end - start) / REPEATS
    return average_seconds * 1000

def make_cross_pattern(size):
    """성능 측정용 Cross 패턴을 만든다."""
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    middle = size // 2

    for i in range(size):
        matrix[middle][i] = 1
        matrix[i][middle] = 1

    return matrix


def make_x_pattern(size):
    """size x size 크기의 X 패턴을 만든다."""
    matrix = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        matrix[i][i] = 1
        matrix[i][size - 1 - i] = 1

    return matrix

def print_pattern(pattern):
    """2차원 패턴을 보기 좋게 출력한다."""
    for row in pattern:
        print(" ".join(str(value) for value in row))


def run_pattern_generator():
    """사용자가 입력한 크기의 Cross와 X 패턴을 자동 생성한다."""
    print("\n=== BONUS: 패턴 자동 생성기 ===")

    while True:
        user_input = input("패턴 크기 N을 입력하세요: ").strip()

        try:
            size = int(user_input)
        except ValueError:
            print("입력 오류: 정수를 입력하세요.")
            continue

        if size < 3:
            print("입력 오류: 3 이상의 숫자를 입력하세요.")
            continue

        break

    cross_pattern = make_cross_pattern(size)
    x_pattern = make_x_pattern(size)

    print(f"\n=== Cross {size}x{size} ===")
    print_pattern(cross_pattern)

    print(f"\n=== X {size}x{size} ===")
    print_pattern(x_pattern)


def show_performance_analysis(sizes):
    """크기별 MAC 평균 시간과 연산 횟수를 출력한다."""
    print("\n=== 성능 분석 ===")
    print(f"각 크기별 MAC 연산을 {REPEATS}회 반복한 평균")
    print()
    print(f"{'크기':<10}{'평균 시간(ms)':<20}{'연산 횟수(N²)':<15}")
    print("-" * 45)

    for size in sizes:
        pattern = make_cross_pattern(size)
        filter_matrix = make_cross_pattern(size)

        average_time = measure_mac_time(
            pattern,
            filter_matrix
        )

        operation_count = size * size

        print(
            f"{size}x{size:<7}"
            f"{average_time:<20.6f}"
            f"{operation_count:<15}"
        )

def decide_mode1(score_a, score_b):
    """두 점수를 epsilon 기준으로 비교한다."""
    if abs(score_a - score_b) < EPSILON:
        return "판정 불가"

    if score_a > score_b:
        return "A"

    return "B"

def normalize_label(label):
    """여러 형태의 라벨을 Cross 또는 X로 통일한다."""
    if not isinstance(label, str):
        raise ValueError("라벨은 문자열이어야 합니다.")

    key = label.strip().lower()

    if key not in LABEL_MAP:
        raise ValueError(f"알 수 없는 라벨입니다: {label}")

    return LABEL_MAP[key]

def validate_matrix_size(matrix, size):
    """배열이 정확히 size x size인지 검사한다."""

    if not isinstance(matrix, list):
        raise ValueError("배열 형식이 아닙니다.")

    if len(matrix) != size:
        raise ValueError(
            f"행 개수가 {size}개가 아닙니다."
        )

    for row in matrix:
        if not isinstance(row, list):
            raise ValueError(
                "행이 리스트 형식이 아닙니다."
            )

        if len(row) != size:
            raise ValueError(
                f"열 개수가 {size}개가 아닙니다."
            )

def extract_size_from_key(pattern_key):
    """size_5_1 같은 키에서 숫자 5를 추출한다."""
    match = re.fullmatch(r"size_(\d+)_(\d+)", pattern_key)

    if not match:
        raise ValueError(f"잘못된 패턴 키 형식입니다: {pattern_key}")

    return int(match.group(1))

def load_json_data():
    """프로젝트 폴더의 data.json 파일을 읽는다."""
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("오류: data.json 파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        print("오류: data.json 형식이 올바르지 않습니다.")
        return None

    return data

def run_mode2():
    print("\n=== 모드 2: data.json 분석 ===")

    data = load_json_data()

    if data is None:
        return

    print("data.json 로드 성공")

    filters = data.get("filters")
    patterns = data.get("patterns")

    if not isinstance(filters, dict):
        print("오류: filters 데이터가 없습니다.")
        return

    if not isinstance(patterns, dict):
        print("오류: patterns 데이터가 없습니다.")
        return

    total_count = 0
    pass_count = 0
    fail_count = 0
    fail_cases = []

    for pattern_key, case in patterns.items():
        total_count += 1

        print(f"\n--- {pattern_key} ---")

        try:
            size = extract_size_from_key(pattern_key)

            filter_key = f"size_{size}"

            if filter_key not in filters:
                raise ValueError(
                    f"{filter_key} 필터를 찾을 수 없습니다."
                )

            filter_group = filters[filter_key]

            normalized_filters = {}

            for raw_label, filter_matrix in filter_group.items():
                normalized_label = normalize_label(raw_label)
                normalized_filters[normalized_label] = filter_matrix

            if "Cross" not in normalized_filters or "X" not in normalized_filters:
                raise ValueError(
                    "Cross 또는 X 필터가 없습니다."
                )

            cross_filter = normalized_filters["Cross"]
            x_filter = normalized_filters["X"]

            pattern = case.get("input")
            expected = normalize_label(case.get("expected"))

            validate_matrix_size(pattern, size)
            validate_matrix_size(cross_filter, size)
            validate_matrix_size(x_filter, size)

            cross_score = mac(pattern, cross_filter)
            x_score = mac(pattern, x_filter)

            decision = decide_mode2(
                cross_score,
                x_score
            )

            print(f"Cross 점수: {cross_score}")
            print(f"X 점수: {x_score}")
            print(f"판정: {decision}")
            print(f"expected: {expected}")

            if decision == expected:
                print("결과: PASS")
                pass_count += 1
            else:
                print("결과: FAIL")
                fail_count += 1

                if decision == "UNDECIDED":
                    reason = "허용오차 내 동점"
                else:
                    reason = (
                        f"판정 {decision}과 expected "
                        f"{expected}가 다름"
                    )

                fail_cases.append(
                    (pattern_key, reason)
                )

        except ValueError as error:
            print(f"결과: FAIL - {error}")

            fail_count += 1
            fail_cases.append(
                (pattern_key, str(error))
            )

    show_performance_analysis([3, 5, 13, 25])

    print("\n=== 결과 요약 ===")
    print(f"총 테스트: {total_count}")
    print(f"통과: {pass_count}")
    print(f"실패: {fail_count}")

    if fail_cases:
        print("\n실패 케이스:")

        for case_id, reason in fail_cases:
            print(f"- {case_id}: {reason}")

def run_mode1():
    print("\n=== 모드 1: 사용자 입력 (3x3) ===")

    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")

    print("\n필터 A와 필터 B를 저장했습니다.")

    pattern = read_matrix("패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    time_a = measure_mac_time(pattern, filter_a)
    time_b = measure_mac_time(pattern, filter_b)

    result = decide_mode1(score_a, score_b)

    print("\n=== MAC 연산 결과 ===")
    print(f"필터 A 점수: {score_a}")
    print(f"필터 B 점수: {score_b}")
    print(f"필터 A 평균 연산 시간: {time_a:.6f} ms")
    print(f"필터 B 평균 연산 시간: {time_b:.6f} ms")
    print(f"판정 결과: {result}")
    show_performance_analysis([3])

def decide_mode2(cross_score, x_score):
    """모드 2에서는 동점일 때 UNDECIDED를 반환한다."""

    if abs(cross_score - x_score) < EPSILON:
        return "UNDECIDED"

    if cross_score > x_score:
        return "Cross"

    return "X"

def show_menu():
    print("\n==============================")
    print("Mini NPU Simulator")
    print("==============================")
    print("1. 사용자 입력 모드 (3x3)")
    print("2. data.json 분석 모드")
    print("3. 패턴 자동 생성기 (BONUS)")
    print("0. 종료")
    print("==============================")


def main():
    while True:
        show_menu()

        choice = input("실행할 모드를 선택하세요: ").strip()

        if choice == "1":
            run_mode1()

        elif choice == "2":
            run_mode2()

        elif choice == "3":
            run_pattern_generator()

        elif choice == "0":
            print("\n프로그램을 종료합니다.")
            break

        else:
            print("\n입력 오류: 0, 1, 2, 3 중 하나를 입력하세요.")


if __name__ == "__main__":
    main()