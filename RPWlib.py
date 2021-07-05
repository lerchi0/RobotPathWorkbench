import os
import Movements
import RPWClasses
import PySide2
import json
import FreeCADGui as Gui
import FreeCAD as App
import datetime

config = None
sphereSize = 10

mainCMDs = None
addSegCMDs = None
newModCMDs = None



def pathOfModule():
    return os.path.dirname(__file__)


def reloadMovementList():
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
        App.Console.PrintMessage("\r\nMovements-file last edited on {} by {}".format(data["lastEditedOn"], data["lastEditor"]))
        for movement in data["Movements"]:
            
            if movement["type"] == "Linear":
                start = movement["startPoint"]
                end = movement["endPoint"]
                speed = movement["speed"]
                label = movement["label"]
                name = movement["name"]
                MovementList.List.append(Movements.LinearMovement(sPoint = start, ePoint= end, speed= speed,name=name, label=label).__dict__)
            if movement["type"] == "P2P":
                start = movement["startPoint"]
                end = movement["endPoint"]
                speed = movement["speed"]
                label = movement["label"]
                name = movement["name"]
                MovementList.List.append(Movements.P2PMovement(sPoint = start, ePoint= end, speed= speed,name=name, label=label).__dict__)
            if movement["type"] == "Circular":
                start = movement["startPoint"]
                mid = movement["midPoint"]
                end =movement["endPoint"]
                speed = movement["speed"]
                label = movement["label"]
                name = movement["name"]
                MovementList.List.append(Movements.CircularMovement(sPoint = start,mPoint=mid, ePoint= end, speed= speed,name=name, label=label).__dict__)
    else:
        MovementList.List = []
    curID = 0
    for el in MovementList.List:
        MovementList.currentId = curID
        if el["type"] == "Linear":
            start = App.Vector(el["startPoint"]["position"]["X"], el["startPoint"]["position"]["Y"], el["startPoint"]["position"]["Z"])
            end   = App.Vector(el["endPoint"]["position"]["X"], el["endPoint"]["position"]["Y"], el["endPoint"]["position"]["Z"])
            Movements.LinearMovement.draw(start, end, el["name"])
        if el["type"] == "P2P":
            start = App.Vector(el["startPoint"]["position"]["X"], el["startPoint"]["position"]["Y"], el["startPoint"]["position"]["Z"])
            end   = App.Vector(el["endPoint"]["position"]["X"], el["endPoint"]["position"]["Y"], el["endPoint"]["position"]["Z"])
            Movements.P2PMovement.draw(start, end,el["name"])
        if el["type"] == "Circular":
            start = App.Vector(el["startPoint"]["position"]["X"], el["startPoint"]["position"]["Y"], el["startPoint"]["position"]["Z"])
            mid = App.Vector(el["midPoint"]["position"]["X"], el["midPoint"]["position"]["Y"], el["midPoint"]["position"]["Z"])
            end   = App.Vector(el["endPoint"]["position"]["X"], el["endPoint"]["position"]["Y"], el["endPoint"]["position"]["Z"])
            Movements.CircularMovement.draw(start,mid, end,el["name"])
        curID = curID +1
    MovementList.currentId = curID
    return MovementList.pathToFile

def reloadPointsList():
    
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
        App.Console.PrintMessage("\r\nPoints-file last edited on {} by {}".format(data["lastEditedOn"], data["lastEditor"]))
        for el in data["Points"]:
            _offsetPos = el["position"]
            _offsetRot = el["orientation"]
            _csID = el["coordinateSystem"] 

            _cs = CSList.List[_csID]
            _csPos =_cs["position"]
            _csRot =_cs["orientation"]
            

            point = RPWClasses.Pathpoint(offsetPos= _offsetPos, offsetRot= _offsetRot, coordSystem = _cs)
            PointsList.List.append(point.__dict__)
        PointsList.lastEditedOn = data["lastEditedOn"]
        PointsList.lastEditor = data["lastEditor"]
       
    else:
        PointsList.List = []
    for idx,el in enumerate(PointsList.List):
        _pos =  App.Vector(el["position"]["X"],el["position"]["Y"],el["position"]["Z"])
        _ori =  App.Rotation(el["orientation"]["yaw"],el["orientation"]["pitch"],el["orientation"]["roll"])
        RPWClasses.Pathpoint.draw("Point_{}".format(idx),2,_pos, _ori)
    return PointsList.pathToFile

def writePointsFile(points,editor):
    pointsdict = []
    for point in points:
        pointsdict.append(
            {
                "position": point["offsetPos"],
                "orientation": point["offsetRot"],
                "coordinateSystem" : point["coordinateSystem"]["id"]
            }
        )
    fileDict = { 
        "lastEditedOn": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "lastEditor": editor ,
        "Points": pointsdict
        }

    with open(PointsList.pathToFile, 'w') as outfile:
        json.dump(fileDict, outfile, indent=4)

def writeMovementsFile(movements, editor):
    movementsdict = []
    for movement in movements:
        if movement["type"] == "Circular":
            movementsdict.append(
            {
                "type": movement["type"],
                "speed": movement["speed"],
                "label": movement["label"],
                "name": movement["name"],
                "startPoint": {
                    "position": movement["startPoint"]["position"],
                    "orientation": movement["startPoint"]["orientation"],
                    "coordinateSystem": movement["startPoint"]["coordinateSystem"]
                },
                "midPoint": {
                    "position": movement["midPoint"]["position"],
                    "orientation": movement["midPoint"]["orientation"],
                    "coordinateSystem": movement["midPoint"]["coordinateSystem"]
                },
                "endPoint": {
                    "position": movement["endPoint"]["position"],
                    "orientation": movement["endPoint"]["orientation"],
                    "coordinateSystem": movement["endPoint"]["coordinateSystem"]
                }
            }
            )
        else:
            movementsdict.append(
            {
                "type": movement["type"],
                "speed": movement["speed"],
                "label": movement["label"],
                "name": movement["name"],
                "startPoint": {
                    "position": movement["startPoint"]["position"],
                    "orientation": movement["startPoint"]["orientation"],
                    "coordinateSystem":movement["startPoint"]["coordinateSystem"]
                },
                "endPoint": {
                    "position": movement["endPoint"]["position"],
                    "orientation": movement["endPoint"]["orientation"],
                    "coordinateSystem":movement["endPoint"]["coordinateSystem"]
                }
            }
        )
    fileDict = { 
        "lastEditedOn": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "lastEditor": editor ,
        "Movements": movementsdict
        }

    with open(MovementList.pathToFile, 'w') as outfile:
        json.dump(fileDict, outfile, indent=4)


def reloadCSList():
    
    try:
        f = open(CSList.pathToFile,)
        data = json.load(f)
        f.close()
    except:
        App.Console.PrintMessage("\r\n")
        App.Console.PrintMessage("File is empty/not existing\r\n")
        data = None
    App.Console.PrintMessage("\r\n")
    if data:
        curID = 0
        for el in data:
            cs = RPWClasses.CoordinateSystem(csId=el["id"], name= el["name"], coordSystem=el["coordinateSystem"], offsetPos= el["offsetPos"], offsetRot=el["offsetRot"])
            CSList.List.append(cs.__dict__)
           
       
    else:
        CSList.List = []
        cs = RPWClasses.CoordinateSystem(csId=0, name= "RobotBase", coordSystem=None, offsetPos= {"X":0.0,"Y":0.0,"Z":0.0}, offsetRot={"yaw":0.0,"pitch":0.0,"roll":0.0})
        CSList.List.append(cs.__dict__)
    for el in CSList.List:
        _pos =  App.Vector(el["position"]["X"],el["position"]["Y"],el["position"]["Z"])
        _ori =  App.Rotation(el["orientation"]["yaw"],el["orientation"]["pitch"],el["orientation"]["roll"])
        RPWClasses.Pathpoint.draw(el["name"],1,_pos, _ori)
    return CSList.pathToFile


class MovementList:
    pathGrp = None
    pathToFile = None
    lastEditedOn = None
    lastEditor = None
    List = []
    currentId = 0
    
class PointsList:
    pointsGrp = None
    pathToFile = None
    lastEditedOn = None
    lastEditor = None
    List = []

    
class CSList:
    csGrp = None
    pathToFile = None
    lastEditedOn = None
    lastEditor = None
    List = []