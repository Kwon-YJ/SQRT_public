using ODBC
using DBInterface
using DataFrames


function create_crypto_table(conn_master, db_name::String, table_name::String)
    conn = ODBC.Connection("Driver={ODBC Driver 17 for SQL Server};Server=DESKTOP-S037THB\\SQLEXPRESS;Database=$(db_name);Trusted_Connection=yes;")

    df_tables = DBInterface.execute(conn, "select * from information_schema.tables;") |> DataFrame
    
    if !(table_name in df_tables[!, :TABLE_NAME])
        try
            DBInterface.execute(conn,
                                "SELECT * INTO $(table_name) FROM crypto_example_table WHERE 1=2;"
                                )
        catch e
            error("Unable to create table $table_name")
        end
    else
        @info("Table $table_name already exists!")
    end
    return conn
end




function add_to_crypto_table(conn, db_name::String, table_name::String, df_input::DataFrame)
    conn = ODBC.Connection("Driver={ODBC Driver 17 for SQL Server};Server=DESKTOP-S037THB\\SQLEXPRESS;Database=$(db_name);Trusted_Connection=yes;")
    stmt = 
    try
        DBInterface.prepare(conn, "INSERT INTO $(table_name) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    catch
        error("Unable to prepare statement")
    end

    try
        DBInterface.executemany(stmt,
                                (
                                  df_input[!, 1],
                                  df_input[!, 2],
                                  df_input[!, 3],
                                  df_input[!, 4],
                                  df_input[!, 5],
                                  df_input[!, 6],
                                  df_input[!, 7],
                                  df_input[!, 8],
                                  df_input[!, 9],
                                  df_input[!, 10],
                                  df_input[!, 11],
                                  df_input[!, 12]
                                )
                                )
    catch
        error("Unable to execute multiple statements")
    finally
        DBInterface.close!(stmt)
        DBInterface.close!(conn)
    end
    return nothing
end



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



function fetch_crypto_df()
    btcusdt_ohlcv = fetch_ohlcv()
    time_list = []
    open_list = []
    high_list = []
    low_list = []
    close_list = []
    volume_list = []
    close_time_list = []
    quote_asset_vol_list = []
    num_of_trades_list = []
    taker_buy_base_vol_list = []
    taker_buy_quote_vol_list = []
    ignore_list = []

    for ohlcv in btcusdt_ohlcv
        time, open, high, low, close, volume, close_time, quote_asset_vol, num_of_trades, taker_buy_base_vol, taker_buy_quote_vol, ignore = ohlcv
        push!(time_list, time)
        push!(open_list, open)
        push!(high_list, high)
        push!(low_list, low)
        push!(close_list, close)
        push!(volume_list, volume)
        push!(close_time_list, close_time)
        push!(quote_asset_vol_list, quote_asset_vol)
        push!(num_of_trades_list, num_of_trades)
        push!(taker_buy_base_vol_list, taker_buy_base_vol)
        push!(taker_buy_quote_vol_list, taker_buy_quote_vol)
        push!(ignore_list, ignore)
    end

    btcusdt_df = DataFrame(
        "time" => time_list,
        "open" => open_list,
        "high" => high_list,
        "low" => low_list,
        "close" => close_list,
        "volume" => volume_list,
        "close_time" => close_time_list,
        "quote_asset_vol" => quote_asset_vol_list,
        "num_of_trades" => num_of_trades_list,
        "taker_buy_base_vol" => taker_buy_base_vol_list,
        "taker_buy_quote_vol" => taker_buy_quote_vol_list,
        "ignore" => ignore_list
    )

    return btcusdt_df
end


# create_crypto_table(conn, "BinanceDB", "BTCUSDT_1m")

# add_to_crypto_table(conn, "BinanceDB", "BTCUSDT", btcusdt_df)

function main()
    conn = ODBC.Connection("Driver={ODBC Driver 17 for SQL Server};Server=DESKTOP-S037THB\\SQLEXPRESS;Database=master;Trusted_Connection=yes;")
    add_to_crypto_table(conn, "BinanceDB", "BTCUSDT_1m", fetch_crypto_df())
end

main()

