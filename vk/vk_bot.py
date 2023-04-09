import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import dotenv_values

config = dotenv_values('.env')

VK_TOKEN = config['TOKEN']

vk_session = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

def echo(event, vk):
    vk.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        print('Новое сообщение:')
        if event.to_me:
            print('Для меня от: ', event.user_id)
            echo(event, vk)
        else:
            print('От меня для: ', event.user_id)
        print('Текст:', event.text)