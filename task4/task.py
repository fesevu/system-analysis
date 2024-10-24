import json

def parse_ranking(ranking):
    """
    Преобразует ранжировку в виде списка в бинарную матрицу
    """
    n = max([max(group) if isinstance(group, list) else group for group in ranking])  # Определяем количество элементов
    matrix = [[0] * n for _ in range(n)]
    
    for i, group in enumerate(ranking):
        if isinstance(group, list):
            for j in group:
                 for k in group:
                      matrix[j-1][k-1] = 1
            for j in group:
                for k in range(n):
                    if (matrix[k][j-1] == 0):
                         matrix[j-1][k] = 1 
        else:
            for k in range(n):
                    if (matrix[k][group-1] == 0):
                         matrix[group-1][k] = 1
    
    return matrix

def find_discrepancies(mat1, mat2):
    """
    Находит противоречия между двумя матрицами
    """
    n = len(mat1)
    discrepancies = []
    for i in range(n):
        for j in range(i):
            if mat1[i][j] * mat2[i][j] == 0 and mat1[j][i] * mat2[j][i] == 0:
                    discrepancies.append((i+1, j+1))
    return discrepancies

def main(ranking1_json, ranking2_json):
    """
    Основная функция, которая находит ядро противоречий для двух ранжировок
    """
    ranking1 = json.loads(ranking1_json)
    print(ranking1)
    ranking2 = json.loads(ranking2_json)
    
    # Преобразование ранжировок в матрицы
    matrix1 = parse_ranking(ranking1)
    print(matrix1)
    matrix2 = parse_ranking(ranking2)
    print(matrix2)
    
    # Поиск противоречий
    discrepancies = find_discrepancies(matrix1, matrix2)
    
    # Формирование результата в виде JSON
    result = json.dumps(discrepancies)
    return result

# Пример вызова функции
if __name__ == "__main__":
    with open('./task4/data/A.json', 'r') as f1, open('./task4/data/B.json', 'r') as f2:
        ranking1_json = f1.read()
        ranking2_json = f2.read()
    
    result = main(ranking1_json, ranking2_json)
    print(result)
