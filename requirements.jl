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
Pkg.add(PackageSpec(url="https://github.com/DennisRutjes/Binance.jl",rev="master"))
Pkg.add("WebSockets")
Pkg.add("CSV")

# packages=["HTTP","JSON","Dates","DataFrames","GR","PyPlot","PyCall","LaTeXStrings"]
packages=["HTTP","JSON","Dates","DataFrames","GR","LaTeXStrings"]
for package in packages
    if get(Pkg.installed(),package,-1) == -1
        Pkg.add(package)
    end
end