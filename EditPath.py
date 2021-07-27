from Movements import Movement
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtGui
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
        self.form.listWidget.itemPressed.connect(self.highlightSegment)
        self.form.Combo_Box_Start.currentIndexChanged.connect(lambda: self.saveCurrentMovement())
        self.form.Combo_Box_Mid.currentIndexChanged.connect(lambda: self.saveCurrentMovement())
        self.form.Combo_Box_End.currentIndexChanged.connect(lambda: self.saveCurrentMovement())
        self.form.Btn_Move_Up.clicked.connect(lambda: self.moveItemUp())
        self.form.Btn_Move_Down.clicked.connect(lambda: self.moveItemDown())

    def highlightSegment(self,item):
        self.form.Combo_Box_Start.blockSignals(True)
        self.form.Combo_Box_Mid.blockSignals(True)
        self.form.Combo_Box_End.blockSignals(True)
        try:
            self.current = self.form.listWidget.currentRow()
            self.currentName = item.text()
            movement = RPWlib.MovementList.List[self.current]
        except Exception as e:
            App.Console.PrintMessage(e)
        self.form.Box_Seg_Name.setText(movement.name)
        self.form.Combo_Box_Start.setCurrentIndex(movement.startPoint["id"])
        self.form.Combo_Box_End.setCurrentIndex(movement.endPoint["id"])
        self.form.Btn_Move_Up.setEnabled(True)
        self.form.Btn_Move_Down.setEnabled(True)
        if movement.id == 0:
            self.form.Btn_Move_Up.setEnabled(False)
        elif movement.id == len(RPWlib.MovementList.List)-1:
            self.form.Btn_Move_Down.setEnabled(False)

        if movement.type == "Circular":
            self.form.Combo_Box_Mid.setEnabled(True)
            self.form.Combo_Box_Mid.setCurrentIndex(movement.midPoint["id"])
        else:
            self.form.Combo_Box_Mid.setEnabled(False)
        
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(App.ActiveDocument.Name,self.currentName)

        self.form.Combo_Box_Start.blockSignals(False)
        self.form.Combo_Box_Mid.blockSignals(False)
        self.form.Combo_Box_End.blockSignals(False)

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
        for idx, val in enumerate(RPWlib.MovementList.List):
            self.form.listWidget.addItem(val.name)
        self.form.listWidget.setCurrentRow(self.current)


    def accept(self):
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
                    RPWlib.MovementList.List[idx].speed,
                    RPWlib.MovementList.List[idx].name,
                    RPWlib.MovementList.List[idx].label)
            RPWlib.MovementList.List[idx].selfdraw()
        elif RPWlib.MovementList.List[idx].type == "P2P":
            RPWlib.MovementList.List[idx] = Movements.P2PMovement(idx,sPoint,ePoint,
                    RPWlib.MovementList.List[idx].speed,
                    RPWlib.MovementList.List[idx].name,
                    RPWlib.MovementList.List[idx].label)
            RPWlib.MovementList.List[idx].selfdraw()
        elif RPWlib.MovementList.List[idx].type == "Linear":
            RPWlib.MovementList.List[idx] = Movements.LinearMovement(idx,sPoint,ePoint,
                    RPWlib.MovementList.List[idx].speed,
                    RPWlib.MovementList.List[idx].name,
                    RPWlib.MovementList.List[idx].label)
            RPWlib.MovementList.List[idx].selfdraw()

        

    def saveMovements(self):
        TempList = []
        for idx in range(self.form.listWidget.count()):
            curSeg = self.form.listWidget.item(idx)
            curSegName = curSeg.text()
            for i,j in enumerate(RPWlib.MovementList.List):
                if j.name == curSegName:
                    j.id = idx
                    TempList.append(j)
                    App.Console.PrintMessage("ID: {}, Name: {}\r\n".format(j.id, j.name))
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
