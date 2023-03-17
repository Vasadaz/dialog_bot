import random

import vk_api as vk

from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType
from run_dialogflow import create_api_key, detect_intent_text


def send_msg(event, vk_api):
    env = Env()
    env.read_env()

    dialogflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')

    create_api_key(dialogflow_project_id)

    dialogflow_response = detect_intent_text(
        project_id=dialogflow_project_id,
        session_id=event.user_id,
        text=event.text,
    )

    vk_api.messages.send(
        user_id=event.user_id,
        message=dialogflow_response,
        random_id=random.randint(1, 1000)
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()

    vk_token = env.str('VK_BOT_TOKEN')

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_msg(event, vk_api)
