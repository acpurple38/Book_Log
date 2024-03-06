
import sys

import PyQt6.QtCore as QCore
import PyQt6.QtWidgets as QWidge
import PyQt6.QtGui as QGUI
from book_db import Book_Log

class BookTableModel(QCore.QAbstractTableModel):
    def __init__(self, table_data = None, parent = None):
        super().__init__()

        if table_data is None:
            table_data = [["", "", ""]]
        
        self.table_data = table_data

        self.headers = ["Title", "Author","Date Finished"]
        
        self.sort_changed_signal = QCore.pyqtSignal(int, int)
    
    def rowCount(self, parent = None, *args, **kwargs):
        return len(self.table_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def headerData(self, section, orientation, role = None):
        if role == QCore.Qt.ItemDataRole.DisplayRole and orientation == QCore.Qt.Orientation.Horizontal:
            return self.headers[section]
        
    def data(self, index, role = None):
        if role == QCore.Qt.ItemDataRole.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.table_data[row][column]
            return value
        
    def update_data(self, new_data):
        self.layoutAboutToBeChanged.emit()
        self.table_data = new_data
        self.layoutChanged.emit()
    

class BookTableView(QWidge.QTableView):
    def __init__(self):
        super().__init__()
        self.setVisible(True)

    def resizeEvent(self, event):
        width = event.size().width()
        self.setColumnWidth(0, int(width * 0.40))
        self.setColumnWidth(1, int(width * 0.40))
        self.setColumnWidth(2, int(width * 0.20))


class BookWidge(QWidge.QWidget):
    def __init__(self):
        super().__init__()

        self.library = Book_Log()

        self.title_input = QWidge.QLineEdit("Title")
        self.author_input = QWidge.QLineEdit("Author")
        self.date_input = QWidge.QLineEdit("Date")
        self.add_button = QWidge.QPushButton('add')
        self.search_button = QWidge.QPushButton('search')
        self.rem_button = QWidge.QPushButton('remove')
        self.display = BookTableView()
        self.display_model = BookTableModel(self.library.show_log())
        self.display.setModel(self.display_model)

        self.add_button.clicked.connect(self.add_entry)
        self.search_button.clicked.connect(self.search_entries)
        self.rem_button.clicked.connect(self.rem_entry)

        grid = QWidge.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.title_input, 1, 1)
        grid.addWidget(self.author_input, 2, 1)
        grid.addWidget(self.date_input, 3, 1)
        grid.addWidget(self.add_button, 1, 2)
        grid.addWidget(self.search_button, 2, 2)
        grid.addWidget(self.rem_button, 3, 2)
        grid.addWidget(self.display, 4, 1, 4, 4)
        self.setLayout(grid)

    def add_entry(self):
        title = self.title_input.text()
        author = self.author_input.text()
        date = self.date_input.text()
        self.library.add_entry(title, author, date)
        self.display_model.update_data(self.library.show_log())
        self.title_input.clear()
        self.author_input.clear()
        self.date_input.clear()

    def search_entries(self):
        title = self.title_input.text()
        author = self.author_input.text()
        date = self.date_input.text()
        self.display_model.update_data(self.library.search_entries(title, author, date))

    def rem_entry(self):
        title = self.title_input.text()
        author = self.author_input.text()
        date = self.date_input.text()
        self.library.rem_entry(title, author, date)
        self.display_model.update_data(self.library.show_log())

class BookWindow(QWidge.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Book Log")
        self.resize(500, 400)
        self.center = BookWidge()
        self.setCentralWidget(self.center)
        
        self.show()

def main():
    app = QWidge.QApplication(sys.argv)
    ui = BookWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

