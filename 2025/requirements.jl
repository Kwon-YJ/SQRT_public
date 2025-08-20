ENV["JULIA_SSL_CA_ROOTS_PATH"] = ""

using Pkg
Pkg.add("GLM")
Pkg.add("DataFrames")
Pkg.add("FileIO")
Pkg.add("HTTP")
Pkg.add("JSON")
Pkg.add("Statistics")
Pkg.add("Telegram")
Pkg.add("Nettle")
Pkg.add("BenchmarkTools")
Pkg.add("Formatting")
Pkg.add("Logging")
Pkg.add("ArgParse")
Pkg.add("WebSockets")
Pkg.add("CSV")
Pkg.add("DotEnv")
Pkg.add("ODBC")
Pkg.add("DBInterface")
Pkg.add("YAML")
Pkg.add("JSON3")
Pkg.add("Dates")
Pkg.add("GR")
Pkg.add("LaTeXStrings")
Pkg.add("Arrow")
Pkg.add("Tables")
Pkg.add("Plots")

Pkg.add(PackageSpec(url="https://github.com/DennisRutjes/Binance.jl", rev="master"))



