from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
 
class myLabel(QLabel):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()

    def enterEvent(self, a0) -> None:
        self.setStyleSheet("""
        
        QLabel{text-decoration: underline;
        /*background-color:red;*/}""")
 
        return super().enterEvent(a0)

    def leaveEvent(self, a0) -> None:
        self.setStyleSheet("""QLabel{}""")
 
        return super().leaveEvent(a0)

 
class Wind(QDialog):
    clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.label = myLabel()
        self.label.setText('This is a text label')
 
        vb = QVBoxLayout()
        vb.addWidget(self.label)
        self.setLayout(vb)
        
        self.label.clicked.connect(self.showData)
        self.clicked.connect(self.showData)
 
    def showData(self):
        print('ok')
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Wind()
    win.show()
    sys.exit(app.exec_())