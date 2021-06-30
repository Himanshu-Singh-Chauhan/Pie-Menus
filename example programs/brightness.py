import screen_brightness_control as sbc

#get the current screen brightness (for all detected displays)
all_screens_brightness = sbc.get_brightness()
#get the brightness of the primary display
primary_display_brightness = sbc.get_brightness(display=0)
print(f"{all_screens_brightness = }")
print(f"{primary_display_brightness = }")
# sbc.set_brightness("+10")
sbc.fade_brightness(0, increment = 1)
#get the brightness of the secondary display (if connected)
# secondary_display_brightness = sbc.get_brightness(display=1)