# from PyQt5 import QtCore, QtWidgets
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# '''
# Created on 2018年1月27日
# @author: Irony."[讽刺]
# @site: https://pyqt5.com , https://github.com/892768447
# @email: 892768447@qq.com
# @file: BubbleTips
# @description: 
# '''
import sys

from PySide2.QtCore import QRectF, Qt, QPropertyAnimation, Property, \
    QPoint, QParallelAnimationGroup, QEasingCurve
from PySide2.QtGui import QPainter, QPainterPath, QColor, QPen
from PySide2.QtWidgets import QLabel, QWidget, QVBoxLayout, QApplication,\
    QLineEdit, QPushButton


__Author__ = "By: Irony.\"[讽刺]\nQQ: 892768447\nEmail: 892768447@qq.com"
__Copyright__ = "Copyright (c) 2018 Irony.\"[讽刺]"
__Version__ = "Version 1.0"


class BubbleLabel(QWidget):

    BackgroundColor = QColor(0, 0, 0)
    BorderColor = QColor(150, 150, 150)

    def __init__(self, *args, **kwargs):
        text = kwargs.pop("text", "")
        super().__init__(*args, **kwargs)
        # 设置无边框置顶
        self.setWindowFlags(Qt.Window | Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMinimumWidth(200)
        self.setMinimumHeight(48)
        layout = QVBoxLayout(self)
        # 左上右下的边距（下方16是因为包括了三角形）
        layout.setContentsMargins(8, 8, 8, 16)
        self.label = QLabel(self)
        layout.addWidget(self.label)
        self.setText(text)
        # 获取屏幕高宽
        self._desktop = QApplication.instance().desktop()

    def setText(self, text):
        self.label.setText(text)

    def text(self):
        return self.label.text()

    def stop(self):
        self.hide()
        self.animationGroup.stop()
        self.close()

    def show(self):
        super().show()

        # start end position for move animation
        startPos = QPoint(
            self._desktop.screenGeometry().width()/2 - self.width()/2,
            self._desktop.availableGeometry().height() - self.height() - 50)
        endPos = QPoint(
            self._desktop.screenGeometry().width()/2 - self.width()/2,
            self._desktop.availableGeometry().height() - self.height() * 3 - 5)
        # print(startPos, endPos)
        self.move(startPos)
        self.initAnimation(startPos, endPos)

    def initAnimation(self, startPos, endPos):
        opacityAnimation = QPropertyAnimation(self, b"opacity")
        opacityAnimation.setStartValue(1.0)
        opacityAnimation.setEndValue(0.0)
        opacityAnimation.setEasingCurve(QEasingCurve.InCubic)
        opacityAnimation.setDuration(1000)

        # move animation code, if required.
        # moveAnimation = QPropertyAnimation(self, b"pos")
        # moveAnimation.setStartValue(startPos)
        # moveAnimation.setEndValue(endPos)
        # # moveAnimation.setEasingCurve(QEasingCurve.InQuad)
        # moveAnimation.setDuration(5000)  
        self.animationGroup = QParallelAnimationGroup(self)
        self.animationGroup.addAnimation(opacityAnimation)
        # self.animationGroup.addAnimation(moveAnimation)
        self.animationGroup.finished.connect(self.close)
        self.animationGroup.start()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rectPath = QPainterPath()
        height = self.height() - 8
        rectPath.addRoundedRect(QRectF(0, 0, self.width(), height), 8, 8)
        # painting the border of toast msg
        # painter.setPen(QPen(self.BorderColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(self.BackgroundColor)
        painter.drawPath(rectPath)

    def windowOpacity(self):
        return super().windowOpacity()

    def setWindowOpacity(self, opacity):
        super().setWindowOpacity(opacity)

    # Because the opacity property is not in QWidget, one needs to be redefined
    # opacity = pyqtProperty(float, windowOpacity, setWindowOpacity)
    opacity = Property(float, windowOpacity, setWindowOpacity)


class TestWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.msgEdit = QLineEdit(self, returnPressed=self.onMsgShow)
        self.msgButton = QPushButton("Show toast", self, clicked=self.onMsgShow)
        self.testbtn = QPushButton("test btn", self)
        self.msgButton.setStyleSheet("""background-color:blue;border-radius:10px;padding-top: 5px;
                        padding-bottom: 5px;
                        padding-left: 15px;
                        padding-right: 15px;""")
        layout.addWidget(self.msgEdit)
        
        layout.addWidget(self.msgButton)
        
    def onMsgShow(self):
        msg = self.msgEdit.text().strip()
        if not msg:
            return
        # if hasattr(self, "_blabel"):
        #     self._blabel.stop()
        #     self._blabel.deleteLater()
        #     del self._blabel
        self._blabel = BubbleLabel()
        self._blabel.setText(msg)
        self._blabel.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TestWidget()
    w.show()
    sys.exit(app.exec_())