import time
import telegram


def telegram_send(data):
    bot = telegram.Bot(token=my_token)
    if type(data) != "str":
        data = str(data)
    while 1:
        try:
            bot.send_message(chat_id=801167350, text=data)
            time.sleep(3)
            return None
        except:
            continue


telegram_send("123")
