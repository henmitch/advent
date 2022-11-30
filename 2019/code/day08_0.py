"""https://adventofcode.com/2019/day/8"""
import boilerplate as bp

DATA_PATH = bp.get_data_path()


def load_data(path: str, width: int = 25, height: int = 6) -> list[str]:
    with open(path, "r") as f:
        data = f.read().strip()
    out = []
    while data:
        out.append(extract_data(data, width, height))
        data = data[width*height:]
    return out


def extract_data(data: str, width: int = 25, height: int = 6) -> str:
    return data[:width*height]


def verify(layers: list[str]) -> int:
    zero_count = len(layers[0]) + 1
    out = None
    for layer in layers:
        if (new_zero_count := layer.count("0")) < zero_count:
            zero_count = new_zero_count
            out = layer.count("1")*layer.count("2")
    if out is None:
        raise ValueError("Couldn't find any nonzero layers")
    return out


def main():
    data = load_data(DATA_PATH)
    print(verify(data))


if __name__ == "__main__":
    main()
