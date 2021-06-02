from PySide2 import QtCore, QtGui, QtWidgets
from time import sleep
from ContextMenutest import ContextMenu

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        # settings.triggered.connect(self.showDialog)
        self.activated.connect(self.showMenuOnTrigger)
        menu = makecontext()
        self.setContextMenu(menu)

    def showMenuOnTrigger(self, reason = None):
        if reason == self.Context:
            print(1)
            # opacity, pos = menu.getAnim()
            # opacity.start()
            # pos.start()
            # menu.exec_(QtGui.QCursor.pos())
            # menu.show_menu(showAnim=True, up_right = True)
            self.contextMenu().show_menu(showAnim=True, up_right=True)

    def showDialog(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText("TEST Message Box")
        msgBox.setWindowTitle("testing context menu items")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            print('OK clicked')

    def msgButtonClick(self, event):
        print("Button clicked is:", event.text())

    def exit(self):
        print("asdf")
        QtCore.QCoreApplication.exit()

class Window(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.initMenu()
        # self.initAnimation()

    def contextMenuEvent(self, event):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(1)
        shadow.setColor(QtGui.QColor(255, 0, 0, 160))
        shadow.setOffset(1)
        self._contextMenu.setGraphicsEffect(shadow)
        self._contextMenu.show_menu(event=event)

    def hello(self):
        QtWidgets.QApplication.instance().aboutQt()

    def initMenu(self):
        self._contextMenu = ContextMenu(self)
        self._contextMenu.set_stock_css(Style)
        self._contextMenu.add_action('Menu item 1', self.hello)
        self._contextMenu.add_action('Menu item 2', self.hello)
        self._contextMenu.add_action('Menu item 3', self.hello)
        self._contextMenu.add_action('Menu item 4', self.hello)
        self._contextMenu.add_action('Menu item 5', self.hello)
        self._contextMenu.add_action('Menu item 6', self.hello, custom_css=exit_css)

Style = """
QMenu {
    /* 
    border: none; */
    background-color: rgb(255, 255, 255);
    border-radius: 9px;
    /*padding: 8px 8px 8px 6px;*/
    font-size: 18px;
}

QMenu::item {
    padding: 8px 108px 8px 36px;
    background-color: transparent;
    margin: 10px 0 10px 0;
}
QMenu::item:selected {
    background-color: rgba(75, 116, 255, 130);
}
QMenu::item:disabled {
    background-color: transparent;
}
QMenu::icon {
    left: 15px;
}
QMenu::separator {
    height: 2px;
    background-color: rgb(232, 236, 243);
}
"""

exit_css = """
QMenu::item:selected {
    color:white;
    font-weight: bold;
    background-color: red;
}
"""

def makecontext():
    menu = ContextMenu()
    menu.set_stock_css(Style)
    exit = menu.addAction("Exit")
    settings = menu.addAction("Settings")
    return menu
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    image ="C:\\Users\\S\\Downloads\\twitter no alpha channel.png"
    menu = ContextMenu()
    menu.set_stock_css(Style)
    exit = menu.addAction("Exit")
    settings = menu.addAction("Settings")
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()
    # app.setQuitOnLastWindowClosed(False)
    sys.exit(app.exec_())