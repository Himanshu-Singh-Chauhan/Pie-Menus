# from PyQt5 import QtCore, QtGui, QtWidgets


# class PushButton(QtWidgets.QPushButton):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._animation = QtCore.QVariantAnimation(
#             startValue=QtGui.QColor("#4CAF50"),
#             endValue=QtGui.QColor("white"),
#             valueChanged=self._on_value_changed,
#             duration=400,
#         )
#         self._update_stylesheet(QtGui.QColor("white"), QtGui.QColor("black"))
#         self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

#     def _on_value_changed(self, color):
#         foreground = (
#             QtGui.QColor("black")
#             if self._animation.direction() == QtCore.QAbstractAnimation.Forward
#             else QtGui.QColor("white")
#         )
#         self._update_stylesheet(color, foreground)

#     def _update_stylesheet(self, background, foreground):

#         self.setStyleSheet(
#             """
#         QPushButton{
#             background-color: %s;
#             border: none;
#             color: %s;
#             padding: 16px 32px;
#             text-align: center;
#             text-decoration: none;
#             font-size: 16px;
#             margin: 4px 2px;
#             border: 2px solid #4CAF50;
#         }
#         """
#             % (background.name(), foreground.name())
#         )

#     def enterEvent(self, event):
#         self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
#         self._animation.start()
#         super().enterEvent(event)

#     def leaveEvent(self, event):
#         self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
#         self._animation.start()
#         super().leaveEvent(event)


# class Dialog(QtWidgets.QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.setWindowTitle(self.tr("Dialog"))

#         self.pushButton = PushButton()
#         self.pushButton.setText(self.tr("Click Here"))
#         self.pushButton.setSizePolicy(
#             QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
#         )

#         lay = QtWidgets.QVBoxLayout(self)
#         lay.addWidget(self.pushButton)

#         self.resize(400, 300)


# if __name__ == "__main__":
#     import sys

#     app = QtWidgets.QApplication(sys.argv)
#     w = Dialog()
#     w.show()
#     sys.exit(app.exec_())


# another example

# from PyQt5 import QtWidgets, QtGui, QtCore
# from colour import Color # pip install colour

# class Main(QtWidgets.QWidget):
# 	def __init__(self):
# 		super().__init__()
# 		self.setStyleSheet("QPushButton{height: 30px;width: 200px;}")

# 		layout = QtWidgets.QHBoxLayout()

# 		btn = Button("2020 is an interesting year.")
		
# 		layout.addStretch()
# 		layout.addWidget(btn)
# 		layout.addStretch()
# 		self.setLayout(layout)


# class Button(QtWidgets.QPushButton):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.shadow = QtWidgets.QGraphicsDropShadowEffect()
#         self.setGraphicsEffect(self.shadow)
#         self.tm = QtCore.QBasicTimer()
#         self.shadow.setOffset(0, 0)
#         self.shadow.setBlurRadius(20)
#         self.shadow.setColor(QtGui.QColor("#3F3F3F"))
#         self.mouse = ''
        
#         self.changeColor(color="lightgrey")

#         #button shadow grading.
#         self.expand = 0
#         self.maxExpand = 4 # expanding size - #optional
#         self.init_s_color = "#3F3F3F" #optional
#         self.end_s_color = "#FFFF33"  #optional
#         self.garding_s_seq = self.gradeColor(c1=self.init_s_color, 
# 									        c2=self.end_s_color, 
# 									        steps=self.maxExpand)
#         #button color grading.
#         self.grade = 0
#         self.maxGrade=15 # gradding size - #optional
#         self.init_bg_color = "lightgrey"   #optional
#         self.end_bg_color = "darkgrey"     #optional
#         self.gradding_bg_seq = self.gradeColor( c1=self.init_bg_color, 
# 									        	c2=self.end_bg_color, 
# 									        	steps=self.maxGrade)

#     def changeColor(self, color=(255,255,255)):
#         palette = self.palette()
#         palette.setColor(QtGui.QPalette.Button, QtGui.QColor(color))
#         self.setPalette(palette)

#     def gradeColor(self, c1, c2, steps):
#         return list([str(i) for i in Color(c1).range_to(Color(c2), steps)])

#     def enterEvent(self, e) -> None:
#         self.mouse = 'on'
#         #self.setGraphicsEffect(self.shadow)
#         self.tm.start(15, self)

#     def leaveEvent(self, e) -> None:
#         self.mouse = 'off'

#     def timerEvent(self, e) -> None:
        
#         if self.mouse == 'on' and self.grade < self.maxGrade:
#             self.grade += 1
#             self.changeColor(color=self.gradding_bg_seq[self.grade-1])
        
#         elif self.mouse == 'off' and self.grade > 0:
#             self.changeColor(color=self.gradding_bg_seq[self.grade-1])
#             self.grade -= 1

#         if self.mouse == 'on' and self.expand < self.maxExpand:
#             self.expand += 1
#             self.shadow.setColor(QtGui.QColor(self.garding_s_seq[self.expand-1]))
#             self.setGeometry(self.x()-1, int(self.y()-1), self.width()+2, self.height()+2)
        
#         elif self.mouse == 'off' and  self.expand > 0:
#             self.expand -= 1
#             self.setGeometry(self.x()+1, int(self.y()+1), self.width()-2, self.height()-2)
        
#         elif self.mouse == 'off' and self.expand in [0, self.maxExpand] and self.grade in [0, self.maxGrade]:
#             self.shadow.setColor(QtGui.QColor(self.init_s_color))
#             self.tm.stop()


# if __name__ == '__main__':
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     app.setStyle("Fusion")
#     main = Main()
#     main.show()
#     app.exec_()


from PyQt5 import QtCore, QtGui, QtWidgets


class LoginButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(60, 60)

        self.color1 = QtGui.QColor(255, 0, 68)
        self.color2 = QtGui.QColor(242, 252, 130)

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )

    def _animate(self, value):
        qss = """
            font: 75 10pt "Microsoft YaHei UI";
            font-weight: bold;
            color: rgb(255, 255, 255);
            border-style: solid;
            border-radius:21px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        qss += grad
        self.setStyleSheet(qss)

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)

    for i in range(5):
        button = LoginButton()
        button.setText("Login")
        lay.addWidget(button)
    lay.addStretch()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())