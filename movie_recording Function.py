from telegram.ext import ConversationHandler

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start_note', start_note)],
        states={
            MOVIE_NAME: [MessageHandler(Filters.text & ~Filters.command, receive_name)],
            MOVIE_GENRE: [MessageHandler(Filters.text & ~Filters.command, receive_genre)],
            MOVIE_NOTE: [MessageHandler(Filters.text & ~Filters.command, receive_note)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler)



MOVIE_NAME, MOVIE_GENRE, MOVIE_NOTE = range(3)

def start_note(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Please input the movie name:")
    return MOVIE_NAME


def receive_name(update, context):
    name = update.message.text
    context.user_data['name'] = name
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks! Now please input the genre:")
    return MOVIE_GENRE


def receive_genre(update, context):
    genre = update.message.text
    context.user_data['genre'] = genre
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks! Now please input the note:")
    return MOVIE_NOTE


def receive_note(update, context):
    note = update.message.text
    context.user_data['note'] = note
    context.user_data['username'] = update.effective_user.username
    context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks! Here is the information you provided:\nName: {}\nAge: {}\nNote: {}\nUsername: {}".format(context.user_data['name'], context.user_data['genre'], context.user_data['note'], context.user_data['username']))
    #addToNote(context.user_data)
    return ConversationHandler.END

def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, something went wrong. Conversation canceled.")
    return ConversationHandler.END