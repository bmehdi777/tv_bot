import logging

import telegram
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext.dispatcher import run_async

from bdd import database
from modules import updater as update

@run_async
def on_new_member(bot, update):
    logging.info("Nouveau membre '{m}' dans le chat : {c}".format(m=update.message.new_chat_members, c=update.message.chat_id))
    for user in update.message.new_chat_members:
        database.insert_user(user["id"], user["first_name"], user["last_name"], user["username"], update.message.chat_id)

@run_async
def on_left_member(bot, update):
    logging.info("Un membre '{m}' a quitté le chat : {c}".format(m=update.message.left_chat_member, c=update.message.chat_id))
    database.remove_user(update.message.left_chat_member["id"], update.message.chat_id)

@run_async
def on_new_message(bot, update):
    user = update.message.from_user
    logging.info("Nouveau message reçu de '{m}' sur le chat : {c}".format(m=user["username"], c=update.message.chat_id))
    database.insert_user(user["id"], user["first_name"], user["last_name"], user["username"],update.message.chat_id)
    if (database.get_chat_option_modifying_prime_list(update.message.chat_id) == 1):
        database.set_reminder_list(update.message.chat_id, update.message.text)
        logging.info("Reminder list mis à jour.")
        bot.send_message(chat_id=update.message.chat_id, text="Liste mise à jour.")
        database.set_chat_option_modifying_prime_list(update.message.chat_id, 0)


class Message:
    handlers = (
        MessageHandler(Filters.status_update.new_chat_members & ~Filters.user(user_id=update.bot.id), on_new_member),
        MessageHandler(Filters.status_update.left_chat_member & ~Filters.user(user_id=update.bot.id), on_left_member),
        MessageHandler(Filters.group, on_new_message),
    )