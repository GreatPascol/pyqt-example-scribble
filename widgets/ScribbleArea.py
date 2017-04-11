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
        self.image = QImage()
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
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.image = self.resizeImage(self.image, QSize(newWidth, newHeight))
            self.update()
        super(ScribbleArea, self).resizeEvent(event)

    def drawLineTo(self, endPoint):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.currentPenColor, self.currentPenWidth,
                            Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(self.lastPoint, endPoint)
        self.modified = True

        rad = (self.currentPenWidth / 2) + 2  # specialize the rect to update for optimization
        self.update(QRect(self.lastPoint, endPoint).normalized()
                    .adjusted(-rad, -rad, +rad, +rad))
        self.lastPoint = endPoint

    def openImage(self, fileName):
        loadedImage = QImage()
        if not loadedImage.load(fileName):
            return False
        newSize = loadedImage.size().expandedTo(self.size())
        loadedImage = self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = True
        self.update()
        return True

    def saveImage(self, fileName, fileFormat):
        visibleImage = self.resizeImage(self.image, self.size())
        if visibleImage.save(fileName, fileFormat):
            self.modified = False
            return True
        else:
            return False

    @staticmethod
    def resizeImage(oldImage, newSize):
        if oldImage is None or oldImage.size() == newSize:
            return oldImage
        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        painter = QPainter(newImage)
        painter.drawImage(QPoint(0, 0), oldImage)
        return newImage

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


if __name__ == '__main__':
    import sys

    qpp = QApplication(sys.argv)
    window = ScribbleArea()
    window.show()
    sys.exit(qpp.exec_())
