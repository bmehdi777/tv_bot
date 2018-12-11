import logging

from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bdd import database
#Menu build  option for telegrams
def main_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                            message_id=query.message.message_id, 
                            text="Menu de configuration",
                            reply_markup=main_menu_keyboard())

def reminder_prime_menu(bot, update):
    query = update.callback_query
    if (database.get_chat_option_remind_prime(query.message.chat_id) == 1):
        txt = "Configuration du rappel : Activé"
    elif (database.get_chat_option_remind_prime(query.message.chat_id) == 0):
        txt = "Configuration du rappel : Desactivé"
    else:
        txt = "Configuration : "
    bot.edit_message_text(chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            text=txt,
                            reply_markup=reminder_prime_keyboard())
def start_menu(bot, update):
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id, 
                            message_id=query.message.message_id,
                            text="Configuration : ",
                            reply_markup=start_menu_keyboard())

def list_reminder(bot, update):
    query = update.callback_query
    txt = str(database.get_reminder_list(query.message.chat_id))
    for i in ["[","]", "(",")", "'"]:
        txt = txt.replace(i, "")
    bot.edit_message_text(chat_id=query.message.chat_id, 
                            message_id= query.message.message_id,
                            text="Liste actuelle :\n"+txt,
                            reply_markup=modify_prime_list_keyboard())
#Keyboards
def start_menu_keyboard():
    keyboard = [[InlineKeyboardButton("Commencer configuration", callback_data="main_menu")]]
    return InlineKeyboardMarkup(keyboard)
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Option', callback_data='reminder_prime_menu')],
                [InlineKeyboardButton('Quitter', callback_data='start_menu')]]
    return InlineKeyboardMarkup(keyboard)
def reminder_prime_keyboard():
    keyboard = [[InlineKeyboardButton('On', callback_data='on_reminder'), InlineKeyboardButton('Off', callback_data='off_reminder')],
                [InlineKeyboardButton('Liste filtre', callback_data='list_reminder')],
                [InlineKeyboardButton('Arrière', callback_data='main_menu')]]
    return InlineKeyboardMarkup(keyboard)
def modify_prime_list_keyboard():
    keyboard = [[InlineKeyboardButton('Modifier', callback_data='modify_prime_list')],
                [InlineKeyboardButton('Arrière', callback_data='reminder_prime_menu')]]
    return InlineKeyboardMarkup(keyboard)

# Callback function
def on_reminder(bot, update):
    query = update.callback_query
    logging.info("Reminder prime on.")
    database.set_chat_option_remind_prime(query.message.chat_id, 1)
    bot.edit_message_text(chat_id=query.message.chat_id,
                            message_id=query.message.message_id,
                            text="Reminder mis sur on.",
                            reply_markup=main_menu_keyboard())

def off_reminder(bot, update):
    query = update.callback_query
    logging.info("Reminder prime off.")
    database.set_chat_option_remind_prime(query.message.chat_id, 0)
    bot.edit_message_text(chat_id=query.message.chat_id, 
                            message_id=query.message.message_id, 
                            text="Reminder mis sur off.", 
                            reply_markup=main_menu_keyboard())

def modify_prime_list(bot, update):
    query = update.callback_query
    bot.send_message(chat_id=query.message.chat_id, text="Envoyez la liste des mots-clés.")
    database.set_chat_option_modifying_prime_list(query.message.chat_id, 1)
    logging.info("Modification de la liste en cours...")

# Command function
def cconfig(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Configuration : ", reply_markup=start_menu_keyboard())
    logging.info("/config a été entré.")

class Config:
    handlers = (
        CommandHandler('config', cconfig),
        CallbackQueryHandler(main_menu, pattern='main_menu'),
        CallbackQueryHandler(reminder_prime_menu, pattern='reminder_prime'),
        CallbackQueryHandler(on_reminder, pattern='on_reminder'),
        CallbackQueryHandler(off_reminder, pattern='off_reminder'),
        CallbackQueryHandler(list_reminder, pattern='list_reminder'),
        CallbackQueryHandler(modify_prime_list, pattern='modify_prime_list'),
        CallbackQueryHandler(start_menu, pattern='start_menu'),
    )
