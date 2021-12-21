"""https://adventofcode.com/2021/day/21"""
from typing import Tuple
import boilerplate as bp
import itertools

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path):
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return list(map(int, (line.split()[-1] for line in raw)))


class Player():
    def __init__(self, position: int, board_size: int):
        self.position = 0
        self.score = 0
        self.board = itertools.cycle(range(1, board_size + 1))
        self.move(position, update_score=False)

    def __str__(self):
        return f"Player at {self.position} with {self.score}"

    def __repr__(self) -> str:
        return self.__str__()

    def move(self, distance: int, update_score: bool = True) -> int:
        for _ in range(distance):
            self.position = next(self.board)
        if update_score:
            self.score += self.position
        return self.position


def play(p1_position: int, p2_position: int, die: iter,
         board_size: int) -> Tuple[Player, Player, int]:
    p1 = Player(p1_position, board_size)
    p2 = Player(p2_position, board_size)
    players = itertools.cycle([p1, p2])
    n_rolls = 0
    for player in players:
        rolls = [next(die) for _ in range(3)]
        n_rolls += 3
        player.move(sum(rolls))
        if player.score >= 1000:
            return p1, p2, n_rolls


def play_practice_round(p1_position: int,
                        p2_position: int) -> Tuple[Player, Player, int]:
    die = itertools.cycle(range(1, 101))
    board = 10
    return play(p1_position, p2_position, die, board)


def get_score(p1: Player, p2: Player, n_rolls: int) -> int:
    return min(p1.score, p2.score)*n_rolls


def run(p1_position: int, p2_position: int) -> int:
    return get_score(*play_practice_round(p1_position, p2_position))


def test():
    data = load_data(TEST_PATH)
    assert run(*data) == 739785


if __name__ == "__main__":
    test()
    data = load_data(DATA_PATH)
    print(run(*data))
