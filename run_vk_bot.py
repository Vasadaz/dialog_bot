import logging
import random
import time

import vk_api as vk

from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import detect_intent_text
from bot_logger import BotLogsHandler

logger = logging.getLogger(__name__)


def send_msg(event, vk_api):
    dialogflow_response = detect_intent_text(
        project_id=dialogflow_project_id,
        session_id=event.user_id,
        text=event.text,
        is_fallbac=False,
    )

    if dialogflow_response:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_response,
            random_id=random.randint(1, 1000)
        )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
    logger.setLevel(logging.DEBUG)

    env = Env()
    env.read_env()
    vk_token = env.str('VK_BOT_TOKEN')
    vk_bot_name = env.str('VK_BOT_NAME')
    dialogflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')
    admin_tg_token = env.str('TELEGRAM_ADMIN_BOT_TOKEN')
    admin_tg_chat_id = env.str('TELEGRAM_ADMIN_CHAT_ID')

    logger.addHandler(BotLogsHandler(
        bot_name=vk_bot_name,
        admin_tg_token=admin_tg_token,
        admin_tg_chat_id=admin_tg_chat_id,
    ))

    logger.info('Start VK bot.')

    while True:
        try:
            vk_session = vk.VkApi(token=vk_token)
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    send_msg(event, vk_api)
        except Exception as error:
            logger.exception(error)
            time.sleep(60)
