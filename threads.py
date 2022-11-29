import os.path

from PyQt5.QtCore import QThread
from time import  sleep
from PIL import ImageQt
from pynotifier import Notification
from ocr import OcrReader


class OcrThread(QThread):

    def __init__(self, queue):
        super().__init__()
        self.work_queue = queue
        self.running = True
        self.reader = OcrReader(0.1)
        icon = os.path.abspath("icon.ico")
        self.notify_ok = Notification(title="Shotxt", icon_path=icon, description=f"Ocr finish!")
        self.notify_err = Notification(title="Shotxt", icon_path=icon, description=f"No text find!")

    def run(self):
        while self.running:
            if not self.work_queue.empty():
                print(f"Ocr got image!")
                img = self.work_queue.get()
                img = ImageQt.fromqimage(img)
                if self.reader.readtext(img):
                    self.notify_ok.send()
                else:
                    self.notify_err.send()
            else:
                pass
            sleep(0.1)
        print(f"Ocr quit")


# class SingalThread(QThread):
#     def __init__(self, rec):
#         super().__init__()
#         self.rec = rec
#         self.running = True
#
#     def run(self) -> None:
#         while self.running:
#             self.rec.show()
#             sleep(10)