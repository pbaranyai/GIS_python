#Works in ArcGIS Pro

import arcpy,sys

Tool = '\\FILELOCATION\GIS\ArcAutomations\GIS_Dept\Python\TopologyExport.py'
Report = '\\FILELOCATION\GIS\ArcAutomations\GIS_Dept\ArcProChecker.txt'

arcpy.AnalyzeToolsForPro_management(Tool, Report)
print(arcpy.GetMessages(1))
print ("  Report has been generated at:"+Report )

sys.exit()    
