# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Utilities_Data_Spreader.py
# Created on: 2019-03-05 
# Updated on 2019-04-25
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# HYDRANTS  
# NATIONAL_FUEL_LINES
# NATIONAL_FUEL_STATIONS
# NWREC_SUBSTATIONS
# TOWER_SITES 
# UTILITY_POLES
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
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
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Utilities_Data_Spreader.log"  
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
OPEN_DATA = "Database Connections\\public_od@ccsde.sde"
PUBLIC_SAFETY = "Database Connections\\PUBLIC_SAFETY@ccsde.sde"
PUBLIC_WEB = "Database Connections\\public_web@ccsde.sde"

# Local variables:
HYDRANTS_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS"
HYDRANTS_INTERNAL = CRAW_INTERNAL + "\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS_INTERNAL"
HYDRANTS_WEB = PUBLIC_WEB + "\\PUBLIC_WEB.Utilities\\PUBLIC_WEB.HYDRANTS_WEB"
NATIONAL_FUEL_LINES_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.National_Fuel_Lines"
NATIONAL_FUEL_LINES_INTERNAL = CRAW_INTERNAL + "\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.National_Fuel_Lines_INTERNAL"
NATIONAL_FUEL_STATIONS_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.National_Fuel_Stations"
NATIONAL_FUEL_STATIONS_INTERNAL = CRAW_INTERNAL + "\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.National_Fuel_Station_INTENRAL"
NWREC_SUBSTATIONS_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.NWREC_SUBSTATIONS"
NWREC_SUBSTATIONS_INTERNAL = CRAW_INTERNAL + "\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.NWREC_SUBSTATIONS_INTERNAL"
TOWER_SITES_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES"
TOWER_SITES_INTERNAL = CRAW_INTERNAL + "\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL"
TOWER_SITES_WEB = PUBLIC_WEB + "\\PUBLIC_WEB.Utilities\\PUBLIC_WEB.TOWER_SITES_WEB"
UTILITY_POLES_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.Utility_Poles"
UTILITY_POLES_INTERNAL = CRAW_INTERNAL + "\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.UTILITY_POLES_INTERNAL"

start_time = time.time()

print ("============================================================================")
print ("Updating Utilities datasets: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nHydrants Feature Class")
print ("National Fuel Lines Feature Class")
print ("National Fuel Stations Feature Class")
print ("NW Rec Substations Feature Class")
print ("Tower Sites Feature Class")
print ("Utilities Feature Class")
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Utilities datasets: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nHydrants Feature Class", logfile)  
write_log("National Fuel Lines Feature Class", logfile) 
write_log("National Fuel Stations Feature Class", logfile)
write_log("NW Rec Substations Feature Class", logfile)
write_log("Tower Sites Feature Class", logfile) 
write_log("Utilities Feature Class", logfile)
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Hydrants - CRAW_INTERNAL from PUBLIC_SAFETYY")
write_log("\n Updating Hydrants - CRAW_INTERNAL from PUBLIC_SAFETY: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Hydrants - CRAW_INTERNAL
    arcpy.DeleteRows_management(HYDRANTS_INTERNAL)
except:
    print ("\n Unable to delete rows from Hydrants - CRAW_INTERNAL")
    write_log("Unable to delete rows from Hydrants - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Hydrants - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append Hydrants - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(HYDRANTS_PS, HYDRANTS_INTERNAL, "NO_TEST", 'HYDRANT_ID "HYDRANT ID" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,HYDRANT_ID,-1,-1;BODY_COLOR "BODY COLOR" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,BODY_COLOR,-1,-1;TOP_COLOR "TOP COLOR" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,TOP_COLOR,-1,-1;TYPE "TYPE" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,TYPE,-1,-1;MUNI_NAME "MUNICIPALITY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,MUNI_NAME,-1,-1;MUNI_FIPS "MUNICIPALITY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,MUNI_FIPS,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,UPDATE_DATE,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#;HYDRANT_NUMBER "Hydrant Number" true true false 20 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,HYDRANT_NUMBER,-1,-1;LOCATION_DESCRIPTION "Description of hydrant location" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,LOCATION_DESCRIPTION,-1,-1;SERIAL_NUMBER "Serial Number" true true false 20 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,SERIAL_NUMBER,-1,-1;IN_SERVICE "IN_SERVICE" true true false 3 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.HYDRANTS,IN_SERVICE,-1,-1', "")
    Hydrants_Internal_result = arcpy.GetCount_management(HYDRANTS_INTERNAL)
    print ('{} has {} records'.format(HYDRANTS_INTERNAL, Hydrants_Internal_result[0]))
except:
    print ("\n Unable to append Hydrants - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append Hydrants - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append Hydrants - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Hydrants - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating Hydrants - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating Hydrants - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Hydrants - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Hydrants - PUBLIC_WEB
    arcpy.DeleteRows_management(HYDRANTS_WEB)
except:
    print ("\n Unable to delete rows from Hydrants - PUBLIC_WEB")
    write_log("Unable to delete rows from Hydrants - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Hydrants - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append Hydrants - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(HYDRANTS_INTERNAL, HYDRANTS_WEB, "NO_TEST", "HYDRANT_ID \"HYDRANT ID\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS_INTERNAL,HYDRANT_ID,-1,-1;BODY_COLOR \"BODY COLOR\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS_INTERNAL,BODY_COLOR,-1,-1;TOP_COLOR \"TOP COLOR\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS_INTERNAL,TOP_COLOR,-1,-1;TYPE \"TYPE\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS_INTERNAL,TYPE,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS_INTERNAL,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS_INTERNAL,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS_INTERNAL,UPDATE_DATE,-1,-1", "")
    Hydrants_Web_result = arcpy.GetCount_management(HYDRANTS_WEB)
    print ('{} has {} records'.format(HYDRANTS_WEB, Hydrants_Web_result[0]))
except:
    print ("\n Unable to append Hydrants - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Hydrants - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Hydrants - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Hydrants - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Hydrants - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

print ("\n Updating National Fuel Lines - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating National Fuel Lines - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete Rows from National Fuel Lines - CRAW_INTERNAL
    arcpy.DeleteRows_management(NATIONAL_FUEL_LINES_INTERNAL)
except:
    print ("\n Unable to delete rows from National Fuel Lines - CRAW_INTERNAL")
    write_log("Unable to delete rows from National Fuel Lines - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from National Fuel Lines - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append National Fuel Lines - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(NATIONAL_FUEL_LINES_PS, NATIONAL_FUEL_LINES_INTERNAL, "NO_TEST", "LINE_TYPE \"LINE_TYPE\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.National_Fuel_Lines,LINE_TYPE,-1,-1;DATE_RECORDED \"DATE_RECORDED\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.National_Fuel_Lines,DATE_RECORDED,-1,-1;SHAPE.LEN \"SHAPE.LEN\" false false true 0 Double 0 0 ,First,#", "")
    NFLines_Internal_result = arcpy.GetCount_management(NATIONAL_FUEL_LINES_INTERNAL)
    print ('{} has {} records'.format(NATIONAL_FUEL_LINES_INTERNAL, NFLines_Internal_result[0]))
except:
    print ("\n Unable to append National Fuel Lines - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append National Fuel Lines - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append National Fuel Lines - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating National Fuel Lines - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating National Fuel Lines - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating National Fuel Stations - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating National Fuel Stations - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Process: Delete Rows from National Fuel Stations - CRAW_INTERNAL
    arcpy.DeleteRows_management(NATIONAL_FUEL_STATIONS_INTERNAL)
except:
    print ("\n Unable to delete rows from National Fuel Stations - CRAW_INTERNAL")
    write_log("Unable to delete rows from National Fuel Stations - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from National Fuel Stations - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append National Fuel Stations - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(NATIONAL_FUEL_STATIONS_PS, NATIONAL_FUEL_STATIONS_INTERNAL, "NO_TEST", "STATION_TYPE \"STATION_TYPE\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.National_Fuel_Stations,STATION_TYPE,-1,-1;NAME \"NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.National_Fuel_Stations,NAME,-1,-1;IDENTIFIER \"IDENTIFIER\" true true false 255 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.National_Fuel_Stations,IDENTIFIER,-1,-1", "")
    NFStations_Internal_result = arcpy.GetCount_management(NATIONAL_FUEL_STATIONS_INTERNAL)
    print ('{} has {} records'.format(NATIONAL_FUEL_STATIONS_INTERNAL, NFStations_Internal_result[0]))
except:
    print ("\n Unable to append National Fuel Stations - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append National Fuel Stations - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append National Fuel Stations - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating National Fuel Stations - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating National Fuel Stations - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating NWREC Substations - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating NWREC Substations - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete Rows from NWREC Substations - CRAW_INTERNAL
    arcpy.DeleteRows_management(NWREC_SUBSTATIONS_INTERNAL)
except:
    print ("\n Unable to delete rows from NWREC Substations - CRAW_INTERNAL")
    write_log("Unable to delete rows from NWREC Substations - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from NWREC Substations - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append NWREC Substations - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(NWREC_SUBSTATIONS_PS, NWREC_SUBSTATIONS_INTERNAL, "NO_TEST", "GS_NAME \"GS_NAME\" true true false 20 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.NWREC_SUBSTATIONS,GS_NAME,-1,-1", "")
    NWRECSubStations_Internal_result = arcpy.GetCount_management(NWREC_SUBSTATIONS_INTERNAL)
    print ('{} has {} records'.format(NWREC_SUBSTATIONS_INTERNAL, NWRECSubStations_Internal_result[0]))
except:
    print ("\n Unable to append NWREC Substations - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append NWREC Substations - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append NWREC Substations - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating NWREC Substations - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating NWREC Substations - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating Tower Sites - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating Tower Sites - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete Rows from Tower Sites - CRAW_INTERNAL
    arcpy.DeleteRows_management(TOWER_SITES_INTERNAL)
except:
    print ("\n Unable to delete rows from Tower Sites - CRAW_INTERNAL")
    write_log("Unable to delete rows from Tower Sites - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Tower Sites - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Tower Sites - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(TOWER_SITES_PS, TOWER_SITES_INTERNAL, "NO_TEST", "CARRIER_NAME \"CARRIER NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,CARRIER_NAME,-1,-1;HSENUMBER \"ADDRESS #\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,HSENUMBER,-1,-1;PREDIR \"PRE-DIRECTIONAL\" true true false 4 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,PREDIR,-1,-1;STREET \"STREET\" true true false 75 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,STREET,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,MUNI_FIPS,-1,-1;SITE_NAME \"SITE NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,SITE_NAME,-1,-1;PUBLIC_SAFETY_TOWER \"PUBLIC SAFETY TOWER\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,PUBLIC_SAFETY_TOWER,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.TOWER_SITES,UPDATE_DATE,-1,-1", "")
    Towers_Internal_result = arcpy.GetCount_management(TOWER_SITES_INTERNAL)
    print ('{} has {} records'.format(TOWER_SITES_INTERNAL, Towers_Internal_result[0]))
except:
    print ("\n Unable to append Tower Sites - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append Tower Sites - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append Tower Sites - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Tower Sites - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating Tower Sites - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating Tower Sites- PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Tower Sites- PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Tower Sites - PUBLIC_WEB
    arcpy.DeleteRows_management(TOWER_SITES_WEB)
except:
    print ("\n Unable to delete rows from Tower Sites - PUBLIC_WEB")
    write_log("Unable to delete rows from Tower Sites - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Tower Sites - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Tower Sites - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(TOWER_SITES_INTERNAL, TOWER_SITES_WEB, "NO_TEST", "CARRIER_NAME \"CARRIER NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,CARRIER_NAME,-1,-1;HSENUMBER \"ADDRESS #\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,HSENUMBER,-1,-1;PREDIR \"PRE-DIRECTIONAL\" true true false 4 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,PREDIR,-1,-1;STREET \"STREET\" true true false 75 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,STREET,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,MUNI_FIPS,-1,-1;SITE_NAME \"SITE NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,SITE_NAME,-1,-1;PUBLIC_SAFETY_TOWER \"PUBLIC SAFETY TOWER\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,PUBLIC_SAFETY_TOWER,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.TOWER_SITES_INTERNAL,UPDATE_DATE,-1,-1", "")
    Towers_Web_result = arcpy.GetCount_management(TOWER_SITES_WEB)
    print ('{} has {} records'.format(TOWER_SITES_WEB, Towers_Web_result[0]))
except:
    print ("\n Unable to append Tower Sites - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Tower Sites - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Tower Sites - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Tower Sites - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Tower Sites - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

print ("\n Updating Utility Poles - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating Utility Poles - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete Rows from Utility Poles - CRAW_INTERNAL
    arcpy.DeleteRows_management(UTILITY_POLES_INTERNAL)
except:
    print ("\n Unable to delete rows from Utility Poles - CRAW_INTERNAL")
    write_log("Unable to delete rows from Utility Poles - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Utility Poles - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Utility Poles - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(UTILITY_POLES_PS, UTILITY_POLES_INTERNAL, "NO_TEST", "TYPE \"TYPE\" true true false 254 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.Utility_Poles,TYPE,-1,-1;OWNER \"OWNER\" true true false 254 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.Utility_Poles,OWNER,-1,-1;POLE_ID \"POLE_ID\" true true false 254 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.Utility_Poles,POLE_ID,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 255 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.Utility_Poles,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.Utility_Poles,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 255 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.Utility_Poles,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.Utility_Poles,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Utilities\\CCSDE.PUBLIC_SAFETY.Utility_Poles,UPDATE_DATE,-1,-1", "")
    Poles_Internal_result = arcpy.GetCount_management(UTILITY_POLES_INTERNAL)
    print ('{} has {} records'.format(UTILITY_POLES_INTERNAL, Poles_Internal_result[0]))
except:
    print ("\n Unable to append Utility Poles - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append Utility Poles - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append Utility Poles - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Utility Poles - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating Utility Poles - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL UTILITY DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL UTILITY DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
