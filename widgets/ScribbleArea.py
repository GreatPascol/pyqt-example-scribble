# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *


class ScribbleArea(QWidget):
    def __init__(self, parent=None):
        super(ScribbleArea, self).__init__(parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.modified = False
        self.scribbling = False
        self.currentPenWidth = 1
        self.currentPenColor = Qt.black
        self.image = None
        self.lastPoint = None

    def paintEvent(self, QPaintEvent):
        if self.image is not None:
            painter = QPainter(self)
            dirtyRect = QPaintEvent.rect()
            painter.drawImage(dirtyRect, self.image, dirtyRect)

