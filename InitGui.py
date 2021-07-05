import FreeCADGui as Gui
import FreeCAD as App


class RobotPathWorkbench(Gui.Workbench):
    def __init__(self):
        import RPWlib
        self.__class__.MenuText = "Robot Path Workbench"
        self.__class__.ToolTip = "A Workbench to create and export Paths for Robots"
        self.__class__.Icon = RPWlib.pathOfModule() + "/icons/WB_main_icon.svg"

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        import CreateSeg, AddOrigin, AddPoints, NewModule, ShowPath
        self.segmentCommands = ["Create_Linear_Segment","Create_P2P_Segment","Create_Circular_Segment"] # A list of command names created in the line above
        self.mainCommands = ["Add_Origin_Command", "Add_Points_Command"]
        self.advancedCommands = ["Add_New_Module_Command"]
        self.RPWMenu = ["Edit_Path_Command"]
        self.appendToolbar("Main Commands",self.mainCommands)
        self.appendToolbar("Add Segment",self.segmentCommands) 
        self.appendToolbar("Advanced Commands",self.advancedCommands) # creates a new toolbar with your commands
        
        
    
        
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
        try:
            RPWlib.mainCMDs = mw.findChild(QtGui.QToolBar, "Main Commands")
            RPWlib.addSegCMDs = mw.findChild(QtGui.QToolBar, "Add Segment")
            RPWlib.newModCMDs = mw.findChild(QtGui.QToolBar, "Advanced Commands")
            RPWlib.mainCMDs.show()
            RPWlib.addSegCMDs.show()
            RPWlib.newModCMDs.show()
        except Exception as e:
            App.Console.PrintError(e)
        return

    def Deactivated(self):
        """This function is executed when the workbench is deactivated"""
        return

    def ContextMenu(self,recipient):
        self.appendContextMenu(["RPW Commands", "Path"],self.RPWMenu)

    def GetClassName(self): 
        # This function is mandatory if this is a full python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"

Gui.addWorkbench(RobotPathWorkbench)