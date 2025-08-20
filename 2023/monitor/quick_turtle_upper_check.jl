using Dates
include("./../../2022/julia_test/utils.jl")

ticker_list = get_tickers()
sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))

for ticker in ticker_list
    ohlcv = fetch_ohlcv(ticker, "1d", "10")
    if length(ohlcv) != 10
        continue
    end
    highs = [high[3] for high in ohlcv]
    if highs[end] == maximum(highs[end-4:end])
        println(ticker," // " ,maximum(highs[end-4:end-1]), " // " ,ohlcv[end][5])
    end
end