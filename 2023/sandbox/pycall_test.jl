using PyCall

include("./../../2022/julia_test/utils.jl")

pd = pyimport("pandas")
ta = pyimport("pandas_ta")
np = pyimport("numpy")

py"""
def add20(x):
    return x + 20
"""

pydata = py"add20"(20)

println(pydata)

BTC_ohlcv = fetch_ohlcv("BTCUSDT")


df = pd.DataFrame(data=np.array(BTC_ohlcv), columns=["0","0", "close", "0", "0", "0", "0", "0", "0", "0", "0", "0"]) ## rsi(15, high)
println(df)
rsi_entry = df.ta.rsi(length=15).tolist()
println(rsi_entry)

println(typeof(rsi_entry))
