#!/bin/bash

rm -r build
mkdir build
cd build || exit

pyinstaller ../app/app.py --hidden-import='PIL._tkinter_finder' --add-data='../app/icons/*.png:icons' --onefile
