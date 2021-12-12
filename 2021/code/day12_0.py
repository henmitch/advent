"""https://adventofcode.com/2021/day/12"""
from __future__ import annotations

import logging
import os
import sys
from typing import Dict, List

import boilerplate as bp

DATA_PATH = os.path.join(bp.data_dir, "day12.txt")
TEST_PATH = os.path.join(bp.test_dir, "day12.txt")


def load_data(path) -> List[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def pretty_print(lst, indent=0):
    for element in lst:
        if isinstance(element, list):
            pretty_print(element, indent + 1)
        else:
            print(indent*" " + element)


def flatten(lst):
    for element in lst:
        if isinstance(element, list):
            for subelement in flatten(element):
                yield subelement
        else:
            yield element


class Node:
    def __init__(self, name: str):
        self.name = name
        self.visited = False
        self.friends: List[Node] = list()
        self.big = name.isupper()
        self.small = not self.big

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"{self.name} - "\
            f"{','.join(friend.name for friend in self.friends)}"

    def __eq__(self, other: Node) -> bool:
        return self.name == other.name

    def copy(self) -> Node:
        n = Node(self.name)
        for friend in self.friends:
            n.add_friend(friend)
        return n

    def add_friend(self, friend: Node) -> None:
        # logger.info("Adding friend %s to %s", friend.name, self.name)
        self.friends.append(friend)

    def kill_friend(self, friend: Node | str) -> None:
        if friend in self.friends:
            self.friends.pop(self.friends.index(friend))

    def is_dead(self) -> bool:
        return (self.small and len(self.friends) == 1
                and all(friend.small for friend in self.friends))

    def combine(self, other: Node) -> None:
        if self.name != other.name:
            raise ValueError("Can't combine two nodes with different names.")
        for friend in other.friends:
            self.add_friend(friend)

    def viable(self) -> bool:
        return self.big or not self.visited


class Graph:
    def __init__(self, input_list: List[str]) -> None:
        self.nodes = self.parse(input_list)
        self.prune()

        self.start = self["start"]
        self.start.visited = True
        self.current = self.start

        self.end = self["end"]

    def __getitem__(self, key: str) -> Node:
        return self.nodes[key]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Graph: {'; '.join(str(node) for node in self.nodes.values())}"

    @staticmethod
    def parse(input_list: List[str]) -> Dict[str, Node]:
        out: Dict[str, Node] = dict()
        for row in input_list:
            left, right = row.split("-")
            l = out.get(left, Node(left))
            r = out.get(right, Node(right))

            l.add_friend(r)
            r.add_friend(l)

            out[left] = l
            out[right] = r

        return out

    def prune(self):
        to_prune: List[Node] = []
        for node in self.nodes.values():
            if node.is_dead():
                to_prune.append(node)

        for dead in to_prune:
            for node in self.nodes.values():
                node.kill_friend(dead)
            del self.nodes[dead.name]

    def go_to(self, node: Node | str):
        if isinstance(node, str):
            node = self[node]
        if node in self.current.friends:
            # Not allowed if small and already visited
            if node.small and node.visited:
                raise ValueError("Can't revisit a small node")
            node.visited = True
            self.current = node
            return node
        raise ValueError(f"Can't visit node {node} from {self.current}.")

    def viable_next_steps(self, node: Node = None) -> List[Node]:
        if node is None:
            node = self.current
        return [friend for friend in node.friends if friend.viable()]

    def reset(self, *nodes, position: bool = False):
        if position:
            self.current = self.start
        if nodes:
            for node in nodes:
                node.visited = False
            return None

        for _, node in self.nodes.items():
            node.visited = False
        return None

    def walk(self, start: Node = None):
        if start is None:
            start = self.start

        if start == self.end:
            return ["end"]
        out = []
        for step in self.viable_next_steps(start):
            self.go_to(step)
            walked = self.walk(step)
            if walked:
                out += [start.name, walked]
            self.reset(step)
            self.current = start
        return out

    def count_paths(self):
        walked = self.walk()
        return list(flatten(walked)).count("end")


def test():
    data = load_data(TEST_PATH)
    assert Graph(data).count_paths() == 226


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(Graph(data).count_paths())
