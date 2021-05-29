import sys
import os
from cx_Freeze import executable, setup, Executable

# Add files
files = ['piemenu_backend.py', "fastIO.py", "keyboardhook.py", "mousehook.py", "pieFunctions.py", "systemTrayIcon.py", "resources/", "settings/"]

# Target
target = Executable(
    script = "main.py",
    base = "Win32GUI",
    icon = "resources/icons/tray_icon.png"
)

# Setup CX Freeze
setup(
    name = "Pie Menus",
    version = "1.0",
    description = "Pie menus for every app",
    author = "Himanshu Singh Chauhan",
    options = ( { 'build_exe' : { 'include_files' :  files} } ),
    executables = [target]

)