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
    params = params[0]
    keyboard.send(params)


def runScript(params):
    pass


