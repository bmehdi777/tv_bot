import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

from modules import updater
from modules import disp
from modules import bt

import logging

from modules import command
from modules import message
from modules import config

#Log parameter
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main():
    for handler in command.Command.handlers:
        disp.add_handler(handler)

    for handler in config.Config.handlers:
        disp.add_handler(handler)
        
    for handler in message.Message.handlers:
        disp.add_handler(handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()