# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import dateparser
from datetime import datetime, timezone
import time
from binance.client import Client


def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds
        :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
        :type interval: str
        :return:
             None if unit not one of m, h, d or w
             None if string not in correct format
             int value of interval in milliseconds
    """
    ms = None

    seconds_per_unit = {
        "m": 60,
        "h": 60 ** 2,
        "d": 24 * 60 ** 2,
        "w": 7 * 24 * 60 ** 2
    }

    unit = interval[-1]

    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass

    return ms


def date_to_milliseconds(date_str):
    epoch = datetime.fromtimestamp(0, tz=timezone.utc)

    d = dateparser.parse(date_str)

    if d.tzinfo is None or d.tzingo.utcoffset(d) is None:
        d = d.replace(tzinfo=timezone.utc)
    return int((d - epoch).total_seconds() * 1000)
    """[
        1499040000000,  # Open time
        "0.01634790",  # Open
        "0.80000000",  # High
        "0.01575800",  # Low
        "0.01577100",  # Close
        "148976.11427815",  # Volume
        1499644799999,  # Close time
        "2434.19055334",  # Quote asset volume
        308,  # Number of trades
        "1756.87402397",  # Taker buy base asset volume
        "28.46694368",  # Taker buy quote asset volume
        "17928899.62484339"  # Ignore
    ]"""

def get_historical_klines(symbol, interval, start_str, end_str=None):
    """Get Historical Klines from Binance

        See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/

        If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

        :param symbol: Name of symbol pair e.g BNBBTC
        :type symbol: str
        :param interval: Biannce Kline interval
        :type interval: str
        :param start_str: Start date string in UTC format
        :type start_str: str
        :param end_str: optional - end date string in UTC format
        :type end_str: str
        :return: list of OHLCV values
        """
    client = Client("", "")

    output_data = []

    limit = 500

    timeframe = interval_to_milliseconds(interval)

    start_ts = date_to_milliseconds(start_str)

    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    # set start data before the symbol list data, which is unknown
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts
        )

        # handle the case where our start date is before the symbol was listed
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to the output data
            output_data += temp_data

            # update our start timestamp
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe

        else:
            # update our start time
            start_ts += timeframe

        idx += 1
        # check if we received less than the required limit
        if len(temp_data) < limit:
            break

        # sleep after third call
        if idx % 3 == 0:
            time.sleep(1)

    return output_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    klines = get_historical_klines("ETHBUSD", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2020", "2 Dec, 2020")
    print(klines)