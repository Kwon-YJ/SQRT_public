import mojito
import pprint


def init_broker():
    with open("./krinv.key") as f:
        lines = f.readlines()

        key = lines[0].strip()
        secret = lines[1].strip()
        acc_no = lines[2].strip()

        broker = mojito.KoreaInvestment(api_key=key, api_secret=secret, acc_no=acc_no)
    return broker


broker = init_broker()


def buy_samsung_1_qty():
    resp = broker.create_market_buy_order(symbol="005930", quantity=1)
    return resp


def get_balance():
    return broker.fetch_balance()
