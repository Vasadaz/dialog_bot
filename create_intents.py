#!/usr/bin/env python

import json

from dialogflow import create_intent


INTENTS_FILE_NAME = 'intents.json'


if __name__ == '__main__':
    with open(INTENTS_FILE_NAME, 'r') as file:
        intents = json.load(file)

    for intent_name, phrases in intents.items():
        create_intent(
            intent_name=intent_name,
            questions=phrases['questions'],
            answers=phrases['answers']
        )
