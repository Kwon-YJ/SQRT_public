# println("hello world")


using Dates


function telegram_send(data)
   chat_id = "801167350"
   tg = TelegramClient(token, chat_id = chat_id)
   while true
      try
         sendMessage(text  = data)
      catch
         sleep(2)
         continue
      end
end


#=
def telegram_send(data):
    bot = telegram.Bot(token = my_token)
    if type(data) != 'str':
        data = str(data)
    while(1):
        try:
            bot.send_message(chat_id = 801167350, text = data)
            time.sleep(3)
            return None
        except:
            continue
=#




exit()
###################
###################



using Base.Threads
using Dates




time_ = now(Dates.UTC)


a = rand(100000000)  # Create array of random numbers
p = zeros(nthreads())  # Allocate a partial sum for each thread
# Threads macro splits the iterations of array `a` evenly among threads
@threads for x in a
   p[threadid()] += x  # Compute partial sums for each thread
end
s = sum(p)  # Compute the total sum
println(s)

println(now(Dates.UTC) - time_)