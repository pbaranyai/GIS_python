# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Transportation_Data_Spreader.py
# Created on: 2019-03-05 
# Updated on 2019-04-25
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# AIRPORT LOCATIONS  
# BRIDGES 
# CATA_BUS_STOPS
# MILE_MARKERS
# RAILROADS
# RAILROAD CROSSINGS
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
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Transportation_Data_Spreader.log"  
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
AIRPORT_LOCATIONS_GIS = GIS + "\\CCSDE.GIS.Transportation\\CCSDE.GIS.AIRPORT_LOCATIONS"
AIRPORT_LOCATIONS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.AIRPORTS_INTERNAL"
AIRPORT_LOCATIONS_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Transportation\\CCSDE.PUBLIC_WEB.AIRPORT_LOCATIONS_WEB"
BRIDGES_GIS = GIS + "\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES"
BRIDGES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.BRIDGES_INTERNAL"
CATA_BUS_STOPS_GIS = GIS + "\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS"
CATA_BUS_STOPS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.CATA_BUS_STOPS_INTERNAL"
MILE_MARKERS_GIS = GIS + "\\CCSDE.GIS.Transportation\\CCSDE.GIS.MILE_MARKERS_LOCATIONS"
MILE_MARKERS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL"
MILE_MARKERS_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Transportation\\CCSDE.PUBLIC_WEB.MILE_MARKERS_LOCATIONS_WEB"
RAILROADS_GIS = GIS + "\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROADS"
RAILROADS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL"
RAILROADS_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Transportation\\CCSDE.PUBLIC_WEB.RAILROADS_WEB"
RAILROAD_CROSSINGS_GIS = GIS + "\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS"
RAILROAD_CROSSINGS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROAD_CROSSINGS_INTERNAL"

start_time = time.time()

print ("============================================================================")
print ("Updating Transportation Datasets: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nAirport Locations Feature Class")
print ("Bridges Feature Class")
print ("CATA Bus Stops Feature Class")
print ("Mile Markers Feature Class")
print ("Railroads Feature Class")
print ("Railroad Crossings Feature Class")
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Transportation Datasets: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nAirport Locations Feature Class", logfile)  
write_log("Bridges Feature Class", logfile) 
write_log("CATA Bus Stops Feature Class Feature Class", logfile)
write_log("Mile Markers Feature Class", logfile)
write_log("Railroads Feature Class", logfile) 
write_log("Railroad Crossings Feature Class", logfile)
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Airports - CRAW_INTERNAL from GIS")
write_log("\n Updating Airports - CRAW_INTERNAL from GIS: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Airports - CRAW_INTERNAL
    arcpy.DeleteRows_management(AIRPORT_LOCATIONS_INTERNAL)
except:
    print ("\n Unable to delete rows from Airports - CRAW_INTERNAL")
    write_log("Unable to delete rows from Airports - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Airports - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append Airports - CRAW_INTERNAL from GIS
    arcpy.Append_management(AIRPORT_LOCATIONS_GIS, AIRPORT_LOCATIONS_INTERNAL, "NO_TEST", "AIRPORT_NAME \"AIRPORT NAME\" true true false 150 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.AIRPORT_LOCATIONS,AIRPORT_NAME,-1,-1;RUNWAY_LENGTH \"RUNWAY_LENGTH\" true true false 2 Short 0 5 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.AIRPORT_LOCATIONS,RUNWAY_LENGTH,-1,-1;RUNWAY_SURF_TYPE \"RUNWAY SURFACE TYPE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.AIRPORT_LOCATIONS,RUNWAY_SURF_TYPE,-1,-1;AIRPORT_TYPE \"AIRPORT TYPE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.AIRPORT_LOCATIONS,AIRPORT_TYPE,-1,-1;TOWER \"TOWER\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.AIRPORT_LOCATIONS,TOWER,-1,-1;AIRPORT_OWNER \"AIRPORT_OWNER\" true true false 150 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.AIRPORT_LOCATIONS,AIRPORT_OWNER,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    Airports_Internal_result = arcpy.GetCount_management(AIRPORT_LOCATIONS_INTERNAL)
    print ('{} has {} records'.format(AIRPORT_LOCATIONS_INTERNAL, Airports_Internal_result[0]))
except:
    print ("\n Unable to append Airports - CRAW_INTERNAL from GIS")
    write_log("Unable to append Airports - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Airports - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Airports - CRAW_INTERNAL from GIS completed")
write_log("       Updating Airports - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Airports - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Airports - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Airports - PUBLIC_WEB
    arcpy.DeleteRows_management(AIRPORT_LOCATIONS_WEB)
except:
    print ("\n Unable to delete rows from Airports - PUBLIC_WEB")
    write_log("Unable to delete rows from Airports - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Airports - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append Airports - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(AIRPORT_LOCATIONS_INTERNAL, AIRPORT_LOCATIONS_WEB, "NO_TEST", "AIRPORT_NAME \"AIRPORT NAME\" true true false 150 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.AIRPORTS_INTERNAL,AIRPORT_NAME,-1,-1;RUNWAY_LENGTH \"RUNWAY_LENGTH\" true true false 2 Short 0 5 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.AIRPORTS_INTERNAL,RUNWAY_LENGTH,-1,-1;RUNWAY_SURF_TYPE \"RUNWAY SURFACE TYPE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.AIRPORTS_INTERNAL,RUNWAY_SURF_TYPE,-1,-1;AIRPORT_TYPE \"AIRPORT TYPE\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.AIRPORTS_INTERNAL,AIRPORT_TYPE,-1,-1;TOWER \"TOWER\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.AIRPORTS_INTERNAL,TOWER,-1,-1", "")
    Airports_Web_result = arcpy.GetCount_management(AIRPORT_LOCATIONS_WEB)
    print ('{} has {} records'.format(AIRPORT_LOCATIONS_WEB, Airports_Web_result[0]))
except:
    print ("\n Unable to append Airports - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Airports - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Airports - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Airports - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Airports - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

print ("\n Updating Bridges - CRAW_INTERNAL from GIS")
write_log("\n Updating Bridges - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Bridges - CRAW_INTERNAL
    arcpy.DeleteRows_management(BRIDGES_INTERNAL)
except:
    print ("\n Unable to delete rows from Bridges - CRAW_INTERNAL")
    write_log("Unable to delete rows from Bridges - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Bridges - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append Bridges - CRAW_INTERNAL from GIS
    arcpy.Append_management(BRIDGES_GIS, BRIDGES_INTERNAL, "NO_TEST", "COUNTY_CODE \"COUNTY_CODE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,COUNTY_CODE,-1,-1;TOWNSHIP_CODE \"TOWNSHIP CODE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,TOWNSHIP_CODE,-1,-1;ROAD_CODE \"ROAD CODE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,ROAD_CODE,-1,-1;BRIDGE_CODE \"BRIDGE_CODE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,BRIDGE_CODE,-1,-1;BMS_ID \"BMS_ID\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,BMS_ID,-1,-1;MUNICIPALITY \"MUNICIPALITY\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,MUNICIPALITY,-1,-1;NBIS_WORK_TYPE \"NBIS_WORK_TYPE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,NBIS_WORK_TYPE,-1,-1;ROAD_NAME \"ROAD_NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,ROAD_NAME,-1,-1;OWNER \"OWNER\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,OWNER,-1,-1;WATER_FEATURE \"WATER_FEATURE\" true true false 255 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,WATER_FEATURE,-1,-1;STATUS \"STATUS\" true true false 255 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,STATUS,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 255 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 255 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.BRIDGES,SHAPE.STLength(),-1,-1", "")
    Bridges_Internal_result = arcpy.GetCount_management(BRIDGES_INTERNAL)
    print ('{} has {} records'.format(BRIDGES_INTERNAL, Bridges_Internal_result[0]))
except:
    print ("\n Unable to append Bridges - CRAW_INTERNAL from GIS")
    write_log("Unable to append Bridges - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Bridges - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Bridges - CRAW_INTERNAL from GIS completed")
write_log("       Updating Bridges - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating CATA Bus Stops - CRAW_INTERNAL from GIS")
write_log("\n Updating CATA Bus Stops - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from CATA Bus Stops - CRAW_INTERNAL
    arcpy.DeleteRows_management(CATA_BUS_STOPS_INTERNAL)
except:
    print ("\n Unable to delete rows from CATA Bus Stops - CRAW_INTERNAL")
    write_log("Unable to delete rows from CATA Bus Stops - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from CATA Bus Stops - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append CATA Bus Stops - CRAW_INTERNAL from GIS
    arcpy.Append_management(CATA_BUS_STOPS_GIS, CATA_BUS_STOPS_INTERNAL, "NO_TEST", "STOPID \"STOPID\" true true false 4 Long 0 10 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,STOPID,-1,-1;STOPNAME \"STOPNAME\" true true false 254 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,STOPNAME,-1,-1;ROUTES \"ROUTES\" true true false 254 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,ROUTES,-1,-1;ON_STREET \"ON_STREET\" true true false 254 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,ON_STREET,-1,-1;AT_STREET \"AT_STREET\" true true false 254 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,AT_STREET,-1,-1;LOCATION \"LOCATION\" true true false 254 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,LOCATION,-1,-1;BENCH \"BENCH\" true true false 4 Long 0 10 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,BENCH,-1,-1;SHELTER \"SHELTER\" true true false 4 Long 0 10 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,SHELTER,-1,-1;GARBAGE \"GARBAGE\" true true false 4 Long 0 10 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,GARBAGE,-1,-1;BIKE_RACK \"BIKE_RACK\" true true false 4 Long 0 10 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,BIKE_RACK,-1,-1;LIGHTING \"LIGHTING\" true true false 4 Long 0 10 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,LIGHTING,-1,-1;ADA_SIDEWA \"ADA_SIDEWA\" true true false 4 Long 0 10 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,ADA_SIDEWA,-1,-1;AGENCY \"AGENCY\" true true false 254 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,AGENCY,-1,-1;COUNTY \"COUNTY\" true true false 254 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,COUNTY,-1,-1;CITY \"CITY\" true true false 254 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,CITY,-1,-1;LAT \"LAT\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,LAT,-1,-1;LON \"LON\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.CATA_BUS_STOPS,LON,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    BusStops_Internal_result = arcpy.GetCount_management(CATA_BUS_STOPS_INTERNAL)
    print ('{} has {} records'.format(CATA_BUS_STOPS_INTERNAL, BusStops_Internal_result[0]))
except:
    print ("\n Unable to append CATA Bus Stops - CRAW_INTERNAL from GIS")
    write_log("Unable to append CATA Bus Stops - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append CATA Bus Stops - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating CATA Bus Stops - CRAW_INTERNAL from GIS completed")
write_log("       Updating CATA Bus Stops - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Mile Markers - CRAW_INTERNAL from GIS")
write_log("\n Updating Mile Markers - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Mile Markers - CRAW_INTERNAL
    arcpy.DeleteRows_management(MILE_MARKERS_INTERNAL)
except:
    print ("\n Unable to delete rows from Mile Markers - CRAW_INTERNAL")
    write_log("Unable to delete rows from Mile Markers - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Mile Markers - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append Mile Markers - CRAW_INTERNAL from GIS
    arcpy.Append_management(MILE_MARKERS_GIS, MILE_MARKERS_INTERNAL, "NO_TEST", "MILE_POST \"MILE POST\" true true false 25 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.MILE_MARKERS_LOCATIONS,MILE_POST,-1,-1;STREET_NAME \"STREET NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.MILE_MARKERS_LOCATIONS,STREET_NAME,-1,-1;MARKER_NAME \"MARKER NAME\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.MILE_MARKERS_LOCATIONS,MARKER_NAME,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.MILE_MARKERS_LOCATIONS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNI FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.MILE_MARKERS_LOCATIONS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.MILE_MARKERS_LOCATIONS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.MILE_MARKERS_LOCATIONS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.MILE_MARKERS_LOCATIONS,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    MileMarkers_Internal_result = arcpy.GetCount_management(MILE_MARKERS_INTERNAL)
    print ('{} has {} records'.format(MILE_MARKERS_INTERNAL, MileMarkers_Internal_result[0]))
except:
    print ("\n Unable to append Mile Markers - CRAW_INTERNAL from GIS")
    write_log("Unable to append Mile Markers - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Mile Markers - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Mile Markers - CRAW_INTERNAL from GIS completed")
write_log("       Updating Mile Markers - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Mile Markers - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Mile Markers - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Mile Markers - PUBLIC_WEB
    arcpy.DeleteRows_management(MILE_MARKERS_WEB)
except:
    print ("\n Unable to delete rows from Mile Markers - PUBLIC_WEB")
    write_log("Unable to delete rows from Mile Markers - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Mile Markers - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append Mile Markers - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(MILE_MARKERS_INTERNAL, MILE_MARKERS_WEB, "NO_TEST", "MILE_POST \"MILE POST\" true true false 25 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL,MILE_POST,-1,-1;STREET_NAME \"STREET NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL,STREET_NAME,-1,-1;MARKER_NAME \"MARKER NAME\" true true false 75 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL,MARKER_NAME,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNI FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL,UPDATE_DATE,-1,-1", "")
    MileMarkers_Web_result = arcpy.GetCount_management(MILE_MARKERS_WEB)
    print ('{} has {} records'.format(MILE_MARKERS_WEB, MileMarkers_Web_result[0]))
except:
    print ("\n Unable to append Mile Markers - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Mile Markers - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Mile Markers - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Mile Markers - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Mile Markers - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

print ("\n Updating Railroad Crossings - CRAW_INTERNAL from GIS")
write_log("\n Updating Railroad Crossings - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Railroad Crossings - CRAW_INTERNAL
    arcpy.DeleteRows_management(RAILROAD_CROSSINGS_INTERNAL)
except:
    print ("\n Unable to delete rows from Railroad Crossings - CRAW_INTERNAL")
    write_log("Unable to delete rows from Railroad Crossings - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Railroad Crossings - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append Railroad Crossings - CRAW_INTERNAL from GIS
    arcpy.Append_management(RAILROAD_CROSSINGS_GIS, RAILROAD_CROSSINGS_INTERNAL, "NO_TEST", "RAIL_NAME \"RAIL NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS,RAIL_NAME,-1,-1;DOT_INVENTORY_NUM \"DOT INVENTORY NUM\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS,DOT_INVENTORY_NUM,-1,-1;SIGNAL \"SIGNAL\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS,SIGNAL,-1,-1;GATE_ARMS \"GATE ARMS\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS,GATE_ARMS,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS,UPDATE_DATE,-1,-1;MILE_MARKER \"MILE MARKER\" true true false 255 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROAD_CROSSINGS,MILE_MARKER,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    RRCrossings_Internal_result = arcpy.GetCount_management(RAILROAD_CROSSINGS_INTERNAL)
    print ('{} has {} records'.format(RAILROAD_CROSSINGS_INTERNAL, RRCrossings_Internal_result[0]))
except:
    print ("\n Unable to append Railroad Crossings - CRAW_INTERNAL from GIS")
    write_log("Unable to append Railroad Crossings - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Railroad Crossings - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Railroad Crossings - CRAW_INTERNAL from GIS completed")
write_log("       Updating Railroad Crossings - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Railroads - CRAW_INTERNAL from GIS")
write_log("\n Updating Railroads - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Railroads - CRAW_INTERNAL
    arcpy.DeleteRows_management(RAILROADS_INTERNAL)
except:
    print ("\n Unable to delete rows from Railroads - CRAW_INTERNAL")
    write_log("Unable to delete rows from Railroads - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Railroads - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append Railroads - CRAW_INTERNAL from GIS
    arcpy.Append_management(RAILROADS_GIS, RAILROADS_INTERNAL, "NO_TEST", "OPERATIONS_OWNER \"OPERATIONS OWNER\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROADS,OPERATIONS_OWNER,-1,-1;NON_OPERATIONS_OWNER \"NON-OPERATIONS OWNER\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROADS,NON_OPERATIONS_OWNER,-1,-1;TRACK_RIGHTS \"TRACK RIGHTS\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROADS,TRACK_RIGHTS,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROADS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNI FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROADS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROADS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROADS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROADS,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Transportation\\CCSDE.GIS.RAILROADS,SHAPE.STLength(),-1,-1", "")
    Railroads_Internal_result = arcpy.GetCount_management(RAILROADS_INTERNAL)
    print ('{} has {} records'.format(RAILROADS_INTERNAL, Railroads_Internal_result[0]))
except:
    print ("\n Unable to append Railroads - CRAW_INTERNAL from GIS")
    write_log("Unable to append Railroads - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Railroads - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Railroads - CRAW_INTERNAL from GIS completed")
write_log("       Updating Railroads - CRAW_INTERNAL from GIS completed", logfile)

print ("\n Updating Railroads - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Railroads - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Railroads - PUBLIC_WEB
    arcpy.DeleteRows_management(RAILROADS_WEB)
except:
    print ("\n Unable to delete rows from Railroads - PUBLIC_WEB")
    write_log("Unable to delete rows from Railroads - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Railroads - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append Railroads - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(RAILROADS_INTERNAL, RAILROADS_WEB, "NO_TEST", "OPERATIONS_OWNER \"OPERATIONS OWNER\" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL,OPERATIONS_OWNER,-1,-1;NON_OPERATIONS_OWNER \"NON-OPERATIONS OWNER\" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL,NON_OPERATIONS_OWNER,-1,-1;TRACK_RIGHTS \"TRACK RIGHTS\" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL,TRACK_RIGHTS,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNI FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL,UPDATE_DATE,-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL,SHAPE.STLength(),-1,-1", "")
    Railroads_Web_result = arcpy.GetCount_management(RAILROADS_WEB)
    print ('{} has {} records'.format(RAILROADS_WEB, Railroads_Web_result[0]))
except:
    print ("\n Unable to append Railroads - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Railroads - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Railroads - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Railroads - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Railroads - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL TRANSPORTATION DATASET UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL TRANSPORTATION DATASET UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
