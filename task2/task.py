import sys
from collections import defaultdict, deque

def main(var: str) -> str:
    # Разбираем входную строку как список ребер
    edges = [tuple(map(int, line.split(','))) for line in var.strip().split('\n')]

    # Создаем структуры для хранения графа
    children = defaultdict(list)  # Для r1 и r3 (потомки)
    parents = defaultdict(list)   # Для r2 и r4 (предки)

    # Заполняем граф
    for parent, child in edges:
        children[parent].append(child)
        parents[child].append(parent)

    # Функции для поиска всех потомков и предков с произвольной глубиной
    def get_all_descendants(node):
        descendants = set()
        queue = deque([node])
        while queue:
            current = queue.popleft()
            for child in children[current]:
                if child not in descendants:
                    descendants.add(child)
                    queue.append(child)
        return descendants

    def get_all_ancestors(node):
        ancestors = set()
        queue = deque([node])
        while queue:
            current = queue.popleft()
            for parent in parents[current]:
                if parent not in ancestors:
                    ancestors.add(parent)
                    queue.append(parent)
        return ancestors

    # Находим всех узлов
    nodes = set(children.keys()).union(set(parents.keys()))

    result = []
    
    # Для каждого узла находим значения для всех отношений
    for node in sorted(nodes):
        r1 = len(children[node])  # Непосредственные потомки
        r2 = len(parents[node])   # Непосредственные предки
        r3 = len(get_all_descendants(node))  # Все потомки
        r4 = len(get_all_ancestors(node))    # Все предки

        # Для r5 находим узлы на одном уровне (с тем же родителем)
        r5 = 0
        for parent in parents[node]:
            siblings = children[parent]
            r5 += len(siblings) - 1  # Убираем текущий узел

        # Добавляем результат для текущего узла
        result.append(f'{r1},{r2},{r3},{r4},{r5}')
    
    # Возвращаем результат как CSV-строку
    return '\n'.join(result)

if __name__ == "__main__":
    # Чтение аргумента с командной строки или стандартного ввода
    if len(sys.argv) == 2:
        input_string = sys.argv[1].replace('\\n', '\n')
    else:
        input_string = sys.stdin.read().strip()
    
    # Вызов основной функции
    output = main(input_string)
    print(output)
