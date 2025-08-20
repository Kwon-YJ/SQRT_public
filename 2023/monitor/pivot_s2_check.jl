using HTTP
import JSON
using Statistics
using Dates
include("./../../2022/julia_test/utils.jl")
using Random

ticker_list = get_tickers()
# sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))

function log_maker(limit, All_ohlcv, ticker_list, value1, value2, double_ohlcv)

end







println("12")
All_ohlcv = []
for ticker = ticker_list
    ohlcv = fetch_ohlcv(ticker, "12h", "7")
    if length(ohlcv) == 7
        push!(All_ohlcv, ohlcv)
    end
end
log_maker(7, All_ohlcv, ticker_list, 1.93, 1.9325, true)

println("8")
All_ohlcv = []
for ticker = ticker_list
    ohlcv = fetch_ohlcv(ticker, "8h", "9")
    if length(ohlcv) == 9
        push!(All_ohlcv, ohlcv)
    end
end
log_maker(9, All_ohlcv, ticker_list, 1.94, 1.935, true)

println("6")
All_ohlcv = []
for ticker = ticker_list
    ohlcv = fetch_ohlcv(ticker, "6h", "11")
    if length(ohlcv) == 11
        push!(All_ohlcv, ohlcv)
    end
end
log_maker(11, All_ohlcv, ticker_list, 1.93, 1.925, true)

println("4")
All_ohlcv = []
for ticker = ticker_list
    ohlcv = fetch_ohlcv(ticker, "4h", "15")
    if length(ohlcv) == 15
        push!(All_ohlcv, ohlcv)
    end
end

log_maker(15, All_ohlcv, ticker_list, 1.955, 1.95, false)
println("4_D")
log_maker(15, All_ohlcv, ticker_list, 1.96, 1.955, true)

println("2")
All_ohlcv = []
for ticker = ticker_list
    ohlcv = fetch_ohlcv(ticker, "2h", "27")
    if length(ohlcv) == 27
        push!(All_ohlcv, ohlcv)
    end
end

log_maker(27, All_ohlcv, ticker_list, 1.94, 1.935, false)
println("2_d")
log_maker(27, All_ohlcv, ticker_list, 1.96, 1.955, true)


println("1")
All_ohlcv = []
for ticker = ticker_list
    ohlcv = fetch_ohlcv(ticker, "1h", "51")
    if length(ohlcv) == 51
        push!(All_ohlcv, ohlcv)
    end
end

log_maker(51, All_ohlcv, ticker_list, 1.945, 1.94, true)


