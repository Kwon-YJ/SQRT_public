# using Binance,Dates, DataFrames, Plots
using Dates, DataFrames, Plots
include("./temp_binance.jl")

#=
tickersChannel = Channel(1)
@async Binance.wsTradeAgg(tickersChannel, "BTCUSDT")


symbols = ["BTCUSDT", "XRPUSDT", "DOGEUSDT"]
for symbol in symbols
    @async Binance.wsTradeAgg(tickersChannel, symbol)
end



@sync while true
    kline = take!(tickersChannel)
    println(kline)
    println(now(Dates.UTC))
end
=#





#=

tickersChannel_1 = Channel(1)
@async Binance.wsDepth(tickersChannel_1, "BTCUSDT")
sleep(1.5)

tickersChannel_2 = Channel(1)
@async Binance.wsDepth(tickersChannel_2, "XRPUSDT")
sleep(1.5)

tickersChannel_3 = Channel(1)
@async Binance.wsDepth(tickersChannel_3, "DOGEUSDT")
sleep(1.5)

tickersChannel_4 = Channel(1)
@async Binance.wsDepth(tickersChannel_4, "XMRUSDT")
sleep(1.5)

tickersChannel_5 = Channel(1)
@async Binance.wsDepth(tickersChannel_5, "EOSUSDT")
sleep(1.5)

tickersChannel_6 = Channel(1)
@async Binance.wsDepth(tickersChannel_6, "NEOUSDT")
sleep(1.5)

tickersChannel_7 = Channel(1)
@async Binance.wsDepth(tickersChannel_7, "STMXUSDT")
sleep(1.5)

tickersChannel_8 = Channel(1)
@async Binance.wsDepth(tickersChannel_8, "JOEUSDT")
sleep(1.5)

tickersChannel_9 = Channel(1)
@async Binance.wsDepth(tickersChannel_9, "XVGUSDT")
sleep(1.5)

tickersChannel_10 = Channel(1)
@async Binance.wsDepth(tickersChannel_10, "TRBUSDT")
sleep(1.5)

tickersChannel_11 = Channel(1)
@async Binance.wsDepth(tickersChannel_11, "ARKMUSDT")
sleep(1.5)

tickersChannel_12 = Channel(1)
@async Binance.wsDepth(tickersChannel_12, "GMXUSDT")
sleep(1.5)

tickersChannel_13 = Channel(1)
@async Binance.wsDepth(tickersChannel_13, "ZENUSDT")
sleep(1.5)

tickersChannel_14 = Channel(1)
@async Binance.wsDepth(tickersChannel_14, "TRUUSDT")
sleep(1.5)

tickersChannel_15 = Channel(1)
@async Binance.wsDepth(tickersChannel_15, "QNTUSDT")
sleep(1.5)

tickersChannel_16 = Channel(1)
@async Binance.wsDepth(tickersChannel_16, "AGIXUSDT")
sleep(1.5)

tickersChannel_17 = Channel(1)
@async Binance.wsDepth(tickersChannel_17, "CFXUSDT")
sleep(1.5)

println("start!")



# @sync while true
while true
    result = []

    push!(result, take!(tickersChannel_1))
    println("1 done")
    push!(result, take!(tickersChannel_2))
    println("2 done")
    push!(result, take!(tickersChannel_3))
    println("3 done")
    push!(result, take!(tickersChannel_4))
    println("4 done")
    push!(result, take!(tickersChannel_5))
    println("5 done")
    push!(result, take!(tickersChannel_6))
    println("6 done")
    push!(result, take!(tickersChannel_7))
    println("7 done")
    push!(result, take!(tickersChannel_8))
    println("8 done")
    push!(result, take!(tickersChannel_9))
    println("9 done")
    push!(result, take!(tickersChannel_10))
    println("10 done")
    push!(result, take!(tickersChannel_11))
    println("11 done")
    push!(result, take!(tickersChannel_12))
    println("12 done")
    push!(result, take!(tickersChannel_13))
    println("13 done")
    push!(result, take!(tickersChannel_14))
    println("14 done")
    push!(result, take!(tickersChannel_15))
    println("15 done")
    push!(result, take!(tickersChannel_16))
    println("16 done")
    push!(result, take!(tickersChannel_17))
    println("17 done")


    println(result)
    println(now(Dates.UTC))
end

=#

#=
@sync while true
    kline = take!(tickersChannel_6)
    println(kline)
    println(now(Dates.UTC))
end
=#


#=

using WebSockets: serve, writeguarded, readguarded, @wslog, open, HTTP, Response, ServerWS, with_logger, WebSocketLogger


open("wss://fstream.binance.com/ws/bnbusdt@aggTrade") do ws_client
    data, success = readguarded(ws_client)
    if success
        println(stderr, ws_client, " received: ", String(data))
    end
end

=#


#=
result = Dict()
tickersChannel = Channel(100)
@async Binance.ws_test(tickersChannel)
count = 0
@time begin
    @sync while true
    #while true
        global count
        kline = take!(tickersChannel)
        print(kline)
        error()
        if kline["s"] in keys(result)
            result[kline["s"]] += 1
        else
            result[kline["s"]] = 1
        end
        # println("$(now(Dates.UTC)), $(count)")
        count += 1
        if count > 100000
            break
        end
    end
end
# 각 티커 별로 몇 번 받았는가
for key in keys(result)
    println("$(key) : $(result[key])")
end
# 해당 기간 동안 0회 받은 티커 색출
temp =  ["TRXUSDT", "BAKEUSDT", "SOLUSDT", "SPELLUSDT", "RADUSDT", "SSVUSDT", "ARUSDT", "TOMOUSDT", "ARBUSDT", "LRCUSDT", "DOGEUSDT", "NEOUSDT", "GALAUSDT", "SUIUSDT", "MANAUSDT", "LTCUSDT", "LEVERUSDT", "BLURUSDT", "COMPUSDT", "VETUSDT", "LUNA2USDT", "CTKUSDT", "MASKUSDT", "PEOPLEUSDT", "TRUUSDT", "DARUSDT", "C98USDT", "ENSUSDT", "AAVEUSDT", "COMBOUSDT", "CKBUSDT", "KSMUSDT", "ALPHAUSDT", "CRVUSDT", "LDOUSDT", "SKLUSDT", "HFTUSDT", "OPUSDT", "DGBUSDT", "QNTUSDT", "ADAUSDT", "HOTUSDT", "IOSTUSDT", "IOTXUSDT", "CTSIUSDT", "ACHUSDT", "UMAUSDT", "MATICUSDT", "PERPUSDT", "THETAUSDT", "STORJUSDT", "SANDUSDT", "JOEUSDT", "HBARUSDT", "BNBUSDT", "INJUSDT", "ZRXUSDT", "DASHUSDT", "REEFUSDT", "GALUSDT", "AMBUSDT", "FETUSDT", "FLOWUSDT", "WAVESUSDT", "RVNUSDT", "CFXUSDT", "SXPUSDT", "EGLDUSDT", "API3USDT", "ROSEUSDT", "EOSUSDT", "XTZUSDT", "AVAXUSDT", "ICPUSDT", "FOOTBALLUSDT", "SNXUSDT", "RENUSDT", "XLMUSDT", "1000PEPEUSDT", "FTMUSDT", "WOOUSDT", "KAVAUSDT", "ZENUSDT", "AUDIOUSDT", "IDUSDT", "BLUEBIRDUSDT", "ONEUSDT", "OGNUSDT", "ARPAUSDT", "RDNTUSDT", "BCHUSDT", "DEFIUSDT", "CHZUSDT", "MKRUSDT", "KLAYUSDT", "KEYUSDT", "UNIUSDT", "HOOKUSDT", "CELOUSDT", "ETCUSDT", "STGUSDT", "LINAUSDT", "ONTUSDT", "ATOMUSDT", "ASTRUSDT", "BATUSDT", "QTUMUSDT", "SFPUSDT", "ATAUSDT", "MINAUSDT", "SUSHIUSDT", "RUNEUSDT", "RSRUSDT", "ZECUSDT", "TLMUSDT", "RLCUSDT", "FXSUSDT", "APTUSDT", "ANTUSDT", "BLZUSDT", "DENTUSDT", "XEMUSDT", "BALUSDT", "MTLUSDT", "HIGHUSDT", "DUSKUSDT", "JASMYUSDT", "GTCUSDT", "XVSUSDT", "ANKRUSDT", "PHBUSDT", "COTIUSDT", "XMRUSDT", "DOTUSDT", "KNCUSDT", "OMGUSDT", "GMTUSDT", "UNFIUSDT", "AGIXUSDT", "TRBUSDT", "GRTUSDT", "BELUSDT", "ENJUSDT", "AXSUSDT", "FILUSDT", "ALGOUSDT", "DYDXUSDT", "CVXUSDT", "LPTUSDT", "STXUSDT", "TUSDT", "RNDRUSDT", "1000SHIBUSDT", "APEUSDT", "IDEXUSDT", "BANDUSDT", "1000XECUSDT", "IMXUSDT", "LQTYUSDT", "LINKUSDT", "1000FLOKIUSDT", "OCEANUSDT", "ZILUSDT", "IOTAUSDT", "EDUUSDT", "FLMUSDT", "STMXUSDT", "CELRUSDT", "NEARUSDT", "GMXUSDT", "1INCHUSDT", "ALICEUSDT", "XRPUSDT", "MAGICUSDT", "ICXUSDT", "LITUSDT", "BNXUSDT", "ETHUSDT", "1000LUNCUSDT", "CHRUSDT", "NKNUSDT"]
for key in temp
    try
        a = result[key]
    catch
        println(key)
    end
end
=#







using Dates
include("./../../2022/julia_test/utils.jl")
using Base.Threads




#=
function ws_run(channel::Channel, ticker)
    try
        HTTP.WebSockets.open(string(BINANCE_API_WS_new, "btcusdt@bookTicker"); verbose=false) do io
            while !eof(io);
                put!(channel, r2j(readavailable(io)))
            end
        end
    catch e
        @async println("reconnection at $(now(Dates.UTC)) cuz : $(e)")
        ws_run(channel)
    end
    @async println("reconnection at $(now(Dates.UTC))")
    ws_run(channel)
end



=#




function r2j(response)
    JSON.parse(String(response))
end



function ws_run(channel::Channel)
    try
        global url
        # HTTP.WebSockets.open(string(BINANCE_API_WS, "$(ticker)@bookTicker"); verbose=false) do io
        HTTP.WebSockets.open(url[1:end-1]; verbose=false) do io
        # HTTP.WebSockets.open("wss://fstream.binance.com/stream?streams=bnbusdt@bookTicker/btcusdt@bookTicker") do io
            while !eof(io);
                put!(channel, r2j(readavailable(io)))
            end
        end
    catch e
        @async println("reconnection at $(now(Dates.UTC)) cuz : $(e)")
        ws_run(channel)
    end
    @async println("reconnection at $(now(Dates.UTC))")
    ws_run(channel)
end




function main()
    data_channel = Channel(10000)
    ticker_list = get_tickers()


    @async ws_run(data_channel)


    while true
        minute = parse(Int8, Dates.format(now(Dates.UTC), "MM"))  
        data = take!(data_channel)

        #time_data = data["T"]
        #ticker = data["s"]

        #@async println(ticker)
        #@async println("$(unix2datetime(time_data/1000))")
        #@async println(now(Dates.UTC))
        
        
        ticker = uppercase(split(data["stream"],"@")[1])
        price = parse(Float16, data["data"]["b"])
        time_ = data["data"]["T"]

        # @async println("$(ticker)\n $(unix2datetime(time_/1000))\n $(now(Dates.UTC))")

        println("$(ticker)\n$(unix2datetime(time_/1000))\n$(now(Dates.UTC)) \n$(parse(Float16, data["data"]["b"])) \n$(parse(Float32, data["data"]["b"])) \n$(parse(Float64, data["data"]["b"]))")

    end
end


BINANCE_API_WS = "wss://fstream.binance.com/ws/" # futures




ticker_list = get_tickers()


url = "wss://fstream.binance.com/stream?streams="




for ticker in ticker_list
    global url
    ticker = lowercase(ticker)
    url *= "$(ticker)@bookTicker/"
end


main()