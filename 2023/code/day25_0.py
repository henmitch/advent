"""https://adventofcode.com/2023/day/24"""
from __future__ import annotations
from random import choice

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Network:

    def __init__(self,
                 edges: dict[str, tuple[str, ...]],
                 sizes: dict[str, int] = None) -> None:
        self.edges = edges
        self.nodes = tuple(edges.keys())
        if sizes is None:
            sizes = {node: 1 for node in self.nodes}
        self.sizes = sizes

    def edge_count(self) -> int:
        return sum(len(self.edges[node]) for node in self.edges)//2

    def most_connected_node(self) -> str:
        return max(self.nodes, key=lambda x: len(self.edges[x]))

    def combine(self, a: str, b: str) -> Network:
        """Combine two nodes into one"""
        new_edges = {}
        new_edges[a] = self.edges[a] + self.edges[b]
        new_edges[a] = [x for x in new_edges[a] if x not in (a, b)]

        new_sizes = self.sizes.copy()
        new_sizes[a] = self.sizes[a] + self.sizes[b]
        new_sizes.pop(b)

        for node in self.nodes:
            if node not in (a, b):
                new_edges[node] = [
                    x if x not in (a, b) else a for x in self.edges[node]
                ]
        return Network(new_edges, new_sizes)

    def random_edge(self) -> str:
        # Not actually random, but close enough
        random_node = choice(self.nodes)
        other = choice(self.edges[random_node])
        return random_node, other

    def copy(self) -> Network:
        return Network(self.edges.copy())


def load_data(path: str) -> Network:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    edges = {}
    for line in raw:
        for a, b in _parse(line):
            edges[a] = edges.get(a, []) + [b]
            edges[b] = edges.get(b, []) + [a]
    return Network(edges)


def _parse(line: str) -> list[tuple[str, str]]:
    out = []
    first, friends = line.split(": ")
    for friend in friends.split(" "):
        out.append((first, friend))
    return out


def run(data: Network) -> int:
    while True:
        checking = data.copy()
        # Randomly contract the graph until two nodes remain
        while len(checking.nodes) > 2:
            a, b = checking.random_edge()
            checking = checking.combine(a, b)
        if checking.edge_count() == 3:
            break
    return checking.sizes[checking.nodes[0]]*checking.sizes[checking.nodes[1]]


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 54


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
