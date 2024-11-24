"""https://adventofcode.com/2023/day/24"""
from __future__ import annotations
from heapq import heappop, heappush

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Network:

    def __init__(self, edges: dict[str, frozenset[str]]) -> None:
        self.edges = edges
        self.nodes = frozenset(edges.keys())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Network):
            return False
        return self.edges == other.edges

    def without(self, nodes: set[str]) -> Network:
        """Return a copy of the network without the given nodes"""
        out = {}
        for node in self.nodes:
            if node not in nodes:
                out[node] = self.edges[node] - nodes
        return Network(out)

    def subgraph(self, nodes: set[str]) -> Network:
        """Return a subgraph of the network with only the given nodes"""
        out = {}
        for node in self.nodes:
            if node in nodes:
                out[node] = self.edges[node] & nodes
        return Network(out)

    def neighbors_of(self, node: str) -> set[str]:
        return self.edges[node]

    def subgraph_neighbors(self, nodes: set[str]) -> set[str]:
        """The neighbors of a subgraph, excluding itself"""
        out = set()
        for node in nodes:
            out |= self.neighbors_of(node)
        return out - nodes

    def edge_count(self) -> int:
        return sum(len(self.edges[node]) for node in self.edges)//2

    def most_connected_node(self) -> str:
        return max(self.nodes, key=lambda x: len(self.edges[x]))


def load_data(path: str) -> Network:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    edges = {}
    for line in raw:
        for a, b in _parse(line):
            edges[a] = edges.get(a, set()) | {b}
            edges[b] = edges.get(b, set()) | {a}
    return Network(edges)


def _parse(line: str) -> list[tuple[str, str]]:
    out = []
    first, friends = line.split(": ")
    for friend in friends.split(" "):
        out.append((first, friend))
    return out


def run(data: Network) -> int:
    # Total number of edges
    number_of_edges = data.edge_count()
    # Start with a random node (the in-subgraph)
    to_check = []
    seen = set()
    heappush(to_check, frozenset({data.most_connected_node()}))
    n = 0
    while to_check:
        n += 1
        if not n%1000:
            print(n, len(to_check), len(seen))
        ins_nodes = heappop(to_check)
        ins = data.subgraph(ins_nodes)
        outs = data.without(ins_nodes)
        # Count the number of connections to the out-subgraph
        if number_of_edges - (ins.edge_count() + outs.edge_count()) == 3:
            # If we have 3, that's our split
            print(f"{n=}")
            return len(ins.nodes)*len(outs.nodes)
        # If it's more than 3, look at all the subgraphs created by adding
        # each of the neighbors of the in-subgraph to the in-subgraph
        for new_node in data.subgraph_neighbors(ins_nodes):
            new_graph = frozenset(ins_nodes | {new_node})
            if new_graph not in seen:
                heappush(to_check, new_graph)
                seen.add(new_graph)
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
