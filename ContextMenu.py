from PySide2 import QtCore, QtGui, QtWidgets
from time import sleep


class ContextMenu(QtWidgets.QMenu):
    def __init__(self, parent=None):
        QtWidgets.QMenu.__init__(self, parent)
        self.stock_css = ""
        self.is_stock_css = True

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.initAnimation()


    def reset_css(self):
        if not self.is_stock_css:
            self.setStyleSheet(self.stock_css)
            self.is_stock_css = True

    def update_css(self, custom_css):
        self.is_stock_css = False
        self.setStyleSheet(self.stock_css + custom_css)

    def set_stock_css(self, css):
        self.setStyleSheet(css)
        self.is_stock_css = True
        self.stock_css = css

    def initAnimation(self):
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self, opacity=1.0)
        self.setGraphicsEffect(self.opacityEffect)
        self.opacityAnim = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity", duration=1)
        self.opacityAnim.setStartValue(0)
        self.opacityAnim.setEndValue(1)

        self.geomAnim = QtCore.QPropertyAnimation(self, b'geometry', easingCurve=QtCore.QEasingCurve.OutCubic, duration=130)
        # self.posAnim.setStartValue(startPos)
        # self.posAnim.setEndValue(endPos)
        # self.posAnim.setEasingCurve(QtCore.QEasingCurve.InSine)

    def readyUp_Anim(self, event = None, up_right = False, up_left = False, bottom_left = False):

        if up_left and (up_right or bottom_left) or (up_right and bottom_left):
            print("please give set only one direction for context menu")
            print("Either up_right or up_left or bottom_left")
            return
        if event:
            pos = event.globalPos()
        else:
            pos = QtGui.QCursor.pos()
        size = self.sizeHint()
        x, y, w, h = pos.x(), pos.y(), size.width(), size.height()
        self.geomAnim.setStartValue(QtCore.QRect(x, y, 0, 0))
        if up_right:
            self.geomAnim.setEndValue(QtCore.QRect(x, y-h, w, h))
        elif up_left:
            self.geomAnim.setEndValue(QtCore.QRect(x-w, y-h, w, h))
        elif bottom_left:
            self.geomAnim.setEndValue(QtCore.QRect(x-w, y, w, h))
        else:
            self.geomAnim.setEndValue(QtCore.QRect(x, y, w, h))

        self.opacityAnim.setDirection(QtCore.QVariantAnimation.Forward)

    def getAnim(self):
        return [self.opacityAnim, self.geomAnim]

    def add_action(self, *args, custom_css = None):
        action = self.addAction(*args)

        if custom_css:
            action.hovered.connect(lambda: self.update_css(custom_css))
        else:
            action.hovered.connect(self.reset_css)

        return action

    def hideEvent(self, arg__1: QtGui.QHideEvent) -> None:
        # do stuff when context menu is hidden here
        self.destroy()
        return super().hideEvent(arg__1)

    def show_menu(self, showAnim = False, event = None, **kwargs):
        self.readyUp_Anim(event= event, **kwargs)
        if not event:
            pos = QtGui.QCursor.pos()
        else:
            pos = event.globalPos()
        if showAnim:
            self.opacityAnim.start()
            self.geomAnim.start()

        self.exec_(pos)        