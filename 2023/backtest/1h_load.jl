include("./../../2022/julia_test/utils.jl")
using HTTP
import JSON
using Statistics
using Dates
# using Base.Threads


using Telegram, Telegram.API
using Nettle
using Formatting
using Logging



function main(price_ch_interval)
    deleteat!(ticker_list, findall(x->x=="BTCDOMUSDT",ticker_list))



    All_ohlcvs = []
    ticker_lists = []
    

    for i in range(1, 24)
        println(i)
        All_ohlcv = Dict()
        del_list = []

        if i%2==0
            sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
        end

        interval = "1h"
        # limit = "240" #960
        # limit = "975"
        limit::Int64 = 960
        
        time_flag = 41

        btc_ohlcv = fetch_ohlcv("BTCUSDT", "1d", "1000")

        start_time = string(btc_ohlcv[end-time_flag*i][1])
        end_time = string(btc_ohlcv[end-time_flag*(i-1)][1])

        global ticker_list
        for ticker in ticker_list
            ohlcv = fetch_ohlcv(ticker, interval, string(limit+price_ch_interval), start_time, end_time)
            # ohlcv = fetch_ohlcv(ticker, interval, string(limit+price_ch_interval), start_time, end_time, "spot")
            All_ohlcv[ticker] = ohlcv
        end
        ticker_list=setdiff!(ticker_list, del_list)
        push!(All_ohlcvs, All_ohlcv)
        push!(ticker_lists, ticker_list)

    end
    return All_ohlcvs, ticker_lists
end




ticker_list = get_tickers()
# ticker_list = get_tickers_btc()

All_ohlcvs, ticker_lists = main(35)

