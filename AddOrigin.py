import FreeCADGui as Gui
import FreeCAD as App
import Part
from PySide import QtGui
from PySide import QtCore
from PySide.QtUiTools import QUiLoader
import os
import RPWlib
import json

path_to_ui = RPWlib.pathOfModule() + "/updateOrigin.ui"


class AddOrigin():

    def __init__(self):
        self.form = Gui.PySideUic.loadUi(path_to_ui)
        self.form.buttonSetStart.clicked.connect(lambda: self.updateOriginPos())


    def accept(self):
        zRot = self.form.Box_Rot_Z.value()
        yRot = self.form.Box_Rot_Y.value()
        xRot = self.form.Box_Rot_X.value()
        originPoint = App.Vector(self.form.Box_Origin_X.value(),self.form.Box_Origin_Y.value(),self.form.Box_Origin_Z.value())
        lcs = App.activeDocument().addObject( 'PartDesign::CoordinateSystem', 'LCS' )
        lcs.Placement = App.Placement(originPoint,App.Rotation(zRot,yRot,xRot))
    
    def updateOriginPos(self):
        sel = Gui.Selection.getSelection()   
        mydoc = App.activeDocument().Name
        document_ = mydoc
        try:
            object_Label = sel[0].Label
            object_Name  = sel[0].Name
        except Exception:
            object_Label = ""
            object_Name  = ""
        try:
            SubElement = Gui.Selection.getSelectionEx()[0]   
            element_ = SubElement.SubObjects[0]
            pos = element_.BoundBox.Center
        except Exception:
            element_ = ""
        self.form.Box_Origin_X.setValue(pos[0])
        self.form.Box_Origin_Y.setValue(pos[1])
        self.form.Box_Origin_Z.setValue(pos[2])
        App.Console.PrintMessage("x = {}\r\n".format(pos[0]))
        App.Console.PrintMessage("y = {}\r\n".format(pos[1]))
        App.Console.PrintMessage("z = {}\r\n".format(pos[2]))
        App.Console.PrintMessage("\r\n")


class AddOriginCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_linSegCMD_2_icon.svg", # the name of a svg file available in the resources
                'Accel' : "Alt+O", # a default shortcut (optional)
                'MenuText': "Add Origin to the Model",
                'ToolTip' : "Add Origin"}

    def Activated(self):
        panelOrig = AddOrigin()
        Gui.Control.showDialog(panelOrig)
        return True

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True



Gui.addCommand('Add_Origin_Command',AddOriginCmd())
