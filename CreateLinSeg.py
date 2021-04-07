import FreeCADGui as Gui
import FreeCAD as App
import Part
import os
import RPWlib
import Movements
import json
path_to_ui = "C:/Users/t-ler/AppData/Roaming/FreeCAD/Mod/RobotPathWorkbench//createLinSegDialog.ui"


class CreateLinSeg():

    def __init__(self):
        self.form = Gui.PySideUic.loadUi(path_to_ui)
        self.form.buttonSetStart.clicked.connect(lambda: self.updateStartPos())
        self.form.buttonSetEnd.clicked.connect(lambda: self.updateEndPos())

    def accept(self):
        startPoint = [self.form.Box_Start_X.value(), self.form.Box_Start_Y.value(), self.form.Box_Start_Z.value()]
        endPoint = [self.form.Box_End_X.value(), self.form.Box_End_Y.value(), self.form.Box_End_Z.value()]
        RPWlib.MovementList.List.append(Movements.LinearMovement(id= RPWlib.MovementList.currentId,sPoint=startPoint, ePoint= endPoint).__dict__)
        RPWlib.MovementList.currentId = RPWlib.MovementList.currentId +1
        with open(RPWlib.MovementList.pathToFile, 'w') as outfile:
            json.dump(RPWlib.MovementList.List, outfile, indent=4)


    def updateStartPos(self):
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
        self.form.Box_Start_X.setValue(pos[0])
        self.form.Box_Start_Y.setValue(pos[1])
        self.form.Box_Start_Z.setValue(pos[2])
        App.Console.PrintMessage("x = {}\r\n".format(pos[0]))
        App.Console.PrintMessage("y = {}\r\n".format(pos[1]))
        App.Console.PrintMessage("z = {}\r\n".format(pos[2]))
        App.Console.PrintMessage("\r\n")


    def updateEndPos(self):
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
        self.form.Box_End_X.setValue(pos[0])
        self.form.Box_End_Y.setValue(pos[1])
        self.form.Box_End_Z.setValue(pos[2])
        App.Console.PrintMessage("x = {}\r\n".format(pos[0]))
        App.Console.PrintMessage("y = {}\r\n".format(pos[1]))
        App.Console.PrintMessage("z = {}\r\n".format(pos[2]))
        App.Console.PrintMessage("\r\n")

    

