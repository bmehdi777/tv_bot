import logging
import sqlite3

import os.path

from bdd import sql

class Database:

    def __init__(self, path):
        self.db_path = path
        self.init_db()

    def init_db(self):
        try:
            self.conn()
            cursor = self.conn.cursor()
            logging.info("Création de la base de donnée.")
            cursor.execute(sql.CREATE_TABLE_USER)
            logging.info("Table User créer.")
            cursor.execute(sql.CREATE_TABLE_USERCHAT)
            logging.info("Table UserChat créer.")
            cursor.execute(sql.CREATE_TABLE_CHAT)
            logging.info("Table Chat créer.")
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.info("Erreur : la table existe déjà.")
        except Exception as e:
            logging.info("Erreur : {}".format(e))
            self.conn.rollback()

    def conn(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)

    def insert_user(self, user_id, first_name, last_name, username, chat_id):
        cursor = self.conn.cursor()
        cursor.execute(sql.INSERT_USER, (user_id, first_name, last_name, username))
        cursor.execute(sql.INSERT_USER_CHAT, (chat_id, user_id))
        self.conn.commit()

    def insert_chat(self, chat_id, remind_prime, enable, l):
        cursor = self.conn.cursor()
        cursor.execute(sql.INSERT_CHAT,(chat_id,enable,remind_prime,l,0))
        self.conn.commit()

    def set_enable_chat(self, chat_id, enable):
        cursor = self.conn.cursor()
        cursor.execute(sql.SET_ENABLE, (enable, chat_id))
        self.conn.commit()

    def get_chat_option(self, chat_id):
        cursor = self.conn.cursor()
        cursor.execute(sql.GET_OPTION_CHAT, (chat_id,))
        data = cursor.fetchall()
        self.conn.commit()
        return data

    def get_chat_enable(self, chat_id):
        option_chat = self.get_chat_option(chat_id)
        return option_chat[0][1]

    def set_chat_option_remind_prime(self, chat_id, remind_prime):
        cursor = self.conn.cursor()
        cursor.execute(sql.SET_OPTION_CHAT_REMIND_PRIME, (remind_prime, chat_id))
        self.conn.commit()
    def get_chat_option_remind_prime(self, chat_id):
        option_remind_prime = self.get_chat_option(chat_id)
        return option_remind_prime[0][2]

    def get_chat_option_modifying_prime_list(self, chat_id):
        option_list_prime = self.get_chat_option(chat_id)
        return option_list_prime[0][4]
    def set_chat_option_modifying_prime_list(self, chat_id, modify_list_bool):
        cursor = self.conn.cursor()
        cursor.execute(sql.SET_BOOL_PRIME_LIST, (modify_list_bool, chat_id))
        self.conn.commit()
    
    def get_reminder_list(self, chat_id):
        cursor = self.conn.cursor()
        cursor.execute(sql.GET_LIST_REMINDER, (chat_id,))
        data = cursor.fetchall()
        self.conn.commit()
        return data
    def set_reminder_list(self, chat_id, reminder_list):
        cursor = self.conn.cursor()
        cursor.execute(sql.SET_LIST_REMINDER, (reminder_list, chat_id))
        self.conn.commit()

    def remove_user(self, user_id, chat_id):
        cursor = self.conn.cursor()
        cursor.execute(sql.REMOVE_USER, (chat_id, user_id))
        self.conn.commit()
    
    def get_user_in_chat(self, chat_id):
        cursor = self.conn.cursor()
        cursor.execute(sql.GET_USER, (chat_id,))
        data = cursor.fetchall()
        self.conn.commit()
        return data
    
    def get_number_user_in_chat(self, chat_id):
        cursor = self.conn.cursor()
        cursor.execute(sql.COUNT_USER_IN_CHAT, (chat_id,))
        data = cursor.fetchall()
        self.conn.commit()
        return data

    def close_connection(self):
        self.conn.close()
