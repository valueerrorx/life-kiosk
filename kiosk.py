#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Thomas Michael Weissel
#
# This software may be modified and distributed under the terms
# of the GPLv3 license.  See the LICENSE file for details.

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

import ConfigParser
import sys
import os

class MeinDialog(QtWidgets.QDialog):
  
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.scriptdir=os.path.dirname(os.path.abspath(__file__))
        uifile=os.path.join(self.scriptdir,'kiosk.ui')
        winicon=os.path.join(self.scriptdir,'images/kiosk.png')
        
        self.ui = loadUi(uifile)        # load UI
        self.ui.setWindowIcon(QIcon(winicon))
        self.ui.exit.clicked.connect(self.onAbbrechen)        # setup Slots
        self.ui.start.clicked.connect(self.onStartConfig)

        self.configpath = "kiosk"
        self.lastprofilepath = os.path.join(self.scriptdir,'profiles/last.profile')
        self.configfiles = []
        self.restrictionsdict = {}  #this dict will contain a list of all keys for evey kiosk section
        
        self.getConfigFiles()   # fills self.configfiles with the name of the files that contain all kisok keys and creates a section in self.configoptions for every file
        self.createTabs()  # builds the UI - reads the configfiles and creates widgets for every option
        self.loadLastconfig()   #reads profiles/last.profile and activates the checkboxes
       
        
    

    def getConfigFiles(self):
        """
        searches for config files in the config path and
        fills self.configfiles and self.restrictionsdict
        """
        for root, dirs, files in os.walk(self.configpath):
            for configfilename in files:
                if configfilename.endswith((".kiosk")):
                    self.configfiles.append(configfilename)
                    self.restrictionsdict[configfilename]=[] #create an empty list for each entry in the dictionary



    def ConfigSectionMap(self, section):
        """ 
        creates a dictionary of the specified config section
        returns: dict1
        """
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







    def createTabs(self):
        """
        Generates a tab in the UI for every found configuration .kiosk file and 
        triggers createGrid() in order to fill the tabs with widgets for all restriction keys
        """
        for configfilename in self.configfiles:
            generalgrid,groupname,sectionicon = self.createGrid(configfilename)
            tab = QtWidgets.QWidget()
            tab.setLayout(generalgrid)
            self.ui.tabWidget.addTab(tab, sectionicon, groupname)
            
            
            #we need to parse a profile file here and restore the checkbox states
            #for restriction in self.restrictionsdict[configfilename]:
                #print(restriction.rcheckbox.isChecked() )
            

    
    
    def createGrid(self, configfilename):
        """
        this section reads the config.kiosk file 
        and creates tabs for every configfile and qtwidgets for every action 
        in the config file
        returns: maingrid, groupname, sectionicon
        """
        self.Config = ConfigParser.ConfigParser()
        configfilepath = os.path.join(self.configpath,configfilename)
        self.Config.read(configfilepath)
        sections = self.Config.sections()   #creates a list of all found sections in the config file

        maingrid = QtWidgets.QGridLayout()   #this is the mainlayout that is returned and later applied to the tab 
        scrollarea = QtWidgets.QScrollArea()  # scrollarea is the only widget inside the mainlayout
        scrollgrid = QtWidgets.QGridLayout()  # scrollgrid is the gridlayout inside the scroallarea
        scrollwidget = QtWidgets.QWidget()  #scrollwidget is the first widget for the scrollarea and gets scrollgrid as layout
        scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
 
        widgets = []
        for section in sections:
            if section == "Group":   # this is a mandatory section of every configfile and creates the tab, description, tabicon etc.
                try:
                    groupicon = self.ConfigSectionMap(section)['icon']
                    groupname = self.ConfigSectionMap(section)['name']
                    groupdesc = self.ConfigSectionMap(section)['description']
                except KeyError:
                    print("one or more keys not found")
       
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
                
            else:  #these are normal kiosk restriction keys 
                try:
                    sectiontype = self.ConfigSectionMap(section)['type']
                    sectionkey = self.ConfigSectionMap(section)['key']
                    sectionname = self.ConfigSectionMap(section)['name']
                    sectiondesc = self.ConfigSectionMap(section)['description']
                except KeyError:
                    print("one or more keys not found")
                
                itemtype = sectiontype
                itemkey = sectionkey
                
                itemname = QtWidgets.QLabel()
                itemname.setText("%s" % sectionname)
                itemname.font=QFont()
                itemname.font.setBold(True)
                itemname.setFont(itemname.font)
                itemname.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
                itemname.setAlignment(Qt.AlignLeft)
                itemname.setStyleSheet("margin-top:1px;")
                
                itemdesc = QtWidgets.QLabel()
                itemdesc.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
                itemdesc.setText(sectiondesc)
                itemdesc.setWordWrap(True);
                itemdesc.setStyleSheet("margin-left:1px;")
                itemdesc.setAlignment(Qt.AlignTop)
    
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
                widgets.append(widget)  #add the finalized widget to the widgets list
                
                
                #collect and store every created widget as attribute of a  restriction-object in the restrictionsdict
                restriction = Restriction(itemtype, itemkey, itemname, itemdesc, itemcheckBox)
                self.restrictionsdict[configfilename].append(restriction)  #append to list in section of the dictionary


        for widget in widgets:
            scrollgrid.addWidget(widget)   # add all widgets to the scrollgrid layout

        scrollwidget.setLayout(scrollgrid)  # set scrollgrid as layout for the scroll widget
        scrollarea.setWidget(scrollwidget)  # set the scrollwidget as mainwidget for the scrollarea
        maingrid.addWidget(scrollarea,0,0)  # add the scrollalrea to the maingrid layout which will then be used as mainlayout for the specfic Tab
         
        return maingrid, groupname, sectionicon

    
    
    
    

    
    
    
    def onStartConfig(self):
        """
        parses all widgets and writes the state of the checkboxes into "last.profile" 
        then writes the plasma configuration files and reloads plasma desktop  
        """
        fileobject = open(self.lastprofilepath,"w")
        
        activerestrictions = []
        
        for configfilename in self.configfiles:
            print("Restrictions active in %s" % configfilename)
            
            for restriction in self.restrictionsdict[configfilename]:
                if restriction.rcheckbox.isChecked():
                    print(restriction.rname.text() )
                    activerestrictions.append(restriction.rname.text() )
           
        
        #generate profile file text
        profileconfigcontent = ""
        for activerestriction in activerestrictions:
            profileconfigcontent += "%s\n" % activerestriction
        
        print(profileconfigcontent)
        fileobject.write(profileconfigcontent)
        
        
        #write plasma Config
        
        #reload desktop
        
        
    def loadLastconfig(self):
        with open(self.lastprofilepath) as fileobject:
            lastconfig = fileobject.readlines()
        # remove whitespace characters like `\n` at the end of each line
        lastconfig = [x.strip() for x in lastconfig] 
        
        for configfilename in self.configfiles:
            for restriction in self.restrictionsdict[configfilename]:
                if restriction.rname.text() in lastconfig:
                    restriction.rcheckbox.setChecked(True)
  
            
        
    def onAbbrechen(self):    # Exit button
        self.ui.close()
        os._exit(0)


    


class Restriction(object):
    rtype = ""
    rkey  = ""
    rname = ""
    rdesc = ""
    rcheckbox = ""
    
    # The class "constructor"
    def __init__(self, rtype, rkey, rname, rdesc, rcheckbox):
        self.rtype = rtype
        self.rkey = rkey
        self.rname = rname
        self.rdesc = rdesc
        self.rcheckbox = rcheckbox


app = QtWidgets.QApplication(sys.argv)
dialog = MeinDialog()
dialog.ui.show()   #show user interface
sys.exit(app.exec_())
