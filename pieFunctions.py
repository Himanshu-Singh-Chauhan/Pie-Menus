from time import sleep
import keyboard
import screen_brightness_control as sbc
# as of now, recieving all params as one list in one var
# receive them directly as parameters

def sendKeys(params):
    params = params[0]
    # print(params)
    keyboard.write(params)

def sendKeysTyping(params):
    params = params[0]
    for ch in params:
        keyboard.write(ch)

def sendHotkey(params):
    hotkey = params[0]

    try: repeat_count = params[1]
    except: repeat_count = 1

    if "brightness" in hotkey:
        brightness_control(params)
        return

    for _ in range(int(repeat_count)):
        keyboard.send(hotkey)

def runScript(params):
    pass

def brightness_control(params):
    hotkey = params[0]
    change_value = params[1]
    if "up" in hotkey:
        change_value = "+" + str(change_value)
        sbc.set_brightness(change_value)
    if "down" in hotkey:
        change_value = "-" + str(change_value)
        sbc.set_brightness(change_value)
    if "fade" in hotkey:
        change_value = int(change_value)
        sbc.fade_brightness(change_value, increment = 10)