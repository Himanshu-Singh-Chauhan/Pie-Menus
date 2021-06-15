#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on March 30, 2017
@author: Irony." (Sarcasm)
@site: https://pyqt5.com , https://github.com/892768447
@email: 892768447@qq.com
@file: WindowNotify
@description: The lower right corner pops the window
'''
# import web browser

from PyQt5. QtCore import Qt, QPropertyAnimation, QPoint, QTimer, pyqtSignal
from PyQt5. QtWidgets import QWidget, QPushButton

from Lib.UiNotify import Ui_NotifyForm # @UnresolvedImport


__version__ = "0.0.1"


class WindowNotify(QWidget, Ui_NotifyForm):

    # SignalClosed s pyqtSignal() smh.com.au

    def __init__(self, title="", content="", timeout=5000, *args, **kwargs):
        super(WindowNotify, self). __init__(*args, **kwargs)
        self. setupUi(self)
        self. setTitle(title). setContent(content)
        self. _timeout = timeout
        self. _init()

    def setTitle(self, title):
        if title:
            self. labelTitle. setText(title)
        return self

    def title(self):
        return self. labelTitle. text()

    def setContent(self, content):
        if content:
            self. labelContent. setText(content)
        return self

    def content(self):
        return self. labelContent. text()

    def setTimeout(self, timeout):
        if isinstance(timeout, int):
            self. _timeout = timeout
        return self

    def timeout(self):
        return self. _timeout

    def onView(self):
        print("onView")
        # webbrowser. open_new_tab("http://alyl.vip")

    def onClose(self):
        #点击关闭按钮时
        print("onClose")
        self. isShow = False
        QTimer. singleShot(100, self.  closeAnimation)#启动弹回动画

    def _init(self):
        # Hide the top layer of the taskbar | remove the border |
        self. setWindowFlags(Qt. Tool | Qt. X11BypassWindowManagerHint |
                            Qt. FramelessWindowHint | Qt. WindowStaysOnTopHint)
        # Turn off the button event
        self. buttonClose. clicked. connect(self. onClose)
        # Click the view button
        self. buttonView. clicked. connect(self. onView)
        # Whether the flag is displayed
        self. isShow = True
        # Time-out
        self. _timeouted = False
        # Desktops
        self. _desktop = QApplication. instance(). desktop()
        # The initial start position of the window
        self. _startPos = QPoint(
            self. _desktop. screenGeometry(). width() - self. width() - 5,
            self. _desktop. screenGeometry(). height()
        )
        # The end position of the window pop-up
        self. _endPos = QPoint(
            self. _desktop. screenGeometry(). width() - self. width() - 5,
            self. _desktop. availableGeometry(). height() - self. height() - 5
        )
        # The initialization position is in the lower right corner
        self. move(self. _startPos)

        # The animation
        self. animation = QPropertyAnimation(self, b"pos")
        self. animation. finished. connect(self. onAnimationEnd)
        self. animation. setDuration(1000) # 1s

        # Bounce back the timer
        self. _timer = QTimer(self, timeout=self. closeAnimation)

    def show(self, title="", content="", timeout=5000):
        # self. _timer. Stop() stop the timer to prevent problems with the timer before the second pop-up pops up
        self. hide() 
        self. move(self.  _startPos) #. . . initializes the position to the lower right corner
        super(WindowNotify, self). show()
        self. setTitle(title). setContent(content). setTimeout(timeout)
        return self

    def showAnimation(self):
        print("showAnimation isShow = True")
        # The animation is displayed
        self. isShow = True
        self. animation. stop()#先停止之前的动画 and start over
        self. animation. setStartValue(self. pos())
        self. animation. setEndValue(self. _endPos)
        self. animation. start()
        # After 5 seconds of ejection, bounce back if there is no focus
        self. _timer. start(self. _timeout)
#         QTimer.singleShot(self._timeout, self.closeAnimation)

    def closeAnimation(self):
        print("closeAnimation hasFocus", self. hasFocus())
        # Turn off animation
        if self. hasFocus():
            # If there is a focus after 5 seconds of the pop-up countdown, the focus needs to be actively triggered to close after losing focus
            self. _timeouted = True
            # Return . . . does not close if there is focus
        self. isShow = False
        self. animation. stop()
        self. animation. setStartValue(self. pos())
        self. animation. setEndValue(self. _startPos)
        self. animation. start()

    def onAnimationEnd(self):
        # The animation ends
        print("onAnimationEnd isShow", self. isShow)
        if not self. isShow:
            print("onAnimationEnd close()")
            self. close()
            print("onAnimationEnd stop timer")
            self. _timer. stop()
            print("onAnimationEnd close and emit signal")
            self. SignalClosed. emit()

    def enterEvent(self, event):
        super(WindowNotify, self). enterEvent(event)
        # Setting the focus (it doesn't seem to work, but with a mouse click, it works)
        print("enterEvent setFocus Qt.MouseFocusReason")
        self. setFocus(Qt. MouseFocusReason)

    def leaveEvent(self, event):
        super(WindowNotify, self). leaveEvent(event)
        # - Unfocused
        print("leaveEvent clearFocus")
        self. clearFocus()
        if self. _timeouted:
            QTimer. singleShot(1000, self. closeAnimation)

if __name__ == "__main__":
    import sys
    from PyQt5. QtWidgets import QApplication, QHBoxLayout
    app = QApplication(sys. argv)

    window = QWidget()
    notify = WindowNotify(parent=window)

    layout = QHBoxLayout(window)

    b1 = QPushButton(
        "弹窗1", window, clicked=lambda: notify. show(content=b1. text()). showAnimation())
    b2 = QPushButton(
        "弹窗2", window, clicked=lambda: notify. show(content=b2. text()). showAnimation())

    layout. addWidget(b1)
    layout. addWidget(b2)

    window. show()

    sys. exit(app. exec_())