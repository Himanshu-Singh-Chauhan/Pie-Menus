from PySide2.QtGui import QCursor, QScreen
# from PySide2 import QtCore, QtGui, QtWidgets

# enum _PROCESS_DPI_AWARENESS    
PROCESS_DPI_UNAWARE = 0
PROCESS_SYSTEM_DPI_AWARE = 1
PROCESS_PER_MONITOR_DPI_AWARE = 2
#  InnI: Get per-monitor DPI scaling factor (https://www.autoitscript.com/forum/topic/189341-get-per-monitor-dpi-scaling-factor/?tab=comments#comment-1359832)
DPI_AWARENESS_CONTEXT_UNAWARE = -1
DPI_AWARENESS_CONTEXT_SYSTEM_AWARE = -2
DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE = -3
DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4

TASKBARSIZE = 32



test = QScreen()
# test.

class Monitor_Manager:
    def __init__(self, screens, primary_screen = None) -> None:
        if primary_screen:
            self.primary_screen = primary_screen
        else:
            self.primary_screen = screens[0]
        self.screens = screens
        self.active_screen = self.primary_screen
        self.last_active_screen = self.primary_screen
        screens_count = len(screens)

    def get_desktop_area(self) -> int:
        pass

    def get_active_screen(self, curosrpos):

        """Active screen is the one which has mouse cursor in it."""

        active_screen = None
        
        for screen in self.screens:
            """top_lx is topleft x coordinate
               top_ly is top left y coordinate and so on"""
            top_lx, top_ly, bottom_rx, bottom_ry = screen.geometry().getCoords()
            if top_lx <= curosrpos.x() <= bottom_rx:
                if top_ly <= curosrpos.y() <= bottom_ry:
                    active_screen = screen
                    # print(active_screen.devicePixelRatio())
                    break

        if not active_screen:
            active_screen = self.primary_screen

        self.last_active_screen = self.active_screen
        self.active_screen = active_screen

        return active_screen

    def move_to_active_screen(self, cursorpos, window):
        if self.get_active_screen(cursorpos) == self.last_active_screen:
            return "no_change"
        top_lx, top_ly, width, height = self.active_screen.geometry().getRect()
        try:
            window.showNormal()
            window.move(top_lx, top_ly)
            # print(top_lx, top_ly)
            # print("moved")
        except Exception as e:
            print(e)
            print("window move to active screen failed, trying to open on primary screen")
            top_lx, top_ly, bottom_rx, bottom_ry = self.primary_screen.geometry().getCoords()
            window.move(top_lx, top_ly)