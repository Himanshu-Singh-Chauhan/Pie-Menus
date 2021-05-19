SetCapsLockState, AlwaysOff
CapsLock & d::Run, "C:\Users\S\Downloads\"
CapsLock & i::Send {Up}
CapsLock & k::Send {Down}
CapsLock & j::Send {Left}
CapsLock & l::Send {Right}
CapsLock & o::Send {BackSpace}
CapsLock & Space::Send {Media_Play_Pause}
CapsLock & ]::Send {Volume_Up}
CapsLock & [::Send {Volume_Down}
CapsLock & Alt::Run, "C:\Users\S\Desktop\"
CapsLock & a::Send !{Left}
CapsLock & s::Send !{Right}
CapsLock & q::Send #!{d}
+=:: Send {=}
=::Send {NumpadAdd}
CapsLock & h::
IF GetKeyState("Shift","P")
	Send +{Home}
Else
	Send {Home}
Return
CapsLock & e::
IF GetKeyState("Shift","P")
	Send +{End}
Else
	Send {End}
Return

;capslock up::

;if GetKeyState("CapsLock", "T") = 1
; {
;   SetCapsLockState, off
; }
;else if GetKeyState("CapsLock", "F") = 0
; {
;   SetCapsLockState, on
; }

