import sys

from screenshot import Snipper
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSize
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from threads import OcrThread
from queue import Queue
from ocr import OcrReader

def do_ocr():
    print(f"In do ocr!")


def once():
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    mw = QMainWindow()
    reader = OcrReader()
    snipper = Snipper(mw, reader)
    snipper.show()
    sys.exit(app.exec_())



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About shotxt")
        self.setFixedSize(QSize(400, 300))
        self.label = QLabel("This is about me")
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)


class Trayer(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.ocr = QAction("OCR")
        self.ocr_to_chinese = QAction("OCR+")
        self.act_quit = QAction("Quit")
        self.about = QAction("About shotxt")

        self.menu = QMenu()
        self.menu.addAction(self.ocr)
        self.menu.addAction(self.ocr_to_chinese)
        self.menu.addAction(self.about)
        self.menu.addAction(self.act_quit)
        self.setContextMenu(self.menu)

        self.setToolTip("Ocr")

        self.icon = QIcon("icon.png")
        self.setIcon(self.icon)
        self.setVisible(True)


def main():
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    mw = MainWindow()
    mw.hide()

    tray = Trayer()
    tray.act_quit.triggered.connect(app.quit)
    tray.about.triggered.connect(mw.show)

    mq = Queue(maxsize=1)

    snipper = Snipper(mw, mq)
    tray.ocr.triggered.connect(snipper.show)
    tray.ocr_to_chinese.triggered.connect(snipper.show)
    tray.activated.connect(snipper.show)

    ocr = OcrThread(mq)
    ocr.start()

    sys.exit(app.exec_())


class CLI:
    def once(self):
        once()

    def background(self):
        main()

    def ocr(self):
        do_ocr()


if __name__ == "__main__":
    import fire
    fire.Fire(CLI())
