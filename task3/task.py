import csv
import math

# Функция для вычисления энтропии на основе содержимого CSV
# Аргумент - строка с содержимым CSV


def calculate_entropy(csv_data: str) -> float:
    csv_reader = csv.reader(csv_data.splitlines(), delimiter=',')
    data_rows = list(csv_reader)
    num_rows = len(data_rows)
    total_entropy = 0.0

    # Обработка строк и значений в каждой ячейке
    for record in data_rows:
        for entry in record:
            numeric_value = int(entry)

            if numeric_value > 0:
                probability = numeric_value / (num_rows - 1)
                total_entropy -= probability * \
                    math.log2(probability)

    return round(total_entropy, 1)


def main():
    # Пример содержимого CSV для тестирования
    example_csv = '2,0,2,0,0\n0,1,0,0,1\n2,1,0,0,1\n0,1,0,1,1\n0,1,0,1,1\n'
    result_entropy = calculate_entropy(example_csv)
    print(result_entropy)


if __name__ == '__main__':
    main()
