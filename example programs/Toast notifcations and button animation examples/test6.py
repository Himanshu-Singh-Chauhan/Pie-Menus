# -*-  coding: utf-8 -*-
 
# @author： daimashiren
# @time:    2020/07/06
from time import sleep
from PyQt5.QtCore import  Qt,QRect,QPoint,QTimer
from PyQt5.QtWidgets import QDialog,QLabel,QApplication,QHBoxLayout,QDesktopWidget
 
 
class Msg(QDialog):
    def __init__(self):
        super(Msg, self).__init__()
        self.ini_ui()
 
 
    def ini_ui(self):
        self.setWindowModality(Qt.NonModal)
        self.setWindowOpacity(0.8) # Set window transparency
        self.setStyleSheet("""
                QDialog{
                border: none;
                background:rgb(150,150,150,100);}
                """)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        win_center = QDesktopWidget().availableGeometry().center()
        geo = QRect(win_center.x() + 50, win_center.y() - 75, 300, 100)
        self.setGeometry(geo)
        self.setContentsMargins(0, 0, 0, 0)
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        self.msg_label = QLabel()
        self.msg_label.setStyleSheet("""
        QLabel{
            color:#7fccde;
            text-align:left;
            border:none;
            border-image:none;
            font-size:25px;
            font-weight:300;
                         font-family: "HeiTi","Arial","Microsoft YaHei","Song Ti",sans-serif;
        }
        """)
        main_layout.addWidget(self.msg_label)
 
        self.fade_timer = QTimer()
        self.fade_timer.setInterval(2000)
        self.fade_timer.timeout.connect(self.faded_out)
 
         # (Central display) can only be called after the show method
    def center_show(self, offset):
        geo = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center() # Get the display resolution and find the middle point
        if offset:
            print("window offset")
            geo.moveCenter(cp + offset) # offset the midpoint of the window
        else:
                         geo.moveCenter(cp) # Put the middle point of the window in the middle of the screen
        self.move(geo.topLeft())
 
    def show_msg(self,text):
        self.fade_timer.start()
        self.msg_label.setText(text)
        self.msg_label.repaint()
        self.raise_()
        self.show()
        self.center_show(QPoint(75,0))
        self.exec_() # Animation pop up
        sleep(0.5)
 
 
 
    def faded_out(self):
        print("Window fade")
        for i in range(80,0,-1):
            opacity = i/100
            print("opacity:",opacity)
            self.setWindowOpacity(opacity) # Set window transparency
            self.repaint()
            QApplication.processEvents()
            sleep(0.05)
 
        self.fade_timer.stop()
        self.close()
 
 
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    msg = Msg()
    msg.show_msg("Test information...")
    sys.exit(app.exec_())


