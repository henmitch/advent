"""https://adventofcode.com/2022/day/7"""
from collections.abc import Iterator
from dataclasses import dataclass

import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


class Directory:
    def __init__(self, name: str, contents: str = None, parent=None):
        self.name = name
        self.set_contents(contents)
        self.set_parent(parent)

    def _parse(self, contents: str) -> dict:
        out = {}
        for line in contents.splitlines():
            t, n = line.split(" ")
            if t == "dir":
                out[n] = Directory(n, parent=self)
            else:
                out[n] = File(int(t), n, self)
        return out

    def set_parent(self, parent):
        self.parent = parent

    def set_contents(self, contents: str):
        if contents is None:
            self.contents = None
            return
        self.contents = self._parse(contents)
        return self

    def size(self) -> int:
        return sum(item.size() for item in self.contents.values())

    def walk(self) -> Iterator:
        for content in self.contents.values():
            if isinstance(content, File):
                yield content
            elif isinstance(content, Directory):
                yield content
                yield from content.walk()


@dataclass
class File:
    size_: str
    name: str
    parent: Directory

    def size(self):
        return self.size_


def parse_input(data: str) -> Directory:
    cwd = Directory("/")
    data = data.split("$ ")[2:]
    for group in data:
        group = group.split("\n", 1)
        command = group[0]
        if command == "ls":
            cwd = cwd.set_contents(group[1])
        elif command.startswith("cd"):
            cwd = cd(command.split()[1], cwd)
    return top(cwd)


def cd(to: str, cwd: Directory = None) -> Directory:
    if to == "..":
        cwd = cwd.parent
    elif to == "/":
        cwd = top(cwd)
    elif to in cwd.contents:
        cwd = cwd.contents[to]
    else:
        raise ValueError(f"Invalid argument for 'cd' {to}")
    return cwd


def top(cwd: Directory) -> Directory:
    while cwd.parent is not None:
        cwd = cwd.parent
    return cwd


def ls(contents: str, cwd: Directory) -> Directory:
    cwd.set_contents(contents)
    return cwd


def load_data(path: str) -> object:
    with open(path, "r") as f:
        raw = f.read()
    return parse_input(raw)


def run(data: Directory) -> int:
    out = 0
    for item in data.walk():
        if isinstance(item, Directory) and (size := item.size()) <= 100_000:
            out += size
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 95437


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
