from win32gui import GetWindowText, GetForegroundWindow,GetClassName 
import win32process
import psutil
#//import wmi
#c = wmi.WMI()
from time import sleep
sleep(2)
for i in range(19999999):
	sleep(1)
	print(GetClassName(GetForegroundWindow()))
	print(GetWindowText(GetForegroundWindow()))
	pid = win32process.GetWindowThreadProcessId(GetForegroundWindow())
	print("talent : ", psutil.Process(pid[-1]).name())
sleep(1000)
raw_input("sdfasdf")