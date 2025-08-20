all_csv_name = readdir("fx_data")

csv_list_1 = all_csv_name[1:556]


csv_list_2 = all_csv_name[557:end]

@async begin
    for ticker in csv_list_1
        run(`pypy3 euro816_grid_csv.py --file_name $(ticker)`)
    end
end



for ticker in csv_list_2
    run(`pypy3 euro816_grid_csv.py --file_name $(ticker)`)
end



sleep(86400)