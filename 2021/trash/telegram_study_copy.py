# buttons_bot.py
import time
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler


updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def cmd_task_buttons(update, context):
    task_buttons = [
        [
            InlineKeyboardButton("1.네이버 뉴스", callback_data=1),
            InlineKeyboardButton("2.직방 매물", callback_data=2),
        ],
        [InlineKeyboardButton("3.취소", callback_data=3)],
    ]

    reply_markup = InlineKeyboardMarkup(task_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="작업을 선택해주세요.",
        reply_markup=reply_markup,
    )


def cb_button(update, context):
    query = update.callback_query
    data = query.data

    context.bot.send_chat_action(
        chat_id=update.effective_user.id, action=ChatAction.TYPING
    )
    context.bot.edit_message_text(
        text="[{}] 작업을 완료하였습니다.".format(data),
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
    )


task_buttons_handler = CommandHandler("tasks", cmd_task_buttons)
button_callback_handler = CallbackQueryHandler(cb_button)

dispatcher.add_handler(task_buttons_handler)
dispatcher.add_handler(button_callback_handler)

updater.start_polling()
updater.idle()

updater.stop_polling()
print("123")
