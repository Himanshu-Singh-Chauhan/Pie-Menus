###### To dos

- [x] Load settings file into python
- [x] refactor **little bit** the settings json
- [x] get the root exe of the active window or app
- [x] instead of lettings new Qtimers get created everytime, just stop and start them, it will save time and CPU
- [x] add frosty glass behind pie menus, and lock mouse to that region to receive mouse clicks and keyboard events. (Instead of doing this, I implemented own mouse hook, so now this is not required)
- [x] Multi Monitor support 
- [ ] Android like toast messege, on errors, exceptions, volume up and down, bg tasks, way to use and limitations of pie menus.
- [ ] wheel up and down on pie slices
- [ ] toast messages with icons
- [ ] if mouse is out of certain radius, kill pie menus, take care of padding. only if maya marking rope is disabled, define radius in only global, not per.
- [ ] if mouse goes out of certain rectangular radius of context menu, kill it. only global settings.
- [ ] Add capslock key remaping just like that ahk script.
- [ ] improve window change detection function, maybe its working extra stuff not required, (maybe nothing can be improved more, it is what it is.)
- [x] DPI change per monitor
- [x] Suspend/Resume entire app from tray icon
- [ ] Suspend current profile from tray icon
- [ ] Secret shift or alt hold change action type, something superior, like holding shift and pressing restart in windows gives it a hard restart. should only happen when pie menu are held open.
- [ ] Context menu save padding, if space not available, change opening position/direction.
- [ ] marking menu: show static rope from original position to submenu pos like maya. Keep it as an option.



###### DISCARDED TODOS (Could not happen)

- [x] detect window changes by capturing system messages on window change. (researched a lot, could not get it to work)
- [x] Get new moniters plugged notification