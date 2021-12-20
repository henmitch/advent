"""https://adventofcode.com/2021/day/20"""
from itertools import cycle
import day20_0 as old

def enhance_a_lot(img: old.Image, alg: str, n_times: int = 50) -> old.Image:
    padder = "."
    for _ in range(n_times):
        img = old.enhance(img, alg, padder)
        padder = old.enhance([[padder]], alg, padder)[0][0]
    return img

def test():
    data = old.load_data(old.TEST_PATH)
    assert old.n_illuminated(enhance_a_lot(*data)) == 3351

if __name__ == "__main__":
    test()
    data = old.load_data(old.DATA_PATH)
    assert old.n_illuminated(enhance_a_lot(*data, 2)) == 5354
    enhanced = enhance_a_lot(*data)
    old.pretty_print(enhanced)
    print(old.n_illuminated(enhanced))
