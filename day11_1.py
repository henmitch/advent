"""https://adventofcode.com/2021/day/11"""
import day11_0 as old

def synchronized(data: old.Grid) -> bool:
    for row in data:
        for cell in row:
            if cell != 0:
                return False
    return True

def run_until_synchronized(data: old.Grid) -> int:
    """Run until the grid is synchronized."""
    count = 0
    while not synchronized(data):
        old.step(data)
        count += 1
    return count


def test():
    data = old.load_data(old.TEST_PATH)
    assert run_until_synchronized(data) == 195

def main():
    data = old.load_data(old.DATA_PATH)
    print(run_until_synchronized(data))

if __name__ == "__main__":
    test()
    main()
