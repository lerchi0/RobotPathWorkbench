import os
import Movements
import RPWClasses
import PySide2
import json
import FreeCADGui as Gui
import FreeCAD as App


config = None

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
        f.close()
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
                MovementList.List.append(Movements.LinearMovement(sPoint = start, ePoint= end).__dict__)
    else:
        MovementList.List = []
    return MovementList.pathToFile

def reloadPointsList():
    doc = App.activeDocument()
    try:
        fullpath = doc.FileName
        index = fullpath.rfind("/")
        path = fullpath[:index+1]
    except:
        path = pathOfModule()
    PointsList.pathToFile, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the Points File",  "/", "Points  (*.pts);;")
    App.Console.PrintMessage(PointsList.pathToFile)
    try:
        f = open(PointsList.pathToFile,)
        data = json.load(f)
        f.close()
    except:
        App.Console.PrintMessage("\r\n")
        App.Console.PrintMessage("File is empty/not existing\r\n")
        data = None
    App.Console.PrintMessage("\r\n")
    if data:
        curID = 0
        for el in data["Points"]:
            point = RPWClasses.Pathpoint(position= [el["Position"]["X"],el["Position"]["Y"],el["Position"]["Z"]], coordSystem = el["CoordinateSystem"])
            PointsList.List.append(point)
            App.Console.PrintMessage(point.__dict__)
            App.Console.PrintMessage("\r\n")
       
    else:
        PointsList.List = []
    return PointsList.pathToFile


class MovementList:
    pathToFile = None
    List = []
    
class PointsList:
    pathToFile = None
    List = []