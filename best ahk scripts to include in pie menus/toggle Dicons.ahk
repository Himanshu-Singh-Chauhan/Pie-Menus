#NoTrayIcon
#Persistent
#NoEnv
#SingleInstance, Force


#IfWinActive ahk_class Progman
Space::
ControlGetFocus, vCtlClassNN, A
ControlGet, vCtlStyle, Style,, % vCtlClassNN, A
if (SubStr(vCtlClassNN, 1, 4) = "Edit") && !(vCtlStyle = 0x54000080)
{
	Send {Space}
}
else{
	If (toggle := !toggle)
		Control, Hide,, SysListView321, ahk_class Progman
	else
		Control, Show,, SysListView321, ahk_class Progman
	return
}
