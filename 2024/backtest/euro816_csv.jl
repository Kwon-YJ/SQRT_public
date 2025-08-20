using Statistics
using DataFrames
using CSV
using Dates

function csv_init(input_data, file_name)
    if isempty(input_data) || input_data[4] < 0
        return nothing
    end
    df = DataFrame(A = [input_data[1]], B = [input_data[2]], C = [input_data[3]], D = [input_data[4]])
    CSV.write(file_name, df, append=true)
end


function shortest_distance(ratio, winrate)
    lins = [i/10000 for i in 0:100000]
    y = [-log(0.99) / (log(1+0.01*i) - log(0.99)) for i in lins]
    least_distance = 100
    for i in 1:100000
        dx = lins[i] - ratio
        dy = y[i] - winrate
        distance = sqrt(dx^2 + dy^2)
        if distance < least_distance
            least_distance = distance
        end
    end
    base_line = -log(0.99) / (log(1+0.01*ratio) - log(0.99))
    if winrate > base_line
        return least_distance
    else
        return -least_distance
    end
end


function get_performance(trade_log)
    if length(trade_log) == 0
        return 0
    else
        trade_count = length(trade_log)
    end
    win = []
    lose = []
    for value in trade_log
        if value > 0
            push!(win,value)
        else
            push!(lose,value)
        end
    end

    if length(lose) == 0
        avg_lose = 10^-6
        std_lose = 10^-6
    else
        avg_lose = mean(lose)
        std_lose = std(lose, corrected=false)
    end

    if length(win) == 0
        avg_win = 10^-6
        win_count = 0
    else
        avg_win = mean(win)
        win_count = length(win)
    end

    avg_w_l_ratio = -1 * avg_win / avg_lose
    if avg_w_l_ratio < 0
        total_perform = "Nan"
    else
        total_perform = shortest_distance(avg_w_l_ratio, win_count / trade_count)
    end
    return total_perform
end


function load_data(data_dir="../../data/", file_name="E6_1d.CSV")
    csv_data = CSV.read(data_dir*file_name, DataFrame)
    csv_data = csv_data[2:end, :]
    try
        rename!(csv_data, [:t, :o, :h, :l, :c, :v, :s, :real_v])
    catch
        rename!(csv_data, [:t, :o, :h, :l, :c, :v])
    end
    #only_close = csv_data[!, "c"]
    #ema_8 = ema(only_close, 8)
    #ema_16 = ema(only_close, 16)
    #return csv_data, ema_8, ema_16
    return csv_data
end


function back_test(ohlc, param_1=3, param_2=1.5, file_name="temp_reult.csv")
    
    open_data=ohlc[!, "o"]
    high_data=ohlc[!, "h"]
    low_data =ohlc[!, "l"]
    close_data=ohlc[!,"c"]
    time_data = ohlc[!,"t"]


    ema_8 = ema(close_data, 8)
    ema_16 = ema(close_data, 16)

    is_long = false

    trade_log = []

    slippage = 1

    long_entry_price = []

    long_sl = []
    long_tp = []

    for i=1:length(ohlc[!,"c"])-1

        high_ = high_data[i]
        low_ = low_data[i]
        close_ = close_data[i]

        short_ema = ema_8[i]
        long_ema = ema_16[i]
        
        open_ = open_data[i]

        # long case
        if is_long == false
            if low_ < short_ema && min(close_, open_) > short_ema && short_ema > long_ema
                tail_d = min(close_, open_) - low_
                body_d = abs(close_ - open_)
                if body_d * param_1 < tail_d
                    is_long = true
                    text = "$( (unix2datetime( time_data[i])) ) long : $(open_data[i+1]) "
                    println(text)
                    push!(long_entry_price, open_data[i+1])
                    push!(long_sl, low_)
                    push!(long_tp, open_data[i+1] + param_2* abs((low_-max(close_, open_))))
                    long_entry_time = time_data[i+1]
                end
            end
        else
            if low_ < long_sl[end]
                is_long = false
                earning = 100 * (long_sl[end] / long_entry_price[end] * slippage -1)
                text = "$( (unix2datetime( time_data[i])) ) exit : $(long_sl[end]) "
                println(text)
                push!(trade_log, earning)
            elseif high_ > long_tp[end]
                is_long = false
                earning = 100 * (long_tp[end] / long_entry_price[end] * slippage -1)
                text = "$( (unix2datetime( time_data[i])) ) exit : $(long_tp[end]) "
                println(text)
                push!(trade_log, earning)
            end
        end
    end
        
    result = get_performance(trade_log)


    # py"csv_init([param_1, param_2, len(trade_log), result], args.file_name)"
    csv_init([param_1, param_2, length(trade_log), result], file_name)
end


function ema(data::Vector{T}, period::Int) where T
    alpha = 2 / (period + 1)
    ema_values = similar(data, T)
    sma = sum(@view data[1:period]) / period
    ema_values[period] = sma
    @fastmath @simd for i in (period+1):length(data)
        ema_values[i] = (data[i] - ema_values[i-1]) * alpha + ema_values[i-1]
    end
    return ema_values
end

    

data_dir = "fx_data/"

file_name = "ADAUSD_1d.csv"
back_test(load_data(data_dir, file_name), 3, 1.5, file_name)



