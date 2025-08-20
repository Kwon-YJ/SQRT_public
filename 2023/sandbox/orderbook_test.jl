using Dates
include("./../../2022/julia_test/utils.jl")


#function get_all_ask_price(ticker_list)
#    result = map(x-> parse(Float64, get_depth(x)["asks"][1][1]), ticker_list)
#end

function get_all_ask_price(ticker_list)
    prices = [parse(Float64, get_depth(ticker)["asks"][1][1]) for ticker in ticker_list]
    return Dict(zip(ticker_list), prices)
end


ticker_list = get_tickers()

sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))


while true
    @time result = get_all_ask_price(ticker_list)
end



