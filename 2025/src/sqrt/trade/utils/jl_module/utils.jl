using Telegram, Telegram.API
using HTTP
import JSON
using Statistics
using Dates
using Nettle
using Formatting
using Logging
using FileIO
using DotEnv

function mkdir_exist_ok(dir_path)
    if isdir(dir_path) != true
        mkdir(dir_path)
    end
end


function get_current_price_new(ticker_list)
    url = "https://fapi.binance.com/fapi/v1/ticker/bookTicker"
    raw = HTTP.request("GET", url; verbose=0)
    json_data = JSON.parse(String(raw.body))
    result = Dict()
    for data in json_data
        result[data["symbol"]] = parse(Float64, data["bidPrice"])
    end
    return result
end

function get_current_price(ticker_list)
    prices = [parse(Float64, get_depth(ticker)["asks"][1][1]) for ticker in ticker_list]
    return Dict(ticker => prices[i] for (i, ticker) in enumerate(ticker_list))
end

function get_current_price_kline(ticker_list)
    prices = [fetch_ohlcv(ticker, "1m", "1", "", "", "future")[1][4] for ticker in ticker_list]
    return Dict(ticker => prices[i] for (i, ticker) in enumerate(ticker_list))
end

function get_current_price_old(option="futures")
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    if cmp(option, "futures") != 0
        url = "https://api.binance.com/api/v3/ticker/price"
    end
    raw = HTTP.request("GET", url; verbose=0)
    json_data = JSON.parse(String(raw.body))
    Dict((ticker["symbol"], parse(Float64, ticker["price"])) for ticker in json_data if occursin("USDT", ticker["symbol"]) && occursin("_", ticker["symbol"]) == false)
end

function get_depth(ticker)
    url = "https://fapi.binance.com/fapi/v1/depth?symbol=$(ticker)&limit=5"
    raw = HTTP.request("GET", url; verbose=0)
    json_data = JSON.parse(String(raw.body))
    return json_data
end

function wait_next_day()
    hours, minute = parse(Int8, Dates.format(now(Dates.UTC), "HH")), parse(Int8, Dates.format(now(Dates.UTC), "MM"))
    sleep(86400 - 60 - (3600(hours) + 60(minute))) # D-day UTC 11:59:00
    sleep(rand() * 10)
end

function wait_next(time_frame)
    ohlcv = fetch_ohlcv("BTCUSDT", time_frame, 2)
    time_shift = ohlcv[end][1] - ohlcv[1][1]
    target_time = ohlcv[end][1] + time_shift
    sleep(target_time / 1000 - time() - rand() * 10)
end

function nP2(array::Array)
    result = []
    for (i, item1) in enumerate(array)
        sub_array = deepcopy(array)
        splice!(sub_array, i)
        for item2 in sub_array
            push!(result, (item1, item2))
        end
    end
    return result
end

function log_file_maker(data) # data_example=["abc\n", "efg\n", "hij\n"]
    open("$(string(now(Dates.UTC))[1:10]).txt", "w") do fd
        result = ""
        for str_lint in data
            result *= str_lint
        end
        write(fd, result)
    end
end

function telegram_send(data)
    chat_id = "801167350"
    tg = TelegramClient(token, chat_id=chat_id)
    # sendMessage(text  = data)
    while true
        try
            sendMessage(text=data)
            return nothing
        catch
            sleep(2)
            continue
        end
    end
end

function precision_optimize(ticker::String, amount, price)
    market_info_row = HTTP.request("GET", "https://fapi.binance.com/fapi/v1/exchangeInfo"; verbose=0)
    market_info = JSON.parse(String(market_info_row.body))["symbols"]
    for values in market_info
        if values["symbol"] == ticker
            return round(amount, digits=values["quantityPrecision"]), round(price, digits=values["pricePrecision"])
        end
    end
end

function precision_optimize_spot(ticker::String, amount, price)
    market_info_row = HTTP.request("GET", "https://api.binance.com/api/v3/exchangeInfo"; verbose=0)
    market_info = JSON.parse(String(market_info_row.body))["symbols"]
    for values in market_info
        if values["symbol"] == ticker
            return round(amount, digits=values["quantityPrecision"]), round(price, digits=values["pricePrecision"])
        end
    end
end

function get_amount(ticker::String, money)
    price = fetch_ohlcv(ticker)[end][5]
    amount = money / price
    amount, price = precision_optimize(ticker, amount, price)
    if occursin("e", string(amount))
        amount = format(amount)
    end
    return amount, price
end

function get_amount(ticker::String, money, price)
    amount = money / price
    amount, price = precision_optimize(ticker, amount, price)
    if occursin("e", string(amount))
        amount = format(amount)
    end
    return amount, price
end

function get_amount_spot(ticker::String, money)
    price = fetch_ohlcv(ticker, "1m", 2, "", "", "spot")[end][5]
    amount = money / price
    amount, price = precision_optimize(ticker, amount, price)
    if occursin("e", string(amount))
        amount = format(amount)
    end
    return amount, price
end

function get_tickers_old()
    return ["TRXUSDT", "BAKEUSDT", "SOLUSDT", "SPELLUSDT", "RADUSDT", "SSVUSDT", "ARUSDT", "ARBUSDT", "LRCUSDT", "DOGEUSDT", "NEOUSDT", "GALAUSDT", "SUIUSDT", "MANAUSDT", "LTCUSDT", "LEVERUSDT", "BLURUSDT", "COMPUSDT", "VETUSDT", "LUNA2USDT", "CTKUSDT", "MASKUSDT", "PEOPLEUSDT", "TRUUSDT", "DARUSDT", "C98USDT", "ENSUSDT", "AAVEUSDT", "COMBOUSDT", "CKBUSDT", "KSMUSDT", "ALPHAUSDT", "CRVUSDT", "LDOUSDT", "SKLUSDT", "HFTUSDT", "OPUSDT", "DGBUSDT", "QNTUSDT", "ADAUSDT", "HOTUSDT", "IOSTUSDT", "IOTXUSDT", "CTSIUSDT", "ACHUSDT", "UMAUSDT", "MATICUSDT", "PERPUSDT", "THETAUSDT", "STORJUSDT", "SANDUSDT", "JOEUSDT", "HBARUSDT", "BNBUSDT", "INJUSDT", "ZRXUSDT", "DASHUSDT", "REEFUSDT", "GALUSDT", "AMBUSDT", "FETUSDT", "FLOWUSDT", "WAVESUSDT", "RVNUSDT", "CFXUSDT", "SXPUSDT", "EGLDUSDT", "API3USDT", "ROSEUSDT", "EOSUSDT", "XTZUSDT", "AVAXUSDT", "ICPUSDT", "FOOTBALLUSDT", "SNXUSDT", "RENUSDT", "XLMUSDT", "1000PEPEUSDT", "FTMUSDT", "WOOUSDT", "KAVAUSDT", "ZENUSDT", "AUDIOUSDT", "IDUSDT", "BLUEBIRDUSDT", "ONEUSDT", "OGNUSDT", "ARPAUSDT", "RDNTUSDT", "BCHUSDT", "DEFIUSDT", "CHZUSDT", "MKRUSDT", "KLAYUSDT", "KEYUSDT", "UNIUSDT", "HOOKUSDT", "CELOUSDT", "ETCUSDT", "STGUSDT", "LINAUSDT", "ONTUSDT", "ATOMUSDT", "ASTRUSDT", "BATUSDT", "QTUMUSDT", "SFPUSDT", "ATAUSDT", "MINAUSDT", "SUSHIUSDT", "RUNEUSDT", "RSRUSDT", "ZECUSDT", "TLMUSDT", "RLCUSDT", "FXSUSDT", "APTUSDT", "ANTUSDT", "BLZUSDT", "DENTUSDT", "XEMUSDT", "BALUSDT", "MTLUSDT", "HIGHUSDT", "DUSKUSDT", "JASMYUSDT", "GTCUSDT", "XVSUSDT", "ANKRUSDT", "PHBUSDT", "COTIUSDT", "XMRUSDT", "DOTUSDT", "KNCUSDT", "OMGUSDT", "GMTUSDT", "UNFIUSDT", "AGIXUSDT", "TRBUSDT", "GRTUSDT", "BELUSDT", "ENJUSDT", "AXSUSDT", "FILUSDT", "ALGOUSDT", "DYDXUSDT", "CVXUSDT", "LPTUSDT", "STXUSDT", "TUSDT", "RNDRUSDT", "1000SHIBUSDT", "APEUSDT", "IDEXUSDT", "BANDUSDT", "1000XECUSDT", "IMXUSDT", "LQTYUSDT", "LINKUSDT", "1000FLOKIUSDT", "OCEANUSDT", "ZILUSDT", "IOTAUSDT", "EDUUSDT", "FLMUSDT", "STMXUSDT", "CELRUSDT", "NEARUSDT", "GMXUSDT", "1INCHUSDT", "ALICEUSDT", "XRPUSDT", "MAGICUSDT", "ICXUSDT", "LITUSDT", "BNXUSDT", "ETHUSDT", "1000LUNCUSDT", "CHRUSDT", "NKNUSDT"]
    #sever_time_raw = HTTP.request("GET", "https://fapi.binance.com/fapi/v1/time"; verbose=0)
    #sever_time = JSON.parse(String(sever_time_raw.body))["serverTime"]
    #url = "https://fapi.binance.com/fapi/v1/ticker/price"
    #raw = HTTP.request("GET", url; verbose=0)
    #json_data = JSON.parse(String(raw.body))
    #[ticker["symbol"] for ticker in json_data if occursin("USDT", ticker["symbol"]) && occursin("_", ticker["symbol"]) == false && abs(sever_time-ticker["time"]) < 86400.00]
end

function get_tickers()
    # return ["SSVUSDT", "ORBSUSDT", "SUPERUSDT", "AUCTIONUSDT", "DASHUSDT", "CYBERUSDT", "OPUSDT", "REZUSDT", "ACEUSDT", "STRKUSDT", "MINAUSDT", "PIXELUSDT", "SFPUSDT", "PERPUSDT", "ETHFIUSDT", "ENJUSDT", "1000XECUSDT", "UNIUSDT", "BLZUSDT", "YGGUSDT", "WAVESUSDT", "AEVOUSDT", "TRBUSDT", "XRPUSDT", "ALGOUSDT", "RENUSDT", "TRXUSDT", "CHZUSDT", "UMAUSDT", "FETUSDT", "TOKENUSDT", "BEAMXUSDT", "ARKUSDT", "RIFUSDT", "JUPUSDT", "AMBUSDT", "C98USDT", "VETUSDT", "LINAUSDT", "OMGUSDT", "CELRUSDT", "HIFIUSDT", "REEFUSDT", "FXSUSDT", "LRCUSDT", "JASMYUSDT", "1000PEPEUSDT", "1000FLOKIUSDT", "OMUSDT", "SXPUSDT", "BIGTIMEUSDT", "FLMUSDT", "AGLDUSDT", "XAIUSDT", "LPTUSDT", "HOOKUSDT", "1000LUNCUSDT", "NEARUSDT", "EGLDUSDT", "BICOUSDT", "FTMUSDT", "DODOXUSDT", "NEOUSDT", "MAGICUSDT", "ONDOUSDT", "ARBUSDT", "ALICEUSDT", "JTOUSDT", "NKNUSDT", "BNBUSDT", "BATUSDT", "LEVERUSDT", "BONDUSDT", "ZENUSDT", "THETAUSDT", "BADGERUSDT", "DENTUSDT", "CTSIUSDT", "PORTALUSDT", "STGUSDT", "EDUUSDT", "MEMEUSDT", "ILVUSDT", "RDNTUSDT", "OCEANUSDT", "RVNUSDT", "TIAUSDT", "MASKUSDT", "HIGHUSDT", "XLMUSDT", "MKRUSDT", "CAKEUSDT", "ARUSDT", "XVGUSDT", "BOMEUSDT", "XEMUSDT", "GASUSDT", "SEIUSDT", "FLOWUSDT", "LSKUSDT", "ZRXUSDT", "RONINUSDT", "NMRUSDT", "QTUMUSDT", "ALPHAUSDT", "ETHUSDT", "INJUSDT", "DYMUSDT", "ATAUSDT", "UNFIUSDT", "YFIUSDT", "KASUSDT", "WUSDT", "MYROUSDT", "MTLUSDT", "PYTHUSDT", "BALUSDT", "DARUSDT", "WOOUSDT", "LUNA2USDT", "STEEMUSDT", "TUSDT", "OGNUSDT", "DYDXUSDT", "METISUSDT", "COMPUSDT", "MANAUSDT", "TLMUSDT", "BANDUSDT", "AXSUSDT", "BNXUSDT", "WLDUSDT", "ZECUSDT", "HBARUSDT", "XVSUSDT", "1000SATSUSDT", "SOLUSDT", "NOTUSDT", "TNSRUSDT", "ACHUSDT", "CRVUSDT", "ASTRUSDT", "LOOMUSDT", "IOSTUSDT", "CHRUSDT", "ALTUSDT", "MANTAUSDT", "WAXPUSDT", "MOVRUSDT", "GTCUSDT", "PHBUSDT", "GRTUSDT", "MATICUSDT", "ONGUSDT", "QNTUSDT", "POLYXUSDT", "STXUSDT", "GLMUSDT", "LQTYUSDT", "ANKRUSDT", "AAVEUSDT", "RUNEUSDT", "BSVUSDT", "LITUSDT", "BBUSDT", "1000BONKUSDT", "LTCUSDT", "HFTUSDT", "TAOUSDT", "BLURUSDT", "CFXUSDT", "IMXUSDT", "EOSUSDT", "SANDUSDT", "GMXUSDT", "ONEUSDT", "BAKEUSDT", "MAVUSDT", "PENDLEUSDT", "SAGAUSDT", "ENAUSDT", "VANRYUSDT", "APTUSDT", "HOTUSDT", "DOGEUSDT", "TWTUSDT", "ADAUSDT", "KAVAUSDT", "OXTUSDT", "ONTUSDT", "ROSEUSDT", "ENSUSDT", "GALUSDT", "TRUUSDT", "ZETAUSDT", "KEYUSDT", "FRONTUSDT", "JOEUSDT", "SPELLUSDT", "ARKMUSDT", "CKBUSDT", "COTIUSDT", "RNDRUSDT", "GALAUSDT", "WIFUSDT", "GMTUSDT", "NFPUSDT", "SNXUSDT", "DEFIUSDT", "OMNIUSDT", "MAVIAUSDT", "POWRUSDT", "DOTUSDT", "1INCHUSDT", "ZILUSDT", "ETHWUSDT", "USTCUSDT", "ARPAUSDT", "STMXUSDT", "ICXUSDT", "API3USDT", "SUSHIUSDT", "DUSKUSDT", "ETCUSDT", "PEOPLEUSDT", "AIUSDT", "AGIXUSDT", "TONUSDT", "ORDIUSDT", "1000SHIBUSDT", "XMRUSDT", "LINKUSDT", "RLCUSDT", "1000RATSUSDT", "SKLUSDT", "CELOUSDT", "IOTXUSDT", "SUIUSDT", "ATOMUSDT", "BCHUSDT", "NTRNUSDT", "KSMUSDT", "KNCUSDT", "FILUSDT", "STORJUSDT", "RSRUSDT", "XTZUSDT", "COMBOUSDT", "IDUSDT", "IOTAUSDT", "AXLUSDT", "BNTUSDT", "AVAXUSDT", "BELUSDT", "ICPUSDT", "LDOUSDT", "APEUSDT", "KLAYUSDT"]
    sever_time_raw = HTTP.request("GET", "https://fapi.binance.com/fapi/v1/time"; verbose=0)
    sever_time = JSON.parse(String(sever_time_raw.body))["serverTime"]
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    raw = HTTP.request("GET", url; verbose=0)
    json_data = JSON.parse(String(raw.body))
    result = [ticker["symbol"] for ticker in json_data if occursin("USDT", ticker["symbol"]) && occursin("_", ticker["symbol"]) == false && abs(sever_time - ticker["time"]) < 86400.00]
    deleteat!(result, findall(x -> x == "BTCDOMUSDT", result))
    deleteat!(result, findall(x -> x == "BTCUSDT", result))
    deleteat!(result, findall(x -> x == "USDCUSDT", result))
    return result
end

function get_tickers_btc()
    return ["TRXBTC", "BAKEBTC", "SOLBTC", "SPELLBTC", "RADBTC", "SSVBTC", "ARBTC", "TOMOBTC", "ARBBTC", "LRCBTC", "DOGEBTC", "NEOBTC", "GALABTC", "SUIBTC", "MANABTC", "LTCBTC", "COMPBTC", "VETBTC", "CTKBTC", "PEOPLEBTC", "TRUBTC", "DARBTC", "C98BTC", "ENSBTC", "AAVEBTC", "CKBBTC", "KSMBTC", "ALPHABTC", "CRVBTC", "LDOBTC", "SKLBTC", "HFTBTC", "OPBTC", "DGBBTC", "QNTBTC", "ADABTC", "HOTBTC", "IOSTBTC", "IOTXBTC", "CTSIBTC", "ACHBTC", "UMABTC", "MATICBTC", "PERPBTC", "THETABTC", "STORJBTC", "SANDBTC", "JOEBTC", "HBARBTC", "BNBBTC", "INJBTC", "ZRXBTC", "DASHBTC", "REEFBTC", "GALBTC", "AMBBTC", "FETBTC", "FLOWBTC", "WAVESBTC", "RVNBTC", "CFXBTC", "SXPBTC", "EGLDBTC", "API3BTC", "ROSEBTC", "EOSBTC", "XTZBTC", "AVAXBTC", "ICPBTC", "SNXBTC", "RENBTC", "XLMBTC", "FTMBTC", "WOOBTC", "KAVABTC", "ZENBTC", "AUDIOBTC", "IDBTC", "ONEBTC", "OGNBTC", "ARPABTC", "RDNTBTC", "BCHBTC", "CHZBTC", "MKRBTC", "KLAYBTC", "KEYBTC", "UNIBTC", "HOOKBTC", "CELOBTC", "ETCBTC", "STGBTC", "LINABTC", "ONTBTC", "ATOMBTC", "ASTRBTC", "BATBTC", "QTUMBTC", "SFPBTC", "ATABTC", "MINABTC", "SUSHIBTC", "RUNEBTC", "RSRBTC", "ZECBTC", "TLMBTC", "RLCBTC", "FXSBTC", "APTBTC", "ANTBTC", "BLZBTC", "DENTBTC", "XEMBTC", "BALBTC", "MTLBTC", "HIGHBTC", "DUSKBTC", "JASMYBTC", "GTCBTC", "XVSBTC", "ANKRBTC", "PHBBTC", "COTIBTC", "XMRBTC", "DOTBTC", "KNCBTC", "OMGBTC", "GMTBTC", "UNFIBTC", "AGIXBTC", "TRBBTC", "GRTBTC", "BELBTC", "ENJBTC", "AXSBTC", "FILBTC", "ALGOBTC", "DYDXBTC", "CVXBTC", "LPTBTC", "STXBTC", "RNDRBTC", "YFIBTC", "APEBTC", "IDEXBTC", "BANDBTC", "IMXBTC", "LQTYBTC", "LINKBTC", "OCEANBTC", "ZILBTC", "IOTABTC", "EDUBTC", "FLMBTC", "STMXBTC", "CELRBTC", "NEARBTC", "GMXBTC", "1INCHBTC", "ALICEBTC", "XRPBTC", "MAGICBTC", "ICXBTC", "LITBTC", "BNXBTC", "ETHBTC", "CHRBTC", "NKNBTC"]
end

function get_tickers_eth()
    return ["TRXETH", "SOLETH", "SSVETH", "ARBETH", "LRCETH", "NEOETH", "GALAETH", "MANAETH", "LTCETH", "VETETH", "PEOPLEETH", "DARETH", "AAVEETH", "KSMETH", "CRVETH", "OPETH", "ADAETH", "HOTETH", "IOSTETH", "IOTXETH", "MATICETH", "THETAETH", "STORJETH", "SANDETH", "BNBETH", "ZRXETH", "DASHETH", "GALETH", "AMBETH", "WAVESETH", "EGLDETH", "ROSEETH", "EOSETH", "XTZETH", "AVAXETH", "ICPETH", "SNXETH", "XLMETH", "FTMETH", "KAVAETH", "ZENETH", "ONEETH", "ARPAETH", "KEYETH", "UNIETH", "ETCETH", "ONTETH", "ATOMETH", "ASTRETH", "BATETH", "QTUMETH", "RUNEETH", "ZECETH", "RLCETH", "APTETH", "BLZETH", "DENTETH", "XEMETH", "MTLETH", "JASMYETH", "XMRETH", "DOTETH", "KNCETH", "OMGETH", "GMTETH", "UNFIETH", "GRTETH", "BELETH", "ENJETH", "AXSETH", "FILETH", "ALGOETH", "DYDXETH", "APEETH", "LINKETH", "ZILETH", "IOTAETH", "STMXETH", "CELRETH", "NEARETH", "XRPETH", "ICXETH", "LITETH", "CHRETH"]
end

function get_tickers_bnb()
    return ["TRXBNB", "BAKEBNB", "SOLBNB", "SPELLBNB", "RADBNB", "ARBNB", "TOMOBNB", "LRCBNB", "DOGEBNB", "NEOBNB", "GALABNB", "SUIBNB", "MANABNB", "LTCBNB", "COMPBNB", "VETBNB", "CTKBNB", "MASKBNB", "PEOPLEBNB", "DARBNB", "C98BNB", "ENSBNB", "AAVEBNB", "COMBOBNB", "KSMBNB", "ALPHABNB", "CRVBNB", "OPBNB", "QNTBNB", "ADABNB", "HOTBNB", "CTSIBNB", "MATICBNB", "THETABNB", "SANDBNB", "HBARBNB", "INJBNB", "ZRXBNB", "DASHBNB", "GALBNB", "AMBBNB", "FETBNB", "FLOWBNB", "WAVESBNB", "SXPBNB", "EGLDBNB", "API3BNB", "ROSEBNB", "EOSBNB", "XTZBNB", "AVAXBNB", "ICPBNB", "SNXBNB", "RENBNB", "XLMBNB", "FTMBNB", "WOOBNB", "KAVABNB", "ZENBNB", "IDBNB", "ONEBNB", "OGNBNB", "ARPABNB", "BCHBNB", "CHZBNB", "MKRBNB", "KLAYBNB", "UNIBNB", "HOOKBNB", "ETCBNB", "LINABNB", "ONTBNB", "ATOMBNB", "BATBNB", "QTUMBNB", "ATABNB", "MINABNB", "SUSHIBNB", "RUNEBNB", "RSRBNB", "ZECBNB", "TLMBNB", "RLCBNB", "ANTBNB", "BLZBNB", "XEMBNB", "BALBNB", "HIGHBNB", "DUSKBNB", "JASMYBNB", "GTCBNB", "XVSBNB", "ANKRBNB", "PHBBNB", "COTIBNB", "XMRBNB", "DOTBNB", "KNCBNB", "OMGBNB", "GMTBNB", "UNFIBNB", "TRBBNB", "BELBNB", "ENJBNB", "AXSBNB", "FILBNB", "ALGOBNB", "DYDXBNB", "LPTBNB", "STXBNB", "YFIBNB", "APEBNB", "IDEXBNB", "BANDBNB", "IMXBNB", "LINKBNB", "OCEANBNB", "ZILBNB", "IOTABNB", "EDUBNB", "FLMBNB", "CELRBNB", "NEARBNB", "ALICEBNB", "XRPBNB", "ICXBNB", "BNXBNB", "CHRBNB", "NKNBNB"]
end

function get_tickers_spot_new(market)
    if cmp(market, "BTC") == 0
        return get_tickers_btc()
    elseif cmp(market, "ETH") == 0
        return get_tickers_eth()
    elseif cmp(market, "BNB") == 0
        return get_tickers_bnb()
    end
    error("invalid symbol")
end

function get_tickers_spot(market)
    sever_time_raw = HTTP.request("GET", "https://fapi.binance.com/fapi/v1/time"; verbose=0)
    sever_time = JSON.parse(String(sever_time_raw.body))["serverTime"]
    url = "https://api.binance.com/api/v3/ticker/price"
    raw = HTTP.request("GET", url; verbose=0)
    json_data = JSON.parse(String(raw.body))
    raw_ticker_list = [ticker["symbol"] for ticker in json_data if cmp(ticker["symbol"][end-2:end], market) == 0]
    return raw_ticker_list
    #=
    result = []
    for ticker in raw_ticker_list
        last_ticker_time = fetch_ohlcv(ticker, "1m", 30,"$(sever_time-3600000)","$(sever_time)","spot")
        if length(last_ticker_time) == 30
            push!(result, ticker)
        end
    end
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    return result
    =#
end

function shortest_distance(ratio, winrate)
    lins = [i / 10000 for i in 0:100000]
    y = [-log(0.99) / (log(1 + 0.01 * i) - log(0.99)) for i in lins]
    least_distance = 100
    for i in 1:100000
        dx = lins[i] - ratio
        dy = y[i] - winrate
        distance = sqrt(dx^2 + dy^2)
        if distance < least_distance
            least_distance = distance
        end
    end
    base_line = -log(0.99) / (log(1 + 0.01 * ratio) - log(0.99))
    if winrate > base_line
        return least_distance
    else
        return -least_distance
    end
end


function get_performance(trade_log, verbose, money=1)
    io = open("log.txt", "a")
    logger = SimpleLogger(io)
    global_logger(logger)

    if length(trade_log) == 0
        return 0, 0
    else
        trade_count = length(trade_log)
    end
    win = []
    lose = []
    for value in trade_log
        if value > 0
            push!(win, value)
        else
            push!(lose, value)
        end
    end
    risk_free = 0.038 / 365
    avg = mean(trade_log)

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

    std_value = std(trade_log, corrected=false)
    avg_w_l_ratio = -1 * avg_win / avg_lose
    win_rate = 100 * length(win) / length(trade_log)
    sharp = (avg - risk_free) / std_value
    sortino = (avg - risk_free) / std_lose
    if avg_w_l_ratio < 0
        total_perform = "Nan"
    else
        total_perform = shortest_distance(avg_w_l_ratio, win_count / trade_count)
    end
    size = (avg - risk_free) / std_value^2
    if verbose == true
        println("총 거래 수 : $(trade_count)")
        println("수익 거래 수 : $(win_count)")
        println("손실 거래 수 : $(length(lose))")
        println("평균 손익률 : $(avg)%")
        println("평균 수익률 : $(avg_win)%")
        println("평균 손실률 : $(avg_lose)%")
        println("평균 손익비 : $(avg_w_l_ratio)")
        println("승 률 : $(win_rate)%")
        println("포지션 사이징 : $(size)")
        println("sharp ratio : $(sharp)%")
        println("sortino ratio : $(sortino)")
        @info("총 거래 수 : $(trade_count)")
        @info("수익 거래 수 : $(win_count)")
        @info("손실 거래 수 : $(length(lose))")
        @info("평균 손익률 : $(avg)%")
        @info("평균 수익률 : $(avg_win)%")
        @info("평균 손실률 : $(avg_lose)%")
        @info("평균 손익비 : $(avg_w_l_ratio)")
        @info("승 률 : $(win_rate)%")
        @info("포지션 사이징 : $(size)")
        @info("sharp ratio : $(sharp)%")
        @info("sortino ratio : $(sortino)")
        if length(lose) != 0
            println("최대 손실 : $(minimum(lose))%")
            @info("최대 손실 : $(minimum(lose))%")
        end
        println(sum(trade_log) * money * 0.01)
        println("$(total_perform)\n")
        @info(sum(trade_log) * money * 0.01)
        @info("$(total_perform)\n")
        @info("")
    end
    flush(io)
    #close(io)
    return total_perform, trade_count
end

function fetch_ohlcv(ticker="BTCUSDT"::String,
    interval="1m"::String,
    limit="605"::String,
    start_time=""::String,
    end_time=""::String,
    option="future"::String)
    if cmp(option, "future") == 0
        base_url = "https://fapi.binance.com/fapi/v1/klines?symbol="
    else
        base_url = "https://api.binance.com/api/v3/klines?symbol="
    end
    if cmp(start_time, "") == 0 || cmp(end_time, "") == 0
        url = "$base_url$ticker&interval=$interval&limit=$limit"
    else
        url = "$base_url$ticker&interval=$interval&limit=$limit&startTime=$start_time&endTime=$end_time"
    end
    raw = HTTP.request("GET", url; verbose=0)
    ohlcv_string = JSON.parse(String(raw.body))
    ohlcv_float = [Array(map(x -> typecasting_support(x), ohlcv)) for ohlcv in ohlcv_string]
end


function typecasting_support(x)
    if typeof(x) == String
        parse(Float32, x)
    else
        x
    end
end


function log_post_processing(filepath::AbstractString)
    file_content = read(filepath, String)
    lines = split(file_content, '\n')
    cleaned_lines = filter(line -> !contains(line, "└ @ Main"), lines)
    cleaned_lines = map(line -> replace(line, "┌ Info: " => ""), cleaned_lines)
    cleaned_content = join(cleaned_lines, '\n')
    write(filepath, cleaned_content)
end


macro catch_errors(expr)
    quote
        try
            $expr
        catch e
            println("Error: ", e)
            sleep(2)
        end
    end
end


function log_source_code(dir, file_name) # @__DIR__, @__FILE__
    io = open("log.txt", "a")
    logger = SimpleLogger(io)
    global_logger(logger)
    file_path = abspath(joinpath(dir, file_name))  # 현재 파일 경로 얻기
    source_code = read(file_path, String)  # 소스코드 읽어오기
    @info "Source code:" source_code  # 로깅하기
    flush(io)
    #close(io)
end

Moving_average(var, n::Int64) = [sum(@view var[i:(i+n-1)]) / n for i in 1:(length(var)-(n-1))]

True_range(ohlcv) = [(i == 1) ? var[3] - var[4] : maximum([var[3] - var[4], abs(var[3] - ohlcv[i-1][5]), abs(var[4] - ohlcv[i-1][5])]) for (i, var) in enumerate(ohlcv)]

function rma(data::Vector{T}, period::Int) where {T}
    alpha = 1 / period # RMA
    # alpha = 2 / (period + 1) # EMA
    ema_values = similar(data, T)
    sma = sum(@view data[1:period]) / period
    ema_values[period] = sma
    @fastmath @simd for i in (period+1):length(data)
        ema_values[i] = (data[i] - ema_values[i-1]) * alpha + ema_values[i-1]
    end
    return ema_values
end

function rsi(data::Vector{T}, period::Int) where {T}
    delta = diff(data)
    gain = [max(delta[i], 0) for i in 1:length(delta)]
    loss = [max(-delta[i], 0) for i in 1:length(delta)]
    avg_gain = rma(gain, period)
    avg_loss = rma(loss, period)
    rs = avg_gain ./ avg_loss
    rsi_values = 100 .- (100 ./ (1 .+ rs))
    return rsi_values
end


###################### [⬆️ public], [⬇️ private] ######################

function get_key(exchange)
    key_ring = Dict("binance" => [ENV["BINANCE_FUTURE_PUB"], ENV["BINANCE_FUTURE_SEC"]],
        "bybit" => [ENV["BYBIT_FUTURE_PUB"], ENV["BYBIT_FUTURE_SEC"]]
    )
    return key_ring[exchange]
end

function get_server_time()
    sever_time_raw = HTTP.request("GET", "https://fapi.binance.com/fapi/v1/time"; verbose=0)
    JSON.parse(String(sever_time_raw.body))["serverTime"]
end

function fetch_available_balance(ticker, exchange="binance")
    pub, sec = get_key(exchange)
    body = "&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://fapi.binance.com/fapi/v2/balance"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("GET", "$url?$body&signature=$signature", headers=headers)
    result = JSON.parse(String(resp.body))
    for i = eachindex(result)
        if cmp(result[i]["asset"], ticker) == 0
            return parse(Float64, result[i]["maxWithdrawAmount"])
        end
    end
end

function cancel_order(ticker, order_id, exchange="binance")
    pub, sec = get_key(exchange)
    body = "symbol=$ticker&orderId=$order_id&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://fapi.binance.com/fapi/v1/order"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("DELETE", "$url?$body&signature=$signature", headers=headers)
    result = JSON.parse(String(resp.body))
end

function create_order(ticker, side, type, quantity, price="0", exchange="binance")
    pub, sec = get_key(exchange)
    cmp(type, "LIMIT") == 0 ? body = "symbol=$ticker&side=$side&type=$type&timeInForce=GTC&quantity=$quantity&price=$price&recvWindow=5000&timestamp=$(get_server_time())" : body = "symbol=$ticker&side=$side&type=$type&quantity=$quantity&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://fapi.binance.com/fapi/v1/order"
    headers = ["X-MBX-APIKEY" => pub]
    try
        resp = HTTP.request("POST", "$url?$body&signature=$signature", headers=headers)
        return true
    catch e
        return e
    end
    # JSON.parse(String(resp.body))
end

function transfer_coin(from, to, coin, amount, exchange="binance")
    pub, sec = get_key(exchange)
    type = 0
    if from == "spot" && to == "futures"
        type = 1
    elseif from == "futures" && to == "spot"
        type = 2
    elseif from == "spot" && to == "coin-m"
        type = 3
    elseif from == "coin-m" && to == "spot"
        type = 4
    else
        error("""Invalid specification: enter valid parameters for "from" and "to", example: from="spot", to="coin-m" """)
    end
    body = "&recvWindow=5000&asset=$(coin)&amount=$(amount)&type=$(type)&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://api.binance.com/sapi/v1/futures/transfer"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("POST", "$url?$body&signature=$signature", headers=headers)
    JSON.parse(String(resp.body))
end

function cancel_all(ticker, exchange="binance")
    pub, sec = get_key(exchange)
    body = "symbol=$ticker&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://fapi.binance.com/fapi/v1/allOpenOrders"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("DELETE", "$url?$body&signature=$signature", headers=headers)
    result = JSON.parse(String(resp.body))
end

function check_order(ticker, orderid, exchange="binance")
    pub, sec = get_key(exchange)
    body = "symbol=$ticker&orderId=$orderid&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://fapi.binance.com/fapi/v1/order"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("GET", "$url?$body&signature=$signature", headers=headers)
    result = JSON.parse(String(resp.body))
end

function fetch_spot_balance(ticker, exchange="binance")
    pub, sec = get_key(exchange)
    body = "recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://api.binance.com/sapi/v3/asset/getUserAsset"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("POST", "$url?$body&signature=$signature", headers=headers)
    json_result = JSON.parse(String(resp.body))
    for dict_ in json_result
        if cmp(dict_["asset"], ticker) == 0
            return parse(Float64, dict_["free"])
        end
    end
end

function create_order_spot(ticker, side, type, quantity, price="0", exchange="binance")
    pub, sec = get_key(exchange)
    cmp(type, "LIMIT") == 0 ? body = "symbol=$ticker&side=$side&type=$type&timeInForce=GTC&quantity=$quantity&price=$price&recvWindow=5000&timestamp=$(get_server_time())" : body = "symbol=$ticker&side=$side&type=$type&quantity=$quantity&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://api.binance.com/api/v3/order"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("POST", "$url?$body&signature=$signature", headers=headers)
    JSON.parse(String(resp.body))
end

