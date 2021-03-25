import FreeCADGui as Gui
import FreeCAD as App


import RPWlib

import Part,PartGui


class TestCMD_1():

    def __init__(self):   
        pass

    def printObjectCenter(self):
        sel = Gui.Selection.getSelection()   
        mydoc = App.activeDocument().Name
        document_ = mydoc

        try:
            object_Label = sel[0].Label
            object_Name  = sel[0].Name
        except Exception:
            object_Label = ""
            object_Name  = ""
        try:
            SubElement = Gui.Selection.getSelectionEx()[0]   
            element_ = SubElement.SubObjects[0]
            
        except Exception:
            element_ = ""

        doc = App.activeDocument()
        try:
            doc.removeObject("Shape")
        except:
            App.Console.PrintMessage("no previous Center-Sphere found")
            App.Console.PrintMessage("\r\n")


        App.Console.PrintMessage("Type: {}\r\n".format(element_.ShapeType))


        if (element_.ShapeType == "Vertex"):
            pos = element_.Point
            App.Console.PrintMessage("x = {}\r\n".format(pos[0]))
            App.Console.PrintMessage("y = {}\r\n".format(pos[1]))
            App.Console.PrintMessage("z = {}\r\n".format(pos[2]))
            App.Console.PrintMessage("\r\n")
            s = Part.makeSphere(0.5,pos)
            Part.show(s)
        elif (element_.ShapeType == "Face"):
            pos = element_.BoundBox.Center
            normalVect = element_.normalAt(0,0)
            App.Console.PrintMessage("x = {}\r\n".format(pos[0]))
            App.Console.PrintMessage("y = {}\r\n".format(pos[1]))
            App.Console.PrintMessage("z = {}\r\n".format(pos[2]))
            App.Console.PrintMessage("normal Vector = {}\r\n".format(normalVect))
            App.Console.PrintMessage("\r\n")
            s = Part.makeSphere(0.5,pos)
            Part.show(s)
        elif (element_.ShapeType == "Edge"):
            startPoint = element_.Vertexes[0]
            endPoint = element_.Vertexes[1]
            direction = endPoint.Point - startPoint.Point
            pos = startPoint.Point + 0.5*direction
            App.Console.PrintMessage("start = {}\r\n".format(startPoint.Point))
            App.Console.PrintMessage("end = {}\r\n".format(endPoint.Point))
            App.Console.PrintMessage("center = {}\r\n".format(pos))
            App.Console.PrintMessage("direction = {}\r\n".format(direction))
            App.Console.PrintMessage("\r\n")
            s = Part.makeSphere(0.5,pos)
            Part.show(s)

class TestCMD_1_CMD():
    """My new command"""

    def GetResources(self):
        return {'Pixmap'  :  RPWlib.pathOfModule() + "/icons/WB_linSegCMD_2_icon.svg", # the name of a svg file available in the resources
                'Accel' : "", # a default shortcut (optional)
                'MenuText': "Print Center Point",
                'ToolTip' : "Print Selected Object Center Point"}

    def Activated(self):
        panel = TestCMD_1()
        panel.printObjectCenter()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

Gui.addCommand('Print_Selected_ObjectCenter',TestCMD_1_CMD())