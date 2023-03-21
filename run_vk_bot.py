import logging
import random
import time

import vk_api as vk

from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow import create_api_key, detect_intent_text
from emergency_bot import send_alarm

logger = logging.getLogger(__name__)


class VKLogsHandler(logging.Handler):
    def __init__(self, bot_name):
        super().__init__()
        self.bot_name = bot_name

    def emit(self, record):
        log_entry = self.format(record)
        send_alarm(sender=self.bot_name, text=log_entry)


def send_msg(event, vk_api):
    create_api_key()

    dialogflow_response = detect_intent_text(
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

    logger.addHandler(VKLogsHandler(vk_bot_name))
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
