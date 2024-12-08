"""Make a script from the templates based on the given day and year"""
import argparse
import datetime as dt
import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SUBDIRECTORIES = ["answers", "code", "data", "test"]
IGNORE = ["answers", "data"]
PARENT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(PARENT_DIR, "templates")
GITIGNORE_PATH = os.path.join(TEMPLATE_DIR, "gitignore.template")
PART_0_PATH = os.path.join(TEMPLATE_DIR, "part_0.template")
PART_1_PATH = os.path.join(TEMPLATE_DIR, "part_1.template")
with open(GITIGNORE_PATH) as _f:
    GITIGNORE = _f.read()
with open(PART_0_PATH) as _f:
    PART_0_TEMPLATE = _f.read()
with open(PART_1_PATH) as _f:
    PART_1_TEMPLATE = _f.read()

logging.debug("Parent directory: %s", PARENT_DIR)
logging.debug("Template directory: %s", TEMPLATE_DIR)
logging.debug("Gitignore path: %s", GITIGNORE_PATH)
logging.debug("Part 0 path: %s", PART_0_PATH)
logging.debug("Part 1 path: %s", PART_1_PATH)


def make_script(day: int,
                year: int,
                part: int,
                interactive: bool = False) -> None:
    """Make a script from the templates based on the given day and year"""
    logging.info("Making script for day %s, year %s, part %s", day, year, part)
    template_path = os.path.join(TEMPLATE_DIR, f"part_{part}.template")
    out_path = os.path.join(PARENT_DIR, str(year), "code",
                            f"day{day:02}_{part}.py")

    if os.path.exists(out_path):
        if interactive:
            logging.warning("File %s already exists. Overwrite? y/N", out_path)
            response = input()
            if response.lower() != "y":
                logging.info("Skipping %s", out_path)
                return
        else:
            logging.warning("File %s already exists. Skipping", out_path)
            return

    with open(template_path) as f:
        template = f.read()
    template = template.replace("$year", str(year))
    template = template.replace("$day", str(day))
    template = template.replace("$paddedday", str(day).zfill(2))
    with open(out_path, "w") as f:
        f.write(template)


def make_year(year: int) -> None:
    """Make the year directory and subdirectories"""
    year_dir = os.path.join(PARENT_DIR, str(year))
    if os.path.exists(year_dir):
        logging.info("Directory %s already exists", year_dir)
        return

    os.mkdir(year_dir)
    for sub in SUBDIRECTORIES:
        new_path = os.path.join(year_dir, sub)
        logging.info("Creating directory %s", new_path)
        os.mkdir(new_path)
        if sub in IGNORE:
            logging.info("Creating .gitignore in %s", new_path)
            with open(os.path.join(new_path, ".gitignore"), "w") as f:
                f.write(GITIGNORE)
    boilerplate_path = os.path.join(TEMPLATE_DIR, "boilerplate.template")
    with open(boilerplate_path) as f:
        boilerplate = f.read()
    logging.info("Creating boilerplate at %s", boilerplate_path)
    with open(os.path.join(year_dir, "code", "boilerplate.py"), "w") as f:
        f.write(boilerplate.replace("$year", str(year)))


def main():
    parser = argparse.ArgumentParser(description="Make a script from the "\
            "templates based on the given day and year")
    parser.add_argument("--day",
                        "-d",
                        type=int,
                        help="The day of the month",
                        choices=range(1, 32),
                        default=dt.datetime.now().day)
    parser.add_argument("--year",
                        "-y",
                        type=int,
                        help="The year",
                        default=dt.datetime.now().year)
    parser.add_argument("--part",
                        "-p",
                        type=str,
                        help="The part of the day",
                        choices=["0", "1", "both"],
                        default="both")
    args = parser.parse_args()
    day = args.day
    year = args.year
    part = [0] if args.part == "0" else [1] if args.part == "1" else [0, 1]

    make_year(year)

    for p in part:
        make_script(day, year, p, interactive=True)


if __name__ == "__main__":
    main()
