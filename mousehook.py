# Some of this adapted from BoppreH's answer here:http://stackoverflow.com/questions/9817531/applying-low-level-keyboard-hooks-with-python-and-setwindowshookexa
import ctypes
import win32con
from ctypes import wintypes
from collections import namedtuple

from ctypes import windll, CFUNCTYPE, POINTER, c_int, c_void_p, byref
import atexit


KeyEvents=namedtuple("KeyEvents",(['event_type', 'key_code',
                                             'scan_code', 'alt_pressed',
                                             'time']))
rmbUpHandlers=[]
lmbUpHandlers=[]
def listener(keyHeld):
    """The listener listens to events and adds them to mouseHandlers"""
    event_types = {512: 'mouse move', #WM_MouseMove
                   513: 'LButton Down',
                   514: 'LButton Up',
                   516: 'RButton Down',
                   517: 'RButton Up'
                  }
    def low_level_handler(nCode, wParam, lParam):
        """
        Processes a low level Windows mouse event.
        """
        event = KeyEvents(event_types[wParam], lParam[0], lParam[1], lParam[2] == 32, lParam[3])

        if event_types[wParam] == 'RButton Down':
            return -1
        if event_types[wParam] == 'LButton Down':
            return -1

        if event_types[wParam] == 'RButton Up':
            for handle in rmbUpHandlers:
                handle(event)
            # windll.user32.UnhookWindowsHookEx(hook_id)
            return -1

        if event_types[wParam] == 'LButton Up' and not keyHeld:
            # print(event_types[wParam])
            for handle in lmbUpHandlers:
                handle(event)
            return -1
        elif event_types[wParam] == 'LButton Up' and keyHeld:
            return -1

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
    pass

# mouseHandlers.append(print_event)

WM_QUIT = 0x0012
HOOK_ID = None

def mouseHook(keyHeld):
    listener(keyHeld)

def removeMouseHook():
    windll.user32.UnhookWindowsHookEx(HOOK_ID)
    HOOK_ID = None