import FreeCADGui as Gui
import FreeCAD as App
import Part
from PySide import QtGui
import RPWlib
import getpass

path_to_ui = RPWlib.pathOfModule() + "/editPath.ui"
class EditPath():
    
    # Ablauf:
    #           - sollen bestehende geladen werden?
    #           - Ursprungs KS wählen
    #           - Punkte definieren
    #           - Pfade definieren
    #           - abspeichern für mehrmalige Verwendung 



    def __init__(self):
        self.form = Gui.PySideUic.loadUi(path_to_ui)
        self.form.listWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        for i,j in enumerate(RPWlib.MovementList.List):
            self.form.listWidget.addItem(j["name"])
        self.form.listWidget.itemClicked.connect(self.highlightSegment)

    def highlightSegment(self,item):
        try:
            self.current = self.form.listWidget.currentRow()
            self.currentName = item.text()
            App.Console.PrintMessage("Index: {}; Item: {}\r\n".format(self.current, self.currentName))
        except Exception as e:
            App.Console.PrintMessage(e)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(App.ActiveDocument.Name,self.currentName)
    def accept(self):
        TempList = []
        for idx in range(self.form.listWidget.count()):
            curSeg = self.form.listWidget.item(idx)
            curSegName = curSeg.text()
            for i,j in enumerate(RPWlib.MovementList.List):
                if j["name"] == curSegName:
                    TempList.append(j)
        RPWlib.MovementList.List = TempList
        user = getpass.getuser()
        RPWlib.writeMovementsFile(RPWlib.MovementList.List, user )
        return True



class ShowPathCmd():
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



Gui.addCommand("Edit_Path_Command",ShowPathCmd())
