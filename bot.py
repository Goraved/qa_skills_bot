import os

import requests
import telebot
from flask import Flask, request

options = {'Statistics': 'Statistics by today', 'URL': 'Open site', 'Languages': 'Languages comparison'}
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row(options['Statistics'], options['Languages'], options['URL'])


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Please choose an option', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == options['Statistics'].lower():
        bot.send_message(message.chat.id, 'Processing...')
        latest_stats = requests.get('https://qa-skills.herokuapp.com/get_statistics').json()
        stats = '\n'.join([f"{stat['title']} - {stat['count']} ({stat['percent']})" for stat in latest_stats['stats']])
        positions = '\n'.join([f"{position['title']} - {position['count']}" for position in latest_stats['positions']])
        ways = '\n'.join([f"{way['title']} - {way['count']}" for way in latest_stats['ways']])
        bot.send_message(message.chat.id, f'*Statistics by day*: \n{stats}', parse_mode="Markdown")
        bot.send_message(message.chat.id, f'*Positions by day*: \n{positions}', parse_mode="Markdown")
        bot.send_message(message.chat.id, f'*Ways by day*: \n{ways}', parse_mode="Markdown")
        bot.send_message(message.chat.id, f'More info you can find [here](https://qa-skills.herokuapp.com)',
                         parse_mode="Markdown")
    elif message.text.lower() == options['Languages'].lower():
        bot.send_message(message.chat.id, 'Processing...')
        trigger_image = requests.get('https://qa-skills.herokuapp.com/get_language_comparison')
        image_link = 'https://qa-skills.herokuapp.com/static/images/languages.png'
        bot.send_photo(message.chat.id, image_link)

    elif message.text.lower() == options['URL'].lower():
        bot.send_message(message.chat.id, f'Site URL - https://qa-skills.herokuapp.com')
    else:
        bot.send_message(message.chat.id, 'Sorry, I did not understand this command')


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
