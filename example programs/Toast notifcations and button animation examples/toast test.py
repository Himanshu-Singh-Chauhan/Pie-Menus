import sys, os

from PyQt5.QtCore import Qt
# from PySide2.QtWidgets import QApplication, QBoxLayout, QDesktopWidget, QGridLayout, QHBoxLayout, QLabel, QPushButton, QWidget
# from datetime import datetime

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtGui import QIcon
# from PyQt5 import QtCore, QtWidgets

class QToaster(QtWidgets.QFrame):
    # closed = QtCore.pyqtSignal() 
    closed = QtCore.Signal() 

    def __init__(self, *args, **kwargs):
        super(QToaster, self).__init__(*args, **kwargs)
        QtWidgets.QHBoxLayout(self)

        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, 
                           QtWidgets.QSizePolicy.Maximum)

        self.setStyleSheet('''
            QToaster {
                border: 1px solid black;
                border-radius: 10px; 
                background: palette(window);
            }
        ''')
        # alternatively:
        # self.setAutoFillBackground(True)
        # self.setFrameShape(self.Box)

        self.timer = QtCore.QTimer(singleShot=True, timeout=self.hide)

        if self.parent():
            self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(opacity=0)
            self.setGraphicsEffect(self.opacityEffect)
            self.opacityAni = QtCore.QPropertyAnimation(self.opacityEffect, b'opacity')
            # we have a parent, install an eventFilter so that when it's resized
            # the notification will be correctly moved to the right corner
            self.parent().installEventFilter(self)
        else:
            # there's no parent, use the window opacity property, assuming that
            # the window manager supports it; if it doesn't, this won'd do
            # anything (besides making the hiding a bit longer by half a second)
            self.opacityAni = QtCore.QPropertyAnimation(self, b'windowOpacity')
        self.opacityAni.setStartValue(0.)
        self.opacityAni.setEndValue(1.)
        self.opacityAni.setDuration(100)
        self.opacityAni.finished.connect(self.checkClosed)

        self.corner = QtCore.Qt.TopLeftCorner
        self.margin = 10

    def checkClosed(self):
        # if we have been fading out, we're closing the notification
        if self.opacityAni.direction() == self.opacityAni.Backward:
            self.close()

    def restore(self):
        # this is a "helper function", that can be called from mouseEnterEvent
        # and when the parent widget is resized. We will not close the
        # notification if the mouse is in or the parent is resized
        self.timer.stop()
        # also, stop the animation if it's fading out...
        self.opacityAni.stop()
        # ...and restore the opacity
        if self.parent():
            self.opacityEffect.setOpacity(1)
        else:
            self.setWindowOpacity(1)

    def hide(self):
        # start hiding
        self.opacityAni.setDirection(self.opacityAni.Backward)
        self.opacityAni.setDuration(500)
        self.opacityAni.start()

    def eventFilter(self, source, event):
        if source == self.parent() and event.type() == QtCore.QEvent.Resize:
            self.opacityAni.stop()
            parentRect = self.parent().rect()
            geo = self.geometry()
            if self.corner == QtCore.Qt.TopLeftCorner:
                geo.moveTopLeft(
                    parentRect.topLeft() + QtCore.QPoint(self.margin, self.margin))
            elif self.corner == QtCore.Qt.TopRightCorner:
                geo.moveTopRight(
                    parentRect.topRight() + QtCore.QPoint(-self.margin, self.margin))
            elif self.corner == QtCore.Qt.BottomRightCorner:
                geo.moveBottomRight(
                    parentRect.bottomRight() + QtCore.QPoint(-self.margin, -self.margin))
            else:
                geo.moveBottomLeft(
                    parentRect.bottomLeft() + QtCore.QPoint(self.margin, -self.margin))
            self.setGeometry(geo)
            self.restore()
            self.timer.start()
        return super(QToaster, self).eventFilter(source, event)

    def enterEvent(self, event):
        self.restore()

    def leaveEvent(self, event):
        self.timer.start()

    def closeEvent(self, event):
        # we don't need the notification anymore, delete it!
        self.deleteLater()

    def resizeEvent(self, event):
        super(QToaster, self).resizeEvent(event)
        # if you don't set a stylesheet, you don't need any of the following!
        if not self.parent():
            # there's no parent, so we need to update the mask
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(self.rect()).translated(-.5, -.5), 4, 4)
            # self.setMask(QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon()))
        else:
            self.clearMask()

    @staticmethod
    def showMessage(parent, message, 
                    icon=QtWidgets.QStyle.SP_MessageBoxInformation, 
                    corner=QtCore.Qt.TopLeftCorner, margin=10, closable=True, 
                    timeout=5000, desktop=False, parentWindow=True):

        if parent and parentWindow:
            parent = parent.window()

        if not parent or desktop:
            self = QToaster(None)
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint |
                QtCore.Qt.BypassWindowManagerHint)
            # This is a dirty hack!
            # parentless objects are garbage collected, so the widget will be
            # deleted as soon as the function that calls it returns, but if an
            # object is referenced to *any* other object it will not, at least
            # for PyQt (I didn't test it to a deeper level)
            self.__self = self

            currentScreen = QtWidgets.QApplication.primaryScreen()
            if parent and parent.window().geometry().size().isValid():
                # the notification is to be shown on the desktop, but there is a
                # parent that is (theoretically) visible and mapped, we'll try to
                # use its geometry as a reference to guess which desktop shows
                # most of its area; if the parent is not a top level window, use
                # that as a reference
                reference = parent.window().geometry()
            else:
                # the parent has not been mapped yet, let's use the cursor as a
                # reference for the screen
                reference = QtCore.QRect(
                    QtGui.QCursor.pos() - QtCore.QPoint(1, 1), 
                    QtCore.QSize(3, 3))
            maxArea = 0
            for screen in QtWidgets.QApplication.screens():
                intersected = screen.geometry().intersected(reference)
                area = intersected.width() * intersected.height()
                if area > maxArea:
                    maxArea = area
                    currentScreen = screen
            parentRect = currentScreen.availableGeometry()
        else:
            self = QToaster(parent)
            parentRect = parent.rect()

        self.timer.setInterval(timeout)

        # use Qt standard icon pixmaps; see:
        # https://doc.qt.io/qt-5/qstyle.html#StandardPixmap-enum
        if isinstance(icon, QtWidgets.QStyle.StandardPixmap):
            labelIcon = QtWidgets.QLabel()
            self.layout().addWidget(labelIcon)
            icon = self.style().standardIcon(icon)
            size = self.style().pixelMetric(QtWidgets.QStyle.PM_SmallIconSize)
            labelIcon.setPixmap(icon.pixmap(size))

        self.label = QtWidgets.QLabel(message)
        self.layout().addWidget(self.label)

        if closable:
            self.closeButton = QtWidgets.QToolButton()
            self.layout().addWidget(self.closeButton)
            closeIcon = self.style().standardIcon(
                QtWidgets.QStyle.SP_TitleBarCloseButton)
            self.closeButton.setIcon(closeIcon)
            self.closeButton.setAutoRaise(True)
            self.closeButton.clicked.connect(self.close)

        self.timer.start()

        # raise the widget and adjust its size to the minimum
        self.raise_()
        self.adjustSize()

        self.corner = corner
        self.margin = margin

        geo = self.geometry()
        # now the widget should have the correct size hints, let's move it to the
        # right place
        if corner == QtCore.Qt.TopLeftCorner:
            geo.moveTopLeft(
                parentRect.topLeft() + QtCore.QPoint(margin, margin))
        elif corner == QtCore.Qt.TopRightCorner:
            geo.moveTopRight(
                parentRect.topRight() + QtCore.QPoint(-margin, margin))
        elif corner == QtCore.Qt.BottomRightCorner:
            geo.moveBottomRight(
                parentRect.bottomRight() + QtCore.QPoint(-margin, -margin))
        else:
            geo.moveBottomLeft(
                parentRect.bottomLeft() + QtCore.QPoint(margin, -margin))

        self.setGeometry(geo)
        # self.setStyleSheet("background-color:red;")
        self.show()
        self.opacityAni.start()


class W(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        layout = QtWidgets.QVBoxLayout(self)

        toasterLayout = QtWidgets.QHBoxLayout()
        layout.addLayout(toasterLayout)

        self.textEdit = QtWidgets.QLineEdit('Ciao!')
        toasterLayout.addWidget(self.textEdit)

        self.cornerCombo = QtWidgets.QComboBox()
        toasterLayout.addWidget(self.cornerCombo)
        for pos in ('TopLeft', 'TopRight', 'BottomRight', 'BottomLeft'):
            corner = getattr(QtCore.Qt, '{}Corner'.format(pos))
            self.cornerCombo.addItem(pos, corner)

        self.windowBtn = QtWidgets.QPushButton('Show window toaster')
        toasterLayout.addWidget(self.windowBtn)
        self.windowBtn.clicked.connect(self.showToaster)

        self.screenBtn = QtWidgets.QPushButton('Show desktop toaster')
        toasterLayout.addWidget(self.screenBtn)
        self.screenBtn.clicked.connect(self.showToaster)

        # a random widget for the window
        layout.addWidget(QtWidgets.QTableView())

    def showToaster(self):
        if self.sender() == self.windowBtn:
            parent = self
            desktop = False
        else:
            parent = None
            desktop = True
        corner = QtCore.Qt.Corner(self.cornerCombo.currentData())
        # QToaster.setStyleSheet("background-color:red;")
        QToaster.showMessage(
            parent, self.textEdit.text(), corner=corner, desktop=desktop)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = W()
    w.show()
    sys.exit(app.exec_())