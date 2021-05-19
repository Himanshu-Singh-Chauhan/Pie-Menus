import mouse
import pynput
# from ctypes import *
import keyboard
from time import sleep
import win32api
import win32con
import os


from ahk import AHK, Hotkey
import ahk
from ahk.directives import NoTrayIcon

# def on_move(x, y):
#     print(x, y)

def on_click(x, y, button, pressed):
    print(button, pressed)

# def on_scroll(x, y, dx, dy):
#     print(dx, dy)

# def toggleInput(toggle):
#     # print("oyo")
#     ok = windll.user32.BlockInput(toggle)

# input = False
# def temp():
#     global input
#     print(input)
#     if input == False:
#         toggleInput(True)
#         input = True
#     else:
#         toggleInput(False)
#         input = False


# mouse.on_click(on_click)


# keyboard.add_hotkey('r', temp, suppress=True)

# sleep(100)
# print("sleeep over")
# ok = windll.user32.BlockInput(False)
# with pynput.mouse.Listener(on_right_click=on_click, on_click=on_click) as listener:
#     listener.join()


ahk = AHK(directives=[NoTrayIcon])

script = 'Send {esc}'
ahk_script = 'Send {RButton Down}'
# ahk_script = 'MouseClick, right,,,,,Up'
# ahk.run_script(ahk_script, blocking=False)
key_combo = 'RButton' # Define an AutoHotkey key combonation
# script = 'EnvSet, RightClickState, himanshu'  # Define an ahk script
hotkey = Hotkey(ahk, key_combo, ahk_script) # Create Hotkey
# ahk.run_script('EnvSet, RightClickState, himanshu')
# os.startfile()
# print(os.environ["NUMBER_OF_PROCESSORS"])

hotkey.start()  #  Start listening for hotkey

# try:
#     settings = open(os.path.join(script_dir, "Rmb.ahk"), "r")
#     print(settings)
#     print("settings")
# except:
#     print("could not locate or load")

# print(settings)
# while True:
    # print(mouse.is_pressed(button='right'))
# hotkey.stop()
ahk.run_script(script_text=script)
# print("yo", mouse.is_pressed(button='right'))


#     # print(win32api.GetAsyncKeyState(0x02))
#     print(win32api.GetAsyncKeyState(win32con.VK_RBUTTON))
#     # print(mouse.is_pressed(button='right'))
sleep(1000)