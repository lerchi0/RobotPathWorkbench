import FreeCADGui as Gui
import FreeCAD as App
import Part
from PySide2 import QtGui
from PySide import QtGui as QGui 
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
import RPWlib


path_to_ui = RPWlib.pathOfModule() + "/newModul.ui"
class AddModule():
    
    # Ablauf:
    #           - sollen bestehende geladen werden?
    #           - Ursprungs KS wählen
    #           - Punkte definieren
    #           - Pfade definieren
    #           - abspeichern für mehrmalige Verwendung 



    def __init__(self):
        self.form = Gui.PySideUic.loadUi(path_to_ui)

    def accept(self):
        return True


class AddModuleCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_newModule_icon.svg", # the name of a svg file available in the resources
                'Accel' : "", # a default shortcut (optional)
                'MenuText': "Add Standard Module to the Model",
                'ToolTip' : "Add Module"}

    def Activated(self):
        panelMod = AddModule()
        Gui.Control.showDialog(panelMod)
        return True

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True
    def Deactivated(self):
        pass



Gui.addCommand('Add_New_Module_Command',AddModuleCmd())
