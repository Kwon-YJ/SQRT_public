import pickle
from pykrx import stock

ordered_dict = None
with open("ORDERD_DICT.pickle", "rb") as f:
    ordered_dict = pickle.load(f)


ticker_list = stock.get_market_ticker_list(market="ALL")
code2ticker = {}

for code in ticker_list:
    ticker_kr_name = stock.get_market_ticker_name(code)
    code2ticker[code] = ticker_kr_name

for key in ordered_dict.keys():
    print(f"{code2ticker[key]} : {ordered_dict[key]}") 
print(len(ordered_dict))
