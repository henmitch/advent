"""https://adventofcode.com/2021/day/18"""
from __future__ import annotations
import unittest

import ast
import functools
import math
from typing import List, Tuple

import boilerplate as bp

DATA_PATH = bp.get_data_path()
TEST_PATH = bp.get_test_path()


class SnailfishNumber():
    """A snailfish number is a pair whose elements can be regular numbers or
    snailfish numbers.
    """
    def __init__(self, data: List, parent: SnailfishNumber = None) -> None:
        self.parent = parent

        if isinstance(data[0], list):
            self.left = SnailfishNumber(data[0], self)
        elif isinstance(data[0], SnailfishNumber):
            self.left = data[0]
            self.left.parent = self
        else:
            self.left = data[0]

        if isinstance(data[1], list):
            self.right = SnailfishNumber(data[1], self)
        elif isinstance(data[1], SnailfishNumber):
            self.right = data[1]
            self.right.parent = self
        else:
            self.right = data[1]

        self.children = [self.left, self.right]
        if isinstance(self.left, SnailfishNumber) and self.left is self.right:
            raise ValueError("Left and right are the same, somehow")

    def __str__(self) -> str:
        return "[" + str(self.left) + ", " + str(self.right) + "]"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, SnailfishNumber):
            return False
        return self.left == other.left and self.right == other.right

    def depth(self) -> int:
        if self.parent is None:
            return 0
        return self.parent.depth() + 1

    def is_left(self) -> bool:
        if self.parent is None:
            return True
        return self.parent.left is self

    def is_right(self) -> bool:
        if self.parent is None:
            return True
        return self.parent.right is self

    def is_rightmost(self) -> bool:
        if self.parent is None:
            return True
        if self.is_left():
            return False
        return self.parent.is_rightmost()

    def is_leftmost(self) -> bool:
        if self.parent is None:
            return True
        if self.is_right():
            return False
        return self.parent.is_leftmost()

    def bottom_left(self) -> SnailfishNumber:
        if isinstance(self.left, int):
            return self
        return self.left.bottom_left()

    def bottom_right(self) -> SnailfishNumber:
        if isinstance(self.right, int):
            return self
        return self.right.bottom_right()

    def first_left(self) -> Tuple[SnailfishNumber | None, int]:
        """The SnailfishNumber with the first number to the left of this one"""
        # If we're the leftmost, then we don't do anything
        if self.is_leftmost():
            return None, None
        # If we're on the left, then we need to go up to an ancestor for which
        # we're on the right, then go down to the bottom right of that ancestor
        if self.is_left():
            return self.parent.first_left()
        # If we're on the right, then we want the bottom right of our sibling
        if self.is_right():
            if isinstance(self.parent.left, int):
                return self.parent, 0
            return self.parent.left.bottom_right(), 1

    def first_right(self) -> Tuple[SnailfishNumber | None, int]:
        """We want the leftmost element of anything to the right"""
        # If we're the rightmost, then we don't do anything
        if self.is_rightmost():
            return None, None
        # If we're on the right, then we need to go up to an ancestor for which
        # we're on the left, then go down to the bottom left of that ancestor
        if self.is_right():
            return self.parent.first_right()
        # If we're on the left, then we want the bottom left of our sibling
        if self.is_left():
            if isinstance(self.parent.right, int):
                return self.parent, 1
            return self.parent.right.bottom_left(), 0

    def replace(self, idx: int, to: SnailfishNumber | int) -> None:
        if isinstance(to, SnailfishNumber):
            to.parent = self
        if idx == 0:
            self.left = to
        elif idx == 1:
            self.right = to
        else:
            raise ValueError("No index provided to replace")
        self.children = [self.left, self.right]

    def explode(self) -> None:
        left_parent, left_idx = self.first_left()
        if left_parent is not None:
            left_parent.replace(left_idx,
                                left_parent.children[left_idx] + self.left)

        right_parent, right_idx = self.first_right()
        if right_parent is not None:
            right_parent.replace(right_idx,
                                 right_parent.children[right_idx] + self.right)

        if self.is_left():
            self.parent.replace(0, 0)
        else:
            self.parent.replace(1, 0)

    def traverse(self) -> None:
        if any(child.parent is not self for child in self.children
               if isinstance(child, SnailfishNumber)):
            raise ValueError("AHA!")
        yield self
        if isinstance(self.left, SnailfishNumber):
            yield from self.left.traverse()
        if isinstance(self.right, SnailfishNumber):
            yield from self.right.traverse()

    def split(self) -> bool:
        if isinstance(self.left, int) and self.left >= 10:
            self.replace(0, _split(self.left, self))
            return True
        if isinstance(self.right, int) and self.right >= 10:
            self.replace(1, _split(self.right, self))
            return True
        return False

    def reduce(self) -> SnailfishNumber:
        # Only go until we've changed one thing, then restart
        changed = False
        for snail in self.traverse():
            if snail.depth() >= 4:
                snail.explode()
                changed = True
                break
        if not changed:
            for snail in self.traverse():
                if snail.split():
                    changed = True
                    break

        if changed:
            self.reduce()
        return self

    def magnitude(self) -> int:
        # 3 times the magnitude of the left...
        if isinstance(self.left, int):
            left = 3*self.left
        else:
            left = 3*self.left.magnitude()

        # ...plus two times the magnitude of the right
        if isinstance(self.right, int):
            right = 2*self.right
        else:
            right = 2*self.right.magnitude()

        return left + right

    def __add__(self, other: SnailfishNumber) -> SnailfishNumber:
        return SnailfishNumber([self.reduce(), other.reduce()]).reduce()


def _split(num: int, parent: SnailfishNumber | None = None) -> SnailfishNumber:
    left = int(math.floor(num/2))
    right = int(math.ceil(num/2))
    return SnailfishNumber([left, right], parent)


def load_data(path) -> List:
    with open(path, "r") as f:
        data = f.read().splitlines()
    return [SnailfishNumber(ast.literal_eval(line)) for line in data]


def process(data: List[SnailfishNumber]) -> SnailfishNumber:
    return functools.reduce(lambda x, y: x + y, data)


class TestSnailfishNumber(unittest.TestCase):
    def test_explosion_example_1(self):
        data = SnailfishNumber([[[[[9, 8], 1], 2], 3], 4])
        expect = SnailfishNumber([[[[0, 9], 2], 3], 4])
        self.assertEqual(data.reduce(), expect)

    def test_explosion_example_2(self):
        data = SnailfishNumber([7, [6, [5, [4, [3, 2]]]]])
        expect = SnailfishNumber([7, [6, [5, [7, 0]]]])
        self.assertEqual(data.reduce(), expect)

    def test_explosion_example_3(self):
        data = SnailfishNumber([[6, [5, [4, [3, 2]]]], 1])
        expect = SnailfishNumber([[6, [5, [7, 0]]], 3])
        self.assertEqual(data.reduce(), expect)

    def test_explosion_example_4(self):
        data = SnailfishNumber([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])
        expect = SnailfishNumber([[3, [2, [8, 0]]], [9, [5, [7, 0]]]])
        self.assertEqual(data.reduce(), expect)

    def test_addition_example_1(self):
        first = SnailfishNumber([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
        second = SnailfishNumber([1, 1])
        expect = SnailfishNumber([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])
        self.assertEqual(first + second, expect)

    def test_addition_example_2(self):
        to_add = [SnailfishNumber(x) for x in [[1, 1], [2, 2], [3, 3], [4, 4]]]
        added = functools.reduce(lambda x, y: x + y, to_add)
        expect = SnailfishNumber([[[[1, 1], [2, 2]], [3, 3]], [4, 4]])
        self.assertEqual(added, expect)

    def test_addition_example_3(self):
        to_add = [
            SnailfishNumber(x)
            for x in [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]
        ]
        added = functools.reduce(lambda x, y: x + y, to_add)
        expect = SnailfishNumber([[[[3, 0], [5, 3]], [4, 4]], [5, 5]])
        self.assertEqual(added, expect)

    def test_addition_example_4(self):
        to_add = [
            SnailfishNumber(x)
            for x in [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]
        ]
        added = functools.reduce(lambda x, y: x + y, to_add)
        expect = SnailfishNumber([[[[5, 0], [7, 4]], [5, 5]], [6, 6]])
        self.assertEqual(added, expect)

    def test_addition_example_5(self):
        to_add = [
            SnailfishNumber(x)
            for x in [[[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
                      [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
                      [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]],
                      [[[[2, 4], 7], [6, [0, 5]]],
                       [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]],
                      [7, [5, [[3, 8], [1, 4]]]], [[2, [2, 2]], [8, [8, 1]]],
                      [2, 9], [1, [[[9, 3], 9], [[9, 0], [0, 7]]]],
                      [[[5, [7, 4]], 7], 1], [[[[4, 2], 2], 6], [8, 7]]]
        ]
        added = functools.reduce(lambda x, y: x + y, to_add)
        expect = SnailfishNumber([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]],
                                  [[[0, 7], [6, 6]], [8, 7]]])
        self.assertEqual(added, expect)


def test():
    unittest.main()


def main():
    data = load_data(DATA_PATH)
    print(process(data).magnitude())


if __name__ == "__main__":
    main()
    test()
