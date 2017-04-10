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

    def paintEvent(self, event):
        if self.image is not None:
            painter = QPainter(self)
            dirtyRect = event.rect()
            painter.drawImage(dirtyRect, self.image, dirtyRect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            self.scribbling = True

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.scribbling:
            self.drawLineTo(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.scribbling:
            self.drawLineTo(event.pos())
            self.scribbling = False

    def resizeEvent(self, event):
        pass

    def drawLineTo(self, endPoint):
        pass

    def openImage(self, fileName):
        loadedImage = QImage()
        if not loadedImage.load(fileName):
            return False
        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = True
        self.update()
        return True

    def saveImage(self, fileName, fileFormat):
        visibleImage = QImage(self.image)
        self.resizeImage(visibleImage, self.size())
        if visibleImage.save(fileName, fileFormat):
            self.modified = True
            return True
        else:
            return False

    def resizeImage(self, image, newSize):
        pass

    def clearImage(self):
        self.image.fill(qRgb(255, 255, 255))
        self.modified = True
        self.update()

    def printImage(self):
        pass

    def setPenColor(self, newColor):
        self.currentPenColor = newColor

    def setPenWidth(self, newPenWidth):
        self.currentPenWidth = newPenWidth

    def isModified(self):
        return self.modified
