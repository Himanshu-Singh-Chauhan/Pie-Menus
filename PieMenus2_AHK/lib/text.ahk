#Include, Gdip_All.ahk
#Include, GdipHelper.ahk

SetUpGDIP()
StartDrawGDIP()
ClearDrawGDIP()
Gui, 1: -Caption +E0x80000 +LastFound +AlwaysOnTop +ToolWindow +OwnDialogs

; ; Show the window
Gui, 1: Show, NA
hwnd1 := WinExist()

; ; Create a gdi bitmap with width and height of what we are going to draw into it. This is the entire drawing area for everything
hbm := CreateDIBSection(Width, Height)

; ; Get a device context compatible with the screen
hdc := CreateCompatibleDC()

; ; Select the bitmap into the device context
obm := SelectObject(hdc, hbm)

; ; Get a pointer to the graphics of the bitmap, for use with drawing functions
G := Gdip_GraphicsFromHDC(hdc)
pBrush := Gdip_BrushCreateSolid(0xffff0000)
Gdip_FillEllipse(G, pBrush, 5, 5, 200, 300)
Gdip_FillEllipse(G, pBrush, 500, 50, 200, 300)
Gdip_DeleteBrush(pBrush)

OnMessage(0x200, "WM_LBUTTONDOWN")
EndDrawGDIP()
return

WM_LBUTTONDOWN()
{
	;PostMessage, 0xA1, 2
	MouseGetPos, , , id, control
	MsgBox, % id control
}