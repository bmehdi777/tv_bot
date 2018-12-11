import logging

import telegram
from telegram.ext import CommandHandler
from modules import job

import datetime
from bdd import database


def reminder_prime(bot, job):
    pl = getGuide.get_guide()
    planning = get_planning(pl)
    r = database.get_chat_option_modifying_prime_list(job.context))
    remind=  list()
    for i in reminder_prime[0]:
        remind.append(i)
    text_remind = "IMPORTANT - Ce soir :\n"
    for i in range(0, len(planning)):
        if (remind[i].lower() in planning[i][2]):
            text_remind = "Programme sur {} :\n".format(planning[i][0])
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
                        text_remind += planning[i][1] +" -- "+planning[i][2]+"  ["+str(duration)+"]"+"\n"

class Job:
    def __init__(self):
        self.prime_reminder = job.run_daily(reminder_prime, datetime.time(hour=20, minute=00, second=00))

    def enable_job(self):
        self.prime_reminder.enabled = True
    def disabled_job(self):
        self.prime_reminder.disabled = False
        self.prime_reminder.schedule_removal()

            

