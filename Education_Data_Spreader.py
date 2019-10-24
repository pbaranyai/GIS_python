# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Education_Data_Spreader.py
# Created on: 2019-04-04 
# Updated on 2019-04-25
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#  
# School Districts
# School Locations
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
# ---------------------------------------------------------------------------

import arcpy
import sys
import datetime
import os
import traceback
import logging

# Stop geoprocessing log history in metadata
arcpy.SetLogHistory(False)

# Setup error logging
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Education_Data_Spreader.log"  
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
    sys.exit()

#Database variables:
CRAW_INTERNAL = "Database Connections\\craw_internal@ccsde.sde"
OPEN_DATA = "Database Connections\\public_od@ccsde.sde"
PUBLIC_WEB = "Database Connections\\public_web@ccsde.sde"
GIS = "Database Connections\\GIS@ccsde.sde"

# Local variables:
SCHOOL_DISTRICTS_GIS = GIS + "\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_DISTRICTS"
SCHOOL_DISTRICTS_INTERNAL = CRAW_INTERNAL + "\\CRAW_INTERNAL.Education\\CRAW_INTERNAL.SCHOOL_DISTRICTS_INTERNAL"
SCHOOL_DISTRICTS_WEB = PUBLIC_WEB + "\\PUBLIC_WEB.Education\\PUBLIC_WEB.SCHOOL_DISTRICTS_WEB"
SCHOOL_LOCATIONS_GIS = GIS + "\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS"
SCHOOL_LOCATIONS_INTERNAL = CRAW_INTERNAL + "\\CRAW_INTERNAL.Education\\CRAW_INTERNAL.SCHOOL_LOCATIONS_INTERNAL"

start_time = time.time()

print ("============================================================================")
print (("Updating Education feature classes: "+ str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\nSchool Districts")
print ("School Locations")
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Education feature classes: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nSchool Districts", logfile)  
write_log("School Locations", logfile) 
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)", logfile)
write_log("============================================================================", logfile)

print ("\n Updating School Districts - CRAW_INTERNAL from GIS")
write_log("\n Updating School Districts - CRAW_INTERNAL from GIS: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete rows from School Districts - CRAW_INTERNAL
    arcpy.DeleteRows_management(SCHOOL_DISTRICTS_INTERNAL)
except:
    print ("\n Unable to delete rows from School Districts - CRAW_INTERNAL")
    write_log("Unable to delete rows from School Districts - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from School Districts - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append School Districts - CRAW_INTERNAL from GIS
    arcpy.Append_management(SCHOOL_DISTRICTS_GIS, SCHOOL_DISTRICTS_INTERNAL, "NO_TEST", 'DISTRICT_NAME "DISTRICT NAME" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_DISTRICTS,DISTRICT_NAME,-1,-1;ADMINISTRATIVE_ADDRESS "ADMINISTRATIVE ADDRESS" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_DISTRICTS,ADMINISTRATIVE_ADDRESS,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_DISTRICTS,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_DISTRICTS,COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_DISTRICTS,UPDATE_DATE,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_DISTRICTS,SHAPE.STArea(),-1,-1;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_DISTRICTS,SHAPE.STLength(),-1,-1', "")
    SchoolDistrict_Internal_result = arcpy.GetCount_management(SCHOOL_DISTRICTS_INTERNAL)
    print (('{} has {} records'.format(SCHOOL_DISTRICTS_INTERNAL, SchoolDistrict_Internal_result[0])))
except:
    print ("\n Unable to append School Districts - CRAW_INTERNAL from GIS")
    write_log("Unable to append School Districts - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append School Districts - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating School Districts - CRAW_INTERNAL from GIS completed")
write_log("       Updating School Districts - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating School Districts - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating School Districts - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete rows from School Districts - PUBLIC_WEB
    arcpy.DeleteRows_management(SCHOOL_DISTRICTS_WEB)
except:
    print ("\n Unable to delete rows from School Districts - PUBLIC_WEB")
    write_log("Unable to delete rows from School Districts - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from School Districts - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append School Districts - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(SCHOOL_DISTRICTS_INTERNAL, SCHOOL_DISTRICTS_WEB, "NO_TEST", 'DISTRICT_NAME "DISTRICT NAME" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Education\\CCSDE.CRAW_INTERNAL.SCHOOL_DISTRICTS_INTERNAL,DISTRICT_NAME,-1,-1;ADMINISTRATIVE_ADDRESS "ADMINISTRATIVE ADDRESS" true true false 75 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Education\\CCSDE.CRAW_INTERNAL.SCHOOL_DISTRICTS_INTERNAL,ADMINISTRATIVE_ADDRESS,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Education\\CCSDE.CRAW_INTERNAL.SCHOOL_DISTRICTS_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Education\\CCSDE.CRAW_INTERNAL.SCHOOL_DISTRICTS_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Education\\CCSDE.CRAW_INTERNAL.SCHOOL_DISTRICTS_INTERNAL,UPDATE_DATE,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Education\\CCSDE.CRAW_INTERNAL.SCHOOL_DISTRICTS_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Education\\CCSDE.CRAW_INTERNAL.SCHOOL_DISTRICTS_INTERNAL,SHAPE.STLength(),-1,-1', "")
    SchoolDistrict_Web_result = arcpy.GetCount_management(SCHOOL_DISTRICTS_WEB)
    print (('{} has {} records'.format(SCHOOL_DISTRICTS_WEB, SchoolDistrict_Web_result[0])))
except:
    print ("\n Unable to append School Districts - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append School Districts - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append School Districts - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating School Districts - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating School Districts - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

print ("\n Updating School Locations - CRAW_INTERNAL from GIS")
write_log("\n Updating School Locations - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete rows from School Locations - CRAW_INTERNAL
    arcpy.DeleteRows_management(SCHOOL_LOCATIONS_INTERNAL)
except:
    print ("\n Unable to delete rows from School Locations - CRAW_INTERNAL")
    write_log("Unable to delete rows from School Locations - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from School Locations - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append School Locations - CRAW_INTERNAL from GIS
    arcpy.Append_management(SCHOOL_LOCATIONS_GIS, SCHOOL_LOCATIONS_INTERNAL, "NO_TEST", 'NAME "NAME" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,NAME,-1,-1;HSENUMBER "ADDRESS #" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,HSENUMBER,-1,-1;FULL_STREET "FULL STREET" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,FULL_STREET,-1,-1;POST_OFFICE "POST OFFICE" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,POST_OFFICE,-1,-1;STATE "STATE" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,STATE,-1,-1;ZIPCODE "ZIPCODE" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,ZIPCODE,-1,-1;SCHOOL_TYPE "SCHOOL TYPE" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,SCHOOL_TYPE,-1,-1;MUNI_NAME "MUNICIPALITY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,MUNI_NAME,-1,-1;MUNI_FIPS "MUNICIPALITY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,MUNI_FIPS,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Education\\CCSDE.GIS.SCHOOL_LOCATIONS,UPDATE_DATE,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#', "")
    SchoolLocations_Internal_result = arcpy.GetCount_management(SCHOOL_LOCATIONS_INTERNAL)
    print (('{} has {} records'.format(SCHOOL_LOCATIONS_INTERNAL, SchoolLocations_Internal_result[0])))
except:
    print ("\n Unable to append School Locations - CRAW_INTERNAL from GIS")
    write_log("Unable to append School Locations - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append School Locations - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating School Locations - CRAW_INTERNAL from GIS completed")
write_log("       Updating School Locations - CRAW_INTERNAL from GIS completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n ALL EDUCATION FEATURE CLASS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("\n ALL EDUCATION FEATURE CLASS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print (("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)))
write_log("Elapsed time: " + str (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
