import numpy as np
import json
import RPWClasses
import Part
import FreeCAD as App
import RPWlib
import math
class Movement(object):
    def __init__(self, type,speed,name,label):
        self.type = type
        self.speed = speed
        self.name = name
        self.label = label
        
    def draw():
        raise NotImplementedError()

class LinearMovement(Movement):
    def __init__(self,sPoint, ePoint, speed = 50,name = "", label = ""):
        super().__init__("Linear", speed,name,label)
        self.startPoint = sPoint
        self.endPoint = ePoint
    @staticmethod
    def draw(start, end, name):
        
        myLine = Part.makeLine(start, end)
        try:
            App.ActiveDocument.removeObject(name)
        except:
            pass
        shape=App.ActiveDocument.addObject("Part::Feature", name)
        shape.Shape=myLine
        App.ActiveDocument.recompute()
        shape.ViewObject.LineColor=(1.0,0.0,1.0)
        
        RPWlib.MovementList.pathGrp.addObject(App.ActiveDocument.getObject(name))
        

class P2PMovement(Movement):
    def __init__(self,sPoint, ePoint, speed = 50,name = "" ,label = ""):
        super().__init__("P2P", speed,name, label)
        self.startPoint = {}
        self.endPoint = {}

        self.startPoint = sPoint
        self.endPoint = ePoint

    @staticmethod
    def draw(start, end, name):
        myLine = Part.makeLine(start, end)
        try:
            App.ActiveDocument.removeObject(name)
        except:
            pass
        shape=App.ActiveDocument.addObject("Part::Feature", name)
        shape.Shape=myLine
        App.ActiveDocument.recompute()
        shape.ViewObject.LineColor=(0.0,0.0,1.0)
        RPWlib.MovementList.pathGrp.addObject(App.ActiveDocument.getObject(name))

class CircularMovement(Movement):
    def __init__(self,sPoint,mPoint, ePoint, speed = 50,name = "", label = ""):
        super().__init__("Circular",speed,name, label)
        self.startPoint = {}
        self.midPoint = {}
        self.endPoint = {}
        self.startPoint = sPoint
        self.midPoint = mPoint
        self.endPoint = ePoint
    @staticmethod
    def draw(start, mid ,end, name):
        arc = Part.Arc(start,mid,end)
        try:
            App.ActiveDocument.removeObject(name)
        except:
            pass
        myLine = arc.toShape()
        shape=App.ActiveDocument.addObject("Part::Feature", name)
        shape.Shape=myLine
        App.ActiveDocument.recompute()
        shape.ViewObject.LineColor=(1.0,0.0,0.0)
        
        RPWlib.MovementList.pathGrp.addObject(App.ActiveDocument.getObject(name))

if __name__ == "__main__":
    lst = []

    for i in range(10):
        sP = np.random.randint(21,size= (3,1))
        mP = np.random.randint(21, size =(3,1))
        eP = np.random.randint(21, size =(3,1))
        s = np.random.randint(100)
        if i%3 == 0:
            lst.append(LinearMovement(sPoint= sP, ePoint=eP,speed= s).__dict__)
        elif i%3 == 1:
            lst.append(P2PMovement(sPoint= sP, ePoint=eP,speed= s).__dict__)
        elif i%3 == 2:
            lst.append(CircularMovement(sPoint= sP,mPoint=mP, ePoint=eP,speed= s).__dict__)         
    print(json.dumps(lst, indent=4))
    