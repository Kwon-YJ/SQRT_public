using JSON


config = open("config.json") do file
    JSON.parse(read(file, String))
end


println(config["spot"])


