using Random

a = []
Threads.@threads for i=1:10^5
    push!(a, rand(1))
end
println(length(a))

a = []
for i=1:10^6
    @async push!(a, rand(1))
end
sleep(10)
println(length(a))