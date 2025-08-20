using CSV, DataFrames
using Dates
include("./../../2022/julia_test/utils.jl")
using Statistics

# data = CSV.read("./E6_1d.CSV", DataFrame)




function log_maker(ohlcv)
    global total_buy_sell_log
    buy_sell_log = []
    # slippage = 0.9994 * 0.9994
    slippage = 1
    for j=length(ohlcv)-2:-1:3
        
        high = ohlcv[end-(j)][3]
        low = ohlcv[end-(j)][4]
        close = ohlcv[end-(j)][5]

        if high - low == 0
            continue
        end
        ibs = (close - low) / (high - low)
        
        if ibs > 0.9 #1d

            entry_price= ohlcv[end-j+1][2]
            exit_price = ohlcv[end-j+2][2]
            earning = -100(exit_price/entry_price-1)
            entry_time= ohlcv[end-j+1][1]
            exit_time = ohlcv[end-j+2][1]
            text = "$(entry_time) $(exit_time) short : $(entry_price) / exit : $(exit_price) $(earning) $(2.64*earning)"
            #println(text)
            #push!(buy_sell_log, earning)
            #push!(total_buy_sell_log, earning)

            if earning > -1 # ibs > 0.9
                entry_price= ohlcv[end-j+2][2]
                exit_price = ohlcv[end-j+3][2]
                earning = 100(exit_price/entry_price-1) 
                entry_time= ohlcv[end-j+2][1]
                exit_time = ohlcv[end-j+3][1]
                text = "$(entry_time) $(exit_time) short : $(entry_price) / exit : $(exit_price) $(earning) $(2.64*earning)"
                println(text)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
            end

            if earning < 1 # ibs > 0.9
                entry_price= ohlcv[end-j+2][2]
                exit_price = ohlcv[end-j+3][2]
                earning = -100(exit_price/entry_price-1) 
                entry_time= ohlcv[end-j+2][1]
                exit_time = ohlcv[end-j+3][1]
                text = "$(entry_time) $(exit_time) short : $(entry_price) / exit : $(exit_price) $(earning) $(2.64*earning)"
                println(text)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
            end

        end

        if ibs < 0.05 #1d
            entry_price= ohlcv[end-j+1][2]
            exit_price = ohlcv[end-j+2][2]
            earning = -100(exit_price/entry_price-1) 
            entry_time= ohlcv[end-j+1][1]
            exit_time = ohlcv[end-j+2][1]            
            text = "$(entry_time) $(exit_time) short : $(entry_price) / exit : $(exit_price) $(earning) $(2.64*earning)"
            #println(text)
            #push!(buy_sell_log, earning)
            #push!(total_buy_sell_log, earning)

            if earning > 0
                entry_price= ohlcv[end-j+2][2]
                exit_price = ohlcv[end-j+3][2]
                earning = -100(exit_price/entry_price-1) 
                entry_time= ohlcv[end-j+2][1]
                exit_time = ohlcv[end-j+3][1]
                text = "$(entry_time) $(exit_time) short : $(entry_price) / exit : $(exit_price) $(earning) $(2.64*earning)"
                println(text)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
            end

            if earning < 0
                entry_price= ohlcv[end-j+2][2]
                exit_price = ohlcv[end-j+3][2]
                earning = 100(exit_price/entry_price-1) 
                entry_time= ohlcv[end-j+2][1]
                exit_time = ohlcv[end-j+3][1]
                text = "$(entry_time) $(exit_time) short : $(entry_price) / exit : $(exit_price) $(earning) $(2.64*earning)"
                println(text)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
            end
        end
    end
    get_performance(buy_sell_log, true, 30)
    empty!(buy_sell_log)
    # get_performance(total_buy_sell_log, true, 30)
    return nothing
end

ticker_list = get_tickers()
total_buy_sell_log = []
for ticker in ticker_list
    ohlcvs = fetch_ohlcv(ticker, "8h", 1500)
    log_maker(ohlcvs)
    println(ticker)
    sleep(0.07)
    #readline()
end

get_performance(total_buy_sell_log, true, 30)

