#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2021 Lerchbaumer Thomas                                 *
#*                                                                         *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 3 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Lesser General Public License for more details.                   *
#*                                                                         *
#*   You should have received a copy of the GNU Lesser General Public      *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

import FreeCADGui as Gui
import FreeCAD as App
import Part
from PySide import QtGui
from PySide import QtCore
from PySide.QtUiTools import QUiLoader
import os
import RPWlib
import Movements,CreateCircSeg,CreateLinSeg,CreateP2PSeg
import json



class CreateLinSegCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_linSeg_icon.svg", # the name of a svg file available in the resources
                'Accel' : "Alt+L", # a default shortcut (optional)
                'MenuText': "Create a Linear Segment between two points",
                'ToolTip' : "Generate a new linear Segment"}

    def Activated(self):
        
        panelLin = CreateLinSeg.CreateLinSeg()
        Gui.Control.showDialog(panelLin)

        return True

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

class CreateP2PSegCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_P2PSeg_icon.svg", # the name of a svg file available in the resources
                'Accel' : "Alt+P", # a default shortcut (optional)
                'MenuText': "Create a P2P Segment between two points",
                'ToolTip' : "Generate a new P2P Segment"}

    def Activated(self):
        
        panelP2P = CreateP2PSeg.CreateP2PSeg()
        Gui.Control.showDialog(panelP2P)

        return True

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

class CreateCircSegCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_circSeg_icon.svg", # the name of a svg file available in the resources
                'Accel' : "Alt+C", # a default shortcut (optional)
                'MenuText': "Create a Circular Segment between two points",
                'ToolTip' : "Generate a new Circular Segment"}

    def Activated(self):
        
        panelCirc = CreateCircSeg.CreateCircSeg()
        Gui.Control.showDialog(panelCirc)

        return True

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


Gui.addCommand('Create_Linear_Segment',CreateLinSegCmd())
Gui.addCommand('Create_P2P_Segment',CreateP2PSegCmd())
Gui.addCommand('Create_Circular_Segment',CreateCircSegCmd())