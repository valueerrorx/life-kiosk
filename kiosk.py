#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import socket
from PyQt5 import QtCore, uic, QtWidgets
from PyQt5.QtGui import *

import threading
import time

import ConfigParser





class MeinDialog(QtWidgets.QDialog):
  
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        scriptdir=os.path.dirname(os.path.abspath(__file__))
        uifile=os.path.join(scriptdir,'kiosk.ui')
        winicon=os.path.join(scriptdir,'images/frostwire.png')
        
        self.ui = uic.loadUi(uifile)        # load UI
        self.ui.setWindowIcon(QIcon(winicon))
        self.ui.exit.clicked.connect(self.onAbbrechen)        # setup Slots
        self.ui.start.clicked.connect(self.onStartConfig)

       
        self.onReadConfig()
        
    



    def ConfigSectionMap(self, section):
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1





    def onStartConfig(self):
        print("nothing yet")
    


    def onReadConfig(self):
         

        generalgrid = self.createGrid("kiosk/general.kiosk")
        self.ui.generalbox.setLayout(generalgrid)
         
        filegrid = self.createGrid("kiosk/filebrowsing.kiosk")
        self.ui.browsingbox.setLayout(filegrid)
         

        actionsgrid = self.createGrid("kiosk/actions.kiosk")
        self.ui.actionsbox.setLayout(actionsgrid)
        
        settingsgrid = self.createGrid("kiosk/settings.kiosk")
        self.ui.settingsbox.setLayout(settingsgrid)
        
        themesgrid = self.createGrid("kiosk/themes.kiosk")
        self.ui.themesbox.setLayout(themesgrid)

    
    
    def createGrid(self, configfile):
        """
        this section reads the config.kiosk file 
        and creates qtwidgets for every action 
        in the config file
        returns: gridlayout
        """
       
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(configfile)
        sections = self.Config.sections()
        
       
        
        maingrid = QtWidgets.QGridLayout()
        widgets = []
        for section in sections:
            if section == "Group":
                try:
                    groupicon = self.ConfigSectionMap(section)['icon']
                    groupdesc = self.ConfigSectionMap(section)['description']
                except KeyError:
                    print("key not found")
                
                itemicon = QtWidgets.QLabel()
                itemicon.setPixmap(QPixmap("images/%s" % groupicon))
                itemicon.setStyleSheet("margin-left:-4px;")
                
                itemdesc = QtWidgets.QLabel()
                itemdesc.setText(groupdesc)
                itemplaceholder= QtWidgets.QLabel('      ')
                
                grid = QtWidgets.QGridLayout()
                grid.setSpacing(2)
                grid.setRowStretch (0, 0)
                grid.addWidget(itemicon, 0, 0)
                grid.addWidget(itemdesc, 1, 0)
                grid.addWidget(itemplaceholder, 2, 0)
                
                titlewidget = QtWidgets.QWidget()
                titlewidget.setLayout(grid)
                
                maingrid.addWidget(titlewidget)
               
                
            else:
                try:
                    sectiontype = self.ConfigSectionMap(section)['type']
                    sectionkey = self.ConfigSectionMap(section)['key']
                    sectionname = self.ConfigSectionMap(section)['name']
                    sectiondesc = self.ConfigSectionMap(section)['description']
                except KeyError:
                    print("key not found")
                
                itemname = QtWidgets.QLabel()
                itemname.setText("<b>%s</b>" % sectionname)
                itemname.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding);
                itemname.setAlignment(QtCore.Qt.AlignLeft)
                itemname.setStyleSheet("margin-top:1px;")
                
                itemdesc = QtWidgets.QLabel()
                itemdesc.setText(sectiondesc)
                itemdesc.setWordWrap(True);
                itemdesc.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding);
                
                itemcheckBox = QtWidgets.QCheckBox()
                itemcheckBox.setStyleSheet("margin-left:-2px;")
                itemplaceholder= QtWidgets.QLabel('      ')
                    
                grid = QtWidgets.QGridLayout()
                grid.setSpacing(0)
                
                grid.setRowStretch (0, 0)
                grid.addWidget(itemname, 0, 1)
                grid.addWidget(itemcheckBox, 0, 0)
                grid.addWidget(itemdesc, 2, 0, 2, 0 )  #fromRow = 0, fromColumn = 0, rowSpan = 2 and columnSpan = 0
                grid.addWidget(itemplaceholder, 3, 0)
                #grid.setColumnStretch(0, 3)
                #grid.setRowStretch(1, 0)
                
                widget = QtWidgets.QWidget()
                widget.setLayout(grid)
                
                widgets.append(widget)


        for widget in widgets:
            maingrid.addWidget(widget)
        
        return maingrid

    
    def onAbbrechen(self):    # Exit button
        self.ui.close()
        os._exit(0)




app = QtWidgets.QApplication(sys.argv)
dialog = MeinDialog()
dialog.ui.show()   #show user interface
sys.exit(app.exec_())
