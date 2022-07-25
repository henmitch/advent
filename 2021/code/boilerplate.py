import os
import re
import sys

data_dir = os.path.join(os.path.dirname(__file__), os.pardir, "data")
test_dir = os.path.join(os.path.dirname(__file__), os.pardir, "test")


def file_name() -> str:
    caller = os.path.split(sys.argv[0])[1]
    return re.sub(r"_[0-9]+\.py", ".txt", caller)


def get_test_path() -> str:
    return os.path.join(test_dir, file_name())


def get_data_path() -> str:
    return os.path.join(data_dir, file_name())
