include("./../../2022/julia_test/utils.jl")


interval = 3
time_frame = "12h"

ethbtc = fetch_ohlcv("ETHBTC", time_frame, interval, "", "", "spot")
ethbtc = map(x->x[5], ethbtc)
ethbtc_long_earn = 100(ethbtc[end-1] / ethbtc[1] - 1)
println(ethbtc_long_earn)

ethusd = fetch_ohlcv("ETHUSDT", time_frame, interval, "", "", "spot")
ethusd = map(x->x[5], ethusd)
ethusd_long_earn = 100(ethusd[end-1] / ethusd[1] - 1)


btcusd = fetch_ohlcv("BTCUSDT", time_frame, interval, "", "", "spot")
btcusd = map(x->x[5], btcusd)
btcusd_short_earn = -100(btcusd[end-1] / btcusd[1] - 1)

println(ethusd_long_earn + btcusd_short_earn)

