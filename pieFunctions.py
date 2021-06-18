from time import sleep
import keyboard
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

    for _ in range(int(repeat_count)):
        keyboard.send(hotkey)

def runScript(params):
    pass