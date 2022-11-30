"https://adventofcode.com/2019/day/8"
from day08_0 import load_data, DATA_PATH


def stack(layers: list[str]) -> str:
    out = ""
    for i in range(len(layers[0])):
        for layer in layers:
            if (digit := layer[i]) != "2":
                out += digit
                break
        else:
            out += "2"
            raise ValueError("No non-transparent pixels found")
    return out


def reshape(data: str, width: int = 25, height: int = 6) -> tuple[str, ...]:
    out = ()
    for row_num in range(height):
        out = out + (data[row_num*width:(row_num + 1)*width],)
    return out


def run(data: list[str]):
    stacked = stack(data)
    print("\n".join(reshape(stacked.replace("0", " "))))


def main():
    data = load_data(DATA_PATH)
    run(data)


if __name__ == "__main__":
    main()
