import numpy as np


def task() -> list:
    # находим все возможные суммы и произведения
    sums, products = set(), set()
    for i1 in range(1, 7):
        for i2 in range(1, 7):
            sums.add(i1 + i2)
            products.add(i1 * i2)
    sums, products = sorted(sums), sorted(products)

    # словари для нахождения индексов в таблице по сумме и произведению
    sum_lookup = {s: sums.index(s) for s in sums}
    product_lookup = {p: products.index(p) for p in products}

    # матрица с количествами комбинаций для заданных суммы и произведения
    counts = np.zeros((len(sums), len(products)))
    for i1 in range(1, 7):
        for i2 in range(1, 7):
            counts[sum_lookup[i1 + i2], product_lookup[i1 * i2]] += 1

    # матрица с вероятностями комбинаций для заданных суммы и произведения
    probabilities = counts / 36

    # ВЫЧИСЛЕНИЕ H(AB)
    entropy_AB = -np.sum(probabilities * np.log2(probabilities, where=np.abs(probabilities) > 0.0001))
    # print('H(AB) = {}'.format(entropy_AB))  # H(AB)

    # ВЫЧИСЛЕНИЕ H(A)
    # матрица вероятностей только для события A
    probabilities_A = np.sum(probabilities, axis=1)
    entropy_A = -np.sum(probabilities_A * np.log2(probabilities_A, where=np.abs(probabilities_A) > 0.0001))
    # print('H(A) = {}'.format(entropy_A))  # H(A)

    # ВЫЧИСЛЕНИЕ H(B)
    # матрица вероятностей только для события B
    probabilities_B = np.sum(probabilities, axis=0)
    entropy_B = -np.sum(probabilities_B * np.log2(probabilities_B, where=np.abs(probabilities_B) > 0.0001))
    # print('H(B) = {}'.format(entropy_B))  # H(B)

    # ВЫЧИСЛЕНИЕ H_A(B)
    entropy_A_B = entropy_AB - entropy_A  # H(AB) - H(A)
    # print('H_A(B) = {}'.format(entropy_A_B))  # H_A(B)

    # ВЫЧИСЛЕНИЕ I(A,B)
    information_AB = entropy_B - entropy_A_B  # H(B) - H_A(B)
    # print('I(A,B) = {}'.format(information_AB))  # I(A,B)

    return [round(el, 2) for el in [entropy_AB, entropy_A, entropy_B, entropy_A_B, information_AB]]
