Updates log

###### 17 April 2021 - 17042021

started the writing the pie menus in python using pyside and qt, the "piemenu_rewrite successful_v0.1.py.bkp" is versioned 0.1, from next time it will be versioned more sense fully starting from 1.

###### 18 April 2021 - 18042021

loaded the json settings into the app and binded hotkeys, tested it, working fine as of now. Got the root exe file name of the active window or app, but as of now I have not used it for any purpose.

Added the class ActiveWindow which takes control of almost everything. **NOTE** this class should only be instanced once.

###### 11 May 2021 - 12052021

Major updates, implemented custom mouse hook, mouse events are now swallowed when pie open, and detected separately to do actions. (This way, other windows don't catch the event). - This also make sure that working(active) window does not change to pie menus window. - this in turn eliminates the requirement to implement the code to remember the last active window and when action triggered, activating last active window again on which action has to be performed.

Gesture trigger implemented.

Implemented trigger keys, but as of now they only work if the menu is holded, that is key pressed once to open and hold menu.

Implemented some basic pie function (actions to be performed).

Refactored and redesigned the settings.json - removed unwanted variables, removed go out and come back to centre to change pie menu and 360 degree swirl around.