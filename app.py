import os
import socket

import telebot
from flask import Flask, request

options = {'Statistics': 'Statistics by today', 'URL': 'Site URL'}
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

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


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://qa-skills-bot.herokuapp.com/" + TOKEN)
    return "!", 200


if __name__ == '__main__':
    server.run(host=socket.gethostname(), port=int(os.environ.get('PORT', 5000)))
