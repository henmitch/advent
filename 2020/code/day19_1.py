"""https://adventofcode.com/2020/day/19"""
import re
from collections.abc import Callable

import boilerplate as bp

Rules = tuple[str, ...]
Validity = Callable[[str], bool]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[Rules, tuple[str]]:
    with open(path, "r") as f:
        rules, vals = f.read().split("\n\n")
    rules = {
        int(rule.split(": ")[0]): rule.split(": ")[1].replace("\"", "")
        for rule in rules.split("\n")
    }
    rules[8] = "42 | 42 8"
    rules[11] = "42 31 | 42 11 31"
    rules = tuple(rules.get(i, "None") for i in range(max(rules) + 1))
    vals = tuple(vals.split("\n"))
    return rules, vals


class Func:
    def __init__(self, *funcs, l: int = None, name: str = None):
        self.caller = None
        self.funcs = list(funcs)
        for func in self.funcs:
            if func is not None:
                func.caller = self
        self.l = l
        self.name = name

    def __call__(self, x):
        return self.funcs[0](x)

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        return self.funcs[0].__name__

    def __repr__(self) -> str:
        return str(self)


class Anded(Func):
    def __call__(self, x: list[str] | str) -> bool:
        if not x:
            return x
        is_ = {0}
        out = []
        if isinstance(x, str):
            x = [x]
        for val in x:
            for func in self.funcs:
                next_is = set()
                if func is None:
                    func = self.caller
                # This will be a list of strings.
                for i in is_:
                    if evaluateds := func([val[i:]]):
                        next_is |= {
                            i + len(evaluated)
                            for evaluated in evaluateds
                        }
                if not next_is:
                    break
                is_ = next_is
            else:
                out += [val[:i] for i in is_]
        return out

    def __str__(self) -> str:
        return "(" + " & ".join(str(func) for func in self.funcs) + ")"

    def __repr__(self) -> str:
        return str(self)


class Ored(Func):
    def __call__(self, x: list[str] | str) -> bool:
        if not x:
            return x
        worked = []
        if isinstance(x, str):
            x = [x]
        for val in x:
            for func in self.funcs:
                if func([val]):
                    for output in func([val]):
                        worked.append(val[:len(output)])

        if not worked:
            return []

        return worked

    def __str__(self) -> str:
        return "(" + " | ".join(str(func) for func in self.funcs) + ")"

    def __repr__(self) -> str:
        return str(self)


def is_a_base(x: list[str]) -> list[str]:
    out = []
    for val in x:
        if val and val[0] == "a":
            out.append("a")
    return out


def is_b_base(x: list[str]) -> list[str]:
    out = []
    for val in x:
        if val and val[0] == "b":
            out.append("b")
    return out


is_a_base.__name__ = "A"
is_b_base.__name__ = "B"

is_a = Func(is_a_base, l=1)
is_b = Func(is_b_base, l=1)


def get_parents(rules: Rules) -> dict[int, set[int]]:
    parents = {}
    for i, rule in enumerate(rules):
        if rule == "None":
            continue
        if rule in {"a", "b"}:
            parents[rule] = i
            continue
        for child in re.findall(r"\d+", rule):
            parents.setdefault(int(child), set()).add(i)

    return parents


def get_children(rules: Rules) -> dict[int, set[int]]:
    children = {}
    for i, rule in enumerate(rules):
        if rule == "None" or rule in {"a", "b"}:
            continue
        children[i] = set(map(int, re.findall(r"\d+", rule)))

    return children


def funcify(rule: str, funcs: list[Validity]) -> Validity:
    to_ors = rule.split(" | ")
    any_mes = []
    for to_or in to_ors:
        splitted = to_or.split()
        to_ands = [funcs[to_and] for to_and in map(int, splitted)]
        if len(to_ands) == 1:
            any_mes += to_ands
            continue
        any_mes.append(Anded(*to_ands))

    if len(any_mes) > 1:
        return Ored(*any_mes)
    return any_mes[0]


def make_all_funcs(rules: Rules) -> tuple[Validity]:
    # We want a tuple of functions to determine whether a target string matches
    # the corresponding rule
    parents = get_parents(rules)
    children = get_children(rules)
    out = [None for _ in rules]
    out[parents["a"]] = is_a
    out[parents["b"]] = is_b
    remainings = {i for i, rule in enumerate(rules) if rule != "None"}
    accounted_fors = {parents["a"], parents["b"]}
    remainings -= accounted_fors

    recursives = {i for i, child in children.items() if i in child}
    to_add = set()
    for recursive in recursives:
        to_add |= parents[recursive]
    recursives |= to_add
    del to_add
    remainings -= recursives

    while remainings:
        for remaining in remainings:
            if children[remaining] <= accounted_fors:
                out[remaining] = funcify(rules[remaining], out)
                accounted_fors.add(remaining)
                remainings -= accounted_fors
                break

    # Now to deal with the recursive friends.
    while recursives:
        for recursive in recursives:
            if children[recursive] <= accounted_fors | {recursive}:
                out[recursive] = funcify(rules[recursive], out)
                accounted_fors.add(recursive)
                recursives -= accounted_fors
                break

    return tuple(out)


def count_matches(rules: Rules, vals: tuple[str]) -> int:
    funcs = make_all_funcs(rules)
    func = funcs[0]
    out = 0
    l = len(vals)
    for i, val in enumerate(vals):
        print(f"({i + 1:0{len(str(l))}}/{l}) {val}... ", end="")
        if val in func([val]):
            print("Valid")
            out += 1
        else:
            print("Invalid")
    return out


def test():
    rules, vals = load_data(TEST_PATH)
    assert count_matches(rules, vals) == 12


def main():
    rules, vals = load_data(DATA_PATH)
    print(count_matches(rules, vals))


if __name__ == "__main__":
    test()
    main()
