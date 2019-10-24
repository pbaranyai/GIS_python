# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Planning_Data_Spreader.py
# Created on: 2019-10-01 
# Updated on 2019-10-01
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# Zoning Districts  
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import datetime
import os
import traceback
import logging
import __builtin__

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\Planning\\Planning_Data_Spreader.log"  
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())

try:
    # Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
    def write_log(text, file):
        f = open(file, 'a')           # 'a' will append to an existing file if it exists
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    print ("\n Unable to write log file")
    write_log("Unable to write log file", logfile)
    sys.exit ()

try:
    # Set the necessary product code (sets neccesary ArcGIS product license needed for tools running)
    import arceditor
except:
    print ("No ArcEditor (ArcStandard) license available")
    write_log("!!No ArcEditor (ArcStandard) license available!!", logfile)
    logging.exception('Got exception on importing ArcEditor (ArcStandard) license logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()

# Database variables:
CRAW_INTERNAL = "Database Connections\\craw_internal@ccsde.sde"
PLANNING = "Database Connections\\PLANNING@ccsde.sde"
OPEN_DATA = "Database Connections\\public_od@ccsde.sde"
PUBLIC_WEB = "Database Connections\\public_web@ccsde.sde"

# Local variables:
ZONING_PLANNING = PLANNING + "\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts"
ZONING_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL"
ZONING_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Land_Records\\CCSDE.PUBLIC_WEB.ZONING_DISTRICTS_WEB"

start_time = time.time()

print ("============================================================================")
print ("Updating Planning Datasets: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nZoning Districts Feature Class"  )
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Planning Datasets: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nZoning Districts Feature Class", logfile)  
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Zoning Districts - CRAW_INTERNAL from PLANNING")
write_log("\n Updating Zoning Districts - CRAW_INTERNAL from PLANNING: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Zoning Districts - CRAW_INTERNAL
    arcpy.DeleteRows_management(ZONING_INTERNAL)
except:
    print ("\n Unable to delete rows from Zoning Districts - CRAW_INTERNAL")
    write_log("Unable to delete rows from Zoning Districts - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Zoning Districts - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Zoning Districts - CRAW_INTERNAL from PLANNING
    arcpy.Append_management(ZONING_PLANNING, ZONING_INTERNAL, "NO_TEST", 'FIPS "FIPS" true true false 8 Double 8 38 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts,FIPS,-1,-1;MUNI_NAME "MUNICIPALITY" true true false 50 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts,MUNI_NAME,-1,-1;ZONING "ZONING" true true false 100 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts,ZONING,-1,-1;ORDINANCE "ORDINANCE" true true false 150 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts,ORDINANCE,-1,-1;ENACTED "ENACTED" true true false 50 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts,ENACTED,-1,-1;LAST_AMENDED "LAST AMENDED" true true false 50 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts,LAST_AMENDED,-1,-1;EDITED "EDITED" true true false 8 Date 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts,EDITED,-1,-1;GlobalID "GlobalID" false false true 38 GlobalID 0 0 ,First,#;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts,Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts,Shape.STLength(),-1,-1', "")
    Zoning_Dist_Internal_result = arcpy.GetCount_management(ZONING_INTERNAL)
    print ('{} has {} records'.format(ZONING_INTERNAL, Zoning_Dist_Internal_result[0]))
except:
    print ("\n Unable to append Zoning Districts - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append Zoning Districts - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append Zoning Districts - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Zoning Districts - CRAW_INTERNAL from PLANNING completed")
write_log("       Updating Zoning Districts - CRAW_INTERNAL from PLANNING completed", logfile)

print ("\n Updating Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Zoning Districts - PUBLIC_WEB
    arcpy.DeleteRows_management(ZONING_WEB)
except:
    print ("\n Unable to delete rows from Zoning Districts - PUBLIC_WEB")
    write_log("Unable to delete rows from Zoning Districts - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Zoning Districts - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(ZONING_INTERNAL, ZONING_WEB, "NO_TEST", 'FIPS "FIPS" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL,FIPS,-1,-1;MUNI_NAME "MUNICIPALITY" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL,MUNI_NAME,-1,-1;ZONING "ZONING" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL,ZONING,-1,-1;ORDINANCE "ORDINANCE" true true false 150 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL,ORDINANCE,-1,-1;ENACTED "ENACTED" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL,ENACTED,-1,-1;LAST_AMENDED "LAST AMENDED" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL,LAST_AMENDED,-1,-1;EDITED "EDITED" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL,EDITED,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL,GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL,Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL,Shape.STLength(),-1,-1', "")
    Zoning_Dist_Web_result = arcpy.GetCount_management(ZONING_WEB)
    print ('{} has {} records'.format(ZONING_WEB, Zoning_Dist_Web_result[0]))
except:
    print ("\n Unable to append Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL PLANNING DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL PLANNING DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
