import logging
import os
from flask import Flask, request
import telebot

options = {'Statistics': 'Statistics by today', 'URL': 'Site URL'}
bot = telebot.TeleBot(os.getenv('TOKEN'))

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row(options['Statistics'], options['URL'])


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Please choose an option', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == options['Statistics'].lower():
        bot.send_message(message.chat.id, f'Statistics by day - https://qa-skills.herokuapp.com/statistics')
    elif message.text.lower() == options['URL'].lower():
        bot.send_message(message.chat.id, f'Site URL - https://qa-skills.herokuapp.com')
    else:
        bot.send_message(message.chat.id, 'Sorry, I did not understand this command')


# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://min-gallows.herokuapp.com/bot") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)
