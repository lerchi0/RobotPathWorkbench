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

import numpy as np
import json
import Part
import FreeCAD as App
import RPWlib
import math



class Movement(object):
    def __init__(self,id, type,speed,name,label):
        self.type = type
        self.speed = speed
        self.name = name
        self.label = label
        self.id = id
    def selfdraw(self):
        raise NotImplementedError()   
    def draw(self):
        raise NotImplementedError()
    

class Action(Movement):
    def __init__(self, id, name, label):
        super().__init__(id, "Action", 0, name, label)
    
    def selfdraw(self):
        return

    

class LinearMovement(Movement):
    
    def __init__(self,id, sPoint, ePoint, speed = 50,name = "", label = ""):
        super().__init__(id,"Linear", speed,name,label)
        self.startPoint = sPoint
        self.endPoint = ePoint

    def selfdraw(self):
        start = App.Placement(RPWlib.PointsList.List[self.startPoint["id"]].getTotalTransform()).Base
        end = App.Placement(RPWlib.PointsList.List[self.endPoint["id"]].getTotalTransform()).Base
        try:
            App.ActiveDocument.removeObject(self.name)
        except:
            pass
        try:
            myLine = Part.makeLine(start, end)
            shape=App.ActiveDocument.addObject("Part::Feature", self.name)
            shape.Shape=myLine
            App.ActiveDocument.recompute()
            shape.ViewObject.LineColor=RPWlib.lineColorLin
            RPWlib.MovementList.pathGrp.addObject(App.ActiveDocument.getObject(self.name))
        except:
            pass

    @staticmethod
    def draw(startP, endP, name):
        startPoint = startP.getTotalTransform()
        #start = App.Placement(RPWlib.CSList.List[0].getTransform().multiply(startPoint)).Base
        start = App.Placement(startPoint).Base
        endPoint = endP.getTotalTransform()
        end = App.Placement(endPoint).Base
        #end = App.Placement(RPWlib.CSList.List[0].getTransform().multiply(endPoint)).Base
        myLine = Part.makeLine(start, end)
        try:
            App.ActiveDocument.removeObject(name)
            
        except:
            pass
        myLine = Part.makeLine(start, end)
        shape=App.ActiveDocument.addObject("Part::Feature", name)
        shape.Shape=myLine
        App.ActiveDocument.recompute()
        shape.ViewObject.LineColor=RPWlib.lineColorLin
        
        RPWlib.MovementList.pathGrp.addObject(App.ActiveDocument.getObject(name))
        

class P2PMovement(Movement):
    def __init__(self,id,sPoint, ePoint, speed = 50,name = "" ,label = ""):
        super().__init__(id,"P2P", speed,name, label)
        self.startPoint = {}
        self.endPoint = {}

        self.startPoint = sPoint
        self.endPoint = ePoint


    def selfdraw(self):
        start = App.Placement(RPWlib.PointsList.List[self.startPoint["id"]].getTotalTransform()).Base
        end = App.Placement(RPWlib.PointsList.List[self.endPoint["id"]].getTotalTransform()).Base
        try:
            App.ActiveDocument.removeObject(self.name)
        except:
            pass
        try:
            myLine = Part.makeLine(start, end)
            shape=App.ActiveDocument.addObject("Part::Feature", self.name)
            shape.Shape=myLine
            App.ActiveDocument.recompute()
            shape.ViewObject.LineColor=RPWlib.lineColorP2P
            RPWlib.MovementList.pathGrp.addObject(App.ActiveDocument.getObject(self.name))  
        except:
            pass
        

    @staticmethod
    def draw(startP, endP, name):
        startPoint = startP.getTotalTransform()
        #start = App.Placement(RPWlib.CSList.List[0].getTransform().multiply(startPoint)).Base
        start = App.Placement(startPoint).Base
        endPoint = endP.getTotalTransform()
        end = App.Placement(endPoint).Base
        #end = App.Placement(RPWlib.CSList.List[0].getTransform().multiply(endPoint)).Base
        myLine = Part.makeLine(start, end)
        try:
            App.ActiveDocument.removeObject(name)
        except:
            pass
        shape=App.ActiveDocument.addObject("Part::Feature", name)
        shape.Shape=myLine
        App.ActiveDocument.recompute()
        shape.ViewObject.LineColor=RPWlib.lineColorP2P
        RPWlib.MovementList.pathGrp.addObject(App.ActiveDocument.getObject(name))

class CircularMovement(Movement):
    def __init__(self,id,sPoint,mPoint, ePoint, speed = 50,name = "", label = ""):
        super().__init__(id,"Circular",speed,name, label)
        self.startPoint = {}
        self.midPoint = {}
        self.endPoint = {}
        self.startPoint = sPoint
        self.midPoint = mPoint
        self.endPoint = ePoint


    def selfdraw(self):
        start = App.Placement(RPWlib.PointsList.List[self.startPoint["id"]].getTotalTransform()).Base
        mid = App.Placement(RPWlib.PointsList.List[self.midPoint["id"]].getTotalTransform()).Base
        end = App.Placement(RPWlib.PointsList.List[self.endPoint["id"]].getTotalTransform()).Base
        

        
        try:
            App.ActiveDocument.removeObject(self.name)
        except:
            pass
        try:
            arc = Part.Arc(start,mid,end)
            myLine = arc.toShape()
            shape=App.ActiveDocument.addObject("Part::Feature", self.name)
            shape.Shape=myLine
            App.ActiveDocument.recompute()
            shape.ViewObject.LineColor=RPWlib.lineColorCirc
            RPWlib.MovementList.pathGrp.addObject(App.ActiveDocument.getObject(self.name))
        except:
            pass
        

    @staticmethod
    def draw(startP, midP ,endP, name):
        startPoint = startP.getTotalTransform()
        #start = App.Placement(RPWlib.CSList.List[0].getTransform().multiply(startPoint)).Base
        start = App.Placement(startPoint).Base
        midPoint = midP.getTotalTransform()
        #start = App.Placement(RPWlib.CSList.List[0].getTransform().multiply(startPoint)).Base
        mid = App.Placement(midPoint).Base
        endPoint = endP.getTotalTransform()
        end = App.Placement(endPoint).Base
        #end = App.Placement(RPWlib.CSList.List[0].getTransform().multiply(endPoint)).Base
        
        arc = Part.Arc(start,mid,end)
        try:
            App.ActiveDocument.removeObject(name)
        except:
            pass
        myLine = arc.toShape()
        shape=App.ActiveDocument.addObject("Part::Feature", name)
        shape.Shape=myLine
        App.ActiveDocument.recompute()
        shape.ViewObject.LineColor=RPWlib.lineColorCirc
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
    