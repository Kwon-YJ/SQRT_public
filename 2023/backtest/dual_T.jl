using HTTP
import JSON
using Statistics
using Dates
include("./../../2022/julia_test/utils.jl")


total_buy_sell_log = []

for ticker in get_tickers()
    global total_buy_sell_log
    # ticker = "BTCUSDT"
    btc_ohlcv = fetch_ohlcv(ticker, "1d", "1500")
    buy_sell_log = []
    slippage = 0.9994 * 0.9994

    position_handler = Dict()

    for (i, ohlcv) in enumerate(btc_ohlcv)
        if i < 5
        # if i < 10
            continue
        end
        
        temp_ohclv = btc_ohlcv[i-4:i-1]
        
        HH = maximum(map(x->x[3], temp_ohclv))
        HC = maximum(map(x->x[5], temp_ohclv))
        LC = minimum(map(x->x[5], temp_ohclv))
        LL = minimum(map(x->x[4], temp_ohclv))
        K = 0.5
        # K = 0.65
        
        long_target_price = ohlcv[2] + (max(HH-LC, HC-LL) * K)
        short_target_price = ohlcv[2] - (max(HH-LC, HC-LL) * K)
        
        if ohlcv[3] > long_target_price
            keys_ = [key for key in keys(position_handler)]
            if length(keys_) == 0
                position_handler["long"] = long_target_price
            else
                if haskey(position_handler, "long")
                    continue
                else
                    earning = -100(long_target_price/position_handler["short"]/slippage-1)
                    push!(buy_sell_log, earning)        
                    push!(total_buy_sell_log, earning)        
                    entry_time = "$(unix2datetime(ohlcv[1]/1000))"
                    text="$(ticker) $(entry_time) short:$(convert(Float16,short_target_price)) // exit:$(ohlcv[5]) $(earning)"
                    println(text)      
                end
                empty!(position_handler)
                position_handler["long"] = long_target_price
            end
        elseif ohlcv[4] < short_target_price
            keys_ = [key for key in keys(position_handler)]
            if length(keys_) == 0
                position_handler["short"] = short_target_price
            else
                if haskey(position_handler, "short")
                    continue
                else
                    earning = 100(short_target_price/position_handler["long"]*slippage-1)
                    push!(buy_sell_log, earning)        
                    push!(total_buy_sell_log, earning)        
                    entry_time = "$(unix2datetime(ohlcv[1]/1000))"
                    text="$(ticker) $(entry_time) long:$(convert(Float16,short_target_price)) // exit:$(ohlcv[5]) $(earning)"
                    println(text)  

                end
                empty!(position_handler)
                position_handler["short"] = short_target_price
            end
        end
    end
    get_performance(buy_sell_log, true, 100)
end

get_performance(total_buy_sell_log, true, 100)




