"""
steam_preview_widget.py

Created by Scott Rice on 8-22-2014
"""

from PyQt4 import QtGui

from steam_shortcut_widget import SteamShortcutWidget


class SteamPreviewWidget(QtGui.QWidget):

  def __init__(self):
    super(SteamPreviewWidget, self).__init__()
    self.roms = []

    self.initUI()
    self.resizeEvent(None)

  def initUI(self):
    self.grid = QtGui.QGridLayout()
    self.setLayout(self.grid)

  def redraw(self):
    self.clear()
    self.drawROMs()

  def clear(self):
    for index in range(0, self.grid.count()):
      item = self.grid.itemAt(index)
      if item is not None:
        widget = item.widget()
        if widget is not None:
          self.grid.removeWidget(widget)
          widget.deleteLater()

  def drawROMs(self):
    for idx in range(0, len(self.roms)):
      rom = self.roms[idx]
      row = idx / self.numColumns
      col = idx % self.numColumns
      widget = SteamShortcutWidget()
      widget.setName(rom.name())
      widget.setImage(rom.to_shortcut().custom_image(self.user))
      self.grid.addWidget(widget, row, col)

  def setNumberOfGridColumns(self, numGridColumns):
    if self.numGridColumns != numGridColumns:
      self.numGridColumns = numGridColumns
      self.redraw()

  def setROMs(self, roms):
    self.roms = roms
    self.redraw()

  def setUser(self, user):
    self.user = user
    self.redraw()

  def resizeEvent(self, event):
    self.numColumns = self.width() / (SteamShortcutWidget.IMAGE_WIDTH + 10)
    self.redraw()
