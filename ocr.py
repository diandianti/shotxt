import easyocr

import numpy as np
import pyperclip
from PIL import Image, ImageQt


class OcrReader:
    def __init__(self, thd = 0.5):
        self.thd = thd
        self.reader = easyocr.Reader(['ch_sim','en'], gpu=False)

    def readtext(self, img):
        if isinstance(img, Image.Image):
            # img.save("debug.png")
            img = np.array(img)
        elif isinstance(img, PyQt5.QtGui.QPixmap):
            img = ImageQt.fromqimage(img)
            img = np.array(img)
        else:
            pass

        res = self.reader.readtext(img)
        return self.post_process(res)

    def post_process(self, res: list):
        if not len(res):
            return False

        all_txt = [i[1] for i in res if i[2] > self.thd]
        all = " ".join(all_txt)
        pyperclip.copy(all)
        return True
