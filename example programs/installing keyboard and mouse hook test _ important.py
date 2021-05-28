# Some of this adapted from BoppreH's answer here:http://stackoverflow.com/questions/9817531/applying-low-level-keyboard-hooks-with-python-and-setwindowshookexa
import ctypes
import win32con
from ctypes import wintypes
from collections import namedtuple
from ctypes import windll, CFUNCTYPE, POINTER, c_int, c_void_p, byref
import atexit
from threading import Thread 


KeyEvents=namedtuple("KeyEvents",(['event_type', 'key_code',
                                             'scan_code', 'alt_pressed',
                                             'time']))
handlers=[]
def listener():
    """The listener listens to events and adds them to handlers"""
    event_types = {0x100: 'key down', #WM_KeyDown for normal keys
                   0x101: 'key up', #WM_KeyUp for normal keys
                   0x104: 'key down', # WM_SYSKEYDOWN, used for Alt key.
                   0x105: 'key up', # WM_SYSKEYUP, used for Alt key.
                   512: 'mouse move',
                   513: 'LButton Down',
                   514: 'LButton Up',
                   516: 'RButton Down',
                   517: 'RButton Up'
                  }
    global tid
    def low_level_handler(nCode, wParam, lParam):
        """
        Processes a low level Windows keyboard event.
        """
        event = KeyEvents(event_types[wParam], lParam[0], lParam[1],
                          lParam[2] == 32, lParam[3])
        for h in handlers:
            h(event)
        if event_types[wParam] == 'RButton Up':
            print("RButton down")
            windll.user32.UnhookWindowsHookEx(hook_id)
            # msg = None
            # windll.user32.PostThreadMessageW(tid, WM_QUIT, 0, 0)
            windll.user32.PostThreadMessageW(t.ident, WM_QUIT, 0, 0)
            # return wndll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)
            return -1
        #Be nice, return next hookk
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
    # windll.user32.PostThreadMessageW.argtypes = (c_int, c_int, c_int, c_int)
    # windll.user32.PostThreadMessageW.restype = wintypes.HMODULE
    # hook_id = windll.user32.SetWindowsHookExA(0x00D, pointer, windll.kernel32.GetModuleHandleW(None), 0)
    hook_id = windll.user32.SetWindowsHookExA(win32con.WH_KEYBOARD_LL, pointer, windll.kernel32.GetModuleHandleW(None), 0)
    # hook_id = windll.user32.SetWindowsHookExA.argtypes = (c_int, wintypes.HANDLE, wintypes.HMODULE, wintypes.DWORD)

    
    # Register to remove the hook when the interpreter exits.
    atexit.register(windll.user32.UnhookWindowsHookEx, hook_id)
    tid = kernel32.GetCurrentThreadId()
    print(tid)
    while True:
        msg = windll.user32.GetMessageW(None, 0, 0,0)
        print("asdfasdfasdfasdfasdf",msg)
        windll.user32.TranslateMessage(byref(msg))
        windll.user32.DispatchMessageW(byref(msg))


WM_QUIT = 0x0012
tid = None
kernel32 = ctypes.windll.kernel32
if __name__ == '__main__':
    def print_event(e):
        print(e)
        pass

    handlers.append(print_event)
    t = Thread(target=listener)
    t.start()
    # listener()