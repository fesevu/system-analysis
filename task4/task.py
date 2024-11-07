import pandas as pd
import numpy as np


def main():
    # Загружаем данные из CSV файла
    data = pd.read_csv(
        'D:/Lab_sem_7/system analysis/task4/data/условная-энтропия-данные.csv')
       
    # Рассчитываем совместные вероятности
    total_sum = data.iloc[:, 1:].values.sum()
    joint_prob = data.iloc[:, 1:] / total_sum

    # Рассчитываем маргинальные вероятности для A (возрастные группы)
    prob_A = joint_prob.sum(axis=1)

    # Рассчитываем маргинальные вероятности для B (категории товаров)
    prob_B = joint_prob.sum(axis=0)

    # Определяем функцию для расчета энтропии
    def entropy(probabilities):
        return -np.sum([p * np.log2(p) for p in probabilities if p > 0])

    # H(AB) - совместная энтропия двух событий
    H_AB = entropy(joint_prob.values.flatten())

    # H(A) - энтропия события A (возрастные группы)
    H_A = entropy(prob_A)

    # H(B) - энтропия события B (категории товаров)
    H_B = entropy(prob_B)

    # Ha(B) - условная энтропия события B при условии A
    conditional_entropy = 0
    for idx, p_a in enumerate(prob_A):
        if p_a > 0:
            conditional_entropy += p_a * entropy(joint_prob.iloc[idx, :] / p_a)
    Ha_B = conditional_entropy

    # I(A,B) - взаимная информация между событиями A и B
    I_AB = H_B - H_AB

    # Возвращаем результаты с точностью до двух знаков
    return [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(Ha_B, 2), round(I_AB, 2)]


# Пример использования
if __name__ == "__main__":
    result = main()
    print(result)
