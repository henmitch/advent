"""https://adventofcode.com/2021/day/12"""
from typing import List, Tuple

import day12_0 as old
from day12_0 import DATA_PATH


class RevisitableGraph(old.Graph):
    def __init__(self, input_list: List[str]) -> None:
        self.nodes = self.parse(input_list)
        # Removed pruning; everything else is the same

        self.start = self["start"]
        self.start.visited = True
        self.current = self.start

        self.end = self["end"]

        self.visited_dead = False

    def viable_next_steps(self, node: old.Node | str = None):
        # If we've visited a dead node, then it reverts to a regular graph
        if self.visited_dead:
            return super().viable_next_steps(node)

        # If we haven't visited a dead node yet, everything is on the table
        if node is None:
            node = self.current
        return [n for n in node.friends if n.name != "start"]

    def go_to(self, node: old.Node | str) -> Tuple[old.Node, bool]:
        if isinstance(node, str):
            node = self[node]
        old_state = (node.visited, self.visited_dead)
        # If we haven't visited a dead node yet, everything is on the table
        if node.visited and node.small and not self.visited_dead:
            # We do this because go_to will flip this.
            node.visited = False
            self.visited_dead = True
        elif node.visited and node.small and self.visited_dead:
            raise ValueError("Someone snuck through")

        super().go_to(node)
        return old_state

    def walk(self, start: old.Node = None):
        if start is None:
            start = self.start

        if start == self.end:
            self["end"].visited = False
            return ["end"]
        out = []
        for step in self.viable_next_steps(start):
            old_state = self.go_to(step)
            walked = self.walk(step)
            if walked:
                out += [start.name, walked]
            self.current = start
            self[step.name].visited, self.visited_dead = old_state

        return out


def test():
    data = old.load_data(old.TEST_PATH)
    assert RevisitableGraph(data).count_paths() == 3509


if __name__ == "__main__":
    test()
    data = old.load_data(DATA_PATH)
    print(RevisitableGraph(data).count_paths())
