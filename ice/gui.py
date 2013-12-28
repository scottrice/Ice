import sys
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog
from PyQt4 import QtCore
from ui import ui_windowMain, ui_windowSettings

# Ice
import ConfigParser
import settings

from error.config_error import ConfigError

from steam_shortcut_manager import SteamShortcutManager

import steam_user_manager
import filesystem_helper as fs
import console
from rom_manager import IceROMManager
from process_helper import steam_is_running
from grid_image_manager import IceGridImageManager
from ice_logging import ice_logger

class WindowSettings(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = ui_windowSettings.Ui_windowSettings()
        self.ui.setupUi(self)

        # actions
        self.ui.btnSave.pressed.connect(self._saveSettings)
        self.ui.btnCancel.pressed.connect(self._cancel)

        self.ui.openBinNES.pressed.connect(self.openBinNES)
        self.ui.openBinSNES.pressed.connect(self.openBinSNES)
        self.ui.openBinN64.pressed.connect(self.openBinN64)
        self.ui.openBinGameCube.pressed.connect(self.openBinGameCube)
        self.ui.openBinWii.pressed.connect(self.openBinWii)
        self.ui.openBinPS1.pressed.connect(self.openBinPS1)
        self.ui.openBinPS2.pressed.connect(self.openBinPS2)
        self.ui.openBinGenesis.pressed.connect(self.openBinGenesis)
        self.ui.openBinDreamcast.pressed.connect(self.openBinDreamcast)
        self.ui.openBinGameBoy.pressed.connect(self.openBinGameBoy)
        self.ui.openBinGBA.pressed.connect(self.openBinGBA)
        self.ui.openBinNDS.pressed.connect(self.openBinNDS)

        # load current saved settings
        self._loadSettings()

    def _loadSettings(self):
        try:
            for consoleentry in settings.consoles():
                if settings.consoles()[consoleentry]['emulator'] != '':
                    emulator = settings.consoles()[consoleentry]['emulator']

                    if consoleentry == 'Nintendo Entertainment System':
                        self.ui.pathNES.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdNES.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Super Nintendo':
                        self.ui.pathSNES.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdSNES.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Nintendo 64':
                        self.ui.pathN64.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdN64.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Nintendo Gamecube':
                        self.ui.pathGameCube.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdGameCube.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Nintendo Wii':
                        self.ui.pathWii.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdWii.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Playstation 1':
                        self.ui.pathPS1.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdPS1.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Playstation 2':
                        self.ui.pathPS2.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdPS2.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Sega Genesis':
                        self.ui.pathGenesis.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdGenesis.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Sega Dreamcast':
                        self.ui.pathDreamcast.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdDreamcast.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Nintendo Gameboy':
                        self.ui.pathGameBoy.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdGameBoy.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Gameboy Advance':
                        self.ui.pathGBA.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdGBA.setText(settings.emulators()[emulator]['command'])
                    elif consoleentry == 'Nintendo DS':
                        self.ui.pathNDS.setText(settings.emulators()[emulator]['location'])
                        self.ui.cmdNDS.setText(settings.emulators()[emulator]['command'])

        except:
            print 'An error occured while loading configs'
            return

    def _saveSettings(self):
        # initialize config
        configEmulators = ConfigParser.ConfigParser()
        configEmulators.read(settings.user_emulators_path())
        configConsoles = ConfigParser.ConfigParser()
        configConsoles.read(settings.user_consoles_path())

        # check if emulator paths are empty - if so, don't save
        if self.ui.pathNES.text() != '':
            # add NES section to emulators.txt
            configEmulators.add_section('NES')
            configEmulators.set('NES', 'location', self.ui.pathNES.text())
            configEmulators.set('NES', 'command', self.ui.cmdNES.text())

            # add emulator NES to consoles.txt
            configConsoles.set('Nintendo Entertainment System', 'emulator', 'NES')

        # proceed with the rest of the support consoles
        if self.ui.pathSNES.text() != '':
            configEmulators.add_section('SNES')
            configEmulators.set('SNES', 'location', self.ui.pathSNES.text())
            configEmulators.set('SNES', 'command', self.ui.cmdSNES.text())
            configConsoles.set('Super Nintendo', 'emulator', 'SNES')
        if self.ui.pathN64.text() != '':
            configEmulators.add_section('N64')
            configEmulators.set('N64', 'location', self.ui.pathN64.text())
            configEmulators.set('N64', 'command', self.ui.cmdN64.text())
            configConsoles.set('Nintendo 64', 'emulator', 'N64')
        if self.ui.pathGameCube.text() != '':
            configEmulators.add_section('Gamecube')
            configEmulators.set('Gamecube', 'location', self.ui.pathGameCube.text())
            configEmulators.set('Gamecube', 'command', self.ui.cmdGameCube.text())
            configConsoles.set('Nintendo Gamecube', 'emulator', 'Gamecube')
        if self.ui.pathWii.text() != '':
            configEmulators.add_section('Wii')
            configEmulators.set('Wii', 'location', self.ui.pathWii.text())
            configEmulators.set('Wii', 'command', self.ui.cmdWii.text())
            configConsoles.set('Nintendo Wii', 'emulator', 'Wii')
        if self.ui.pathPS1.text() != '':
            configEmulators.add_section('PS1')
            configEmulators.set('PS1', 'location', self.ui.pathPS1.text())
            configEmulators.set('PS1', 'command', self.ui.cmdPS1.text())
            configConsoles.set('Playstation 1', 'emulator', 'PS1')
        if self.ui.pathPS2.text() != '':
            configEmulators.add_section('PS2')
            configEmulators.set('PS2', 'location', self.ui.pathPS2.text())
            configEmulators.set('PS2', 'command', self.ui.cmdPS2.text())
            configConsoles.set('Playstation 2', 'emulator', 'PS2')
        if self.ui.pathGenesis.text() != '':
            configEmulators.add_section('Genesis')
            configEmulators.set('Genesis', 'location', self.ui.pathGenesis.text())
            configEmulators.set('Genesis', 'command', self.ui.cmdGenesis.text())
            configConsoles.set('Sega Genesis', 'emulator', 'Genesis')
        if self.ui.pathDreamcast.text() != '':
            configEmulators.add_section('Dreamcast')
            configEmulators.set('Dreamcast', 'location', self.ui.pathDreamcast.text())
            configEmulators.set('Dreamcast', 'command', self.ui.cmdDreamcast.text())
            configConsoles.set('Sega Dreamcast', 'emulator', 'Dreamcast')
        if self.ui.pathGameBoy.text() != '':
            configEmulators.add_section('Gameboy')
            configEmulators.set('Gameboy', 'location', self.ui.pathGameBoy.text())
            configEmulators.set('Gameboy', 'command', self.ui.cmdGameBoy.text())
            configConsoles.set('Nintendo Gameboy', 'emulator', 'Gameboy')
        if self.ui.pathGBA.text() != '':
            configEmulators.add_section('GBA')
            configEmulators.set('GBA', 'location', self.ui.pathGBA.text())
            configEmulators.set('GBA', 'command', self.ui.cmdGBA.text())
            configConsoles.set('Gameboy Advance', 'emulator', 'GBA')
        if self.ui.pathNDS.text() != '':
            configEmulators.add_section('NDS')
            configEmulators.set('NDS', 'location', self.ui.pathNDS.text())
            configEmulators.set('NDS', 'command', self.ui.cmdNDS.text())
            configConsoles.set('Nintendo DS', 'emulator', 'NDS')

        # save configs
        configEmulators.write(open(settings.user_emulators_path(), 'wb'))
        configConsoles.write(open(settings.user_consoles_path(), 'wb'))

        # hide settings windows
        self.setVisible(False)

    def _cancel(self):
        self.setVisible(False)

    def openBinNES(self):
        self.ui.pathNES.setText(QFileDialog.getOpenFileName())
    def openBinSNES(self):
        self.ui.pathSNES.setText(QFileDialog.getOpenFileName())
    def openBinN64(self):
        self.ui.pathN64.setText(QFileDialog.getOpenFileName())
    def openBinGameCube(self):
        self.ui.pathGameCube.setText(QFileDialog.getOpenFileName())
    def openBinWii(self):
        self.ui.pathWii.setText(QFileDialog.getOpenFileName())
    def openBinPS1(self):
        self.ui.pathPS1.setText(QFileDialog.getOpenFileName())
    def openBinPS2(self):
        self.ui.pathPS2.setText(QFileDialog.getOpenFileName())
    def openBinGenesis(self):
        self.ui.pathGenesis.setText(QFileDialog.getOpenFileName())
    def openBinDreamcast(self):
        self.ui.pathDreamcast.setText(QFileDialog.getOpenFileName())
    def openBinGameBoy(self):
        self.ui.pathGameBoy.setText(QFileDialog.getOpenFileName())
    def openBinGBA(self):
        self.ui.pathGBA.setText(QFileDialog.getOpenFileName())
    def openBinNDS(self):
        self.ui.pathNDS.setText(QFileDialog.getOpenFileName())

class WindowMain(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = ui_windowMain.Ui_MainWindow()
        self.ui.setupUi(self)

        # actions
        QtCore.QObject.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered()"), self._exitApp)
        QtCore.QObject.connect(self.ui.btnRunIce, QtCore.SIGNAL("pressed()"), self.startIce)
        QtCore.QObject.connect(self.ui.btnSettings, QtCore.SIGNAL("pressed()"), self.showSettings)

        # multiple windows
        self.windowSettings = WindowSettings()

    def startIce(self):
        # very similar to the one in ice.py
        try:
            if steam_is_running():
                ice_logger.log_error("Ice cannot be run while Steam is open. Please close Steam and try again")
                return
            ice_logger.log("Starting Ice")
            fs.create_directory_if_needed(fs.roms_directory(), log="Creating ROMs directory at %s" % fs.roms_directory())
            # Find all of the ROMs that are currently in the designated folders
            roms = console.find_all_roms()
            # Find the Steam Account that the user would like to add ROMs for
            user_ids = steam_user_manager.user_ids_on_this_machine()
            grid_manager = IceGridImageManager()
            for user_id in user_ids:
                ice_logger.log("Running for user %s" % str(user_id))
                # Load their shortcuts into a SteamShortcutManager object
                shortcuts_path = steam_user_manager.shortcuts_file_for_user_id(user_id)
                shortcuts_manager = SteamShortcutManager(shortcuts_path)
                rom_manager = IceROMManager(shortcuts_manager)
                # Add the new ROMs in each folder to our Shortcut Manager
                rom_manager.sync_roms(roms)
                # Generate a new shortcuts.vdf file with all of the new additions
                shortcuts_manager.save()
                if IceGridImageManager.should_download_images():
                    ice_logger.log("Downloading grid images")
                    grid_manager.update_user_images(user_id,roms)
                else:
                    ice_logger.log("Skipping 'Download Image' step")
            ice_logger.log("Finished")
        except ConfigError as error:
            ice_logger.log_error('Stopping')
            ice_logger.log_config_error(error)
            ice_logger.log_exception()
        except StandardError as error:
            ice_logger.log_error("An Error has occurred:")
            ice_logger.log_exception()

    def showSettings(self):
        self.windowSettings.setVisible(True)

    def _exitApp(self):
        self.close()




# initialize gui
qtApp = QApplication(sys.argv)
qtWindow = WindowMain()
