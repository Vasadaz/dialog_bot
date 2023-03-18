# Боты Telegram и VK с обработкой сообщений в Dialogflow

Проект реализован для автоматизации ответов на часто задаваемые вопросы.

Примеры:

- [Бот Telegram](https://t.me/lesson_tg_3_devman_bot)
- [Бот VK](https://vk.com/club219388423)


## Как установить

1. Клонировать репозиторий:
    ```shell
    git clone https://github.com/Vasdaz/voise_bot.git
    ```

2. Установить зависимости:
    ```shell
    pip install -r requirements.txt
    ```

3. 1. [Создать агента DialogFlow для русского языка(нужен будет его Project ID)](https://dialogflow.cloud.google.com/#/newAgent);
   2. [Получить файл `credentials.json` с ключами от вашего Google-аккаунта](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk);
   3. Положить в корень проекта файл `credentials.json` - файл хранит секретные данные, его нельзя публиковать; 
   4. [Включить API агента](https://cloud.google.com/dialogflow/es/docs/quick/setup#api).
   

4. [Получить токен Телеграм бота](https://telegram.me/BotFather).


5. 1. [Создать группу VK](https://vk.com/faq18025);
   2. [Получить токен Телеграм бота.](https://vk.com/@articles_vk-token-groups).


6. Создать файл `.env` с данными:
    ```dotenv
    DIALOGFLOW_API_KEY=AIQz...rdEc
    DIALOGFLOW_PROJECT_ID=testbot-7414741
    GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
    TELEGRAM_BOT_TOKEN=585242324741:AAH...q_H7A
    VK_BOT_TOKEN=vk1.a.AP_G...nABw

    ```
   
7. Создать в Dialogflow ответы ботов на список типичных вопросов.
   1. [Вручную](https://cloud.google.com/dialogflow/es/docs/intents-training-phrases);
   2. Через JSON файл:
      1. Заполнить JSON файл с именем `intents.json` [по примеру](./intents.json);
      2. Положить файл `intents.json` в корень проекта;
      2. Запустить скрипт:
        ```shell
        python3 create_intents.py
        ```

8. Запуск ботов:
    
    - Telegram
      ```shell
      python3 run_tg_bot.py
      ```
    - VK
      ```shell
      python3 run_vk_bot.py
      ```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
