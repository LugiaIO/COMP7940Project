import os
import http

from flask import Flask, request
from werkzeug.wrappers import Response
from detail import output
from telegram import Bot, Update
from telegram.ext import (
    Dispatcher,
    Filters,
    MessageHandler,
    CallbackContext,
    CommandHandler,
)

from movie_function import randomMovie, search

app = Flask(__name__)

bot = Bot(token=os.environ["TOKEN"])

def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def helpCommand(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Helping you helping you.")


def searchCommand(update: Update, context: CallbackContext) -> None:
    keyword_list = context.args
    if len(keyword_list)!=0:
        for keyword in keyword_list:
            movie_list = search(keyword)
            for movie in movie_list:
                (detail, image_link) = output(movie)
                update.message.bot.send_photo(
                    chat_id=update.effective_chat.id, photo=image_link, caption=detail
                )
    else:
        update.message.reply_text("Please input keyword! Usage: /search <keyword>")

def randomMovieCommand(update: Update, context: CallbackContext) -> None:
    movie = randomMovie()
    (detail, image_link) = output(movie)
    update.message.bot.send_photo(
        chat_id=update.effective_chat.id, photo=image_link, caption=detail
    )

dispatcher = Dispatcher(bot=bot, update_queue=None)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
dispatcher.add_handler(CommandHandler("help", helpCommand))
dispatcher.add_handler(CommandHandler("random_movie", randomMovieCommand))
dispatcher.add_handler(CommandHandler("search", searchCommand))


@app.post("/")
def index() -> Response:
    dispatcher.process_update(Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT
