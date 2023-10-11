# ---------------------------------------------------------------------------
# Daily_Land_Records_Data_Spreader.py
# Created on: 2020-08-10 
# Updated on 2021-09-21
# Works in ArcPro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL:
#  
# SALDO_Closure_Checks
# Georeferenced_Maps_Assessment
# Georeferenced_Maps_GIS
# 
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
# ---------------------------------------------------------------------------

import arcpy
import sys
import datetime
import os
import logging

# Stop geoprocessing log history in metadata
arcpy.SetLogHistory(False)

# Setup error logging
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\GIS\\Daily_Land_Records_Data_Spreader.log"  
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
Database_Connections = r"\\FILELOCATION\\GIS\\ArcAutomations\\Database_Connections"

#Database variables:
CRAW_INTERNAL = Database_Connections + "\\craw_internal@ccsde.sde"
AST = Database_Connections + "\\AST@ccsde.sde"
GIS = Database_Connections + "\\GIS@ccsde.sde"
PLANNING = Database_Connections + "\\PLANNING@ccsde.sde"

# Local variables:
GEOREFERENCED_MAPS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Georeferenced_Maps_Assessment"
GEOREFERENCED_MAPS_GIS = GIS + "\\CCSDE.GIS.Land_Records\\CCSDE.GIS.Georeferenced_Maps_GIS"
GEOREFERENCED_MAPS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.Georeferenced_Maps_Internal"
SALDO_CLOSURE_CHECKS_PLANNING = PLANNING + "\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks"
SALDO_CLOSURE_CHECKS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.SALDO_Closure_Checks"

start_time = time.time()

print ("============================================================================")
print (("Updating Daily Land Record data feature classes: "+ str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\nSALDO Closure Checks")
print ("Georeferenced Maps - Assessment")
print ("Georeferenced Maps - GIS")
print ("\n From source to CRAW_INTERNAL")
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Daily Land Record data feature classes: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nSALDO Closure Checks", logfile)
write_log("Georeferenced Maps - Assessment", logfile)
write_log("Georeferenced Maps - GIS", logfile)
write_log("\n From source to CRAW_INTERNAL", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Updating SALDO Closure Checks - CRAW_INTERNAL from PLANNING")
write_log("\n Updating SALDO Closure Checks - CRAW_INTERNAL from PLANNING: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete rows from SALDO Closure Checks - CRAW_INTERNAL
    arcpy.DeleteRows_management(SALDO_CLOSURE_CHECKS_INTERNAL)
except:
    print ("\n Unable to delete rows from SALDO Closure Checks - CRAW_INTERNAL")
    write_log("Unable to delete rows from SALDO Closure Checks - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from SALDO Closure Checks - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append SALDO Closure Checks - CRAW_INTERNAL from PLANNING
    arcpy.Append_management(SALDO_CLOSURE_CHECKS_PLANNING, SALDO_CLOSURE_CHECKS_INTERNAL,"NO_TEST", 'Date "Date" true true false 8 Date 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks,Date,-1,-1;Direction "COGO Direction" true true false 12 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks,Direction,-1,-1;Distance "COGO Distance" true true false 10 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks,Distance,-1,-1;Delta "COGO Delta" true true false 10 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks,Delta,-1,-1;Radius "COGO Radius" true true false 10 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks,Radius,-1,-1;Tangent "COGO Tangent" true true false 10 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks,Tangent,-1,-1;ArcLength "COGO ArcLength" true true false 10 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks,ArcLength,-1,-1;Side "COGO Side" true true false 1 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks,Side,-1,-1;Locate_Line "Locate_Line" true true false 10 Text 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks,Locate_Line,-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\PLANNING@ccsde.sde\\CCSDE.PLANNING.Land_Records\\CCSDE.PLANNING.SALDO_Closure_Checks,Shape.STLength(),-1,-1', "")
    SALDO_Closures_Internal_result = arcpy.GetCount_management(SALDO_CLOSURE_CHECKS_INTERNAL)
    print (('{} has {} records'.format(SALDO_CLOSURE_CHECKS_INTERNAL, SALDO_Closures_Internal_result[0])))
except:
    print ("\n Unable to append SALDO Closure Checks - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append SALDO Closure Checks - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append SALDO Closure Checks - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating SALDO Closure Checks - CRAW_INTERNAL from PLANNING completed")
write_log("       Updating SALDO Closure Checks - CRAW_INTERNAL from PLANNING completed", logfile)


print ("\n Updating Georeferenced maps - CRAW_INTERNAL from ASSESSMENT")
write_log("\n Updating Georeferenced maps - CRAW_INTERNAL from ASSESSMENT: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete rows from Georeferenced maps - CRAW_INTERNAL
    arcpy.DeleteRows_management(GEOREFERENCED_MAPS_INTERNAL)
except:
    print ("\n Unable to delete rows from Georeferenced maps - CRAW_INTERNAL")
    write_log("Unable to delete rows from Georeferenced maps - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Georeferenced maps - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append Georeferenced maps - CRAW_INTERNAL from ASSESSMENT
    arcpy.Append_management(GEOREFERENCED_MAPS_AST, GEOREFERENCED_MAPS_INTERNAL, "NO_TEST", 'NAME_DESCRIPTION "Name or Description" true true false 2500 Text 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Georeferenced_Maps_Assessment,NAME_DESCRIPTION,-1,-1;COUNTY_NETWORK_PATH "Location on shared drive in County Network" true true false 500 Text 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Georeferenced_Maps_Assessment,COUNTY_NETWORK_PATH,-1,-1;SCANNED_ITEM_CREATION_DATE "Date of scanned item creation" true true false 8 Date 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Georeferenced_Maps_Assessment,SCANNED_ITEM_CREATION_DATE,-1,-1;PROPERTY_TYPE "Type of property scan" true true false 50 Text 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Georeferenced_Maps_Assessment,PROPERTY_TYPE,-1,-1;DATE_ADDED "Date georeferenced" true true false 8 Date 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Georeferenced_Maps_Assessment,DATE_ADDED,-1,-1;COUNTY_NAME "County Name" true true false 50 Text 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Georeferenced_Maps_Assessment,COUNTY_NAME,-1,-1;COUNTY_FIPS "County FIPS Code" true true false 8 Double 8 38 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Georeferenced_Maps_Assessment,COUNTY_FIPS,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Georeferenced_Maps_Assessment,SHAPE.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Georeferenced_Maps_Assessment,SHAPE.STLength(),-1,-1', "")
except:
    print ("\n Unable to append Georeferenced maps - CRAW_INTERNAL from ASSESSMENT")
    write_log("Unable to append Georeferenced maps - CRAW_INTERNAL from ASSESSMENT", logfile)
    logging.exception('Got exception on append Georeferenced maps - CRAW_INTERNAL from ASSESSMENT logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append Georeferenced maps - CRAW_INTERNAL from GIS
    arcpy.Append_management(GEOREFERENCED_MAPS_GIS, GEOREFERENCED_MAPS_INTERNAL, "NO_TEST", 'NAME_DESCRIPTION "Name or Description" true true false 2500 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Land_Records\\CCSDE.GIS.Georeferenced_Maps_GIS,NAME_DESCRIPTION,-1,-1;COUNTY_NETWORK_PATH "Location on shared drive in County Network" true true false 500 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Land_Records\\CCSDE.GIS.Georeferenced_Maps_GIS,COUNTY_NETWORK_PATH,-1,-1;SCANNED_ITEM_CREATION_DATE "Date of scanned item creation" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Land_Records\\CCSDE.GIS.Georeferenced_Maps_GIS,SCANNED_ITEM_CREATION_DATE,-1,-1;PROPERTY_TYPE "Type of property scan" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Land_Records\\CCSDE.GIS.Georeferenced_Maps_GIS,PROPERTY_TYPE,-1,-1;DATE_ADDED "Date georeferenced" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Land_Records\\CCSDE.GIS.Georeferenced_Maps_GIS,DATE_ADDED,-1,-1;COUNTY_NAME "County Name" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Land_Records\\CCSDE.GIS.Georeferenced_Maps_GIS,COUNTY_NAME,-1,-1;COUNTY_FIPS "County FIPS Code" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Land_Records\\CCSDE.GIS.Georeferenced_Maps_GIS,COUNTY_FIPS,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Land_Records\\CCSDE.GIS.Georeferenced_Maps_GIS,Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Land_Records\\CCSDE.GIS.Georeferenced_Maps_GIS,Shape.STLength(),-1,-1', "")
    Georeferenced_Maps_Internal_result = arcpy.GetCount_management(GEOREFERENCED_MAPS_INTERNAL)
    print (('{} has {} records'.format(GEOREFERENCED_MAPS_INTERNAL, Georeferenced_Maps_Internal_result[0])))
except:
    print ("\n Unable to append Georeferenced maps - CRAW_INTERNAL from GIS")
    write_log("Unable to append Georeferenced maps - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Georeferenced maps - CRAW_INTERNAL from GIS logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Georeferenced maps - CRAW_INTERNAL from ASSESSMENT & GIS completed")
write_log("       Updating Georeferenced maps - CRAW_INTERNAL from ASSESSMENT & GIS completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n ALL DAILY LAND RECORD DATA FEATURE CLASSES UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("\n ALL DAILY LAND RECORD DATA FEATURE CLASSES UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print (("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)))
write_log("Elapsed time: " + str (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
