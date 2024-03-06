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
        

    def add_entry(self, title, author, date):
        if date == "":
            date = str(datetime.date.today())
        self.librarian.execute("INSERT INTO Book VALUES(?, ?, ?)", (title, author, date))
        self.library.commit()

    def search_entries(self, title, author, date):
        data = []
        if title != "":
            self.librarian.execute("SELECT * FROM Book WHERE Title LIKE ('%' || ? || '%') ORDER BY Date ASC", (title,))
            new_data = self.librarian.fetchall()
            for d in new_data:
                if d not in data:
                    data.append(d)

        if author != "":
            self.librarian.execute("SELECT * FROM Book WHERE Author LIKE ('%' || ? || '%') ORDER BY Date ASC", (author,))
            new_data = self.librarian.fetchall()
            for d in new_data:
                if d not in data:
                    data.append(d)
        
        if date != "":
            self.librarian.execute("SELECT * FROM Book WHERE Date LIKE ('%' || ? || '%') ORDER BY Date ASC", (date,))
            new_data = self.librarian.fetchall()
            for d in new_data:
                if d not in data:
                    data.append(d)
        return data

    def show_log(self):
        self.librarian.execute("SELECT * FROM Book ORDER BY Date ASC")
        data = self.librarian.fetchall()
        return data

if __name__ == "__main__":
    libraryOne = Book_Log()
    print(libraryOne.list_tables)
    libraryOne.library.close()

