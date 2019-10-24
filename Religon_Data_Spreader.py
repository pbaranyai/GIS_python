# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Religon_Data_Spreader.py
# Created on: 2019-03-05 
# Updated on 2019-04-25
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# CEMETERIES  
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
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Religion_Data_Spreader.log"  
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
GIS = "Database Connections\\GIS@ccsde.sde"
OPEN_DATA = "Database Connections\\public_od@ccsde.sde"
PUBLIC_WEB = "Database Connections\\public_web@ccsde.sde"

# Local variables:
CEMETERIES_GIS = GIS + "\\CCSDE.GIS.Religion\\CCSDE.GIS.Cemeteries"
CEMETERIES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Religion\\CCSDE.CRAW_INTERNAL.CEMETERIES_INTERNAL"
CEMETERIES_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Religion\\CCSDE.PUBLIC_WEB.CEMETERIES_WEB"

start_time = time.time()

print ("============================================================================")
print ("Updating Religon Datasets: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nCemeteries Feature Class"  )
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Religon Datasets: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nCemeteries Feature Class", logfile)  
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Cemeteries - CRAW_INTERNAL from GIS")
write_log("\n Updating Cemeteries - CRAW_INTERNAL from GIS: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Cemeteries - CRAW_INTERNAL
    arcpy.DeleteRows_management(CEMETERIES_INTERNAL)
except:
    print ("\n Unable to delete rows from Cemeteries - CRAW_INTERNAL")
    write_log("Unable to delete rows from Cemeteries - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Cemeteries - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Cemeteries - CRAW_INTERNAL from GIS
    arcpy.Append_management(CEMETERIES_GIS, CEMETERIES_INTERNAL, "NO_TEST", "NAME \"NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Religion\\CCSDE.GIS.Cemeteries,NAME,-1,-1;ACCESS_ROAD \"ACCESS ROAD\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Religion\\CCSDE.GIS.Cemeteries,ACCESS_ROAD,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Religion\\CCSDE.GIS.Cemeteries,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Religion\\CCSDE.GIS.Cemeteries,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Religion\\CCSDE.GIS.Cemeteries,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Religion\\CCSDE.GIS.Cemeteries,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Religion\\CCSDE.GIS.Cemeteries,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    Cemetery_Internal_result = arcpy.GetCount_management(CEMETERIES_INTERNAL)
    print ('{} has {} records'.format(CEMETERIES_INTERNAL, Cemetery_Internal_result[0]))
except:
    print ("\n Unable to append Cemeteries - CRAW_INTERNAL from GIS")
    write_log("Unable to append Cemeteries - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Cemeteries - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Cemeteries - CRAW_INTERNAL from GIS completed")
write_log("       Updating Cemeteries - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Cemeteries - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Cemeteries - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Cemeteries - PUBLIC_WEB
    arcpy.DeleteRows_management(CEMETERIES_WEB)
except:
    print ("\n Unable to delete rows from Cemeteries - PUBLIC_WEB")
    write_log("Unable to delete rows from Cemeteries - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Cemeteries - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append Cemeteries - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(CEMETERIES_INTERNAL, CEMETERIES_WEB, "NO_TEST", "NAME \"NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Religion\\CCSDE.CRAW_INTERNAL.CEMETERIES_INTERNAL,NAME,-1,-1;ACCESS_ROAD \"ACCESS ROAD\" true true false 75 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Religion\\CCSDE.CRAW_INTERNAL.CEMETERIES_INTERNAL,ACCESS_ROAD,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Religion\\CCSDE.CRAW_INTERNAL.CEMETERIES_INTERNAL,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Religion\\CCSDE.CRAW_INTERNAL.CEMETERIES_INTERNAL,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Religion\\CCSDE.CRAW_INTERNAL.CEMETERIES_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Religion\\CCSDE.CRAW_INTERNAL.CEMETERIES_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Religion\\CCSDE.CRAW_INTERNAL.CEMETERIES_INTERNAL,UPDATE_DATE,-1,-1", "")
    Cemetery_Web_result = arcpy.GetCount_management(CEMETERIES_WEB)
    print ('{} has {} records'.format(CEMETERIES_WEB, Cemetery_Web_result[0]))
except:
    print ("\n Unable to append Cemeteries - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Cemeteries - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Cemeteries - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Cemeteries - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Cemeteries - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL RELIGON DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL RELIGON DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
