#!/bin/bash
xrandr --output eDP --scale 0.85x0.85

# Screen info
connected_screens=$(xrandr --query | grep " connected")

# if laptop-hdmi connected
if echo "$connected_screens" | grep -q "HDMI-A-0"; then
    xrandr --output eDP --primary --mode 1920x1080 --pos 144x1080 --rotate normal --output HDMI-A-0 --mode 1920x1080 --pos 0x0 --rotate normal --output DisplayPort-0 --off
# if hud-hdmi conected
elif echo "$connected_screens" | grep -q "DisplayPort-0"; then
    xrandr --output eDP --primary --mode 1920x1080 --pos 144x1080 --rotate normal --output DisplayPort-0 --mode 1920x1080 --pos 0x0 --rotate normal --output HDMI-A-0 --off
fi
xinput set-prop "MSFT0004:00 06CB:CD98 Touchpad" "libinput Natural Scrolling Enabled" 1
xinput set-prop "MSFT0004:00 06CB:CD98 Touchpad" "libinput Tapping Enabled" 1
setxkbmap es
feh --bg-fill "/home/BM4lex/.config/qtile/wallpaper.png"
light-locker &   
picom &
nm-applet &
volumeicon &
cbatticon -u 5 &
blueman-applet &
greenclip daemon &3