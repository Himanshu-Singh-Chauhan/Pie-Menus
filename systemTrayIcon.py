from PySide2.QtWidgets import QMessageBox
from PySide2 import QtWidgets, QtCore

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        # Qt stuff
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)

        # To quit the app
        exit_app = menu.addAction("Exit Pie Menus")
        exit_app.triggered.connect(self.exit)

        settings = menu.addAction("Settings")
        settings.triggered.connect(self.showDialog)

        # Adding options to the System Tray
        self.setContextMenu(menu)

    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("TEST Message Box")
        msgBox.setWindowTitle("testing context menu items")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def msgButtonClick(self, event):
        print("Button clicked is:", event.text())

    def exit(self):
        QtCore.QCoreApplication.exit()