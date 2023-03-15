import json

from environs import Env

from run_dialogflow import create_intent


INTENTS_FILE_NAME = 'intents.json'


if __name__ == '__main__':
    env = Env()
    env.read_env()
    dialogflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')

    with open(INTENTS_FILE_NAME, 'r') as file:
        intents = json.load(file)

    for intent_name, phrases in intents.items():
        create_intent(
            project_id=dialogflow_project_id,
            intent_name=intent_name,
            questions=phrases['questions'],
            answers=phrases['answers']
        )
