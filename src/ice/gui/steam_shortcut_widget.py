"""
steam_preview_widget.py

Created by Scott Rice on 8-22-2014
"""

from PyQt4 import QtGui


class SteamShortcutWidget(QtGui.QWidget):

  IMAGE_WIDTH = 460
  IMAGE_HEIGHT = 215

  def __init__(self):
    super(SteamShortcutWidget, self).__init__()

    self.initUI()

  def initUI(self):
    picture = QtGui.QLabel(self)
    picture.setMaximumSize(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
    picture.setMinimumSize(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)

    nameLabel = QtGui.QLabel()
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(nameLabel)
    hbox.addStretch(1)

    vbox = QtGui.QVBoxLayout()
    vbox.addWidget(picture)
    vbox.addLayout(hbox)

    self.setLayout(vbox)

    self.pictureWidget = picture
    self.nameLabel = nameLabel

  def setName(self, name):
    self.nameLabel.setText(name)

  def setImage(self, path):
    pixmap = QtGui.QPixmap(path)
    # TODO: Make this handle odd aspect ratios the same way Steam does
    # TODO: Handle null paths (ideally use the same image that Steam does)
    pixmap = pixmap.scaled(self.IMAGE_WIDTH, self.IMAGE_HEIGHT)
    self.pictureWidget.setPixmap(pixmap)
