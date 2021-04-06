import FreeCADGui as Gui
import FreeCAD as App
import Part
from PySide import QtGui
from PySide import QtCore
from PySide.QtUiTools import QUiLoader
import os
import RPWlib
import Movements
import json
path_to_ui = "C:/Users/t-ler/AppData/Roaming/FreeCAD/Mod/RobotPathWorkbench//createLinSegDialog.ui"


class CreateLinSeg():

    def __init__(self):
        # self.ui_path = RPWlib.pathOfModule() + "/createLinSegDialog.ui"
        # self.form = Gui.PySideUic.loadUi(self.ui_path)
        # self.form.setWindowTitle("Create Linear Segment")
        # self.form.pushButton_CreateSegment.clicked.connect(lambda:self.createLinPath())
        # self.form.pushButton_updateStartPos.clicked.connect(lambda:self.updateStartPos())
        # self.form.pushButton_updateEndPos.clicked.connect(lambda:self.updateEndPos())
        # self.form.closeBtn.clicked.connect(lambda:self.close())
        self.form = Gui.PySideUic.loadUi(path_to_ui)

    def accept(self):
        global movementId
        global movementList
        doc = App.activeDocument()
        startPoint = [self.form.Box_Start_X.value(), self.form.Box_Start_Y.value(), self.form.Box_Start_Z.value()]
        endPoint = [self.form.Box_End_X.value(), self.form.Box_End_Y.value(), self.form.Box_End_Z.value()]

        movementList.append(Movements.LinearMovement(id= movementId,sPoint=startPoint, ePoint= endPoint).__dict__)
        movementId = movementId +1
        fullpath = doc.FileName
        index = fullpath.rfind("/")
        path = fullpath[:index+1]
        savepath = path +"Test.json"
        with open(savepath, 'w') as outfile:
            json.dump(movementList, outfile, indent=4)

        Gui.Control.closeDialog()

    def createLinPath(self):
        startX = self.form.StartpointX.value()
        startY = self.form.StartpointY.value()
        startZ = self.form.StartpointZ.value()

        endX = self.form.EndpointX.value()
        endY = self.form.EndpointY.value()
        endZ = self.form.EndpointZ.value()

        strLabel = f"Created linear Path from ({startX},{startY},{startZ}) to ({endX},{endY},{endZ})"
        self.form.resultLabel.setText(strLabel)
        
        App.Console.PrintMessage(strLabel)
        
        

    def close(self):
        self.form.close()

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
        
        App.Console.PrintMessage("x = {}\r\n".format(pos[0]))
        App.Console.PrintMessage("y = {}\r\n".format(pos[1]))
        App.Console.PrintMessage("z = {}\r\n".format(pos[2]))
        App.Console.PrintMessage("\r\n")


        #pad = Gui.Selection.getSelection()
        #[x,y,z] = pad.PickedPoints[0]
        #self.form.StartpointX.setValue(x)
        #self.form.StartpointY.setValue(y)
        #self.form.StartpointZ.setValue(z)

    def updateEndPos(self):
        pad = Gui.Selection.getSelection()
        [x,y,z] = pad.PickedPoints[0]
        self.form.EndpointX.setValue(x)
        self.form.EndpointY.setValue(y)
        self.form.EndpointZ.setValue(z)

    

