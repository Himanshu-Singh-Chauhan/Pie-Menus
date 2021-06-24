#NoTrayIcon
#Persistent
#NoEnv
#SingleInstance, Force


#IfWinActive ahk_class CabinetWClass
Space::
ControlGetFocus, vCtlClassNN, A
ControlGet, vCtlStyle, Style,, % vCtlClassNN, A
if (SubStr(vCtlClassNN, 1, 4) = "Edit") && !(vCtlStyle = 0x54000080)
{
	Send {Space}
}
else{
Send !vn{enter}
}