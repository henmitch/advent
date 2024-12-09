"""https://adventofcode.com/2024/day/9"""
import boilerplate as bp
from day09_0 import DATA_PATH, TEST_PATH, Span, width


def load_data(path: str) -> tuple[list[Span], list[Span]]:
    with open(path, "r") as f:
        raw = f.read().strip()
    files = [int(x) for x in raw[::2]]
    # Have to add 0 for fenceposting
    blocks = [int(x) for x in raw[1::2]] + [0]

    file_spans = []
    block_spans = []
    pos = 0
    for file, block in zip(files, blocks):
        file_spans.append((pos, pos + file))
        pos += file
        block_spans.append((pos, pos + block))
        pos += block

    block_spans = [x for x in block_spans if width(x) > 0]

    return file_spans, block_spans


def checksum(files: list[Span]) -> int:
    out = 0
    for i, file in enumerate(files):
        out += sum(i*v for v in range(*file))
    return out


def run(data: tuple[list[Span], list[Span]]) -> int:
    file_spans, block_spans = data
    out_files = file_spans.copy()
    for _i, file in enumerate(file_spans[::-1]):
        i = len(file_spans) - _i - 1  # Reverse order
        # Check for first block where file fits
        # I *could* make this more efficient by storing block_spans by length
        # but, I won't.
        options = [
            span for span in block_spans
            if width(span) >= width(file) and span[0] <= file[0]
        ]
        if not options:
            # No block big enough
            continue
        first_block = min(options)
        idx = block_spans.index(first_block)
        # Put file in block
        out_files[i] = (first_block[0], first_block[0] + width(file))
        # Shrink block to remainder
        block_spans[idx] = (first_block[0] + width(file), first_block[1])
    return checksum(out_files)


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 2858


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
