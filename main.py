# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import dateparser
from datetime import datetime, timezone


def date_to_milliseconds(date_str):
    epoch = datetime.fromtimestamp(0, tz=timezone.utc)

    d = dateparser.parse(date_str)

    if d.tzinfo is None or d.tzingo.utcoffset(d) is None:
        d = d.replace(tzinfo=timezone.utc)

    return int((d - epoch).total_seconds() * 1000)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(date_to_milliseconds("January 01, 2018"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
