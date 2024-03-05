import sqlite3
import datetime

class Book_Log():
    def __init__(self):
        self.library = self.open_log()
        self.librarian = self.library.cursor()
        self.list_tables = []
        try:
            self.list_tables.append(self.librarian.execute("SELECT * from Book").fetchall())
        except sqlite3.OperationalError:
            self.list_tables.append(self.librarian.execute("""CREATE TABLE Book(Title TEXT,
            Author TEXT, Date TEXT);""").fetchall())

    def open_log(self):
        con = None

        try:
            con = sqlite3.connect("book_log.db")
            return con
        except:
            print(sqlite3.Error)
        

    def add_entry(self, title, author, date=str(datetime.date.today())):
        self.librarian.execute("INSERT INTO Book VALUES(?, ?, ?)", (title, author, date))
        self.library.commit()

    def search_entries(self, title, author, date):
        pass

    def show_log(self):
        self.librarian.execute("SELECT * FROM Book ORDER BY Date ASC")
        data = self.librarian.fetchall()
        return data

if __name__ == "__main__":
    libraryOne = Book_Log()
    print(libraryOne.list_tables)
    libraryOne.library.close()

