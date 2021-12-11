"""https://adventofcode.com/2021/day/8"""
import itertools
import logging
import os
from typing import List, Tuple

import boilerplate as bp

logging.basicConfig(level=logging.INFO)

DATA_PATH = os.path.join(bp.data_dir, "day08.txt")
TEST_PATH = os.path.join(bp.test_dir, "day08.txt")


def load_data(path) -> List[Tuple[List[str], List[str]]]:
    with open(path) as f:
        data = f.read().splitlines()
    intermediate = map(lambda x: x.split(" | "), data)
    out = [(x[0].split(), x[1].split()) for x in intermediate]
    return out


def deduce(data: List[str]) -> tuple:
    """Deduce the letter-to-light mapping

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
    # The easy pickins are the left side and the bottom right
    all_letters = list(itertools.chain(*data))
    top_left = [let for let in all_letters if all_letters.count(let) == 6][0]
    bot_left = [let for let in all_letters if all_letters.count(let) == 4][0]
    bot_rght = [let for let in all_letters if all_letters.count(let) == 9][0]
    # The other letters will all show up 7 or 8 times
    seven_times = [let for let in all_letters if all_letters.count(let) == 7]
    eight_times = [let for let in all_letters if all_letters.count(let) == 8]

    one = set([num for num in data if len(num) == 2][0])
    four = set([num for num in data if len(num) == 4][0])
    seven = set([num for num in data if len(num) == 3][0])
    # 8 doesn't give us any information

    top = seven - one
    top_rght = (set(eight_times) - top).pop()
    top = top.pop()

    bot = set(seven_times) - four
    mid = (set(seven_times) - bot).pop()
    bot = bot.pop()

    return top, mid, bot, top_rght, bot_rght, top_left, bot_left


def decode_num(num: str, *lights) -> str:
    num = set(num)
    if num == set(lights) - {lights[1]}:
        return "0"
    if len(num) == 2:
        return "1"
    if num == {lights[i] for i in [0, 1, 2, 3, 6]}:
        return "2"
    if num == {lights[i] for i in range(5)}:
        return "3"
    if len(num) == 4:
        return "4"
    if num == {lights[i] for i in [0, 1, 2, 4, 5]}:
        return "5"
    if num == {lights[i] for i in [0, 1, 2, 4, 5, 6]}:
        return "6"
    if len(num) == 3:
        return "7"
    if len(num) == 7:
        return "8"
    if num == {lights[i] for i in range(6)}:
        return "9"


def decode_row(ins: List[str], outs: List[str]) -> int:
    lights = deduce(ins)
    return int("".join(decode_num(num, *lights) for num in outs))


def total(data: List[List[str]]) -> int:
    return sum(decode_row(*row) for row in data)


def test():
    data = load_data(TEST_PATH)
    assert total(data) == 61229


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(total(data))
