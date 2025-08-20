run(`julia pivot_s2.jl --market future --base_ticker USDT --interval 1h --option double`)

run(`julia pivot_s2.jl --market future --base_ticker USDT --interval 2h --option default`)

run(`julia pivot_s2.jl --market future --base_ticker USDT --interval 4h --option default`)

run(`julia pivot_s2.jl --market future --base_ticker USDT --interval 6h --option double`)

run(`julia pivot_s2.jl --market future --base_ticker USDT --interval 8h --option double`)

run(`julia pivot_s2.jl --market future --base_ticker USDT --interval 12h --option double`)
