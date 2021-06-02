from PySide2.QtWidgets import QMessageBox
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QCursor
from ContextMenu import ContextMenu
from settings.pie_themes import QMenu as context_theme
from settings.pie_themes import qmenu_danger

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        # Qt stuff
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.activated.connect(self.showMenuOnTrigger)
            

    def make_context(self):
        # menu = QtWidgets.QMenu(parent)
        self.contextMenu = None
        menu = ContextMenu(self.parent())
        menu.set_stock_css(context_theme)

        # To quit the app
        exit_app = menu.add_action("Exit Pie Menus", custom_css=qmenu_danger)
        exit_app.triggered.connect(self.exit)
        
        menu.addSeparator()

        settings = menu.add_action("Settings")
        settings.triggered.connect(self.showDialog)

        self.contextMenu = menu

        # Don't do the following line, animation problem and one right click does not work, see comments on end of this file
        # self.setContextMenu(menu)


    def showMenuOnTrigger(self, reason = None):
        if reason == self.Context:
            self.make_context() #recreate everytime, animation flicker problem
            self.contextMenu.show_menu(showAnim=True, up_right=True)


    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("The settings page will be soon available, as of now please edit JSON if you can.")
        msgBox.setWindowTitle("Sorryyy")
        # msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def msgButtonClick(self, event):
        print("Button clicked is:", event.text())

    def exit(self):
        QtCore.QCoreApplication.exit()




# NOTE: do not set self.setcontextmenu(), animation just flicker
# also trigerred.connect, reason -> trigerred: exec_ has to be called twice
# don't know, clicking right clik once just dont work, I have to double right click.
# Also Context menu has to recreated from scratch, because animation flickers.