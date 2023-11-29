import json
from typing import Any

import numpy as np


class Ranking:
    """Класс, описывающий ранжировку."""

    n: int                  # число носителей в ранжировке
    y: np.array             # матрица ранжировки
    ranking_dict: dict      # описание ранжировки в виде словаря формата {носитель1: вес1, носитель2: вес2, ...}
    key_from_index: dict    # словарь соответствия индексов и обозначений носителей

    def __init__(self, json_string: str) -> None:
        """Конструктор - парсинг данных ранжировки из JSON-строки `json_string`."""

        data = json.loads(json_string)

        # перевод данных в формат словаря вида {носитель1: вес1, носитель2: вес2, ...}
        # (одинаковый вес означает эквивалентность носителей в данной ранжировке,
        # больше вес -> правее носитель в ранжировке)
        self.ranking_dict = {}
        weight = 1.0
        for el in data:
            if isinstance(el, list):
                cluster_weight = weight + (len(el) - 1) / 2
                for el1 in el:
                    self.ranking_dict[el1] = cluster_weight
                weight += len(el)
            else:
                self.ranking_dict[el] = weight
                weight += 1

        # заполнение словаря соответствия индексов и обозначений носителей
        sorted_keys = sorted(self.ranking_dict)
        self.key_from_index = {sorted_keys.index(key): key for key in sorted_keys}

        # заполнение матрицы для данной ранжировки
        self.n = len(self.ranking_dict)
        self.y = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if self.ranking_dict[self.key_from_index[i]] <= self.ranking_dict[self.key_from_index[j]]:
                    self.y[i, j] = 1


def get_core_of_contradictions(ranking1: Ranking, ranking2: Ranking) -> list:
    """Получение ядра противоречий ранжировок `ranking1` и `ranking2`."""

    # вычисление матрицы Y_AB
    y12 = np.logical_and(ranking1.y, ranking2.y)

    # вычисление матрицы Y'_AB
    y12_t = np.transpose(y12)

    # вычисление матрицы, нули (False) в которой соответствуют ядру противоречий
    contradictions = np.logical_or(y12, y12_t)

    # вычисление ядра противоречий
    result = []
    for i in range(ranking1.n):
        for j in range(i + 1, ranking1.n):
            if not contradictions[i, j]:
                if len(result) == 0:
                    result.append({ranking1.key_from_index[i], ranking1.key_from_index[j]})
                else:
                    found = False
                    for el in result:
                        if ranking1.key_from_index[i] in el:
                            el.add(ranking1.key_from_index[j])
                            found = True
                            break
                        elif ranking1.key_from_index[j] in el:
                            el.add(ranking1.key_from_index[i])
                            found = True
                            break
                    if not found:
                        result.append({ranking1.key_from_index[i], ranking1.key_from_index[j]})

    return [sorted(list(cluster)) for cluster in result]


def compare_keys(key1: Any, key2: Any, dict1: dict, dict2: dict) -> int:
    """Сравнение двух носителей в двух ранжировках."""

    # key1 > key2
    if (dict1[key1] > dict1[key2] and dict2[key1] > dict2[key2]) \
            or (dict1[key1] > dict1[key2] and dict2[key1] == dict2[key2]) \
            or (dict1[key1] == dict1[key2] and dict2[key1] > dict2[key2]):
        return 1

    # key1 < key2
    elif (dict1[key1] < dict1[key2] and dict2[key1] < dict2[key2]) \
            or (dict1[key1] < dict1[key2] and dict2[key1] == dict2[key2]) \
            or (dict1[key1] == dict1[key2] and dict2[key1] < dict2[key2]):
        return -1

    # key1 == key2
    return 0


def calculate_final_ranking(ranking1: Ranking, ranking2: Ranking, core: list) -> list:
    """Вычисление согласованной ранжировки для ранжировок `ranking1` и `ranking2`."""

    dict1, dict2 = ranking1.ranking_dict, ranking2.ranking_dict

    # добавление кластеров противоречий в согласованную ранжировку
    final_ranking = [core[0]] if len(core) != 0 else []
    for cluster1 in core[1:]:
        key1 = cluster1[0]
        for i, cluster2 in enumerate(final_ranking):
            key2 = cluster2[0]

            # сравнение key1 и key2
            comparison = compare_keys(key1, key2, dict1, dict2)

            # key1 > key2
            if comparison == 1:
                if i == len(final_ranking) - 1:
                    final_ranking.append(cluster1)
                    break

            # key1 < key2
            elif comparison == -1:
                final_ranking.insert(i, cluster1)
                break

    # получение списка носителей, ещё не добавленных в ранжировку
    keys = list(ranking1.key_from_index.values())
    for cluster in final_ranking:
        for key in cluster:
            keys.remove(key)

    # добавление остальных носителей в согласованную ранжировку
    for key1 in keys:
        for i, key2 in enumerate(final_ranking):
            if isinstance(key2, list):
                key2 = key2[0]

            # сравнение key1 и key2
            comparison = compare_keys(key1, key2, dict1, dict2)

            # key1 > key2
            if comparison == 1:
                if i == len(final_ranking) - 1:
                    final_ranking.append(key1)
                    break
                else:
                    continue

            # key1 < key2
            elif comparison == -1:
                final_ranking.insert(i, key1)
                break

            # key1 == key2
            else:
                if isinstance(final_ranking[i], list):
                    final_ranking[i].append(key1)
                else:
                    final_ranking[i] = [key2, key1]
                break

    return final_ranking


def task(json_string1: str, json_string2: str) -> str:

    # print('Ранжировка 1: {}'.format(json_string1))
    # print('Ранжировка 2: {}'.format(json_string2))

    # создание экземпляров класса ранжировки
    ranking1 = Ranking(json_string1)
    ranking2 = Ranking(json_string2)

    # print('Словарь R1: {}'.format(ranking1.ranking_dict))
    # print('Словарь R2: {}'.format(ranking2.ranking_dict))

    # проверка эквивалентности списка носителей в ранжировках
    assert ranking1.key_from_index == ranking2.key_from_index, 'Списки носителей в ранжировках отличаются.'

    # вычисление кластеров противоречий
    core = get_core_of_contradictions(ranking1, ranking2)
    # print('Ядро противоречий: {}'.format(core))

    # вычисление согласованной ранжировки
    result = calculate_final_ranking(ranking1, ranking2, core)
    # print('Согласованная ранжировка: {}'.format(result))

    return json.dumps(result, separators=(',', ':'))
