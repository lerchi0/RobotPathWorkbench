import datetime




class Pathpoint:
    def __init__(self, position, coordSystem = None):
        self.position = {}
        self.position["X"] = position[0]
        self.position["Y"] = position[1]
        self.position["Z"] = position[2]
        self.coordSystem = coordSystem if coordSystem != None else ""

class CoordinateSystem:
    def __init__(self,parentCS, position, rotation, csId ,name):
        self.csId = csId
        self.parent = parentCS
        self.position = position
        self.rotation = rotation
        self.name = name if name != "" else "CoordinateSystem"

class ProjectConfiguration:
    def __init__(self, pathToSTP =None, robotPose = None, pathToPath= None, createdOn= None, editedOn= None, savedPoints = None, coordinateSystems = None):
        self.stpPath = pathToPath
        self.robotPose = robotPose
        self.pathfilePath = pathToPath
        self.createdOn = createdOn
        self.editedOn = editedOn
        self.savedPoints = savedPoints if savedPoints != None else {}
        self.coordinateSystems = coordinateSystems if coordinateSystems != None else {}
        
    