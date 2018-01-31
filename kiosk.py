#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Thomas Michael Weissel
#
# This software may be modified and distributed under the terms
# of the GPLv3 license.  See the LICENSE file for details.



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
        winicon=os.path.join(scriptdir,'images/kiosk.png')
        
        self.ui = uic.loadUi(uifile)        # load UI
        self.ui.setWindowIcon(QIcon(winicon))
        self.ui.exit.clicked.connect(self.onAbbrechen)        # setup Slots
        self.ui.start.clicked.connect(self.onStartConfig)

        self.configfiles = []
        self.getConfigFiles()
        self.readConfig()
     
        
    

    def getConfigFiles(self):
        
        for root, dirs, files in os.walk("kiosk/"):
            for name in files:
                if name.endswith((".kiosk")):
                     self.configfiles.append(os.path.join(root, name))
        





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
    


    def readConfig(self):
        for configfile in self.configfiles:
            generalgrid,groupname,sectionicon = self.createGrid(configfile)
            tab = QtWidgets.QWidget()
           
            tab.setLayout(generalgrid)
            self.ui.tabWidget.addTab(tab, sectionicon, groupname)
            

    
    
    def createGrid(self, configfile):
        """
        this section reads the config.kiosk file 
        and creates tabs for every configfile and qtwidgets for every action 
        in the config file
        returns: maingrid, groupname
        """
        self.Config = ConfigParser.ConfigParser()
        self.Config.read(configfile)
        sections = self.Config.sections()

        maingrid = QtWidgets.QGridLayout()   #this is the mainlayout that is returned and later applied to the tab 
        scrollarea = QtWidgets.QScrollArea()  # scrollarea is the only widget inside the mainlayout
        scrollgrid = QtWidgets.QGridLayout()  # scrollgrid is the gridlayout inside the scroallarea
        scrollwidget = QtWidgets.QWidget()  #scrollwidget is the first widget for the scrollarea and gets scrollgrid as layout
        scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
 
        widgets = []
        for section in sections:
            if section == "Group":
                try:
                    groupicon = self.ConfigSectionMap(section)['icon']
                    groupname = self.ConfigSectionMap(section)['name']
                    groupdesc = self.ConfigSectionMap(section)['description']
                except KeyError:
                    print("key not found")
       
                sectionicon = QIcon.fromTheme(groupicon)
                itemicon = QtWidgets.QLabel()
                itemicon.setPixmap(QPixmap(sectionicon.pixmap(64)))

                itemicon.setStyleSheet("margin-left:-4px;")
                itemdesc = QtWidgets.QLabel()
                itemdesc.setText(groupdesc)
                verticalSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                
                grid = QtWidgets.QGridLayout()
                grid.setSpacing(2)
                grid.addWidget(itemicon, 0, 0)
                grid.addWidget(itemdesc, 1, 0)
                grid.addItem(verticalSpacer, 2, 0)

                titlewidget = QtWidgets.QWidget()
                titlewidget.setLayout(grid)
                scrollgrid.addWidget(titlewidget,0,0)
                
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
                itemname.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
                itemname.setAlignment(QtCore.Qt.AlignLeft)
                itemname.setStyleSheet("margin-top:1px;")
                
                itemdesc = QtWidgets.QLabel()
                itemdesc.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
                itemdesc.setText(sectiondesc)
                itemdesc.setWordWrap(True);
                itemdesc.setStyleSheet("margin-left:1px;")
                itemdesc.setAlignment(QtCore.Qt.AlignTop)
    
                itemcheckBox = QtWidgets.QCheckBox()
                itemcheckBox.setStyleSheet("margin-left:-2px;")
              
                grid = QtWidgets.QGridLayout()
                grid.setSpacing(0)
                grid.setColumnMinimumWidth(1,600)
                grid.addWidget(itemcheckBox, 0, 0)
                grid.addWidget(itemname, 0, 1)
                grid.addWidget(itemdesc, 1, 1 )  #fromRow = 0, fromColumn = 0, rowSpan = 2 and columnSpan = 0

                widget = QtWidgets.QWidget()
                widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
                widget.setLayout(grid)
                widgets.append(widget)


        for widget in widgets:
            scrollgrid.addWidget(widget)

        scrollwidget.setLayout(scrollgrid)
        scrollarea.setWidget(scrollwidget)
        maingrid.addWidget(scrollarea,0,0)
        
        return maingrid, groupname, sectionicon

    
    
    def onAbbrechen(self):    # Exit button
        self.ui.close()
        os._exit(0)




app = QtWidgets.QApplication(sys.argv)
dialog = MeinDialog()
dialog.ui.show()   #show user interface
sys.exit(app.exec_())
