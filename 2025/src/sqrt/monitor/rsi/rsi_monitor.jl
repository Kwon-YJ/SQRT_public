using CSV
using DataFrames
using Dates
using Logging
include("../../utils/utils.jl")


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



function main(time_frame::String)
    all_qty = fetch_all_open_orders()

    for ticker in ticker_list
        ohlcvs = fetch_ohlcv(ticker, time_frame, 250)
        close_data = [x[5] for x in ohlcvs]
        rsi_var = rsi(close_data; length=14, scalar=100.0, drift=1, offset=0)

        if check_candle_color(ohlcvs[end], ohlcvs[end-1])
            if rsi_var[end-1] < 30
                if find_prev_low_rsi(ohlcvs[end-201:end-1], rsi_var[end-201:end-1], rsi_var[end-1])
                    @info("\n$(ticker) entry\n")
                    trade_amount, price = get_amount(ticker, order_size)
                    # response = create_order(ticker, "BUY", "MARKET", trade_amount, price)
                    msg = "$(ticker) BUY MARKET $(trade_amount) $(price)"
                    telegram_send(msg)
                    if response != true
                        msg = "R entry_side error $(ticker) $(response)"
                        @info msg
                        # telegram_send(msg)
                    end
                end
            end
        end

        if rsi_var[end] > 45
            trade_amount = fetch_open_qty(ticker, all_qty)
            if trade_amount != false
                _, price = get_amount(ticker, order_size)
                # response = create_order(ticker, "SELL", "MARKET", trade_amount, price)
                @info("\n$(ticker) exit\n")
                msg = "$(ticker) SELL MARKET $(trade_amount) $(price)"
                telegram_send(msg)
                if response != true
                    msg = "R exit_side error $(ticker) $(response)"
                    @info msg
                    # telegram_send(msg)
                end
            end
        end
    end
end



const ticker_list = ["1INCHUSDT", "1000SATSUSDT", "AAVEUSDT", "ACEUSDT", "ACHUSDT", "ADAUSDT", "AEVOUSDT", "AGLDUSDT", "AIUSDT", "ALGOUSDT", "ALICEUSDT", "ALPHAUSDT", "ALTUSDT", "ANKRUSDT", "APEUSDT", "API3USDT", "APTUSDT", "ARBUSDT", "ARKMUSDT", "ARKUSDT", "ARPAUSDT", "ARUSDT", "ASTRUSDT", "ATAUSDT", "ATOMUSDT", "AUCTIONUSDT", "AVAXUSDT", "AXLUSDT", "AXSUSDT", "BAKEUSDT", "BANDUSDT", "BATUSDT", "BBUSDT", "BCHUSDT", "BEAMXUSDT", "BELUSDT", "BICOUSDT", "BIGTIMEUSDT", "BLURUSDT", "BNBUSDT", "BNTUSDT", "BOMEUSDT", "BTCUSDT", "C98USDT", "CAKEUSDT", "CELOUSDT", "CELRUSDT", "CFXUSDT", "CHRUSDT", "CHZUSDT", "CKBUSDT", "COMPUSDT", "COTIUSDT", "CRVUSDT", "CTSIUSDT", "CYBERUSDT", "DASHUSDT", "DENTUSDT", "DOGEUSDT", "DOTUSDT", "DUSKUSDT", "DYDXUSDT", "DYMUSDT", "EDUUSDT", "EGLDUSDT", "ENAUSDT", "ENJUSDT", "ENSUSDT", "ETCUSDT", "ETHFIUSDT", "ETHUSDT", "FETUSDT", "FILUSDT", "FLMUSDT", "FLOWUSDT", "FXSUSDT", "GALAUSDT", "GASUSDT", "GLMUSDT", "GMTUSDT", "GMXUSDT", "GRTUSDT", "GTCUSDT", "HBARUSDT", "HFTUSDT", "HIFIUSDT", "HIGHUSDT", "HOOKUSDT", "HOTUSDT", "ICPUSDT", "ICXUSDT", "IDUSDT", "ILVUSDT", "IMXUSDT", "INJUSDT", "IOSTUSDT", "IOTAUSDT", "IOTXUSDT", "JASMYUSDT", "JOEUSDT", "JTOUSDT", "JUPUSDT", "KAVAUSDT", "KNCUSDT", "KSMUSDT", "LDOUSDT", "LINKUSDT", "LPTUSDT", "LQTYUSDT", "LRCUSDT", "LSKUSDT", "LTCUSDT", "MAGICUSDT", "MANAUSDT", "MANTAUSDT", "MASKUSDT", "MAVUSDT", "MEMEUSDT", "METISUSDT", "MINAUSDT", "MKRUSDT", "MOVRUSDT", "MTLUSDT", "NEARUSDT", "NEOUSDT", "NFPUSDT", "NKNUSDT", "NMRUSDT", "NOTUSDT", "NTRNUSDT", "OGNUSDT", "OMNIUSDT", "OMUSDT", "ONDOUSDT", "ONEUSDT", "ONGUSDT", "ONTUSDT", "OPUSDT", "ORDIUSDT", "OXTUSDT", "PENDLEUSDT", "PEOPLEUSDT", "PHBUSDT", "PIXELUSDT", "POLYXUSDT", "PORTALUSDT", "POWRUSDT", "PYTHUSDT", "QNTUSDT", "QTUMUSDT", "RDNTUSDT", "REZUSDT", "RIFUSDT", "RLCUSDT", "RONINUSDT", "ROSEUSDT", "RSRUSDT", "RVNUSDT", "SAGAUSDT", "SANDUSDT", "SEIUSDT", "SFPUSDT", "SKLUSDT", "SNXUSDT", "SOLUSDT", "SPELLUSDT", "SSVUSDT", "STEEMUSDT", "STGUSDT", "STORJUSDT", "STRKUSDT", "STXUSDT", "SUIUSDT", "SUPERUSDT", "SXPUSDT", "TAOUSDT", "THETAUSDT", "TIAUSDT", "TLMUSDT", "TNSRUSDT", "TONUSDT", "TRBUSDT", "TRUUSDT", "TRXUSDT", "TUSDT", "TWTUSDT", "UMAUSDT", "UNIUSDT", "USTCUSDT", "VANRYUSDT", "VETUSDT", "WAXPUSDT", "WIFUSDT", "WLDUSDT", "WOOUSDT", "WUSDT", "XAIUSDT", "XLMUSDT", "XMRUSDT", "XRPUSDT", "XTZUSDT", "XVGUSDT", "XVSUSDT", "YFIUSDT", "YGGUSDT", "ZECUSDT", "ZENUSDT", "ZILUSDT", "ZRXUSDT"]




while true
    sleep(0.3)
    utcurrentime = now(Dates.UTC)

    mins = parse(Int8, Dates.format(now(Dates.UTC), "MM"))
    if mins != 58
        continue
    end


    hours = parse(Int8, Dates.format(utcurrentime, "HH"))

    if hours + 1 % 2 # 2 hours
        @info("START : $(Dates.now())")
        main("2h")
        @info("FINISH : $(Dates.now())")
    end


    if hours + 1 % 4 # 4 hours
        @info("START : $(Dates.now())")
        main("4h")
        @info("FINISH : $(Dates.now())")
    end


    if hours + 1 % 6 # 6 hours
        @info("START : $(Dates.now())")
        main("6h")
        @info("FINISH : $(Dates.now())")
    end


    if hours + 1 % 8 # 8 hours
        @info("START : $(Dates.now())")
        main("8h")
        @info("FINISH : $(Dates.now())")
    end


    if hours + 1 % 12 # 12 hours
        @info("START : $(Dates.now())")
        main("12h")
        @info("FINISH : $(Dates.now())")
    end


    if hours == 23  # 1 day
        @info("START : $(Dates.now())")
        main("1d")
        @info("FINISH : $(Dates.now())")
    end


    flush(stdout)
    flush(stderr)
    sleep(120)
end








# main("2h")


# main("4h")


# main("6h")


# main("8h")


# main("12h")


# main("1d")


