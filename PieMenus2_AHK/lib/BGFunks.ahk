getMonitorCoords(ByRef monLeft, ByRef monTop, ByRef monRight, ByRef monBottom)
{
    global monitorManager := New MonitorManager
    ; msgbox, % monitorManager.monitors[1].dpiX
    monLeft := 0
    monRight := 0
    monTop := 0
    monBottom := 0
    loop
    {
        Sysget, testMon, Monitor, 1
        if testMonLeft is number
            Break
        sleep, 100
    }	
    ;Get the number of monitors from the monitor manager.
    numMonitors := 0
    for monIndex in monitorManager.monitors
    {
        ;Count monitors
        if (IsObject(monitorManager.monitors[monIndex]))
            numMonitors := numMonitors+1
        ;Determine maximum area, only disregard scaling when true/pm is enabled in the compile.
        if (monLeft > monitorManager.monitors[monIndex].left)
            monLeft := monitorManager.monitors[monIndex].left
        if (monRight < monitorManager.monitors[monIndex].right)
            monRight := monitorManager.monitors[monIndex].right
        if (monTop > monitorManager.monitors[monIndex].top)
            monTop := monitorManager.monitors[monIndex].top
        if (monBottom < monitorManager.monitors[monIndex].bottom)
            monBottom := monitorManager.monitors[monIndex].bottom
        ; msgbox, %monIndex% "left:"%monLeft%" Top:"%monTop%" Right:"%monRight%" Bottom:"%monBottom%
    }
    return
}

; removeCharacters function removes special characters from the hotkey string.
removeCharacters(var, chars="!^+#") ; hotkey strings passed are stored in var.
{
    stringreplace,var,var,%A_space%,_,a ; This line replaces all spaces in hotkey with underscore '_'
	; The following loop removes the special chars which are in 'chars' variable from the hotkey by using stringreplace command.
    loop, parse, chars
    {
        stringreplace,var,var,%A_loopfield%,,a
    }
    return var
}

calcAngle(aX, aY, bX, bY)
{
    initVal := (dllcall("msvcrt\atan2","Double",(bY-aY), "Double",(bX-aX), "CDECL Double")*57.29578)
    If initVal < 0
        returnVal := (initVal+360)
    Else
        returnVal := initVal
    return returnVal
}

checkAHK()
{
    AHKVersion := StrReplace(A_AHKVersion, ".","")
    ; msgbox, % AHKVersion < 113202
    ; If ( A_IsCompiled AND A_AhkPath="" AND (AHKVersion < 113201)) 
    If (AHKVersion < 113200) 
    {
        MsgBox, 4, ,Autohotkey needs to be installed/updated to run the Pie Menu apps, Install Autohotkey?
        IfMsgBox, Yes
        {
            UrlDownloadToFile, https://autohotkey.com/download/ahk-install.exe
            , %A_Temp%\AutoHotkeyInstall.exe
            Run, %A_Temp%\AutoHotkeyInstall.exe
            exitapp
        }
        IfMsgBox, No
        {
            Msgbox, ...okay then. I'll just, chill in this corner. Don't mind me. Let me know if you ever want some pie or anything.
                exitapp
        }
        ExitApp
    }
}


; cycleRange function keeps any angle in a range of [0, 360), mind the brackets.....angle passed is in degrees.
cycleRange(var, range=360) ; angle is stored in var
{
    var := var - (range*Floor((var / range)))
    return var
}


pieTipText(text)
{
    global
    StartDrawGDIP()
    ClearDrawGDIP()	

    Gdip_SetSmoothingMode(G, 4)

    TXo := A_ScreenWidth / 2
    TYo := A_ScreenHeight - 100
    textoptions = x%TXo% y%TYo% Center Vcenter cffffffff r4 s16
    ToolTipText = %text%
    Gdip_TextToGraphics(G, ToolTipText, textoptions)
    EndDrawGDIP()
}


RGBAtoHEX(RGBA) ;Converts RGBA array to HEX ARGB
{
    rHex := Format("0x{4:02x}{1:02x}{2:02x}{3:02x}`r`n", RGBA*)
    return rHex
}


whitenRGB(RGBAarray)
{
    NewRGBA := [0, 0, 0, 255]
    loop 3
    {
        NewRGBA[A_Index] := RGBAarray[A_Index]+20		
    }
    ; msgbox, % RGBAarray[1] "," RGBAarray[2] "," RGBAarray[3]
    return NewRGBA
}


drawPieLabel(pGraphics, labelText, xPos, yPos, selected:=0, anchor:="top", activePieProfile=0, pieDPIScale=1, clicked:=false)
{
    p_FontSize := settings.global.fontSize
    xPosition := xPos
    yPosition := yPos
    pad := Ceil(6*(((pieDPIScale-1)/2)+1))
    fontSize := Ceil(p_FontSize*pieDPIScale)
    ; fontSize := 14
    If (selected == 1)
    {
        If (clicked = true)
        {
            strokeColor := RGBAtoHEX(activePieProfile.selColor)
            labelBGColor := RGBAtoHEX(activePieProfile.selColor)
            textColor := RGBAtoHEX(activePieProfile.bgColor)
        }
        else ;slice is focused
        {
            strokeColor := RGBAtoHEX(activePieProfile.selColor)
            ; labelBGColor := RGBAtoHEX(whitenRGB(activePieProfile.bgColor))
            labelBGColor := RGBAtoHEX([255, 255, 255, 255])
            textColor := "FFFFFFFF"
        }	
    }
    else
    {
        strokeColor := RGBAtoHEX([123, 123, 123, 255])
        labelBGColor := RGBAtoHEX(activePieProfile.bgColor)	
        textColor := "FFFFFFFF"	
        ; labelBGColor := RGBAtoHEX([30, 30, 30, 255])		
    }
    textYOffset := Ceil(1*pieDPIScale)
    displayText := labelText
    textOptionsTest := % "x" xPosition " y" yPosition " Center vCenter c00FFFFFF r4 s" fontSize
    Gdip_SetSmoothingMode(pGraphics, 4)
    basicPen := Gdip_CreatePen(strokeColor, 1)
    otherPen := Gdip_CreatePen("0xFFff0000" , 1)
    basicBrush := Gdip_BrushCreateSolid(labelBGColor)
    theRect := Gdip_TextToGraphics(pGraphics, displayText, textOptionsTest, "Arial")
    theRect := StrSplit(theRect, "|")
    theRect[3] := Max(Ceil(theRect[3]), 100*pieDPIScale)
    theRect[4] := Ceil(theRect[4])

    If (anchor == "bottom")
    {
        Gdip_FillRoundedRectangle(pGraphics, basicBrush, Ceil(xPosition-(theRect[3]/2)-pad), Ceil(yPosition-theRect[4]-(2*pad)), Ceil(theRect[3]+(2*pad)), Ceil(theRect[4]+(2*pad)), 3)
        Gdip_DrawRoundedRectangle(pGraphics, basicPen, Ceil(xPosition-(theRect[3]/2)-pad), Ceil(yPosition-theRect[4]-(2*pad)), Ceil(theRect[3]+(2*pad)), Ceil(theRect[4]+(2*pad)), 3)
        textOptions := % "x" xPosition " y" (yPosition-theRect[4]-pad+textYOffset) " Center vCenter c" textColor " r4 s" fontSize
        Gdip_TextToGraphics(pGraphics, displayText, textOptions, "Arial")
    }
    If (anchor == "top")
    {
        Gdip_FillRoundedRectangle(pGraphics, basicBrush, Ceil(xPosition-(theRect[3]/2)-pad), yPosition, Ceil(theRect[3]+(2*pad)), Ceil(theRect[4]+(2*pad)), 3)
        Gdip_DrawRoundedRectangle(pGraphics, basicPen, Ceil(xPosition-(theRect[3]/2)-pad), yPosition, Ceil(theRect[3]+(2*pad)), Ceil(theRect[4]+(2*pad)), 3)
        textOptions := % "x" xPosition " y" (yPosition+pad+textYOffset) " Center vCenter c" textColor " r4 s" fontSize
        Gdip_TextToGraphics(pGraphics, displayText, textOptions, "Arial")
    }
    If (anchor == "left")
    {
        Gdip_FillRoundedRectangle(pGraphics, basicBrush, xPosition, Ceil(yPosition-(theRect[4]/2)-pad), Ceil(theRect[3]+(2*pad)), Ceil(theRect[4]+(2*pad)), 3)
        Gdip_DrawRoundedRectangle(pGraphics, basicPen, xPosition, Ceil(yPosition-(theRect[4]/2)-pad), Ceil(theRect[3]+(2*pad)), Ceil(theRect[4]+(2*pad)), 3)
        textOptions := % "x" (xPosition+(theRect[3]/2)+pad) " y" (yPosition-(theRect[4]/2)+textYOffset) " Center vCenter c" textColor " r4 s" fontSize
        Gdip_TextToGraphics(pGraphics, displayText, textOptions, "Arial")
    }
    If (anchor == "right")
    {
        Gdip_FillRoundedRectangle(pGraphics, basicBrush, Ceil(xPosition-theRect[3]-(2*pad)), Ceil(yPosition-(theRect[4]/2)-pad), Ceil(theRect[3]+(2*pad)), Ceil(theRect[4]+(2*pad)), 3)
        Gdip_DrawRoundedRectangle(pGraphics, basicPen, Ceil(xPosition-theRect[3]-(2*pad)), Ceil(yPosition-(theRect[4]/2)-pad), Ceil(theRect[3]+(2*pad)), Ceil(theRect[4]+(2*pad)), 3)
        textOptions := % "x" (xPosition-(theRect[3]/2)-pad) " y" (yPosition-(theRect[4]/2)+textYOffset) " Center vCenter c" textColor " r4 s" fontSize
        Gdip_TextToGraphics(pGraphics, displayText, textOptions, "Arial")
    }
    ; Gdip_DrawEllipse(pGraphics, otherPen, xPosition, yPosition, 1, 1)
    return
}


drawPie(G, xPos, yPos, dist, theta, numSlices, radius, thickness, bgColor, selectColor, thetaOffset, activePieProfile, pieDPIScale=1, clicked:=false)
{	
    ;init local variables
    ; nTheta := (Floor(cycleRange(theta-thetaOffset)/(360/numSlices))*(360/numSlices))+thetaOffset ; for only focused arc
    nTheta := cycleRange(theta-thetaOffset) ; for smooth circling
    gmx := xPos
    gmy := yPos
    labelRadius := 100*pieDPIScale
    ClearDrawGDIP()
    Gdip_SetSmoothingMode(G, 4)
    basicPen := Gdip_CreatePen(RGBAtoHEX(bgColor), thickness)

	; The following line draws the outer circle of pie menu.
    Gdip_DrawEllipse(G, basicPen, (gmx-(radius / 2)), (gmy-(radius / 2)), radius, radius)

	; The following if-else determines wheather to draw or not the inner circle and the selection highlight circle
    If (dist <= ((radius/2)+(thickness/2)))	
    {
        selectPen := Gdip_CreatePen(RGBAtoHEX(selectColor), thickness/2)
		; the following draws inner circle
        Gdip_DrawEllipse(G, selectPen, (gmx-(radius / 2)+(thickness/4)), (gmy-(radius / 2)+(thickness/4)), radius-(thickness/2), radius-(thickness/2))
        pieRegion := 0
    }
    Else
    {
        selectPen := Gdip_CreatePen(RGBAtoHEX(selectColor), thickness)
		; the following draws selection highlight circle
        Gdip_DrawArc(G, selectPen, (gmx-(radius/2)), (gmy-(radius/2)), radius, radius, (nTheta)-90, (360/numSlices))	
        pieRegion := Floor(cycleRange(theta-thetaOffset)/(360/numSlices))+1	

        ; If (pieRegion == (numSlices + 1))
        ; 	pieRegion := 1
    }

  

    ;Draw pie labels
    loop, %numSlices%
    {
        if (activePieProfile.functions[A_Index+1].label = "")
            activePieProfile.functions[A_Index+1].label := "Empty"
            ; MsgBox % A_Index   activePieProfile.functions[A_Index].label     A_Index activePieProfile.functions[A_Index+1].label
            ; continue
        labelTheta := (((A_Index-1)*(360/numSlices))+(180/numSlices+thetaOffset))
        if labelTheta between 0.1 and 179.9
            labelAnchor := "left"
        else if labelTheta between 180.1 and 359.9
            labelAnchor := "right"
        else If (labelTheta == Mod(labelTheta,360))
            labelAnchor := "top"
        else
            labelAnchor := "bottom"

        If (pieRegion = A_Index)
            selectedLabelState := 1
        Else
            selectedLabelState := 0

        drawPieLabel(G, activePieProfile.functions[A_Index+1].label, Round(gmx+(labelRadius*Cos((labelTheta-90)*0.01745329252))), Round(gmy+(labelRadius*Sin((labelTheta-90)*0.01745329252))), selectedLabelState, labelAnchor, activePieProfile, pieDPIScale, clicked)
    }

    EndDrawGDIP()
    return pieRegion
}


createTriggerKeys(activePieProfile)
{
    TriggerKeys := {}
    Loop, % activePieProfile.numSlices
    {
        if (activePieProfile.functions[A_Index].triggerKey != "None")
        {
            TriggerKeys[activePieProfile.functions[A_Index].triggerKey] := activePieProfile.functions[A_Index].PieNumber
        }
    }

    ; for key, value in TriggerKeys
	;     msgbox %key% = %value%
    Return TriggerKeys

}


registerTriggerKeys(TriggerKeys)
{
    global registeredTriggerKeys := {}
    for triggerKey in TriggerKeys
    {
        if (InStr("""~!@#$%^&*()_+{}|:<>?""", triggerKey))
        {
            ; pass
            ; these trigger keys are not allowed for now.
            MsgBox, These special keys are naut allowed faur now. Program wont behave normally.
        }
        else if (InStr("""`-=[];',./\""", triggerKey))
        {
            if (triggerKey == "`")
            {
                registeredTriggerKeys["Trigger_backTick"] := True
            }
            else if (triggerKey == "-")
            {
                registeredTriggerKeys["Trigger_minus"] := True
            }
            else if (triggerKey == "=")
            {
                registeredTriggerKeys["Trigger_equals"] := True
            }
            else if (triggerKey == "[")
            {
                registeredTriggerKeys["Trigger_sqaureOpen"] := True
            }
            else if (triggerKey == "]")
            {
                registeredTriggerKeys["Trigger_sqaureClose"] := True
            }
            else if (triggerKey == ";")
            {
                registeredTriggerKeys["Trigger_semiColon"] := True
            }
            else if (triggerKey == "'")
            {
                registeredTriggerKeys["Trigger_singleQoute"] := True
            }
            else if (triggerKey == ",")
            {
                registeredTriggerKeys["Trigger_coma"] := True
            }
            else if (triggerKey == ".")
            {
                registeredTriggerKeys["Trigger_fullStop"] := True
            }
            else if (triggerKey == "/")
            {
                registeredTriggerKeys["Trigger_forwardSlash"] := True
            }
            else if (triggerKey == "\")
            {
                registeredTriggerKeys["Trigger_backwardSlash"] := True
            }
        }
        Else
        {
            keyToRegister := "Trigger_" + triggerKey
            registeredTriggerKeys[keyToRegister] := True
        }
    }
}


deregisterTriggerKeys()
{
    global registeredTriggerKeys := {}
}



global depthOfPieMenu := 1
global bkpRunningProfile := []

runPieMenu(profileNum, index, markingMenu)
{
    ;REFACTOR - Declare variables better
    global		
    ; initial x and y position of mouse, where pie was launched.
    MouseGetPos, iMouseX, iMouseY

    ; Get the dpi for the monitor in which mouse is in.
    if (substr(a_osversion, 1, 2) = "10") ; Check if its windows 10 or not.
    {	
        ;detemine what monitor the mouse is in and scale factor
        pieDPIScale := 1
        for monIndex in monitorManager.monitors
        {
            if (iMouseX >= monitorManager.monitors[monIndex].left and iMouseX <= monitorManager.monitors[monIndex].right)
            {
                ; msgbox, % iMouseX " is apparently between " monitorManager.monitors[monIndex].left " and " monitorManager.monitors[monIndex].right
                if (iMouseY >= monitorManager.monitors[monIndex].top and iMouseY <= monitorManager.monitors[monIndex].bottom)
                {
                    pieDPIScale := monitorManager.monitors[monIndex].scaleX					
                    break			
                }
            }
        }
    }
    else
    {
        ;Win7 DPI Scaling (takes value of primary monitor)
        pieDPIScale := A_ScreenDPI / 96
    }
    ; msgbox, % iMouseX " and " iMouseY " pieDPI=" pieDPIScale

    bitmapPadding := [300*pieDPIScale,180*pieDPIScale]
    SetUpGDIP(iMouseX-bitmapPadding[1], iMouseY-bitmapPadding[2], 2*bitmapPadding[1], 2*bitmapPadding[2])
    StartDrawGDIP()

    arm2 := false	
    arm3 := false
    armPie3 := false
    armPie2 := false
    LButtonPressed := false
    RMBPressed := false
    LButtonPressed_LastState := false
    RMBPressed_LastState := false
    LButtonPressed_static := false
    RMBPressed_static := false
    thetaOffset := 0
    activePieNumber := 1 ; There are maximum of three pies under a hotkey, and the first one launch is the first pie.
    if (markingMenu.isThisMarkingMenu == true)
    {
        ; MsgBox, yoyo
        runningProfile := markingMenus.markingMenus[profileNum].pieMenus[index]
    }
    else
    {
        runningProfile := settings.appProfiles[profileNum].pieMenus[index]
    }
    offsetPie := [runningProfile.activePie[1].offset*(180/runningProfile.activePie[1].numSlices), runningProfile.activePie[2].offset*(180/runningProfile.activePie[2].numSlices), runningProfile.activePie[3].offset*(180/runningProfile.activePie[3].numSlices)]
    pieMode := 0 ;what is one this used for?
    pieRegion := 0 
    ranByClick := false
    ranByTrigger := false
    ranMarkingMenu := false
    continueLastPieMenu := false
    RMBCancel := false
    LastActivePieNumber := 0
    forceUpdateGraphics := false
    pieHotkey := removeCharacters(runningProfile.hotkey, "!^+#")
    ; Trigger Keys are also being created here outside the loop to make the pie menus more fast, so that if triggerKey is pressed right after, it doesn't calculate 
    ; the below stuff and break ASAP.
    TriggerKeys := createTriggerKeys(runningProfile.activePie[activePieNumber]) 
    registerTriggerKeys(TriggerKeys)


    ; The following function call, draws all the graphics, if its commented out, pie menus will still work, just you won't be able to see the graphics until you move
	; the mouse, if you move the mouse graphics will update from the loop below.
    drawPie(G, bitmapPadding[1], bitmapPadding[2], 0, 0, runningProfile.activePie[activePieNumber].numSlices, runningProfile.radius*pieDPIScale, runningProfile.thickness*pieDPIScale, runningProfile.activePie[1].bgColor, runningProfile.activePie[1].selColor, offsetPie[1], runningProfile.activePie[activePieNumber], pieDPIScale)

    ; ####################################################Trigger Keys########################################################################
    if (runningProfile.activePie[activePieNumber].triggerKeysActive)
        {
            ; this else condition will improve performace in some cases, when triggerKeysActive is true but none of them is set, can happen in manual mode.
            ; this one CPU cycle can be saved if this is taken care of in the settings generation itself.
            if TriggerKeys.Length() == 0
            {
                runningProfile.activePie[activePieNumber].triggerKeysActive := false
                deregisterTriggerKeys()
            }
            else
            {
                ; triggerKey and triggerKeys are different, pay attention
                for triggerKey, TriggerPieRegion in TriggerKeys
                {
                    if GetKeyState(triggerKey, "P")
                    {
                        if (triggerKey == pieHotkey)
                        {
                            ; pass
                        }
                        else
                        {
                            ; MsgBox, uo
                            pieRegion := TriggerPieRegion - 1 
                            ; I subtracted one from TriggerPieRegion, because the 2very first one is in center
                            runPieFunction([profileNum,index,activePieNumber,pieRegion, iMouseX, iMouseY, markingMenu])
                            ranByTrigger := true
                        }
                    }
                }
            }  ; End of triggerKey logic

        }
    ; #######################################################################################################################################


    ; the following five lines are select graphics logic for quick gesture selection.
    ; I kept this here just after first time pie menu is drawn, to quickly update the graphics ASAP on mouse gesture
    Sleep, 5   ; this single line fixes third issue and first issue in update log oct 6
    MouseGetPos, mouseXGesture, mouseYGesture
    dist := (Sqrt((Abs(mouseXGesture-iMouseX)**2) + (Abs(mouseYGesture-iMouseY)**2)))
    if dist != 0  ; do not calculate if mouse has not been moved, that is dist is 0.
    {
        theta := cycleRange(calcAngle(iMouseX, iMouseY, mouseXGesture, mouseYGesture)+90)
        StartDrawGDIP()
        drawPie(G, bitmapPadding[1], bitmapPadding[2], dist, theta, runningProfile.activePie[activePieNumber].numSlices, runningProfile.radius*pieDPIScale, runningProfile.thickness*pieDPIScale, runningProfile.activePie[1].bgColor, runningProfile.activePie[1].selColor, offsetPie[1], runningProfile.activePie[activePieNumber], pieDPIScale)
    }




    fPieRegion := 0

    f_FunctionLaunchMode := settings.global.functionLaunchMode
    ; msgbox, % runningProfile.hotkey " changed to " pieHotkey    
    

    ; the following 4 lines of code is logic for single keypress hold piemenu.
    sleep 120
    if (!getkeystate(pieHotkey, "P") )&& (dist == 0){
        runningProfile.holdOpenOverride := true
        ; MsgBox talent
    }

    ; The 7 line (CancelBoolean) determines wheather hotkey is RMB and is held down, or pie menu is open and holded and pressing RMB should cancel it or not.
    ; if hotkey is RMB and pie menu is opened by holding RMB then the code is taking RMB as to cancel menu and functions are not running, that is why following CancelBoolean is important.
    CancelBoolean := false
    if (pieHotkey == "RButton") && !getkeystate("RButton"){
        CancelBoolean := true
    }
    if (pieHotkey != "RButton"){
        CancelBoolean := true
    }3


    loop
    {
        continueLastPieMenu := false
        ; ########################################Trigger Keys######################################################

        if ranByTrigger
        {
            break ; this condition will be true if trigger is detected above, outside loop
        }

        if (runningProfile.activePie[activePieNumber].triggerKeysActive)
        {
            ; A_Index != 1 because trigger keys are already loaded for first pie about outside the loop, dont wanna do that again.
            if (A_Index != 1 && (LastActivePieNumber != activePieNumber))
            {
                ; TriggerKeys := "" ; Releases the last reference, and therefore frees the object.
                ; TriggerKeys := createTriggerKeys(runningProfile.activePie[activePieNumber])
                ; I did not call the createTriggerKeys(), because maybe inline code is much faster, cosnidering this is also in a loop.
                TriggerKeys := {}
                Loop, % runningProfile.activePie[activePieNumber].numSlices
                {
                    if (runningProfile.activePie[activePieNumber].functions[A_Index].triggerKey != "None")
                    {
                        TriggerKeys[runningProfile.activePie[activePieNumber].functions[A_Index].triggerKey] := runningProfile.activePie[activePieNumber].functions[A_Index].PieNumber
                    }
                }

                registerTriggerKeys(TriggerKeys)

            }
            Else
            {
                ; this else condition will improve performace in some cases, when triggerKeysActive is true but none of them is set, can happen in manual mode.
                ; this one CPU cycle can be saved if this is taken care of in the settings generation itself.
                if TriggerKeys.Length() == 0
                {
                    runningProfile.activePie[activePieNumber].triggerKeysActive := false
                    deregisterTriggerKeys()
                }
            }



            ; triggerKey and triggerKeys are different, pay attention
            for triggerKey, TriggerPieRegion in TriggerKeys
            {
                if GetKeyState(triggerKey, "P")
                {
                    if (triggerKey == pieHotkey) && (runningProfile.holdOpenOverride == false)
                    {
                        Continue
                    }
                    pieRegion := TriggerPieRegion -1 
                    ; I subtracted one from TriggerPieRegion, because the very first one is in center
                    runPieFunction([profileNum,index,activePieNumber,pieRegion, iMouseX, iMouseY, markingMenu])
                    ranByTrigger := true
                    break 2 ; 2 to break outerloop.
                }
            }
            LastActivePieNumber := activePieNumber
        }  ; End of triggerKey logic


        ; #############################################End of Trigger Keys###########################################################




        if (LButtonPressed = false)
        {
            if (A_Index != 1) && (pieRegion != 0) ;Midpoint stuff
            {
                midMouseX := mouseX
                midMouseY := mouseY
                MouseGetPos, mouseX, mouseY		
                midMouseX := ( ( mouseX + midMouseX ) / 2)
                midMouseY := ( ( mouseY + midMouseY ) / 2)
                midDist := (Sqrt((Abs(midMouseX-iMouseX)**2) + (Abs(midMouseY-iMouseY)**2)))
            }
            else
            {
                MouseGetPos, mouseX, mouseY
                midDist := 99999
            }
        }
        ;Calculate Distance and Angle
        dist := (Sqrt((Abs(mouseX-iMouseX)**2) + (Abs(mouseY-iMouseY)**2)))
        theta := cycleRange(calcAngle(iMouseX, iMouseY, mouseX, mouseY)+90)
        ;if inside circle
        If (dist <= (((runningProfile.radius / 2) + (runningProfile.thickness / 2) ) * pieDPIScale) or midDist <= (( (runningProfile.radius / 2) + (runningProfile.thickness / 2)) * pieDPIScale))
        {
            pieRegion := 0
        }
        Else		
        {		
            pieRegion := Floor(cycleRange(theta-offsetPie[activePieNumber])/(360/runningProfile.activePie[activePieNumber].numSlices))+1	
            ; MsgBox % theta "  "offsetPie[activePieNumber] "  " pieRegion
            If (pieRegion == (runningProfile.activePie[activePieNumber].numSlices + 1))
                pieRegion := 1
        }

		
        if (armPie3 != true) && (pieRegion > 0) ; If out of middle and pie 1 or 2
        {
            ;Refactor Me!!

            ;  If a variable is not declared anywehere before then it is empty and any variable calculated using that variable is also empty.
            atheta := (leftTheta - theta - 180)
            deltaTheta := atheta - (Floor(atheta / 360) * 360)
            if deltaTheta between 0 and 90
            {
                if (arm3 == true)
                    armPie3 := true
                arm2 := true
                ; thetaQuad := 3
            }				
            else if deltaTheta between 270 and 360
            {
                if (arm2 == true)
                    armPie3 := true
                arm3 := true
            }				
            else
            {				
                arm2 := false
                arm3 := false
                ; thetaQuad := 1
            }		
        }

        ;If LButton down - Change State and launch function maybe consider getting this out of the loop
        If (f_FunctionLaunchMode < 2) && (GetKeyState("LButton","P"))
        {
            LButtonPressed := true
            LButtonPressed_static := true
        }
        else
            LButtonPressed := false

        ;If RButton down - Change State and launch function maybe consider getting this out of the loop
        ; MsgBox % getkeystate("RButton", "P")
        If (f_FunctionLaunchMode < 2) && (GetKeyState("RButton","P")) && CancelBoolean
        {
            RMBPressed := true
            RMBPressed_static := true
        }
        else
            RMBPressed := false



        ; If (pieRegion != fPieRegion) ;If region changes
        ; add "or dist != 0" in below 'if' to smooth circling but then, 'if' condition will always run no matter what, wasting CPU cycles.
        If (pieRegion != fPieRegion) or (LButtonPressed_LastState != LButtonPressed) or dist != 0 or forceUpdateGraphics ;If region changes or mouseclick changes
        {
            ;;If you leave the center
            If (pieRegion > 0) && (fPieRegion == 0)
            {
                if (runningProfile.activePie[2].enable)
                    armPie2 := true
                leftTheta := theta
            }

            ;Check armed pie when return to circle
            if (fPieRegion > 0) && (pieRegion == 0)
            {
                if (armPie3 == true) && (runningProfile.activePie[3].enable)
                {
                    activePieNumber := 3
                }
                else if (armPie2 == true) && (runningProfile.activePie[2].enable)
                {
                    activePieNumber := 2
                }
            }
			
            StartDrawGDIP()
            ; The following line keeps updating the graphics.
            fPieRegion := drawPie(G, bitmapPadding[1], bitmapPadding[2], dist, theta, runningProfile.activePie[activePieNumber].numSlices, runningProfile.radius*pieDPIScale, runningProfile.thickness*pieDPIScale, runningProfile.activePie[activePieNumber].bgColor, runningProfile.activePie[activePieNumber].selColor, offsetPie[activePieNumber], runningProfile.activePie[activePieNumber], pieDPIScale, LButtonPressed)

            ; msgBox, % continueLastPieMenu
            if (LButtonPressed_LastState == true) && (LButtonPressed == false)
				{
                    if (runningProfile.activePie[activePieNumber].functions[pieRegion+1].function == "runMarkingMenu")
                    {
                        bkpRunningProfile.push(runningProfile)
                        depthOfPieMenu := depthOfPieMenu + 1
                        continueLastPieMenu := runPieFunction([profileNum,index,activePieNumber,pieRegion, iMouseX, iMouseY, markingMenu])
                        depthOfPieMenu := depthOfPieMenu -1

                        ; this to restore LButtonPressed_LastState, after recursion call variables are messed, AHK has no recursion.
                        LButtonPressed_LastState := LButtonPressed := false
                        ranByClick := false
                        runningProfile := bkpRunningProfile.pop()
                        forceUpdateGraphics := true
                    }
                    Else{
                        continueLastPieMenu := runPieFunction([profileNum,index,activePieNumber,pieRegion, iMouseX, iMouseY, markingMenu])
                        if (continueLastPieMenu.continueLastPieMenu == true)
                        {
                            return continueLastPieMenu
                        }
                    }

                    if (continueLastPieMenu.continueLastPieMenu == true)
                    {
                        if (runningProfile.restoreOriginalPosition == true)
                        {
                            restoreOriginalPosition := true
                        }
                        else if (runningProfile.restoreOriginalPosition == "useGlobal" && settings.global.restoreOriginalPosition == true)
                        {
                            restoreOriginalPosition := true
                        }

                        if (restoreOriginalPosition == true)
                        {
                            MouseMove, continueLastPieMenu.iMouseX, continueLastPieMenu.iMouseY, 0
                            iMouseX := continueLastPieMenu.iMouseX 
                            iMouseY := continueLastPieMenu.iMouseY
                            SetUpGDIP(iMouseX-bitmapPadding[1], iMouseY-bitmapPadding[2], 2*bitmapPadding[1], 2*bitmapPadding[2])
                        }

                        restoreOriginalPosition := false
                        
                        continue
                    }
                    ; LButtonPressed_LastState := LButtonPressed
                    ; I had to set the following variable true because for some reason after breaking, else condition is running below, which is causing pieFunction to run twice.
                    ranByClick := true
                    ; MsgBox % LButtonPressed_LastState " " ranByClick
                    if !GetKeyState(pieHotkey, "P")
                    {
                        break
                    }
                }
      

                
            LButtonPressed_LastState := LButtonPressed
            forceupdateGraphics := false


        }


        

        ; sleep, 10	

        ; The below code is here for a reason, i forgot why, before it was at the starting of the loop, which might seem tempting for performance, but be carefull, it might break something.
        ; !ranByClick, because if user has launched a pie by click then releasing the hotkey should launch some pie based on mouse position
        if ( (!ranByClick) && ( !GetKeyState(pieHotkey, "P") && (runningProfile.holdOpenOverride == false)) )
            {
                runPieFunction([profileNum,index,activePieNumber,pieRegion,iMouseX,iMouseY,markingMenu])
                break
            }
        else if (( !GetKeyState(pieHotkey, "P") && (runningProfile.holdOpenOverride == false)))
            {
                break
            }

        

        if (RMBPressed_LastState == true) && (RMBPressed == false)
				{
                    RMBCancel := true
                    break
                }

        RMBPressed_LastState := RMBPressed

       
    } ;end pie loop
    
 

    StartDrawGDIP()
    ClearDrawGDIP()
    EndDrawGDIP()
    if (RMBCancel && runningProfile.holdOpenOverride == false)
    {   
        ; This following keywait command is to make sure that pie menus dont open again instantly right after user cancels pie menus using RMB which were open by holding hotkey.
        ; after user cancel, sometimes user may not let go hotkey, so it should not instantly trigger the pie menu again, user have to press again.
        KeyWait % pieHotkey
        deregisterTriggerKeys()
        return false
        ; i can also use the following, but I think it will use more CPU cycles, and using keywait is cleaner way.
        ; Loop
        ; {
        ;     if !GetKeyState(pieHotkey, "P")
        ;         return false
        ; }
    }
    else if ((ranByClick) || (RMBCancel) || (ranByTrigger) || (ranMarkingMenu))
    {
        KeyWait % pieHotkey
        ; the above keywait will prevent rapid repeatation of a pie command, when a user is held down both the trigger key first and pie hot key after.
        runningProfile.holdOpenOverride := false
        deregisterTriggerKeys()
        return false
    }
    else
    {
        if (f_FunctionLaunchMode != 1)
        {
            runningProfile.holdOpenOverride := false
            deregisterTriggerKeys()
            return
        }
    }
}



Class pieModifier
{
    modToggle(){		
        If (!WinActive("ahk_group regApps"))
        {
            Hotkey, IfWinNotActive, ahk_group regApps
                for menus in settings.appProfiles[1].pieMenus
                Hotkey, % settings.appProfiles[1].pieMenus[menus].hotkey, Toggle
            return
        }
        Else
        {
            global activeProfile := getActiveProfile()
            Hotkey, IfWinActive, % activeProfile[1]
                for menus in settings.appProfiles[activeProfile[2]].pieMenus
                Hotkey, % settings.appProfiles[activeProfile[2]].pieMenus[menus].hotkey, Toggle
            return
        }
    }
    modOn(){
        If (!WinActive("ahk_group regApps"))
        {
            Hotkey, IfWinNotActive, ahk_group regApps
                for menus in settings.appProfiles[1].pieMenus
                Hotkey, % settings.appProfiles[1].pieMenus[menus].hotkey, On
            return
        }
        Else
        {
            global activeProfile := getActiveProfile()
            Hotkey, IfWinActive, % activeProfile[1]
                ; msgbox,  % activeProfile[1]
            for menus in settings.appProfiles[activeProfile[2]].pieMenus
                Hotkey, % settings.appProfiles[activeProfile[2]].pieMenus[menus].hotkey, On
            return
        }
    }
    modOff(){
        If (!WinActive("ahk_group regApps"))
        {
            Hotkey, IfWinNotActive, ahk_group regApps
                for menus in settings.appProfiles[1].pieMenus
            {
                If (settings.appProfiles[1].pieMenus[menus].hotkey != activePieKey)
                    Hotkey, % settings.appProfiles[1].pieMenus[menus].hotkey, Off
            }				
            return
        }
        Else
        {
            ; global activveProfile := getActiveProfile()
            Hotkey, IfWinActive, % activeProfile[1]
                for menus in settings.appProfiles[activeProfile[2]].pieMenus
            {
                If (settings.appProfiles[activeProfile[2]].pieMenus[menus].hotkey != activePieKey)
                    Hotkey, % settings.appProfiles[activeProfile[2]].pieMenus[menus].hotkey, Off
            }				
            return			
        }
    }	
}


runPieFunction(funcNum)
{
    if(funcNum = false)
        {
            ; MsgBox, returnfalse
            return  
        }
    ; MsgBox, ran
    static lastPieFunctionRanTickCount := 0
    static lastPieFunctionRan = ""
    if (funcNum[7].isThisMarkingMenu == true)
    {
        selectedRegion := markingMenus.markingMenus[funcNum[1]].pieMenus[funcNum[2]].activePie[funcNum[3]].functions[funcNum[4]+1]	
    }
    Else
    {
        selectedRegion := settings.appProfiles[funcNum[1]].pieMenus[funcNum[2]].activePie[funcNum[3]].functions[funcNum[4]+1]	
    }

    ; if selectedRegion.returnMousePos = 1
    ; 	{
    ; 	BlockInput, Mouse
    ; 	MouseMove, funcNum[5], funcNum[6], 0		
    ; 	}
    if (selectedRegion.function = "repeatLastFunction")
    {
        ;Determine timeOut 0 := Infinite or >0 := value
        repeatTimeOut := 0	
        If (selectedRegion.params[1] > 0)
        {
            if ((lastPieFunctionRanTickCount + (selectedRegion.params[1]*1000)) > A_TickCount)
                repeatTimeOut := 1		
        }
        else
            repeatTimeOut := 1

        if (lastPieFunctionRan != "") && repeatTimeOut
            selectedRegion := lastPieFunctionRan
        else
            return
    }
    else
    {
        lastPieFunctionRan := selectedRegion	
    }

    if (selectedRegion.function = "resizeWindow") {
        resizeWindow(funcNum[5],funcNum[6])
        return
    }

    if (selectedRegion.function = "moveWindow") {
        moveWindow(funcNum[5],funcNum[6])
        return
    }
    
    ; MsgBox, % selectedRegion.params[1]

    if (selectedRegion.function == "runMarkingMenu") {
        continueLastPieMenu := pie_runMarkingMenu(funcNum, selectedRegion.params)
        Return continueLastPieMenu
    }

    if (selectedRegion.function == "continueLastPieMenu") {
        continueLastPieMenu := pie_continueLastPieMenu()
        Return continueLastPieMenu
    }



    pieFuncToRun := "pie_" . selectedRegion.function	
    pieFuncParamsArray := selectedRegion.params
    %pieFuncToRun%(pieFuncParamsArray)

    lastPieFunctionRanTickCount := A_TickCount

    ; if selectedRegion.returnMousePos = 1
    ; 	BlockInput, Off
}

getActiveProfile()
{
    If (!WinActive("ahk_group regApps"))
    {
        return ["ahk_group regApps", 1]
    }	
    WinGet, activeWinProc, ProcessName, A
    WinGetClass, activeWinClass, A
    for profiles in settings.appProfiles
    {
        testAHKHandle := StrSplit(settings.appProfiles[profiles].ahkHandle, " ", ,2)[2]
        if (testAHKHandle == activeWinProc) || (testAHKHandle == activeWinClass)
        {
            return [settings.appProfiles[profiles].ahkHandle, profiles]
        }
    }	
}

hasValue(var, arr) {
    arrOfKeys := []
    for key, value in arr
        if (value == var)
        arrOfKeys.Push(key)
    return (arrOfKeys.Length() = 0) ? false : arrOfKeys
}

blockBareKeys(hotkeyInput, hotkeyArray, blockState=1){
    ; for key in hotkeyArray
    ; 	msgbox, % hotkeyArray[key]	
    ; if (hotkeyInput == "")
    ; 	return
    if hotkeyArray[1] = ""
        return
    bareKey := removeCharacters(hotkeyInput, "!^+#")

    If (hasValue(bareKey, hotkeyArray) && hasValue("+" + bareKey, hotkeyArray)){
        ; msgbox, both
        return
    }
    If (bareKey == hotkeyInput)
        return
    If (blockState == 1) ; fix this
    {
        ; If !(hasValue(bareKey, hotkeyArray))		
        Try	Hotkey, % bareKey, pieLabel
        Try Hotkey, % "+" + bareKey, pieLabel							
        Try	Hotkey, % bareKey, On
        Try Hotkey, % "+" + bareKey, On
    }
    Else
    {			
        If !(hasValue(bareKey, hotkeyArray)){
            Try Hotkey, % bareKey, Off
            ; msgbox, % hasValue(bareKey, hotkeyArray)
        }
        If !(hasValue("+" + bareKey, hotkeyArray)){
            Try Hotkey, % "+" + bareKey, Off
        }		
        ; msgbox, % bareKey
    }
    return
}

class MonitorManager {
    __New() {
        ;; enum _PROCESS_DPI_AWARENESS    
        PROCESS_DPI_UNAWARE := 0
        PROCESS_SYSTEM_DPI_AWARE := 1
        PROCESS_PER_MONITOR_DPI_AWARE := 2
        ; DllCall("SHcore\SetProcessDpiAwareness", "UInt", PROCESS_PER_MONITOR_DPI_AWARE)
        ;; InnI: Get per-monitor DPI scaling factor (https://www.autoitscript.com/forum/topic/189341-get-per-monitor-dpi-scaling-factor/?tab=comments#comment-1359832)
        DPI_AWARENESS_CONTEXT_UNAWARE := -1
        DPI_AWARENESS_CONTEXT_SYSTEM_AWARE := -2
        DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE := -3
        DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 := -4
        DllCall("User32\SetProcessDpiAwarenessContext", "UInt" , DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE)
        ;; pneumatic: -DPIScale not working properly (https://www.autohotkey.com/boards/viewtopic.php?p=241869&sid=abb2db983d2b3966bc040c3614c0971e#p241869)

        ptr := A_PtrSize ? "Ptr" : "UInt"
        this.monitors := []
        DllCall("EnumDisplayMonitors", ptr, 0, ptr, 0, ptr, RegisterCallback("MonitorEnumProc", "", 4, &this), "UInt", 0)
        ;; Solar: SysGet incorrectly identifies monitors (https://autohotkey.com/board/topic/66536-sysget-incorrectly-identifies-monitors/)
    }
}

MonitorEnumProc(hMonitor, hdcMonitor, lprcMonitor, dwData) {
    l := NumGet(lprcMonitor + 0, 0, "Int")
    t := NumGet(lprcMonitor + 0, 4, "Int")
    r := NumGet(lprcMonitor + 0, 8, "Int")
    b := NumGet(lprcMonitor + 0, 12, "Int")

    this := Object(A_EventInfo)
    ;; Helgef: Allow RegisterCallback with BoundFunc objects (https://www.autohotkey.com/boards/viewtopic.php?p=235243#p235243)
    this.monitors.push(New Monitor(hMonitor, l, t, r, b))

    Return, 1
}

class Monitor {
    __New(handle, left, top, right, bottom) {
        ;When compiled with true/pm these values are based on real pixel coordinates without scaling.
        this.handle := handle
        this.left := left
        this.top := top
        this.right := right
        this.bottom := bottom

        this.x := left
        this.y := top
        this.width := right - left
        this.height := bottom - top

        dpi := this.getDpiForMonitor()
        this.dpiX := dpi.x	
        this.dpiY := dpi.y
        this.scaleX := this.dpiX / 96
        this.scaleY := this.dpiY / 96
    }

    getDpiForMonitor() {
        ;; enum _MONITOR_DPI_TYPE
        MDT_EFFECTIVE_DPI := 0
        MDT_ANGULAR_DPI := 1
        MDT_RAW_DPI := 2
        MDT_DEFAULT := MDT_EFFECTIVE_DPI
        ptr := A_PtrSize ? "Ptr" : "UInt"
        dpiX := dpiY := 0
        DllCall("SHcore\GetDpiForMonitor", ptr, this.handle, "Int", MDT_DEFAULT, "UInt*", dpiX, "UInt*", dpiY)

        Return, {x: dpiX, y: dpiY}
    }
    ;; InnI: Get per-monitor DPI scaling factor (https://www.autoitscript.com/forum/topic/189341-get-per-monitor-dpi-scaling-factor/?tab=comments#comment-1359832)

}

resizeWindow(xPos,yPos){
    WinGetPos, winX, winY, width, height, A
    if (xPos < winX){ ;to left of origin
        if (yPos > winY){ ;below origin
            WinMove, A,,xPos,, width+(winX-xPos), (yPos-winY)
        }else{ ;above origin
            WinMove, A,, xPos, yPos, width+(winX-xPos), height+(winY-yPos)		
        }	
    }else{ ;right of origin
        if (yPos > winY){ ;mouse below origin
            WinMove, A,,,, (xPos-winX), (yPos-winY)
        } else { ;mouse above origin
            WinMove, A,,,yPos, (xPos-winX), height+(winY-yPos)
        }	
    }	
    Return
}

moveWindow(xPos,yPos){
    WinGetPos, winX, winY, width, height, A
    WinMove, A, , xPos-(width/2), yPos-(width/3)
}

logTime(start=True){
    static timeArray := []
    if (start == True){
    }
} 