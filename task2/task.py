import sys

def parse_parent_child_string(input_string):
    # Разделяем входную строку по символу переноса строки
    pairs = input_string.strip().split('/n')
    
    # Инициализируем хеш-таблицу (словарь)
    parent_child_dict = {}
    
    # Проходим по всем парам родитель-ребёнок
    for pair in pairs:
        # Разделяем каждую пару по запятой
        parent, child = pair.split(',')
        parent = int(parent.strip())  # Приводим родителя к типу int
        child = int(child.strip())      # Приводим ребёнка к типу int
        
        # Добавляем ребёнка в список детей родителя
        if parent in parent_child_dict:
            parent_child_dict[parent].append(child)
        else:
            parent_child_dict[parent] = [child]
    
    return parent_child_dict

def main(input_string):
    result = parse_parent_child_string(input_string)
    print("Результат:", result)

if __name__ == "__main__":
    # Проверяем, передан ли параметр
    if len(sys.argv) > 1:
        input_string = sys.argv[1]
        main(input_string)
    else:
        print("Пожалуйста, передайте строку в качестве первого параметра.")
