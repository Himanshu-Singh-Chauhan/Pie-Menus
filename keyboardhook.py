# Some of this adapted from BoppreH's answer here:http://stackoverflow.com/questions/9817531/applying-low-level-keyboard-hooks-with-python-and-setwindowshookexa
import ctypes
import win32con
from ctypes import wintypes
from collections import namedtuple

from ctypes import windll, CFUNCTYPE, POINTER, c_int, c_void_p, c_uint, byref
import atexit


# https://msdn.microsoft.com/en-us/library/windows/desktop/ms646307(v=vs.85).aspx
MAPVK_VK_TO_CHAR = 2
MAPVK_VK_TO_VSC = 0
MAPVK_VSC_TO_VK = 1
MAPVK_VK_TO_VSC_EX = 4
MAPVK_VSC_TO_VK_EX = 3

MapVirtualKey = windll.user32.MapVirtualKeyW
MapVirtualKey.argtypes = [c_uint, c_uint]
MapVirtualKey.restype = c_uint

official_virtual_keys = {
    0x03: ('control-break processing', False),
    0x08: ('backspace', False),
    0x09: ('tab', False),
    0x0c: ('clear', False),
    0x0d: ('enter', False),
    0x10: ('shift', False),
    0x11: ('ctrl', False),
    0x12: ('alt', False),
    0x13: ('pause', False),
    0x14: ('caps lock', False),
    0x15: ('ime kana mode', False),
    0x15: ('ime hanguel mode', False),
    0x15: ('ime hangul mode', False),
    0x17: ('ime junja mode', False),
    0x18: ('ime final mode', False),
    0x19: ('ime hanja mode', False),
    0x19: ('ime kanji mode', False),
    0x1b: ('esc', False),
    0x1c: ('ime convert', False),
    0x1d: ('ime nonconvert', False),
    0x1e: ('ime accept', False),
    0x1f: ('ime mode change request', False),
    0x20: ('spacebar', False),
    0x21: ('page up', False),
    0x22: ('page down', False),
    0x23: ('end', False),
    0x24: ('home', False),
    0x25: ('left', False),
    0x26: ('up', False),
    0x27: ('right', False),
    0x28: ('down', False),
    0x29: ('select', False),
    0x2a: ('print', False),
    0x2b: ('execute', False),
    0x2c: ('print screen', False),
    0x2d: ('insert', False),
    0x2e: ('delete', False),
    0x2f: ('help', False),
    0x30: ('0', False),
    0x31: ('1', False),
    0x32: ('2', False),
    0x33: ('3', False),
    0x34: ('4', False),
    0x35: ('5', False),
    0x36: ('6', False),
    0x37: ('7', False),
    0x38: ('8', False),
    0x39: ('9', False),
    0x41: ('a', False),
    0x42: ('b', False),
    0x43: ('c', False),
    0x44: ('d', False),
    0x45: ('e', False),
    0x46: ('f', False),
    0x47: ('g', False),
    0x48: ('h', False),
    0x49: ('i', False),
    0x4a: ('j', False),
    0x4b: ('k', False),
    0x4c: ('l', False),
    0x4d: ('m', False),
    0x4e: ('n', False),
    0x4f: ('o', False),
    0x50: ('p', False),
    0x51: ('q', False),
    0x52: ('r', False),
    0x53: ('s', False),
    0x54: ('t', False),
    0x55: ('u', False),
    0x56: ('v', False),
    0x57: ('w', False),
    0x58: ('x', False),
    0x59: ('y', False),
    0x5a: ('z', False),
    0x5b: ('left windows', False),
    0x5c: ('right windows', False),
    0x5d: ('applications', False),
    0x5f: ('sleep', False),
    0x60: ('0', True),
    0x61: ('1', True),
    0x62: ('2', True),
    0x63: ('3', True),
    0x64: ('4', True),
    0x65: ('5', True),
    0x66: ('6', True),
    0x67: ('7', True),
    0x68: ('8', True),
    0x69: ('9', True),
    0x6a: ('*', True),
    0x6b: ('+', True),
    0x6c: ('separator', True),
    0x6d: ('-', True),
    0x6e: ('decimal', True),
    0x6f: ('/', True),
    0x70: ('f1', False),
    0x71: ('f2', False),
    0x72: ('f3', False),
    0x73: ('f4', False),
    0x74: ('f5', False),
    0x75: ('f6', False),
    0x76: ('f7', False),
    0x77: ('f8', False),
    0x78: ('f9', False),
    0x79: ('f10', False),
    0x7a: ('f11', False),
    0x7b: ('f12', False),
    0x7c: ('f13', False),
    0x7d: ('f14', False),
    0x7e: ('f15', False),
    0x7f: ('f16', False),
    0x80: ('f17', False),
    0x81: ('f18', False),
    0x82: ('f19', False),
    0x83: ('f20', False),
    0x84: ('f21', False),
    0x85: ('f22', False),
    0x86: ('f23', False),
    0x87: ('f24', False),
    0x90: ('num lock', False),
    0x91: ('scroll lock', False),
    0xa0: ('left shift', False),
    0xa1: ('right shift', False),
    0xa2: ('left ctrl', False),
    0xa3: ('right ctrl', False),
    0xa4: ('left menu', False),
    0xa5: ('right menu', False),
    0xa6: ('browser back', False),
    0xa7: ('browser forward', False),
    0xa8: ('browser refresh', False),
    0xa9: ('browser stop', False),
    0xaa: ('browser search key', False),
    0xab: ('browser favorites', False),
    0xac: ('browser start and home', False),
    0xad: ('volume mute', False),
    0xae: ('volume down', False),
    0xaf: ('volume up', False),
    0xb0: ('next track', False),
    0xb1: ('previous track', False),
    0xb2: ('stop media', False),
    0xb3: ('play/pause media', False),
    0xb4: ('start mail', False),
    0xb5: ('select media', False),
    0xb6: ('start application 1', False),
    0xb7: ('start application 2', False),
    0xbb: ('+', False),
    0xbc: (',', False),
    0xbd: ('-', False),
    0xbe: ('.', False),
    # 0xbe:('/', False), # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '/?.
    0xe5: ('ime process', False),
    0xf6: ('attn', False),
    0xf7: ('crsel', False),
    0xf8: ('exsel', False),
    0xf9: ('erase eof', False),
    0xfa: ('play', False),
    0xfb: ('zoom', False),
    0xfc: ('reserved ', False),
    0xfd: ('pa1', False),
    0xfe: ('clear', False),
}

virtual_key_reverse = { 
    'control-break processing': 3,
    'backspace': 8, 
    'tab': 9, 
    'clear': 254, 
    'enter': 13, 
    'shift': 16, 
    'ctrl': 17, 
    'alt': 18, 
    'pause': 19, 
    'caps lock': 20, 
    'ime hangul mode': 21, 
    'ime junja mode': 23, 
    'ime final mode': 24, 
    'ime kanji mode': 25, 
    'esc': 27, 
    'ime convert': 28, 
    'ime nonconvert': 29, 
    'ime accept': 30, 
    'ime mode change request': 31, 
    'spacebar': 32, 
    'page up': 33, 
    'page down': 34, 
    'end': 35, 
    'home': 36, 
    'left': 37, 
    'up': 38, 
    'right': 39, 
    'down': 40, 
    'select': 41, 
    'print': 42, 
    'execute': 43, 
    'print screen': 44, 
    'insert': 45, 
    'delete': 46, 
    'help': 47, 
    '0': 96, 
    '1': 97, 
    '2': 98, 
    '3': 99, 
    '4': 100, 
    '5': 101, 
    '6': 102, 
    '7': 103, 
    '8': 104, 
    '9': 105, 
    'a': 65, 
    'b': 66, 
    'c': 67, 
    'd': 68, 
    'e': 69, 
    'f': 70, 
    'g': 71, 
    'h': 72, 
    'i': 73, 
    'j': 74, 
    'k': 75, 
    'l': 76, 
    'm': 77, 
    'n': 78, 
    'o': 79, 
    'p': 80, 
    'q': 81, 
    'r': 82, 
    's': 83, 
    't': 84, 
    'u': 85, 
    'v': 86, 
    'w': 87, 
    'x': 88, 
    'y': 89, 
    'z': 90, 
    'left windows': 91, 
    'right windows': 92, 
    'applications': 93, 
    'sleep': 95, 
    '*': 106, 
    '+': 187, 
    'separator': 108, 
    '-': 189,
    'decimal': 110, 
    '/': 111, 
    'f1': 112, 
    'f2': 113, 
    'f3': 114, 
    'f4': 115, 
    'f5': 116, 
    'f6': 117, 
    'f7': 118, 
    'f8': 119, 
    'f9': 120, 
    'f10': 121, 
    'f11': 122, 
    'f12': 123, 
    'f13': 124, 
    'f14': 125, 
    'f15': 126, 
    'f16': 127, 
    'f17': 128, 
    'f18': 129, 
    'f19': 130, 
    'f20': 131, 
    'f21': 132, 
    'f22': 133, 
    'f23': 134, 
    'f24': 135, 
    'num lock': 144, 
    'scroll lock': 145, 
    'left shift': 160, 
    'right shift': 161, 
    'left ctrl': 162, 
    'right ctrl': 163, 
    'left menu': 164, 
    'right menu': 165, 
    'browser back': 166, 
    'browser forward': 167, 
    'browser refresh': 168, 
    'browser stop': 169, 
    'browser search key': 170, 
    'browser favorites': 171, 
    'browser start and home': 172, 
    'volume mute': 173, 
    'volume down': 174, 
    'volume up': 175, 
    'next track': 176, 
    'previous track': 177, 
    'stop media': 178, 
    'play/pause media': 179, 
    'start mail': 180, 
    'select media': 181, 
    'start application 1': 182, 
    'start application 2': 183, 
    ',': 188, 
    '.': 190, 
    'ime process': 229, 
    'attn': 246, 
    'crsel': 247, 
    'exsel': 248, 
    'erase eof': 249, 
    'play': 250, 
    'zoom': 251, 
    'reserved ': 252, 
    'pa1': 253
    }


KeyEvents = namedtuple("KeyEvents", (['event_type', 'key_code',
                                      'scan_code', 'alt_pressed',
                                      'time']))
HKeyReleaseHandlers = []


def listener(hotkey):
    hotkey = virtual_key_reverse[hotkey]
    """The listener listens to events and adds them to keyboardHandlers"""
    event_types = {0x100: 'key down',  # WM_KeyDown for normal keys
                   0x101: 'key up',  # WM_KeyUp for normal keys
                   0x104: 'key down',  # WM_SYSKEYDOWN, used for Alt key.
                   0x105: 'key up',  # WM_SYSKEYUP, used for Alt key.
                   }

    def low_level_handler(nCode, wParam, lParam):
        """
        Processes a low level Windows keyboard event.
        """
        event = KeyEvents(
            event_types[wParam], lParam[0], lParam[1], lParam[2] == 32, lParam[3])

        pressedKey = MapVirtualKey(lParam[0], MAPVK_VK_TO_CHAR)


        if event_types[wParam] == 'key down':
            if hotkey == pressedKey:
                print("ore")
                return -1

        if event_types[wParam] == 'key up':
            if hotkey == pressedKey:
                print(pressedKey, hotkey)
                for handle in HKeyReleaseHandlers:
                    handle(event)
                return -1

        # Be nice, return next hook
        return windll.user32.CallNextHookEx(hook_id, nCode, wParam, lParam)

    # Our low level handler signature.
    CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
    # Convert the Python handler into C pointer.
    pointer = CMPFUNC(low_level_handler)
    # Added 4-18-15 for move to ctypes:
    windll.kernel32.GetModuleHandleW.restype = wintypes.HMODULE
    windll.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
    # Hook both key up and key down events for common keys (non-system).
    windll.user32.SetWindowsHookExA.argtypes = (
        c_int, wintypes.HANDLE, wintypes.HMODULE, wintypes.DWORD)
    HOOK_ID = hook_id = windll.user32.SetWindowsHookExA(
        win32con.WH_KEYBOARD_LL, pointer, windll.kernel32.GetModuleHandleW(None), 0)
    

    # Register to remove the hook when the interpreter exits.
    atexit.register(windll.user32.UnhookWindowsHookEx, hook_id)
    try:
        msg = windll.user32.GetMessageW(None, 0, 0, 0)
        windll.user32.TranslateMessage(byref(msg))
        windll.user32.DispatchMessageW(byref(msg))
    except:
        # print("Exception raised in keyboard hook thread (maybe WM_QUIT)")
        pass


def print_event(e):
    print(e)
    pass

# keyboardHandlers.append(print_event)


WM_QUIT = 0x0012
HOOK_ID = None


def keyboardHook(hotkey):
    listener(hotkey)


def removekeyboardHook():
    windll.user32.UnhookWindowsHookEx(HOOK_ID)
    HOOK_ID = None