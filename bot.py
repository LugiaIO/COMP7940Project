import os
import http

from flask import Flask, request
from werkzeug.wrappers import Response
from detail import movieOutput, reviewOutput
from telegram import Bot, Update
from telegram.ext import (
    Dispatcher,
    Filters,
    MessageHandler,
    CallbackContext,
    CommandHandler,
)
from tts import textToWav
from movie_function import randomMovie, search, read

app = Flask(__name__)

bot = Bot(token=os.environ["TOKEN"])


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def helpCommand(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Helping you helping you.")


def searchCommand(update: Update, context: CallbackContext) -> None:
    keyword_list = context.args
    if len(keyword_list) != 0:
        for keyword in keyword_list:
            movie_list = search(keyword)
            for movie in movie_list:
                (detail, image_link) = movieOutput(movie)
                update.message.bot.send_photo(
                    chat_id=update.effective_chat.id, photo=image_link, caption=detail
                )
    else:
        update.message.reply_text("Please input keyword! Usage: /search <keyword>")


def readReviewsCommand(update: Update, context: CallbackContext) -> None:
    movie_name = context.args
    if len(movie_name) == 0:
        update.message.reply_text("Please input moive name! Usage: /read_reviews <moive name>")
    else:
        movie_name = " ".join(movie_name)
        print(movie_name)
        print(str(type(movie_name))+"ssss"+movie_name)
        reviews_list = read(movie_name)
        print(reviews_list)
        if len(reviews_list) != 0 and len(movie_name)!=0:
            for review in reviews_list:
                (output, username) = reviewOutput(review)
                update.message.reply_text(output)
                textToWav("en-GB-Neural2-B", output, movie_name, username)
                update.message.bot.send_audio(
                    chat_id=update.effective_chat.id,
                    audio=open(f"{movie_name}_{username}.wav", "rb"),
                )
                os.remove(f"{movie_name}_{username}.wav")
        else:
            update.message.reply_text("No review for this movie.")
        



def randomMovieCommand(update: Update, context: CallbackContext) -> None:
    movie = randomMovie()
    (detail, image_link) = movieOutput(movie)
    update.message.bot.send_photo(
        chat_id=update.effective_chat.id, photo=image_link, caption=detail
    )


dispatcher = Dispatcher(bot=bot, update_queue=None)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
dispatcher.add_handler(CommandHandler("help", helpCommand))
dispatcher.add_handler(CommandHandler("random_movie", randomMovieCommand))
dispatcher.add_handler(CommandHandler("search", searchCommand))
dispatcher.add_handler(CommandHandler("read_reviews", readReviewsCommand))


@app.post("/")
def index() -> Response:
    dispatcher.process_update(Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT
