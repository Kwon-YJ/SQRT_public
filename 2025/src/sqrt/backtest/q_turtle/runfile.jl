# julia --threads 24 runfile.jl

@time begin
    include("quick_turtle_lower_2h_plot_module.jl")
    include("quick_turtle_lower_2h_plot_module2.jl")

    include("quick_turtle_lower_4h_plot_module.jl")
    include("quick_turtle_lower_4h_plot_module2.jl")

    include("quick_turtle_lower_6h_plot_module.jl")
    include("quick_turtle_lower_6h_plot_module2.jl")

    include("quick_turtle_lower_8h_plot_module.jl")
    include("quick_turtle_lower_8h_plot_module2.jl")

    include("quick_turtle_lower_12h_plot_module.jl")
    include("quick_turtle_lower_12h_plot_module2.jl")

    include("quick_turtle_lower_1h_plot_module.jl")
    include("quick_turtle_lower_1h_plot_module2.jl")
end

