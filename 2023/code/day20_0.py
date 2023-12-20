"""https://adventofcode.com/2023/day/20"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import boilerplate as bp

TEST_PATH_0 = bp.get_test_path("0")
TEST_PATH_1 = bp.get_test_path("1")
DATA_PATH = bp.get_data_path()


@dataclass
class Module:
    name: str
    children: list[Module] = None
    parents: list[Module] = None
    pulse: bool = False

    def __post_init__(self):
        self.children = []
        self.parents = []
        self.pulse = False

    def __repr__(self) -> str:
        return (f"{self.name} ({self.pulse}) -> "
                f"{", ".join(child.name for child in self.children)}")

    def __hash__(self):
        return hash(self.name)

    def add_child(self, child: Module) -> None:
        self.children.append(child)

    def add_parent(self, parent: Module) -> None:
        self.parents.append(parent)

    def receive(self, *_) -> list[tuple[Module, bool, Module]]:
        return [(self, self.pulse, child) for child in self.children]


class Broadcaster(Module):

    pass


class FlipFlop(Module):

    def receive(self, pulse: bool,
                _: Module) -> list[tuple[Module, bool, Module]]:
        if pulse:
            return []
        self.pulse = not self.pulse
        return super().receive(pulse, _)


class Conjunction(Module):
    parents: list[Module] = None
    last_received: dict[Module, bool] = None

    def __post_init__(self):
        self.parents = []
        self.last_received = {}
        return super().__post_init__()

    def add_parent(self, parent: Module) -> None:
        self.parents.append(parent)
        self.last_received |= {parent: False}

    def receive(self, pulse: bool,
                sender: Module) -> list[tuple[Module, bool, Module]]:
        self.last_received[sender] = pulse
        self.pulse = not all(p for p in self.last_received.values())
        return super().receive()


def load_data(path: str) -> dict[str, Module]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    # Create all the modules
    modules: dict[str, Module] = {}
    for line in raw:
        name, _ = line.split(" -> ")
        if name == "broadcaster":
            modules[name] = Broadcaster("broadcaster")
        elif name[0] == "%":
            modules[name[1:]] = FlipFlop(name)
        elif name[0] == "&":
            modules[name[1:]] = Conjunction(name)
    # Assign all the parents and children
    for line in raw:
        name, children = line.split(" -> ")
        name = _parse(name)
        module = modules[name]
        children = children.split(", ")
        for child in children:
            if child not in modules:
                modules[child] = Module(child)
            module.add_child(modules[child])
            modules[child].add_parent(module)
    return modules


def _parse(name: str) -> str:
    if name == "broadcaster":
        return name
    return name[1:]


def push_button(modules: dict[str, Module]) -> list[bool]:
    sending_queue = deque([(Module("button"), False, modules["broadcaster"])])
    pulses = []
    while sending_queue:
        sending_from, pulse, sending_to = sending_queue.popleft()
        # print(f"{sending_from.name} -{pulse}-> {sending_to.name}")
        pulses.append(pulse)
        for next_ in sending_to.receive(pulse, sending_from):
            sending_queue.append(next_)
    return pulses


def run(data: dict[str, Module]) -> int:
    pulses = []
    for _ in range(1_000):
        pulses += push_button(data)
    return pulses.count(True)*pulses.count(False)


def test():
    data_0 = load_data(TEST_PATH_0)
    assert run(data_0) == 32000000
    data_1 = load_data(TEST_PATH_1)
    assert run(data_1) == 11687500


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
