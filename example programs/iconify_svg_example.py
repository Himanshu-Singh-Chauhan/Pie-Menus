# importing libraries
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys
import os
import iconify as ico
import subprocess
from iconify.qt import QtGui, QtWidgets
script_dir = os.path.dirname(__file__)

anim = ico.anim.Breathe()
icon = ico.Icon(os.path.join(script_dir, 'default.svg'), anim = anim)
# icon = ico.Icon(
#     # The ':' here denotes a directory and provides cross platform support.
#     'emojione-legacy:1F394',  
#     anim=anim,
# )
# button = QtWidgets.QPushButton()
# button.setIcon(icon)
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Python ")

        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for widgets
    def UiComponents(self):

        # creating a push button
        button = QPushButton("CLICK", self)

        # setting geometry of button
        button.setGeometry(200, 150, 100, 30)

        # adding action to a button
        button.clicked.connect(self.clickme)

        # button.setIcon(icon)
        icon.setAsButtonIcon(button)
        anim.start()

    # action method
    def clickme(self):

        # printing pressed
        print("pressed")
        subprocess.Popen([__file__])
        sys.exit(0)

# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec_())
