from PySide2 import QtCore, QtGui, QtWidgets
from time import sleep

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        # Qt stuff
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        # menu = QtWidgets.QMenu(parent)
        menu = ContextMenu(parent)

        # To quit the app
        exit = menu.addAction("Exit")
        exit.triggered.connect(self.exit)

        settings = menu.addAction("Settings")
        settings.triggered.connect(self.showDialog)

        # Adding options to the System Tray
        self.setContextMenu(menu)

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

class ContextMenu(QtWidgets.QMenu):
    def __init__(self, parent=None):
        # Qt stuff
        QtWidgets.QMenu.__init__(self, parent)
        self.css_set = "Stylef"

    def mouseMoveEvent(self, event) -> None:
        super().mouseMoveEvent(event)
        print("asdf")
        if self.activeAction() and self.activeAction().text() == 'Exit':
            self.setStyleSheet(tempst)
            self.css_set = "tempst"
            return

        if self.css_set != "Style":
            self.css_set = "Style"
            self.setStyleSheet(Style)



class Window(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.initMenu()
        self.initAnimation()

    def contextMenuEvent(self, event):
        pos = event.globalPos()
        size = self._contextMenu.sizeHint()
        x, y, w, h = pos.x(), pos.y(), size.width(), size.height()
        self._animation.stop()
        self._animation.setStartValue(QtCore.QRect(x, y, 0, 0))
        self._animation.setEndValue(QtCore.QRect(x, y, w, h))
        self.posAnim.setStartValue(QtCore.QRect(x, y, 0, 0))
        self.posAnim.setEndValue(QtCore.QRect(x, y, w, h))
        self._animation.start()
        self.opacityAnim.start()
        # self._contextMenu.setStyleSheet(Style)
        # self._animation.finished.connect(self.animf)
        # self.posAnim.start()
        # sleep(0.2)
        self._contextMenu.exec_(event.globalPos())

    def animf(self):
        self._contextMenu.setStyleSheet(tempst)

    def reset_css(self):
        self._contextMenu.setStyleSheet(Style)

    def change_css(self):
        self._contextMenu.setStyleSheet(tempst)

    def hello(self):
        QtWidgets.QApplication.instance().aboutQt()

    def initAnimation(self):
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self._contextMenu, opacity=1.0)
        self._contextMenu.setGraphicsEffect(self.opacityEffect)
        self.opacityAnim = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity")
        self.opacityAnim.setDuration(2)
        # self.posAnim.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        self.opacityAnim.setStartValue(0)
        self.opacityAnim.setEndValue(1)

        self.posAnim = QtCore.QPropertyAnimation(self._contextMenu, b"geometry")
        self.posAnim.setDuration(300)
        # self.posAnim.setEasingCurve(QtCore.QEasingCurve.InSine)
        # self.posAnim.setStartValue(startPos)
        # self.posAnim.setEndValue(endPos)


        self._animation = QtCore.QPropertyAnimation(
            self._contextMenu, b'geometry',
            easingCurve=QtCore.QEasingCurve.Linear, duration=200)

    def initMenu(self):
        self._contextMenu = QtWidgets.QMenu(self)
        # self._contextMenu = ContextMenu(self)
        self._contextMenu.setWindowFlags(self._contextMenu.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self._contextMenu.setAutoFillBackground(False)
        self._contextMenu.setStyleSheet(Style)
        # self._contextMenu.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self._contextMenu.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            
        # self._contextMenu.setWindowFlags(self._contextMenu.windowFlags())

        self._contextMenu.addAction('Menu item 1', self.hello)
        self._contextMenu.addAction('Menu item 2', self.hello)
        self._contextMenu.addAction('Menu item 3', self.hello)
        self._contextMenu.addAction('Menu item 4', self.hello)
        self._contextMenu.addAction('Menu item 5', self.hello)
        self._contextMenu.addAction('Menu item 6', self.hello).hovered.connect(self.reset_css)
        exit_action = self._contextMenu.addAction('Exit', self.hello)
        exit_action.hovered.connect(self.change_css)
        

Style = """
QMenu {
    /* 
    border: none; */
    background-color: rgb(255, 255, 255);
    border-radius: 20px;
}

QMenu::item {
    border-radius: 4px;
    padding: 8px 48px 8px 36px;
    background-color: transparent;
    margin: 10px;
}
QMenu::item:selected {
    color: white;
    border-radius: 10px;
    background-color: rgb(3, 102, 214);
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

tempst = """
QMenu {
    /* 
    border: none; */
    background-color: rgb(255, 255, 255);
    border-radius: 20px;
}

QMenu::item {
    border-radius: 4px;
    padding: 8px 48px 8px 36px;
    background-color: transparent;
    margin: 10px;
}
QMenu::item:selected {
    font-weight: bold;
    color: white;
    border-radius: 10px;
    background-color: red;
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

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    # app.setStyleSheet(Style)
    w.show()
    image ="C:\\Users\\S\\Downloads\\twitter no alpha channel.png"
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.show()
    app.setQuitOnLastWindowClosed(False)
    sys.exit(app.exec_())