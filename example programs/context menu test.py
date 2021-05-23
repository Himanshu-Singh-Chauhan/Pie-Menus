import sys

from PySide2.QtWidgets import QMessageBox
from PySide2 import QtWidgets, QtCore, QtGui

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        # Qt stuff
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)

        # To quit the app
        exit = menu.addAction("Exit Pie Menus")
        exit.triggered.connect(self.exit)

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
        msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def msgButtonClick(self, event):
        print("Button clicked is:", event.text())

    def exit(self):
        print("asdf")
        QtCore.QCoreApplication.exit()


image ="C:\\Users\\S\\Downloads\\pexels-pixabay-38537.jpg"
app = QtWidgets.QApplication(sys.argv)
w = QtWidgets.QWidget()
trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
trayIcon.show()
app.setQuitOnLastWindowClosed(False)
sys.exit(app.exec_())