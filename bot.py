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
from movie_function import randomMovie, search, read, imdbTop3

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
# ####### New ADD
# def send_welcome(update: Update, context:CallbackContext) -> None:
#     update.message.reply_text("Welcome to Note-record, now you can create new records, or view existing records. Add_note format as below, title + content")

# def add_note(update: Update, context:CallbackContext) -> None:
#         chat_id = update.effective_chat.id
#         length = len(context.args)
#         if length == 0:
#             update.message.reply_text("Please specify the title of the new record")
#         elif length ==1:
#             update.message.reply_text("Please also specify the content of the new record")
#         else:
#             title = context.args[0]
#             content = ' '.join(context.args[1:])
#             redis1.hmset(chat_id, {'title': title, 'content': content})
#             update.message.reply_text("A new record has been created with the following title:",content)
       
# def list_note(update: Update,context:CallbackContext) -> None:
#     try:
#         chat_id = update.effective_chat.id
#         if chat_id not in redis1.hgetall(chat_id):
#             update.message.reply_text("No recording")
#         else:
#             reply_message = ''
#             for note_title in redis1.hgetall(chat_id):
#                 reply_message += redis1.hget(chat_id,note_title.decode('utf-8')).decode('utf-8') + '\n'
#             update.message.reply_text(reply_message)
#     except(IndexError,ValueError):
#         update.message.reply_text('Error,please try again')
# ######

dispatcher = Dispatcher(bot=bot, update_queue=None)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
dispatcher.add_handler(CommandHandler("help", helpCommand))
dispatcher.add_handler(CommandHandler("random_movie", randomMovieCommand))
dispatcher.add_handler(CommandHandler("search", searchCommand))
dispatcher.add_handler(CommandHandler("read_reviews", readReviewsCommand))
dispatcher.add_handler(CommandHandler("imdb_top_3", imdbTop3Command))
# #new add
# dispatcher.add_handler(CommandHandler('notebook',send_welcome))
# dispatcher.add_handler(CommandHandler('newnote',add_note))
# dispatcher.add_handler(CommandHandler('listnote',list_note))
# #####

@app.post("/")
def index() -> Response:
    dispatcher.process_update(Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT
