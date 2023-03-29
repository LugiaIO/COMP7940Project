import os
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
import logging


def main():
    # Load your token and create an Updater for your Bot
    updater = Updater(token=os.environ["TOKEN"], use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("help", help_command))
    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Helping you helping you.")


def hello(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        logging.info(context.args[0])
        msg = context.args[0]
        update.message.reply_text("Good day, "+msg+"!")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /hello <keyword>")


if __name__ == "__main__":
    main()
