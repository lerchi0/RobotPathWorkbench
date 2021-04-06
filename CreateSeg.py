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
path_to_ui = "C:/Users/t-ler/AppData/Roaming/FreeCAD/Mod/RobotPathWorkbench//createLinSegDialog.ui"



class CreateLinSegCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_linSegCMD_2_icon.svg", # the name of a svg file available in the resources
                'Accel' : "Alt+S", # a default shortcut (optional)
                'MenuText': "Create a Linear Segment between two points",
                'ToolTip' : "Generate a new linear Segment"}

    def Activated(self):
        # TODO: GUI soll funktionieren
        panelLin = CreateLinSeg.CreateLinSeg()
        panelP2P = None
        panelCirc = None
        Gui.Control.showDialog(panelLin)
        Gui.Control.showDialog(panelP2P)
        Gui.Control.showDialog(panelCirc)

        return True

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

Gui.addCommand('Create_Linear_Segment',CreateLinSegCmd())