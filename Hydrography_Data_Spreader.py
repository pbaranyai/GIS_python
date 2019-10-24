# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Hydrography_Data_Spreader.py
# Created on: 2019-03-05 
# Updated on 2019-04-22
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# Dams
# Lakes 
# Rivers/Streams
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
# ---------------------------------------------------------------------------

import sys
import arcpy
import datetime
import os
import traceback
import logging
#import __builtin__
import builtins

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Hydrography_Data_Spreader.log"  
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

#Database variables:
CRAW_INTERNAL = "Database Connections\\craw_internal@ccsde.sde"
GIS = "Database Connections\\GIS@ccsde.sde"
OPEN_DATA = "Database Connections\\public_od@ccsde.sde"
PUBLIC_SAFETY = "Database Connections\\PUBLIC_SAFETY@ccsde.sde"
PUBLIC_WEB = "Database Connections\\public_web@ccsde.sde"

# Local variables:
DAM_GIS = GIS + "\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM"
DAM_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.DAMS_INTERNAL"
LAKES_GIS = GIS + "\\CCSDE.GIS.Hydrography\\CCSDE.GIS.LAKES"
LAKES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.LAKES_INTERNAL"
LAKES_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Hydrography\\CCSDE.PUBLIC_WEB.LAKES_web"
RIVERS_STREAMS_GIS = GIS + "\\CCSDE.GIS.Hydrography\\CCSDE.GIS.RIVERS_STREAMS"
RIVERS_STREAMS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.RIVERS_STREAMS_INTERNAL"
RIVERS_STREAMS_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Hydrography\\CCSDE.PUBLIC_WEB.RIVERS_STREAMS_WEB"

start_time = time.time()

print ("============================================================================")
print (("Updating Hydrography: "+ str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\nDam Feature Class")
print ("Lakes Feature Class" )
print ("Rivers/Streams Feature Class")
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Hydrography: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nDam Feature Class", logfile)  
write_log("Lakes Feature Class", logfile) 
write_log("Rivers/Streams Feature Class", logfile)
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Dams - CRAW_INTERNAL from GIS")
write_log("\n Updating Dams - CRAW_INTERNAL from GIS: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Dams - CRAW_INTERNAL
    arcpy.DeleteRows_management(DAM_INTERNAL)
except:
    print ("\n Unable to delete rows from Dams - CRAW_INTERNAL")
    write_log("Unable to delete rows from Dams - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Dams - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Dams - CRAW_INTERNAL from GIS
    arcpy.Append_management(DAM_GIS, DAM_INTERNAL, "NO_TEST", "NAME \"NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,NAME,-1,-1;WATER_BODY \"WATER BODY\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,WATER_BODY,-1,-1;OWNERSHIP \"OWNERSHIP\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,OWNERSHIP,-1,-1;HEIGHT \"HEIGHT\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,HEIGHT,-1,-1;POOL_CAPACITY \"POOL  CAPACITY\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,POOL_CAPACITY,-1,-1;EMA_TYPE \"EMA TYPE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,EMA_TYPE,-1,-1;COUNTY_NAME \"COUNTY_NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.DAM,SHAPE.STLength(),-1,-1", "")
    Dams_Internal_result = arcpy.GetCount_management(DAM_INTERNAL)
    print (('{} has {} records'.format(DAM_INTERNAL, Dams_Internal_result[0])))
except:
    print ("\n Unable to append Append Dams - CRAW_INTERNAL from GIS")
    write_log("Unable to append Append Dams - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Append Dams - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Append Dams - CRAW_INTERNAL from GIS completed")
write_log("       Updating Append Dams - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Lakes - CRAW_INTERNAL from GIS")
write_log("\n Updating Lakes - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Lakes - CRAW_INTERNAL
    arcpy.DeleteRows_management(LAKES_INTERNAL)
except:
    print ("\n Unable to delete rows from Lakes - CRAW_INTERNAL")
    write_log("Unable to delete rows from Lakes - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Lakes - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Lakes - CRAW_INERNAL from GIS
    arcpy.Append_management(LAKES_GIS, LAKES_INTERNAL, "NO_TEST", 'NAME "NAME" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.LAKES,NAME,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.LAKES,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.LAKES,COUNTY_FIPS,-1,-1;RECTIFIED "ORTHO-RECTIFIED" true true false 4 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.LAKES,RECTIFIED,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.LAKES,SHAPE.STArea(),-1,-1;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.LAKES,SHAPE.STLength(),-1,-1', "")
    Lakes_Internal_result = arcpy.GetCount_management(LAKES_INTERNAL)
    print (('{} has {} records'.format(LAKES_INTERNAL, Lakes_Internal_result[0])))
except:
    print ("\n Unable to append Append Lakes - CRAW_INERNAL from GIS")
    write_log("Unable to append Append Lakes - CRAW_INERNAL from GIS", logfile)
    logging.exception('Got exception on append Append Lakes - CRAW_INERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Append Lakes - CRAW_INTERNAL from GIS completed")
write_log("       Updating Append Lakes - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Lakes - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Lakes - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Lakes - PUBLIC_WEB
    arcpy.DeleteRows_management(LAKES_WEB)
except:
    print ("\n Unable to delete rows from Lakes - PUBLIC_WEB")
    write_log("Unable to delete rows from Lakes - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Lakes - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Lakes - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(LAKES_INTERNAL, LAKES_WEB, "NO_TEST", "NAME \"NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.LAKES_INTERNAL,NAME,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.LAKES_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.LAKES_INTERNAL,COUNTY_FIPS,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.LAKES_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.LAKES_INTERNAL,SHAPE.STLength(),-1,-1", "")
    Lakes_Web_result = arcpy.GetCount_management(LAKES_WEB)
    print (('{} has {} records'.format(LAKES_WEB, Lakes_Web_result[0])))
except:
    print ("\n Unable to append Append Lakes - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Append Lakes - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Append Lakes - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Append Lakes - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Append Lakes - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

print ("\n Updating Rivers/Streams - CRAW_INTERNAL from GIS")
write_log("\n Updating Rivers/Streams - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Rivers/Streams - CRAW_INTERNAL 
    arcpy.DeleteRows_management(RIVERS_STREAMS_INTERNAL)
except:
    print ("\n Unable to delete rows from Rivers/Streams - CRAW_INTERNAL")
    write_log("Unable to delete rows from Rivers/Streams - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Rivers/Streams - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Rivers/Streams - CRAW_INTERNAL from GIS
    arcpy.Append_management(RIVERS_STREAMS_GIS, RIVERS_STREAMS_INTERNAL, "NO_TEST", "NAME \"NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.RIVERS_STREAMS,NAME,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.RIVERS_STREAMS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.RIVERS_STREAMS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.RIVERS_STREAMS,UPDATE_DATE,-1,-1;RECTIFIED \"ORTHO-RECTIFIED\" true true false 4 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.RIVERS_STREAMS,RECTIFIED,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.RIVERS_STREAMS,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.RIVERS_STREAMS,SHAPE.STLength(),-1,-1", "")
    RIVERS_STREAMS_Internal_result = arcpy.GetCount_management(RIVERS_STREAMS_INTERNAL)
    print (('{} has {} records'.format(RIVERS_STREAMS_INTERNAL, RIVERS_STREAMS_Internal_result[0])))
except:
    print ("\n Unable to append Append Rivers/Streams - CRAW_INTERNAL from GIS")
    write_log("Unable to append Append Rivers/Streams - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Append Rivers/Streams - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Append Rivers/Streams - CRAW_INTERNAL from GIS completed")
write_log("       Updating Append Rivers/Streams - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Rivers/Streams - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Rivers/Streams - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Rivers/Streams - PUBLIC_WEB
    arcpy.DeleteRows_management(RIVERS_STREAMS_WEB)
except:
    print ("\n Unable to delete rows from Rivers/Streams - PUBLIC_WEB")
    write_log("Unable to delete rows from Rivers/Streams - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Rivers/Streams - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Rivers/Streams - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(RIVERS_STREAMS_INTERNAL, RIVERS_STREAMS_WEB, "NO_TEST", "NAME \"NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.RIVERS_STREAMS_INTERNAL,NAME,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.RIVERS_STREAMS_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.RIVERS_STREAMS_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.RIVERS_STREAMS_INTERNAL,UPDATE_DATE,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.RIVERS_STREAMS_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.RIVERS_STREAMS_INTERNAL,SHAPE.STLength(),-1,-1", "")
    RIVERS_STREAMS_Web_result = arcpy.GetCount_management(RIVERS_STREAMS_WEB)
    print (('{} has {} records'.format(RIVERS_STREAMS_WEB, RIVERS_STREAMS_Web_result[0])))
except:
    print ("\n Unable to append Append Rivers/Streams - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Append Rivers/Streams - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Append Rivers/Streams - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Append Rivers/Streams - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Append Rivers/Streams - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n ALL HYDROGRAPHY UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("\n ALL HYDROGRAPHY UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print (("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
