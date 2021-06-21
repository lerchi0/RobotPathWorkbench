import datetime
import PySide2
import json
import RPWlib
import FreeCAD as App
class Pathpoint:
    def __init__(self, offsetPos, offsetRot, coordSystem):
        self.position = {}
        self.offsetPos = {}
        self.offsetRot = {}
        self.orientation = {}
        self.offsetPos["X"] = offsetPos["X"]
        self.offsetPos["Y"] = offsetPos["Y"]
        self.offsetPos["Z"] = offsetPos["Z"] 
        self.offsetRot["yaw"] = offsetRot["yaw"]
        self.offsetRot["pitch"] = offsetRot["pitch"]
        self.offsetRot["roll"] = offsetRot["roll"]
        if coordSystem != None:
            self.position["X"] = coordSystem["position"]["X"] + offsetPos["X"]
            self.position["Y"] = coordSystem["position"]["Y"] + offsetPos["Y"]
            self.position["Z"] = coordSystem["position"]["Z"] + offsetPos["Z"]
            self.orientation["yaw"] = coordSystem["orientation"]["yaw"] + offsetRot["yaw"]
            self.orientation["pitch"] = coordSystem["orientation"]["pitch"] + offsetRot["pitch"]
            self.orientation["roll"] = coordSystem["orientation"]["roll"] + offsetRot["roll"]
        else:
            self.position["X"] = offsetPos["X"]
            self.position["Y"] = offsetPos["Y"]
            self.position["Z"] = offsetPos["Z"]
            self.orientation["yaw"] = offsetRot["yaw"]
            self.orientation["pitch"] = offsetRot["pitch"]
            self.orientation["roll"] = offsetRot["roll"]
        self.coordinateSystem = coordSystem
    @staticmethod
    def draw(name, _type, pos, ori):
        doc = App.activeDocument
        try:
            doc.removeObject(name)
        except:
            pass
        try:
            doc.removeObject("Shape")
        except:
            pass
        #s = Part.makeSphere(RPWlib.sphereSize,pos)
        #Part.show(s)
        lcs = App.activeDocument().addObject('PartDesign::CoordinateSystem',name)
        lcs.Placement = App.Placement(pos,ori)
        if _type == 1:
            RPWlib.CSList.csGrp.addObject(App.ActiveDocument.getObject(name))
        elif _type == 2:
            RPWlib.PointsList.pointsGrp.addObject(App.ActiveDocument.getObject(name))

class CoordinateSystem (Pathpoint):
    def __init__(self,coordSystem, offsetPos, offsetRot, csId ,name = ""):
        self.id = csId
        self.name = name if name != "" else "CoordinateSystem_{}".format(self.id)
        super().__init__(offsetPos, offsetRot, coordSystem)
def delWithChildren(obj):
        doc = App.ActiveDocument
        for o in obj.OutList:
            delWithChildren(o)
        doc.removeObject(obj.Name)    

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
        App.open(self.configData["PathToCell"])
        try:
            path = App.ActiveDocument.getObject("Path")
            pts = App.ActiveDocument.getObject("Points")
            cs = App.ActiveDocument.getObject("Coordinate_Systems")
            delWithChildren(path)
            delWithChildren(pts)
            delWithChildren(cs)
            
        except:
            pass
        RPWlib.MovementList.pathGrp = App.ActiveDocument.addObject("App::DocumentObjectGroup", "Path")
        RPWlib.PointsList.pointsGrp = App.ActiveDocument.addObject("App::DocumentObjectGroup", "Points")
        RPWlib.CSList.csGrp = App.ActiveDocument.addObject("App::DocumentObjectGroup", "Coordinate_Systems")
        if self.configData["PathToMovements"] == None:
            doc = App.activeDocument()
            try:
                fullpath = doc.FileName
                index = fullpath.rfind("/")
                path = fullpath[:index+1]
            except:
                path = RPWlib.pathOfModule()
            RPWlib.MovementList.pathToFile, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the json File with the Movements",  path, "json files  (*.json);;")
            App.Console.PrintMessage(RPWlib.MovementList.pathToFile)
            self.configData["PathToMovements"] = RPWlib.MovementList.pathToFile
        else:
            RPWlib.MovementList.pathToFile = self.configData["PathToMovements"]
        RPWlib.reloadMovementList()

        if self.configData["PathToCell"] == None:
            cellPath, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the robot cell",  "/", "Robot cells  (*.FCStd);;")
            self.configData["PathToCell"] = cellPath
        else:
            pass

        if self.configData["PathToCoordinateSystems"] == None:
            doc = App.activeDocument()
            try:
                fullpath = doc.FileName
                index = fullpath.rfind("/")
                path = fullpath[:index+1]
            except:
                path = RPWlib.pathOfModule()
            RPWlib.CSList.pathToFile, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the CS File",  "/", "Coordinate Systems  (*.coords);;")
            App.Console.PrintMessage(RPWlib.CSList.pathToFile)
        else:
            RPWlib.CSList.pathToFile = self.configData["PathToCoordinateSystems"]
        RPWlib.reloadCSList()


        if self.configData["PathToPoints"] == None:
            doc = App.activeDocument()
            try:
                fullpath = doc.FileName
                index = fullpath.rfind("/")
                path = fullpath[:index+1]
            except:
                path = RPWlib.pathOfModule()
            RPWlib.PointsList.pathToFile, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the Points File",  "/", "Points  (*.pts);;")
            App.Console.PrintMessage(RPWlib.PointsList.pathToFile)
            self.configData["PathToPoints"] = RPWlib.PointsList.pathToFile
        else:
            RPWlib.PointsList.pathToFile = self.configData["PathToPoints"]
        RPWlib.reloadPointsList()
    
    def writeConfig(self):
        with open(self.configFile, 'w') as fp:
            self.configData["EditedOn"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            json.dump(self.configData, fp, indent=4)
       