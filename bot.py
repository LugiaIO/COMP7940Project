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
    ConversationHandler,
)
from tts import textToWav
from movie_function import randomMovie, search, read, imdbTop3, addToNote

MOVIE_NAME, MOVIE_GENRE, MOVIE_NOTE = range(3)

app = Flask(__name__)

bot = Bot(token=os.environ["TOKEN"])


# def echo(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text(update.message.text)


def helpCommand(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Helping you helping you.")


def searchCommand(update: Update, context: CallbackContext) -> None:
    keyword_list = context.args
    if len(keyword_list) != 0:
        for keyword in keyword_list:
            movie_list = search(keyword)
            if len(movie_list) != 0:
                for movie in movie_list:
                    (detail, image_link) = movieOutput(movie)
                    update.message.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=image_link,
                        caption=detail,
                    )
            else:
                update.message.reply_text("No results found!")
    else:
        update.message.reply_text("Please input keyword! Usage: /search <keyword>")


def readReviewsCommand(update: Update, context: CallbackContext) -> None:
    movie_name = context.args
    if len(movie_name) == 0:
        update.message.reply_text(
            "Please input moive name! Usage: /read_reviews <moive name>"
        )
    else:
        movie_name = " ".join(movie_name)
        print(movie_name)
        print(str(type(movie_name)) + "ssss" + movie_name)
        reviews_list = read(movie_name)
        print(reviews_list)
        if len(reviews_list) != 0 and len(movie_name) != 0:
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

def imdbTop3Command(update: Update, context: CallbackContext) -> None:
    
    movie_list = imdbTop3()
    if len(movie_list) != 0:
        for movie in movie_list:
            (detail, image_link) = movieOutput(movie)
            update.message.bot.send_photo(
                chat_id=update.effective_chat.id, photo=image_link, caption=detail
            )
    else:
        update.message.reply_text("No results found!")

def start_note(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Please input the movie name:")
    return MOVIE_NAME


def receive_name(update: Update, context: CallbackContext) -> None:
    name = update.message.text
    context.user_data['name'] = name
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks! Now please input the genre:")
    return MOVIE_GENRE


def receive_genre(update: Update, context: CallbackContext) -> None:
    genre = update.message.text
    context.user_data['genre'] = genre
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks! Now please input the note:")
    return MOVIE_NOTE


def receive_note(update: Update, context: CallbackContext) -> None:
    note = update.message.text
    context.user_data['note'] = note
    context.user_data['username'] = update.effective_user.username
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks! Here is the information you provided:\nName: {}\nAge: {}\nNote: {}\nUsername: {}".format(context.user_data['name'], context.user_data['genre'], context.user_data['note'], context.user_data['username']))
    addToNote(context.user_data)
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, something went wrong. Conversation canceled.")
    return ConversationHandler.END

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start_note', start_note)],
        states={
            MOVIE_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_name)],
            MOVIE_GENRE: [MessageHandler(Filters.text & ~Filters.command, receive_genre)],
            MOVIE_NOTE: [MessageHandler(Filters.text & ~Filters.command, receive_note)]
        },
        fallbacks=[CommandHandler('cancel',cancel)]
    )

dispatcher = Dispatcher(bot=bot, update_queue=None)
#dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
dispatcher.add_handler(CommandHandler("help", helpCommand))
dispatcher.add_handler(CommandHandler("random_movie", randomMovieCommand))
dispatcher.add_handler(CommandHandler("search", searchCommand))
dispatcher.add_handler(CommandHandler("read_reviews", readReviewsCommand))
dispatcher.add_handler(CommandHandler("imdb_top_3", imdbTop3Command))
dispatcher.add_handler(ConversationHandler('start_note', start_note))
dispatcher.add_handler(CommandHandler('cancel', cancel))


@app.post("/")
def index() -> Response:
    dispatcher.process_update(Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT
