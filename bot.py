import os
import http
from flask import Flask, request
from werkzeug.wrappers import Response
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
from detail import movieOutput, reviewOutput, noteOutput
from movie_function import (
    randomMovie,
    search,
    read,
    imdbTop3,
    addToNote,
    addReview,
    listNotes,
)

MOVIE_NAME, MOVIE_GENRE, MOVIE_NOTE = range(3)
MOVIE_NAME_REVIEW, MOVIE_REVIEW = range(2)


app = Flask(__name__)

bot = Bot(token=os.environ["TOKEN"])


def helpCommand(update: Update, context: CallbackContext) -> None:
    """Handler for the '/help' command."""
    update.message.reply_text("Helping you helping you.")


def searchCommand(update: Update, context: CallbackContext) -> None:
    """Handler for the '/search' command."""
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
    """Handler for the '/read_reviews' command."""
    movie_name = context.args
    if len(movie_name) == 0:
        update.message.reply_text(
            "Please input movie name! Usage: /read_reviews <movie name>"
        )
    else:
        movie_name = " ".join(movie_name)
        reviews_list = read(movie_name)
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
    """Handler for the '/random_movie' command."""
    movie = randomMovie()
    (detail, image_link) = movieOutput(movie)
    update.message.bot.send_photo(
        chat_id=update.effective_chat.id, photo=image_link, caption=detail
    )


def listNoteCommand(update: Update, context: CallbackContext) -> None:
    """Handler for the '/list_note' command."""
    note_list = listNotes()
    for note in note_list:
        (detail, username) = noteOutput(note)
        update.message.reply_text(detail)
        textToWav("en-GB-Neural2-B", detail, note["name"], username)
        update.message.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=open(f"{note['name']}_{username}.wav", "rb"),
        )
        os.remove(f"{note['name']}_{username}.wav")


def startNote(update: Update, context: CallbackContext) -> None:
    """Handler for starting the note conversation."""
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! Please input the movie name:"
    )
    return MOVIE_NAME


def receiveName(update: Update, context: CallbackContext) -> None:
    """Handler for receiving the movie name in the note conversation."""
    name = update.message.text
    context.user_data["name"] = name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Thanks! Now please input the genre:"
    )
    return MOVIE_GENRE


def receiveGenre(update: Update, context: CallbackContext) -> None:
    """Handler for receiving the genre in the note conversation."""
    genre = update.message.text
    context.user_data["genre"] = genre
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Thanks! Now please input the note:"
    )
    return MOVIE_NOTE


def receiveNote(update: Update, context: CallbackContext) -> None:
    """Handler for receiving the note in the note conversation."""
    note = update.message.text
    context.user_data["note"] = note
    context.user_data["username"] = update.effective_user.username
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Thanks! Here is the information you provided:\nName: {}\nAge: {}\nNote: {}\nUsername: {}".format(
            context.user_data["name"],
            context.user_data["genre"],
            context.user_data["note"],
            context.user_data["username"],
        ),
    )
    addToNote(context.user_data)
    return ConversationHandler.END


def writereviewCommand(update: Update, context: CallbackContext) -> None:
    """Handler for the '/write_review' command."""
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Hello! Please input the movie name:"
    )
    return MOVIE_NAME_REVIEW


def receiveMovieName(update: Update, context: CallbackContext) -> None:
    """Handler for receiving the movie name in the review conversation."""
    name = update.message.text
    context.user_data["movie_name"] = name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Thanks! Now please input the review:"
    )
    return MOVIE_REVIEW


def receiveReview(update: Update, context: CallbackContext) -> None:
    """Handler for receiving the review in the review conversation."""
    movie_reviews = update.message.text
    context.user_data["movie_reviews"] = movie_reviews
    context.user_data["username"] = update.effective_user.username
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Thanks! Here is the information you provided:\nMovie name: {}\nReview: {}\nUsername: {}".format(
            context.user_data["movie_name"],
            context.user_data["movie_reviews"],
            context.user_data["username"],
        ),
    )
    addReview(context.user_data)
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> None:
    """Handler for canceling the conversation."""
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, something went wrong. Conversation canceled.",
    )
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start_note", startNote)],
    states={
        MOVIE_NAME: [MessageHandler(Filters.text & ~Filters.command, receiveName)],
        MOVIE_GENRE: [MessageHandler(Filters.text & ~Filters.command, receiveGenre)],
        MOVIE_NOTE: [MessageHandler(Filters.text & ~Filters.command, receiveNote)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

review_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("write_review", writereviewCommand)],
    states={
        MOVIE_NAME_REVIEW: [
            MessageHandler(Filters.text & ~Filters.command, receiveMovieName)
        ],
        MOVIE_REVIEW: [MessageHandler(Filters.text & ~Filters.command, receiveReview)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

dispatcher = Dispatcher(bot=bot, update_queue=None)
dispatcher.add_handler(CommandHandler("help", helpCommand))
dispatcher.add_handler(CommandHandler("random_movie", randomMovieCommand))
dispatcher.add_handler(CommandHandler("search", searchCommand))
dispatcher.add_handler(CommandHandler("read_reviews", readReviewsCommand))
dispatcher.add_handler(CommandHandler("list_note", listNoteCommand))
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(review_conv_handler)


@app.post("/")
def index() -> Response:
    """Main endpoint for receiving updates from Telegram."""
    dispatcher.process_update(Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT
