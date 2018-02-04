# life-kiosk

A simple KIOSK tool for KDE Plasma 5

This application is written in Python, PyQt5.

The applications allows to lock down plasma desktop, filemanagmenet and other important settings.

State:  Alpha (UI is working but NONE of the restrictions have been tested)

The .kiosk files contain all the available action restrictions, url restrictions, control module restrictions.
The UI autogenerates itself by reading those config files. Therefore this application should be very easy to maintain.


Example:

* [Action-1]
* Type=action restriction
* Key=action/kwin_rmb
* Name=Disable Window Manager context menu (Alt-F3)
* Description=The Window Manager context menu is normally shown when Alt-F3 is pressed or when the menu button on the window frame is pressed


Installation:
Just download the repository as zip file, extract and run kiosk.py
Please test and report bugs and feature requests here on github (new issue)
None of the restriction keys are tested yet. I will check most of them eventually.


![Image of life-kiosk](http://life-edu.eu/images/life-kiosk2.gif)



