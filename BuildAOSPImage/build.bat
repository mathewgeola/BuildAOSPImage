@echo off
pyside6-rcc resources.qrc -o resources_rc.py
pyinstaller -F -w -i icon.ico -n BuildAOSPImage main.py