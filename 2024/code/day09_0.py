"""https://adventofcode.com/2024/day/9"""
import boilerplate as bp

Span = tuple[int, int]
Files = dict[Span, int]

TEST_PATH = bp.get_test_path()
DATA_PATH = bp.get_data_path()


def load_data(path: str) -> tuple[Files, list[Span]]:
    with open(path, "r") as f:
        raw = f.read().strip()
    files = [int(x) for x in raw[::2]]
    # Have to add 0 for fenceposting
    blocks = [int(x) for x in raw[1::2]] + [0]

    file_spans = {}
    block_spans = []
    pos = 0
    for i, (file, block) in enumerate(zip(files, blocks)):
        file_spans[(pos, pos + file)] = i
        pos += file
        block_spans.append((pos, pos + block))
        pos += block

    block_spans = [x for x in block_spans if width(x) > 0]

    return file_spans, block_spans


def width(span: Span) -> int:
    # Convenience function for length of span
    return span[1] - span[0]


def update(files: Files, blocks: list[Span]) -> tuple[Files, list[Span]]:
    first_block = min(blocks)
    last_file = max(files)
    if first_block[0] > last_file[1]:
        # No overlap
        return files, []
    file_num = files[last_file]

    if width(first_block) < width(last_file):
        # Last file can't all fit in the first block
        # Fill the first block with the last file
        files[first_block] = file_num

        # Create a new file for what's left
        remainder = (last_file[0], last_file[1] - width(first_block))
        files[remainder] = file_num

    elif width(first_block) > width(last_file):
        # Last file doesn't fill the first block
        # Put all of the last file in the first block
        new_file = (first_block[0], first_block[0] + width(last_file))
        files[new_file] = file_num

        new_block = (first_block[0] + width(last_file), first_block[1])
        blocks.append(new_block)

    else:
        files[first_block] = file_num

    del files[last_file]
    blocks.remove(first_block)

    return files, blocks


def checksum(files: Files) -> int:
    out = 0
    for file in files:
        out += sum(files[file]*v for v in range(*file))
    return out


def run(data: tuple[Files, list[int]]) -> int:
    files, blocks = data
    while blocks:
        files, blocks = update(files, blocks)
    out = checksum(files)
    return out


def test():
    data = load_data(TEST_PATH)
    assert run(data) == 1928


def main():
    data = load_data(DATA_PATH)
    out = run(data)
    bp.write_answer(out)
    print(out)


if __name__ == "__main__":
    test()
    main()
