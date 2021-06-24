Filearray := []
Loop, Files, C:\Users\%A_UserName%\Pictures\*.png 
	Filearray.push(A_LoopFileLongPath)
total := Filearray.MaxIndex()

1::
    Random, number, 1, % total
	FileCopy, % Filearray[number], C:\Users\%A_UserName%\Pictures\Windows Terminal bg\Windows Terminal Background.png, 1
	FileCopy, C:\Users\S\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json, C:\Users\S\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json.bkp, 1
	FileDelete, C:\Users\S\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json
	sleep, 5000
	FileCopy, C:\Users\S\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json.bkp, C:\Users\S\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json, 1
return