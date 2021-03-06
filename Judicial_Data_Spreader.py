# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Judicial_Data_Spreader.py
# Created on: 2020-01-14 
# Updated on 2020-01-14
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# MAGISTERIAL_DISTRICTS  
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
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Judicial_Data_Spreader.log"  
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
MAGISTERIAL_DISTRICTS_GIS = GIS + "\\CCSDE.GIS.Judicial\\CCSDE.GIS.Magisterial_Districts"
MAGISTERIAL_DISTRICTS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.MAGISTERIAL_DISTRICTS_INTERNAL"
MAGISTERIAL_DISTRICTS_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Boundaries\\CCSDE.PUBLIC_WEB.MAGISTERIAL_DISTRICTS_WEB"

start_time = time.time()

print ("============================================================================")
print ("Updating Judicial Datasets: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nMagisterial Districts Feature Class"  )
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Judicial Datasets: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nMagisterial Districts Feature Class", logfile)  
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Magisterial Districts - CRAW_INTERNAL from GIS")
write_log("\n Updating Magisterial Districts - CRAW_INTERNAL from GIS: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Magisterial Districts - CRAW_INTERNAL
    arcpy.DeleteRows_management(MAGISTERIAL_DISTRICTS_INTERNAL)
except:
    print ("\n Unable to delete rows from Magisterial Districts - CRAW_INTERNAL")
    write_log("Unable to delete rows from Magisterial Districts - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Magisterial Districts - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Magisterial Districts - CRAW_INTERNAL from GIS
    arcpy.Append_management(MAGISTERIAL_DISTRICTS_GIS, MAGISTERIAL_DISTRICTS_INTERNAL, "NO_TEST", 'DISTRICT "District #" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\CCSDE.GIS.Judicial\\CCSDE.GIS.Magisterial_Districts,DISTRICT,-1,-1;MAGISTRATE "Magistrate Name" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\CCSDE.GIS.Judicial\\CCSDE.GIS.Magisterial_Districts,MAGISTRATE,-1,-1;UPDATED_DATE "Date Updated" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\CCSDE.GIS.Judicial\\CCSDE.GIS.Magisterial_Districts,UPDATED_DATE,-1,-1;COUNTY_NAME "County Name" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\CCSDE.GIS.Judicial\\CCSDE.GIS.Magisterial_Districts,COUNTY_NAME,-1,-1;COUNTY_FIPS "County FIPS" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\CCSDE.GIS.Judicial\\CCSDE.GIS.Magisterial_Districts,COUNTY_FIPS,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\CCSDE.GIS.Judicial\\CCSDE.GIS.Magisterial_Districts,Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\CCSDE.GIS.Judicial\\CCSDE.GIS.Magisterial_Districts,Shape.STLength(),-1,-1', "")
    Magisterial_Districts_Internal_result = arcpy.GetCount_management(MAGISTERIAL_DISTRICTS_INTERNAL)
    print ('{} has {} records'.format(MAGISTERIAL_DISTRICTS_INTERNAL, Magisterial_Districts_Internal_result[0]))
except:
    print ("\n Unable to append Magisterial Districts - CRAW_INTERNAL from GIS")
    write_log("Unable to append Magisterial Districts - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Magisterial Districts - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Magisterial Districts - CRAW_INTERNAL from GIS completed")
write_log("       Updating Magisterial Districts - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Magisterial Districts - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Magisterial Districts - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Magisterial Districts - PUBLIC_WEB
    arcpy.DeleteRows_management(MAGISTERIAL_DISTRICTS_WEB)
except:
    print ("\n Unable to delete rows from Magisterial Districts - PUBLIC_WEB")
    write_log("Unable to delete rows from Magisterial Districts - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Magisterial Districts - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append Magisterial Districts - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(MAGISTERIAL_DISTRICTS_INTERNAL, MAGISTERIAL_DISTRICTS_WEB, "NO_TEST", 'DISTRICT "District #" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.MAGISTERIAL_DISTRICTS_INTERNAL,DISTRICT,-1,-1;MAGISTRATE "Magistrate Name" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.MAGISTERIAL_DISTRICTS_INTERNAL,MAGISTRATE,-1,-1;UPDATED_DATE "Date Updated" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.MAGISTERIAL_DISTRICTS_INTERNAL,UPDATED_DATE,-1,-1;COUNTY_NAME "County Name" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.MAGISTERIAL_DISTRICTS_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS "County FIPS" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.MAGISTERIAL_DISTRICTS_INTERNAL,COUNTY_FIPS,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.MAGISTERIAL_DISTRICTS_INTERNAL,Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.MAGISTERIAL_DISTRICTS_INTERNAL,Shape.STLength(),-1,-1', "")
    Magisterial_Districts_Web_result = arcpy.GetCount_management(MAGISTERIAL_DISTRICTS_WEB)
    print ('{} has {} records'.format(MAGISTERIAL_DISTRICTS_WEB, Magisterial_Districts_Web_result[0]))
except:
    print ("\n Unable to append Magisterial Districts - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Magisterial Districts - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Magisterial Districts - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Magisterial Districts - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Magisterial Districts - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL JUDICIAL DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL JUDICIAL DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
