#!/usr/bin/env python

import datetime

from environs import Env

from google.cloud import api_keys_v2
from google.cloud import dialogflow


def create_api_key(project_id: str) -> api_keys_v2.Key:
    client = api_keys_v2.ApiKeysClient()

    key = api_keys_v2.Key()
    key.display_name = f'API key {datetime.datetime.now().timestamp()}'

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f'projects/{project_id}/locations/global'
    request.key = key

    response = client.create_key(request=request).result()

    print(f'Successfully created an API key: {response.name}')
    print(response)

    return response


def create_intent(project_id: str, intent_name: str, questions: list, answers: list):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for question in questions:
        part = dialogflow.Intent.TrainingPhrase.Part(text=question)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=answers)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=intent_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    response = intents_client.create_intent(request={"parent": parent, "intent": intent})

    print("Intent created: {}".format(response))


def detect_intent_text(
        project_id: str,
        session_id: str,
        text: str,
        language_code: str = 'RU-ru',
        is_fallbac: bool = True,
) -> str | None:
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print(
        'Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print('Fulfillment text: {}\n'.format(response.query_result.fulfillment_text))

    if response.query_result.intent.is_fallback and not is_fallbac:
        return None
    else:
        return response.query_result.fulfillment_text


if __name__ == '__main__':
    env = Env()
    env.read_env()
    dialogflow_project_id = env.str('DIALOGFLOW_PROJECT_ID')

    my_key = create_api_key(dialogflow_project_id)

    detect_intent_text(
        project_id=dialogflow_project_id,
        session_id='16121996',
        text='Привет',
    )
