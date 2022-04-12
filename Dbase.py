import sqlite3

connect = sqlite3.connect("tgbot_db.db")


# def print_db():
#     cursor = connect.cursor()
#     cursor.execute("""CREATE TABLE tbdb
#                       (user_id int, user_name text, user_prog int)
#                    """)
#     connect.commit()


def init():
    print("Prepare DB ")


def readScore():
    cursor = connect.cursor()
    cursor.execute("SELECT user_name, user_prog FROM tbdb")
    rows = cursor.fetchall()
    return rows;


def saveScore(userId, userName, userScore):
    cursor = connect.cursor()
    cursor.execute("INSERT OR IGNORE INTO tbdb VALUES (?,?,?);", (userId, userName, userScore))
    cursor.execute("UPDATE tbdb SET user_prog = ? WHERE user_id = ?;", (userScore, userId))
    connect.commit()

saveScore(88006543,"Georgiy", 80)
print(readScore())
# UPDATE visits SET hits = hits + 1 WHERE ip LIKE $ip;
# readScore()

