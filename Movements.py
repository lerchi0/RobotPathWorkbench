import numpy as np
import json
import RPWClasses

class Movement(object):
    def __init__(self, type):
        self.type = type
        

class LinearMovement(Movement):
    def __init__(self,sPoint, ePoint, speed = 50):
        super().__init__("Linear")
        self.startPoint = RPWClasses.Pathpoint(position = sPoint).__dict__
        self.endPoint = RPWClasses.Pathpoint(position = ePoint).__dict__
        self.speed = speed

class P2PMovement(Movement):
    def __init__(self,sPoint, ePoint, speed = 50):
        super().__init__("P2P")
        self.startPoint = {}
        self.endPoint = {}

        self.startPoint["X"] = sPoint[0]
        self.startPoint["Y"] = sPoint[1]
        self.startPoint["Z"] = sPoint[2]
        self.endPoint["X"] = ePoint[0]
        self.endPoint["Y"] = ePoint[1]
        self.endPoint["Z"] = ePoint[2]
        self.speed = speed

class CircularMovement(Movement):
    def __init__(self,sPoint,mPoint, ePoint, speed = 50):
        super().__init__("Circular")
        self.startPoint = {}
        self.midPoint = {}
        self.endPoint = {}
        
        self.startPoint["X"] = sPoint[0]
        self.startPoint["Y"] = sPoint[1]
        self.startPoint["Z"] = sPoint[2]
        self.midPoint["X"] = mPoint[0]
        self.midPoint["Y"] = mPoint[1]
        self.midPoint["Z"] = mPoint[2]
        self.endPoint["X"] = ePoint[0]
        self.endPoint["Y"] = ePoint[1]
        self.endPoint["Z"] = ePoint[2]
        self.speed = speed


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
    