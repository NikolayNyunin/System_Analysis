import csv


def task(graph: str) -> list:
    result = [[], [], [], [], []]

    reader = csv.reader(graph.split('\n'))
    edges = []
    for edge in reader:
        node1, node2 = map(int, edge)
        edges.append((node1, node2))
        result[0].append(node1)  # r1
        result[1].append(node2)  # r2

    for edge in edges:
        node1, node2 = edge
        if node2 in result[0]:
            result[2].append(node1)  # r3
        if node1 in result[1]:
            result[3].append(node2)  # r4
        if result[0].count(node1) > 1:
            result[4].append(node2)  # r5

    return [list(set(el)) for el in result]
