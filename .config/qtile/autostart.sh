#! /bin/sh

export EDITOR=nvim
xinput --set-prop "ELAN1300:00 04F3:3087 Touchpad" "libinput Natural Scrolling Enabled" 1 &
setxkbmap -option grp:alt_shift_toggle us,es &
nitrogen --restore &
picom -f -b --config /home/mura/.config/picom/picom_not_rounded.conf
light -S 50 &
blueberry-tray &
xfce4-power-manager &
nm-applet &
