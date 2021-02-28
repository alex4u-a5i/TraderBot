from binance.client import Client
from binance.helpers import date_to_milliseconds, interval_to_milliseconds


class HistoricalKlines:
    client = Client("", "")

    def __init__(self, symbol, interval, start_str, klines=[None]):
        self.symbol = symbol
        self.klines = klines
        self.interval = interval
        self.start_str = start_str
        self.end_str = start_str
        self.start_ts = date_to_milliseconds(self.start_str)
        self.end_ts = date_to_milliseconds(self.end_str)

    def fetch_klines(self, end_str=None):
        assert date_to_milliseconds(end_str) > self.end_ts
        assert (date_to_milliseconds(end_str) - self.end_ts) / interval_to_milliseconds(self.interval) < 500
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
            f.write(json.dumps(klines))
