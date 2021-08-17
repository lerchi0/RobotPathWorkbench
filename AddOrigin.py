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
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
import RPWlib
import RPWClasses
import getpass
path_to_ui = RPWlib.pathOfModule() + "/updateOrigin.ui"


class AddOrigin():

    def __init__(self):
        self.current = None
        self.form = Gui.PySideUic.loadUi(path_to_ui)
        self.reloadList()
        item = self.form.listWidget.item(0)
        self.form.listWidget.setCurrentRow(0)
        if (len(RPWlib.CSList.List) != 0):
            self.printItem(item)
        self.form.listWidget.itemClicked.connect(self.printItem)
        self.form.Button_Del.clicked.connect(lambda: self.deleteCS())
        self.form.Button_Save.clicked.connect(lambda: self.saveCS())
        self.form.Button_NewCS.clicked.connect(lambda: self.addCS())
        self.form.Button_SetPos.clicked.connect(lambda: self.setPos())
        self.form.Box_CS_X.valueChanged.connect(lambda: self.updateLCS())
        self.form.Box_CS_Y.valueChanged.connect(lambda: self.updateLCS())
        self.form.Box_CS_Z.valueChanged.connect(lambda: self.updateLCS())
        self.form.Box_CS_Yaw.valueChanged.connect(lambda: self.updateLCS())
        self.form.Box_CS_Pitch.valueChanged.connect(lambda: self.updateLCS())
        self.form.Box_CS_Roll.valueChanged.connect(lambda: self.updateLCS())
        self.form.Box_Combo_Parent.currentIndexChanged.connect(lambda: self.updateLCS())
        
        

    def printItem(self,item):
        self.form.Box_CS_X.blockSignals(True)
        self.form.Box_CS_Y.blockSignals(True)
        self.form.Box_CS_Z.blockSignals(True)
        self.form.Box_CS_Yaw.blockSignals(True)
        self.form.Box_CS_Pitch.blockSignals(True)
        self.form.Box_CS_Roll.blockSignals(True)
        self.form.Box_Combo_Parent.blockSignals(True)
        cs = RPWlib.CSList.List[self.form.listWidget.currentRow()]
        self.current =self.form.listWidget.currentRow()
        self.form.Box_Combo_Parent.clear()
        for idx, el in enumerate(RPWlib.CSList.List):
            self.form.Box_Combo_Parent.addItem(el.name)
        if cs.coordinateSystem != None:
            self.form.Box_Combo_Parent.setEnabled(False)
            self.form.Box_Combo_Parent.setCurrentIndex(cs.coordinateSystem)    
        else:
            self.form.Box_Combo_Parent.setPlaceholderText("None")
            self.form.Box_Combo_Parent.setCurrentIndex(-1)
            self.form.Box_Combo_Parent.setEnabled(False)
        self.form.Box_CS_ID.setText(str(cs.id))
        self.form.Box_CS_Name.setText(cs.name)
        self.form.Box_CS_X.setValue(cs.offsetPos["X"])
        self.form.Box_CS_Y.setValue(cs.offsetPos["Y"])
        self.form.Box_CS_Z.setValue(cs.offsetPos["Z"])
        self.form.Box_CS_Yaw.setValue(cs.offsetRot["yaw"])
        self.form.Box_CS_Pitch.setValue(cs.offsetRot["pitch"])
        self.form.Box_CS_Roll.setValue(cs.offsetRot["roll"])
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(App.ActiveDocument.Name,RPWlib.CSList.List[self.current].name)
        self.form.Box_CS_X.blockSignals(False)
        self.form.Box_CS_Y.blockSignals(False)
        self.form.Box_CS_Z.blockSignals(False)
        self.form.Box_CS_Yaw.blockSignals(False)
        self.form.Box_CS_Pitch.blockSignals(False)
        self.form.Box_CS_Roll.blockSignals(False)
        self.form.Box_Combo_Parent.blockSignals(False)
        self.updateLCS()
        
    def reloadList(self):
        self.form.listWidget.clear()
        for idx, el in enumerate(RPWlib.CSList.List):
            self.form.listWidget.addItem(el.name)

    def drawLCS(self, trafo):
        cs = RPWlib.CSList.List[self.current]
        
        cs.selfDraw(cs.name,1)
        

    def addCS(self):
        App.Console.PrintMessage("adding new CS")
        App.Console.PrintMessage("\r\n")
        parent = RPWlib.CSList.List[0].id
        _pos ={"X":0,"Y":0,"Z":0}
        _ori =  {"yaw":0,"pitch":0,"roll":0}
        cs = RPWClasses.CoordinateSystem(coordSystem= parent , csId= len(RPWlib.CSList.List),offsetPos= _pos, offsetRot= _ori)
        RPWlib.CSList.List.append(cs)
        
        self.reloadList()
        item = self.form.listWidget.item(len(RPWlib.CSList.List)-1)
        self.form.listWidget.setCurrentRow(len(RPWlib.CSList.List)-1)
        self.printItem(item)

    def deleteCS(self):
        doc = App.activeDocument()
        deletedPoint = RPWlib.CSList.List.pop(self.current)
        try:
            doc.removeObject(deletedPoint.name)
        except:
            App.Console.PrintMessage("no previous CS found")
            App.Console.PrintMessage("\r\n")
        App.Console.PrintMessage("Successfully deleted Point {}\r\n".format(deletedPoint))
        self.reloadList()
        item = self.form.listWidget.item(len(RPWlib.CSList.List)-1)
        self.form.listWidget.setCurrentRow(len(RPWlib.CSList.List)-1)
        self.printItem(item)


    def saveCS(self):
        self.form.Box_Combo_Parent.setEnabled(True)
        idxCS = self.form.Box_Combo_Parent.currentIndex()
        self.form.Box_Combo_Parent.setEnabled(False)
        if idxCS >= 0:
            cs = RPWlib.CSList.List[idxCS]
        else:
            cs = None
        RPWlib.CSList.List[self.current].name = self.form.Box_CS_Name.text()
        if cs != None:
            RPWlib.CSList.List[self.current].position["X"] = cs.position["X"] + self.form.Box_CS_X.value()
            RPWlib.CSList.List[self.current].position["Y"] = cs.position["Y"] + self.form.Box_CS_Y.value()
            RPWlib.CSList.List[self.current].position["Z"] = cs.position["Z"] + self.form.Box_CS_Z.value()
            RPWlib.CSList.List[self.current].orientation["yaw"] = cs.orientation["yaw"] + self.form.Box_CS_Yaw.value()
            RPWlib.CSList.List[self.current].orientation["pitch"] = cs.orientation["pitch"] + self.form.Box_CS_Pitch.value()
            RPWlib.CSList.List[self.current].orientation["roll"] = cs.orientation["roll"] + self.form.Box_CS_Roll.value()
            RPWlib.CSList.List[self.current].coordinateSystem = cs.id
        else:
            RPWlib.CSList.List[self.current].position["X"] = self.form.Box_CS_X.value()
            RPWlib.CSList.List[self.current].position["Y"] = self.form.Box_CS_Y.value()
            RPWlib.CSList.List[self.current].position["Z"] = self.form.Box_CS_Z.value()
            RPWlib.CSList.List[self.current].orientation["yaw"] = self.form.Box_CS_Yaw.value()
            RPWlib.CSList.List[self.current].orientation["pitch"] = self.form.Box_CS_Pitch.value()
            RPWlib.CSList.List[self.current].orientation["roll"] = self.form.Box_CS_Roll.value()
            RPWlib.CSList.List[self.current].coordinateSystem = cs
        RPWlib.CSList.List[self.current].offsetPos["X"] = self.form.Box_CS_X.value()
        RPWlib.CSList.List[self.current].offsetPos["Y"] = self.form.Box_CS_Y.value()
        RPWlib.CSList.List[self.current].offsetPos["Z"] = self.form.Box_CS_Z.value()
        RPWlib.CSList.List[self.current].offsetRot["yaw"] = self.form.Box_CS_Yaw.value()
        RPWlib.CSList.List[self.current].offsetRot["pitch"] = self.form.Box_CS_Pitch.value()
        RPWlib.CSList.List[self.current].offsetRot["roll"] = self.form.Box_CS_Roll.value()
        
        self.reloadList()

    def updateLCS(self):
        self.saveCS()        
        trafo = RPWlib.CSList.List[self.current].getTotalTransform()
        self.drawLCS(trafo)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(App.ActiveDocument.Name,RPWlib.CSList.List[self.current].name)

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
            App.Console.PrintMessage("x = {}\r\n".format(pos[0]))
            App.Console.PrintMessage("y = {}\r\n".format(pos[1]))
            App.Console.PrintMessage("z = {}\r\n".format(pos[2]))
            App.Console.PrintMessage("\r\n")
        elif (element_.ShapeType == "Face"):
            pos = element_.BoundBox.Center
            normalVect = element_.normalAt(0,0)
            ori = [0,0,0]
            App.Console.PrintMessage("x = {}\r\n".format(pos[0]))
            App.Console.PrintMessage("y = {}\r\n".format(pos[1]))
            App.Console.PrintMessage("z = {}\r\n".format(pos[2]))
            App.Console.PrintMessage("normal Vector = {}\r\n".format(normalVect))
            App.Console.PrintMessage("\r\n")
        elif (element_.ShapeType == "Edge"):
            startPoint = element_.Vertexes[0]
            endPoint = element_.Vertexes[1]
            direction = endPoint.Point - startPoint.Point
            pos = startPoint.Point + 0.5*direction
            ori = [0,0,0]
            App.Console.PrintMessage("start = {}\r\n".format(startPoint.Point))
            App.Console.PrintMessage("end = {}\r\n".format(endPoint.Point))
            App.Console.PrintMessage("center = {}\r\n".format(pos))
            App.Console.PrintMessage("direction = {}\r\n".format(direction))
        self.form.Box_Combo_Parent.setEnabled(True)
        idxCS = self.form.Box_Combo_Parent.currentIndex()
        self.form.Box_Combo_Parent.setEnabled(False)
        if idxCS >= 0:
            posCS = [RPWlib.CSList.List[idxCS].position["X"],RPWlib.CSList.List[idxCS].position["Y"],RPWlib.CSList.List[idxCS].position["Z"]]
            oriCS = [RPWlib.CSList.List[idxCS].orientation["yaw"],RPWlib.CSList.List[idxCS].orientation["pitch"],RPWlib.CSList.List[idxCS].orientation["roll"]]
        else:
            posCS = [0,0,0]
            oriCS = [0,0,0]
           
        self.form.Box_CS_X.setValue(pos[0] - posCS[0])
        self.form.Box_CS_Y.setValue(pos[1] - posCS[1])
        self.form.Box_CS_Z.setValue(pos[2] - posCS[2])
        self.form.Box_CS_Yaw.setValue(ori[0] - oriCS[0])
        self.form.Box_CS_Pitch.setValue(ori[1] - oriCS[1])
        self.form.Box_CS_Roll.setValue(ori[2] - oriCS[2])
        self.updateLCS()


    def accept(self):
        self.saveCS()
        user = getpass.getuser()
        RPWlib.writeCSFile(RPWlib.CSList.List, user)
        return True

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
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_newOrigin_icon.svg", # the name of a svg file available in the resources
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
