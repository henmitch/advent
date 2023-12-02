"""https://adventofcode.com/2023/day/2"""
import boilerplate as bp

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()

Match = list[tuple[str, int]]
Game = list[int, Match]

MAXES = {"red": 12, "blue": 14, "green": 13}


def load_data(path: str) -> list[Game]:
    with open(path, "r") as f:
        raw = f.read().splitlines()
    return [parse(line) for line in raw]


def parse(line: str) -> Game:
    game_id, game = line.split(": ")
    game_id = int(game_id.split()[1])
    matches = game.split("; ")
    out = [game_id]
    for match in matches:
        pairs = match.split(", ")
        parsed_match = []
        for pair in pairs:
            number, color = pair.split()
            parsed_match.append((color, int(number)))
        out.append(parsed_match)
    return out


def validate(game: Game) -> int:
    game_id, *matches = game
    for match in matches:
        for color, number in match:
            if number > MAXES[color]:
                return 0
    return game_id


def run(data: list[Game]) -> int:
    return sum(map(validate, data))


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 8


def main():
    data = load_data(DATA_PATH)
    print(run(data))


if __name__ == "__main__":
    test()
    main()
