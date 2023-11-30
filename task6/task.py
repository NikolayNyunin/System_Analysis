import json

import numpy as np


class Ranking:
    """Класс, описывающий ранжировку."""

    n: int              # число носителей в ранжировке
    ranking_list: list  # описание ранжировки в виде списка
    ranking_dict: dict  # описание ранжировки в виде словаря формата {носитель1: вес1, носитель2: вес2, ...}
    sorted_keys: list   # отсортированный список носителей в ранжировке

    def __init__(self, json_string: str) -> None:
        """Конструктор - парсинг данных ранжировки из JSON-строки `json_string`."""

        self.ranking_list = json.loads(json_string)

        # перевод данных в формат словаря вида {носитель1: вес1, носитель2: вес2, ...}
        # (одинаковый вес означает эквивалентность носителей в данной ранжировке,
        # больше вес -> правее носитель в ранжировке)
        self.ranking_dict = {}
        weight = 1.0
        for el in self.ranking_list:
            if isinstance(el, list):
                cluster_weight = weight + (len(el) - 1) / 2
                for el1 in el:
                    self.ranking_dict[el1] = cluster_weight
                weight += len(el)
            else:
                self.ranking_dict[el] = weight
                weight += 1

        # получение числа носителей в ранжировке
        self.n = len(self.ranking_dict)

        # получение отсортированного списка носителей в ранжировке
        self.sorted_keys = sorted(self.ranking_dict)

    def get_matrix_col(self) -> np.ndarray:
        """Получение столбца матрицы, соответствующего данной ранжировке."""

        items = list(self.ranking_dict.items())
        items.sort(key=lambda el: el[0])

        return np.array(list(map(lambda el: el[1], items)))


def t(ranking_list: list) -> float:
    """Вычисление значения T_s."""

    result = 0
    for el in ranking_list:
        if isinstance(el, list):
            h_k = len(el)
            result += h_k ** 3 - h_k

    return result


def task(*json_strings: str) -> float:
    """Вычисление коэффициента согласованности `W`."""

    # получение числа ранжировок
    m = len(json_strings)

    if m == 0:
        raise TypeError('Недостаточно аргументов.')

    # создание объектов ранжировок
    rankings = [Ranking(json_string) for json_string in json_strings]

    # проверка эквивалентности списка носителей в ранжировках
    keys = rankings[0].sorted_keys
    for ranking in rankings[1:]:
        assert ranking.sorted_keys == keys, 'Списки носителей в ранжировках отличаются.'

    # for i, ranking in enumerate(rankings):
    #     print('Словарь R{}: {}'.format(i + 1, ranking.ranking_dict))

    # получение числа носителей
    n = rankings[0].n

    # создание матрицы для данных ранжировок
    matrix = np.empty((n, m))
    for i in range(m):
        matrix[:, i] = rankings[i].get_matrix_col().copy()

    # вычисление сумм по строкам (xi)
    x = np.sum(matrix, axis=1)

    # вычисление среднего значения для сумм по строкам xi (x_average)
    x_avg = x.mean()

    # вычисление суммы квадратов разностей xi и x_average (S)
    s = np.sum(np.square(x - x_avg))

    # вычисление дисперсии (D)
    d = s / (n - 1)

    # вычисление максимально возможной дисперсии (D_max)
    # (также работает для случая с кластерами эквивалентности)
    d_max = (m ** 2 * (n ** 3 - n) - m * sum([t(rankings[s].ranking_list) for s in range(m)])) / (12 * (n - 1))

    # вычисление коэффициента согласованности (W)
    w = d / d_max

    return round(w, 2)
