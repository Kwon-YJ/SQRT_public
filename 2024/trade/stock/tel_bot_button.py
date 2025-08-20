from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import requests


from tel_bot_module import *




def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("잔고 확인", callback_data="1"),
            InlineKeyboardButton("삼성전자 1주 매수", callback_data="2"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("버튼을 선택하세요:", reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == "1":
        response = get_balance()
        query.edit_message_text(text=f"버튼 1을 눌렀습니다. 서버 응답: {response}")
    elif query.data == "2":
        response = requests.get(
            "https://fapi.binance.com/fapi/v1/depth?symbol=BTCUSDT&limit=5"
        )
        response = buy_samsung_1_qty()
        query.edit_message_text(text=f"버튼 2를 눌렀습니다. 서버 응답: {response}")


def main() -> None:
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
