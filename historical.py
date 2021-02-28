from binance.client import Client
from binance.helpers import date_to_milliseconds
import json


class HistoricalKlines:
    client = Client("", "")

    def __init__(self, symbol, interval, start_str, klines=[[]]):
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
