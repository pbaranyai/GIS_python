# ---------------------------------------------------------------------------
# Assessment_Historic_Tracks_Updater.py
# Created on: 2021-10-19 
# Updated on 2021-10-19 
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from AST to CRAW_INTERNAL:
#  
# Tracks
# 
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
# ---------------------------------------------------------------------------

import arcpy
import sys
import datetime
import time,sys
import logging

# Stop geoprocessing log history in metadata
arcpy.SetLogHistory(False)

# Setup error logging
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\Assessment\\Assessment_Historic_Tracks_Updater.log"  
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())
today = datetime.date.today()

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
Database_Connections = r"\\FILELOCATION\\GIS\\ArcAutomations\\Database_Connections"

#Database variables:
AST = Database_Connections + "\\AST@ccsde.sde"
CRAW_INTERNAL = Database_Connections + "\\craw_internal@ccsde.sde"

# Local variables:
ASMT_TRACKS_AST = AST + "\\CCSDE.AST.Assessment_Field_Tracks\\CCSDE.AST.Assessment_Historic_Tracks"
ASMT_TRACKS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Assessment_Field_Tracks\\CCSDE.CRAW_INTERNAL.Assessment_Historic_Tracks"


start_time = time.time()

print ("============================================================================")
print (("Updating Tracker data feature classes: "+ str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\nAssessment Historic Tracks")
print ("\n From source to CRAW_INTERNAL")
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Tracker feature classes: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nAssessment Historic Tracks", logfile)  
write_log("\n From source to CRAW_INTERNAL", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Assessment Historic Tracks - CRAW_INTERNAL from AST")
write_log("\n Updating Assessment Historic Tracks - CRAW_INTERNAL from AST: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Assessment Historic Tracks - CRAW_INTERNAL
    arcpy.management.DeleteRows(ASMT_TRACKS_INTERNAL)
except:
    print ("\n Unable to Delete Rows from Assessment Historic Tracks - CRAW_INTERNAL")
    write_log("Unable to Delete Rows from Assessment Historic Tracks - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on Delete Rows from Assessment Historic Tracks - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append Assessment Historic Tracks - CRAW_INTERNAL from AST
    arcpy.management.Append(ASMT_TRACKS_AST, ASMT_TRACKS_INTERNAL, "NO_TEST", r'globalid "GlobalID" false false false 38 GlobalID 0 0,First,#,'+ASMT_TRACKS_AST+',globalid,-1,-1;activity "Activity" true true false 4 Long 0 10,First,#,'+ASMT_TRACKS_AST+',activity,-1,-1;altitude "Altitude" true true false 8 Double 8 38,First,#,'+ASMT_TRACKS_AST+',altitude,-1,-1;app_id "Application ID" true true false 255 Text 0 0,First,#,'+ASMT_TRACKS_AST+',app_id,0,255;battery_percentage "Battery Percentage" true true false 8 Double 8 38,First,#,'+ASMT_TRACKS_AST+',battery_percentage,-1,-1;battery_state "Battery State" true true false 4 Long 0 10,First,#,'+ASMT_TRACKS_AST+',battery_state,-1,-1;course "Course" true true false 8 Double 8 38,First,#,'+ASMT_TRACKS_AST+',course,-1,-1;device_id "Device ID" true true false 255 Text 0 0,First,#,'+ASMT_TRACKS_AST+',device_id,0,255;floor "Floor" true true false 4 Long 0 10,First,#,'+ASMT_TRACKS_AST+',floor,-1,-1;horizontal_accuracy "Horizontal Accuracy" true true false 8 Double 8 38,First,#,'+ASMT_TRACKS_AST+',horizontal_accuracy,-1,-1;location_source "Location Source" true true false 255 Text 0 0,First,#,'+ASMT_TRACKS_AST+',location_source,0,255;location_timestamp "Location Timestamp" true true false 8 Date 0 0,First,#,'+ASMT_TRACKS_AST+',location_timestamp,-1,-1;session_id "Session ID" true true false 255 Text 0 0,First,#,'+ASMT_TRACKS_AST+',session_id,0,255;signal_strength "Signal Strength" true true false 8 Double 8 38,First,#,'+ASMT_TRACKS_AST+',signal_strength,-1,-1;speed "Speed" true true false 8 Double 8 38,First,#,'+ASMT_TRACKS_AST+',speed,-1,-1;vertical_accuracy "Vertical Accuracy" true true false 8 Double 8 38,First,#,'+ASMT_TRACKS_AST+',vertical_accuracy,-1,-1;full_name "Full Name" true true false 255 Text 0 0,First,#,'+ASMT_TRACKS_AST+',full_name,0,255;category "Category" true true false 255 Text 0 0,First,#,'+ASMT_TRACKS_AST+',category,0,255;created_user "Created User" true true false 255 Text 0 0,First,#,'+ASMT_TRACKS_AST+',created_user,0,255;created_date "Created Date" true true false 8 Date 0 0,First,#,'+ASMT_TRACKS_AST+',created_date,-1,-1;last_edited_user "Last Edited User" true true false 255 Text 0 0,First,#,'+ASMT_TRACKS_AST+',last_edited_user,0,255;last_edited_date "Last Edited Date" true true false 8 Date 0 0,First,#,'+ASMT_TRACKS_AST+',last_edited_date,-1,-1;Municipality "Municipality" true true false 255 Text 0 0,First,#,'+ASMT_TRACKS_AST+',Municipality,0,255', '', '')
    ASMT_Tracks_result = arcpy.GetCount_management(ASMT_TRACKS_INTERNAL)
    print ('{} has {} records'.format(ASMT_TRACKS_INTERNAL, ASMT_Tracks_result[0]))
    write_log('{} has {} records'.format(ASMT_TRACKS_INTERNAL, ASMT_Tracks_result[0]),logfile)
except:
    print ("\n Unable append to Assessment Historic Tracks - CRAW_INTERNAL from AST")
    write_log("Unable to append Assessment Historic Tracks - CRAW_INTERNAL from AST", logfile)
    logging.exception('Got exception on append Assessment Historic Tracks - CRAW_INTERNAL from AST logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Assessment Historic Tracks - CRAW_INTERNAL from AST completed")
write_log("       Updating Assessment Historic Tracks - CRAW_INTERNAL from AST completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n ALL TRACKER FEATURE CLASSES UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("\n ALL TRACKER FEATURE CLASSES UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print (("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)))
write_log("Elapsed time: " + str (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
