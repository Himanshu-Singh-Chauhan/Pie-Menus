#Persistent
#Include %A_ScriptDir%\Environment.ahk 


RButton::
;msgbox data
RMBState := FileOpen("RMBState.txt", "w")
if !IsObject(RMBState)
{
    MsgBox Can't open "%FileName%" for writing.
    return
}
RMBState.Write("1")
RMBState.close()
Return

RButton Up::
;msgbox data
RMBState := FileOpen("RMBState.txt", "w")
if !IsObject(RMBState)
{
    MsgBox Can't open "%FileName%" for writing.
    return
}
RMBState.Write("0")
RMBState.close()
Return

h::
RMBState := FileOpen(RMBState.txt, "r")
FileRead, data, %A_ScriptDir%\RMBState.txt
msgbox %data%