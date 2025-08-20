using Dates

function do_something()
    for i=1:10
        sleep(i)
    end
end

tasks = Task[]

push!(tasks, @async do_something())
push!(tasks, @async do_something())
push!(tasks, @async do_something())

while !all(istaskdone, tasks)
    println("Tasks are still running...")
    sleep(1)
end

println("done...?")



