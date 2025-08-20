"""모든 전략 실행"""

import os
import time
import datetime
import logging
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv
load_dotenv()

def send_log_file(filename):
    token = os.getenv("telegram_token")
    chat_id = os.getenv("telegram_id")
    try:
        # 파일 경로 확인
        file_path = os.path.join(os.getcwd(), filename)
        # 파일 확장자 검증
        if not filename.lower().endswith('.txt'):
            print("Error: Only .txt files are allowed.")
            return False
        # 파일 존재 여부 확인
        if not os.path.exists(file_path):
            print(f"Error: File '{filename}' not found in current directory.")
            return False
        # 봇 생성 및 파일 전송
        bot = Bot(token=token)
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id=chat_id, document=file)
        return True
    except TelegramError as e:
        # bot.send_message(chat_id=os.getenv("telegram_id"), text=f"log file send err(TelegramError) cuz: {e}")
        print(e)
        return False
    except Exception as e:
        # bot.send_message(chat_id=os.getenv("telegram_id"), text=f"log file send err(Exception) cuz: {e}")
        print(e)
        return False


def get_time() -> str:
    result = str(datetime.datetime.utcfromtimestamp(time.time()))
    return result[11:13] + result[14:16]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TIME_VAR = str(datetime.datetime.utcfromtimestamp(time.time()))
date_var = TIME_VAR.split(" ")[0]


if __name__ == "__main__":
    os.system(
        f"nohup julia crypto/binance/ws_launcher.jl >> pivot_binance_{date_var}.txt &"
    )

    os.system(f"nohup python3 crypto/bybit/ws_launcher.py >> q_turtle_{date_var}.txt &")

    while True:
        time.sleep(10)
        if get_time() == "0002" or get_time() == "1202":
            time.sleep(10)
            TIME_VAR = str(datetime.datetime.utcfromtimestamp(time.time()))
            date_var = TIME_VAR.split(" ")[0]

            file_list = os.listdir()
            file_list = [x for x in file_list if x.split(".")[-1] == "txt"]
            for file_name in file_list:
                send_log_file(file_name)
                os.system(f"rm {file_name}")

            logger.info("restart system")
            os.system(
                f"nohup julia crypto/binance/ws_launcher.jl >> pivot_binance_{date_var}.txt &"
            )

            os.system(
                f"nohup python3 crypto/bybit/ws_launcher.py >> q_turtle_{date_var}.txt &"
            )

            time.sleep(60)

            
