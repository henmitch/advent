"""https://adventofcode.com/2021/day/14"""
from typing import Dict, Tuple

import boilerplate as bp

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


def load_data(path):
    with open(path) as f:
        raw = f.read()
    first_line, data = raw.split("\n\n")
    data = data.splitlines()
    out = dict()
    for i, line in enumerate(data):
        data[i] = line.split(" -> ")
        out[tuple(data[i][0])] = data[i][1]

    return first_line, out


def polymerize_unit(pair: Tuple[str, str], mapping: Dict[Tuple, str]) -> str:
    return mapping[pair] + pair[1]


def polymerize_chain(chain: str, mapping: Dict[Tuple, str]) -> str:
    out = chain[0]
    for pair in zip(chain, chain[1:]):
        out += polymerize_unit(pair, mapping)
    return out


def score_chain(chain: str, mapping: Dict[Tuple, str]) -> int:
    counts = {chain.count(l) for l in mapping.values()}
    return max(counts) - min(counts)


def get_score(chain: str, mapping: Dict[Tuple, str], n_iter: int = 10) -> int:
    for _ in range(n_iter):
        chain = polymerize_chain(chain, mapping)
    return score_chain(chain, mapping)


def test():
    chain, mapping = load_data(TEST_PATH)
    assert get_score(chain, mapping) == 1588


if __name__ == "__main__":
    test()
    first_line, mapping = load_data(DATA_PATH)
    print(get_score(first_line, mapping))
