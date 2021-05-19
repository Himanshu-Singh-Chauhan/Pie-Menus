from PySide2 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
import os

transparent = QtGui.QColor(255, 255, 255, 0)

def getWidgetCenterPos(widget):
    """Get the center position of the given widget.

    Args:n
        widget (QtWidgets.QWidget): The widget to dertemine the center position

    Returns:
        QtCore.QPoint: The relative center position of the widget
    """
    return QtCore.QPoint((widget.rect().width() - widget.rect().x())/2, (widget.rect().height() - widget.rect().y())/2)
class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self._menu = None
        # self.setAttribute(Qt)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # following line for window less app
        # self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        # following line for transparent background
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.setGeometry(QtCore.QRect(1282, 570, 640, 480))
        self.show()
        
    def paintEvent(self, event):        
        # this function draws a rectangle in the window.
        painter = QtGui.QPainter(self)
        painter.setBrush(QtGui.QColor("#393938"))
        painter.drawRect(self.rect())
        painter.end()
   
    def mousePressEvent(self, event):
        # this is automatically called when a mouse key press event occurs
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if self._menu:
                self._menu.kill()
                return
            self._menu = RadialMenu(self, event.pos())
            self._menu.show()

class RadialMenu(QtWidgets.QWidget):
    def __init__(self, parent, summonPosition):
        print(parent)
        super(RadialMenu, self).__init__(parent=parent)
        self.setMouseTracking(True)

        self.setGeometry(self.parent().rect())
        self._outRadius = 80
        self._inRadius = 15
        self._btnList = []
        self._selectedBtn = None
        self._mousePressed = False
        self._animFinished = False
        self._debugDraw = False
            
        self._summonPosition = summonPosition
        self._currentMousePos = QtCore.QPoint(self._summonPosition)
        # print(self._summonPosition)

        for i in range(4):
            self.addButton("Button {}".format(i))

    def fixSummonPosition(self, pos):
        # return pos
        savepadding = 10
        minSpaceToBorder = savepadding + self._outRadius
        maxX = self.rect().width() - minSpaceToBorder
        maxY = self.rect().height() - minSpaceToBorder

        # Guess the button position
        # print(self._btnList[0].x())
        _minX = _minY = _maxX = _maxY = self._btnList[0]
        for btn in self._btnList:
            if _minX.pos().x() > btn.pos().x():
                _minX = btn
            if _minY.pos().y() > btn.pos().y():
                _minY = btn
            if _maxX.pos().x() + _maxX.width() < btn.pos().x() + btn.width():
                _maxX = btn
            if _maxY.pos().y() + _maxY.height() < btn.pos().y() + btn.height():
                _maxY = btn                
        
        minX = minSpaceToBorder + _minX.width()
        minY = minSpaceToBorder + _minY.height()
        maxX = maxX - _minX.width()
        maxY = maxY - _maxY.height()

        if pos.x() < minX:
            pos.setX(minX)
        if pos.x() > maxX:
            pos.setX(maxX)
        if pos.y() < minY:
            pos.setY(minY)
        if pos.y() > maxY:
            pos.setY(maxY)
        return pos

    def mousePressEvent(self, event):
        super(RadialMenu, self).mousePressEvent(event)
        if self._selectedBtn:
            self._mousePressed = True
        # self.kill()
    
    def mouseReleaseEvent(self, event):
        super(RadialMenu, self).mouseReleaseEvent(event)
        if self._selectedBtn:
            self._selectedBtn.click()
        # TODO: execute the button
        self.kill()

    def mouseMoveEvent(self, event):
        self._currentMousePos = event.pos()
        self.update()
    
    def paintEvent(self, event):
        angle = None
        circleRect = QtCore.QRect(self._summonPosition.x()-self._inRadius, self._summonPosition.y()-self._inRadius, self._inRadius*2, self._inRadius*2) # The rect of the center circle
        arcSize = 36
        self._selectedBtn = None
        mouseInCircle = (self._currentMousePos.x() - self._summonPosition.x())**2 + (self._currentMousePos.y() - self._summonPosition.y())**2 < self._inRadius**2
        bgCirclePen = QtGui.QPen(QtGui.QColor("#232323"), 5)
        fgCirclePen = QtGui.QPen(QtGui.QColor("#5176b2"), 5)  
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        refLine = QtCore.QLineF(self._summonPosition, self._currentMousePos)

        # guess the target button
        targetBtn = self._btnList[0]
        targetLine = QtCore.QLineF(self._summonPosition, targetBtn.pos() + getWidgetCenterPos(targetBtn))
        minAngle = 360
        for btn in self._btnList:
            # reset the hover and the press effect
            btn.setHover(False)
            btn.setPress(False)

            btnLine = QtCore.QLineF(self._summonPosition, btn.pos() + getWidgetCenterPos(btn))
            angle = btnLine.angleTo(refLine)
            if angle > 180:
                angle = refLine.angleTo(btnLine)

            if angle < minAngle:
                targetBtn = btn
                targetLine = btnLine # Used for the debug lines
                minAngle = angle # Used for the comparaison


        if not mouseInCircle:            
            normLine = refLine.unitVector() # Create a line with the same origine and direction but with a length of 1
            finalPointF = normLine.p1() + (normLine.p2() - normLine.p1())*self._inRadius
            finalPoint = QtCore.QPoint(int(finalPointF.x()), int(finalPointF.y()))
            angle = QtCore.QLineF(self._summonPosition, self._summonPosition+QtCore.QPoint(self._inRadius, 0)).angleTo(normLine)


        # Draw Background circle
        painter.setPen(bgCirclePen)
        painter.drawEllipse(circleRect)

        # Draw Forebround circle
        if angle and not mouseInCircle:
            painter.setPen(fgCirclePen)
            painter.drawArc(circleRect, int(angle-arcSize/2)*16, arcSize*16)

        
        if targetBtn and self._animFinished is True and not mouseInCircle:
            self._selectedBtn = targetBtn
            self._selectedBtn.setHover(True)
            if self._mousePressed is True:
                self._selectedBtn.setPress(True)
        
        # debug draw
        if self._debugDraw is True:
            painter.setBrush(transparent)
            painter.setPen(QtCore.Qt.blue)
            painter.drawEllipse(self._summonPosition, self._outRadius, self._outRadius)     
            painter.drawLine(self._summonPosition, self._currentMousePos)
            for btn in self._btnList:            
                painter.drawLine(self._summonPosition, btn.pos()+getWidgetCenterPos(btn))
            painter.setPen(QtGui.QPen(QtCore.Qt.yellow, 5))
            painter.drawLine(targetLine)

    def addButton(self, name):
        btn = Button(name, parent=self)
        self._btnList.append(btn)
        self.setButtonsPositions()
        btn.clicked.connect(self.btnAction)
        btn.clicked.connect(self.kill)
        return btn

    def btnAction(self):
        print(self.sender().text())

    def setButtonsPositions(self):
        counter = 0
        for btn in self._btnList:
            line = QtCore.QLineF(self._summonPosition, self._summonPosition+QtCore.QPoint(self._outRadius, 0))
            line.setAngle(counter*(360/len(self._btnList)))
            pos = getWidgetCenterPos(btn)
            if abs(int(line.p2().x())- self._summonPosition.x()) < 3:
                pass
            elif int(line.p2().x()) < self._summonPosition.x():
                pos.setX(btn.rect().width())
            else:
                pos.setX(btn.rect().x())

            if abs(int(line.p2().y())- self._summonPosition.y()) < 3:
                pass
            elif int(line.p2().y()) < self._summonPosition.y():
                pos.setY(btn.rect().height())
            else:
                pos.setY(btn.rect().y())

            btn.move(line.p2().toPoint()-pos)
            btn.targetPos = line.p2().toPoint()
            counter += 1

    def kill(self):
        self.animGroup.setDirection(QtCore.QAbstractAnimation.Backward)
        self.animGroup.finished.connect(self.hide)
        self.animGroup.start()
        self.parent()._menu = None

    def show(self):
        super(RadialMenu, self).show()

        self._summonPosition = self.fixSummonPosition(self._summonPosition)
        self._currentMousePos = QtCore.QPoint(self._summonPosition)
        self.setButtonsPositions()
        
        self.animGroup = QtCore.QParallelAnimationGroup()
        for btn in self._btnList:
            anims = btn.animate(self._summonPosition-getWidgetCenterPos(btn), btn.pos(), False, 100)
            for anim in anims:
                self.animGroup.addAnimation(anim)

        self.animGroup.finished.connect(self.animFinished)

        self.animGroup.start()

    def animFinished(self):
        self._animFinished=True
        for btn in self._btnList:
            btn.setEnabled(True)

class Button(QtWidgets.QPushButton):
    def __init__(self, name, parent=None):
        super().__init__(name, parent=parent)
        self.setMouseTracking(True)
        self.setStyleSheet("""
        QPushButton
        {
            color: white;
            background-color: #232323;
            border-color: #232323;
            outline: none;
            border-style: solid;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 15px;
            padding-right: 15px;
            border-style: solid;
            border-width:1px;
            border-radius:4px;
            min-width: 10px;
            min-height: 10px;
        }
        QPushButton[hover=true]
        {
            background-color: #585858;
            border-color: #585858;
        }
        QPushButton:pressed, QPushButton[pressed=true]
        {
            background-color: #5479b5;
            border-color: #5479b5;
        }
        
        """)

        self._hoverEnabled = False
        self._pressEnabled = False
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self, opacity=1.0)
        self.setGraphicsEffect(self.opacityEffect)
        self.setEnabled(False)
        self.targetPos = self.pos()
        print(self.targetPos)
        # self.setAttribute(QtCore.Qt.WA_Hover, False)

    def mouseMoveEvent(self, event):
        """Override the mouseMoveEvent method to avoid the event catch by the current widget
        Send the same event to the parent widget to keep mouse tracking on the RadialMenu widget

        Args:
            event (PySide2.QtGui.QMouseEvent): QMouseEvent sent by QT Framework
        """
        super(Button, self).mouseMoveEvent(event)
        self.parent().mouseMoveEvent(event)

    def setHover(self, value):
        if self.isHovered() != value:
            self._hoverEnabled = value
            self.setProperty("hover", value)            
            self.style().unpolish(self)
            self.style().polish(self)

    def isHovered(self):
        return self._hoverEnabled

    def setPress(self, value):
        if self.isPressed() != value:
            self._pressEnabled = value
            self.setProperty("pressed", value)            
            self.style().unpolish(self)
            self.style().polish(self)

    def isPressed(self):
        return self._pressEnabled

    def animate(self, startPos, endPos, start=True, duration=100):
        self.parallelAnim = QtCore.QParallelAnimationGroup()

        self.posAnim = QtCore.QPropertyAnimation(self, b"pos")
        self.posAnim.setDuration(duration)
        self.posAnim.setStartValue(startPos)
        self.posAnim.setEndValue(endPos)

        self.opacityAnim = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity")
        self.opacityAnim.setDuration(duration)
        self.opacityAnim.setStartValue(0)
        self.opacityAnim.setEndValue(1)

        self.parallelAnim.addAnimation(self.posAnim)
        self.parallelAnim.addAnimation(self.opacityAnim)
        if start:
            self.parallelAnim.start()

        return [self.posAnim, self.opacityAnim]
def main():
    app = QtWidgets.QApplication()
    window = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()