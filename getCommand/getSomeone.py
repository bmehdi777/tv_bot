from bdd import database
import random

def getSomeone(chat_id):
    print(chat_id)
    users = database.get_user_in_chat(chat_id)
    len_user = database.get_number_user_in_chat(chat_id)[0][0]
    random_user = random.randint(0, len_user-1)
    return users[random_user]

if __name__ == "__main__":
    print(getSomeone(-285698150))