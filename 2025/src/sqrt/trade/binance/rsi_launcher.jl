using CSV
using DataFrames
using Dates
using Logging
include("../../../utils/utils.jl")


function is_bullish(ohlcv)
    if ohlcv[2] < ohlcv[5]
        return true
    elseif ohlcv[2] > ohlcv[5]
        return false
    end
    return nothing
end

function check_candle_color(current_ohlcv, prev_ohlcv)
    # 현재 캔들은 양봉
    if is_bullish(current_ohlcv) == true
        # D-1 캔들은 음봉
        if is_bullish(prev_ohlcv) == false
            return true
        end
    end
    return false
end

function find_prev_low_rsi(partial_ohlcvs, partial_rsi, min_rsi)
    if minimum(partial_rsi) + 5 < min_rsi
        return true
    end
    return false
end



function main()
    all_qty = fetch_all_open_orders()

    for ticker in ticker_list
        ohlcvs = fetch_ohlcv(ticker, time_frame, 250)
        close_data = [x[5] for x in ohlcvs]
        rsi_var = rsi(close_data; length=14, scalar=100.0, drift=1, offset=0)

        if check_candle_color(ohlcvs[end], ohlcvs[end-1])
            if rsi_var[end-1] < 27
                if find_prev_low_rsi(ohlcvs[end-201:end-1], rsi_var[end-201:end-1], rsi_var[end-1])
                    @info("\n$(ticker) entry\n")
                    trade_amount, price = get_amount(ticker, order_size * ticker_dict[ticker])
                    response = create_order(ticker, "BUY", "MARKET", trade_amount, price)
                    if response != true
                        msg = "R entry_side error $(ticker) $(response)"
                        @info msg
                        # telegram_send(msg)
                    else
                        ticker_dict[ticker] += 1
                        position_size_dict[ticker] += parse(Float32, trade_amount)
                    end
                end
            end
        end

        if rsi_var[end] > 50
            trade_amount = fetch_open_qty(ticker, all_qty)
            if trade_amount != false
                _, price = get_amount(ticker, order_size)
                if position_size_dict[ticker] == 0.0
                    continue
                end
                response = create_order(ticker, "SELL", "MARKET", min(trade_amount,position_size_dict[ticker]), price)
                @info("\n$(ticker) exit\n")
                if response != true
                    msg = "R exit_side error $(ticker) $(response)"
                    @info msg
                    # telegram_send(msg)
                else
                    ticker_dict[ticker] = 1
                    var::Float64 = 0.0
                    position_size_dict[ticker] = var
                end
            end
        end
    end
end


# const ticker_list = get_tickers_listed_over_1year()
const order_size::Int64 = 600
const time_frame::String = "15m"
# const ticker_list = ["1INCHUSDT", "ACEUSDT", "ACHUSDT", "ADAUSDT", "AGLDUSDT", "AIUSDT", "ALGOUSDT", "ALPHAUSDT", "ALTUSDT", "ANKRUSDT", "APEUSDT", "API3USDT", "APTUSDT", "ARKMUSDT", "ARKUSDT", "ARPAUSDT", "ARUSDT", "ATAUSDT", "ATOMUSDT", "AVAXUSDT", "AXLUSDT", "BAKEUSDT", "BANDUSDT", "BCHUSDT", "BEAMXUSDT", "BELUSDT", "BIGTIMEUSDT", "BLURUSDT", "BNTUSDT", "BOMEUSDT", "BTCUSDT", "C98USDT", "CELOUSDT", "CELRUSDT", "CHRUSDT", "CHZUSDT", "CKBUSDT", "COMPUSDT", "COTIUSDT", "CRVUSDT", "CTSIUSDT", "CYBERUSDT", "DASHUSDT", "DENTUSDT", "DOGEUSDT", "DOTUSDT", "DUSKUSDT", "DYMUSDT", "EDUUSDT", "EGLDUSDT", "ENAUSDT", "ENSUSDT", "ETCUSDT", "ETHUSDT", "FETUSDT", "FLMUSDT", "FLOWUSDT", "GALAUSDT", "GLMUSDT", "GRTUSDT", "GTCUSDT", "HBARUSDT", "HFTUSDT", "HIGHUSDT", "HOOKUSDT", "HOTUSDT", "ICPUSDT", "ICXUSDT", "IDUSDT", "ILVUSDT", "IMXUSDT", "IOSTUSDT", "IOTAUSDT", "IOTXUSDT", "JASMYUSDT", "JOEUSDT", "JTOUSDT", "JUPUSDT", "KAVAUSDT", "KSMUSDT", "LDOUSDT", "LINKUSDT", "LPTUSDT", "LQTYUSDT", "LRCUSDT", "LSKUSDT", "LTCUSDT", "MAGICUSDT", "MANAUSDT", "MANTAUSDT", "MASKUSDT", "MAVUSDT", "MEMEUSDT", "MINAUSDT", "MKRUSDT", "MTLUSDT", "NEOUSDT", "NFPUSDT", "NKNUSDT", "NMRUSDT", "NOTUSDT", "NTRNUSDT", "OGNUSDT", "OMUSDT", "ONDOUSDT", "ONEUSDT", "ONGUSDT", "OPUSDT", "OXTUSDT", "PENDLEUSDT", "PEOPLEUSDT", "PIXELUSDT", "PORTALUSDT", "POWRUSDT", "PYTHUSDT", "QNTUSDT", "QTUMUSDT", "REZUSDT", "RLCUSDT", "RONINUSDT", "ROSEUSDT", "RSRUSDT", "RVNUSDT", "SANDUSDT", "SFPUSDT", "SKLUSDT", "SNXUSDT", "SOLUSDT", "SPELLUSDT", "STEEMUSDT", "STXUSDT", "SUIUSDT", "SUPERUSDT", "SUSHIUSDT", "SXPUSDT", "TAOUSDT", "THETAUSDT", "TLMUSDT", "TONUSDT", "TRBUSDT", "TRUUSDT", "TRXUSDT", "TUSDT", "TWTUSDT", "UMAUSDT", "UNIUSDT", "USTCUSDT", "VANRYUSDT", "VETUSDT", "WAXPUSDT", "WIFUSDT", "WLDUSDT", "WUSDT", "XAIUSDT", "XLMUSDT", "XMRUSDT", "XRPUSDT", "XTZUSDT", "XVGUSDT", "XVSUSDT", "YFIUSDT", "YGGUSDT", "ZECUSDT", "ZILUSDT", "ZRXUSDT"]
const ticker_list = ["ACHUSDT", "ALICEUSDT", "ALTUSDT", "ANKRUSDT", "API3USDT", "ARPAUSDT", "ARUSDT", "ATAUSDT", "BLURUSDT", "DUSKUSDT", "EDUUSDT", "ENSUSDT", "ETCUSDT", "FETUSDT", "HOTUSDT", "ICPUSDT", "ICXUSDT", "IOTAUSDT", "JTOUSDT", "JUPUSDT", "MINAUSDT", "NFPUSDT", "NOTUSDT", "OGNUSDT", "ONDOUSDT", "ONGUSDT", "ROSEUSDT", "RVNUSDT", "STEEMUSDT", "SUIUSDT", "SUPERUSDT", "TAOUSDT", "TWTUSDT", "UMAUSDT", "VANRYUSDT", "VETUSDT", "WIFUSDT", "WLDUSDT", "XAIUSDT", "XLMUSDT", "XTZUSDT", "ZRXUSDT"]
const ticker_dict = Dict()
for ticker in ticker_list
    ticker_dict[ticker] = 1
end

const position_size_dict = Dict()
for ticker in ticker_list
    var::Float32 = 0.0
    position_size_dict[ticker] = var
end


while true
    sleep(0.3)
    utcurrentime = now(Dates.UTC)
    min = parse(Int8, Dates.format(utcurrentime, "MM"))
    if min % 30 != 29
        continue
    end
    seconds = parse(Int8, Dates.format(now(Dates.UTC), "SS"))
    if seconds != 45
        continue
    end

    @info("START : $(Dates.now())")
    main()
    @info("FINISH : $(Dates.now())")

    flush(stdout)
    flush(stderr)
    sleep(60)
end

