import time

import binance_pb2
from lib import config

def get_binance_url(data: binance_pb2.SubscriptionRequest) -> str:
    symbols = [s.lower() + "@ticker" for s in data.symbols]

    url = f"{config.BINANCE_URL}?streams={'/'.join(symbols)}"

    return url

def binance_response_to_model(json_data: dict) -> binance_pb2.TickerData:
    symbol = json_data['data']['s']
    price = json_data['data']['c']
    ts = int(time.time() * 1000)

    model = binance_pb2.TickerData(symbol=symbol, price=price, timestamp=ts)

    return model