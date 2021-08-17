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
import Part
from PySide2 import QtGui
from PySide import QtGui as QGui 
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
import RPWlib


path_to_ui = RPWlib.pathOfModule() + "/newModul.ui"
class AddModule():
    
    # Ablauf:
    #           - sollen bestehende geladen werden?
    #           - Ursprungs KS wählen
    #           - Punkte definieren
    #           - Pfade definieren
    #           - abspeichern für mehrmalige Verwendung 



    def __init__(self):
        self.form = Gui.PySideUic.loadUi(path_to_ui)

    def accept(self):
        return True


class AddModuleCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_newModule_icon.svg", # the name of a svg file available in the resources
                'Accel' : "", # a default shortcut (optional)
                'MenuText': "Add Standard Module to the Model",
                'ToolTip' : "Add Module"}

    def Activated(self):
        panelMod = AddModule()
        Gui.Control.showDialog(panelMod)
        return True

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True
    def Deactivated(self):
        pass



Gui.addCommand('Add_New_Module_Command',AddModuleCmd())
