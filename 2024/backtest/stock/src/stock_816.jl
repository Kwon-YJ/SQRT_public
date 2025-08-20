using Statistics
using DataFrames
using CSV
using Dates
using FileIO
using ArgParse

include("./../../../../2022/julia_test/utils.jl")

function parse_commandline()
    s = ArgParseSettings()

    @add_arg_table! s begin
        "--thres"
            help = "임계값 설정"
            arg_type = Float64
            default = 0.22
    end

    return parse_args(s)
end

function csv_init(input_data, file_name, threshold)
    if isempty(input_data)
        return nothing
    end
    if length(input_data) < 4
        return nothing
    end
    try 
        if input_data[4] < threshold
            return nothing
        end
    catch
        if parse(Float64, input_data[4]) < threshold
            return nothing
        end
    end

    df = DataFrame(A = [input_data[1]], B = [input_data[2]], C = [input_data[3]], D = [input_data[4]])
    try
        CSV.write("../result/"*file_name, df, append=true)
    catch
        return nothing
    end
end


function shortest_distance_(ratio, winrate)
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


function get_performance_(trade_log)
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
        total_perform = shortest_distance_(avg_w_l_ratio, win_count / trade_count)
    end
    return total_perform
end


function load_data(data_dir="../../data/", file_name="E6_1d.CSV")
    csv_data = CSV.read(data_dir*file_name, DataFrame)
    csv_data = csv_data[2:end, :]
    try
        # rename!(csv_data, [:t, :o, :h, :l, :c, :v, :s, :real_v])
        rename!(csv_data, [:t, :o, :h, :l, :c, :v, :temp])
    catch
        rename!(csv_data, [:t, :o, :h, :l, :c, :v])
    end
    #only_close = csv_data[!, "c"]
    #ema_8 = ema(only_close, 8)
    #ema_16 = ema(only_close, 16)
    #return csv_data, ema_8, ema_16
    return csv_data
end








function back_test(open_data::Vector{Float32}, high_data::Vector{Float32}, low_data::Vector{Float32}, close_data::Vector{Float32}, time_data, ema_8::Vector{Float32},ema_16::Vector{Float32},tail_d::Vector{Float32},body_d::Vector{Float32}, param_1::Float32, param_2::Float32, file_name::String, threshold::Float32)
    is_long = false
    # slippage = 0.997f0
    # slippage = 1
    slippage = 0.995f0

    long_entry_price = Vector{Float32}([])
    trade_log = Vector{Float32}([])
    long_sl = Vector{Float32}([])
    long_tp = Vector{Float32}([])

    for i::Int64=1:length(close_data)-1
        low_::Float32 = low_data[i]
        close_::Float32 = close_data[i]
        short_ema::Float32 = ema_8[i]
        open_::Float32 = open_data[i]

        if is_long == false
            if low_ < short_ema && min(close_, open_) > short_ema && short_ema > ema_16[i]
                if body_d[i] * param_1 < tail_d[i]
                    is_long = true
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
                push!(trade_log, earning)
            elseif high_data[i] > long_tp[end]
                is_long = false
                earning = 100 * (long_tp[end] / long_entry_price[end] * slippage -1)
                push!(trade_log, earning)
            end
        end
    end
        
    result = get_performance_(filter(isfinite, trade_log))
    csv_init([param_1, param_2, length(trade_log), result], file_name, threshold)
end




@inbounds function ema(data::Vector{T}, period::Int) where T
    alpha = 2 / (period + 1)
    ema_values = similar(data, T)
    sma = sum(@view data[1:period]) / period
    ema_values[period] = sma
    @fastmath @simd for i in (period+1):length(data)
        ema_values[i] = (data[i] - ema_values[i-1]) * alpha + ema_values[i-1]
    end
    return ema_values
end



function mkdir_exist_ok(dir_path)
    if isdir(dir_path) != true
        mkdir(dir_path)    
    end
end


mkdir_exist_ok("../result")

data_dir = "../csv_raw_file/"

function main()
    parsed_args = parse_commandline()
    threshold = Float32(parsed_args["thres"])
    
    mkdir_exist_ok("../result")
    data_dir = "../csv_raw_file/"

    Threads.@threads for file_name = readdir(data_dir)
        println(file_name)
        ohlc = 0
        try
            ohlc = load_data(data_dir, file_name)
        catch
            println("load_fail $(file_name)")
            continue
        end

        open_data = ohlc.o
        high_data = ohlc.h
        low_data = ohlc.l
        close_data = ohlc.c
        time_data = ohlc.t


        open_data = map(x->convert(Float32, x), open_data) 
        high_data = map(x->convert(Float32, x), high_data) 
        low_data = map(x->convert(Float32, x), low_data) 
        close_data = map(x->convert(Float32, x), close_data) 
        

        if length(close_data) < 40
            continue
        end


        ema_8 = ema(close_data, 8)
        ema_16 = ema(close_data, 16)


        tail_d = Vector{Float32}([])
        body_d = Vector{Float32}([])


        for i::Int64=1:length(close_data)
            low_::Float32 = low_data[i]
            close_::Float32 = close_data[i]
            open_::Float32 = open_data[i]
            push!(tail_d, min(close_, open_) - low_)
            push!(body_d, abs(close_ - open_))
        end

        println("start : $(file_name)")
        for param_1 in Float32.(range(start=0.8, stop=5, length=35))
            for param_2 in Float32.(range(start=0.8, stop=5, length=35))
                try
                    back_test(open_data, high_data, low_data, close_data, time_data, 
                             ema_8, ema_16, tail_d, body_d, param_1, param_2, file_name, threshold)
                catch
                    continue
                end
            end
        end
    end
end

if abspath(PROGRAM_FILE) == @__FILE__
    @time main()
end
