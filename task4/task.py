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
    entropy_ab = -np.sum(probabilities * np.log2(probabilities, where=np.abs(probabilities) > 0.0001))
    # print('H(AB) = {}'.format(entropy_ab))  # H(AB)

    # ВЫЧИСЛЕНИЕ H(A)
    # матрица вероятностей только для события A
    probabilities_a = np.sum(probabilities, axis=1)
    entropy_a = -np.sum(probabilities_a * np.log2(probabilities_a, where=np.abs(probabilities_a) > 0.0001))
    # print('H(A) = {}'.format(entropy_a))  # H(A)

    # ВЫЧИСЛЕНИЕ H(B)
    # матрица вероятностей только для события B
    probabilities_b = np.sum(probabilities, axis=0)
    entropy_b = -np.sum(probabilities_b * np.log2(probabilities_b, where=np.abs(probabilities_b) > 0.0001))
    # print('H(B) = {}'.format(entropy_b))  # H(B)

    # ВЫЧИСЛЕНИЕ H_A(B)
    entropy_a_b = entropy_ab - entropy_a  # H(AB) - H(A)
    # print('H_A(B) = {}'.format(entropy_a_b))  # H_A(B)

    # ВЫЧИСЛЕНИЕ I(A,B)
    information_ab = entropy_b - entropy_a_b  # H(B) - H_A(B)
    # print('I(A,B) = {}'.format(information_ab))  # I(A,B)

    return [round(el, 2) for el in [entropy_ab, entropy_a, entropy_b, entropy_a_b, information_ab]]
