# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from widgets.ScribbleArea import ScribbleArea


class ScribbleWindow(QMainWindow):
    def __init__(self):
        super(ScribbleWindow, self).__init__()

        self.scribbleArea = ScribbleArea(self)
        self.saveAsMenu = QMenu()
        self.fileMenu = QMenu()
        self.optionMenu = QMenu()
        self.helpMenu = QMenu()
        self.openAct = None
        self.saveAsActs = []
        self.exitAct = None
        self.penColorAct = None
        self.penWidthAct = None
        self.printAct = None
        self.clearScreenAct = None
        self.aboutAct = None


        self.initUI()

    def initUI(self):
        self.setCentralWidget(self.scribbleArea)
        self.createActions()
        self.createMenus()
        self.setWindowTitle(u"Scribble")
        self.resize(500, 500)

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

    def open(self):
        if self.maybeSave():
            fileName = QFileDialog.getOpenFileName(self, u"Open File", QDir.currentPath())
            if not fileName.isEmpty():
                self.scribbleArea.openImage(fileName)

    def save(self):
        action = self.sender()
        self.saveFile(action.data().toByteArray())

    def penColor(self):
        newColor = QColorDialog.getColor(self.scribbleArea.currentPenColor)
        if newColor.isValid():
            self.scribbleArea.setPenColor(newColor)

    def penWidth(self):
        newWidth, ok = QInputDialog.getInt(self, u"scribble",
                                           u"Select pen width: ",
                                           self.scribbleArea.currentPenWidth,
                                           1, 50, 1)
        if ok:
            self.scribbleArea.setPenWidth(newWidth)

    def about(self):
        QMessageBox.about(self, u"About Scribble",
                          u"<p>The <b>Scribble</b> example shows how to use QMainWindow as the "
                          u"base widget for an application, and how to reimplement some of "
                          u"QWidget's event handlers to receive the events generated for "
                          u"the application's widgets:</p><p> We reimplement the mouse event "
                          u"handlers to facilitate drawing, the paint event handler to "
                          u"update the application and the resize event handler to optimize "
                          u"the application's appearance. In addition we reimplement the "
                          u"close event handler to intercept the close events before "
                          u"terminating the application.</p><p> The example also demonstrates "
                          u"how to use QPainter to draw an image in real time, as well as "
                          u"to repaint widgets.</p>")

    def createActions(self):
        self.openAct = QAction(u"&Open...", self)
        self.openAct.setShortcut(QKeySequence.Open)
        self.openAct.triggered.connect(self.open)

        for fmt in QImageWriter.supportedImageFormats():
            tmpAction = QAction("&%s..." % QString(fmt).toUpper(), self)
            tmpAction.setData(fmt)
            tmpAction.triggered.connect(self.save)
            self.saveAsActs.append(tmpAction)

        self.printAct = QAction("&Print...", self)
        self.printAct.triggered.connect(self.scribbleArea.printImage)

        self.exitAct = QAction("&Exit...", self)
        self.exitAct.setShortcut(QKeySequence.Quit)
        self.exitAct.triggered.connect(self.close)

        self.penColorAct = QAction("&Pen Color...", self)
        self.penColorAct.triggered.connect(self.penColor)
        self.penWidthAct = QAction("&Pen Width...", self)
        self.penWidthAct.triggered.connect(self.penWidth)

        self.clearScreenAct = QAction("&Clear Screen...", self)
        self.clearScreenAct.setShortcut("Ctrl+L")
        self.clearScreenAct.triggered.connect(self.scribbleArea.clearImage)
        self.aboutAct = QAction("&About...", self)
        self.aboutAct.triggered.connect(self.about)

    def createMenus(self):
        self.saveAsMenu = QMenu("Save As", self)
        for action in self.saveAsActs:
            self.saveAsMenu.addAction(action)

        self.fileMenu = QMenu("File", self)
        self.fileMenu.addAction(self.openAct);
        self.fileMenu.addMenu(self.saveAsMenu)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.optionMenu = QMenu("Options", self)
        self.optionMenu.addAction(self.penColorAct)
        self.optionMenu.addAction(self.penWidthAct)
        self.optionMenu.addSeparator()
        self.optionMenu.addAction(self.clearScreenAct)

        self.helpMenu = QMenu("Help", self)
        self.helpMenu.addAction(self.aboutAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.optionMenu)
        self.menuBar().addMenu(self.helpMenu)

    def maybeSave(self):
        if self.scribbleArea.isModified():
            ret = QMessageBox.warning(self, "Scribble",
                                      u"The image has been modified.\n"
                                      u"Do you want to save your changes?",
                                      QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.saveFile("png")
            elif ret == QMessageBox.Cancel:
                return False
        return True

    def saveFile(self, fileFormat):
        initialPath = QDir.currentPath() + "/untitled." + fileFormat
        fileName = QFileDialog.getSaveFileName(self, "Save As",
                                               initialPath,
                                               "%s Files (*.%s);;All Files (*)" % (QString(fileFormat).toUpper(), QString(fileFormat)))
        if fileName.isEmpty():
            return False
        else:
            return self.scribbleArea.saveImage(fileName, fileFormat)

if __name__ == '__main__':
    import sys

    qpp = QApplication(sys.argv)
    window = ScribbleWindow()
    window.show()
    sys.exit(qpp.exec_())
