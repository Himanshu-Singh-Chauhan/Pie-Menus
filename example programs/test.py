from time import sleep
from ahk import AHK, Hotkey
import ahk
from ahk.directives import NoTrayIcon

ahk = AHK(directives=[NoTrayIcon])
ahk_script = '''
RMBState := FileOpen("RMBState.txt", "w")
if !IsObject(RMBState)
{
    MsgBox Can't open "%FileName%" for writing.
    return
}
RMBState.Write("1")
RMBState.close()
Return'''

key_combo = 'RButton' # Define an AutoHotkey key combonation

script = '''data := 0
if getkeystate("RButton")
{
    data := 1
}
FileAppend, %data%, *'''

fileRead = '''
FileRead, settings, %A_ScriptDir%\RMBState.txt
FileAppend, %settings%, *'''

testEnv = '''EnvSet, EnvVar, Value'''
hotkey = Hotkey(ahk, key_combo, testEnv) # Create Hotkey
hotkey.start()  #  Start listening for hotkey
# print(hotkey.running)
sleep(5)
# result = ahk.run_script(script)
result = ahk.run_script(fileRead)
print(result)