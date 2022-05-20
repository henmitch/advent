import os
import platform
import re
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

_cookie = os.environ["AOC_SESSION_COOKIE"]
_url = "https://adventofcode.com/2019/day/{}/input"

data_dir = os.path.join(os.path.dirname(__file__), os.pardir, "data")
test_dir = os.path.join(os.path.dirname(__file__), os.pardir, "test")


def file_name() -> str:
    caller = os.path.split(sys.argv[0])[1]
    return re.sub(r"_[0-9]+\.py", ".txt", caller)


def day_num() -> str:
    return re.match(r"day([0-9]+)", file_name()).group(1).lstrip("0")


def get_data_path() -> str:
    out = os.path.join(data_dir, file_name())
    if os.path.exists(out):
        return out
    url = _url.format(day_num())
    data = requests.get(url, cookies={"session": _cookie}).text
    if data.startswith("Puzzle inputs differ by user.  "
                       "Please log in to get your puzzle input."):
        raise ValueError("Your AoC session cookie is outdated.")
    with open(out, "w") as f:
        f.write(data)
    return out


def get_test_path() -> str:
    return os.path.join(test_dir, file_name())
