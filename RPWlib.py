import os
import Movements
import RPWClasses
import PySide2
import json
import FreeCADGui as Gui
import FreeCAD as App


config = None
sphereSize = 10

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
    curID = 0
    if data:
        
        for movement in data:
            curID = curID+1
            if movement["type"] == "Linear":
                start = movement["startPoint"]
                end = movement["endPoint"]
                speed = movement["speed"]
                MovementList.List.append(Movements.LinearMovement(sPoint = start, ePoint= end, speed= speed).__dict__)
            if movement["type"] == "P2P":
                start = movement["startPoint"]
                end = movement["endPoint"]
                speed = movement["speed"]
                MovementList.List.append(Movements.P2PMovement(sPoint = start, ePoint= end, speed= speed).__dict__)
            if movement["type"] == "Circular":
                start = movement["startPoint"]
                mid = movement["midPoint"]
                end =movement["endPoint"]
                speed = movement["speed"]
                MovementList.List.append(Movements.CircularMovement(sPoint = start,mPoint=mid, ePoint= end, speed= speed).__dict__)
    else:
        MovementList.List = []
    curID = 0
    for el in MovementList.List:
        
        MovementList.currentId = curID
        if el["type"] == "Linear":
            start = App.Vector(el["startPoint"]["position"]["X"], el["startPoint"]["position"]["Y"], el["startPoint"]["position"]["Z"])
            end   = App.Vector(el["endPoint"]["position"]["X"], el["endPoint"]["position"]["Y"], el["endPoint"]["position"]["Z"])
            Movements.LinearMovement.draw(start, end)
        if el["type"] == "P2P":
            start = App.Vector(el["startPoint"]["position"]["X"], el["startPoint"]["position"]["Y"], el["startPoint"]["position"]["Z"])
            end   = App.Vector(el["endPoint"]["position"]["X"], el["endPoint"]["position"]["Y"], el["endPoint"]["position"]["Z"])
            Movements.P2PMovement.draw(start, end)
        if el["type"] == "Circular":
            start = App.Vector(el["startPoint"]["position"]["X"], el["startPoint"]["position"]["Y"], el["startPoint"]["position"]["Z"])
            mid = App.Vector(el["midPoint"]["position"]["X"], el["midPoint"]["position"]["Y"], el["midPoint"]["position"]["Z"])
            end   = App.Vector(el["endPoint"]["position"]["X"], el["endPoint"]["position"]["Y"], el["endPoint"]["position"]["Z"])
            Movements.CircularMovement.draw(start,mid, end)
        curID = curID +1
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
        for el in data:
            point = RPWClasses.Pathpoint(offsetPos= el["offsetPos"], offsetRot= el["offsetRot"], coordSystem = el["coordinateSystem"])
            PointsList.List.append(point.__dict__)
       
    else:
        PointsList.List = []
    for idx,el in enumerate(PointsList.List):
        _pos =  App.Vector(el["position"]["X"],el["position"]["Y"],el["position"]["Z"])
        _ori =  App.Rotation(el["orientation"]["yaw"],el["orientation"]["pitch"],el["orientation"]["roll"])
        RPWClasses.Pathpoint.draw("Point_{}".format(idx),2,_pos, _ori)
    return PointsList.pathToFile

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
    List = []
    currentId = 0
    
class PointsList:
    pointsGrp = None
    pathToFile = None
    List = []

    
class CSList:
    csGrp = None
    pathToFile = None
    List = []