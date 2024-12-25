import json


def calculate_membership(value, fuzzy_sets):
    """Вычисление степени принадлежности значения нечетким множествам."""
    membership_degrees = {}
    for label, boundaries in fuzzy_sets.items():
        membership_value = 0
        for i in range(len(boundaries) - 1):
            x_start, y_start = boundaries[i]
            x_end, y_end = boundaries[i + 1]
            if x_start <= value <= x_end:  # Линейная интерполяция
                if x_start == x_end:  # На случай вертикального отрезка
                    membership_value = max(y_start, y_end)
                else:
                    membership_value = y_start + \
                        (y_end - y_start) * (value - x_start) / (x_end - x_start)
                break
        membership_degrees[label] = membership_value
    return membership_degrees


def compute_crisp_value(fuzzy_result, output_sets):
    """Перевод нечеткого результата в четкое значение."""
    weighted_sum = 0
    weight_total = 0
    for term, membership_degree in fuzzy_result.items():
        if membership_degree > 0:
            points = output_sets[term]
            # Среднее арифметическое x-координат
            centroid = sum(coord[0] for coord in points) / len(points)
            weighted_sum += membership_degree * centroid
            weight_total += membership_degree
    return weighted_sum / weight_total if weight_total != 0 else 0


def fuzzy_control_system(input_data, output_data, rule_map, input_value):
    """Основной алгоритм нечеткого управления."""
    # Преобразование данных
    fuzzy_input_sets = json.loads(input_data)
    fuzzy_output_sets = json.loads(output_data)
    rule_mapping = json.loads(rule_map)

    # Фаззификация
    fuzzy_input = calculate_membership(input_value, fuzzy_input_sets)
    print("Фаззификация входного значения:", fuzzy_input)

    # Применение правил
    resulting_fuzzy_output = {}
    for input_label, degree in fuzzy_input.items():
        if input_label in rule_mapping:
            mapped_output = rule_mapping[input_label]
            resulting_fuzzy_output[mapped_output] = max(
                resulting_fuzzy_output.get(mapped_output, 0), degree)
    print("Применение правил перехода:", resulting_fuzzy_output)

    # Дефаззификация
    crisp_result = compute_crisp_value(
        resulting_fuzzy_output, fuzzy_output_sets)
    print("Результирующее четкое значение:", crisp_result)

    return crisp_result


def main():
    """Точка входа в программу."""
    # Пример данных для тестирования
    input_data_json = """{
        "холодно": [
            [0, 1],
            [16, 1],
            [20, 0],
            [50, 0]
        ],
        "комфортно": [
            [16, 0],
            [20, 1],
            [22, 1],
            [26, 0]
        ],
        "жарко": [
            [0, 0],
            [22, 0],
            [26, 1],
            [50, 1]
        ]
    }"""

    output_data_json = """{
        "низко": [
            [0, 1],
            [6, 1],
            [10, 0],
            [20, 0]
        ],
        "средне": [
            [6, 0],
            [10, 1],
            [12, 1],
            [16, 0]
        ],
        "высоко": [
            [0, 0],
            [12, 0],
            [16, 1],
            [20, 1]
        ]
    }"""

    rule_mapping_json = """{
        "холодно": "высоко",
        "комфортно": "средне",
        "жарко": "низко"
    }"""

    input_value = 19.3
    result = fuzzy_control_system(
        input_data_json, output_data_json, rule_mapping_json, input_value)
    print("Итоговый результат работы системы:", result)


if __name__ == "__main__":
    main()
