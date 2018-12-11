CREATE_TABLE_USER = """
CREATE TABLE IF NOT EXISTS Users(
    user_id INTEGER PRIMARY KEY, 
    first_name TEXT,
    last_name TEXT,
    username TEXT
);
"""

CREATE_TABLE_USERCHAT="""
CREATE TABLE IF NOT EXISTS UserChat(
    chat_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (chat_id, user_id)
);
"""

#remind_prime = 0 -> false / 1 -> true
CREATE_TABLE_CHAT="""
CREATE TABLE IF NOT EXISTS Chat(
    chat_id INTEGER PRIMARY KEY,
    bool_enable INTEGER,
    bool_remind_prime INTEGER,
    remind_prime_list TEXT,
    bool_prime_list INTEGER
);
"""

INSERT_USER = """
INSERT OR REPLACE INTO Users(user_id, first_name, last_name, username)
VALUES (?, ?, ?, ?);
"""

INSERT_USER_CHAT = """
INSERT OR REPLACE INTO UserChat(chat_id, user_id)
VALUES (?, ?);
"""

INSERT_CHAT = """
INSERT OR REPLACE INTO Chat(chat_id, bool_enable, bool_remind_prime, remind_prime_list, bool_prime_list)
VALUES (?,?,?,?,?);
"""

SET_ENABLE = """
UPDATE Chat
SET bool_enable = ?
WHERE chat_id = ?;
"""

SET_BOOL_PRIME_LIST="""
UPDATE Chat
SET bool_prime_list= ?
WHERE chat_id=?;
"""

SET_OPTION_CHAT_REMIND_PRIME="""
UPDATE Chat
SET bool_remind_prime=?
WHERE chat_id=?;
"""

REMOVE_USER = """
DELETE 
FROM UserChat
WHERE chat_id = ? AND user_id = ?;
"""

GET_USER = """
SELECT us.*
FROM UserChat AS ch
INNER JOIN Users AS us
ON ch.user_id = us.user_id
WHERE ch.chat_id = ?;
"""

GET_OPTION_CHAT= """
SELECT *
FROM Chat
WHERE chat_id = ?;
"""

GET_LIST_REMINDER="""
SELECT remind_prime_list
FROM Chat
WHERE chat_id = ?;
"""
SET_LIST_REMINDER="""
UPDATE Chat
SET remind_prime_list=?
WHERE chat_id=?;
"""

COUNT_USER_IN_CHAT = """
SELECT count(user.user_id) as cnt
FROM UserChat AS chat
INNER JOIN Users AS user
ON chat.user_id = user.user_id
WHERE chat.chat_id = ?;
"""