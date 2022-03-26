"""https://adventofcode.com/2020/day/22"""
import day22_0 as old


def play_round(decks: tuple, seens: list[list] = None) -> tuple[list, list]:
    seen = seens[0]
    match decks:
        case d1, []:
            return (d1, []), seens

        case [], d2:
            return ([], d2), seens

        case d1, d2:
            if (d1, d2) in seen:  # We have a winner of the game (d1)
                return (d1, []), seens

            seen.append((d1, d2))

            d1, d2 = d1.copy(), d2.copy()
            t1, t2 = d1.pop(0), d2.pop(0)

            if t1 > len(d1) or t2 > len(d2): # We have a winner of the hand!
                if t1 > t2:
                    d1, d2 = d1 + [t1, t2], d2
                elif t2 > t1:
                    d1, d2 = d1, d2 + [t2, t1]
                return (d1, d2), seens

            # We need a sub-game
            return (d1[:t1], d2[:t2], [t1] + d1, [t2] + d2), [[]] + seens

        # When d1 has won the sub-game...
        case d1, [], p1, p2, *parents:
            return (p1[1:] + [p1[0], p2[0]], p2[1:], *parents), seens[1:]

        # When d2 has won the sub-game...
        case [], d2, p1, p2, *parents:
            return (p1[1:], p2[1:] + [p2[0], p1[0]], *parents), seens[1:]

        case d1, d2, p1, p2, *parents:
            if (d1, d2) in seen:  # We have a winner of the sub-game (d1)
                return (p1[1:] + [p1[0], p2[0]], p2[1:], *parents), seens[1:]

            seen.append((d1, d2))

            d1, d2 = d1.copy(), d2.copy()
            t1, t2 = d1.pop(0), d2.pop(0)

            if t1 > len(d1) or t2 > len(d2):  # Someone wins the hand
                if t1 > t2:
                    d1, d2 = d1 + [t1, t2], d2
                elif t2 > t1:
                    d1, d2 = d1, d2 + [t2, t1]
                return (d1, d2, p1, p2, *parents), seens

            return (d1[:t1], d2[:t2], [t1] + d1, [t2] + d2, p1, p2, *parents), [[]] + seens


    raise ValueError("We shouldn't be here.")


def score(d1: list[int], d2: list[int]) -> tuple[int, int]:
    if not d2:
        return old.score(d1)
    elif not d1:
        return old.score(d2)


def play(d1: list[int], d2: list[int]) -> int:
    decks = (d1, d2)
    seens = [[]]
    while True:
        decks, seens = play_round(decks, seens)
        if len(decks) == 2 and (not decks[0] or not decks[1]):
            return score(*decks)


def test():
    d1, d2 = old.load_data(old.TEST_PATH)
    assert play(d1, d2) == 291


def main():
    d1, d2 = old.load_data(old.DATA_PATH)
    print(play(d1, d2))


if __name__ == "__main__":
    test()
    main()
