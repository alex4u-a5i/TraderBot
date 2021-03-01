from binance.client import Client
from binance.helpers import date_to_milliseconds
import json

""" Kline Format e.g.
[
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

class HistoricalKlines:
    """Fetch Historical Klines from Binance"""
    client = Client("", "")

    def __init__(self, symbol, interval, start_str, klines=None):
        if klines is None:
            klines = [[]]
        self.symbol = symbol
        self.klines = klines
        self.interval = interval
        self.start_str = start_str
        self.end_str = start_str

    def fetch_klines(self, end_str=None):
        if end_str:
            assert date_to_milliseconds(end_str) > date_to_milliseconds(self.start_str)
        new_klines = self.client.get_historical_klines(self.symbol, self.interval, self.end_str, end_str)
        self.klines[-1] = new_klines[0]
        self.klines += new_klines[1:]
        self.end_str = end_str

    def get_klines(self):
        return self.klines

    def save_to_file(self):
        with open(
                "Binance_{}_{}_{}-{}.json".format(
                    self.symbol,
                    self.interval,
                    date_to_milliseconds(self.start_str),
                    date_to_milliseconds(self.end_str)
                ),
                "w"
        ) as f:
            f.write(json.dumps(self.klines))
