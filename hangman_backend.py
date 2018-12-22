import sqlite3
import random


class Backend(object):
    def __init__(self, newBackend=False):

        if newBackend: self.clear_all()

        db = sqlite3.connect("hangman.db")
        cur = db.cursor()

        sql = "CREATE TABLE IF NOT EXISTS words( id_word INTEGER PRIMARY KEY NOT NULL, word TEXT NOT NULL UNIQUE);"
        cur.execute(sql)

        sql = "CREATE TABLE IF NOT EXISTS hangman (" \
                        "id_game INTEGER PRIMARY KEY NOT NULL, word_id INTEGER NOT NULL, " \
                        "number_of_tries INTEGER NOT NULL, won BOOLEAN NOT NULL, " \
                        "FOREIGN KEY(word_id) REFERENCES words(id_word));"
        cur.execute(sql)

        db.commit()
        db.close()

    def add_game(self, txt, number_of_tries=0, won=False):
        db = sqlite3.connect("hangman.db")
        cur = db.cursor()
        cur.execute("INSERT INTO hangman VALUES (NULL, ?, ?, ?)", (txt, number_of_tries, won))
        db.commit()
        db.close()

    def add_word(self, txt):

        if not self.get_word_id(txt):
            db = sqlite3.connect("hangman.db")
            cur = db.cursor()
            cur.execute("INSERT INTO words VALUES (NULL, ?)", (txt,))
            db.commit()
            db.close()
            return True
        else:
            return False

    def view_all_games(self):
        db = sqlite3.connect("hangman.db")
        cur = db.cursor()
        cur.execute("SELECT * FROM hangman")
        rows = cur.fetchall()
        db.close()
        return rows

    def view_all_words(self):
        db = sqlite3.connect("hangman.db")
        cur = db.cursor()
        cur.execute("SELECT * FROM words")
        rows = cur.fetchall()
        db.close()
        return rows

    def get_word(self, index):
        db = sqlite3.connect("hangman.db")
        cur = db.cursor()
        cur.execute("SELECT word FROM words WHERE id_word=?", (index,))
        rows = cur.fetchall()
        db.close()
        if rows:
            return rows[0][0]
        else:
            return False

    def get_random_word(self):
        return random.choice(self.view_all_words())[1]

    def get_word_id(self, txt):
        db = sqlite3.connect("hangman.db")
        cur = db.cursor()
        cur.execute("SELECT id_word FROM words WHERE word=?", (txt,))
        rows = cur.fetchall()
        db.close()
        if rows:
            return rows[0][0]
        else:
            return False

    def delete_word(self, txt):

        if self.get_word_id(txt):
            db = sqlite3.connect("hangman.db")
            cur = db.cursor()
            cur.execute("DELETE FROM words WHERE word=?", (txt,))
            db.commit()
            db.close()
            return True
        else:
            return False

    def delete_word_by_id(self, index):

        if self.get_word(index):
            db = sqlite3.connect("hangman.db")
            cur = db.cursor()
            cur.execute("DELETE FROM words WHERE id_word=?", (index,))
            db.commit()
            db.close()
            return True
        else:
            return False

    def get_win(self):
        db = sqlite3.connect("hangman.db")
        cur = db.cursor()
        cur.execute("SELECT count(won) FROM hangman WHERE won=1")
        rows = cur.fetchall()
        db.close()
        if rows:
            return rows[0][0]
        else:
            return False

    def get_lost(self):
        db = sqlite3.connect("hangman.db")
        cur = db.cursor()
        cur.execute("SELECT count(won) FROM hangman WHERE won=0")
        rows = cur.fetchall()
        db.close()
        if rows:
            return rows[0][0]
        else:
            return False

    def clear_all(self):
        db = sqlite3.connect("hangman.db")
        cur = db.cursor()
        cur.execute("DROP TABLE IF EXISTS hangman")
        cur.execute("DROP TABLE IF EXISTS words")
        db.commit()
        db.close()


# we do some tests here
if __name__ == "__main__":
    print("This is my backend part")

    restart = True
    bk = Backend(restart)

    # adding words from a text file I downloaded
    if restart:
        words = open("words.txt", "r").read().split("\n")
        for word in words:
            bk.add_word(word)

    # print(bk.view_all_words())

    # bk.add_game(20, 4, False)
    print(bk.view_all_games())
    #
    # bk.add_word("aquarium")
    # a = bk.get_word_id("aquarium")
    # print(a)
    # print(bk.get_word(a))
    # print(bk.delete_word("aquarium"))
    # print(bk.get_word(a))
    # print(bk.delete_word_by_id(a))
    # print(bk.delete_word_by_id(a))
    # print(bk.get_word_id("aquarium"))

    # print(bk.get_random_word())

    print(bk.get_win())
    print(bk.get_lost())

    # deleting all information in database
    # bk.clear_all()
