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
lineColorPurple = (1.0,0.0,1.0)
lineColorRed = (1.0,0.0,0.0)
lineColorBlue = (0.0,0.0,1.0)
lineColorCyan = (0.0,1.0,1.0)
lineColorLin = lineColorCyan
lineColorP2P = lineColorCyan
lineColorCirc = lineColorCyan

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
        curID = 0
        for movement in data["Movements"]:
            if movement["type"] == "Action":
                speed = movement["speed"]
                label = movement["label"]
                name = movement["name"]
                MovementList.List.append(Movements.Action(id = curID, name = name, label = label))
            if movement["type"] == "Linear":
                start = movement["startPoint"]
                end = movement["endPoint"]
                speed = movement["speed"]
                label = movement["label"]
                name = movement["name"]
                MovementList.List.append(Movements.LinearMovement(id = curID,sPoint = start, ePoint= end, speed= speed,name=name, label=label))
            if movement["type"] == "P2P":
                start = movement["startPoint"]
                end = movement["endPoint"]
                speed = movement["speed"]
                label = movement["label"]
                name = movement["name"]
                MovementList.List.append(Movements.P2PMovement(id = curID,sPoint = start, ePoint= end, speed= speed,name=name, label=label))
            if movement["type"] == "Circular":
                start = movement["startPoint"]
                mid = movement["midPoint"]
                end =movement["endPoint"]
                speed = movement["speed"]
                label = movement["label"]
                name = movement["name"]
                MovementList.List.append(Movements.CircularMovement(id = curID,sPoint = start,mPoint=mid, ePoint= end, speed= speed,name=name, label=label))
            curID = curID +1
    else:
        MovementList.List = []
    curID = 0
    for el in MovementList.List:
        MovementList.currentId = curID
        el.selfdraw()
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

            point = RPWClasses.Pathpoint(offsetPos= _offsetPos, offsetRot= _offsetRot, coordSystem = _csID)
            PointsList.List.append(point)
        PointsList.lastEditedOn = data["lastEditedOn"]
        PointsList.lastEditor = data["lastEditor"]
       
    else:
        PointsList.List = []
    for idx,el in enumerate(PointsList.List):
        _pos =  App.Vector(el.position["X"],el.position["Y"],el.position["Z"])
        _ori =  App.Rotation(el.orientation["yaw"],el.orientation["pitch"],el.orientation["roll"])
        el.selfDraw("Point_{}".format(idx),2)
    return PointsList.pathToFile

def writePointsFile(points,editor):
    pointsdict = getPointsDict(points)
    fileDict = { 
        "lastEditedOn": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "lastEditor": editor ,
        "Points": pointsdict
        }

    with open(PointsList.pathToFile, 'w') as outfile:
        json.dump(fileDict, outfile, indent=4)

def writeMovementsFile(movements, editor):
    movementsdict = getMovementDict(movements)
    fileDict = { 
        "lastEditedOn": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "lastEditor": editor ,
        "Movements": movementsdict
        }

    with open(MovementList.pathToFile, 'w') as outfile:
        json.dump(fileDict, outfile, indent=4)

def writeCSFile(coords, editor):
    csDict = getCSDict(coords)
    fileDict = {
        "lastEditedOn": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "lastEditor": editor ,
        "CoordinateSystems": csDict
    }
    with open(CSList.pathToFile, 'w') as outfile:
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
        for el in data["CoordinateSystems"]:
            cs = RPWClasses.CoordinateSystem(csId=el["id"], name= el["name"], coordSystem=el["coordinateSystem"], offsetPos= el["offsetPos"], offsetRot=el["offsetRot"])
            CSList.List.append(cs) 
    else:
        CSList.List = []
        cs = RPWClasses.CoordinateSystem(csId=0, name= "RobotBase", coordSystem=None, offsetPos= {"X":0.0,"Y":0.0,"Z":0.0}, offsetRot={"yaw":0.0,"pitch":0.0,"roll":0.0})
        CSList.List.append(cs)
    
    for el in CSList.List:
        
        el.selfDraw(el.name,1)
        
    return CSList.pathToFile

def getMovementDict(movements):
    mDict = []
    for movement in movements:
        if movement.type == "Action":
            mDict.append({
                "type": movement.type,
                "speed": movement.speed,
                "label": movement.label,
                "name": movement.name,
                "id" : movement.id
            }
            )
        elif movement.type == "Circular":
            mDict.append(
            {
                "type": movement.type,
                "speed": movement.speed,
                "label": movement.label,
                "name": movement.name,
                "id" : movement.id,
                "startPoint": {
                    "id":movement.startPoint["id"],
                    "position": movement.startPoint["position"],
                    "orientation": movement.startPoint["orientation"],
                    "coordinateSystem": movement.startPoint["coordinateSystem"]
                },
                "midPoint": {
                    "id":movement.midPoint["id"],
                    "position": movement.midPoint["position"],
                    "orientation": movement.midPoint["orientation"],
                    "coordinateSystem": movement.midPoint["coordinateSystem"]
                },
                "endPoint": {
                    "id":movement.endPoint["id"],
                    "position": movement.endPoint["position"],
                    "orientation": movement.endPoint["orientation"],
                    "coordinateSystem": movement.endPoint["coordinateSystem"]
                }
            }
            )
        else:
            mDict.append(
            {
                "type": movement.type,
                "speed": movement.speed,
                "label": movement.label,
                "name": movement.name,
                "id" : movement.id,
                "startPoint": {
                    "id":movement.startPoint["id"],
                    "position": movement.startPoint["position"],
                    "orientation": movement.startPoint["orientation"],
                    "coordinateSystem": movement.startPoint["coordinateSystem"]
                },
                "endPoint": {
                    "id":movement.endPoint["id"],
                    "position": movement.endPoint["position"],
                    "orientation": movement.endPoint["orientation"],
                    "coordinateSystem": movement.endPoint["coordinateSystem"]
                }
            })
    return mDict



def getPointsDict(points):
    pDict = []
    for point in points:
        pDict.append(
            {
                "position": point.offsetPos,
                "orientation": point.offsetRot,
                "coordinateSystem" : point.coordinateSystem
            }
        )
    return pDict
def getCSDict(coordinateSystems):
    csDict = []
    for cs in coordinateSystems:
        csDict.append(
            {
                "id": cs.id,
                "name": cs.name,
                "position": cs.position,
                "orientation": cs.orientation,
                "offsetPos": cs.offsetPos,
                "offsetRot": cs.offsetRot,
                "coordinateSystem": cs.coordinateSystem
        }
        )
    return csDict

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