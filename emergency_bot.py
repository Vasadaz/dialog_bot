from environs import Env
from telegram import Bot


def send_alarm(sender: str, text: str, parser=None) -> None:
    env = Env()
    env.read_env()
    admin_tg_token = env.str('TELEGRAM_ADMIN_BOT_TOKEN')
    admin_tg_chat_id = env.str('TELEGRAM_ADMIN_CHAT_ID')

    bot = Bot(admin_tg_token)
    bot.send_message(
        chat_id=admin_tg_chat_id,
        text=f'SENDER: {sender}\n\n{text}',
        parse_mode=parser
    )
