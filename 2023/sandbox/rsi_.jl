using PyCall
include("./../../2022/julia_test/utils.jl")
pd = pyimport("pandas")
ta = pyimport("pandas_ta")
np = pyimport("numpy")


function fetch_rsi(ohlcv_data, type)
    if cmp(type, "hihg") == 0
        df = pd.DataFrame(data=np.array(ohlcv_data), columns=["0", "0", "close", "0", "0", "0", "0", "0", "0", "0", "0", "0"]) ## rsi(15, high)
    else
        df = pd.DataFrame(data=np.array(ohlcv_data), columns=["0", "0", "0", "close", "0", "0", "0", "0", "0", "0", "0", "0"]) ## rsi(15, high)
    end
    df.ta.rsi(length=15).tolist()
end

function log_maker(ticker, ohlcv, rsi_entry, rsi_exit)
    global buy_sell_log
    global total_buy_sell_log

    price = 0
    entry_time_buffer = []
    for (i, rsi) in enumerate(rsi_entry) 
        if i == 1 || i == 2
            continue
        end
        if i == length(rsi_entry)
            break
        end

        if price == 0
            # if rsi_entry[i-1] < 23 && ohlcv[i][2] > ohlcv[i][5] && ohlcv[i][6] > ohlcv[i-1][6] && ohlcv[i][6] > ohlcv[i-2][6]
            if rsi_entry[i-1] < 23
                entry_price = ohlcv[i+1][2]
                push!(entry_time_buffer, unix2datetime(ohlcv[i+1][1]*10^-3))
            end
        else
            if rsi_exit[i] > 38
                earning = 100(ohlcv[i+1][2] / entry_price * slippage - 1)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
                exit_time = unix2datetime(ohlcv[i+1][1]*10^-3)
                println("$(ticker) $(entry_time_buffer[1][1:6]) buy : $(entry_time_buffer[1][7:end]) // sell $(exit_time) $(earning)")
                empty!(entry_time_buffer)
                price = 0
            end
        end
    end
    if price != 0
        earning = 100(ohlcv[end][2] / entry_price * slippage - 1)
        push!(buy_sell_log, earning)
        push!(total_buy_sell_log, earning)
        exit_time = unix2datetime(ohlcv[end][1]*10^-3)
        println("$(ticker) $(entry_time_buffer[1][1:6]) buy : $(entry_time_buffer[1][7:end]) // sell $(exit_time) $(earning)")
        empty!(entry_time_buffer)
    end
    return nothing
end

const Slippage = 0.9982 * 0.9982
All_ohlcv = []
buy_sell_log = []
total_buy_sell_log = []
ticker_names = []
interval = "15m"

ticker_list = get_tickers()
sleep(60)

for day=2:365

    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))

    println("$(day)일 전부터 $(day-1)일 전까지")

    btc_ohlcv = fetch_ohlcv("BTCUSDT", "1d", "1000")
    start_time = string(btc_ohlcv[end-day-7][1])
    end_time = string(btc_ohlcv[end-day][1])

    for ticker in ticker_list
        push!(All_ohlcv, fetch_ohlcv(ticker, interval, 600, start_time, end_time))
        push!(ticker_names, ticker)
    end

    for (i, ohlcv) in enumerate(All_ohlcv)
        if ohlcv === nothing
            continue
        end
        
        df = 0
        rsi_entry = 0
        rsi_exit = 0

        if length(ohlcv) != 600
            continue
        end

        println(ohlcv[end])
        exit()

        df = pd.DataFrame(data=np.array(ohlcv), columns=["0","0", "close", "0", "0", "0", "0", "0", "0", "0", "0", "0"]) ## rsi(15, high)
        rsi_entry = df.ta.rsi(length=15).tolist()

        df = pd.DataFrame(data=np.array(ohlcv), columns=["0","0", "0", "close", "0", "0", "0", "0", "0", "0", "0", "0"]) ## rsi(8, low)
        rsi_exit = df.ta.rsi(length=8).tolist()


        log_maker(ticker_names[i], ohlcv[end-96:end],rsi_entry[end-96:end], rsi_exit[end-96:end])
    end
    get_performance(buy_sell_log, true, 100)
    get_performance(total_buy_sell_log, true, 100)


    empty!(All_ohlcv)
    empty!(buy_sell_log)
    empty!(ticker_names)

end
