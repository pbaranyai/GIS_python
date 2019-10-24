# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Boundaries_CountyData_Spreader.py
# Created on: 2019-03-04 
# Updated on: 2019-06-06
#
# Author: Phil Baranyai/GIS Manager
# 
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB -> PUBLIC_OD as needed:
#  County Adjusted Municipal Boundary
#  County Boundary CL XY Boundary Points
#  Zipcodes
#  Assessor Areas
#  Surrounding County Boundaries
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
#import __builtin__
import builtins

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Boundaries_Data_Spreader.log"  
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
AST = "Database Connections\\AST@ccsde.sde"
CRAW_INTERNAL = "Database Connections\\craw_internal@ccsde.sde"
OPEN_DATA = "Database Connections\\public_od@ccsde.sde"
PUBLIC_SAFETY = "Database Connections\\PUBLIC_SAFETY@ccsde.sde"
PUBLIC_WEB = "Database Connections\\public_web@ccsde.sde"

# Local variables:
ASSESSOR_AREAS_AST = AST + "\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas"
ASSESSOR_AREAS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.CRAWFORD_ASSESSOR_AREAS_INTERNAL"
COUNTY_ADJ_MUNI_BOUND_PUBLIC_SAFETY = "Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES"
COUNTY_ADJ_MUNI_BOUND_INTERNAL = "Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL"
COUNTY_ADJ_MUNI_BOUND_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Boundaries\\CCSDE.PUBLIC_WEB.COUNTY_ADJ_MUNI_BOUND_WEB"
COUNTY_BOUNDARY_CL_XY_PUBLIC_SAFETY = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_BOUNDARY_CL_XY"
COUNTY_BOUNDARY_CL_XY_OD = OPEN_DATA + "\\CCSDE.PUBLIC_OD.Boundaries\\CCSDE.PUBLIC_OD.COUNTY_BOUNDARY_CL_XY_OD"
SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.SURROUNDING_COUNTY_BOUNDARIES"
SURROUNDING_CNTY_BOUND_PUBLIC_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Boundaries\\CCSDE.PUBLIC_WEB.SURROUNDING_COUNTY_BNDRY_WEB"
ZIPCODES_PUBLIC_SAFETY = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.ZIPCODES"
ZIPCODES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL"
ZIPCODES_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Boundaries\\CCSDE.PUBLIC_WEB.ZIPCODES_WEB"

start_time = time.time()

print ("===============================================================================================")
print (("UPDATING COUNTY BOUNDARIES: " + str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\n County Adjusted Municipal Boundary Feature Class")
print ("County Boundary CL XY Boundary Points Feature Class")
print ("Zipcodes Feature Class")
print ("Assessor Areas Feature Class")
print ("Surrounding County Boundaries")
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB -> PUBLIC_OD (where applicable)")
print ("===============================================================================================")

write_log("============================================================================", logfile)
write_log("UPDATING COUNTY BOUNDARIES: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\n County Adjusted Municipal Boundary Feature Class", logfile)  
write_log("County Boundary CL XY Boundary Points Feature Class", logfile) 
write_log("Zipcodes Feature Class", logfile)
write_log("Assessor Areas Feature Class", logfile)
write_log("Surrounding County Boundaries", logfile) 
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB -> PUBLIC_OD (where applicable)", logfile)
write_log("============================================================================", logfile)


print ("\n Updating CRAW_INTERNAL County Adjusted Municipal Boundaries from PUBLIC_SAFETY")
write_log("Updating CRAW_INTERNAL County Adjusted Municipal Boundaries from PUBLIC_SAFETY: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete rows from Crawford Adjusted Municipal Boundaries - CRAW_INTERNAL
    arcpy.DeleteRows_management(COUNTY_ADJ_MUNI_BOUND_INTERNAL)
except:
    print ("\n Unable to delete rows from Crawford Adjusted Municipal Boundaries - CRAW_INTERNAL")
    write_log("Unable to delete rows from Crawford Adjusted Municipal Boundaries - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Crawford Adjusted Municipal Boundaries - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(COUNTY_ADJ_MUNI_BOUND_PUBLIC_SAFETY, COUNTY_ADJ_MUNI_BOUND_INTERNAL, "NO_TEST", "MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,SHAPE.STLength(),-1,-1", "")
    AdjMuniBound_Internal_result = arcpy.GetCount_management(COUNTY_ADJ_MUNI_BOUND_INTERNAL)
    print (('{} has {} records'.format(COUNTY_ADJ_MUNI_BOUND_INTERNAL, AdjMuniBound_Internal_result[0])))
except:
    print ("\n Unable to append County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)
    
print ("\n Updating PUBLIC_WEB County Adjusted Municipal Boundaries from CRAW_INTERNAL")
write_log("\n Updating PUBLIC_WEB County Adjusted Municipal Boundaries from CRAW_INTERNAL", logfile)


try:
    # Delete rows County Adjusted Municipal Boundaries - PUBLIC_WEB
    arcpy.DeleteRows_management(COUNTY_ADJ_MUNI_BOUND_WEB)
except:
    print ("\n Unable to delete rows County Adjusted Municipal Boundaries - PUBLIC_WEB")
    write_log("Unable to delete rows County Adjusted Municipal Boundaries - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows County Adjusted Municipal Boundaries - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Append County Adjusted Municipal Boundaries - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(COUNTY_ADJ_MUNI_BOUND_INTERNAL, COUNTY_ADJ_MUNI_BOUND_WEB, "NO_TEST", "MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL,UPDATE_DATE,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL,SHAPE.STLength(),-1,-1", "")
    AdjMuniBound_Web_result = arcpy.GetCount_management(COUNTY_ADJ_MUNI_BOUND_WEB)
    print (('{} has {} records'.format(COUNTY_ADJ_MUNI_BOUND_WEB, AdjMuniBound_Web_result[0])))
except:
    print ("\n Unable to append County Adjusted Municipal Boundaries - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append County Adjusted Municipal Boundaries - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append County Adjusted Municipal Boundaries - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating County Adjusted Municipal Boundaries - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating County Adjusted Municipal Boundaries - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)
    
print ("\n Updating Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete rows Zipcodes - CRAW_INTERNAL from CRAW_INTERNAL
    arcpy.DeleteRows_management(ZIPCODES_INTERNAL)
except:
    print ("\n Unable to delete rows Zipcodes - CRAW_INTERNAL")
    write_log("Unable to delete rows Zipcodes - CRAW_INTERNAL from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows Zipcodes - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(ZIPCODES_PUBLIC_SAFETY, ZIPCODES_INTERNAL, "NO_TEST", "POST_OFFICE \"POST OFFICE\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.ZIPCODES,POST_OFFICE,-1,-1;ZIPCODE \"ZIPCODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.ZIPCODES,ZIPCODE,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.ZIPCODES,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.ZIPCODES,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE_DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.ZIPCODES,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.ZIPCODES,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.ZIPCODES,SHAPE.STLength(),-1,-1", "")
    Zipcode_Internal_result = arcpy.GetCount_management(ZIPCODES_INTERNAL)
    print (('{} has {} records'.format(ZIPCODES_INTERNAL, Zipcode_Internal_result[0])))
except:
    print ("\n Unable to append Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating Zipcodes - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Zipcodes - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete rows Zipcodes - PUBLIC_WEB
    arcpy.DeleteRows_management(ZIPCODES_WEB)
except:
    print ("\n Unable to delete rows Zipcodes - PUBLIC_WEB")
    write_log("Unable to delete rows Zipcodes - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows Zipcodes - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Zipcodes - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(ZIPCODES_INTERNAL, ZIPCODES_WEB, "NO_TEST", "POST_OFFICE \"POST OFFICE\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,POST_OFFICE,-1,-1;ZIPCODE \"ZIPCODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,ZIPCODE,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE_DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,UPDATE_DATE,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,SHAPE.STLength(),-1,-1", "")
    Zipcode_Web_result = arcpy.GetCount_management(ZIPCODES_WEB)
    print (('{} has {} records'.format(ZIPCODES_WEB, Zipcode_Web_result[0])))
except:
    print ("\n Unable to append Zipcodes - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Zipcodes - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Zipcodes - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Zipcodes - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Zipcodes - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

print ("\n Updating Assessor Areas - CRAW_INTERNAL from AST")
write_log("\n Updating Assessor Areas - CRAW_INTERNAL from AST", logfile)
    
try:
    # Delete rows Assessor Areas - CRAW_INTERNAL
    arcpy.DeleteRows_management(ASSESSOR_AREAS_INTERNAL)
except:
    print ("\n Unable to delete rows Assessor Areas - CRAW_INTERNAL")
    write_log("Unable to delete rows Assessor Areas - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows Assessor Areas - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Assessor Areas - CRAW_INTERNAL from AST
    arcpy.Append_management(ASSESSOR_AREAS_AST, ASSESSOR_AREAS_INTERNAL, "NO_TEST", "MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas,UPDATE_DATE,-1,-1;MUNICIPAL_NUMBER \"MUNICIPAL NUMBER\" true true false 2 Short 0 5 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas,MUNICIPAL_NUMBER,-1,-1;CITY_WARD \"CITY WARD\" true true false 2 Short 0 5 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas,CITY_WARD,-1,-1;ASSESSOR_NAME \"ASSESSOR_NAME\" true true false 75 Text 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas,ASSESSOR_NAME,-1,-1;Shape.STArea() \"Shape.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas,SHAPE.STArea(),-1,-1;Shape.STLength() \"Shape.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\AST@ccsde.sde\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas,SHAPE.STLength(),-1,-1", "")
    AssessorArea_Internal_result = arcpy.GetCount_management(ASSESSOR_AREAS_INTERNAL)
    print (('{} has {} records'.format(ASSESSOR_AREAS_INTERNAL, AssessorArea_Internal_result[0])))
except:
    print ("\n Unable to append Assessor Areas - CRAW_INTERNAL from AST")
    write_log("Unable to append Assessor Areas - CRAW_INTERNAL from AST", logfile)
    logging.exception('Got exception on append Assessor Areas - CRAW_INTERNAL from AST logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Assessor Areas - CRAW_INTERNAL from AST completed")
write_log("       Updating Assessor Areas - CRAW_INTERNAL from AST completed", logfile)

print ("\n Updating County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY")
write_log("\n Updating County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY", logfile)

try:
    # Delete rows County Boundary Centerline XY Snap Points - PUBLIC_OD
    arcpy.DeleteRows_management(COUNTY_BOUNDARY_CL_XY_OD)
except:
    print ("\n Unable to delete rows County Boundary Centerline XY Snap Points - PUBLIC_OD")
    write_log("Unable to delete rows County Boundary Centerline XY Snap Points - PUBLIC_OD", logfile)
    logging.exception('Got exception on delete rows County Boundary Centerline XY Snap Points - PUBLIC_OD logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY
    arcpy.Append_management(COUNTY_BOUNDARY_CL_XY_PUBLIC_SAFETY, COUNTY_BOUNDARY_CL_XY_OD, "NO_TEST", "COUNTY_1_NAME \"COUNTY 1 NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_BOUNDARY_CL_XY,COUNTY_1_NAME,-1,-1;COUNTY_2_NAME \"COUNTY 2 NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_BOUNDARY_CL_XY,COUNTY_2_NAME,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_BOUNDARY_CL_XY,UPDATE_DATE,-1,-1;LATITUDE \"LATITUDE\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_BOUNDARY_CL_XY,LATITUDE,-1,-1;LONGITUDE \"LONGITUDE\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_BOUNDARY_CL_XY,LONGITUDE,-1,-1", "")
    CLXY_Internal_result = arcpy.GetCount_management(COUNTY_BOUNDARY_CL_XY_OD)
    print (('{} has {} records'.format(COUNTY_BOUNDARY_CL_XY_OD, CLXY_Internal_result[0])))
except:
    print ("\n Unable to append County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY")
    write_log("Unable to append County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY completed")
write_log("       Updating County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY completed", logfile)

print ("\n Updating Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY")
write_log("\n Updating Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY", logfile)

try:
    # Delete rows Surrounding County Boundaries - PUBLIC_WEB
    arcpy.DeleteRows_management(SURROUNDING_CNTY_BOUND_PUBLIC_WEB)
except:
    print ("\n Unable to delete rows Surrounding County Boundaries - PUBLIC_WEB")
    write_log("Unable to delete rows Surrounding County Boundaries - PUBLIC_WEBL", logfile)
    logging.exception('Got exception on delete rows Surrounding County Boundaries - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY
    arcpy.Append_management(SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY, SURROUNDING_CNTY_BOUND_PUBLIC_WEB, "NO_TEST", 'COUNTY_NAME "County Name" true true false 100 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.SURROUNDING_COUNTY_BOUNDARIES,COUNTY_NAME,-1,-1;COUNTY_FIPS "County FIPS Code" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.SURROUNDING_COUNTY_BOUNDARIES,COUNTY_FIPS,-1,-1;STATE "State" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.SURROUNDING_COUNTY_BOUNDARIES,STATE,-1,-1;UPDATE_DATE "Update Date" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.SURROUNDING_COUNTY_BOUNDARIES,UPDATE_DATE,-1,-1;COUNTY_GIS_URL "County GIS Website" true true false 255 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.SURROUNDING_COUNTY_BOUNDARIES,COUNTY_GIS_URL,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.SURROUNDING_COUNTY_BOUNDARIES,SHAPE.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.SURROUNDING_COUNTY_BOUNDARIES,SHAPE.STLength(),-1,-1', "")
    SurroundCnty_result = arcpy.GetCount_management(SURROUNDING_CNTY_BOUND_PUBLIC_WEB)
    print (('{} has {} records'.format(SURROUNDING_CNTY_BOUND_PUBLIC_WEB, SurroundCnty_result[0])))
except:
    print ("\n Unable to append Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY")
    write_log("Unable to append Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY completed")
write_log("       Updating Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("===========================================================")
print (("       ALL BOUNDARY UPDATES HAVE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("       ALL BOUNDARY UPDATES HAVE COMPLETED: " + str(Day) + " " + str(end_time), logfile)
write_log("===========================================================",logfile)

print (("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)))
write_log("Elapsed time: " + str (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)

write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
