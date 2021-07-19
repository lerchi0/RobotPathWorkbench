import datetime
import PySide2
import json
import RPWlib
import FreeCAD as App
import math
import getpass
class Pathpoint:
    def __init__(self,offsetPos, offsetRot, coordSystem):
        self.position = {}
        self.offsetPos = {}
        self.offsetRot = {}
        self.orientation = {}
        self.offsetPos["X"] = round(offsetPos["X"],2)
        self.offsetPos["Y"] = round(offsetPos["Y"],2)
        self.offsetPos["Z"] = round(offsetPos["Z"],2)
        self.offsetRot["yaw"] = round(offsetRot["yaw"],2)
        self.offsetRot["pitch"] = round(offsetRot["pitch"],2)
        self.offsetRot["roll"] = round(offsetRot["roll"],2)
        self.coordinateSystem = coordSystem
        if coordSystem != None:
            cs = RPWlib.CSList.List[coordSystem]
            place = App.Placement(self.getTotalTransform())
            self.position["X"] = round(place.Base.x,2)
            self.position["Y"] = round(place.Base.y,2)
            self.position["Z"] = round(place.Base.z,2)
            self.orientation["yaw"] = round(place.Rotation.toEuler()[0],2)
            self.orientation["pitch"] = round(place.Rotation.toEuler()[1],2)
            self.orientation["roll"] = round(place.Rotation.toEuler()[2],2)
        else:
            self.position["X"] = round(offsetPos["X"],2)
            self.position["Y"] = round(offsetPos["Y"],2)
            self.position["Z"] = round(offsetPos["Z"],2)
            self.orientation["yaw"] = round(offsetRot["yaw"],2)
            self.orientation["pitch"] = round(offsetRot["pitch"],2)
            self.orientation["roll"] = round(offsetRot["roll"],2)
    def getTransform(self):
        transform = App.Base.Matrix()

        transform.A11 = math.cos(math.radians(self.offsetRot["yaw"]))*math.cos(math.radians(self.offsetRot["pitch"]))
        transform.A21 = math.sin(math.radians(self.offsetRot["yaw"]))*math.cos(math.radians(self.offsetRot["pitch"]))
        transform.A31 = -math.sin(math.radians(self.offsetRot["pitch"]))
        transform.A41 = 0

        transform.A12 = math.cos(math.radians(self.offsetRot["yaw"]))*math.sin(math.radians(self.offsetRot["pitch"]))*math.sin(math.radians(self.offsetRot["roll"])) - math.sin(math.radians(self.offsetRot["yaw"]))*math.cos(math.radians(self.offsetRot["roll"]))
        transform.A22 = math.sin(math.radians(self.offsetRot["yaw"]))*math.sin(math.radians(self.offsetRot["pitch"]))*math.sin(math.radians(self.offsetRot["roll"])) + math.cos(math.radians(self.offsetRot["yaw"]))*math.cos(math.radians(self.offsetRot["roll"]))
        transform.A32 = math.cos(math.radians(self.offsetRot["pitch"]))*math.sin(math.radians(self.offsetRot["roll"]))
        transform.A42 = 0

        transform.A13 = math.cos(math.radians(self.offsetRot["yaw"]))*math.sin(math.radians(self.offsetRot["pitch"]))*math.cos(math.radians(self.offsetRot["roll"])) + math.sin(math.radians(self.offsetRot["yaw"]))*math.sin(math.radians(self.offsetRot["roll"]))
        transform.A23 = math.sin(math.radians(self.offsetRot["yaw"]))*math.sin(math.radians(self.offsetRot["pitch"]))*math.cos(math.radians(self.offsetRot["roll"])) - math.cos(math.radians(self.offsetRot["yaw"]))*math.sin(math.radians(self.offsetRot["roll"]))
        transform.A33 = math.cos(math.radians(self.offsetRot["pitch"]))*math.cos(math.radians(self.offsetRot["roll"]))
        transform.A43 = 0
        
        transform.A14 = self.offsetPos["X"]
        transform.A24 = self.offsetPos["Y"]
        transform.A34 = self.offsetPos["Z"]
        transform.A44 = 1
        return transform

    def getTotalTransform(self):
        totalTransform = App.Base.Matrix()
        parentList = []
        cs = self
        while True:
            parent = cs.coordinateSystem
            if parent == None:
                break
            parentList.append(parent)
            cs = RPWlib.CSList.List[parent]
        while len(parentList) != 0:
            cs = RPWlib.CSList.List[parentList.pop()]
            if cs.id != 0:
                totalTransform = totalTransform.multiply(cs.getTransform())
        totalTransform = totalTransform*self.getTransform()
        return totalTransform

    @staticmethod
    def draw(name, _type, trafo, isBase = False):
        doc = App.ActiveDocument
        try:
            doc.removeObject(name)
        except Exception as e:
            App.Console.PrintError("{}\r\n{}".format(e, name))

        lcs = doc.addObject('PartDesign::CoordinateSystem',name)
        if not isBase:
            trafo = RPWlib.CSList.List[0].getTransform().multiply(trafo)
        
        lcs.Placement = App.Placement(trafo)
        try:
            if _type == 1:
                RPWlib.CSList.csGrp.addObject(App.ActiveDocument.getObject(name))
            elif _type == 2:
                RPWlib.PointsList.pointsGrp.addObject(App.ActiveDocument.getObject(name))
        except Exception as e:
            App.Console.PrintMessage(e)


class CoordinateSystem(Pathpoint):
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

        if self.configData["PathToCell"] == None or self.configData["PathToCell"] == "":
            cellPath, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the robot cell",  "/", "Robot cells  (*.FCStd);;")
            self.configData["PathToCell"] = cellPath
        else:
            pass
        
        App.open(self.configData["PathToCell"])
        doc = App.ActiveDocument

        try:
            path = doc.getObject("Path")
            pts = doc.getObject("Points")
            cs = doc.getObject("Coordinate_Systems")
            delWithChildren(path)
            delWithChildren(pts)
            delWithChildren(cs)
            
        except:
            pass

        
        try:
            fullpath = doc.FileName
            index = fullpath.rfind("/")
            path = fullpath[:index+1]
        except:
            path = RPWlib.pathOfModule()

        try:
            RPWlib.MovementList.pathGrp = doc.addObject("App::DocumentObjectGroup", "Path")
            RPWlib.PointsList.pointsGrp = doc.addObject("App::DocumentObjectGroup", "Points")
            RPWlib.CSList.csGrp = doc.addObject("App::DocumentObjectGroup", "Coordinate_Systems")
        except Exception as e:
            App.Console.PrintMessage(e)
        user = getpass.getuser()

        
        # Load defined Coordinate Systems
        if self.configData["PathToCoordinateSystems"] == None or self.configData["PathToCoordinateSystems"] == "":
            RPWlib.CSList.pathToFile, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the CS File", path, "Coordinate Systems  (*.coords);;")
            self.configData["PathToCoordinateSystems"] = RPWlib.CSList.pathToFile
        else:
            RPWlib.CSList.pathToFile = self.configData["PathToCoordinateSystems"]
        RPWlib.reloadCSList()
        RPWlib.writeCSFile(RPWlib.CSList.List, user)

        # Load defined Poses
        if self.configData["PathToPoints"] == None or self.configData["PathToPoints"] == "":
            RPWlib.PointsList.pathToFile, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the Points File",  path, "Points  (*.pts);;")
            self.configData["PathToPoints"] = RPWlib.PointsList.pathToFile
        else:
            RPWlib.PointsList.pathToFile = self.configData["PathToPoints"]
        RPWlib.reloadPointsList()
        RPWlib.writePointsFile(RPWlib.PointsList.List, user)

        # Load saved Movements (Path)
        if self.configData["PathToMovements"] == None or self.configData["PathToMovements"] == "":
            RPWlib.MovementList.pathToFile, Filter = PySide2.QtWidgets.QFileDialog.getSaveFileName(None, "Choose the json File with the Movements",  path, "json files  (*.json);;")
            self.configData["PathToMovements"] = RPWlib.MovementList.pathToFile
        else:
            RPWlib.MovementList.pathToFile = self.configData["PathToMovements"]
        RPWlib.reloadMovementList()
        RPWlib.writeMovementsFile(RPWlib.MovementList.List, user)
        
    
    def writeConfig(self):
        with open(self.configFile, 'w') as fp:
            self.configData["EditedOn"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            json.dump(self.configData, fp, indent=4)
       