include("./../../2022/julia_test/utils.jl")

while true
    wait_next_day()
    sleep(180)
    run(`julia pivot_s2_daily.jl --market future --base_ticker USDT --interval 1h --option double`)
    run(`julia pivot_s2_daily.jl --market future --base_ticker USDT --interval 2h --option default`)
    run(`julia pivot_s2_daily.jl --market future --base_ticker USDT --interval 4h --option default`)
    run(`julia pivot_s2_daily.jl --market future --base_ticker USDT --interval 6h --option double`)
    run(`julia pivot_s2_daily.jl --market future --base_ticker USDT --interval 8h --option double`)
    run(`julia pivot_s2_daily.jl --market future --base_ticker USDT --interval 12h --option double`)
    run(`julia quick_turtle_lower_all.jl --market future --base_ticker USDT --interval 1h`)
    run(`julia quick_turtle_lower_all.jl --market future --base_ticker USDT --interval 2h`)
    run(`julia quick_turtle_lower_all.jl --market future --base_ticker USDT --interval 4h`)
    run(`julia quick_turtle_lower_all.jl --market future --base_ticker USDT --interval 6h`)
    run(`julia quick_turtle_lower_all.jl --market future --base_ticker USDT --interval 8h`)
    run(`julia quick_turtle_lower_all.jl --market future --base_ticker USDT --interval 12h`)
end