import FreeCADGui as Gui
import FreeCAD as App
from PySide2 import QtGui
from PySide import QtGui as QGui 
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
import RPWlib
import RPWClasses
import getpass
path_to_ui = RPWlib.pathOfModule() + "/pointsView.ui"


class AddPoints():
    def __init__(self):
        self.current = 0
        self.form = Gui.PySideUic.loadUi(path_to_ui)
        self.reloadList()
        for cs in RPWlib.CSList.List:
            self.form.Box_Combo_CS.addItem(cs.name)
        item = self.form.listWidget.item(0)
        self.form.listWidget.setCurrentRow(0)
        if (len(RPWlib.PointsList.List) != 0):
            self.printItem(item)
        self.form.listWidget.itemClicked.connect(self.printItem)
        self.form.Button_Del.clicked.connect(lambda: self.deletePoint())
        self.form.Button_Save.clicked.connect(lambda: self.savePoint())
        self.form.Button_AddPoint.clicked.connect(lambda: self.addPoint())
        self.form.Button_SetPos.clicked.connect(lambda: self.setPos())
        
        self.form.Box_Point_X.valueChanged.connect(lambda: self.updateSphere())
        self.form.Box_Point_Y.valueChanged.connect(lambda: self.updateSphere())
        self.form.Box_Point_Z.valueChanged.connect(lambda: self.updateSphere())
        self.form.Box_Point_Yaw.valueChanged.connect(lambda: self.updateSphere())
        self.form.Box_Point_Pitch.valueChanged.connect(lambda: self.updateSphere())
        self.form.Box_Point_Roll.valueChanged.connect(lambda: self.updateSphere())
        self.form.Box_Combo_CS.currentIndexChanged.connect(lambda: self.updateSphere())

    
    def reloadList(self):
        self.form.listWidget.clear()
        for idx, val in enumerate(RPWlib.PointsList.List):
            self.form.listWidget.addItem(str(idx))
        self.form.listWidget.setCurrentRow(self.current)
            
    def printItem(self,item):
        self.form.Box_Point_X.blockSignals(True)
        self.form.Box_Point_Y.blockSignals(True)
        self.form.Box_Point_Z.blockSignals(True)
        self.form.Box_Point_Yaw.blockSignals(True)
        self.form.Box_Point_Pitch.blockSignals(True)
        self.form.Box_Point_Roll.blockSignals(True)
        self.form.Box_Combo_CS.blockSignals(True)
        self.current = self.form.listWidget.currentRow()
        point = RPWlib.PointsList.List[self.form.listWidget.currentRow()]
        index = next((i for i, item in enumerate(RPWlib.CSList.List) if item.id == point.coordinateSystem), None)
        self.form.Box_Combo_CS.setCurrentIndex(index)
        self.form.Box_Point_ID.setText(str(self.form.listWidget.currentRow()))
        self.form.Box_Point_X.setValue(point.offsetPos["X"])
        self.form.Box_Point_Y.setValue(point.offsetPos["Y"])
        self.form.Box_Point_Z.setValue(point.offsetPos["Z"])
        self.form.Box_Point_Yaw.setValue(point.offsetRot["yaw"])
        self.form.Box_Point_Pitch.setValue(point.offsetRot["pitch"])
        self.form.Box_Point_Roll.setValue(point.offsetRot["roll"])
        self.form.Box_Point_X.blockSignals(False)
        self.form.Box_Point_Y.blockSignals(False)
        self.form.Box_Point_Z.blockSignals(False)
        self.form.Box_Point_Yaw.blockSignals(False)
        self.form.Box_Point_Pitch.blockSignals(False)
        self.form.Box_Point_Roll.blockSignals(False)
        self.form.Box_Combo_CS.blockSignals(False)
        self.updateSphere()
        

    def drawSphere(self, trafo):
        RPWClasses.Pathpoint.draw("Point_{}".format(self.current),2,trafo)

    def addPoint(self):
        idxCS = self.form.Box_Combo_CS.currentIndex()
        defaultCS = RPWlib.CSList.List[idxCS]
        RPWlib.PointsList.List.append(RPWClasses.Pathpoint(offsetPos= {"X":0,"Y":0,"Z":0}, offsetRot= {"yaw":0,"pitch":0,"roll":0}, coordSystem=idxCS))
        self.reloadList()
        item = self.form.listWidget.item(len(RPWlib.PointsList.List)-1)
        self.form.listWidget.setCurrentRow(len(RPWlib.PointsList.List)-1)
        self.printItem(item)
        self.updateSphere()

    def deletePoint(self):
        doc = App.activeDocument()
        deletedPoint = RPWlib.PointsList.List.pop(self.current)
        try:
            doc.removeObject("Point_{}".format(self.current))
        except:
            App.Console.PrintMessage("no previous CS found")
            App.Console.PrintMessage("\r\n")
        App.Console.PrintMessage("Successfully deleted Point {}\r\n".format(deletedPoint))
        self.reloadList()
        if (len(RPWlib.PointsList.List) != 0):
            item = self.form.listWidget.item(len(RPWlib.PointsList.List)-1)
            self.form.listWidget.setCurrentRow(len(RPWlib.PointsList.List)-1)
            self.printItem(item)

    def savePoint(self):
        if (len(RPWlib.PointsList.List) != 0):
            idxCS = self.form.Box_Combo_CS.currentIndex()
            cs = RPWlib.CSList.List[idxCS]
            RPWlib.PointsList.List[self.current].offsetPos["X"] = self.form.Box_Point_X.value()
            RPWlib.PointsList.List[self.current].position["X"] = cs.position["X"] + self.form.Box_Point_X.value()
            RPWlib.PointsList.List[self.current].offsetPos["Y"] = self.form.Box_Point_Y.value()
            RPWlib.PointsList.List[self.current].position["Y"] = cs.position["Y"] + self.form.Box_Point_Y.value()
            RPWlib.PointsList.List[self.current].offsetPos["Z"] = self.form.Box_Point_Z.value()
            RPWlib.PointsList.List[self.current].position["Z"] = cs.position["Z"] + self.form.Box_Point_Z.value()
            RPWlib.PointsList.List[self.current].offsetRot["yaw"] = self.form.Box_Point_Yaw.value()
            RPWlib.PointsList.List[self.current].orientation["yaw"] = cs.orientation["yaw"] + self.form.Box_Point_Yaw.value()
            RPWlib.PointsList.List[self.current].offsetRot["pitch"] = self.form.Box_Point_Pitch.value()
            RPWlib.PointsList.List[self.current].orientation["pitch"] = cs.orientation["pitch"] + self.form.Box_Point_Pitch.value()
            RPWlib.PointsList.List[self.current].offsetRot["roll"] = self.form.Box_Point_Roll.value()
            RPWlib.PointsList.List[self.current].orientation["roll"] = cs.orientation["roll"] + self.form.Box_Point_Roll.value()
            RPWlib.PointsList.List[self.current].coordinateSystem = idxCS
        self.reloadList()

    def updateSphere(self):
        self.current = self.form.listWidget.currentRow()
        self.savePoint()        
        if (len(RPWlib.PointsList.List) != 0):
            trafo = RPWlib.PointsList.List[self.current].getTotalTransform()
            self.drawSphere(trafo)
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(App.ActiveDocument.Name,"Point_{}".format(self.current))


    def setPos(self):
        sel = Gui.Selection.getSelection()   
        mydoc = App.activeDocument().Name
        document_ = mydoc
        global movementId
        global movementList
        try:
            object_Label = sel[0].Label
            object_Name  = sel[0].Name
        except Exception:
            object_Label = ""
            object_Name  = ""
        try:
            SubElement = Gui.Selection.getSelectionEx()[0]   
            element_ = SubElement.SubObjects[0]
        except Exception:
            element_ = ""
        App.Console.PrintMessage("Type: {}\r\n".format(element_.ShapeType))
        if (element_.ShapeType == "Vertex"):
            pos = element_.Point
            ori = [0,0,0]
        elif (element_.ShapeType == "Face"):
            pos = element_.BoundBox.Center
            normalVect = element_.normalAt(0,0)
            ori = [0,0,0]
        elif (element_.ShapeType == "Edge"):
            startPoint = element_.Vertexes[0]
            endPoint = element_.Vertexes[1]
            direction = endPoint.Point - startPoint.Point
            pos = startPoint.Point + 0.5*direction
            ori = [0,0,0]
        idxCS = self.form.Box_Combo_CS.currentIndex()
        posCS = [RPWlib.CSList.List[idxCS].position["X"],RPWlib.CSList.List[idxCS].position["Y"],RPWlib.CSList.List[idxCS].position["Z"]]
        oriCS = [RPWlib.CSList.List[idxCS].orientation["yaw"],RPWlib.CSList.List[idxCS].orientation["pitch"],RPWlib.CSList.List[idxCS].orientation["roll"]]

        self.form.Box_Point_X.setValue(pos[0] - posCS[0])
        self.form.Box_Point_Y.setValue(pos[1] - posCS[1])
        self.form.Box_Point_Z.setValue(pos[2] - posCS[2])
        self.form.Box_Point_Yaw.setValue(ori[0] - oriCS[0])
        self.form.Box_Point_Pitch.setValue(ori[1] - oriCS[1])
        self.form.Box_Point_Roll.setValue(ori[2] - oriCS[2])
        self.updateSphere()

    def accept(self):
        if (len(RPWlib.PointsList.List) != 0):
            self.savePoint()
        doc = App.activeDocument()
        user = getpass.getuser()
        RPWlib.writePointsFile(RPWlib.PointsList.List, user)
        return True


class AddPointsCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_newPose_icon.svg", # the name of a svg file available in the resources
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
