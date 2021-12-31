"""https://adventofcode.com/2020/day/4"""
import re
from typing import List

import day04_0 as old


def validate_year(year: str, low: int, high: int) -> bool:
    if len(year) != 4:
        return False
    year = int(year)
    return low <= year <= high


def validate_height(hgt: str) -> bool:
    if (unit := hgt[-2:]) not in ["in", "cm"]:
        return False
    if unit == "cm":
        return 150 <= int(hgt[:-2]) <= 193
    return 59 <= int(hgt[:-2]) <= 76


def validate_color(color: str) -> bool:
    return bool(re.fullmatch(r"#[0-9a-f]{6}", color))


def validate_pid(pid: str) -> bool:
    return bool(re.fullmatch(r"[0-9]{9}", pid))


def valid(psport: dict) -> bool:
    if not old.valid(psport):
        return False

    if not validate_year(psport["byr"], 1920, 2002):
        return False

    if not validate_year(psport["iyr"], 2010, 2020):
        return False

    if not validate_year(psport["eyr"], 2020, 2030):
        return False

    if not validate_height(psport["hgt"]):
        return False

    if not validate_color(psport["hcl"]):
        return False

    if psport["ecl"] not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
        return False

    if not validate_pid(psport["pid"]):
        return False

    return True


def count_valid(psports: List[dict]):
    return sum(valid(old.parse(psport)) for psport in psports)


if __name__ == "__main__":
    data = old.load_data(old.DATA_PATH)
    print(count_valid(data))
