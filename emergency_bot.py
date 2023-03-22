import logging

from environs import Env
from telegram import Bot, ParseMode

logger = logging.getLogger(__name__)


def send_alarm(sender: str, text: str, parser: ParseMode.__base__ = None) -> None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    logger.setLevel(logging.DEBUG)

    env = Env()
    env.read_env()
    admin_tg_token = env.str('TELEGRAM_ADMIN_BOT_TOKEN')
    admin_tg_chat_id = env.str('TELEGRAM_ADMIN_CHAT_ID')

    logger.info('Start EMERGENCY Telegram bot.')

    bot = Bot(admin_tg_token)
    bot.send_message(
        chat_id=admin_tg_chat_id,
        text=f'SENDER: {sender}\n\n{text}',
        parse_mode=parser,
    )
