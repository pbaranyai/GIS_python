# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Recreational_Data_Spreader.py
# Created on: 2019-03-05 
# Updated on 2021-09-21
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# CAMPGROUNDS  
# FISH_BOAT_ACCESS
# RECREATIONAL TRAILS
# TRAIL EMERGENCY ACCESS
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
# ---------------------------------------------------------------------------

# Import arcpy module
import sys
import arcpy
import datetime
import os
import traceback
import logging

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Recreational_Data_Spreader.log"  
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

# Database variables:
CRAW_INTERNAL = Database_Connections + "\\craw_internal@ccsde.sde"
GIS = Database_Connections + "\\GIS@ccsde.sde"
    
# Local variables:
CAMPGROUNDS_GIS = GIS + "\\CCSDE.GIS.Recreational\\CCSDE.GIS.CAMPGROUNDS"
CAMPGROUNDS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Recreational\\CCSDE.CRAW_INTERNAL.CAMPGROUNDS_INTERNAL"
FISH_BOAT_ACCESS_GIS = GIS + "\\CCSDE.GIS.Recreational\\CCSDE.GIS.FISH_BOAT_ACCESS"
FISH_BOAT_ACCESS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Recreational\\CCSDE.CRAW_INTERNAL.FISH_BOAT_ACCESS_INTERNAL"
RECREATIONAL_TRAILS_GIS = GIS + "\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS"
RECREATIONAL_TRAILS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Recreational\\CCSDE.CRAW_INTERNAL.RECREATIONAL_TRAILS_INTERNAL"
TRAIL_EMERGENCY_ACCESS_GIS = GIS + "\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS"
TRAIL_EMERGENCY_ACCESS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Recreational\\CCSDE.CRAW_INTERNAL.TRAIL_EMEGNCY_ACCESS_INTERNAL"

start_time = time.time()

print ("============================================================================")
print ("Updating Land Records: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nCampgrounds Feature Class")
print ("Fish & Boat Access Feature Class")
print ("Recreational Trails Feature Class")
print ("Trail Emergency Access Feature Class")
print ("\n From source to CRAW_INTERNAL")
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Land Records: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nCampgrounds Feature Class", logfile)  
write_log("Fish & Boat Access Feature Class", logfile) 
write_log("Recreational Trails Feature Class", logfile)
write_log("Trail Emergency Access Feature Class", logfile)
write_log("\n From source to CRAW_INTERNAL", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Campgrounds - CRAW_INTERNAL from GIS")
write_log("\n Updating Campgrounds - CRAW_INTERNAL from GIS: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Campgrounds - CRAW_INTERNAL
    arcpy.DeleteRows_management(CAMPGROUNDS_INTERNAL)
except:
    print ("\n Unable to delete rows from Campgrounds - CRAW_INTERNAL")
    write_log("Unable to delete rows from Campgrounds - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Campgrounds - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append Campgrounds - CRAW_INTERNAL from GIS
    arcpy.Append_management(CAMPGROUNDS_GIS, CAMPGROUNDS_INTERNAL, "NO_TEST", "CAMPGROUND_NAME \"CAMPGROUND NAME\" true true false 150 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.CAMPGROUNDS,CAMPGROUND_NAME,-1,-1;SITE_ID \"SITE ID\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.CAMPGROUNDS,SITE_ID,-1,-1;TYPE \"TYPE\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.CAMPGROUNDS,TYPE,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.CAMPGROUNDS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNI FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.CAMPGROUNDS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.CAMPGROUNDS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.CAMPGROUNDS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE_DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.CAMPGROUNDS,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    Campground_Internal_result = arcpy.GetCount_management(CAMPGROUNDS_INTERNAL)
    print ('{} has {} records'.format(CAMPGROUNDS_INTERNAL, Campground_Internal_result[0]))
except:
    print ("\n Unable to append Campgrounds - CRAW_INTERNAL from GIS")
    write_log("Unable to append Campgrounds - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Campgrounds - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Campgrounds - CRAW_INTERNAL from GIS completed")
write_log("       Updating Campgrounds - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Fish & Boat Access - CRAW_INTERNAL from GIS")
write_log("\n Updating Fish & Boat Access - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Fish & Boat Access - CRAW_INTERNAL
    arcpy.DeleteRows_management(FISH_BOAT_ACCESS_INTERNAL)
except:
    print ("\n Unable to delete rows from Fish & Boat Access - CRAW_INTERNAL")
    write_log("Unable to delete rows from Fish & Boat Access - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on Unable to delete rows from Fish & Boat Access - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Fish & Boat Access - CRAW_INTERNAL from GIS
    arcpy.Append_management(FISH_BOAT_ACCESS_GIS, FISH_BOAT_ACCESS_INTERNAL, "NO_TEST", "ACCESS_NAME \"ACCESS NAME\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.FISH_BOAT_ACCESS,ACCESS_NAME,-1,-1;WATER_BODY \"WATER BODY\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.FISH_BOAT_ACCESS,WATER_BODY,-1,-1;OWNER \"OWNER\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.FISH_BOAT_ACCESS,OWNER,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.FISH_BOAT_ACCESS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNI FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.FISH_BOAT_ACCESS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.FISH_BOAT_ACCESS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.FISH_BOAT_ACCESS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE_DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.FISH_BOAT_ACCESS,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    Fish_Boat_Internal_result = arcpy.GetCount_management(FISH_BOAT_ACCESS_INTERNAL)
    print ('{} has {} records'.format(FISH_BOAT_ACCESS_INTERNAL, Fish_Boat_Internal_result[0]))
except:
    print ("\n Unable to append Fish & Boat Access - CRAW_INTERNAL from GIS")
    write_log("Unable to append Fish & Boat Access - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Fish & Boat Access - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Fish & Boat Access - CRAW_INTERNAL from GIS completed")
write_log("       Updating Fish & Boat Access - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Recreational Trails - CRAW_INTERNAL from GIS")
write_log("\n Updating Recreational Trails - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Recreational Trials  - CRAW_INTERNAL
    arcpy.DeleteRows_management(RECREATIONAL_TRAILS_INTERNAL)
except:
    print ("\n Unable to delete rows from Recreational Trials  - CRAW_INTERNAL")
    write_log("Unable to delete rows from Recreational Trials  - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on Unable to delete rows from Recreational Trials  - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append_Internal Recreational Trails - CRAW_INTERNAL from GIS
    arcpy.Append_management(RECREATIONAL_TRAILS_GIS, RECREATIONAL_TRAILS_INTERNAL, "NO_TEST", "NAME \"NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,NAME,-1,-1;TYPE \"TYPE\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,TYPE,-1,-1;MAINTENANCE \"MAINTENANCE\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,MAINTENANCE,-1,-1;CONTACT \"CONTACT\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,CONTACT,-1,-1;SURFACE_TYPE \"SURFACE_TYPE\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,SURFACE_TYPE,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNI FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE_DATE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.RECREATIONAL_TRAILS,SHAPE.STLength(),-1,-1", "")
    Trails_Internal_result = arcpy.GetCount_management(RECREATIONAL_TRAILS_INTERNAL)
    print ('{} has {} records'.format(RECREATIONAL_TRAILS_INTERNAL, Trails_Internal_result[0]))
except:
    print ("\n Unable to append Recreational Trails - CRAW_INTERNAL from GIS")
    write_log("Unable to append Recreational Trails - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Recreational Trails - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Recreational Trails - CRAW_INTERNAL from GIS completed")
write_log("       Updating Recreational Trails - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Trail Emergency Access - CRAW_INTERNAL from GIS")
write_log("\n Updating Trail Emergency Access - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Trail Emergency Access - CRAW_INTERNAL
    arcpy.DeleteRows_management(TRAIL_EMERGENCY_ACCESS_INTERNAL)
except:
    print ("\n Unable to delete rows from Trail Emergency Access - CRAW_INTERNAL")
    write_log("Unable to delete rows from Trail Emergency Access - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on Unable to delete rows from Trail Emergency Access - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Trail Emergency Access - CRAW_INTERNAL from GIS
    arcpy.Append_management(TRAIL_EMERGENCY_ACCESS_GIS, TRAIL_EMERGENCY_ACCESS_INTERNAL, "NO_TEST", "TRAIL_NAME \"TRAIL NAME\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS,TRAIL_NAME,-1,-1;ACCESS_STREET \"ACCESS STREET\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS,ACCESS_STREET,-1,-1;RESTRICTIONS \"RESTRICTIONS\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS,RESTRICTIONS,-1,-1;SURFACE_TYPE \"SURFACE TYPE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS,SURFACE_TYPE,-1,-1;MUNI_NAME \"MUNI NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUN FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Recreational\\CCSDE.GIS.TRAIL_EMERGENCY_ACCESS,SHAPE.STLength(),-1,-1", "")
    Trail_Access_Internal_result = arcpy.GetCount_management(TRAIL_EMERGENCY_ACCESS_INTERNAL)
    print ('{} has {} records'.format(TRAIL_EMERGENCY_ACCESS_INTERNAL, Trail_Access_Internal_result[0]))
except:
    print ("\n Unable to append Trail Emergency Access - CRAW_INTERNAL from GIS")
    write_log("Unable to append Trail Emergency Access - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Trail Emergency Access - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("       Updating Trail Emergency Access - CRAW_INTERNAL from GIS completed")
write_log("       Updating Trail Emergency Access - CRAW_INTERNAL from GIS completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL RECREATIONAL UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL RECREATIONAL UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
