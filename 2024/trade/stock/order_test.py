import mojito
import pprint

with open("./krinv.key") as f:
    lines = f.readlines()

key = lines[0].strip()
secret = lines[1].strip()
acc_no = lines[2].strip()

broker = mojito.KoreaInvestment(api_key=key, api_secret=secret, acc_no=acc_no)
resp = broker.fetch_balance()
pprint.pprint(resp)


resp = broker.create_market_buy_order(symbol="005930", quantity=1)


print(resp)
