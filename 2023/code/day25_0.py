"""https://adventofcode.com/2023/day/24"""
from __future__ import annotations
from heapq import heappop, heappush

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Network:

    def __init__(self, edges: set[frozenset[str, str]]) -> None:
        self.edges = frozenset(edges)
        self.nodes = frozenset(node for edge in edges for node in edge)

    def __hash__(self) -> int:
        return hash(self.edges)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Network):
            return False
        return self.edges == other.edges

    def without(self, nodes: set[str]) -> Network:
        """Return a copy of the network without the given nodes"""
        edges = self.edges.copy()
        to_remove = set()
        for node in nodes:
            for edge in edges:
                if node in edge:
                    to_remove.add(edge)
        return Network(edges - to_remove)

    def subgraph(self, nodes: set[str]) -> Network:
        """Return a subgraph of the network with only the given nodes"""
        edges = set()
        for edge in self.edges:
            if edge <= nodes:
                edges.add(edge)
        return Network(edges)

    def neighbors(self, node: str) -> set[str]:
        out = set()
        for edge in self.edges:
            if node in edge:
                out.add(edge - node)
        return out

    def subgraph_neighbors(self, nodes: set[str]) -> set[str]:
        out = set()
        for node in nodes:
            for edge in self.edges:
                if node in edge and not edge <= nodes:
                    out |= edge - {node}
        return out


def load_data(path: str) -> Network:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    edges = set()
    for line in raw:
        for pair in _parse(line):
            if pair not in edges:
                edges.add(pair)
    return Network(edges)


def _parse(line: str) -> list[set]:
    out = []
    first, friends = line.split(": ")
    for friend in friends.split(" "):
        out.append(frozenset((first, friend)))
    return out


def run(data: Network) -> int:
    # Total number of edges
    number_of_edges = len(data.edges)
    # Start with a random node (the in-subgraph)
    to_check = []
    heappush(to_check, {next(iter(data.nodes))})
    while to_check:
        ins_nodes = heappop(to_check)
        ins = data.subgraph(ins_nodes)
        outs = data.without(ins_nodes)
        # Count the number of connections to the out-subgraph
        if number_of_edges - (len(ins.edges) + len(outs.edges)) == 3:
            return len(ins.nodes)*len(outs.nodes)
        # If it's more than 3, look at all the subgraphs created by adding
        # each of the neighbors of the in-subgraph to the in-subgraph
        for new_node in data.subgraph_neighbors(ins_nodes):
            new_graph = ins_nodes | {new_node}
            if new_graph not in to_check:
                heappush(to_check, new_graph)
        # Otherwise, we've got our split
    raise ValueError("Couldn't find the split!")


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 54


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
