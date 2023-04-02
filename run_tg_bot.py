import html
import json
import logging
import time
import traceback

from environs import Env
from telegram import Update, ForceReply, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow import create_api_key, detect_intent_text
from emergency_bot import send_alarm

logger = logging.getLogger(__name__)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot_name):
        super().__init__()
        self.bot_name = bot_name

    def emit(self, record):
        log_entry = self.format(record)
        send_alarm(sender=self.bot_name, text=log_entry)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'{user.mention_markdown_v2()}, будем знакомы, я Бот Ботыч\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Бот написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org')


def send_err(update: Update, context: CallbackContext) -> None:
    logger.error(msg='Exception during message processing:', exc_info=context.error)

    if update.effective_message:
        text = 'К сожалению произошла ошибка в момент обработки сообщения. ' \
               'Мы уже работаем над этой проблемой.'
        update.effective_message.reply_text(text)

    traceback_steps = ''.join(traceback.format_exception(None, context.error, context.error.__traceback__))
    update_str = update.to_dict() if isinstance(update, Update) else str(update)

    message = (
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>\n\n'
        f'{traceback_steps}'
    )

    send_alarm(sender=context.bot.name, text=message, parser=ParseMode.HTML)


def send_msg(update: Update, context: CallbackContext) -> None:
    create_api_key()

    dialogflow_response = detect_intent_text(
        session_id=update.message.chat.id,
        text=update.message.text,
    )

    update.message.reply_text(dialogflow_response)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    logger.setLevel(logging.DEBUG)

    env = Env()
    env.read_env()
    tg_token = env.str('TELEGRAM_BOT_TOKEN')
    tg_bot_name = env.str('TELEGRAM_BOT_NAME')

    logger.addHandler(TelegramLogsHandler(tg_bot_name))
    logger.info('Start Telegram bot.')

    while True:
        try:
            updater = Updater(tg_token)

            dispatcher = updater.dispatcher
            dispatcher.add_error_handler(send_err)
            dispatcher.add_handler(CommandHandler('start', start))
            dispatcher.add_handler(CommandHandler('help', help_command))
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_msg))

            updater.start_polling()
            updater.idle()
        except Exception as error:
            logger.exception(error)
            time.sleep(60)
