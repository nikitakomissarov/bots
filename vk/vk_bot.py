import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import dotenv_values
from google.cloud import dialogflow
import logging
from logging.handlers import TimedRotatingFileHandler
import json

config = dotenv_values('.env')

VK_TOKEN = config['TOKEN']
GOOGLE_APPLICATION_CREDENTIALS = config['GOOGLE_APPLICATION_CREDENTIALS']

vk_session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

logger_info = logging.getLogger('loggerinfo')
logger_error = logging.getLogger("loggererror")
handler = TimedRotatingFileHandler("app.log", when='D', interval=30, backupCount=1)
handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


with open(GOOGLE_APPLICATION_CREDENTIALS, "r") as my_file:
    credentials = my_file.read()
    credentials = json.loads(credentials)


def main():
    handler.setFormatter(handler_format)

    logger_info.setLevel(logging.INFO)
    logger_info.addHandler(handler)

    logger_error.setLevel(logging.ERROR)
    logger_error.addHandler(handler)

    logger_info.info('here we go')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
                echo(event, vk)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    logger_info.info("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    logger_info.info("=" * 20)
    logger_info.info("Query text: {}".format(response.query_result.query_text))
    logger_info.info(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        ))
    if response.query_result.intent.is_fallback is True\
            or response.query_result.intent_detection_confidence == 0:
        logger_error.error('Нулевое совпадение')
        return None
    else:
        answer = (format(response.query_result.fulfillment_text))
        return answer


def echo(event, vk):
    try:
        language_code = 'ru'
        text = event.text
        session_id = event.peer_id
        google_reply = detect_intent_texts(credentials['quota_project_id'], session_id, text, language_code)
        if google_reply != None:
            google_reply = google_reply
            vk.messages.send(
                user_id=event.user_id,
                message=google_reply,
                random_id=random.randint(1, 1000)
            )
        else:
            pass
    except Exception as err:
        logger_error.exception(err)


if __name__ == '__main__':
    main()


