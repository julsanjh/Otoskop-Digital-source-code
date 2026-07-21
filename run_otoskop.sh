#!/bin/bash
export DISPLAY=:0
export XAUTHORITY=/root/.Xauthority

xset s off
xset -dpms
xset s noblank

# Panggil manajer jendela
openbox &
sleep 1

# [KUNCI]: Jalankan Layar Loading TERLEBIH DAHULU
/usr/bin/python3 /home/home/loading_medis.py

# Setelah layar loading selesai (menghancurkan dirinya), Tembak Menu Utama!
exec /usr/bin/python3 /home/home/ui_medis.py
