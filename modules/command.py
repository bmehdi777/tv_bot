import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from functools import wraps

import datetime

import logging

from getCommand import getBook
from getCommand import getGuide
from getCommand import getHackernews
from getCommand import getMeteo
from getCommand import getSomeone

from bdd import database

#Function
def read_f(path):
    f = open(path, 'r')
    return f.read()
    
def get_planning(pl):
    planning = []
    for i in pl["rss"]["channel"]["item"]:
        planning.append(i["title"].split("|"))
    return planning


def get_chaine(pl):
    txt_ch = []
    for i in pl:
        if (i[0] not in txt_ch):
            txt_ch += i[0]
    return txt_ch

#Command
def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(*args, **kwargs):
        bot, update = args
        if(database.get_chat_option(update.message.chat_id) == []):
            database.insert_chat(update.message.chat_id, 0,0,"")
        if(database.get_chat_enable(update.message.chat_id) == 1):
            bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
            func(bot, update, **kwargs)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Bot pas activé.\n/start pour activé ce dernier.")

    return command_func

######## ON/OFF COMMAND ###########
def cstart(bot, update):
    if (database.get_chat_enable(update.message.chat_id) == 0):
        bot.send_message(chat_id=update.message.chat_id, text="Démarrage du bot...")
        database.insert_chat(update.message.chat_id, 0, 0, "")
        database.set_enable_chat(update.message.chat_id, 1)
        logging.info("/start a été entré.")
    elif (database.get_chat_enable(update.message.chat_id) == 1):
        bot.send_message(chat_id=update.message.chat_id, text="Le bot est déjà allumé.")
        logging.info("/start a été entré alors que le bot est déjà allumé.")
def cstop(bot, update):
    if (database.get_chat_enable(update.message.chat_id) == 1):
        bot.send_message(chat_id=update.message.chat_id, text="Au revoir.")
        database.set_enable_chat(update.message.chat_id, 0)
        logging.info("/stop a été entré.")
    elif (database.get_chat_enable(update.message.chat_id) == 0):
        bot.send_message(chat_id=update.message.chat_id, text="Le bot est déjà éteint.")
        logging.info("/stop a été entré mais le bot est déjà éteint.")



######## MAIN COMMAND ############
@send_typing_action
def chelp(bot, update):
    help_str = read_f("file/helpercmd")
    bot.send_message(chat_id=update.message.chat_id, text=help_str, parse_mode=telegram.ParseMode.MARKDOWN)
    logging.info("/help a été entré.")

def wrongFormatCommand(bot, update):
    txt = "Mauvais format de commande.\nUtilisez /help pour plus d'information."
    bot.send_message(chat_id=update.message.chat_id, text=txt)


@send_typing_action
def cbook(bot, update):
    title = getBook.get_book_title()
    m = getBook.get_book_time()
    n = m[:2]+"h"+m[3:-3]+"m"+m[6:]
    nameBook = "Le livre du jour disponible sur Packtpub est : {t}.\nIl vous reste {tps} pour l'obtenir.\nAller sur Packtpub pour l'obtenir : {l}".format(t=title, tps=n, l=getBook.freelearning_url)
    bot.send_message(chat_id=update.message.chat_id, text=nameBook)
    logging.info("/book a été entré.")

@send_typing_action
def cweather2(bot, update, args):
    if (len(args)>0):
        word = ""
        for i in args:
            word+=i+"-"
        path_weather = getMeteo.getWeathercli(word)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(path_weather, 'rb'))
    else:
        wrongFormatCommand(bot, update)
    logging.info("/weathercli a été entré")
@send_typing_action
def cweather(bot, update, args):
    if (len(args) > 0):
        word = ""
        for i in args:
            word += i+"-"
        txt_weather = getMeteo.getWeather(word, 3)
        bot.send_message(chat_id=update.message.chat_id, text=txt_weather)
    else:
        wrongFormatCommand(bot, update)
    logging.info("/weather a été entré.")

@send_typing_action
def cinfo(bot, update, args):
    if (args[0] != ""):
        pl = getGuide.get_guide()
        planning = get_planning(pl)
        p= False
        word = ""
        for i in args:
            word += i
        for i in planning:
            if (word.lower().replace(" ", "")== i[0].lower().replace(" ","")):
                p=True
                
                break
            else:
                p=False
        if(p):
            text_pl = "Le planning pour {c} le {dt} est : \n".format(c=" ".join(args), dt=datetime.datetime.now().strftime('%d/%m/%Y') )
            for i in range(0,len(planning)):
                if (word.lower().replace(" ","") == planning[i][0].lower().replace(" ","")):
                    if (i+1 < len(planning) and args[0].lower() in planning[i+1][0].lower()):
                        n = datetime.datetime.now()
                        h, m = map(int, planning[i][1].split(':'))
                        d1 = datetime.datetime(n.year, n.month, n.day, h, m)
                        h, m= map(int, planning[i+1][1].split(':'))
                        d2 = datetime.datetime(n.year, n.month, n.day, h, m)
                        duration = d2- d1
                        if (int(d1.hour) >= 20):
                            text_pl += planning[i][1] +" -- "+planning[i][2]+"  ["+str(duration)+"]"+"\n"
                    else:
                        n = datetime.datetime.now()
                        h, m = map(int, planning[i][1].split(':'))
                        d1 = datetime.datetime(n.year, n.month, n.day, h, m)
                        if (int(d1.hour) >= 20):
                            text_pl += planning[i][1]+" -- "+planning[i][2]+" [??:??]\n"
            bot.send_message(chat_id=update.message.chat_id, text=text_pl)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Cette chaine n'existe pas. Veuillez vous référer à la commande /getchaine")
    else:
        wrongFormatCommand(bot, update)

@send_typing_action
def cprime(bot, update, args):
    pl = getGuide.get_guide()
    planning = get_planning(pl)
    p= True
        
    if (len(args)>0):
        cinfo(bot, update, args)
    else:
        text_pl = "Le prime pour le {dt} est : \n".format(dt=datetime.datetime.now().strftime('%d/%m/%Y') )
        for i in range(0,len(planning)):
            if (planning[i][0] not in text_pl)  :
                text_pl += "Programme sur {} : \n".format(planning[i][0])
            if (i+1 < len(planning)-1):
                n = datetime.datetime.now()
                h, m = map(int, planning[i][1].split(':'))
                d1 = datetime.datetime(n.year, n.month, n.day, h, m)
                h, m= map(int, planning[i+1][1].split(':'))
                d2 = datetime.datetime(n.year, n.month, n.day, h, m)
                duration = d2- d1
                if (d1 >= datetime.datetime(n.year, n.month, n.day, 20, 30) and 
                d1 <= datetime.datetime(n.year, n.month, n.day, 22, 30) and 
                duration >= datetime.timedelta(hours=0, minutes=30)):
                    if (planning[i][0].replace(" ", "") != ""):
                        text_pl += planning[i][1] +" -- "+planning[i][2]+"  ["+str(duration)+"]"+"\n"
            else:
                n = datetime.datetime.now()
                h, m = map(int, planning[i][1].split(':'))
                d1 = datetime.datetime(n.year, n.month, n.day, h, m)
                if (d1 >= datetime.datetime(n.year, n.month, n.day, 20, 30) and 
                d1 <= datetime.datetime(n.year, n.month, n.day, 22, 30) and 
                duration >= datetime.timedelta(hours=0, minutes=30)):
                    text_pl += planning[i][1]+" -- "+planning[i][2]+" [??:??]\n"
        bot.send_message(chat_id=update.message.chat_id, text=text_pl)
    logging.info("/prime a été entré.")

@send_typing_action
def cgetchaine(bot, update):
    pl = getGuide.get_guide()
    planning = get_planning(pl)
    
    text_ch = "Les chaines sont les suivantes : \n"
    for i in planning:
        if (i[0] not in text_ch):
            text_ch += i[0]+"\n"
    bot.send_message(chat_id=update.message.chat_id, text=text_ch)
    logging.info("/chaine a été entré.")

@send_typing_action
def chackerNews(bot, update):
    top = getHackernews.getTop50ID()
    article = getHackernews.getRandomArticle(top)
    ttl = article["title"]
    url_ttl = article["url"]
    txt = "*{t}*\nLiens : {u}".format(t=ttl, u=url_ttl)
    bot.send_message(chat_id=update.message.chat_id, text=txt, parse_mode=telegram.ParseMode.MARKDOWN)
    logging.info("/hackernews a été entré.")

@send_typing_action
def csomeone(bot, update):
    logging.info("/someone a été entré.")
    user = getSomeone.getSomeone(update.message.chat_id)
    txt = "@"+user[3]+" a été choisi."
    bot.send_message(chat_id=update.message.chat_id, text=txt)

class Command:
    handlers = (
        CommandHandler('stop', cstop),
        CommandHandler('start', cstart),
        CommandHandler('help', chelp),
        CommandHandler('chaine', cgetchaine),
        CommandHandler('prime', cprime, pass_args=True),
        CommandHandler('weather', cweather, pass_args=True),
        CommandHandler('weathercli', cweather2, pass_args=True),
        CommandHandler('book', cbook),
        CommandHandler('hackernews', chackerNews),
        CommandHandler('someone', csomeone),
        CommandHandler('info',cinfo, pass_args=True),
    )