import FreeCADGui as Gui
import FreeCAD as App
import Part
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
import os
import RPWlib
import RPWClasses
import json

path_to_ui = RPWlib.pathOfModule() + "/pointsView.ui"
path_to_widget = RPWlib.pathOfModule() + "/pointsDisp.ui"

class AddPoints():
    def __init__(self):
        self.form = Gui.PySideUic.loadUi(path_to_ui)
        for idx, val in enumerate(RPWlib.PointsList.List):
            self.form.listWidget.addItem(str(idx))
        self.form.listWidget.itemClicked.connect(self.printItem)

    def printItem(self,item):
        point = RPWlib.PointsList.List[int(item.text())]

        self.form.Box_Point_CS.setText(point.coordinateSystem)
        self.form.Box_Point_ID.setText(item.text())
        self.form.Box_Point_X.setText(str(point.position["X"]))
        self.form.Box_Point_Y.setText(str(point.position["Y"]))
        self.form.Box_Point_Z.setText(str(point.position["Z"]))
        self.form.Box_Point_Yaw.setText("0")
        self.form.Box_Point_Pitch.setText("0")
        self.form.Box_Point_Roll.setText("0")

        App.Console.PrintMessage(RPWlib.PointsList.List[int(item.text())].__dict__)
        App.Console.PrintMessage("\r\n")

    def accept(self):
       pass

    def updatePos(self):
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
        #self.form.Box_Origin_X.setValue(pos[0])
        #self.form.Box_Origin_Y.setValue(pos[1])
        #self.form.Box_Origin_Z.setValue(pos[2])
        App.Console.PrintMessage("x = {}\r\n".format(pos[0]))
        App.Console.PrintMessage("y = {}\r\n".format(pos[1]))
        App.Console.PrintMessage("z = {}\r\n".format(pos[2]))
        App.Console.PrintMessage("\r\n")


class AddPointsCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_linSegCMD_2_icon.svg", # the name of a svg file available in the resources
                'Accel' : "Alt+P", # a default shortcut (optional)
                'MenuText': "Add Points to the Model",
                'ToolTip' : "Add Points"}

    def Activated(self):
        panelOrig = AddPoints()
        Gui.Control.showDialog(panelOrig)
        return True

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True



Gui.addCommand('Add_Points_Command',AddPointsCmd())
