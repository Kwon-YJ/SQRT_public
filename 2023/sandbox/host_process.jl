using Distributed
addprocs(3)


@everywhere include("./../../2022/julia_test/utils.jl")


ticker_list = get_tickers()
sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
del_list = []
for ticker in ticker_list
    if length(fetch_ohlcv(ticker, "1d", 43)) != 43
        push!(del_list, ticker)
    end
end
ticker_list=setdiff!(ticker_list, del_list)
deleteat!(ticker_list, findall(x->x=="BTCUSDT",ticker_list))
deleteat!(ticker_list, findall(x->x=="BTCDOMUSDT",ticker_list))
@everywhere @eval ticker_list = $ticker_list










while true
    all_ohlcv["1h"] = get_ohlc("1h")
    all_ohlcv["2h"] = get_ohlc("2h")
    all_ohlcv["4h"] = get_ohlc("4h")
    all_ohlcv["6h"] = get_ohlc("6h")
    all_ohlcv["8h"] = get_ohlc("8h")
    all_ohlcv["12h"] = get_ohlc("12h")

end



result = remotecall_fetch(()->all_ohlcv, 2)
println((result))

remotecall(get_ohlc, 2, "1h")
# remotecall_fetch(get_ohlc, 2, "1h")


result = remotecall_fetch(()->all_ohlcv, 2)
println((result["BTCUSDT"][end]))

@everywhere all_ohlcv = Dict{String, Any}()


println(all_ohlcv)

result = remotecall_fetch(()->all_ohlcv, 2)
println((result))













function get_ohlc(time_frame::String)
    global ticker_list
    global all_ohlcv
    all_ohlcv = Dict{String, Any}()
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, time_frame, 45)
        if length(ohlcv) !=45
            continue
        end
        all_ohlcv[ticker] = ohlcv
    end
end




all_ohlcv = Dict()

all_ohlcv["1h"] = get_ohlc("1h")
all_ohlcv["2h"] = get_ohlc("2h")
all_ohlcv["4h"] = get_ohlc("4h")
all_ohlcv["6h"] = get_ohlc("6h")
all_ohlcv["8h"] = get_ohlc("8h")
all_ohlcv["12h"] = get_ohlc("12h")

@everywhere @eval all_ohlcv = $all_ohlcv










exit()

@everywhere begin
    # if myid == 2

        global all_ohlcv = 123456
    
        function get_ohlc(time_frame::String)
            global ticker_list
            #
            ticker_list = ["BTCUSDT", "BNBUSDT"]
            #
            result = Dict{String, Any}()
            for ticker in ticker_list
                ohlcv = fetch_ohlcv(ticker, time_frame, 45)
                if length(ohlcv) !=45
                    continue
                end
                result[ticker] = ohlcv
            end
            return result
        end

        function get_all_ohlcv()
            result = Dict{String, Any}()
            result["1h"] = get_ohlc("1h")
            #result["2h"] = get_ohlc("2h")
            #result["4h"] = get_ohlc("4h")
            #result["6h"] = get_ohlc("6h")
            #result["8h"] = get_ohlc("8h")
            #result["12h"] = get_ohlc("12h")
            return result
        end

        global all_ohlcv = get_all_ohlcv()
    # end

end



#=
@everywhere begin
    if myid == 2

        global all_ohlcv = 123456

        function get_ohlc(time_frame::String)
            global ticker_list
            result = Dict{String, Any}()
            for ticker in ticker_list
                ohlcv = fetch_ohlcv(ticker, time_frame, 45)
                if length(ohlcv) !=45
                    continue
                end
                result[ticker] = ohlcv
            end
            return result
        end

        function get_all_ohlcv()
            result = Dict{String, Any}()
            result["1h"] = get_ohlc("1h")
            result["2h"] = get_ohlc("2h")
            result["4h"] = get_ohlc("4h")
            result["6h"] = get_ohlc("6h")
            result["8h"] = get_ohlc("8h")
            result["12h"] = get_ohlc("12h")
            return result
        end
        # all_ohlcv = get_all_ohlcv()
        
    end
end
=#


# area = @spawnat 2 circle_area(10)
# result = fetch(area)
# println(result) # 314.0

sleep(10)

result = remotecall_fetch(()->all_ohlcv, 2)

# println(result["BTCUSDT"][end][5])
println(typeof(result))

sleep(120)





result = remotecall_fetch(()->all_ohlcv, 2)

# println(result["BTCUSDT"][end][5])
println(typeof(result))
