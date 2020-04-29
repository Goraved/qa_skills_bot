import os

import telebot
from flask import Flask, request

from data import get_stats, get_image_link

options = {'Statistics': 'Statistics by today', 'URL': 'Open site', 'Languages': 'Languages comparison'}
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row(options['Statistics'], options['Languages'], options['URL'])


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIBlF6psFYlbJCeQj7Ter-NBzwhfGLmAAIBAQACVp29CiK-nw64wuY0GQQ')
    bot.send_message(message.chat.id, 'Please choose an option', reply_markup=keyboard1)


@bot.message_handler(content_types=['sticker'])
def get_sticker_id(sticker):
    bot.send_message(sticker.chat.id, f'Sticker Id - {sticker.sticker.file_id}')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == options['Statistics'].lower():
        bot.send_message(message.chat.id, 'Processing...')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIBk16psBCMPBU_NmudwEd_jzye7P52AAICAQACVp29Ck7ibIHLQOT_GQQ')
        bot.send_message(message.chat.id, get_stats(), parse_mode="Markdown")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIBh16prxNbEgme1n_uECeShXDlUhekAAIFAQACVp29Crfk_bYORV93GQQ')
    elif message.text.lower() == options['Languages'].lower():
        bot.send_message(message.chat.id, 'Processing...')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIBk16psBCMPBU_NmudwEd_jzye7P52AAICAQACVp29Ck7ibIHLQOT_GQQ')
        bot.send_photo(message.chat.id, get_image_link())
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIBh16prxNbEgme1n_uECeShXDlUhekAAIFAQACVp29Crfk_bYORV93GQQ')


    elif message.text.lower() == options['URL'].lower():
        bot.send_message(message.chat.id, f'Site URL - https://qa-skills.herokuapp.com')
    else:
        bot.send_message(message.chat.id, 'Sorry, I did not understand this command')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIBkl6pr4kVOGisB5LUX54w8USsN6hWAAL5AANWnb0KlWVuqyorGzYZBA')


# Local
# bot.remove_webhook()
# bot.polling(none_stop=True)

# Heroku
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return '!', 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://qa-skills-bot.herokuapp.com/" + TOKEN)
    return "!", 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
