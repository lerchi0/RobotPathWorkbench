import FreeCADGui as Gui
import FreeCAD as App


class RobotPathWorkbench (Workbench):
    

    def __init__(self):
        import RPWlib
        self.__class__.MenuText = "Robot Path Workbench"
        self.__class__.ToolTip = "A Workbench to create and export Paths for Robots"
        self.__class__.Icon = RPWlib.pathOfModule() + "/icons/WB_main_icon.svg"

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import CreateSeg
        import AddOrigin
        import TestCMDs
        self.list = ["Add_Origin_Command","Create_Linear_Segment","Create_P2P_Segment","Create_Circular_Segment"] # A list of command names created in the line above
        self.testCMDs = ["Print_Selected_ObjectCenter"]
        self.appendToolbar("Add Segment",self.list) # creates a new toolbar with your commands
        
        
    def Activated(self):
        import RPWlib
        RPWlib.reloadMovementList()
        """This function is executed when the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("Test Commands",self.testCMDs) # add commands to the context menu

    def GetClassName(self): 
        # This function is mandatory if this is a full python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(RobotPathWorkbench())