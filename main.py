import HistoricalData
from binance.client import Client

if __name__ == '__main__':
    symbol = ""
    klines = HistoricalData.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1HOUR, "25 Feb, 2021",
                                                  "26 Feb, 2021")
    HistoricalData.save_to_file(klines, "ETHUSDT", Client.KLINE_INTERVAL_1HOUR, "25 Feb, 2021", "26 Feb, 2021")
