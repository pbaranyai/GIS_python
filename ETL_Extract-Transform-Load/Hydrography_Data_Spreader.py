# ---------------------------------------------------------------------------
# Hydrography_Data_Spreader.py
# Created on: 2019-03-05 
# Updated on 2021-09-21
# Author: Phil Baranyai/GIS Manager
# Works in ArcGIS Pro
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# Dams
# Lakes 
# Rivers/Streams
# Dam evacuation routes
# Dam innundation zones
# Dam traffic control points
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
# ---------------------------------------------------------------------------

import sys,arcpy,datetime,time,logging

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\GIS\\Hydrography_Data_Spreader.log"  
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
    sys.exit ()

#Database Connection Folder
Database_Connections = r"\\FILELOCATION\\GIS\\ArcAutomations\\Database_Connections"

#Database variables:
CRAW_INTERNAL = Database_Connections + "\\craw_internal@ccsde.sde"
GIS = Database_Connections + "\\GIS@ccsde.sde"
OPEN_DATA = Database_Connections + "\\public_od@ccsde.sde"
PUBLIC_SAFETY = Database_Connections + "\\PUBLIC_SAFETY@ccsde.sde"
PUBLIC_WEB = Database_Connections + "\\public_web@ccsde.sde"

# Local variables:
DAM_GIS = GIS + "\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations"
DAM_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Locations_Internal"
DAM_EVAC_ROUTES_GIS = GIS + "\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Evacuation_Routes"
DAM_EVAC_ROUTES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Evacuation_Routes"
DAM_EVAC_ROUTES_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Hydrography\\CCSDE.PUBLIC_WEB.Dam_Evacuation_Routes"
DAM_INUNDATION_ZONES_GIS = GIS + "\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Inundation_Zones"
DAM_INUNDATION_ZONES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Inundation_Zones"
DAM_INUNDATION_ZONES_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Hydrography\\CCSDE.PUBLIC_WEB.Dam_Inundation_Zones"
DAM_TCP_GIS = GIS + "\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Traffic_Control_Points"
DAM_TCP_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Traffic_Control_Points"
DAM_TCP_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Hydrography\\CCSDE.PUBLIC_WEB.Dam_Traffic_Control_Points"
LAKES_GIS = GIS + "\\CCSDE.GIS.Hydrography\\CCSDE.GIS.LAKES"
LAKES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.LAKES_INTERNAL"
RIVERS_STREAMS_GIS = GIS + "\\CCSDE.GIS.Hydrography\\CCSDE.GIS.RIVERS_STREAMS"
RIVERS_STREAMS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.RIVERS_STREAMS_INTERNAL"

start_time = time.time()

print ("============================================================================")
print (("Updating Hydrography: "+ str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\nDam Feature Class")
print ("Lakes Feature Class" )
print ("Rivers/Streams Feature Class")
print ("Dam evacuation routes Feature Class")
print ("Dam inundation zones Feature Class")
print ("Dam traffic control points Feature Class")
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)")
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Hydrography: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nDam Feature Class", logfile)  
write_log("Lakes Feature Class", logfile) 
write_log("Rivers/Streams Feature Class", logfile)
write_log("Dam evacuation routes Feature Class", logfile)
write_log("Dam inundation zones Feature Class", logfile)
write_log("Dam traffic control points Feature Class", logfile)
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)", logfile)
write_log("Works in ArcGIS Pro", logfile)
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
    arcpy.Append_management(DAM_GIS, DAM_INTERNAL, "NO_TEST", 'NAME "Dam Name" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,NAME,-1,-1;WATER_BODY "Water Body" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,WATER_BODY,-1,-1;COUNTY_NAME "County Name" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,COUNTY_NAME,-1,-1;COUNTY_FIPS "County FIPS Code" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,COUNTY_FIPS,-1,-1;UPDATE_DATE "Last Edit Date" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,UPDATE_DATE,-1,-1;MUNICIPALITY "Municipality Name" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,MUNICIPALITY,-1,-1;DAM_CLASS "Classification" true true false 5 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,DAM_CLASS,-1,-1;DAM_PURPOSE_1 "Dam purpose code 1" true true false 4 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,DAM_PURPOSE_1,-1,-1;DAM_PURPOSE_2 "Dam purpose code 2" true true false 4 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,DAM_PURPOSE_2,-1,-1;DAM_PURPOSE_3 "Dam purpose code 3" true true false 4 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,DAM_PURPOSE_3,-1,-1;DAM_TYPE_1 "Dam Type 1" true true false 4 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,DAM_TYPE_1,-1,-1;DAM_TYPE_2 "Dam Type 2" true true false 4 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,DAM_TYPE_2,-1,-1;DAM_TYPE_3 "Dam Type 3" true true false 4 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,DAM_TYPE_3,-1,-1;HIGH_HAZARD "Is dam high-hazard?" true true false 5 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,HIGH_HAZARD,-1,-1;LATITUDE "Latitude" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,LATITUDE,-1,-1;LONGITUDE "Longitude" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,LONGITUDE,-1,-1;DAM_NUMBER "Dam Number" true true false 10 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,DAM_NUMBER,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Locations,Shape.STLength(),-1,-1', "")
    Dams_Internal_result = arcpy.GetCount_management(DAM_INTERNAL)
    print (('{} has {} records'.format(DAM_INTERNAL, Dams_Internal_result[0])))
except:
    print ("\n Unable to append Append Dams - CRAW_INTERNAL from GIS")
    write_log("Unable to append Append Dams - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Append Dams - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Append Dams - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Append Dams - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Lakes - CRAW_INTERNAL from GIS")
write_log("\n Updating Lakes - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Lakes - CRAW_INTERNAL
    arcpy.DeleteRows_management(LAKES_INTERNAL)
except:
    print ("\n Unable to delete rows from Lakes - CRAW_INTERNAL")
    write_log("Unable to delete rows from Lakes - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Lakes - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
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
    logging.exception('Got exception on append Append Lakes - CRAW_INERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Append Lakes - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Append Lakes - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Rivers/Streams - CRAW_INTERNAL from GIS")
write_log("\n Updating Rivers/Streams - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Rivers/Streams - CRAW_INTERNAL 
    arcpy.DeleteRows_management(RIVERS_STREAMS_INTERNAL)
except:
    print ("\n Unable to delete rows from Rivers/Streams - CRAW_INTERNAL")
    write_log("Unable to delete rows from Rivers/Streams - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Rivers/Streams - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
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
    logging.exception('Got exception on append Append Rivers/Streams - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Append Rivers/Streams - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Append Rivers/Streams - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Dam evacuation routes - CRAW_INTERNAL from GIS")
write_log("\n Updating Dam evacuation routes - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Dam evacuation routes - CRAW_INTERNAL 
    arcpy.DeleteRows_management(DAM_EVAC_ROUTES_INTERNAL)
except:
    print ("\n Unable to delete rows from Dam evacuation routes - CRAW_INTERNAL")
    write_log("Unable to delete rows from Dam evacuation routes - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Dam evacuation routes - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Dam evacuation routes - CRAW_INTERNAL from GIS
    arcpy.Append_management(DAM_EVAC_ROUTES_GIS, DAM_EVAC_ROUTES_INTERNAL, "NO_TEST", 'DAM_NAME "Dam Name" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Evacuation_Routes,DAM_NAME,-1,-1;WATERBODY "Waterbody" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Evacuation_Routes,WATERBODY,-1,-1;DATE_EDITED "Date Last Edited" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Evacuation_Routes,DATE_EDITED,-1,-1;DATE_STUDY_COMPLETED "Date Study Completed" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Evacuation_Routes,DATE_STUDY_COMPLETED,-1,-1;Engineering_Firm "Engineering firm that conducted study" true true false 255 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Evacuation_Routes,Engineering_Firm,-1,-1;STREET_NAME "Street Name" true true false 255 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Evacuation_Routes,STREET_NAME,-1,-1;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Evacuation_Routes,SHAPE.STLength(),-1,-1', "")
    DAM_EVAC_Internal_result = arcpy.GetCount_management(DAM_EVAC_ROUTES_INTERNAL)
    print (('{} has {} records'.format(DAM_EVAC_ROUTES_INTERNAL, DAM_EVAC_Internal_result[0])))
except:
    print ("\n Unable to append Append Dam evacuation routes - CRAW_INTERNAL from GIS")
    write_log("Unable to append Append Dam evacuation routes - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Append Dam evacuation routes - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Append Dam evacuation routes - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Append Dam evacuation routes - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Dam evacuation routes - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Dam evacuation routes - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Dam evacuation routes - PUBLIC_WEB
    arcpy.DeleteRows_management(DAM_EVAC_ROUTES_WEB)
except:
    print ("\n Unable to delete rows from Dam evacuation routes - PUBLIC_WEB")
    write_log("Unable to delete rows from Dam evacuation routes - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Dam evacuation routes - PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Dam evacuation routes - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(DAM_EVAC_ROUTES_INTERNAL, DAM_EVAC_ROUTES_WEB, "NO_TEST", 'DAM_NAME "Dam Name" true true false 75 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Evacuation_Routes,DAM_NAME,-1,-1;WATERBODY "Waterbody" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Evacuation_Routes,WATERBODY,-1,-1;DATE_EDITED "Date Last Edited" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Evacuation_Routes,DATE_EDITED,-1,-1;DATE_STUDY_COMPLETED "Date Study Completed" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Evacuation_Routes,DATE_STUDY_COMPLETED,-1,-1;Engineering_Firm "Engineering firm that conducted study" true true false 255 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Evacuation_Routes,Engineering_Firm,-1,-1;STREET_NAME "Street Name" true true false 255 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Evacuation_Routes,STREET_NAME,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Evacuation_Routes,SHAPE.STLength(),-1,-1', "")
    DAM_EVAC_Web_result = arcpy.GetCount_management(DAM_EVAC_ROUTES_WEB)
    print (('{} has {} records'.format(DAM_EVAC_ROUTES_WEB, DAM_EVAC_Web_result[0])))
except:
    print ("\n Unable to append Append Dam evacuation routes - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Append Dam evacuation routes - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Append Dam evacuation routes - PUBLIC_WEB from CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Append Dam evacuation routes - PUBLIC_WEB from CRAW_INTERNAL completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Append Dam evacuation routes - PUBLIC_WEB from CRAW_INTERNAL completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Dam inundation zones - CRAW_INTERNAL from GIS")
write_log("\n Updating Dam inundation zones - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Dam inundation zones - CRAW_INTERNAL 
    arcpy.DeleteRows_management(DAM_INUNDATION_ZONES_INTERNAL)
except:
    print ("\n Unable to delete rows from Dam inundation zones - CRAW_INTERNAL")
    write_log("Unable to delete rows from Dam inundation zones - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Dam inundation zones - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Dam inundation zones - CRAW_INTERNAL from GIS
    arcpy.Append_management(DAM_INUNDATION_ZONES_GIS, DAM_INUNDATION_ZONES_INTERNAL, "NO_TEST", 'DAM_NAME "Dam Name" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Inundation_Zones,DAM_NAME,-1,-1;WATERBODY "Waterbody" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Inundation_Zones,WATERBODY,-1,-1;DATE_EDITED "Date Last Edited" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Inundation_Zones,DATE_EDITED,-1,-1;DATE_STUDY_COMPLETED "Date Study Completed" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Inundation_Zones,DATE_STUDY_COMPLETED,-1,-1;Engineering_Firm "Engineering firm that conducted study" true true false 255 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Inundation_Zones,Engineering_Firm,-1,-1;Inundation_Type "Inundation type" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Inundation_Zones,Inundation_Type,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Inundation_Zones,SHAPE.STArea(),-1,-1;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Inundation_Zones,SHAPE.STLength(),-1,-1', "")
    DAM_INUNDATION_Internal_result = arcpy.GetCount_management(DAM_INUNDATION_ZONES_INTERNAL)
    print (('{} has {} records'.format(DAM_INUNDATION_ZONES_INTERNAL, DAM_INUNDATION_Internal_result[0])))
except:
    print ("\n Unable to append Append Dam inundation zones - CRAW_INTERNAL from GIS")
    write_log("Unable to append Append Dam inundation zones - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Append Dam inundation zones - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Append Dam inundation zones - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Append Dam inundation zones - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Dam inundation zones - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Dam inundation zones - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Dam inundation zones - PUBLIC_WEB
    arcpy.DeleteRows_management(DAM_INUNDATION_ZONES_WEB)
except:
    print ("\n Unable to delete rows from Dam inundation zones - PUBLIC_WEB")
    write_log("Unable to delete rows from Dam inundation zones - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Dam inundation zones - PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Dam inundation zones - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(DAM_INUNDATION_ZONES_INTERNAL, DAM_INUNDATION_ZONES_WEB, "NO_TEST", 'DAM_NAME "Dam Name" true true false 75 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Inundation_Zones,DAM_NAME,-1,-1;WATERBODY "Waterbody" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Inundation_Zones,WATERBODY,-1,-1;DATE_EDITED "Date Last Edited" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Inundation_Zones,DATE_EDITED,-1,-1;DATE_STUDY_COMPLETED "Date Study Completed" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Inundation_Zones,DATE_STUDY_COMPLETED,-1,-1;Engineering_Firm "Engineering firm that conducted study" true true false 255 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Inundation_Zones,Engineering_Firm,-1,-1;Inundation_Type "Inundation type" true true false 75 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Inundation_Zones,Inundation_Type,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Inundation_Zones,SHAPE.STArea(),-1,-1;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Inundation_Zones,SHAPE.STLength(),-1,-1', "")
    DAM_INUNDATION_Web_result = arcpy.GetCount_management(DAM_INUNDATION_ZONES_WEB)
    print (('{} has {} records'.format(DAM_INUNDATION_ZONES_WEB, DAM_INUNDATION_Web_result[0])))
except:
    print ("\n Unable to append Append Dam inundation zones - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Append Dam inundation zones - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Append Dam inundation zones - PUBLIC_WEB from CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Append Dam inundation zones - PUBLIC_WEB from CRAW_INTERNAL completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Append Dam inundation zones - PUBLIC_WEB from CRAW_INTERNAL completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Dam inundation traffic control points - CRAW_INTERNAL from GIS")
write_log("\n Updating Dam inundation traffic control points - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Dam inundation traffic control points - CRAW_INTERNAL 
    arcpy.DeleteRows_management(DAM_TCP_INTERNAL)
except:
    print ("\n Unable to delete rows from Dam inundation traffic control points - CRAW_INTERNAL")
    write_log("Unable to delete rows from Dam inundation traffic control points - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Dam inundation traffic control points - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Dam inundation traffic control points - CRAW_INTERNAL from GIS
    arcpy.Append_management(DAM_TCP_GIS, DAM_TCP_INTERNAL, "NO_TEST", 'DAM_NAME "Dam Name" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Traffic_Control_Points,DAM_NAME,-1,-1;WATERBODY "Waterbody" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Traffic_Control_Points,WATERBODY,-1,-1;DATE_EDITED "Date Last Edited" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Traffic_Control_Points,DATE_EDITED,-1,-1;DATE_STUDY_COMPLETED "Date Study Completed" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Traffic_Control_Points,DATE_STUDY_COMPLETED,-1,-1;TRAFFIC_CONTROL_POINT_DESIGNATI "Traffic Control Point Designation" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Traffic_Control_Points,TRAFFIC_CONTROL_POINT_DESIGNATI,-1,-1;Engineering_Firm "Engineering firm that conducted study" true true false 255 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Hydrography\\CCSDE.GIS.Dam_Traffic_Control_Points,Engineering_Firm,-1,-1', "")
    DAM_TCP_Internal_result = arcpy.GetCount_management(DAM_TCP_INTERNAL)
    print (('{} has {} records'.format(DAM_TCP_INTERNAL, DAM_TCP_Internal_result[0])))
except:
    print ("\n Unable to append Append Dam inundation traffic control points - CRAW_INTERNAL from GIS")
    write_log("Unable to append Append Dam inundation traffic control points - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Append Dam inundation zones - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Append Dam inundation traffic control points - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Append Dam inundation traffic control points - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Dam inundation traffic control points - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Dam inundation traffic control points - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Dam inundation traffic control points - PUBLIC_WEB
    arcpy.DeleteRows_management(DAM_TCP_WEB)
except:
    print ("\n Unable to delete rows from Dam inundation traffic control points - PUBLIC_WEB")
    write_log("Unable to delete rows from Dam inundation traffic control points - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Dam inundation traffic control points - PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Dam inundation traffic control points - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(DAM_TCP_INTERNAL, DAM_TCP_WEB, "NO_TEST", 'DAM_NAME "Dam Name" true true false 75 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Traffic_Control_Points,DAM_NAME,-1,-1;WATERBODY "Waterbody" true true false 100 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Traffic_Control_Points,WATERBODY,-1,-1;DATE_EDITED "Date Last Edited" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Traffic_Control_Points,DATE_EDITED,-1,-1;DATE_STUDY_COMPLETED "Date Study Completed" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Traffic_Control_Points,DATE_STUDY_COMPLETED,-1,-1;TRAFFIC_CONTROL_POINT_DESIGNATI "Traffic Control Point Designation" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Traffic_Control_Points,TRAFFIC_CONTROL_POINT_DESIGNATI,-1,-1;Engineering_Firm "Engineering firm that conducted study" true true false 255 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Hydrography\\CCSDE.CRAW_INTERNAL.Dam_Traffic_Control_Points,Engineering_Firm,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#', "")
    DAM_TCP_Web_result = arcpy.GetCount_management(DAM_TCP_WEB)
    print (('{} has {} records'.format(DAM_TCP_WEB, DAM_TCP_Web_result[0])))
except:
    print ("\n Unable to append Append Dam inundation traffic control points - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Append Dam inundation traffic control points - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Append Dam inundation traffic control points - PUBLIC_WEB from CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Append Dam inundation traffic control points - PUBLIC_WEB from CRAW_INTERNAL completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Append Dam inundation traffic control points - PUBLIC_WEB from CRAW_INTERNAL completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n ALL HYDROGRAPHY UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("\n ALL HYDROGRAPHY UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)

write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
