import numpy as np
import json

class Movement(object):
    def __init__(self, type,id):
        self.id = id
        self.type = type
        

class LinearMovement(Movement):
    def __init__(self, id,sPoint, ePoint, speed = 50):
        super().__init__("Linear", id)
        self.startPoint = {}
        self.endPoint = {}

        self.startPoint["X"] = sPoint[0]
        self.startPoint["Y"] = sPoint[1]
        self.startPoint["Z"] = sPoint[2]
        self.endPoint["X"] = ePoint[0]
        self.endPoint["Y"] = ePoint[1]
        self.endPoint["Z"] = ePoint[2]
        self.speed = speed

class P2PMovement(Movement):
    def __init__(self, id,sPoint, ePoint, speed = 50):
        super().__init__("P2P", id)
        self.startPoint = {}
        self.endPoint = {}

        self.startPoint["X"] = int(sPoint[0][0])
        self.startPoint["Y"] = int(sPoint[1][0])
        self.startPoint["Z"] = int(sPoint[2][0])
        self.endPoint["X"] = int(ePoint[0][0])
        self.endPoint["Y"] = int(ePoint[1][0])
        self.endPoint["Z"] = int(ePoint[2][0])
        self.speed = int(speed)

class CircularMovement(Movement):
    def __init__(self, id,sPoint,mPoint, ePoint, speed = 50):
        super().__init__("Circular", id)
        self.startPoint = {}
        self.midPoint = {}
        self.endPoint = {}
        
        self.startPoint["X"] = int(sPoint[0][0])
        self.startPoint["Y"] = int(sPoint[1][0])
        self.startPoint["Z"] = int(sPoint[2][0])
        self.midPoint["X"] = int(mPoint[0][0])
        self.midPoint["Y"] = int(mPoint[1][0])
        self.midPoint["Z"] = int(mPoint[2][0])
        self.endPoint["X"] = int(ePoint[0][0])
        self.endPoint["Y"] = int(ePoint[1][0])
        self.endPoint["Z"] = int(ePoint[2][0])
        self.speed = int(speed)


if __name__ == "__main__":
    lst = []

    for i in range(10):
        sP = np.random.randint(21,size= (3,1))
        mP = np.random.randint(21, size =(3,1))
        eP = np.random.randint(21, size =(3,1))
        s = np.random.randint(100)
        if i%3 == 0:
            lst.append(LinearMovement(id = i,sPoint= sP, ePoint=eP,speed= s).__dict__)
        elif i%3 == 1:
            lst.append(P2PMovement(id = i,sPoint= sP, ePoint=eP,speed= s).__dict__)
        elif i%3 == 2:
            lst.append(CircularMovement(id = i,sPoint= sP,mPoint=mP, ePoint=eP,speed= s).__dict__)         
    print(json.dumps(lst, indent=4))
    