import ccxt


def get_tickers():
    base_ticker = list(binance.fetch_tickers().keys())
    base_ticker = [
        base_ticker[i] for i in range(len(base_ticker)) if "/USDT" in base_ticker[i]
    ]
    base_ticker.remove("BTCDOM/USDT")
    return base_ticker


binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "bOHcvOmxqFVGN6FPsJwcnh4QOxw0D6oaFGHjEhpU2pby1bt7EJDb6t9TExauOccU",
        "secret": "Yece0g5APcAZR4sXJl1M007tLL9w9bB7Qp2o3fGFYJjN3f6tfx6lOCq1LdmRk4Ob",
        "enableRateLimit": False,
    }
)
binance.load_markets()

ticker_list = get_tickers()

result = 0

for ticker in ticker_list:
    temp = binance.fetch_open_orders(ticker)
    result += len(temp)

print(result)

a = [len(binance.fetch_open_orders(ticker)) for ticker in ticker_list]

print(sum(a))
