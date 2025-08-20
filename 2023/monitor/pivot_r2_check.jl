using HTTP
import JSON
using Statistics
using Dates
include("./../../2022/julia_test/utils.jl")

ticker_list = get_tickers()
# sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))

function log_maker(limit, All_ohlcv, ticker_list, value1, value2, double_ohlcv)

end


All_ohlcv = []
limit = [9, 15, 27, 51]

# limit = limit*2

println("888888888888888888888888")
for ticker = ticker_list
    ohlcv = fetch_ohlcv(ticker, "8h", string(limit[1]))
    if length(ohlcv) == limit[1]
        push!(All_ohlcv, ohlcv)
    end
end


log_maker(limit[1], All_ohlcv, ticker_list, 2.24, 2.24, true)

println("444444444444444444444444")
All_ohlcv = []
for ticker = ticker_list
    ohlcv = fetch_ohlcv(ticker, "4h", string(limit[2]))
    if length(ohlcv) == limit[2]
        push!(All_ohlcv, ohlcv)
    end
end
log_maker(limit[2], All_ohlcv, ticker_list, 2.3, 2.15, true)

println("222222222222222222222222")
All_ohlcv = []
for ticker = ticker_list
    ohlcv = fetch_ohlcv(ticker, "2h", string(limit[3]))
    if length(ohlcv) == limit[3]
        push!(All_ohlcv, ohlcv)
    end
end
log_maker(limit[3], All_ohlcv, ticker_list, 2.3, 2.15, true)

println("111111111111111111111111")
All_ohlcv = []
for ticker = ticker_list
    ohlcv = fetch_ohlcv(ticker, "1h", string(limit[4]))
    if length(ohlcv) == limit[4]
        push!(All_ohlcv, ohlcv)
    end
end
log_maker(limit[4], All_ohlcv, ticker_list, 2.3, 2.15, false)

