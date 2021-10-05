# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Active_VISION_Missing_GIS.py
# Created on: 2021-07-19
# Updated on 2021-07-19
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
#
# Description: 
# Geocode the VIS_REALMAST_TBL (active records only), filter out unmatched records and export to R:\GIS\Assessment\Reports as excel file
#
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import datetime
import os
import traceback
import logging

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\Assessment\\Active_VISION_Missing_GIS.log"  
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

#Database Connection Folder
Database_Connections = r"\\CCFILE\\anybody\\GIS\\ArcAutomations\\Database_Connections"

#Database variables:
AUTOWORKSPACE = Database_Connections + "\\auto_workspace@ccsde.sde"
ASMT_REPORT_FLDR = r"\\CCFILE\\anybody\\GIS\\Assessment\\Reports"
LOCATOR_WKSP = r"\\CCFILE\\anybody\\GIS\\CurrentWebsites\\Locators\\Intranet_Locators"

# Local variables:
MISSING_GIS_REPORT = ASMT_REPORT_FLDR + "\\Active_VISION_Missing_GIS.xls"
MISSING_GIS_GEOCODE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Active_VISION_Missing_GIS_Geocode"
CC_PARCEL_LOC = LOCATOR_WKSP + "\\CAMA_PID_Locator"

# Local variables - tables:
VISION_REALMAST_TBL_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL"

start_time = time.time()

print ("============================================================================")
print ("Creating Active VISION record missing from GIS Report: "+ str(Day) + " " + str(Time))
print ("Located at: R:\GIS\Assessment\Reports")
print ("Works in ArcGIS Pro")
print ("============================================================================")
write_log("============================================================================", logfile)
write_log("Creating Active VISION record missing from GIS Report: "+ str(Day) + " " + str(Time), logfile)
write_log("Located at: R:\GIS\Assessment\Reports", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Deleting excel file & Geocoding all VISION records")
write_log("\n Deleting excel file & Geocoding all VISION records",logfile)

try:
    # Delete excel file so it can be replaced
    if arcpy.Exists(MISSING_GIS_REPORT):
        os.remove(MISSING_GIS_REPORT)
        #arcpy.Delete_management(MISSING_GIS_REPORT, "Table")
        print (MISSING_GIS_REPORT + " found - table deleted")
        write_log(MISSING_GIS_REPORT + " found - table deleted", logfile)
except:
    print ("\n Unable to delete "+MISSING_GIS_REPORT+", need to delete existing FGDB manually and/or close program locking the tables")
    write_log("\n Unable to delete "+MISSING_GIS_REPORT+", need to delete existing FGDB manually and/or close program locking the tables", logfile)
    logging.exception('Got exception on Unable to delete '+MISSING_GIS_REPORT+', need to delete existing FGDB manually and/or close program locking the tables logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Delete rows from MISSING_GIS_GEOCODE in AUTOWORKSPACE (prep existing FC, by cleaning out rows)
    arcpy.DeleteRows_management(MISSING_GIS_GEOCODE)
except:
    print ("\n Unable to delete rows from MISSING_GIS_GEOCODE")
    write_log("\n Unable to delete rows from MISSING_GIS_GEOCODE", logfile)
    logging.exception('Got exception on delete rows from MISSING_GIS_GEOCODE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Geocode VIS_REALMAST_TBL in AUTOWORKSPACE against CC_PARCEL_Locator, into "memory"
    VIS_REALMAST_GEOCODE = arcpy.geocoding.GeocodeAddresses(VISION_REALMAST_TBL_SDE, CC_PARCEL_LOC, "'Single Line Input' REM_PID VISIBLE NONE", "in_memory/VIS_REALMAST_GEOCODE", "STATIC", None, '', None, "ALL")
    print ("\n Geocoding REALMAST Table into memory")
    write_log ("\n Geocoding REALMAST Table into memory", logfile)
except:
    print ("\n Unable to Geocode VIS_REALMAST_TBL in AUTOWORKSPACE against CC_PARCEL_Locator, into memory")
    write_log("\n Unable to Geocode VIS_REALMAST_TBL in AUTOWORKSPACE against CC_PARCEL_Locator, into memory", logfile)
    logging.exception('Got exception on Geocode VIS_REALMAST_TBL in AUTOWORKSPACE against CC_PARCEL_Locator, into memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT
    arcpy.management.Append(VIS_REALMAST_GEOCODE, MISSING_GIS_GEOCODE, "NO_TEST", r'REM_PID "REM_PID" true true false 4 Long 0 10,First,#,in_memory/VIS_REALMAST_GEOCODE,USER_REM_PID,-1,-1;REM_PARCEL_STATUS "REM_PARCEL_STATUS" true true false 1 Text 0 0,First,#,in_memory/VIS_REALMAST_GEOCODE,USER_REM_PARCEL_STATUS,0,1;STATUS "STATUS" true true false 50 Text 0 0,First,#,in_memory/VIS_REALMAST_GEOCODE,Status,0,1', '', '')
    print ("\n   Appending VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT")
    write_log ("\n   Appending VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT", logfile)
except:
    print ("\n Unable to Append VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT")
    write_log("\n Unable to Append VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT", logfile)
    logging.exception('Got exception on Append VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for (keeps in_memory from getting overloaded or corrupted)
    arcpy.Delete_management("in_memory")
except:
    print ("\n Unable to clear VIS_REALMAST_GEOCODE from in_memory")
    write_log("Unable to clear VIS_REALMAST_GEOCODE from in_memory", logfile)
    logging.exception('Got exception on clear VIS_REALMAST_GEOCODE from in_memory logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Make Feature Layer of MISSING_GIS_GEOCODE, selecting only unmatched records
    Unmatched_Geocoded_VISION_Records = arcpy.MakeFeatureLayer_management(MISSING_GIS_GEOCODE, "Unmatched_Geocoded_VISION_Records", "STATUS = 'U' AND REM_PARCEL_STATUS = 'A'", "", "OBJECTID OBJECTID VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;REM_PARCEL_STATUS REM_PARCEL_STATUS VISIBLE NONE;STATUS STATUS VISIBLE NONE;SHAPE SHAPE VISIBLE NONE")
except:
    print ("\n Unable to Append VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT")
    write_log("\n Unable to Append VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT", logfile)
    logging.exception('Got exception on Append VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Export unmatched records to excel
    arcpy.TableToExcel_conversion(Unmatched_Geocoded_VISION_Records, MISSING_GIS_REPORT, "ALIAS", "DESCRIPTION")
    print ("\n Exporting unmatched records report to: R:\GIS\Assessment\Reports")
    write_log("\n Exporting unmatched records report to: R:\GIS\Assessment\Reports", logfile)
except:
    print ("\n Unable to Export unmatched records to excel")
    write_log("\n Unable to Export unmatched records to excel", logfile)
    logging.exception('Got exception on Export unmatched records to excel logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("         Exporting update table to excel file at R:\GIS\Assessment\Reports completed")
write_log("         Exporting update table to excel file at R:\GIS\Assessment\Reports completed", logfile)


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n Active VISION record missing from GIS REPORT HAS BEEN UPDATED: " + str(Day) + " " + str(end_time))
write_log("\n Active VISION record missing from GIS REPORT HAS BEEN UPDATED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()

