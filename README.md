<p align = "center"><a><img src="https://github.com/Himanshu-Singh-Chauhan/Pie-Menus/blob/main/resources/readme_banner.png" alt=Pie menus banner"></a></p>

###### there is still a lot to do in pie menus, go easy on it, and keep an eye on updates. 😉

# What is Pie Menus

Blender like pie menus for windows, (blender is free 3d software), its not limited or confined to app, you can set up pie menus for any app or window on your system. 

Pie Menus allow you to improve your workflow, you can use it to launch applications, simulate long hotkeys, open URLs, open favourite file folder locations, run other python scripts which automates repetitive tasks and navigate browsers, explorers and windows much faster. It’s very powerful tool once mastered, which is fairly easy. It also has submenus, which is like another pie menu inside a pie menu, you also bind different task on scroll wheel for menu, like volume or brightness control.

Pie Menus are somewhat like context menu, but instead of showing a menu with options in a listed manner, pie menus shows the option in a circle around the mouse cursor. In case you don't know what context menu are, the menu that pop up when you right click on desktop, or on a file, or on some selected text is called context menu. You can check out some screenshots below as to how pie menus look like.

**Note**: Pie menus are designed to be used in with combination of keyboard and mouse (**not trackpad**), although with the use trigger keys (a feature in pie menus) you can eliminate the use of mouse in some cases, which is still efficient but definitely not the best. Triggers keys are there for times when you don't have your any hand on mouse and don't want to take your hand off keyboard or don't want to reach the mouse at all.

**How to use Pie Menus** 🖱
---

The Pie menus will pop up when you press an assigned hotkey, once open you can select an menu/option in it using mouse. 

There are two ways to use:

- You press the hotkey normally (press and let go), the pie menus will open and stay until a menu is selected or the pie menu is cancelled using 'esc' or right click. To activate a menu, select using hovering mouse near it, and pressing left click (lifting left click will activate the selected menu).
- Pressing and holding down the hotkey, the pie menus will stay open until the held hotkey is released, when releasing the hotkey, the selected menu will automatically get activated, there is no need for left click, just hover on the menu to activate and release the hotkey. Using this mode which I like to call marking mode (from Autodesk Maya), you can speed up your workflow significantly. It will feel just like drawing gesture using mouse. After a few usage of it, you can also do it with your eyes closed as your muscle memory will remember which way to flick the mouse to activate certain menu. and yes in marking mode also pie menu can be cancelled using 'esc'  or right click. 

**Quick Getting Started** : After installing and running, go to desktop and press tilde key  `  on keyboard to call a pie menu.

**List of stock Pie Menus**: Yet to be documented.

**List of stock themes**: Yet to be documented.

**Installation**
---

Download the latest release from the <a href = "https://github.com/Himanshu-Singh-Chauhan/Pie-Menus/releases">releases</a> tab, and Install just like any other windows app/software.

To disable it to run with windows boot, you can open task manager, go to startup tab, select pie menus and disable it. same to enable it again.

**Features**
---

- Multi monitor support.
- High DPI support, can be used on 4k monitors.
- Sub Menus - Marking Menus (kind of like pie Menus inside pie Menus)
- Smooth Animations & Transitions.
- Multiple themes, can be set different of different menus.
- Scroll wheel action on menus
- Trigger keys when you are lazy and don't want to reach mouse.
- Maya like tracking line, Blender like tracking slice.

**System Requirements**
---

Any windows 10 - 64 bit.

Not tested on 32 bit, although should work fine. Let me know if anyone tests it on a 32 bit machine, whether it works fine or have issues.

**Screenshots**
---

<a><img src="https://github.com/Himanshu-Singh-Chauhan/Pie-Menus/blob/main/resources/pie_screenshots/screen%201.png" alt="Pie Menus screen shots" style="border-radius:20px"></a>



<a><img src="https://github.com/Himanshu-Singh-Chauhan/Pie-Menus/blob/main/resources/pie_screenshots/screen%203.png" alt="Pie Menus screen shots" style="border-radius:20px"></a>

**Create your own Pie Menus**
--
Yet to be documented. Sorry. Please edit appProfiles.json.

**A Special Thanks** ❤❤❤
---

A very special thanks to <a href = "https://github.com/dumbeau">Beau Gills</a> for his marvellous work <a href = "https://github.com/dumbeau/AutoHotPie">AutoHotPie</a>, He in the first place created pie menus for windows using Autohotkey scripting language, Its just awesome and mind blowing how much effort he has put into it. For days I was searching for pie menus for windows and it was the only project I found after too many google searches and it changed everything. I must admit that this project wouldn't be here *how it is* without Beau. My heartful thanks to him ❤😊.


**Feature request, Bugs and Issue reporting**
---
More features coming soon, if you have any feature request, you can create a new issue for it.

**How to run from source code**
---

- Clone the repo or download as zip.
		`git clone https://github.com/Himanshu-Singh-Chauhan/Pie-Menus.git`
- install python v3 or above, version I use during development is `v3.9.4` and a bunch of packages which are stored in <a href = "https://github.com/Himanshu-Singh-Chauhan/Pie-Menus/blob/main/resources/pip_requirements.txt">pip_requirements.txt</a> and can be installed from following command.
```
		pip install -r /resources/pip_requirements.txt
```
- run "main.py" directly or from any code editor
- to exit app, exit from hidden icon in tray

**How to Contribute** 
---

Any contributions you make are most welcome and are greatly appreciated.

1. Clone repo and create a new branch: `git checkout https://github.com/Himanshu-Singh-Chauhan/Pie-Menus -b name_for_new_branch`.
2. Make changes and test
3. Submit Pull Request with comprehensive description of changes

You can contribute new set of Pie Menus which can be useful to most people, or new theme.

The set of pie menus contributed should be available with appprofile, should be disabled by default, document it properly, and should use the default theme. 

DO NOT submit a menu which is very very specific to your workflow which may not work on other's system.

**Acknowledgements** / Attributions
---

- <a href = "https://www.flaticon.com/free-icon/pie_1411020?term=pies&related_id=1411020" >Icon</a> used for the app - Icons made by <a href="https://www.flaticon.com/authors/ultimatearm" title="ultimatearm">ultimatearm</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
- Keyboard module for global hotkeys by <a href = "https://github.com/boppreh/keyboard" >boppreh</a>
- Many references taken from stack overflow and all over from internet are listed in <a href = "https://github.com/Himanshu-Singh-Chauhan/Pie-Menus/blob/main/resources/references%20taken%20while%20developing%20program.md" >here</a>.

**Additional Information**
---

- <a href = "">Change log / Updates log</a> (not updated regularly because I am lazy.)
- FAQs <a href="">here</a>.
- Marking Menus <a href = "https://damassets.autodesk.net/content/dam/autodesk/research/publications-assets/pdf/the-design-and-evaluation.pdf">documentation</a> by Autodesk
- Marking menu how to use <a href = "http://www.e-nzone.com/LAB/Working_with_Marking_Menu.pdf">here</a>.
- Blender Pie Menus <a href = "https://www.youtube.com/watch?v=oyW5JJ0rS0U">tutorial</a>
- My tweaked version of AHK AutoHotPie by Beau can be found in this repository.

<br>

## want to *Support* the project ##
<p align = "left"><a href = "https://www.buymeacoffee.com/HimanshuChauhan"><img src="https://github.com/Himanshu-Singh-Chauhan/Pie-Menus/blob/main/resources/buymeacoffee.png" alt="Donation Link to Buy Me a Coffee" width="250" height="70"></a></p>



[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FHimanshu-Singh-Chauhan%2FPie-Menus&count_bg=%23020202&title_bg=%23EC095B&icon=&icon_color=%23E7E7E7&title=visitor+count&edge_flat=false)](https://hits.seeyoufarm.com)