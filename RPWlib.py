
import os
import Movements
import PySide2
import json
import FreeCADGui as Gui
import FreeCAD as App


def pathOfModule():
    return os.path.dirname(__file__)


def reloadMovementList():
    doc = App.activeDocument()
    try:
        fullpath = doc.FileName
        index = fullpath.rfind("/")
        path = fullpath[:index+1]
    except:
        path = pathOfModule()
    MovementList.pathToFile, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the json File with the Movements",  path, "json files  (*.json);;")
    App.Console.PrintMessage(MovementList.pathToFile)
    try:
        f = open(MovementList.pathToFile,)
        data = json.load(f)
    except:
        App.Console.PrintMessage("\r\n")
        App.Console.PrintMessage("File is empty/not existing\r\n")
        data = None
    App.Console.PrintMessage("\r\n")
    if data:
        curID = 0
        for movement in data:
            if movement["type"] == "Linear":
                start = [movement["startPoint"]["X"],movement["startPoint"]["X"],movement["startPoint"]["Z"] ]
                end = [movement["endPoint"]["X"],movement["endPoint"]["X"],movement["endPoint"]["Z"] ]
                MovementList.List.append(Movements.LinearMovement(id = movement["id"], sPoint = start, ePoint= end).__dict__)
                if curID < movement["id"]:
                    curID = movement["id"]
        MovementList.currentId = curID +1
    else:
        MovementList.List = []
        MovementList.currentId = 0
    App.Console.PrintMessage(MovementList.List)


class MovementList:
    pathToFile = None
    List = []
    currentId = 0
    
        
