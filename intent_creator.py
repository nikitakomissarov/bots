from main import logger_info, logger_error, handler, handler_format
from google.cloud import dialogflow
import json
from dotenv import dotenv_values
import logging

config = dotenv_values('.env')

TRAINING_PHRASES = config['TRAINING_PHRASES']
GOOGLE_APPLICATION_CREDENTIALS = config['GOOGLE_APPLICATION_CREDENTIALS']

with open(GOOGLE_APPLICATION_CREDENTIALS, "r") as google_file:
  credentials = google_file.read()
  credentials = json.loads(credentials)

with open(TRAINING_PHRASES, "r",  encoding='utf-8') as phrases_file:
  training_phrases_parts = phrases_file.read()
  training_phrases_parts = json.loads(training_phrases_parts)

def create_intent(project_id, training_phrases_parts):

    handler.setFormatter(handler_format)

    logger_info.setLevel(logging.INFO)
    logger_info.addHandler(handler)

    logger_error.setLevel(logging.ERROR)
    logger_error.addHandler(handler)

    try:
        for section in training_phrases_parts:
            display_name = section

        message_texts = []
        message_texts.append(training_phrases_parts[display_name]['answer'])

        intents_client = dialogflow.IntentsClient()
        parent = dialogflow.AgentsClient.agent_path(project_id)

        training_phrases = []
        training_phrases_part = training_phrases_parts[display_name]['questions']

        for question in training_phrases_part:
            part = dialogflow.Intent.TrainingPhrase.Part(text=question)
            training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
            training_phrases.append(training_phrase)

        text = dialogflow.Intent.Message.Text(text=message_texts)
        message = dialogflow.Intent.Message(text=text)

        intent = dialogflow.Intent(
            display_name=display_name, training_phrases=training_phrases, messages=[message]
        )

        response = intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )
        logger_info.info("Intent created: {}".format(response))
    except Exception as err:
        logger_error.exception(err)

create_intent(credentials['quota_project_id'], training_phrases_parts)