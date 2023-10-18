import csv
from math import log2


def task(graph: str) -> float:
    graph = graph.split('\n')
    reader = csv.reader(graph)
    n = len(graph)
    total_entropy = 0
    for row in reader:
        entropy = sum([lij / (n - 1) * log2(lij / (n - 1)) if lij != 0 else 0 for lij in map(int, row)])
        total_entropy -= entropy

    return round(total_entropy, 1)
