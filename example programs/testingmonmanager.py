from PySide2 import QtCore, QtWidgets
from time import sleep
from PySide2.QtGui import QCursor
from examplemonmanager import Monitor_Manager

class Window(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.resize(800, 600)

    
        
def qt_message_handler(mode, context, message):

    """This method handles warning messages, sometimes, it might eat up 
       some warning which won't be printed, so it is good to disable this
       when developing, debuging and testing."""
    
    if "QWindowsWindow::setGeometry: Unable to set geometry" in message:
        """This is ignore the warning message when changing the 
           screen on which app is shown on multi monitor systems.
           Qt automatically decides best size, that's I have ignored it here."""
        return

    if mode == QtCore.QtInfoMsg: mode = 'INFO'
    elif mode == QtCore.QtWarningMsg: mode = 'WARNING'
    elif mode == QtCore.QtCriticalMsg: mode = 'CRITICAL'
    elif mode == QtCore.QtFatalMsg: mode = 'FATAL'
    else: mode = 'DEBUG'
    print(f'qt_message_handler: line: {context.line}, func: {context.function}(), file: {context.file}')
    print(f'{mode}: {message}')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    QtCore.qInstallMessageHandler(qt_message_handler)
    mon_manager = Monitor_Manager(app.screens(), app.primaryScreen())


    cursorpos = QCursor.pos()
    mon_manager.move_to_active_screen(cursorpos, w)
    # w.showMaximized()
    w.showFullScreen()
    # print(w.size())

    i = 0
    while(i<2000000):
        i += 0.1
    print("loop over")
    # while this loop completes, move you mouse to another monitor, to test.

    cursorpos = QCursor.pos()
    mon_manager.move_to_active_screen(cursorpos, w)
    # w.showMaximized()
    w.showFullScreen()
    # print(w.size())
    
    
    # allScreens = app.desktop().geometry()
    sys.exit(app.exec_())