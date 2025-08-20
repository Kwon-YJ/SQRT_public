using Plots

x = range(1, 2, length=100)


y1 = sin.(x)
y2 = cos.(x)
plot(x, [y1 y2])

println(x)

println(y1)

println(y2)


savefig("myplot.png")