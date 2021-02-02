import time
from json.decoder import JSONDecodeError

import requests


def get_ways() -> str:
    latest_stats = try_to_get_latest_stats()
    ways = '\n'.join([f"{way['title']} - {way['count']}" for way in latest_stats['ways']])
    return '\n\n'.join([f'*Ways by day*: \n{ways}',
                        'More info you can find [here](https://qa-skills.herokuapp.com)'])


def get_positions() -> str:
    latest_stats = try_to_get_latest_stats()
    positions = '\n'.join([f"{position['title']} - {position['count']}" for position in latest_stats['positions']])
    return '\n\n'.join([f'*Positions by day*: \n{positions}',
                        'More info you can find [here](https://qa-skills.herokuapp.com)'])


def get_stats() -> str:
    latest_stats = try_to_get_latest_stats()
    stats = '\n'.join([f"{stat['title']} - {stat['count']} ({stat['percent']})" for stat in latest_stats['stats']])
    return '\n\n'.join([f'*Statistics by day*: \n{stats}',
                        'More info you can find [here](https://qa-skills.herokuapp.com)'])


def get_image_link():
    # To make sure image created
    trigger_image = requests.get('https://qa-skills.herokuapp.com/get_language_comparison').json()
    url = trigger_image['image'].replace('/app', 'https://qa-skills.herokuapp.com')
    return url


def try_to_get_latest_stats() -> dict:
    for _ in range(10):
        try:
            latest_stats = requests.get('https://qa-skills.herokuapp.com/get_statistics').json()
            return latest_stats
        except JSONDecodeError:
            time.sleep(1)
