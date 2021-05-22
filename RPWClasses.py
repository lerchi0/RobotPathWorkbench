import datetime
import PySide2
import json
import RPWlib

class Pathpoint:
    def __init__(self, position, coordSystem = None):
        self.position = {}
        self.position["X"] = position[0]
        self.position["Y"] = position[1]
        self.position["Z"] = position[2]
        self.coordinateSystem = coordSystem if coordSystem != None else ""

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
        f = open(self.configFile)
        try:
            data = json.load(f)
        except:
            data= {}
        for key in keys:
            if key in data == False:
                if key != "CreatedOn":
                    data[key] = None
                data["CreatedOn"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")  
        f.close()
        
        self.configData = data
        if self.configData["PathToMovements"] == None:
            movementsPath = RPWlib.reloadMovementList()
            self.configData["PathToMovements"] = movementsPath
        if self.configData["PathToCell"] == None:
            stepFilePath, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the robot cell",  "/", "Robot cells  (*.FCStd);;")
            self.configData["PathToCell"] = stepFilePath
        if self.configData["PathToCoordinateSystems"] == None:
            stepFilePath, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the Coordinate Systems File",  "/", "Coordinate Systems  (*.coord);;")
            self.configData["PathToCoordinateSystems"] = stepFilePath
        if self.configData["PathToPoints"] == None:
            stepFilePath=RPWlib.reloadPointsList()
            self.configData["PathToPoints"] = stepFilePath
            
    
    def writeConfig(self):
        with open(self.configFile, 'w') as fp:
            self.configData["EditedOn"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            json.dump(self.configData, fp, indent=4)
       