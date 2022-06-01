import logging
import os
import random

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

WATCHLIST_CARD_ID = "or6keq7d"


async def get_random_movie(update: Update, context: CallbackContext.DEFAULT_TYPE):
    request = requests.get(f'https://api.trello.com/1/cards/{WATCHLIST_CARD_ID}/checklists',
                           params={'key': os.environ['TRELLO_API_KEY'],
                                   'token': os.environ['TRELLO_API_TOKEN']})
    await context.bot.send_message(chat_id=update.effective_chat.id, text=generate_bot_response(request))


def generate_bot_response(request):
    if request:
        watchlist = request.json()[0]['checkItems']
        return get_random_movie_name(watchlist)
    else:
        return "Couldn't fetch the data from Trello. Help."


def get_random_movie_name(watchlist):
    remove_completed_movies(watchlist)
    random_index = random.randint(0, len(watchlist) - 1)
    return watchlist[random_index]['name']


def remove_completed_movies(watchlist):
    for item in watchlist:
        if item['state'] == 'complete':
            watchlist.remove(item)


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ['BOT_TOKEN']).build()
    get_random_movie_handler = CommandHandler('movie', get_random_movie)
    application.add_handler(get_random_movie_handler)

    application.run_polling()
