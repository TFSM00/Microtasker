"""
Module containing useful functions for the website
"""
import datetime as dt
import re


def time_ago(time: str) -> str:
    """
    Returns a string showing how long ago the inputted time string was.
    """
    formatted_dt = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    time_ago = re.split(r"[:\.\,]+", str(dt.datetime.utcnow() - formatted_dt))

    if len(time_ago) > 4:
        return f"{time_ago[0]} ago"

    if int(time_ago[-4]) > 0:
        if int(time_ago[-4]) == 1:
            return f"{int(time_ago[-4])} hour ago"
        return f"{int(time_ago[-4])} hours ago"

    if int(time_ago[-3]) > 0:
        if int(time_ago[-3]) == 1:
            return f"{int(time_ago[-3])} minute ago"
        return f"{int(time_ago[-3])} minutes ago"

    return "Just now"


if __name__ == '__main__':
    class Obj:
        def __init__(self) -> None:
            self.date_created = "2023-09-18 19:00:20.448339"
    obj = Obj()
    print(time_ago(object.date_created))
