import queue

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from queue import Queue


class Snipper(QtWidgets.QWidget):
    def __init__(self, parent, queue_or_ocr, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)

        self.queue = queue_or_ocr

        self.setWindowTitle("TextShot")
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog
        )
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)

        # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.start, self.end = QtCore.QPoint(), QtCore.QPoint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            # print(f"get esc exit!")
            self.hide()
            # QtWidgets.QApplication.quit()

        return super().keyPressEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 100))
        painter.drawRect(0, 0, self.width(), self.height())

        if self.start == self.end:
            return super().paintEvent(event)

        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255), 3))
        painter.setBrush(painter.background())
        painter.drawRect(QtCore.QRect(self.start, self.end))
        return super().paintEvent(event)

    def mousePressEvent(self, event):
        self.start = self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.start == self.end:
            return super().mouseReleaseEvent(event)

        self.hide()
        QtWidgets.QApplication.processEvents()
        shot = self.screen.copy(
            min(self.start.x(), self.end.x()),
            min(self.start.y(), self.end.y()),
            abs(self.start.x() - self.end.x()),
            abs(self.start.y() - self.end.y()),
        )

        self.start.setX(0)
        self.start.setY(0)
        self.end.setX(0)
        self.end.setY(0)
        print(f"Get shot {shot}")

        if isinstance(self.queue, queue.Queue):
            self.queue.put(shot)
        else:
            self.queue.readtext(shot)
            QtWidgets.QApplication.quit()


    def show(self) -> None:
        screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos()).grabWindow(0)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(screen))
        self.setPalette(palette)
        self.screen = screen
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        super().show()

    def hide(self) -> None:
        QtWidgets.QApplication.restoreOverrideCursor()
        super(Snipper, self).hide()
