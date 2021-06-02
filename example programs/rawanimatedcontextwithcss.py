import string
from random import choice, randint
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import sys

from PySide2.QtWidgets import QMessageBox
from PySide2 import QtWidgets, QtCore, QtGui


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        # Qt stuff
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        menu.setAttribute(Qt.WA_TranslucentBackground, on=True)
    # 无边框、去掉自带阴影
        menu.setWindowFlags(
                menu.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        # To quit the app
        exit = menu.addAction("Exit Pie Menus")
        exit.triggered.connect(self.exit)
        menu.addSeparator()
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
        QtCore.QCoreApplication.exit()


Style = """
QMenu {
    /* 半透明效果 */
    background-color: rgba(255, 255, 255, 255);
    border: none;
    border-radius: 10px;
}

QMenu::item {
    border-radius: 4px;
    /* 这个距离很麻烦需要根据菜单的长度和图标等因素微调 */
    padding: 8px 48px 8px 36px; /* 36px是文字距离左侧距离*/
    background-color: transparent;
    margin: 10px;
}
/* 鼠标悬停和按下效果 */
QMenu::item:selected {
    border-radius: 10px;
    background-color: rgba(232, 232, 232, 232);
}
/* 禁用效果 */
QMenu::item:disabled {
    background-color: transparent;
}
/* 图标距离左侧距离 */
QMenu::icon {
    left: 15px;
}
/* 分割线效果 */
QMenu::separator {
    height: 2px;
    background-color: rgb(232, 236, 243);
}
"""


def get_icon():
    # 测试模拟图标
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.transparent)
    painter = QPainter()
    painter.begin(pixmap)
    painter.setFont(QFont('Webdings', 11))
    painter.setPen(Qt.GlobalColor(randint(4, 18)))
    painter.drawText(0, 0, 16, 16, Qt.AlignCenter,
                     choice(string.ascii_letters))
    painter.end()
    return QIcon(pixmap)


def about_qt():
    # 关于Qt
    QApplication.instance().aboutQt()


class Window(QLabel):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(400, 400)
        self.setAlignment(Qt.AlignCenter)
        self.setText('右键弹出菜单')
        self.context_menu = QMenu(self)

        # self.shadow = QGraphicsDropShadowEffect(self.context_menu)
        # self.shadow.setColor(QColor("rgb(3, 102, 214"))
        # self.context_menu.setGraphicsEffect(self.shadow)

        self.init_menu()

    def contextMenuEvent(self, event):
        # self.context_menu.exec_(event.globalPos())
        self.initAnimation()
        pos = event.globalPos()
        size = self.context_menu.sizeHint()
        x, y, w, h = pos.x(), pos.y(), size.width(), size.height()
        self._animation.setStartValue(QRect(x, y, 0, 0))
        self.animForward = True
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.setEndValue(QRect(x, y, w, h))
        self._animation.finished.connect(self.animFinished)
        self._animation.start()
        self.context_menu.exec_(QPoint(x, y)) # actual call to context menu
        # self.context_menu.show()

    def animFinished(self):
        self._animation.stop()
        # self.context_menu.hide()
        # if self.animForward:
            # self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
            # self.animForward = False
            # self._animation.start()
        # self._animation.updateCurrentValue(QRect(0, 0, 0, 0))
        self.context_menu.updateGeometry()
        print("animation finished")
        
    
    def initAnimation(self):
        # 按钮动画
        self._animation = QPropertyAnimation(self.context_menu, b'geometry', duration=200)
    def init_menu(self):
        self.context_menu.setAttribute(Qt.WA_TranslucentBackground)
        self.context_menu.setWindowFlags(
            self.context_menu.windowFlags() | Qt.FramelessWindowHint)
        
        # 模拟菜单项
        for i in range(10):
            if i % 2 == 0:
                action = self.context_menu.addAction('Menu %d' % i, about_qt)
                action.setEnabled(i % 4)
            elif i % 3 == 0:
                self.context_menu.addAction(get_icon(), 'Menuuu %d' % i, about_qt)
            if i % 4 == 0:
                self.context_menu.addSeparator()
            if i % 5 == 0:
                # 二级菜单
                # 二级菜单
                menu = QMenu('Menu %d' % i, self.context_menu)
                # 背景透明
                menu.setAttribute(Qt.WA_TranslucentBackground)
                # 无边框、去掉自带阴影
                menu.setWindowFlags(menu.windowFlags() | Qt.FramelessWindowHint)
                for j in range(3):
                    menu.addAction(get_icon(), 'Menu %d' % j)
                self.context_menu.addMenu(menu)


if __name__ == '__main__':
    import sys
    import cgitb

    # cgitb.enable(1, None, 5, '')
    app = QApplication(sys.argv)
    
    app.setStyleSheet(Style)
    image ="C:\\Users\\S\\Downloads\\pexels-pixabay-38537.jpg"
    w1 = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w1)
    # w1.setStyleSheet(Style)
    trayIcon.show()
    w = Window()
    # w.setStyleSheet(Style)
    w.show()
    sys.exit(app.exec_())