import os
import http

from flask import Flask, request
from werkzeug.wrappers import Response
from detail import output,The_Jungle_Book
from telegram import Bot, Update
from telegram.ext import Dispatcher, Filters, MessageHandler, CallbackContext, CommandHandler

app = Flask(__name__)

(detail, image_link) = output(The_Jungle_Book)

def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Helping you helping you.")

def test_command(update: Update, context: CallbackContext) -> None:
    update.message.bot(chat_id=update.effective_chat.id, photo=
image_link, caption=detail)

bot = Bot(token=os.environ["TOKEN"])



dispatcher = Dispatcher(bot=bot, update_queue=None)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
dispatcher.add_handler(CommandHandler("help", help_command))

@app.post("/")
def index() -> Response:
    dispatcher.process_update(
        Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT