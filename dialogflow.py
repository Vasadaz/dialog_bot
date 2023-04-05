from google.cloud import dialogflow


def create_intent(project_id: str, intent_name: str, questions: list, answers: list):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

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


def detect_intent_text(project_id: str, session_id: str, text: str) -> dialogflow.QueryResult:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code='RU-ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={'session': session, 'query_input': query_input})

    return response.query_result
