import datetime
import PySide2
import json
import RPWlib
import FreeCAD as App
class Pathpoint:
    def __init__(self, position, coordSystem = None):
        self.position = {}
        self.position["X"] = position[0]
        self.position["Y"] = position[1]
        self.position["Z"] = position[2]
        self.coordinateSystem = coordSystem if coordSystem != None else "?"

class CoordinateSystem:
    def __init__(self,parentCS, position, rotation, csId ,name):
        self.csId = csId
        self.parent = parentCS
        self.position = position
        self.rotation = rotation
        self.name = name if name != "" else "CoordinateSystem"

class ProjectConfiguration:
    def __init__(self, configFile = None):
        self.configFile = configFile if configFile != None else ""
        if self.configFile == "":
            configFilePath, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the config-file",  "/", "config files  (*.cfg);;")
            self.configFile = configFilePath

    def readConfig(self):
        keys = ["PathToCell","PathToCoordinateSystems","PathToPoints","PathToMovements","CreatedOn","EditedOn","Origin"]
        
        try:
            f = open(self.configFile)
            data = json.load(f)
            f.close()
        except:
            data= {}
        for key in keys:
            if key in data == False:
                if key != "CreatedOn":
                    data[key] = None
                data["CreatedOn"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")  
        
        
        self.configData = data
        App.Console.PrintMessage(data)
        if self.configData["PathToMovements"] == None:
            movementsPath = RPWlib.reloadMovementList()
            self.configData["PathToMovements"] = movementsPath
        else:
            pass

        if self.configData["PathToCell"] == None:
            cellPath, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the robot cell",  "/", "Robot cells  (*.FCStd);;")
            self.configData["PathToCell"] = cellPath
        else:
            pass

        if self.configData["PathToCoordinateSystems"] == None:
            csPath, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the Coordinate Systems File",  "/", "Coordinate Systems  (*.coord);;")
            self.configData["PathToCoordinateSystems"] = csPath
        else:
            pass  
        if self.configData["PathToPoints"] == None:
            pointsPath=RPWlib.reloadPointsList()
            self.configData["PathToPoints"] = pointsPath
        else:
            try:
                f = open(self.configData["PathToPoints"]) 
                data = json.load(f)
                f.close()
            except:
                App.Console.PrintMessage("\r\n")
                App.Console.PrintMessage("File is empty/not existing\r\n")
                data = None
            App.Console.PrintMessage("\r\n")
            if data:
                for el in data["Points"]:
                    point = Pathpoint(position= [el["Position"]["X"],el["Position"]["Y"],el["Position"]["Z"]], coordSystem = el["CoordinateSystem"])
                    RPWlib.PointsList.List.append(point)
            else:
                RPWlib.PointsList.List = []
            
    
    def writeConfig(self):
        with open(self.configFile, 'w') as fp:
            self.configData["EditedOn"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            json.dump(self.configData, fp, indent=4)
       