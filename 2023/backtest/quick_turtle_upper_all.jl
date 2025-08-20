include("./../../2022/julia_test/utils.jl")
using HTTP
import JSON
using Statistics
using Dates
using Telegram, Telegram.API
using Nettle
using Formatting
using ArgParse


function parse_commandline()
    s = ArgParseSettings()
    ArgParse.@add_arg_table s begin
        "--market"
            help = "(spot, future)"
            required = false
            arg_type = String
            default = ""
        "--base_ticker"
            help = "(BTC, ETH, BNB, USDT)"
            required = false
            arg_type = String
            default = ""
        "--interval"
            help = "(1h, 2h, 4h, 6h, 8h, 12h)"
            required = false
            arg_type = String
            default = ""
    end
    return parse_args(s)
end


function elastic(n, time_frame)
    if time_frame == 8
        values = [0, 0.04, 0.08, 0.12, 0.16, 0.2, 0.33, 0.46, 0.59, 0.72, 0.85, 1.04, 1.23, 1.42, 1.61, 1.8, 1.99, 2.18, 2.37, 2.56, 2.75, 2.94, 3.13, 3.32, 3.51, 3.7, 3.89, 4.08, 4.27, 4.46, 4.65, 4.84, 5.03, 5.22, 5.41, 5.6, 5.79, 5.98, 6.17, 6.36, 6.55, 6.74, 6.93, 7.12, 7.31, 7.5, 7.69, 7.88, 8.07, 8.26, 8.45, 8.64, 8.83, 9.02]
        return values[n+1]
    elseif time_frame == 4 || time_frame == 6
        values = [0, 0.04, 0.08, 0.12, 0.16, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95, 2, 2.05, 2.1, 2.15, 2.2, 2.25, 2.3, 2.35, 2.4, 2.45, 2.5]
        return values[n+1]
    else
        # values = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.79, 0.98, 1.17, 1.36, 1.55, 1.74, 1.93, 2.12, 2.31, 2.5, 2.69, 2.88, 3.07, 3.26, 3.45, 3.64, 3.83, 4.02, 4.21, 4.4, 4.59, 4.78, 4.97, 5.16, 5.35, 5.54, 5.73, 5.92, 6.11, 6.3, 6.49, 6.68, 6.87, 7.06, 7.25, 7.44, 7.63, 7.82, 8.01, 8.2, 8.39, 8.58, 8.77, 8.96, 9.15, 9.34, 9.53, 9.72, 9.91, 10.1, 10.29, 10.48, 10.67, 10.86, 11.05, 11.24, 11.43, 11.62, 11.81, 12.00, 12.19, 12.38, 12.57, 12.76, 12.95, 13.14]
        try
            values = [0, 0.01, 0.02, 0.03, 0.04, 0.08, 0.12, 0.16, 0.2, 0.24, 0.28, 0.32, 0.36, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.64, 0.68, 0.72, 0.76, 0.80, 0.84, 0.88, 0.92, 0.96, 1.0, 1.04, 1.08, 1.12, 1.16, 1.2, 1.24, 1.28, 1.32, 1.36, 1.40, 1.44, 1.48, 1.52, 1.56, 1.6, 1.64, 1.68, 1.72, 1.76, 1.8, 1.84]
            return values[n+1]
        catch
            return values[end]
        end
    end   
end 






function log_maker(days, All_ohlcv, ticker_list, param ,weight)
    slippage = 0.9982 * 0.9982
    std_len = length(All_ohlcv["XRPUSDT"])
    standard_time = convert(Int64, fetch_ohlcv("BTCUSDT", "1d", 3)[1][1])
    global interval
    result = []

    for day in days-value1:-1:1
        momentum_count = 0
        for ticker in ticker_list
            try
                ohlcv = All_ohlcv[ticker][end-day-param+1:end-day+1]
                y_max = maximum( map(x->x[3], ohlcv[1:end-1]) )
                max_tr = maximum( map(x->abs(x[2]-x[5]), ohlcv[1:end-1]) )
                entry_price = y_max + max_tr * (weight+elastic(momentum_count, interval))

                if ohlcv[end][3] > entry_price
                    momentum_count += 1
                    if convert(Int64, ohlcv[end][1]) > standard_time 
                        exit_price = Float16(ohlcv[end][5])
                        earning = -100(ohlcv[end][5]/entry_price/slippage-1)
                        trade_time = string(unix2datetime((ohlcv[end][1])/1000))
                        text = "$(trade_time[6:end-3]) $(ticker[1:end-4])\nS:$(entry_price)\nB:$(exit_price) $(earning)\n\n"
                        push!(result, text)
                    end
                end
            catch e
            #    println(e)
            #    exit()
                continue
            end
        end
    end
    if length(result) > 10
        global result
        result = result[end-10:end]
        telegram_send(interval*" has been traded 10 or more times.")
    end
    send_msg = ""
    for text in result
        send_msg *= text
    end
    telegram_send(send_msg*interval)
    return nothing
end


configs = Dict(
    "1h" => Dict("sleep" => 2, "limit" => "960", "time_flag" => 40, "money"=>600, "value1" => 6, "value2" => 1.0),
    #"2h" => Dict("sleep" => 3, "limit" => "605", "time_flag" => 52, "money"=>650, "value1" => 10, "value2" => 2.9),          #2h default
    #"4h" => Dict("sleep" => 4, "limit" => "240", "time_flag" => 40, "money"=>850, "value1" => 15, "value2" => 0.63),          #4h default
    #"6h" => Dict("sleep" => 5, "limit" => "160", "time_flag" => 40, "money"=>900, "value1" => 40, "value2" => 0.09),
    #"8h" => Dict("sleep" => 7, "limit" => "123", "time_flag" => 41, "money"=>1000, "value1" => 36, "value2" => 0.1),
    #"12h" => Dict("sleep" => 10, "limit" => "80", "time_flag" => 40, "money"=>1100, "value1" => 6, "value2" => 1.43)
)

args = parse_commandline()
market = args["market"]
if cmp(market, "")==0
    println("select (spot, future)")
    market = readline()
end

base_ticker = args["base_ticker"]
if cmp(base_ticker, "")==0
    println("select (BTC, ETH, BNB, USDT)")
    base_ticker = readline()
end

interval = args["interval"]
if cmp(interval, "")==0
    println("select (1h, 2h, 4h, 6h, 8h, 12h)")
    interval = readline()
end


ticker_list = get_tickers()

config = configs[interval]
sleep_interval = config["sleep"]
limit = config["limit"]
time_flag = config["time_flag"]
money = config["money"]
value1 = config["value1"]
value2 = config["value2"]



i = 1
ticker_list = get_tickers()

btc_ohlcv = fetch_ohlcv("BTCUSDT", "1d", "1000")
start_time = string(btc_ohlcv[end-time_flag*i][1])
# end_time = string(btc_ohlcv[end-time_flag*(i-1)][1])
end_time = string(fetch_ohlcv("BTCUSDT", "1h", "1")[end][1])


# All_ohlcv = Dict((ticker, fetch_ohlcv(ticker, interval, limit, start_time, end_time, market)) for ticker in ticker_list)
All_ohlcv = Dict((ticker, fetch_ohlcv(ticker, interval)) for ticker in ticker_list)

# log_maker(parse(Int64, limit), All_ohlcv, ticker_list, value1, value2)
log_maker(984, All_ohlcv, ticker_list, value1, value2)

