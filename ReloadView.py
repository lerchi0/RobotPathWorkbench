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

import FreeCADGui as Gui
import FreeCAD as App
import RPWlib
import RPWClasses
class ReloadViewCmd():
    """My new command"""
        
    def GetResources(self):
        return {'Pixmap'  : RPWlib.pathOfModule() + "/icons/WB_newModule_icon.svg", # the name of a svg file available in the resources
                #'Accel' : "Shift+R", # a default shortcut (optional)
                'MenuText': "Reload 3D View",
                'ToolTip' : "Reload 3D View"}

    def Activated(self):
        try:
            doc = App.ActiveDocument
            path = doc.getObject("Path")
            pts = doc.getObject("Points")
            cs = doc.getObject("Coordinate_Systems")
            RPWClasses.delWithChildren(path)
            RPWClasses.delWithChildren(pts)
            RPWClasses.delWithChildren(cs)
        except:
            pass
        try:
            RPWlib.MovementList.pathGrp = doc.addObject("App::DocumentObjectGroup", "Path")
            RPWlib.PointsList.pointsGrp = doc.addObject("App::DocumentObjectGroup", "Points")
            RPWlib.CSList.csGrp = doc.addObject("App::DocumentObjectGroup", "Coordinate_Systems")
        except Exception as e:
            App.Console.PrintMessage(e)

        try:
            for cs in RPWlib.CSList.List:
                cs.selfDraw(cs.name,1)
            for id,pt in enumerate(RPWlib.PointsList.List):
                pt.selfDraw(f"Point_{id}", 2)
            for mv in RPWlib.MovementList.List:
                mv.selfdraw()
        except Exception as e:
            App.Console.PrintMessage(e)  
        return True

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

Gui.addCommand('Reload_View_Command',ReloadViewCmd())