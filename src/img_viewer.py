from PyQt5 import QtCore, QtWidgets, QtGui
import sys

from PyQt5.QtGui import QResizeEvent


class Slides(QtWidgets.QWidget):
    def __init__(self, image_files, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.lay = QtWidgets.QVBoxLayout()
        self.image_files = image_files
        self.label = QtWidgets.QLabel("", self)
        self.lay.addWidget(self.label)
        self.step = 0
        self.lis = len(self.image_files)
        for i in range(len(self.image_files)):
            image = QtGui.QPixmap(self.image_files[i])
            self.image_files[i] = image
        self.image = self.image_files[self.step]
        self.label.setPixmap(image)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        if self.lis > 1:
            self.cont = QtWidgets.QWidget()
            self.lay1 = QtWidgets.QHBoxLayout()
            self.button1 = QtWidgets.QPushButton(">")
            self.button2 = QtWidgets.QPushButton("<")
            self.lay1.addWidget(self.button2)
            self.lay1.addWidget(self.button1)
            self.button1.clicked.connect(lambda state: self.switch(1))
            self.button2.clicked.connect(lambda state: self.switch(-1))
            self.cont.setLayout(self.lay1)
            self.lay.addWidget(self.cont)
        self.setLayout(self.lay)

    def switch(self, x):
        self.step += x
        self.step = self.step % self.lis
        self.image = self.image_files[self.step]
        self.label.setPixmap(self.image)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.label.setFixedWidth(self.width())
        if self.image.width() > self.image.height():
            self.image = self.image_files[self.step].scaledToWidth(
                int(0.8 * self.width())
            )
        else:
            self.image = self.image_files[self.step].scaledToHeight(
                int(0.8 * self.height())
            )
        if self.lis>1:
            self.cont.setFixedWidth(self.label.width())
        self.label.setPixmap(self.image)