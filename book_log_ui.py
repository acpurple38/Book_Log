
import sys

import PyQt6.QtCore as QCore
import PyQt6.QtWidgets as QWidge
import PyQt6.QtGui as QGUI

class BookTableModel(QCore.QAbstractTableModel):
    def __init__(self, table_data = None, parent = None):
        super().__init__()
        if table_data is None:
            table_data = [[]]
        
        self.table_data = table_data

        self.headers = ["Title", "Author","Date Finished"]
    
    def rowCount(self, parent = None, *args, **kwargs):
        return len(self.table_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def headerData(self, section, orientation, role = None):
        if role == QCore.Qt.ItemDataRole.DisplayRole and orientation == QCore.Qt.Orientation.Horizontal:
            return self.headers[section]

class BookTableView(QWidge.QTableView):
    def __init__(self):
        super().__init__()
        # title = QWidge.QHeaderView
        self.setVisible(True)

    def resizeEvent(self, event):
        width = event.size().width()
        self.setColumnWidth(0, int(width * 0.40))
        self.setColumnWidth(1, int(width * 0.40))
        self.setColumnWidth(2, int(width * 0.20))


class BookWidge(QWidge.QWidget):
    def __init__(self):
        super().__init__()

        self.search_input = QWidge.QLineEdit()
        self.add_button = QWidge.QPushButton('add')
        self.display = BookTableView()
        self.display.setModel(BookTableModel())

        grid = QWidge.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.search_input, 1, 1)
        grid.addWidget(self.add_button, 1, 2)
        grid.addWidget(self.display, 2, 1, 4, 4)
        self.setLayout(grid)


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

