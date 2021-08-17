#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2021 Lerchbaumer Thomas                                 *
#*                                                                         *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************


import FreeCADGui as Gui
import FreeCAD as App

class RobotPathWorkbench(Gui.Workbench):
    def __init__(self):
        import RPWlib
        self.__class__.MenuText = "Robot Path Workbench"
        self.__class__.ToolTip = "A Workbench to create and export Paths for Robots"
        self.__class__.Icon =  RPWlib.pathOfModule() + "/icons/WB_main_icon.svg"

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import CreateSeg, AddOrigin, AddPoints, NewModule, EditPath, ReloadView
        self.segmentCommands = ["Create_Linear_Segment","Create_P2P_Segment","Create_Circular_Segment"] # A list of command names created in the line above
        self.mainCommands = ["Add_Origin_Command", "Add_Points_Command"]
        self.advancedCommands = ["Add_New_Module_Command"]
        self.RPWMenuPath = ["Edit_Path_Command"]
        self.RPWMenu = ["Reload_View_Command"]
        self.appendToolbar("Main Commands",self.mainCommands)
        self.appendToolbar("Add Segment",self.segmentCommands) 
        self.appendToolbar("Advanced Commands",self.advancedCommands) # creates a new toolbar with your commands
        
        
    
        
    def Activated(self):
        import RPWClasses
        import RPWlib
        import json
        from PySide import QtGui
        RPWlib.MovementList.List = []
        RPWlib.PointsList.List = []
        RPWlib.CSList.List = []
        
        RPWlib.config = RPWClasses.ProjectConfiguration()
        RPWlib.config.readConfig()
        RPWlib.config.writeConfig()
        
        App.ActiveDocument.recompute()

        try:
            mw = Gui.getMainWindow()
            c = mw.findChild(QtGui.QTextEdit, "Report view")
            c.clear()
        except Exception as e:
            App.Console.PrintError(e)
        """This function is executed when the workbench is activated"""
        try:
            RPWlib.mainCMDs = mw.findChild(QtGui.QToolBar, "Main Commands")
            RPWlib.addSegCMDs = mw.findChild(QtGui.QToolBar, "Add Segment")
            RPWlib.newModCMDs = mw.findChild(QtGui.QToolBar, "Advanced Commands")
            RPWlib.mainCMDs.show()
            RPWlib.addSegCMDs.show()
            RPWlib.newModCMDs.show()
        except Exception as e:
            App.Console.PrintError(e)
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self,recipient):
        self.appendContextMenu(["RPW Workbench", "Path"],self.RPWMenuPath)
        self.appendContextMenu(["RPW Workbench"], self.RPWMenu)

    def GetClassName(self): 
        # This function is mandatory if this is a full python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"

Gui.addWorkbench(RobotPathWorkbench)