from historical import HistoricalKlines
from binance.client import Client

if __name__ == '__main__':
    symbol = ""
    eth = HistoricalKlines("ETHUSDT", Client.KLINE_INTERVAL_4HOUR, "25 Feb, 2021")
    eth.fetch_klines("26 Feb, 2021")
    eth.fetch_klines("27 Feb, 2021")



