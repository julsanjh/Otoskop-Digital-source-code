#!/bin/bash
export DISPLAY=:0
export XAUTHORITY=/root/.Xauthority

xset s off
xset -dpms
xset s noblank

openbox &
sleep 1

/usr/bin/python3 /home/home/loading_medis.py

exec /usr/bin/python3 /home/home/ui_medis.py
