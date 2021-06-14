from PySide2.QtWidgets import QMenu, QMessageBox
from PySide2 import QtWidgets, QtCore
from PySide2.QtGui import QCursor
from ContextMenu import ContextMenu
from settings.pie_themes import QMenu as context_theme
from settings.pie_themes import qmenu_danger, qmenu_warning

# from main import suspend_app, resume_app, APP_SUSPENDED # Just to resolve undefined vars in vscode or any editors.
# # comment out when compiling.

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, GAR, parent=None):
        # Qt stuff
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.activated.connect(self.showMenuOnTrigger)

        self.GAR = GAR
        self.suspend_app = GAR(True)['suspend_app']
        self.resume_app  = GAR(True)['resume_app']
            

    def make_context(self):
        # menu = QtWidgets.QMenu(parent)
        self.contextMenu = None

        main_menu = ContextMenu(self.parent())

        # ------------ Main context menu--------------------
            # To quit the app
        exit_app = main_menu.add_action("Exit Pie Menus", custom_css=qmenu_danger)
        exit_app.triggered.connect(self.exit)
        
        main_menu.addSeparator()

        settings = main_menu.add_action("Settings")
        settings.triggered.connect(lambda: self.showDialog("The settings page will be soon available, as of now please edit JSON if you can.", "Sorryyy"))
        # ------------ /Main context menu--------------------


        # ------------ suspend sub context menu--------------------
        suspend_menu = ContextMenu("Suspend", main_menu)
        
        if self.GAR()['APP_SUSPENDED']:
            res_app = suspend_menu.add_action("Resume Pie Menus App")
            res_app.triggered.connect(self.resume_app)
        else:
            sus_app = suspend_menu.add_action("Suspend Pie Menus App", custom_css=qmenu_warning)
            sus_app.triggered.connect(self.suspend_app)
            # sus_app.triggered.connect(lambda: self.showDialog("Still in development", "Sorry"))

        sus_profile = suspend_menu.add_action("Suspend current profile")
        sus_profile.triggered.connect(lambda: self.showDialog("Still in dev", "Sorry"))

        main_menu.addMenu(suspend_menu)
        # ------------ /suspend sub context menu--------------------


        main_menu.set_stock_css(context_theme)
        self.contextMenu = main_menu

        # Don't do the following line, animation problem and one right click does not work, see comments on end of this file
        # self.setContextMenu(menu)


    def showMenuOnTrigger(self, reason = None):
        if reason == self.Context:
            self.make_context() #recreate everytime, animation flicker problem
            self.contextMenu.show_menu(showAnim=True, up_left=True)


    def showDialog(self, msg, title):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(msg)
        msgBox.setWindowTitle(title)
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