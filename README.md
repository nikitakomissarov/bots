## Tg_bot ##

Это бот, направленный на автоматизацию поддержки какого-либо продукта в Телеграме. Он основан на возможностях https://dialogflow.cloud.google.com/, с помощью которого узнает фразы пользователя в зависимости от своей обученности. Если бот не узнает фразу пользователя, то он отвечает фразами из заранее подготовленного в dialogflow Intent'a, например «Перефразируйте ваше сообщение, пожалуйста».

![7LWm9tPFtL](https://github.com/nikitakomissarov/bots/assets/59535117/a994755e-4f0c-4a16-a553-14369edd593d) 

В этом же проекте есть logger — бот, который подхватывает ошибки (если они возникнут) и отправляет их в Телеграме тому пользователю, чей id будет указан в качестве id для отправки сообщений. 

Чтобы ими пользоваться, нужно:
1. Создать 2 ботов: один непосредственно tg_bot, второй — бот для логирования ошибок logger. 
2. Создать проект в https://dialogflow.cloud.google.com и получить credentials.
3. Скачать этот репозиторий и установить requirements.txt:
``` C:\Users\big shot>git clone https://github.com/nikitakomissarov/bots
C:\Users\big shot>cd bots
C:\Users\big shot\bots>python  -m venv env
C:\Users\big shot\bots>env\Scripts\activate.bat
(env) C:\Users\big shot\bots>pip install -r requirements.txt
``` 
4. Натренировать dialogflow  фразами через intent_creator.py:
      1. Готовим список фраз, например questions.json.
      2. Подключаем переменные в .env, где TRAINING_PHRASES — ваш json с фразами, GOOGLE_APPLICATION_CREDENTIALS — ваши credentials из dialogflow.
      3. Запускаем скрипт:```(env) C:\Users\big shot\bots>python intent_creator.py```
         Возвращаемся на https://dialogflow.cloud.google.com — проверяем, загрузились ли ответы.
      5. Переходим в настройки агента, затем во вкладку ML Settings, выбираем подходящие для вас настройки тренировки, жмем Train, затем Save. 
5. Подключить переменные для tg_bot в .env, где TG_TOKEN — токен для бота в Телеграме, GOOGLE_APPLICATION_CREDENTIALS — ваши credentials из dialogflow.
6. Подключить logger.py для подхватывания ошибок: в .env указываем переменные, где TG_CHAT_ID — id пользователя, которому будут отправляться ошибки, TG_LOGGER_TOKEN — токен бота, который вы создавали в пункте 1. 
7. Наконец, запускаем:
```
(env) C:\Users\big shot\bots>python tg_bot.py
```

## Vk_bot ##
Это бот, направленный на автоматизацию поддержки группы ВК. Он основан на возможностях https://dialogflow.cloud.google.com/, с помощью которого узнает фразы пользователя в зависимости от своей обученности. Если бот не узнает фразу пользователя, то он хранит молчание. 

![opera_TmqHfUQPwM](https://github.com/nikitakomissarov/bots/assets/59535117/c0bcb5be-4505-4828-8947-1e1c91da40d4)

В этом же проекте есть logger — бот, который подхватывает ошибки (если они возникнут) и отправляет их в Телеграме тому пользователю, чей id будет указан в качестве id для отправки сообщений.
Чтобы ими пользоваться, нужно:
1. Создать группу ВК и получить токен для API, а также бот в Телеграме для логирования ошибок logger. 
2. Повторить пункт 2 из Tg_bot.
3. Повторить пункт 3 из Tg_bot.
4. Повторить пункт 4 из Tg_bot.
5. Подключить переменные для vk_bot в .env, где VK_TOKEN — токен для доступа к API из настроек группы ВК, GOOGLE_APPLICATION_CREDENTIALS — ваши credentials из dialogflow.
6. Повторить пункт 6 из Tg_bot.
7. Наконец, запускаем:
```
(env) C:\Users\big shot\bots>python vk_bot.py
