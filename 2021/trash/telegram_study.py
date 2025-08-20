import requests
import json
import datetime
import time
import logging
import telegram
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

"""
telegram.ext.Updater : 텔레그램으로부터 업데이트를 받아서 dispatcher로 전달
CommandHandler : /(start), @(bot name) 의 command
Messagehandler : 텍스트, 상태 업데이트
CallbakcQueryHandler : callbakc 쿼리
"""



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



"""
# command hander
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
"""


def start(update, context):
    # 사용자 name
    t = "안녕"
    context.bot.send_message(chat_id=update.effective_chat.id, text=t)


def echo(update, context):
    t = "안녕?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=t)


"""
def who(bot, update):
    t = "나는 맥주"
    bot.send_message(chat_id = update.message.chat_id, text = t)
"""


def build_box(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i : i + n_cols] for i in range(0, len(buttons), n_colse)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def test(update, context):
    t = "오늘은 날씨가 추우니까"
    context.bot.send_message(chat_id=update.effective_chat.id, text=t)
    time.sleep(0.3)
    t1 = "이건 어때?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=t1)
    time.sleep(0.3)
    # 키보드에 대답 넣기
    show_list = []
    show_list.append(InlineKeyboardButton("좋아", callback_data="좋아"))
    show_list.append(InlineKeyboardButton("별로야", callback_data="별로야"))
    # show_markup = InlineKeyboardMarkup("내 추천이 어떤지 알려줄래?", reply_markup=show_markup)
    show_markup = InlineKeyboardMarkup(show_markup)


# callback
def callback_get(bot, update):
    print("callback")
    if update.callback_query.data == "좋아":
        bot.edit_message_text(
            text="진짜? 고마워",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
        )
    if update.callback_query.data == "별로야":
        bot.edit_message_text(
            text="솔직한 의견이야",
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
        )


def error(bot, update, error):
    logger.warning("update '%s' caused error '%s'", update, error)


def main():
    updater = Updater(token=token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(MessageHandler(Filters.text, echo))
    # dp.add_handler(CommandHandler('who', who))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CallbackQueryHandler(callback_get))

    # dp.add_handler(error)
    updater.start_polling(timeout=3)
    updater.idle()


if __name__ == "__main__":
    updater = Updater(token=token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(MessageHandler(Filters.text, echo))
    # dp.add_handler(CommandHandler('who', who))
    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CallbackQueryHandler(callback_get))

    # dp.add_handler(error)
    updater.start_polling(timeout=3)
    updater.idle()
