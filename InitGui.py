import FreeCADGui as Gui
import FreeCAD as App


class RobotPathWorkbench(Workbench):

    def __init__(self):
        import RPWlib
        self.__class__.MenuText = "Robot Path Workbench"
        self.__class__.ToolTip = "A Workbench to create and export Paths for Robots"
        self.__class__.Icon = RPWlib.pathOfModule() + "/icons/WB_main_icon.svg"

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import CreateSeg
        import AddOrigin
        import AddPoints
        self.segmentCommands = ["Create_Linear_Segment","Create_P2P_Segment","Create_Circular_Segment"] # A list of command names created in the line above
        self.mainCommands = ["Add_Origin_Command", "Add_Points_Command"]

        self.appendToolbar("Main Commands",self.mainCommands)
        self.appendToolbar("Add Segment",self.segmentCommands) # creates a new toolbar with your commands
        
        
    def Activated(self):
        import RPWClasses
        import RPWlib
        import json
        from PySide import QtGui
        RPWlib.MovementList.List = []
        RPWlib.PointsList.List = []
        RPWlib.CSList.List = []
        
        RPWlib.config = RPWClasses.ProjectConfiguration()
        RPWlib.config.readConfig()
        RPWlib.config.writeConfig()
        
        App.ActiveDocument.recompute()

        try:
            mw = Gui.getMainWindow()
            c = mw.findChild(QtGui.QTextEdit, "Report view")
            c.clear()
        except Exception as e:
            App.Console.PrintError(e)
        """This function is executed when the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        #  # add commands to the context menu

    def GetClassName(self): 
        # This function is mandatory if this is a full python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"

Gui.addWorkbench(RobotPathWorkbench())