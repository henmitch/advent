"""https://adventofcode.com/2021/day/14"""
import logging
from typing import Dict, Tuple
import boilerplate as bp

import os

DATA_PATH = os.path.join(bp.data_dir, "day14.txt")
TEST_PATH = os.path.join(bp.test_dir, "day14.txt")

logging.basicConfig(level=logging.WARN)


def load_data(path) -> Tuple[Dict[Tuple, int], Dict[Tuple, str]]:
    logging.info("Loading data from %s", path)
    with open(path) as f:
        raw = f.read()
    raw_chain, data = raw.split("\n\n")
    last_letter = raw_chain[-1]
    chain = dict()
    for pair in zip(raw_chain, raw_chain[1:]):
        chain[pair] = chain.get(pair, 0) + 1

    data = data.splitlines()
    out = dict()
    for i, line in enumerate(data):
        data[i] = line.split(" -> ")
        out[tuple(data[i][0])] = data[i][1]

    return chain, out, last_letter


def polymerize_unit(pair: Tuple[str, str],
                    mapping: Dict[Tuple, str]) -> Dict[Tuple, str]:
    logging.info("Polumerizing unit")
    # Just in case we get a situation like this.
    if pair[0] == mapping[pair] and mapping[pair] == pair[1]:
        return {pair: 2}
    return {(pair[0], mapping[pair]): 1, (mapping[pair], pair[1]): 1}


def polymerize_chain(chain: Dict[Tuple, str],
                     mapping: Dict[Tuple, str]) -> Dict[Tuple, str]:
    logging.info("Polumerizing chain")
    out = dict()
    for pair, count in chain.items():
        polymer = polymerize_unit(pair, mapping)
        for key, value in polymer.items():
            out[key] = out.get(key, 0) + value*count
    return out


def score_chain(chain: Dict[Tuple, str], last_letter: str) -> int:
    logging.info("Scoring chain")
    letters = set()
    for key in chain:
        letters.update(key)
    scores = {letter: 0 for letter in letters}
    scores[last_letter] = 1
    for letter in letters:
        for key in chain:
            if letter == key[0]:
                scores[letter] = scores[letter] + chain[key]

    return max(scores.values()) - min(scores.values())


def get_score(chain: Dict[Tuple, str],
              mapping: Dict[Tuple, int],
              last_letter: str,
              n_iter: int = 40) -> int:
    for _ in range(n_iter):
        chain = polymerize_chain(chain, mapping)
    return score_chain(chain, last_letter)


def test():
    chain, mapping, last_letter = load_data(TEST_PATH)
    assert get_score(chain, mapping, last_letter, 10) == 1588
    assert get_score(chain, mapping, last_letter) == 2188189693529
    real_chain, real_mapping, real_last_letter = load_data(DATA_PATH)
    assert get_score(real_chain, real_mapping, real_last_letter, 10) == 2915

if __name__ == "__main__":
    test()
    chain, mapping, last_letter = load_data(DATA_PATH)
    print(get_score(chain, mapping, last_letter))
