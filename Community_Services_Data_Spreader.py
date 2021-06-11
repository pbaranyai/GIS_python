# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Community_Services_Data_Spreader.py
# Created on: 2020-04-21 
# Updated on: 2020-04-21
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# CRAWFORD_FOOD_PANTRIES  
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
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Community_Services_Data_Spreader.log"  
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

# Local variables:
CRAWFORD_FOOD_PANTRIES_GIS = GIS + "\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES"
CRAWFORD_FOOD_PANTRIES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Community_Services\\CCSDE.CRAW_INTERNAL.CRAWFORD_FOOD_PANTRIES_INTERNAL"

start_time = time.time()

print ("============================================================================")
print ("Updating Community Services Datasets: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nCrawford Food Pantries Feature Class"  )
print ("\n From source to CRAW_INTERNAL")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Community Services Datasets: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nCrawford Food Pantries Feature Class", logfile)  
write_log("\n From source to CRAW_INTERNAL", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Crawford Food Pantries - CRAW_INTERNAL from GIS")
write_log("\n Updating Crawford Food Pantries - CRAW_INTERNAL from GIS: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Crawford Food Pantries - CRAW_INTERNAL
    arcpy.DeleteRows_management(CRAWFORD_FOOD_PANTRIES_INTERNAL)
except:
    print ("\n Unable to delete rows from Crawford Food Pantries - CRAW_INTERNAL")
    write_log("Unable to delete rows from Crawford Food Pantries - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Crawford Food Pantries - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Crawford Food Pantries - CRAW_INTERNAL from GIS
    arcpy.Append_management(CRAWFORD_FOOD_PANTRIES_GIS, CRAWFORD_FOOD_PANTRIES_INTERNAL, "NO_TEST", 'PANTRY_NAME "Pantry Name" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,PANTRY_NAME,-1,-1;STREET_ADDRESS "911 Street Address" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,STREET_ADDRESS,-1,-1;ADDRESS_POST_OFFICE "Post Office" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,ADDRESS_POST_OFFICE,-1,-1;ADDRESS_STATE "State" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,ADDRESS_STATE,-1,-1;ADDRESS_ZIPCODE "Zipcode" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,ADDRESS_ZIPCODE,-1,-1;PHONE_NUMBER "Phone Number" true true false 30 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,PHONE_NUMBER,-1,-1;CONTACT "Contact" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,CONTACT,-1,-1;ZIP_CODES_SERVED "Zipcodes served" true true false 200 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,ZIP_CODES_SERVED,-1,-1;HOURS_OF_OPERATION "Hours of Operation" true true false 150 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,HOURS_OF_OPERATION,-1,-1;WEBSITE "Website" true true false 200 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,WEBSITE,-1,-1;DATE_ADDED "Date Added" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,DATE_ADDED,-1,-1;DATE_UPDATED "Date Updated" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,DATE_UPDATED,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Community_Services\\CCSDE.GIS.CRAWFORD_FOOD_PANTRIES,GlobalID,-1,-1', "")
    FoodPantry_Internal_result = arcpy.GetCount_management(CRAWFORD_FOOD_PANTRIES_INTERNAL)
    print ('{} has {} records'.format(CRAWFORD_FOOD_PANTRIES_INTERNAL, FoodPantry_Internal_result[0]))
except:
    print ("\n Unable to append Crawford Food Pantries - CRAW_INTERNAL from GIS")
    write_log("Unable to append Crawford Food Pantries - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Crawford Food Pantries - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Crawford Food Pantries - CRAW_INTERNAL from GIS completed")
write_log("       Updating Crawford Food Pantries - CRAW_INTERNAL from GIS completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL Community Services DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL Community Services DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
