#Persistent
#Include %A_ScriptDir%\Environment.ahk 


RButton::
msgbox data
Env_UserNew("NUMBER_OF_GPU_CORES", "9")
EnvSet, RightClickState, 1
Return

h::
EnvGet data, RightClickState
msgbox %data%