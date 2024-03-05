#!/usr/bin/env python

"""
Categorize files by specified date in a folder.

./categorizer.py [folder_path] [date_string] [-s]
"""

import argparse
import datetime
import os


def get_file_list(pwd: str):
    """
    Get a list of files in a folder. All system files and hidden files are excluded.
    :param pwd: Current working directory.
    :return: List of files in a folder, excluding folders.
    """

    # If no such folder, return an empty list.
    if not os.path.exists(pwd):
        print(f"No such folder: {pwd}")
        exit(1)

    # If it is a file, return a list with that file.
    if os.path.isfile(pwd):
        print(f"{pwd} is a file.")
        exit(1)

    return [f for f in os.listdir(pwd)
            if os.path.isfile(os.path.join(pwd, f)) and  # No folders.
            f not in ["desktop.ini", "thumbs.db", ".DS_Store"] and  # No system files.
            not f.startswith(".")  # No hidden files.
            ]


def get_file_time_str(pwd: str, file_name: str, date_format: str):
    """
    Get a time string in format.
    :param pwd: Current working directory.
    :param file_name: File name.
    :param date_format: Date string in format. See https://strftime.org/ for details.
    :return: Time string in format.
    """

    return datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(pwd, file_name))).strftime(date_format)


def generate_time_string(date_format: str):
    """
    Generate time strings in format.
    :param date_format: Date string in format. See https://strftime.org/ for details.
    :return: Time string in format.
    """

    return date_format


def group_by_date(pwd: str, file_list: list, date_format: str):
    """
    Group files by date.
    :param pwd: Current working directory.
    :param file_list: List of files.
    :param date_format: Date string in format. See https://strftime.org/ for details.
    :return: A dictionary of files grouped by date.
    """

    file_group = {}

    for file in file_list:
        time_string = get_file_time_str(pwd, file, date_format)
        file_group[time_string] = file_group.get(time_string, []) + [file]

    return file_group


def print_group_info(group_info: dict):
    """
    Print group info.
    :param group_info: A dictionary of files grouped by date.
    """

    for time_string, files in group_info.items():
        print(f"{time_string}:")
        for file in files:
            print(f"  - {file}")


def do_move(pwd: str, group_info: dict):
    """
    Move files into new folders by group info.
    :param pwd: Current working directory.
    :param group_info: A dictionary of files grouped by date.
    """

    for time_string, files in group_info.items():
        # Create a new folder if not exists.
        if not os.path.exists(os.path.join(pwd, time_string)):
            os.mkdir(os.path.join(pwd, time_string))

        # Do move.
        for file in files:
            os.rename(os.path.join(pwd, file), os.path.join(pwd, time_string, file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Categorize files by specified date in a folder."
    )

    parser.add_argument(
        "folder_path",
        type = str,
        nargs = "?",
        help = "Folder path.",
        default = "."
    )

    parser.add_argument(
        "date_string",
        type = str,
        nargs = "?",
        help = "Date string in format. See https://strftime.org/ for details.",
        default = "%Y%m"
    )

    parser.add_argument(
        "-s",
        "--simulation",
        action = "store_true",
        help = "Do not move files actually, just print group info."
    )

    args = parser.parse_args()

    pwd = args.folder_path
    date_format = args.date_string

    print_group_info(group_by_date(pwd, get_file_list(pwd), args.date_string))

    if not args.simulation:
        do_move(pwd, group_by_date(pwd, get_file_list(pwd), args.date_string))
