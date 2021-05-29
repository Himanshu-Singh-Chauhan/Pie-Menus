import os
import json
import pywintypes
from win32gui import GetWindowText, GetForegroundWindow, GetClassName
from win32process import GetWindowThreadProcessId
import psutil
from piemenu_backend import *
from systemTrayIcon import SystemTrayIcon
from threading import Thread
import mousehook
import datetime
from re import match as re_match
# import keyboardhook
from fastIO import *
class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re_match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

# active window example calls
# w = WindowMgr()
# w.find_window_wildcard(".*Hello.*")
# w.set_foreground()

# Important Note: As of now Trigger keys cannot be same as hotkeys in a single profile

WM_QUIT = 0x0012
thread_id = None
# kernel32 = ctypes.windll.kernel32

class ActiveProfile:
    def __init__(self) -> None:
        # Attributes
        self.activeWindow = None
        self.activeTittle = None
        self.handle_foreground = None
        self.profile = None
        self.loadedHotkeys = []
        self.loadedTriggerKeys = []
        self.A_ThisHotkey = None
        self.A_TriggerKey = None

        self.sameTKeyHKey = None

        self.keyHeld = False
        self.isMenuOpen = False
        self.openPieMenu = None

        self.isRMBup = False
        self.isRMBdown = False
        self.isLMBup = False
        self.isLMBdown = False

        # First default runs
        self.loadGlobal()
        self.timerCheckHotkey = QTimer()
        self.timerCheckHotkey.timeout.connect(self.isHotkeyEvent)
        self.timerCheckHotkey.start(25)

        self.mouseThread = Thread(target = mousehook.mouseHook)
        mousehook.rmbUpHandlers.append(self.regRMBup)
        mousehook.lmbUpHandlers.append(self.regLMBup)

        # Aliases
        # self.chkr = self.checkHeldKeyReleased()

        # Timers
        self.timerKeyHeld = QTimer()
        self.timerKeyHeld.timeout.connect(self.checkHeldKeyReleased)
        self.timerKeyHeld.timeout.connect(self.isTKeyEvent)
        self.timerKeyHeld.timeout.connect(self.lmbTrigger)
        self.timerKeyHeld.timeout.connect(self.menuCancel)


        # Beta variables
        self.menu_open_pos = None
        self.menu_open_time = None
        self.timer_checkKeyHeld = QTimer()
        self.timer_checkKeyHeld.timeout.connect(self.checkKeyHeld)
        self.waitHKey = QTimer()
        self.waitHKey.timeout.connect(self.waitHKeyrelease)
        self.counter = 0
        # self.keyboardThread = Thread(target = keyboardhook.keyboardHook)
        # keyboardhook.HKeyReleaseHandlers.append(self.test)

        self.HKeyLetgo = True


    def changeDetected(self, activeWindow, activeTittle, handle_foreground):
        global regApps
        self.handle_foreground = handle_foreground
        if activeWindow not in regApps:
            self.loadGlobal()
            return
            
        self.activeWindow = activeWindow
        self.activeTittle = activeTittle
        self.loadProfile()
        self.loadHotkeys()

    def loadHotkeys(self):
        self.flushHotkeys()
        for menus in self.profile["pieMenus"]:
            if menus["enable"] == False or menus["enable"] == 0:
                continue
            # keyboard.add_hotkey(menus["hotkey"], doNothing, suppress=True)
            keyboard.add_hotkey(menus["hotkey"], self.registerHotkeyEvent, suppress=True, args = [menus["hotkey"], menus])
            self.loadedHotkeys.append(menus["hotkey"])
        
    def loadTriggerKeys(self):
        # enable the following logic if hotkeys and triggerkeys are allowed to be same/clash.
        # for key in self.loadedHotkeys:
        #     if key != self.A_ThisHotkey:
        #         keyboard.remove_hotkey(key)
            
        for pies in self.openPieMenu["pies"]:
            if pies["triggerKey"] == self.A_ThisHotkey:
                self.sameTKeyHKey = pies
                continue
            if pies["triggerKey"] == "None":
                pass
            else:
                keyboard.add_hotkey(pies["triggerKey"], self.registerTKeyEvent, suppress=True, args=[pies["triggerKey"], pies])
                self.loadedTriggerKeys.append(pies["triggerKey"])


    def loadFinalTriggerKey(self):
        if self.sameTKeyHKey == None: return

        keyboard.add_hotkey(self.sameTKeyHKey["triggerKey"], self.registerTKeyEvent, suppress=True, args=[self.sameTKeyHKey["triggerKey"], self.sameTKeyHKey])
        self.loadedTriggerKeys.append(self.sameTKeyHKey["triggerKey"])
        # self.sameTKeyHKey = None

    def registerTKeyEvent(self, Tkey, pie):
        self.A_TriggerKey = Tkey
        self.triggeredPieSlice = pie

    def isTKeyEvent(self):
        if self.A_TriggerKey == None: return
        self.launchByTriggerKey()
        
    def unloadTriggerKeys(self):
        # if len(self.loadedTriggerKeys) == 0:
        #     return
        # for Tkey in self.loadedTriggerKeys:
        #     keyboard.remove_hotkey(Tkey)
        self.loadedTriggerKeys.clear()
        self.loadHotkeys()

    def launchByTriggerKey(self):
        window.launchByTrigger(int(self.triggeredPieSlice["PieNumber"]) - 1)
        self.resetAttributesOnMenuClose()


    def flushHotkeys(self):
        if len(self.loadedHotkeys):
            keyboard.unhook_all_hotkeys()
        
        self.loadedHotkeys.clear()

    def loadProfile(self):
        global settings
        for profile in settings["appProfiles"]:
            if profile["ahkHandle"] == self.activeWindow:
                self.profile = profile
                break

    def loadGlobal(self):
        global settings

        # Store the global profile in a variable globalProifle
        # so no need to search for it, and keep this logic below if global is not found in globalProfile var

        self.activeWindow = None
        for profile in settings["appProfiles"]:
            if profile["ahkHandle"] == "ahk_group regApps":
                self.profile = profile
                break
        self.loadHotkeys()

    def registerHotkeyEvent(self, hotkey, menus):
        self.A_ThisHotkey = hotkey
        self.openPieMenu = menus
        # --------- Obselete code -------------
        # for hotkey in self.loadedHotkeys:
        #     if keyboard.is_pressed(hotkey):
        #         self.A_ThisHotkey = hotkey
        #         break
        # --------- /Obselete code ------------

    def isHotkeyEvent(self):
        if self.A_ThisHotkey == None: return
        self.hotkeyEvent()

        
    def hotkeyEvent(self):
        if self.isMenuOpen == False and self.HKeyLetgo:
        # if self.isMenuOpen == False:
            self.launch_pie_menus()
            # keep the following call as it is, do not run it on seperate thread(no problems though in doing that, just saving some CPU power).
            # self.checkKeyHeld()

    def launch_pie_menus(self):
        window.showFullScreen()
        win32gui.SetForegroundWindow(self.handle_foreground) 
        self.isMenuOpen = True
        window.showMenu(self.openPieMenu)
        self.initMosPos = mouse.get_position()
        self.loadTriggerKeys()

        self.timerKeyHeld.start(25)
        self.mouseThread = Thread(target = mousehook.mouseHook, args = [self.keyHeld] )
        self.mouseThread.start()

        self.menu_open_pos = GetMousePos()
        self.menu_open_pos = QtCore.QPoint(self.menu_open_pos.x(), self.menu_open_pos.y())
        self.menu_open_time = datetime.datetime.now()
        self.timer_checkKeyHeld.start(194)

    def checkKeyHeld(self):
        # sleep(2.15)
        if self.menu_open_time == None:
            self.timer_checkKeyHeld.stop()
            return
        # time_elapsed = datetime.datetime.now() - self.menu_open_time
        # fast_out( time_elapsed.total_seconds())
        # if time_elapsed.total_seconds() < 0.2:
            # return

        pos = GetMousePos()
        currentMousePos = QtCore.QPoint(pos.x(), pos.y())
        mouseInCircle = (currentMousePos.x() - self.menu_open_pos.x())**2 + (currentMousePos.y() - self.menu_open_pos.y())**2 < self.openPieMenu["inRadius"]**2

        if keyboard.is_pressed(self.A_ThisHotkey):
            self.keyHeld = True
        elif not mouseInCircle:
            self.keyHeld = True
        else:
            self.keyHeld = False
            self.loadFinalTriggerKey()
        self.timer_checkKeyHeld.stop()
        # self.keyboardThread = Thread(target = keyboardhook.keyboardHook, args=self.A_ThisHotkey)

        
    def checkHeldKeyReleased(self):
        if self.keyHeld and keyboard.is_pressed(self.A_ThisHotkey):
            pass
        elif self.keyHeld == False:
            if not window.isMenuOpen():
                self.resetAttributesOnMenuClose()
        else:
            window.releasedHeldKey()
            self.resetAttributesOnMenuClose()

    def lmbTrigger(self):
        if self.isLMBup:
            window.releasedHeldKey()
            self.resetAttributesOnMenuClose()

    def menuCancel(self):
        if keyboard.is_pressed('esc') or self.isRMBup:
            window.killMenu()
            self.resetAttributesOnMenuClose()

    def regRMBdown(self, event):
        self.isRMBdown = True

    def regRMBup(self, event):
        self.isRMBup = True

    def regLMBdown(self, event):
        self.isLMBdown = True

    def regLMBup(self, event):
        self.isLMBup = True

    def waitHKeyrelease(self):
        if self.counter < 100: self.counter += 1
        if (not keyboard.is_pressed(self.A_ThisHotkey)) and self.counter >= 6:
            self.A_ThisHotkey = None
            self.HKeyLetgo = True
            self.waitHKey.stop()
    #     # if self.temp == True:
    #     #     windll.user32.PostThreadMessageW(self.keyboardThread.ident, WM_QUIT, 0, 0)
    #     #     self.keyboardThread.join()
    #     #     self.HKeyLetgo = True
    #     #     self.waitHKey.stop()

    def resetAttributesOnMenuClose(self):
        self.menu_open_pos = None
        self.menu_open_time = None
        self.initMosPos = None
        self.isLMBup = False
        self.isRMBup = False
        windll.user32.PostThreadMessageW(self.mouseThread.ident, WM_QUIT, 0, 0)
        self.mouseThread.join()
        self.unloadTriggerKeys()
        self.timerKeyHeld.stop()
        self.keyHeld = False
        self.isMenuOpen = False
        self.openPieMenu = None
        self.A_TriggerKey = None
        self.sameTKeyHKey = None
        self.HKeyLetgo = False
        # self.A_ThisHotkey = set to None in waitHKeyrelease method
        self.counter = 0
        self.HKeyLetgo = False
        self.waitHKey.start(25)
        # window.hide() # this will hide the window after menu is closed.
# -------------------------------Class End--------------------------------------

# Global varibals:
debugMode = False
flag = False
hold = False

# ----Obselete method---------
# def doNothing():
#     # this just does nothing, is used when to detect hotkey and do nothing
#     pass


def detectWindowChange():
    global activeProfile
    global settings

    previousActiveWindow = activeProfile.activeWindow
    try:
        handle_foreground = GetForegroundWindow()
        activeTittle = GetWindowText(handle_foreground)
        pid = GetWindowThreadProcessId(handle_foreground)
        rootExe = psutil.Process(pid[-1]).name()
    except:
        return

    activeWindow = GetClassName(handle_foreground)
    # print(previousActiveWindow)
    if previousActiveWindow == activeWindow:
        return
    else:
        activeProfile.changeDetected(activeWindow, activeTittle, handle_foreground)
    


# Json settings loading
script_dir = os.path.dirname(__file__)
try:
    settings = open(os.path.join(script_dir, "settings/appProfiles.json"))
    settings = json.load(settings)
except:
    print("could not locate or load the json settings - appProfiles")

try:
    globalSettings = open(os.path.join(script_dir, "settings/globalSettings.json"))
    globalSettings = json.load(globalSettings)
except:
    print("could not locate or load the json globalSettings - globalSettings")


# ------------------------------------ MAIN ---------------------------------
app = QtWidgets.QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

app_icon = "C:\\Users\\S\\Downloads\\pexels-pixabay-38537.jpg"
tray_icon = QtGui.QIcon(os.path.join(script_dir, "resources/icons/tray_icon.png"))

# tray icon attribution : # icon type 2: <div>Icons made by <a href="https://www.flaticon.com/authors/ultimatearm" title="ultimatearm">ultimatearm</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# tray icon link : https://www.flaticon.com/free-icon/pie_1411020?term=pies&related_id=1411020

trayWidgetQT = QWidget()
trayWidget = SystemTrayIcon(QtGui.QIcon(tray_icon), trayWidgetQT)
trayWidgetQT.setStyleSheet(pie_themes.QMenu)
trayWidget.show()

window = Window(settings, globalSettings["globalSettings"])

# *****IMPORTANT********: # get the mouse pos here by itself to increase accuracy of opening position.

# Registering the app profiles 
regApps = []
for profiles in settings["appProfiles"]:
    if profiles["ahkHandle"] == "ahk_group regApps":
        continue
    # do not register profile if not enabled
    if profiles["enable"] == 0:
        continue
    regApps.append(profiles["ahkHandle"])


activeProfile = ActiveProfile()


# Timers
timerWinChange = QTimer()
timerWinChange.timeout.connect(detectWindowChange)

# Timer starts
timerWinChange.start(100)

# ----------------------END-----------------------------
# This statement has to stay the last line
# - everything below it will go out of scope of any thing.
sys.exit(app.exec_())
# ----------------------/END-----------------------------