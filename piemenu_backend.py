from ctypes import windll
from PySide2.QtCore import QTimer, QVariantAnimation, Qt
from PySide2.QtGui import QColor, QCursor, QPainter
from PySide2.QtWidgets import QWidget
from PySide2 import QtGui, QtWidgets, QtCore
import sys
import win32gui
import keyboard
# import mouse
# from ctypes import *
import pieFunctions
from time import sleep
from settings import pie_themes
from dotmap import DotMap


transparent = QtGui.QColor(255, 255, 255, 0)


def getWidgetCenterPos(widget):
    return QtCore.QPoint((widget.rect().width() - widget.rect().x())/2, (widget.rect().height() - widget.rect().y())/2)


class Window(QtWidgets.QWidget):
    def __init__(self, settings, globalSettings):
        super().__init__()
        self._menu = None

        self.settings = settings
        self.globalSettings = globalSettings

        # following line for window less app
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)

        # following line for transparent background
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showMaximized()

    def showMenu(self, openPieMenu, summonPosition):
        if self._menu:
            self._menu.kill()
            return
        self._menu = RadialMenu(self, summonPosition, openPieMenu, self.settings, self.globalSettings)
        self._menu.show()

    def killMenu(self):
        if self._menu:
            self._menu.kill()
            return

    def mousePressEvent(self, event):
        # this is automatically called when a mouse key press event occurs
        # this acts as right click to cancel pie menu
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if self._menu:
                self._menu.kill()
                return

    def launchByTrigger(self, counter):
        if self._menu is None: return
        self._menu.launchByTrigger(counter)
        self.killMenu()

    def releasedHeldKey(self):
        if self._menu is None: return
        self._menu.launchByGesture()
        self.killMenu()

    def isMenuOpen(self):
        if self._menu:
            return True
        else:
            return False

class RadialMenu(QtWidgets.QWidget):
    def __init__(self, parent, summonPosition, openPieMenu, settings, globalSettings):
        super().__init__(parent=parent)
        self.setMouseTracking(True)
        self.settings = settings
        self.globalSettings = globalSettings
        self.setGeometry(self.parent().rect())
        # self._outRadius = 100
        # self._inRadius = 15
        self._outRadius = openPieMenu["outRadius"]
        self._inRadius = openPieMenu["inRadius"]
        self._btnList = []
        self._selectedBtn = None
        self._mousePressed = False
        self._animFinished = False
        self._debugDraw = False

        self.openPieMenu = openPieMenu
            
        # self._summonPosition = QtCore.QPoint(summonPosition.x(), summonPosition.y())
        self._summonPosition = self.parent().mapFromGlobal(summonPosition)
        self._currentMousePos = QtCore.QPoint(self._summonPosition)

        self.global_mouse_timer = QTimer()
        self.global_mouse_timer.timeout.connect(self.globalMouseMoveEvent)
        self.global_mouse_timer.start(5)

        for i in range(int(openPieMenu["numSlices"])):
            pie_label = f'{openPieMenu["pies"][i]["label"]}'
            if globalSettings["showTKeyHint"] and not (openPieMenu["pies"][i]["triggerKey"] == "None"):
                pie_label += ' '*2 + f'( {openPieMenu["pies"][i]["triggerKey"]} )'
            self.addButton(pie_label, i)

    def addButton(self, name, i):
        btn = Button(name, self.openPieMenu, i, parent=self)
        self._btnList.append(btn)
        btn.clicked.connect(self.btnAction)
        btn.clicked.connect(self.kill)
        # btn.animateClick()
        # btn.gestureClick()
        # print("yoyo")
        return btn

    def btnAction(self):
        # print("button pressed")
        # print(self.sender().text())
        pieFunc = self.sender().pieSlice["function"]
        params = self.sender().pieSlice["params"]

        if pieFunc.lower() == "none":
            return
        if pieFunc == "sendKeys": pieFunctions.sendKeys(params)
        if pieFunc == "sendKeysAHK": pieFunctions.sendKeysTyping(params)
        if pieFunc == "sendHotkey": pieFunctions.sendHotkey(params)


    def kill(self):
        self.animGroup.setDirection(QtCore.QAbstractAnimation.Backward)
        self.animGroup.finished.connect(self.hide)
        self.animGroup.start()
        self.parent()._menu = None


    def show(self):
        super().show()

        self._summonPosition = self.fixSummonPosition(self._summonPosition)
        self._currentMousePos = QtCore.QPoint(self._summonPosition)
        self.setButtonsPositions()
        
        self.animGroup = QtCore.QParallelAnimationGroup()
        for btn in self._btnList:
            anims = btn.animate(self._summonPosition-getWidgetCenterPos(btn), btn.pos(), False, 70)
            # for anim in anims:
            #     self.animGroup.addAnimation(anim)
            self.animGroup.addAnimation(anims[1])

        self.animGroup.finished.connect(self.animFinished)

        self.animGroup.start()

    def animFinished(self):
        self._animFinished=True

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

    def fixSummonPosition(self, pos):
        savepadding = int(self.globalSettings["savePadding"])
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

    def globalMouseMoveEvent(self):
        self._currentMousePos = self.parent().mapFromGlobal(QCursor.pos())
        self.update()


# Keep the following enabled, although no mouse events will happen
# as there is not any window shown, but just in case, if something fails, 
# and window recieves some event, these will trigger up and do the same functinality
# instead to blocking program or crashing, or missing user action. makes it less error prone.
# covering all grounds just to be safe.
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self._selectedBtn:
            self._mousePressed = True
        # self.kill()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self._selectedBtn:
            self._selectedBtn.click()
        self.kill()

    def paintEvent(self, event):
        angle = None
        circleRect = QtCore.QRect(self._summonPosition.x()-self._inRadius, self._summonPosition.y()-self._inRadius, self._inRadius*2, self._inRadius*2) # The rect of the center circle
        arcSize = 36
        self._selectedBtn = None
        mouseInCircle = (self._currentMousePos.x() - self._summonPosition.x())**2 + (self._currentMousePos.y() - self._summonPosition.y())**2 < self._inRadius**2
        bgCirclePen = QtGui.QPen(QtGui.QColor("#f9e506"), 7)
        fgCirclePen = QtGui.QPen(QtGui.QColor("#FF0044"), 7)  
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, on=True)
        # highqualityantialising is obselete value now and is ignored 
        # refer this -> https://doc.qt.io/qtforpython-5/PySide2/QtGui/QPainter.html
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, on= True)
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
            if self.globalSettings["useArcOnHover"]:
                painter.drawArc(circleRect, int(angle-arcSize/2)*16, arcSize*16)
            if self.globalSettings["useLineOnHover"]:
                # tracking line
                fgCirclePen.setCapStyle(Qt.RoundCap)
                painter.setPen(fgCirclePen)
                painter.drawLine(self._summonPosition, self._currentMousePos)

        
        # if targetBtn and self._animFinished is True and not mouseInCircle:
        if targetBtn and not mouseInCircle:
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

    def launchByGesture(self):
        for btn in self._btnList:
            if btn.isHovered():
                btn.animateClick()
                break          
                
    def launchByTrigger(self, counter):
        self._btnList[counter].animateClick()

class Button(QtWidgets.QPushButton):
    def __init__(self, name, openPieMenu, i, parent=None):
        super().__init__(name, parent=parent)
        self.setMouseTracking(True)
        # self.setStyleSheet(pie_themes.dhalu_theme)
        self.setStyleSheet(pie_themes.testing_theme)

        self._hoverEnabled = False
        self._pressEnabled = False
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self, opacity=1.0)
        self.setGraphicsEffect(self.opacityEffect)
        # keep the buttons always enabled even before the animation to speed up things
        # so don't uncomment the following line
        # self.setEnabled(False)
        self.targetPos = self.pos()

        self.pieSlice = openPieMenu["pies"][i]

        # Beta Stuff
        self._animation = QVariantAnimation(startValue=0.0)
        self._animation.valueChanged.connect(self._handle_valueChanged)
        self._animation.finished.connect(self._handle_finished)
        self._animation.setDuration(600)
        self._radius = 0


    def setHover(self, value):
        if self.isHovered() != value:
            self._hoverEnabled = value
            self.setProperty("hover", value)            
            self.style().unpolish(self)
            self.style().polish(self)
            # self._start_animation()

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

    def gestureClick(self):
        super().animateClick()

    def animate(self, startPos, endPos, start=True, duration=200):
        self.parallelAnim = QtCore.QParallelAnimationGroup()

        self.posAnim = QtCore.QPropertyAnimation(self, b"pos")
        self.posAnim.setDuration(duration)
        self.posAnim.setEasingCurve(QtCore.QEasingCurve.InSine)
        self.posAnim.setStartValue(startPos)
        self.posAnim.setEndValue(endPos)

        self.opacityAnim = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity")
        self.opacityAnim.setDuration(duration)
        self.posAnim.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        self.opacityAnim.setStartValue(0)
        self.opacityAnim.setEndValue(1)

        # self.parallelAnim.addAnimation(self.posAnim)
        self.parallelAnim.addAnimation(self.opacityAnim)
        if start:
            self.parallelAnim.start()

        return [self.posAnim, self.opacityAnim]


    # Beta Stuff
    def _start_animation(self):
        self._animation.setDirection(QVariantAnimation.Forward)
        self._animation.setEndValue(self.width() / 1.0)
        self._animation.start()

    def _handle_valueChanged(self, value):
        self._radius = value
        self.update()

        
    def _handle_finished(self):
        # self._animation.setDirection(QVariantAnimation.Backward)
        # self._animation.start()
        self._radius = 0
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._radius:
            qp = QPainter(self)
            qp.setBrush(QColor(249, 229, 6, 45))
            qp.setPen(Qt.NoPen)
            qp.drawEllipse(self.rect().center(), self._radius, self._radius)
            # qp.drawText(self.rect().center(),self.text)
            # qp.drawEllipse(QPoint(self.x, self.y), self._radius, self._radius)