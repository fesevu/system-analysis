import sys
from itertools import chain

def parse_parent_child_string(input_string):
    # Разделяем входную строку по символу переноса строки
    pairs = input_string.strip().split('/n')
    
    # Инициализируем хеш-таблицу (словарь)
    parent_child_dict = {}
    
    #ищем количество узлов - самый большой номер
    maximum = -1
    # Проходим по всем парам родитель-ребёнок
    for pair in pairs:
        # Разделяем каждую пару по запятой
        parent, child = pair.split(',')
        parent = int(parent.strip())  # Приводим родителя к типу int
        child = int(child.strip())      # Приводим ребёнка к типу int
        maximum = max(maximum, parent, child) #ищем максимальное число
        
        # Добавляем ребёнка в список детей родителя
        if parent in parent_child_dict:
            parent_child_dict[parent].append(child)
        else:
            parent_child_dict[parent] = [child]
    
    return parent_child_dict, maximum

#считаем количество отношений
def count_relationships(parent_child_dict, node_counts):
    relation_table = [[0 for _ in range(5)] for _ in range(node_counts)] #создаём таблицу отношений

    # отношение r1
    for i in parent_child_dict.keys():  
          relation_table[i-1][0] += len(parent_child_dict[i])

    # отношение r2
    for i in parent_child_dict.values(): 
          for j in i: 
                    relation_table[j-1][1] += 1  

    # отношение r3
    # добавляем подчинённых всех подчинненых управляющих, которые были найденны на r1 отношении
    for i in parent_child_dict.keys(): 
          queue = parent_child_dict[i].copy()
          for j in queue:
               if relation_table[j-1][0] != 0:
                    relation_table[i-1][2] += relation_table[j-1][0]        
                    queue.extend(parent_child_dict[j]) 

    # отношение r4
    for i in parent_child_dict.values(): 
          for j in i:
               queue = [j]
               for k in queue:
                    parent = get_key_by_value(parent_child_dict, k)
                    if relation_table[parent - 1][1] != 0:          
                              relation_table[k-1][3] += relation_table[parent-1][1]        
                              queue.append(parent) 

    # отношение r5
    root = set(parent_child_dict.keys()) - set(list(chain.from_iterable(parent_child_dict.values())))  #ищем корень
    root = list(root)
    root = root[0]

    #находим на каких уровнях находтся узлы      
    graph_level = {}
    queue = [[root, 0]]
    for i in queue:
         node = i[0]
         level = i[1]
         if level not in graph_level.keys():
              graph_level[level] = [node]
         else:
              graph_level[level] = graph_level[level] + [node]      
         if node in parent_child_dict.keys():
              for j in parent_child_dict[node]:
                    queue.append([j, level+1])

    # смотрим сколько на уровне узлов
    for i in graph_level.keys():
         if len(graph_level[i]) > 1:
              for j in graph_level[i]:
                   relation_table[j-1][4] += len(graph_level[i]) - 1      

    print(graph_level)                        
    return relation_table     

# Функция для поиска ключа по значению
def get_key_by_value(d, value):
    for key, val in d.items():
        if value in val:
            return key
    return None  # Если значение не найдено 

def main(input_string:str) -> str:
    result, node_counts = parse_parent_child_string(input_string)
    print("Результат:", result)
    relation_table = count_relationships(result, node_counts)
    print(relation_table)
    # Преобразуем в строку CSV
    csv_output = '\n'.join(','.join(map(str, row)) for row in relation_table)

    # Выводим результат в консоль
    print(csv_output)

if __name__ == "__main__":
    # Проверяем, передан ли параметр
    if len(sys.argv) > 1:
        input_string = sys.argv[1]
        main(input_string)
    else:
        print("Пожалуйста, передайте строку в качестве первого параметра.")
