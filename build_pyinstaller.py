import os
import shutil
import PyInstaller.__main__
import pyinstaller_versionfile

script_dir = os.path.dirname(__file__)

version_file_name = "version.txt"

pyinstaller_versionfile.create_versionfile(
    output_file       = version_file_name,
    version           = "1.1.0.0",
    file_description  = "Pie Menus of any windows app",
    internal_name     = "Pie Menus",
    original_filename = "Pie Menus.exe",
    product_name      = "Pie Menus"
)


PyInstaller.__main__.run([
    f'-i "{os.path.join(script_dir, "resources/icons/tray_icon.ico")}"', # application icon
    '-n "Pie Menus"', # Name of the application
    '-w', # do not start cmd with application
    '--clean', # clean previous build and dist folders and temp files
    'main.py' # Main files to compile
    f'--version-file "{os.path.join(script_dir, version_file_name)}"'
])


# Manually copying files // not including in spec as I don't understand it.
resources   = os.path.join(script_dir, "resources/")
settings    = os.path.join(script_dir, "settings/")
dist_folder = os.path.join(script_dir, "dist/Pie Menus")
destination = shutil.copytree(resources, dist_folder) # copying
destination = shutil.copytree(settings, dist_folder)  # copying