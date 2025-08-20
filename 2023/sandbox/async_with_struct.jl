mutable struct data_struct
    ordered::Vector{String}
end

function del_world(struct_data)
    sleep(10)
    deleteat!(struct_data.ordered, findall(x->x=="world",struct_data.ordered))
end

temp_ = data_struct(["hello", "world"])

@async del_world(temp_)

while true
    sleep(0.5)
    println(temp_.ordered)
end


