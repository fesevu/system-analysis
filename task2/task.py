from collections import defaultdict
import csv


def process_hierarchy(input_data: str) -> str:
    """
    Обрабатывает входные данные о родительских и дочерних узлах дерева, рассчитывая различные метрики.
    :param input_data: Строка с CSV-данными, где каждая строка содержит пару "родитель, потомок".
    :return: Строка с результатами подсчета метрик в формате CSV.
    """
    child_map = defaultdict(list)  # Словарь для хранения дочерних узлов
    parent_map = defaultdict(list)  # Словарь для хранения родительских узлов

    csv_reader = csv.reader(input_data.splitlines(), delimiter=',')

    for line in csv_reader:
        if not line:
            continue
        # Извлекаем родителя и потомка
        parent, child = line
        child_map[parent].append(child)
        parent_map[child].append(parent)

        # Убедимся, что каждый узел присутствует в обеих структурах
        if parent not in parent_map:
            parent_map[parent] = []
        if child not in child_map:
            child_map[child] = []

    # Находим корневой узел (у которого нет родителей)
    root = next((node for node in parent_map if not parent_map[node]), None)

    # Определяем листовые узлы (без потомков)
    leaf_nodes = [node for node in child_map if not child_map[node]]

    # Инициализация результатов для каждого узла
    metrics = {node: {
        'descendants': set(child_map[node]),
        'ancestors': set(parent_map[node]),
        'all_descendants': set(),
        'all_ancestors': set(),
        'sibling_descendants': set()
    } for node in parent_map}

    # Прямой проход для вычисления all_ancestors и sibling_descendants
    traversal_stack = [root]
    while traversal_stack:
        current_node = traversal_stack.pop()
        for child in child_map[current_node]:
            metrics[child]['all_ancestors'].update(
                metrics[current_node]['ancestors'])
            metrics[child]['all_ancestors'].add(current_node)
            metrics[child]['sibling_descendants'].update(
                metrics[current_node]['descendants'] - {child})
            traversal_stack.append(child)

    # Обратный проход для вычисления all_descendants
    reverse_stack = leaf_nodes[:]
    while reverse_stack:
        current_node = reverse_stack.pop()
        for parent in parent_map[current_node]:
            metrics[parent]['all_descendants'].update(
                metrics[current_node]['descendants'])
            metrics[parent]['all_descendants'].add(current_node)
            if parent not in reverse_stack:
                reverse_stack.append(parent)

    # Форматирование результатов в CSV
    output_fields = ('descendants', 'ancestors', 'all_descendants',
                     'all_ancestors', 'sibling_descendants')
    csv_output = '\n'.join(
        [
            ','.join([str(len(metrics[node][field]))
                     for field in output_fields])
            for node in sorted(metrics)
        ]
    ) + '\n'

    return csv_output


def main():
    input = "1,2\n1,3\n3,4\n3,5\n"
    print(process_hierarchy(input))


if __name__ == '__main__':
    main()
