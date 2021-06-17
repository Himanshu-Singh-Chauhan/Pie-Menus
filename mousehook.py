# Some of this adapted from BoppreH's answer here:http://stackoverflow.com/questions/9817531/applying-low-level-keyboard-hooks-with-python-and-setwindowshookexa
import ctypes
import win32con
from ctypes import wintypes
from collections import namedtuple
from ctypes import windll, CFUNCTYPE, POINTER, c_int, c_void_p, byref
from key_codes import mouse_codes
import atexit


KeyEvents=namedtuple("KeyEvents",(['event_type', 'key_code',
                                             'scan_code', 'alt_pressed',
                                             'time']))
mouseHandlers=[]
def listener():
    """The listener listens to events and adds them to mouseHandlers"""
    
    def low_level_handler(nCode, wParam, lParam):
        """
        Processes a low level Windows mouse event.
        """
        event = KeyEvents(mouse_codes[wParam], lParam[0], lParam[1], lParam[2] == 32, lParam[3])

        if mouse_codes.get(wParam):
            returnval = None
            for handle in mouseHandlers:
                # return value from last handler will be used, obviously.
                returnval = handle(event)

            if returnval == -1: return -1
            if returnval == "pass_event":
                return windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)

        #Be nice, return next hook
        return windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)
    
    # Our low level handler signature.
    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    # Convert the Python handler into C pointer.
    pointer = CMPFUNC(low_level_handler)
    #Added 4-18-15 for move to ctypes:
    windll.kernel32.GetModuleHandleW.restype = wintypes.HMODULE
    windll.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
    # Hook both key up and key down events for common keys (non-system).
    windll.user32.SetWindowsHookExA.argtypes = (c_int, wintypes.HANDLE, wintypes.HMODULE, wintypes.DWORD)
    hook_id = windll.user32.SetWindowsHookExA(win32con.WH_MOUSE_LL, pointer, windll.kernel32.GetModuleHandleW(None), 0)
    global HOOK_ID
    HOOK_ID = hook_id

    # Register to remove the hook when the interpreter exits.
    atexit.register(windll.user32.UnhookWindowsHookEx, hook_id)
    try:
        msg = windll.user32.GetMessageW(None, 0, 0,0)
        windll.user32.TranslateMessage(byref(msg))
        windll.user32.DispatchMessageW(byref(msg))
    except:
        # print("Exception raised in mouse hook thread (maybe WM_QUIT)")
        pass

def print_event(e):
    print(e)
    wParam = e[0]
    # pass

# mouseHandlers.append(print_event)

WM_QUIT = 0x0012
HOOK_ID = None

def mouseHook():
    listener()

def removeMouseHook():
    global HOOK_ID
    windll.user32.UnhookWindowsHookEx(HOOK_ID)
    HOOK_ID = None