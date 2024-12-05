import os
import re
import sys
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

_cookie = os.environ["AOC_SESSION_COOKIE"]
_email = os.environ["EMAIL"]
_url = "https://adventofcode.com/2024/day/{}/input"

data_dir = os.path.join(os.path.dirname(__file__), os.pardir, "data")
test_dir = os.path.join(os.path.dirname(__file__), os.pardir, "test")
answers_dir = os.path.join(os.path.dirname(__file__), os.pardir, "answers")


class colors:
    """ANSI color codes for terminal output."""
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def file_name(suffix: str = None, keep_part: bool = False) -> str:
    caller = os.path.split(sys.argv[0])[1]
    if suffix is not None:
        suffix = "_" + suffix
    else:
        suffix = ""
    if keep_part:
        replace = r".py"
    else:
        replace = r"_[0-9]+\.py"
    return re.sub(replace, f"{suffix}.txt", caller)


def day_num() -> str:
    return re.match(r"day([0-9]+)", file_name()).group(1).lstrip("0")


def get_data_path(suffix: str = None) -> str:
    out = os.path.join(data_dir, file_name(suffix))
    if os.path.exists(out):
        return out
    url = _url.format(day_num())
    cookies = {
        "session": _cookie,
        "User-agent": f"github.com/henmitch/advent at {_email}"
    }

    data = requests.get(url, cookies=cookies, timeout=10).text
    if data.startswith("Puzzle inputs differ by user.  "
                       "Please log in to get your puzzle input."):
        raise ValueError("Your AoC session cookie is outdated.")
    with open(out, "w") as f:
        f.write(data)
    return out


def get_test_path(suffix: str = None) -> str:
    return os.path.join(test_dir, file_name(suffix))


def write_answer(answer: Any) -> None:
    file = os.path.join(answers_dir, file_name(keep_part=True))
    with open(file, "a") as f:
        f.write(str(answer) + "\n")
