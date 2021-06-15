runPieMenu(profileNum, index, markingMenu)
{
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

    loop
    {
        
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
}


