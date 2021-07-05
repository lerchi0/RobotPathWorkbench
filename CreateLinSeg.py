import FreeCADGui as Gui
import FreeCAD as App
import Part
import os
import RPWlib
import Movements
import json
import getpass
path_to_ui = RPWlib.pathOfModule() + "/createLinSegDialog.ui"


class CreateLinSeg():

    def __init__(self):
        self.form = Gui.PySideUic.loadUi(path_to_ui)
        for idx, point in enumerate(RPWlib.PointsList.List):
            self.form.Box_Combo_Start.addItem("Point {}".format(idx))
            self.form.Box_Combo_End.addItem("Point {}".format(idx))
        self.updateStart()
        self.updateEnd()
        self.form.Box_Combo_Start.currentIndexChanged.connect(lambda: self.updateStart())
        self.form.Box_Combo_End.currentIndexChanged.connect(lambda: self.updateEnd())

    def updateStart(self):
        point = RPWlib.PointsList.List[self.form.Box_Combo_Start.currentIndex()]
        self.form.Text_Start_X.setText(str(point["position"]["X"]))
        self.form.Text_Start_Y.setText(str(point["position"]["Y"]))
        self.form.Text_Start_Z.setText(str(point["position"]["Z"]))
        self.form.Text_Start_Yaw.setText(str(point["orientation"]["yaw"]))
        self.form.Text_Start_Pitch.setText(str(point["orientation"]["pitch"]))
        self.form.Text_Start_Roll.setText(str(point["orientation"]["roll"]))
    def updateEnd(self):
        point = RPWlib.PointsList.List[self.form.Box_Combo_End.currentIndex()]
        self.form.Text_End_Y.setText(str(point["position"]["Y"]))
        self.form.Text_End_X.setText(str(point["position"]["X"]))
        self.form.Text_End_Z.setText(str(point["position"]["Z"]))
        self.form.Text_End_Yaw.setText(str(point["orientation"]["yaw"]))
        self.form.Text_End_Pitch.setText(str(point["orientation"]["pitch"]))
        self.form.Text_End_Roll.setText(str(point["orientation"]["roll"]))

    def accept(self):
        name = self.form.Box_Seg_Name.text()
        startPoint =RPWlib.PointsList.List[self.form.Box_Combo_Start.currentIndex()]
        endPoint = RPWlib.PointsList.List[self.form.Box_Combo_End.currentIndex()]
        start = App.Vector(startPoint["position"]["X"], startPoint["position"]["Y"], startPoint["position"]["Z"])
        end   = App.Vector(endPoint["position"]["X"], endPoint["position"]["Y"], endPoint["position"]["Z"])
        label = self.form.Box_Seg_Note.toPlainText()
        Movements.LinearMovement.draw(start, end,name)
        sPoint = {
            "position" : startPoint["position"],
            "orientation" : startPoint["orientation"],
            "coordinateSystem" : startPoint["coordinateSystem"]["id"],
        }
        
        ePoint = {
            "position" : endPoint["position"],
            "orientation" : endPoint["orientation"],
            "coordinateSystem" : endPoint["coordinateSystem"]["id"],
        }
        
        RPWlib.MovementList.List.append(Movements.LinearMovement(sPoint=sPoint, ePoint= ePoint,name=name,label= label).__dict__)
        RPWlib.MovementList.currentId = RPWlib.MovementList.currentId + 1
        user = getpass.getuser()
        RPWlib.writeMovementsFile(RPWlib.MovementList.List, user )
        return True

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

    

