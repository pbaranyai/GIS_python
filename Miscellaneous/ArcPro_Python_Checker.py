#Works in ArcGIS Pro

import arcpy

Tool = 'R:\GIS\ArcAutomations\GIS_Dept\Python\TopologyExport.py'
Report = 'R:\GIS\ArcAutomations\GIS_Dept\ArcProChecker.txt'

arcpy.AnalyzeToolsForPro_management(Tool, Report)

print(arcpy.GetMessages(1))

print ("  Report has been generated")

del arcpy
sys.exit()    
