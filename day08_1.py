"""https://adventofcode.com/2021/day/8"""
import logging
import itertools
import os
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)

data_dir = os.path.join(os.path.dirname(__file__), "data")
test_dir = os.path.join(os.path.dirname(__file__), "test")
DATA_PATH = os.path.join(data_dir, "day08_0.txt")
TEST_PATH = os.path.join(test_dir, "day08_0.txt")


def encode(num: str) -> int:
    out = 1
    if "a" in num:
        out *= 2
    if "b" in num:
        out *= 3
    if "c" in num:
        out *= 5
    if "d" in num:
        out *= 7
    if "e" in num:
        out *= 11
    if "f" in num:
        out *= 13
    if "g" in num:
        out *= 17

    return out


def load_data(path) -> List[Tuple[List[str], List[str]]]:
    with open(path) as f:
        data = f.read().splitlines()
    intermediate = map(lambda x: x.split(" | "), data)
    out = [(x[0].split(), x[1].split()) for x in intermediate]
    return out


def deduce(data: List[str]) -> Dict[str, int]:
    """Deduce the mapping from the data

    Two letters long => 1
    Three letters long => 7
    Four letters long => 4
    Five letters long...
        And including all letters in 1 => 3
        And missing only one letter from 9 => 5
        And missing more than one letter from 9 => 2
    Six letters long...
        And including all letters in 4 => 9
        And missing any letters from 1 => 6
        Otherwise => 0
    Seven letters long => 8
    """
    let_to_num = {}
    num_to_let = {}
    for number in itertools.cycle(data):
        if len(let_to_num) == len(set(data)):
            # We've figured out enough numbers
            break
        number = set(number)
        encoded = encode(number)
        if len(number) == 2:
            # 1 is the only two-light number
            let_to_num[encoded] = 1
            num_to_let[1] = encoded
        elif len(number) == 3:
            # 7 is the only three-light number
            let_to_num[encoded] = 7
            num_to_let[7] = encoded
        elif len(number) == 4:
            # 4 is the only four-light number
            let_to_num[encoded] = 4
            num_to_let[4] = encoded
        elif len(number) == 7:
            # 8 is the only seven-light number
            let_to_num[encoded] = 8
            num_to_let[8] = encoded

        # On to the harder stuff
        elif len(number) == 5:
            if 1 in num_to_let.keys():
                # if the 5-letter word is a superset of 1
                if number > set([num_to_let.get(1, "")]):
                    let_to_num[encoded] = 3
                    num_to_let[3] = encoded
                elif number > set([num_to_let.get(9, "")]):
                    let_to_num[encoded] = 5
                    num_to_let[5] = encoded
                else:
                    let_to_num[encoded] = 2
                    num_to_let[2] = encoded
        elif len(number) == 6:
            if 4 in num_to_let.keys():
                # if the 6-letter word is a superset of 4
                if number > set([num_to_let.get(4, "")]):
                    let_to_num[encoded] = 9
                    num_to_let[9] = encoded
                if number > set([num_to_let.get(1, "")]):
                    let_to_num[encoded] = 6
                    num_to_let[6] = encoded
                else:
                    let_to_num[encoded] = 0
                    num_to_let[0] = encoded
    return let_to_num


def translate(outs, mapping):
    default = None
    for i in range(10):
        if i not in mapping.values():
            default = i
            break
    return int("".join(str(mapping.get(encode(out), default)) for out in outs))


def row_sum(row: List[List[str]]) -> int:
    mapping = deduce(row[0])
    return translate(row[1], mapping)


def test():
    data = load_data(TEST_PATH)
    assert sum(row_sum(row) for row in data) == 61229


if __name__ == "__main__":
    test()
