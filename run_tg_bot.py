import logging
import time

from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow import detect_intent_text
from bot_logger import BotLogsHandler

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'{user.mention_markdown_v2()}, будем знакомы, я Бот Ботыч\!',
        reply_markup=ForceReply(selective=True),
    )


def send_err(update: Update, context: CallbackContext) -> None:
    logger.error(msg='Exception during message processing:', exc_info=context.error)

    if update.effective_message:
        text = 'К сожалению произошла ошибка в момент обработки сообщения. ' \
               'Мы уже работаем над этой проблемой.'
        update.effective_message.reply_text(text)


def send_msg(update: Update, context: CallbackContext) -> None:
    dialogflow_response = detect_intent_text(
        project_id=dialogflow_project_id,
        session_id=update.message.chat.id,
        text=update.message.text,
    )

    update.message.reply_text(dialogflow_response.fulfillment_text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    logger.setLevel(logging.DEBUG)

    env = Env()
    env.read_env()
    tg_token = env.str('TELEGRAM_BOT_TOKEN')
    tg_bot_name = env.str('TELEGRAM_BOT_NAME')
    dialogflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')
    admin_tg_token = env.str('TELEGRAM_ADMIN_BOT_TOKEN')
    admin_tg_chat_id = env.str('TELEGRAM_ADMIN_CHAT_ID')

    logger.addHandler(BotLogsHandler(
        bot_name=tg_bot_name,
        admin_tg_token=admin_tg_token,
        admin_tg_chat_id=admin_tg_chat_id,
    ))

    logger.info('Start Telegram bot.')

    while True:
        try:
            updater = Updater(tg_token)

            dispatcher = updater.dispatcher
            dispatcher.add_error_handler(send_err)
            dispatcher.add_handler(CommandHandler('start', start))
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_msg))

            updater.start_polling()
            updater.idle()
        except Exception as error:
            logger.exception(error)
            time.sleep(60)
