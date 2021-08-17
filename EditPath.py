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
from PySide import QtGui, QtCore
import RPWlib
import getpass
import Movements

path_to_ui = RPWlib.pathOfModule() + "/editPath.ui"
class EditPath():

    def __init__(self):
        self.form = Gui.PySideUic.loadUi(path_to_ui)
        self.form.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        for i,j in enumerate(RPWlib.MovementList.List):
            self.form.listWidget.addItem(j.name)
        
        for idx,p in enumerate(RPWlib.PointsList.List):
            self.form.Combo_Box_Start.addItem("Point_{}".format(idx))
            self.form.Combo_Box_Mid.addItem("Point_{}".format(idx))
            self.form.Combo_Box_End.addItem("Point_{}".format(idx))
        self.current = 0
        item = self.form.listWidget.item(0)
        self.form.listWidget.setCurrentRow(0)
        if (len(RPWlib.MovementList.List) != 0):
            self.highlightSegment(item)
        self.updateSpeed()
        self.form.listWidget.itemPressed.connect(self.highlightSegment)
        self.form.Combo_Box_Start.currentIndexChanged.connect(lambda: self.saveCurrentMovement())
        self.form.Combo_Box_Mid.currentIndexChanged.connect(lambda: self.saveCurrentMovement())
        self.form.Combo_Box_End.currentIndexChanged.connect(lambda: self.saveCurrentMovement())
        self.form.Box_Seg_Name.returnPressed.connect(lambda: self.saveCurrentMovement())
        self.form.Btn_Move_Up.clicked.connect(lambda: self.moveItemUp())
        self.form.Btn_Move_Down.clicked.connect(lambda: self.moveItemDown())
        self.form.Slider_Seg_Speed.valueChanged.connect(lambda: self.updateSpeed())
        self.form.Btn_Del.clicked.connect(lambda: self.deleteSegment())
        self.form.Btn_Action.clicked.connect(lambda: self.addAction())

    def deleteSegment(self):
        try:
            App.ActiveDocument.removeObject(RPWlib.MovementList.List[self.current].name)
        except:
            pass
        try:
            RPWlib.MovementList.List.pop(self.current)
        except Exception as e:
            App.Console.PrintMessage("\r\n{}\r\n".format(e))
        if (len(RPWlib.MovementList.List) != 0):
            newID = self.current - 1
            self.reloadList()
            temp = self.saveMovements()
            RPWlib.MovementList.List = temp
            item = self.form.listWidget.item(newID)
            self.form.listWidget.setCurrentRow(newID)
            self.highlightSegment(item)
        

    def addAction(self):
        id = len(RPWlib.MovementList.List)
        action = Movements.Action(id, "RENAME ME","")
        RPWlib.MovementList.List.append(action)
        self.reloadList()
        self.current = id
        item = self.form.listWidget.item(self.current)
        self.form.listWidget.setCurrentRow(self.current)
        App.Console.PrintMessage(item)
        
        self.highlightSegment(item)
       

    def highlightSegment(self,item):
        self.form.Combo_Box_Start.blockSignals(True)
        self.form.Combo_Box_Mid.blockSignals(True)
        self.form.Combo_Box_End.blockSignals(True)
        self.form.Slider_Seg_Speed.blockSignals(True)
        
        try:
            self.current = self.form.listWidget.currentRow()
            self.currentName = item.text()
        except Exception as e:
            App.Console.PrintError(f"Error: {e}")
        
        movement = RPWlib.MovementList.List[self.current]
        self.form.Box_Seg_Name.setText(movement.name)
        self.form.Disp_Seg_Speed.setText("{} %".format(movement.speed))
        self.form.Slider_Seg_Speed.setValue(movement.speed)
        self.form.Btn_Move_Up.setEnabled(True)
        self.form.Btn_Move_Down.setEnabled(True)
        self.form.Combo_Box_Start.setEnabled(True)
        self.form.Combo_Box_Mid.setEnabled(True)
        self.form.Combo_Box_End.setEnabled(True)
        self.form.Slider_Seg_Speed.setEnabled(True)
        if movement.id == 0:
            self.form.Btn_Move_Up.setEnabled(False)
        elif movement.id == len(RPWlib.MovementList.List)-1:
            self.form.Btn_Move_Down.setEnabled(False)
        
        if movement.type == "Action":
            self.form.Combo_Box_Start.setPlaceholderText("None")
            self.form.Combo_Box_Start.setCurrentIndex(-1)
            self.form.Combo_Box_Start.setEnabled(False)
            self.form.Combo_Box_Mid.setPlaceholderText("None")
            self.form.Combo_Box_Mid.setCurrentIndex(-1)
            self.form.Combo_Box_Mid.setEnabled(False)
            self.form.Combo_Box_End.setPlaceholderText("None")
            self.form.Combo_Box_End.setCurrentIndex(-1)
            self.form.Combo_Box_End.setEnabled(False)
            self.form.Slider_Seg_Speed.setEnabled(False)
        else:

            
            
            self.form.Combo_Box_Start.setCurrentIndex(movement.startPoint["id"])
            self.form.Combo_Box_End.setCurrentIndex(movement.endPoint["id"])
            
            if movement.type == "Circular":
                self.form.Combo_Box_Mid.setCurrentIndex(movement.midPoint["id"])
            else:
                self.form.Combo_Box_Mid.setPlaceholderText("None")
                self.form.Combo_Box_Mid.setCurrentIndex(-1)
                self.form.Combo_Box_Mid.setEnabled(False)
        
        try:
            Gui.Selection.clearSelection()
            Gui.Selection.addSelection(App.ActiveDocument.Name,self.currentName)
        except:
            pass
        self.form.Combo_Box_Start.blockSignals(False)
        self.form.Combo_Box_Mid.blockSignals(False)
        self.form.Combo_Box_End.blockSignals(False)
        self.form.Slider_Seg_Speed.blockSignals(False)

    def moveItemUp(self):
        self.current = self.form.listWidget.currentRow()
        newPos = self.current -1
        currentMovement = RPWlib.MovementList.List[self.current]
        otherMovement = RPWlib.MovementList.List[newPos]
        currentMovement.id = newPos
        otherMovement.id = self.current
        RPWlib.MovementList.List[self.current] = otherMovement
        RPWlib.MovementList.List[newPos] = currentMovement
        self.reloadList()
        self.form.listWidget.setCurrentRow(newPos)
        self.current = newPos
        self.highlightSegment(item=self.form.listWidget.item(newPos))
        
    def updateSpeed(self):
        speed = self.form.Slider_Seg_Speed.value()
        self.form.Disp_Seg_Speed.setText(f"{speed} %")
    def moveItemDown(self):
        self.current = self.form.listWidget.currentRow()
        newPos = self.current +1
        currentMovement = RPWlib.MovementList.List[self.current]
        otherMovement = RPWlib.MovementList.List[newPos]
        currentMovement.id = newPos
        otherMovement.id = self.current
        RPWlib.MovementList.List[self.current] = otherMovement
        RPWlib.MovementList.List[newPos] = currentMovement
        self.reloadList()
        self.form.listWidget.setCurrentRow(newPos)
        self.current = newPos
        self.highlightSegment(item=self.form.listWidget.item(newPos))


    def reloadList(self):
        self.form.listWidget.clear()
        for val in RPWlib.MovementList.List:
            self.form.listWidget.addItem(val.name)
        self.form.listWidget.setCurrentRow(self.current)


    def accept(self):
        if len(RPWlib.MovementList.List) != 0:
            newList = self.saveMovements()
            RPWlib.MovementList.List = newList
            self.saveCurrentMovement()
        user = getpass.getuser()
        RPWlib.writeMovementsFile(RPWlib.MovementList.List, user)
        return True
    
    
    def dropEvent(self):
        App.Console.PrintMessage("Dropped")
        newList = self.saveMovements()
        App.Console.PrintMessage("sorted")
        RPWlib.MovementList.List = newList
        App.Console.PrintMessage("saved")
        self.highlightSegment(self.form.listWidget.currentItem())

    def saveCurrentMovement(self):
        idx = self.form.listWidget.currentRow()
        startPoint = RPWlib.PointsList.List[self.form.Combo_Box_Start.currentIndex()]
        endPoint = RPWlib.PointsList.List[self.form.Combo_Box_End.currentIndex()]
        speed = self.form.Slider_Seg_Speed.value()
        name = self.form.Box_Seg_Name.text()
        if name == "" or name == " ":
            diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, 'Error in macro MessageBox', "Name of Segment must not be empty\n\r"
                "(Segment ID: {}, Previous Name: {})".format(idx, RPWlib.MovementList.List[idx].name))
            diag.setWindowModality(QtCore.Qt.ApplicationModal)
            diag.exec_()
            return
        sPoint = {
            "id": self.form.Combo_Box_Start.currentIndex(),
            "position" : startPoint.position,
            "orientation" : startPoint.orientation,
            "coordinateSystem" : startPoint.coordinateSystem,
        }
        ePoint = {
            "id": self.form.Combo_Box_End.currentIndex(),
            "position" : endPoint.position,
            "orientation" : endPoint.orientation,
            "coordinateSystem" : endPoint.coordinateSystem,
        }
        if RPWlib.MovementList.List[idx].type == "Circular":
            midPoint = RPWlib.PointsList.List[self.form.Combo_Box_Mid.currentIndex()]

            mPoint = {
                "id": self.form.Combo_Box_Mid.currentIndex(),
                "position" : midPoint.position,
                "orientation" : midPoint.orientation,
                "coordinateSystem" : midPoint.coordinateSystem,
            }
            RPWlib.MovementList.List[idx] = Movements.CircularMovement(idx,sPoint,mPoint,ePoint,
                    speed,
                    name,
                    RPWlib.MovementList.List[idx].label)
        elif RPWlib.MovementList.List[idx].type == "P2P":
            RPWlib.MovementList.List[idx] = Movements.P2PMovement(idx,sPoint,ePoint,
                    speed,
                    name,
                    RPWlib.MovementList.List[idx].label)
        elif RPWlib.MovementList.List[idx].type == "Linear":
            RPWlib.MovementList.List[idx] = Movements.LinearMovement(idx,sPoint,ePoint,
                    speed,
                    name,
                    RPWlib.MovementList.List[idx].label)
        elif RPWlib.MovementList.List[idx].type == "Action":
            RPWlib.MovementList.List[idx] = Movements.Action(idx,name,RPWlib.MovementList.List[idx].label)
        RPWlib.MovementList.List[idx].selfdraw()
        self.reloadList()
        

    def saveMovements(self):
        TempList = []
        for idx in range(self.form.listWidget.count()):
            curSeg = self.form.listWidget.item(idx)
            curSegName = curSeg.text()
            for i,j in enumerate(RPWlib.MovementList.List):
                if j.name == curSegName:
                    j.id = idx
                    TempList.append(j)
                    break
        return TempList


class EditPathCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_newModule_icon.svg", # the name of a svg file available in the resources
                #'Accel' : "", # a default shortcut (optional)
                'MenuText': "Show and Edit Path",
                'ToolTip' : "Show Path"}

    def Activated(self):
        panelMod = EditPath()
        Gui.Control.showDialog(panelMod)
        return True

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True
    def Deactivated(self):
        pass



Gui.addCommand("Edit_Path_Command",EditPathCmd())
