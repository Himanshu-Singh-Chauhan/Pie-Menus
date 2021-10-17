from ctypes import windll
from PySide2.QtCore import QSize, QTimer, QVariantAnimation, Qt
from PySide2.QtGui import QColor, QCursor, QIcon, QPainter
from PySide2.QtWidgets import QWidget
from PySide2 import QtGui, QtWidgets, QtCore
import os
import iconify
import sys
import win32gui
import keyboard
# import mouse
# from ctypes import *
import pieFunctions
from time import sleep
# from random import choice, randint
from dotmap import DotMap
from settings.pie_themes import pie_themes, tray_theme, pie_selection_theme

from math import sin, cos, ceil
from pympler import muppy, summary

script_dir = os.path.dirname(__file__)
icons_dir = os.path.join(script_dir, "resources/icons/")
transparent = QtGui.QColor(255, 255, 255, 0)


# import string
# def get_random_qticon():
#     pixmap =QtGui.QPixmap(16, 16)
#     pixmap.fill(Qt.transparent)
#     painter = QPainter()
#     painter.begin(pixmap)
#     painter.setFont(QtGui.QFont('Webdings', 11))
#     painter.setPen(Qt.GlobalColor(randint(4, 18)))
#     painter.drawText(0, 0, 16, 16, Qt.AlignCenter,
#                      choice(string.ascii_letters))
#     painter.end()
#     return QIcon(pixmap)

def getWidgetCenterPos(widget):
    # if widget.rect().x() > 0:
    #     print(f"{widget.rect().x() = }")
    # if widget.rect().y() > 0:
    #     print(f"{widget.rect().y() = }")
    # x() and y() are always, always zero. 🤷‍♂️🤷‍♂️ check with above if's.
    # so I am now commenting following line and will be removed after some time.
    # return QtCore.QPoint((widget.rect().width() - widget.rect().x())/2, (widget.rect().height() - widget.rect().y())/2)
    return QtCore.QPoint(widget.rect().width()/2, widget.rect().height()/2)


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


        all_objects = muppy.get_objects()
        # print(all_objects)
        print(len(all_objects))
        # Prints out a summary of the large objects
        # sum1 = summary.summarize(all_objects)
        # summary.print_(sum1)


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

    def ll_wheel_event(self, event):
        if self._menu is None: return
        self._menu.ll_wheel_event(event)

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
        self._inRadius, self._outRadius = list(map(float, openPieMenu["in_out_radius"].split("_")))
        self._btnList = []
        self._selectedBtn = None
        self._mousePressed = False
        self._animFinished = False
        self._debugDraw = False

        self.openPieMenu = openPieMenu
            
        self._summonPosition = self.parent().mapFromGlobal(summonPosition)
        self._currentMousePos = QtCore.QPoint(self._summonPosition)

        self.global_mouse_timer = QTimer()
        self.global_mouse_timer.timeout.connect(self.globalMouseMoveEvent)
        self.global_mouse_timer.start(5)


        pies = openPieMenu["pies"]
        pies = pies[ : int(openPieMenu["numSlices"])]
        if openPieMenu.get("offset_pies"):
            pies = pies[-1*openPieMenu.get("offset_pies"): ] + pies[ : -1*openPieMenu.get("offset_pies")]

        for pie in pies:
            self.addButton(pie)

    def addButton(self, pie):
        btn = Button(self.openPieMenu, pie, self.globalSettings, parent=self)
        self._btnList.append(btn)
        return btn

    def kill(self):
        self.animGroup.setDirection(QtCore.QAbstractAnimation.Backward)
        self.animGroup.finished.connect(self.hide)
        self.animGroup.start()
        self.parent()._menu = None
        for btn in self._btnList:
            btn.deleteLater()

        self.deleteLater()
        del self


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
        offset_angle = -1 * self.openPieMenu["offset_angle"]
        angle = 360/len(self._btnList)
        line = QtCore.QLineF(self._summonPosition, self._summonPosition - QtCore.QPoint(0, self._outRadius))
        for btn in self._btnList:
            if counter == 0:
                line.setAngle(line.angle() + offset_angle)
            else:
                line.setAngle(line.angle() + angle + offset_angle)
                
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
                if round(line.angle() % 90) == 0:
                    pos.setY(btn.rect().height())
            else:
                if round(line.angle() % 90) == 0:
                    pos.setY(btn.rect().y())

            btn.move(line.p2().toPoint()-pos)
            btn.targetPos = line.p2().toPoint()
            counter += 1

    def fixSummonPosition(self, pos):
        savepadding = int(self.globalSettings["savePadding"])
        minSpaceToBorder = savepadding + self._outRadius
        maxX = self.rect().width() - minSpaceToBorder
        maxY = self.rect().height() - minSpaceToBorder

        angle = 360/len(self._btnList)
        line = QtCore.QLineF(self._summonPosition, self._summonPosition - QtCore.QPoint(0, self._outRadius))
        counter = 0
        offset_angle = -1 * self.openPieMenu["offset_angle"]

        _minX = _minY = _maxX = _maxY = self._btnList[0]

        # self.setButtonsPositions() # uncomment this if you can't live with few pixels off in right side padding
        # Guess the button position
        for btn in self._btnList:
            if counter == 0:
                line.setAngle(line.angle() + offset_angle)
            else:
                line.setAngle(line.angle() + angle + offset_angle)

            if line.angle() < 89 or line.angle() > 271:
                if _maxX.pos().x() + _maxX.width() < btn.pos().x() + btn.width():
                    _maxX = btn
            elif line.angle() > 91 and line.angle() < 269:
                if _minX.width() < btn.width():
                    _minX = btn

            counter += 1

            if _minY.pos().y() > btn.pos().y():
                _minY = btn
            if _maxY.pos().y() + _maxY.height() < btn.pos().y() + btn.height():
                _maxY = btn
        
        minX = minSpaceToBorder + _minX.width()
        minY = minSpaceToBorder + _minY.height()
        maxX = maxX - _maxX.width()
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
        last_pos = self._currentMousePos
        self._currentMousePos = self.parent().mapFromGlobal(QCursor.pos())
        if last_pos == self._currentMousePos:
            return
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
        try:
            selectiontheme = self.openPieMenu.get("theme")
            bgCirclePen = QtGui.QPen(QtGui.QColor(pie_selection_theme[selectiontheme]["bg_circle"]), pie_selection_theme[selectiontheme]["thickness"])
            fgCirclePen = QtGui.QPen(QtGui.QColor(pie_selection_theme[selectiontheme]["fg_circle"]), pie_selection_theme[selectiontheme]["thickness"])
        except:
            bgCirclePen = QtGui.QPen(QtGui.QColor(pie_selection_theme.default["bg_circle"]), pie_selection_theme.default["thickness"])
            fgCirclePen = QtGui.QPen(QtGui.QColor(pie_selection_theme.default["fg_circle"]), pie_selection_theme.default["thickness"])
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

    def ll_wheel_event(self, event):
        for btn in self._btnList:
            if btn.isHovered():
                if (btn.pie.get("w_up") or btn.pie.get("w_down")):
                    if not btn.is_actually_hovered():
                        btn.optional_wheelEvent(custom_event = event)
                    elif btn.is_actually_hovered() and btn.pie.get("onPie_w_up") == None and btn.pie.get("onPie_w_down") == None:
                        btn.optional_wheelEvent(custom_event = event)
                break
                
    def launchByTrigger(self, counter):
        self._btnList[counter].animateClick()

class Button(QtWidgets.QPushButton):
    def __init__(self, openPieMenu, pie, globalSettings, parent=None):
        pie_label = f'{pie["label"]}'
        if globalSettings["showTKeyHint"] and not (pie["triggerKey"] == "None"):
            pie_label += ' '*2 + f'( {pie["triggerKey"]} )'

        super().__init__(pie_label, parent=parent)

        self.pie = self.pieSlice = pie

        self.setMouseTracking(True)
        self._hoverEnabled = False
        self._pressEnabled = False
        self._actual_hover = False # this determines wheather mouse is actually on button or not.
        self.targetPos = self.pos()
        self.icon = None
        self.svg_changes_color = False

        if pie.get("icon"):
            icon = os.path.join(icons_dir, pie.get("icon").strip())
            if not os.path.exists(icon):
                icon = os.path.join(icons_dir, "default.svg")

            self.setText(globalSettings.get("icon-padding-right") + self.text())
            if pie.get("icon").strip()[-4:] == ".svg":
                try:
                    svg_nohover_hover = pie_selection_theme.get(openPieMenu.get("theme")).get("svg_nohover_hover")
                    nohover_col, hover_col = svg_nohover_hover.strip().split("_")
                    self.nohover_icon = iconify.Icon(icon, color = QtGui.QColor(nohover_col))
                    self.hover_icon = iconify.Icon(icon, color = QtGui.QColor(hover_col))
                    self.svg_changes_color = True
                    icon = self.nohover_icon
                except:
                    icon = iconify.Icon(icon)

            self.icon = icon
            self.setIcon(QIcon(icon))

        if not openPieMenu["theme"]:
            self.setStyleSheet(pie_themes.dhalu_theme)
        else:
            self.setStyleSheet(pie_themes[openPieMenu["theme"]])

        if self.pie.get("onPie_w_up") or self.pie.get("onPie_w_down"):
            self.wheelEvent = self.optional_wheelEvent

        
        self.clicked.connect(self.btnAction)
        self.clicked.connect(self.parent().kill)

        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self, opacity=1.0)
        self.setGraphicsEffect(self.opacityEffect)
        # keep the buttons always enabled even before the animation to speed up things
        # so don't uncomment the following line
        # self.setEnabled(False)


    def setHover(self, value):
        if self.isHovered() != value:
            self._hoverEnabled = value
            self.setProperty("hover", value)            
            self.style().unpolish(self)
            self.style().polish(self)

        if self.svg_changes_color:
            if value:
                self.setIcon(self.nohover_icon)
            else:
                self.setIcon(self.hover_icon)
            

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
        self.posAnim.setStartValue(startPos)
        self.posAnim.setEndValue(endPos)
        self.posAnim.setDuration(duration)
        self.posAnim.setEasingCurve(QtCore.QEasingCurve.InSine)
        self.posAnim.setEasingCurve(QtCore.QEasingCurve.OutQuad)

        self.opacityAnim = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity")
        self.opacityAnim.setStartValue(0)
        self.opacityAnim.setEndValue(1)
        self.opacityAnim.setDuration(duration)

        self.parallelAnim.addAnimation(self.posAnim)
        self.parallelAnim.addAnimation(self.opacityAnim)
        if start:
            self.parallelAnim.start()

        return [self.posAnim, self.opacityAnim]


    def enterEvent(self, event) -> None:
        self._actual_hover = True
        # return super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self._actual_hover = False
        # return super().leaveEvent(event)

    def is_actually_hovered(self):
        return self._actual_hover


    def optional_wheelEvent(self, event = False, custom_event = False) -> None:
        if custom_event:
            event = custom_event
            # Custom wheel events here.
            if event.scan_code == 7864320 and self.pie.get("w_up"):
                # Scroll up(7864320), away from the user
                self.run_pie_function(wheel=self.pie.get("w_up"))
            elif event.scan_code == 4287102976 and self.pie.get("w_down"):
                # Scroll down(4287102976), towards user
                self.run_pie_function(wheel=self.pie.get("w_down"))
            return

        # Default wheel event
        if event.angleDelta().y() > 0 and self.pie.get("onPie_w_up"):
            # Scroll up, away from the user
            self.run_pie_function(wheel=self.pie.get("onPie_w_up"))

        elif event.angleDelta().y() < 0 and self.pie.get("onPie_w_down"):
            # Scroll down, towards user
            self.run_pie_function(wheel=self.pie.get("onPie_w_down"))

        return super().wheelEvent(event)

    def btnAction(self):
        # print("button pressed")
        # print(self.sender().text())
        # pie_func = self.sender().pieSlice["function"]
        # params = self.sender().pieSlice["params"]
        self.run_pie_function()

    def run_pie_function(self, wheel = False):

        if wheel:
            pie_func, params = wheel
            # print(pie_func, params)
        else:
            pie_func = self.pieSlice["function"]
            params = self.pieSlice["params"]

        if pie_func.lower() == "none" or not pie_func:
            return
        if pie_func == "sendKeys": pieFunctions.sendKeys(params)
        if pie_func == "sendKeysAHK": pieFunctions.sendKeysTyping(params)
        if pie_func == "sendHotkey": pieFunctions.sendHotkey(params)
        if "brightness" in pie_func: pieFunctions.sendHotkey([pie_func, params[0]])