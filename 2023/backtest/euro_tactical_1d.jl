using CSV, DataFrames
using Dates
include("./../../2022/julia_test/utils.jl")
using Statistics

data = CSV.read("./E6_1d.CSV", DataFrame)

ohlcvs = []
for i=1:nrow(data)
    ohlcv = values( data[i, :] )
    push!(ohlcvs, ohlcv)
end

function log_maker(ohlcv)
    global total_buy_sell_log
    global money_stack
    buy_sell_log = []
    # slippage = 0.9994 * 0.9994
    slippage = 1
    for j=length(ohlcv)-5:-1:2
        
        high = ohlcv[end-(j)][3]
        low = ohlcv[end-(j)][4]
        close = ohlcv[end-(j)][5]

        if high - low == 0
            continue
        end
        ibs = (close - low) / (high - low)
        
        if ibs > 0.9  #1d

            entry_price= ohlcv[end-j+1][2]
            exit_price = ohlcv[end-j+2][2]
            earning = -100(exit_price/entry_price-1) *47
            entry_time= ohlcv[end-j+1][1]
            exit_time = ohlcv[end-j+2][1]
            text = "$(entry_time) $(exit_time) short : $(entry_price) / exit : $(exit_price) $(earning) $(2.64*earning)"
            push!(money_stack, 2.64*earning)
            println(text)
            push!(buy_sell_log, earning)
            push!(total_buy_sell_log, earning)

            if earning > 3
                entry_price= ohlcv[end-j+2][2]
                exit_price = ohlcv[end-j+3][2]
                earning_local = 100(exit_price/entry_price-1) *47
                entry_time= ohlcv[end-j+2][1]
                exit_time = ohlcv[end-j+3][1]
                text = "$(entry_time) $(exit_time) long : $(entry_price) / exit : $(exit_price) $(earning_local) $(2.64*earning_local)"
                #push!(money_stack, 2.64*earning_local)
                #println(text)
                #push!(buy_sell_log, earning_local)
                #push!(total_buy_sell_log, earning_local)
            end

            if earning < -3
                entry_price= ohlcv[end-j+2][2]
                exit_price = ohlcv[end-j+3][2]
                earning_local = -100(exit_price/entry_price-1) *47
                entry_time= ohlcv[end-j+2][1]
                exit_time = ohlcv[end-j+3][1]
                text = "$(entry_time) $(exit_time) short : $(entry_price) / exit : $(exit_price) $(earning_local) $(2.64*earning_local)"
                #push!(money_stack, 2.64*earning_local)
                #println(text)
                #push!(buy_sell_log, earning_local)
                #push!(total_buy_sell_log, earning_local)
            end

        end

        if ibs < 0.05 #1d
            entry_price= ohlcv[end-j+1][2]
            exit_price = ohlcv[end-j+2][2]
            earning = -100(exit_price/entry_price-1) *47
            entry_time= ohlcv[end-j+1][1]
            exit_time = ohlcv[end-j+2][1]            
            text = "$(entry_time) $(exit_time) short : $(entry_price) / exit : $(exit_price) $(earning) $(2.64*earning)"
            push!(money_stack, 2.64*earning)
            println(text)
            push!(buy_sell_log, earning)
            push!(total_buy_sell_log, earning)

            if earning > 5
                entry_price= ohlcv[end-j+2][2]
                exit_price = ohlcv[end-j+3][2]
                earning_local = 100(exit_price/entry_price-1) *47
                entry_time= ohlcv[end-j+2][1]
                exit_time = ohlcv[end-j+3][1]
                text = "$(entry_time) $(exit_time) long : $(entry_price) / exit : $(exit_price) $(earning_local) $(2.64*earning_local)"
                #push!(money_stack, 2.64*earning_local)
                #println(text)
                #push!(buy_sell_log, earning_local)
                #push!(total_buy_sell_log, earning_local)
            end

            if earning < 5
                entry_price= ohlcv[end-j+2][2]
                exit_price = ohlcv[end-j+3][2]
                earning_local = -100(exit_price/entry_price-1) *47
                entry_time= ohlcv[end-j+2][1]
                exit_time = ohlcv[end-j+3][1]
                text = "$(entry_time) $(exit_time) short : $(entry_price) / exit : $(exit_price) $(earning_local) $(2.64*earning_local)"
                #push!(money_stack, 2.64*earning_local)
                #println(text)
                #push!(buy_sell_log, earning_local)
                #push!(total_buy_sell_log, earning_local)
            end
        end
    end
    get_performance(buy_sell_log, true)
    empty!(buy_sell_log)
    get_performance(total_buy_sell_log, true, 264)
    return nothing
end

money_stack = []

total_buy_sell_log = []

log_maker(ohlcvs)



using Plots
result = []
for (i, money) in enumerate(money_stack) 
    push!(result, sum(money_stack[1:i]))
end
x = 1:1:length(result)
y =result
plot(x, y)
savefig("myplot.png")


result = []
for (i, money) in enumerate(money_stack)
    if i < 12
        continue
    end
    push!(result, sum(money_stack[i-11:i]))
end
println(minimum(result))
# 최대 연속 누적 손실 673불 