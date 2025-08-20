


using Logging
# io = open("log.txt", "w+")
io = open("log.txt", "a")
logger = SimpleLogger(io)
global_logger(logger)
@info("전역 로그 메시지")
@info("전역 로그 메시지")
@info("전역 로그 메시지")
@info("전역 로그 메시지")
flush(io)
close(io)



function remove_main_string(filepath::AbstractString)
    file_content = read(filepath, String)
    lines = split(file_content, '\n')
    cleaned_lines = filter(line -> !contains(line, "└ @ Main"), lines)
    cleaned_content = join(cleaned_lines, '\n')
    write(filepath, cleaned_content)
end


remove_main_string("log.txt")


using Logging
# io = open("log.txt", "w+")
io = open("log.txt", "a")
logger = SimpleLogger(io)
global_logger(logger)
file_path = abspath(joinpath(@__DIR__, @__FILE__))  # 현재 파일 경로 얻기
source_code = read(file_path, String)  # 소스코드 읽어오기
@info "Source code:" source_code  # 로깅하기
flush(io)
close(io)






