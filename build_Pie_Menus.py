import os
import shutil
import PyInstaller.__main__
import pyinstaller_versionfile

script_dir = os.path.dirname(__file__)

"""
Build, Dists and Spec files will generated where cmd running this python script is pointing,
so better make sure it is in right directory first.
"""
USE_UPX = True
DELETE_QT_PyInstaller_file = True

version_file_name = "version.txt"
upx_version = "3.96-win64"
upx_excludes = [
    # https://stackoverflow.com/questions/38811966/error-when-creating-executable-file-with-pyinstaller
    # qwindows.dll file is under -> dist\PySide2\plugins\platforms
    # if again pie menus gives error like "The application failed to start because no Qt platform plugin could be initialized.
    #                                      Reinstalling the application may fix this problem." and it is most probably because 
    # of upx compression, and we have to exclude that files which after upx_compression are causing this problem.
    # So if you want to cover all grounds, better exclude all files under dist\PySide2\plugins\platforms.
    # As of now, I don't want to cover all ground, as everything is working fine and I want size 
    # of the app to less. so yeah, I am not excluding them, and let them compress.
    "qwindows.dll"
]
# sometime latest version 3.96 does not works for some reason 
# use previous version then, v3.95-win64
# https://stackoverflow.com/questions/63134762/winerror-5-access-is-denied-when-trying-to-include-upx-dir-in-pyinstaller

pyinstaller_versionfile.create_versionfile(
    output_file       = os.path.join(script_dir, version_file_name),
    version           = "1.1.0.0",
    file_description  = "Pie Menus for any windows app",
    internal_name     = "Pie Menus",
    original_filename = "Pie Menus.exe",
    product_name      = "Pie Menus"
)

build_command = "pyinstaller"
build_command += f' -i "{os.path.join(script_dir, "resources/icons/tray_icon.ico")}" ' # application icon
build_command += ' -n "Pie Menus" ' # Name of the application
build_command += ' -w ' # do not start cmd with application
build_command += ' --clean ' # clean previous build and dist folders and temp files
build_command += f' "{os.path.join(script_dir, "main.py")}" ' # Main file to compile
build_command += f' --version-file "{os.path.join(script_dir, version_file_name)}" '
if USE_UPX:
    build_command += ' --upx-dir "{0}" '.format(os.path.join(script_dir, 'resources\\upx-3.96-win64'))
    for file in upx_excludes:
        build_command += f' --upx-exclude={file} '



print(build_command)
os.system(f'cd "{script_dir}"')
os.system(build_command)



# Manually copying files // not including in spec as I don't understand it.
resources   = os.path.join(script_dir, "resources")
settings    = os.path.join(script_dir, "settings")
dist_folder = os.path.join(script_dir, "dist/Pie Menus")
os.system('echo D|xcopy "{0}" "{1}" /E/K/Y'.format(resources, os.path.join(dist_folder, "resources"))) # copying
os.system('echo D|xcopy "{0}" "{1}" /E/K/Y'.format(settings, os.path.join(dist_folder, "settings"))) # copying


# These are files which are not required by Pie Menus, 
# and pie menus works fine without them, 
# deleting to reduce size.
if DELETE_QT_PyInstaller_file:
    files_to_delete = [
        "resources/AHK pie menus demonstration.mp4",
        "resources/buymeacoffee.png",
        "resources/buymeacoffee_small.png",
        "resources/can be removed from pyinstaller dist.txt",
        "resources/Original pyqt radial menu.zip",
        "resources/pip_requirements.txt",
        "resources/readme_banner.png",
        "resources/readme_banner_old.png",
        "resources/references taken while developing program.md",
    # ----------------------------------
        "Qt5Pdf.dll",
        "Qt5VirtualKeyboard.dll",
        "Qt5QmlModels.dll",
        "Qt5DBus.dll",
        "Qt5WebSockets.dll",
        "opengl32sw.dll",
        "Qt5Quick.dll",
        "d3dcompiler_47.dll",
        "libcrypto-1_1.dll",
        "libGLESv2.dll",
        "ucrtbase.dll",
        "libssl-1_1.dll",
        "PySide2/QtNetwork.pyd"

    ]

    dirs_to_delete = [
        "resources/upx-3.96-win64",
        "resources/pie_screenshots",
        "resources/docs",
        "settings/__pycache__",
        "settings/settings UI",  # Do Not delete if setttings UI is ready.
    # ----------------------------------
        "PySide2/translations",
        "PySide2/plugins/styles",
        "PySide2/plugins/platformthemes",
        "PySide2/plugins/platforminputcontexts",
        "PySide2/plugins/imageformats",
        "PySide2/plugins/iconengines",
        "PySide2/plugins/bearer",

    ]

    for file in files_to_delete:
        file = os.path.join(dist_folder, file).replace("/", "\\")
        print(f"Deleting file : {file}")
        try:
            os.system(f'del "{file}"')
        except Exception as e:
            print(e, file)

    for dir in dirs_to_delete:
        print(f"Deleting dir : {dir}")
        dir = os.path.join(dist_folder, dir)
        try:
            os.system(f'rmdir "{dir}" /S/Q')
        except Exception as e:
            print(e, dir)