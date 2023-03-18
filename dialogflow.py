#!/usr/bin/env python

import datetime

from environs import Env

from google.cloud import api_keys_v2
from google.cloud import dialogflow

env = Env()
env.read_env()

DIALOGFLOW_PROJECT_ID = env.str('DIALOGFLOW_PROJECT_ID')


def create_api_key() -> api_keys_v2.Key:
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f'API key {datetime.datetime.now().timestamp()}'

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f'projects/{DIALOGFLOW_PROJECT_ID}/locations/global'
    request.key = key

    response = client.create_key(request=request).result()

    return response


def create_intent(intent_name: str, questions: list, answers: list):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(DIALOGFLOW_PROJECT_ID)

    training_phrases = []
    for question in questions:
        part = dialogflow.Intent.TrainingPhrase.Part(text=question)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=answers)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=intent_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    intents_client.create_intent(request={"parent": parent, "intent": intent})


def detect_intent_text(
        session_id: str,
        text: str,
        language_code: str = 'RU-ru',
        is_fallbac: bool = True,
) -> str | None:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={'session': session, 'query_input': query_input})

    if response.query_result.intent.is_fallback and not is_fallbac:
        return None
    else:
        return response.query_result.fulfillment_text
