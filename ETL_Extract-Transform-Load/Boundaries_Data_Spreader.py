# ---------------------------------------------------------------------------
# Boundaries_CountyData_Spreader.py
# Created on: 2019-03-04 
# Updated on: 2019-09-21
# Works in ArcPro
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
#  Crawford County Municipal Boundaries
#  Crawford County Municipal Boundaries Relate
#  Address Points Web Relate
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
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\GIS\\Boundaries_Data_Spreader.log"  
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
AST = Database_Connections + "\\AST@ccsde.sde"
CRAW_INTERNAL = Database_Connections + "\\craw_internal@ccsde.sde"
OPEN_DATA = Database_Connections + "\\public_od@ccsde.sde"
PLANNING = Database_Connections + "\\PLANNING@ccsde.sde"
PUBLIC_SAFETY = Database_Connections + "\\PUBLIC_SAFETY@ccsde.sde"
PUBLIC_WEB = Database_Connections + "\\public_web@ccsde.sde"

# Local variables:
ASSESSOR_AREAS_AST = AST + "\\CCSDE.AST.Assessor_Responsibilities\\CCSDE.AST.Assessor_Areas"
ASSESSOR_AREAS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.CRAWFORD_ASSESSOR_AREAS_INTERNAL"
ADDRESS_POINTS_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Land_Records\\CCSDE.PUBLIC_WEB.Site_Structure_Address_Points_WEB"
ADDRESS_POINTS_WEB_RELATE = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Boundaries\\CCSDE.PUBLIC_WEB.ADDRESS_POINTS_WEB_RELATE"
COUNTY_ADJ_MUNI_BOUND_PUBLIC_SAFETY = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES"
COUNTY_ADJ_MUNI_BOUND_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL"
COUNTY_BOUNDARY_CL_XY_PUBLIC_SAFETY = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_BOUNDARY_CL_XY"
COUNTY_BOUNDARY_CL_XY_OD = OPEN_DATA + "\\CCSDE.PUBLIC_OD.Boundaries\\CCSDE.PUBLIC_OD.COUNTY_BOUNDARY_CL_XY_OD"
CRAWFORD_COUNTY_MUNI_PLANNING = PLANNING + "\\CCSDE.PLANNING.Crawford_Co_Data\\CCSDE.PLANNING.CRAWFORD_MUNICIPAL_BOUNDARIES"
CRAWFORD_COUNTY_MUNI_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.CRAWFORD_MUNICIPAL_BOUNDARIES_INTERNAL"
CRAWFORD_COUNTY_MUNI_WEB_RELATE = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Boundaries\\CCSDE.PUBLIC_WEB.CRAWFORD_MUNICIPAL_BOUNDARIES_WEB_RELATE"
SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.SURROUNDING_COUNTY_BOUNDARIES"
SURROUNDING_CNTY_BOUND_PUBLIC_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Boundaries\\CCSDE.PUBLIC_WEB.SURROUNDING_COUNTY_BNDRY_WEB"
ZIPCODES_PUBLIC_SAFETY = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.ZIPCODES"
ZIPCODES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL"

start_time = time.time()
elapsed_time = time.time() - start_time

print ("===============================================================================================")
print (("UPDATING COUNTY BOUNDARIES: " + str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\n County Adjusted Municipal Boundary Feature Class")
print ("County Boundary CL XY Boundary Points Feature Class")
print ("Zipcodes Feature Class")
print ("Assessor Areas Feature Class")
print ("Surrounding County Boundaries")
print ("Crawford County Municpal Boundaries")
print ("Crawford County Municpal Boundaries Relate")
print ("Address Point Web Relate")
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB -> PUBLIC_OD (where applicable)")
print ("Works in ArcGIS Pro")
print ("===============================================================================================")

write_log("============================================================================", logfile)
write_log("UPDATING COUNTY BOUNDARIES: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\n County Adjusted Municipal Boundary Feature Class", logfile)  
write_log("County Boundary CL XY Boundary Points Feature Class", logfile) 
write_log("Zipcodes Feature Class", logfile)
write_log("Assessor Areas Feature Class", logfile)
write_log("Surrounding County Boundaries", logfile)
write_log("Crawford County Municpal Boundaries", logfile)
write_log("Crawford County Municpal Boundaries Relate", logfile)
write_log("Address Points Web Relate", logfile)
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB -> PUBLIC_OD (where applicable)", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)


print ("\n Updating CRAW_INTERNAL County Adjusted Municipal Boundaries from PUBLIC_SAFETY")
write_log("Updating CRAW_INTERNAL County Adjusted Municipal Boundaries from PUBLIC_SAFETY: " + time.strftime("%I:%M:%S %p", time.localtime()), logfile)

try:
    # Delete rows from Crawford Adjusted Municipal Boundaries - CRAW_INTERNAL
    arcpy.DeleteRows_management(COUNTY_ADJ_MUNI_BOUND_INTERNAL)
except:
    print ("\n Unable to delete rows from Crawford Adjusted Municipal Boundaries - CRAW_INTERNAL")
    write_log("Unable to delete rows from Crawford Adjusted Municipal Boundaries - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Crawford Adjusted Municipal Boundaries - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(COUNTY_ADJ_MUNI_BOUND_PUBLIC_SAFETY, COUNTY_ADJ_MUNI_BOUND_INTERNAL, "NO_TEST", 'MUNI_NAME "MUNICIPALITY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,MUNI_NAME,-1,-1;MUNI_FIPS "MUNICIPALITY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,MUNI_FIPS,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,UPDATE_DATE,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#;STATE "State" true true false 2 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,STATE,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,DiscrpAgID,-1,-1;COUNTRY "Country" true true false 2 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,COUNTRY,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,SHAPE.STArea(),-1,-1;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Boundaries\\CCSDE.PUBLIC_SAFETY.COUNTY_ADJ_MUNI_BOUNDARIES,SHAPE.STLength(),-1,-1', "")
    AdjMuniBound_Internal_result = arcpy.GetCount_management(COUNTY_ADJ_MUNI_BOUND_INTERNAL)
    print (('{} has {} records'.format(COUNTY_ADJ_MUNI_BOUND_INTERNAL, AdjMuniBound_Internal_result[0])))
except:
    print ("\n Unable to append County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY completed at "+time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating County Adjusted Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    
print ("\n Updating Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete rows Zipcodes - CRAW_INTERNAL from CRAW_INTERNAL
    arcpy.DeleteRows_management(ZIPCODES_INTERNAL)
except:
    print ("\n Unable to delete rows Zipcodes - CRAW_INTERNAL")
    write_log("Unable to delete rows Zipcodes - CRAW_INTERNAL from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows Zipcodes - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
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
    logging.exception('Got exception on append Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Zipcodes - CRAW_INTERNAL from PUBLIC_SAFETY completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Assessor Areas - CRAW_INTERNAL from AST")
write_log("\n Updating Assessor Areas - CRAW_INTERNAL from AST", logfile)
    
try:
    # Delete rows Assessor Areas - CRAW_INTERNAL
    arcpy.DeleteRows_management(ASSESSOR_AREAS_INTERNAL)
except:
    print ("\n Unable to delete rows Assessor Areas - CRAW_INTERNAL")
    write_log("Unable to delete rows Assessor Areas - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows Assessor Areas - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
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
    logging.exception('Got exception on append Assessor Areas - CRAW_INTERNAL from AST logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Assessor Areas - CRAW_INTERNAL from AST completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Assessor Areas - CRAW_INTERNAL from AST completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY")
write_log("\n Updating County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY", logfile)

try:
    # Delete rows County Boundary Centerline XY Snap Points - PUBLIC_OD
    arcpy.DeleteRows_management(COUNTY_BOUNDARY_CL_XY_OD)
except:
    print ("\n Unable to delete rows County Boundary Centerline XY Snap Points - PUBLIC_OD")
    write_log("Unable to delete rows County Boundary Centerline XY Snap Points - PUBLIC_OD", logfile)
    logging.exception('Got exception on delete rows County Boundary Centerline XY Snap Points - PUBLIC_OD logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
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
    logging.exception('Got exception on append County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating County Boundary Centerline XY Snap Points - PUBLIC_OD from PUBLIC_SAFETY completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY")
write_log("\n Updating Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY", logfile)

try:
    # Delete rows Surrounding County Boundaries - PUBLIC_WEB
    arcpy.DeleteRows_management(SURROUNDING_CNTY_BOUND_PUBLIC_WEB)
except:
    print ("\n Unable to delete rows Surrounding County Boundaries - PUBLIC_WEB")
    write_log("Unable to delete rows Surrounding County Boundaries - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows Surrounding County Boundaries - PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY
    arcpy.Append_management(SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY, SURROUNDING_CNTY_BOUND_PUBLIC_WEB, "NO_TEST", 'COUNTY_NAME "County Name" true true false 100 Text 0 0 ,First,#,'+SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY+',COUNTY_NAME,-1,-1;COUNTY_FIPS "County FIPS Code" true true false 8 Double 8 38 ,First,#,'+SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY+',COUNTY_FIPS,-1,-1;STATE "State" true true false 50 Text 0 0 ,First,#,'+SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY+',STATE,-1,-1;UPDATE_DATE "Update Date" true true false 8 Date 0 0 ,First,#,'+SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY+',UPDATE_DATE,-1,-1;COUNTY_GIS_URL "County GIS Website" true true false 255 Text 0 0 ,First,#,'+SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY+',COUNTY_GIS_URL,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY+',SHAPE.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+SURROUNDING_CNTY_BOUND_PUBLIC_SAFETY+',SHAPE.STLength(),-1,-1', "")
    SurroundCnty_result = arcpy.GetCount_management(SURROUNDING_CNTY_BOUND_PUBLIC_WEB)
    print (('{} has {} records'.format(SURROUNDING_CNTY_BOUND_PUBLIC_WEB, SurroundCnty_result[0])))
except:
    print ("\n Unable to append Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY")
    write_log("Unable to append Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Surrounding County Boundaries - PUBLIC_WEB from PUBLIC_SAFETY completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating CRAW_INTERNAL Crawford County Municipal Boundaries from PLANNING")
write_log("Updating CRAW_INTERNAL Crawford County Municipal Boundaries from PLANNING: " + time.strftime("%I:%M:%S %p", time.localtime()), logfile)

try:
    # Delete rows from Crawford County Municipal Boundaries - CRAW_INTERNAL
    arcpy.DeleteRows_management(CRAWFORD_COUNTY_MUNI_INTERNAL)
except:
    print ("\n Unable to delete rows from Crawford County Municipal Boundaries - CRAW_INTERNAL")
    write_log("Unable to delete rows from Crawford County Municipal Boundaries - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Crawford County Municipal Boundaries - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Crawford County Municipal Boundaries - CRAW_INTERNAL from PLANNING
    arcpy.Append_management(CRAWFORD_COUNTY_MUNI_PLANNING, CRAWFORD_COUNTY_MUNI_INTERNAL, "NO_TEST", 'Municipality "Municipality Name" true true false 50 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',MUNI_NAME,-1,-1;FIPS "Municipal FIPS Code" true true false 8 Double 8 38 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',MUNI_FIPS,-1,-1;COUNTY_NAME "County Name" true true false 50 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',COUNTY_NAME,-1,-1;COUNTY_FIPS "County FIPS Code" true true false 8 Double 8 38 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',COUNTY_FIPS,-1,-1;UPDATE_DATE "Last Update Date" true true false 8 Date 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',UPDATE_DATE,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#;MAILING_STREET_ADDRESS "Mailing Street Address" true true false 50 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',MAILING_STREET_ADDRESS,-1,-1;MAILING_CITY_ADDRESS "Mailing Address City" true true false 50 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',MAILING_CITY_ADDRESS,-1,-1;MAILING_ZIP_ADDRESS "Mailing Address Zipcode" true true false 50 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',MAILING_ZIP_ADDRESS,-1,-1;PHYSICAL_STREET_ADDRESS "Physical Street Address" true true false 50 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',PHYSICAL_STREET_ADDRESS,-1,-1;PHYSICAL_CITY_ADDRESS "Physical Address City" true true false 50 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',PHYSICAL_CITY_ADDRESS,-1,-1;PHYSICAL_ZIP_ADDRESS "Physical Address Zipcode" true true false 8 Double 8 38 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',PHYSICAL_ZIP_ADDRESS,-1,-1;EMAIL_ADDRESS "Email address" true true false 100 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',EMAIL_ADDRESS,-1,-1;WEBSITE "Website" true true false 150 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',WEBSITE,-1,-1;OFFICE_HOURS "Office Hours" true true false 75 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',OFFICE_HOURS,-1,-1;OFFICE_PHONE "Office Phone #" true true false 60 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',OFFICE_PHONE,-1,-1;ZONING_ORDINANCE "Zoning ordinance available?" true true false 5 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',ZONING_ORDINANCE,-1,-1;SALDO "SALDO available?" true true false 5 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',SALDO,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_PLANNING+',Shape.STLength(),-1,-1', "")
    CCMuniBound_Internal_result = arcpy.GetCount_management(CRAWFORD_COUNTY_MUNI_INTERNAL)
    print (('{} has {} records'.format(CRAWFORD_COUNTY_MUNI_INTERNAL, CCMuniBound_Internal_result[0])))
except:
    print ("\n Unable to append Crawford County Municipal Boundaries - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append Crawford County Municipal Boundaries - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append Crawford County Municipal Boundaries - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Crawford County Municipal Boundaries - CRAW_INTERNAL from PLANNING completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Crawford County Municipal Boundaries - CRAW_INTERNAL from PLANNING completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating PUBLIC_WEB Crawford County Municipal Boundaries Relate from CRAW_INTERNAL")
write_log("Updating PUBLIC_WEB Crawford County Municipal Boundaries Relate from CRAW_INTERNAL: " + time.strftime("%I:%M:%S %p", time.localtime()), logfile)

try:
    # Delete rows from Crawford County Municipal Boundaries Relate - PUBLIC_WEB
    arcpy.DeleteRows_management(CRAWFORD_COUNTY_MUNI_WEB_RELATE)
except:
    print ("\n Unable to delete rows from Crawford County Municipal Boundaries Relate - PUBLIC_WEB")
    write_log("Unable to delete rows from Crawford County Municipal Boundaries Relate - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Crawford County Municipal Boundaries Relate - PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Crawford County Municipal Boundaries Relate - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(CRAWFORD_COUNTY_MUNI_INTERNAL, CRAWFORD_COUNTY_MUNI_WEB_RELATE, "NO_TEST", 'MUNI_NAME "MUNICIPALITY NAME" true true false 50 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',MUNI_NAME,-1,-1;MUNI_FIPS "MUNICIPALITY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',MUNI_FIPS,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE DATE" true true false 8 Date 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',UPDATE_DATE,-1,-1;MAILING_STREET_ADDRESS "Mailing Street Address" true true false 50 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',MAILING_STREET_ADDRESS,-1,-1;MAILING_CITY_ADDRESS "Mailing Address City" true true false 255 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',MAILING_CITY_ADDRESS,-1,-1;MAILING_ZIP_ADDRESS "Mailing Address Zipcode" true true false 255 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',MAILING_ZIP_ADDRESS,-1,-1;PHYSICAL_STREET_ADDRESS "Physical Street Address" true true false 255 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',PHYSICAL_STREET_ADDRESS,-1,-1;PHYSICAL_CITY_ADDRESS "Physical Address City" true true false 255 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',PHYSICAL_CITY_ADDRESS,-1,-1;PHYSICAL_ZIP_ADDRESS "Physical Address Zipcode" true true false 8 Double 8 38 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',PHYSICAL_ZIP_ADDRESS,-1,-1;EMAIL_ADDRESS "Email Address" true true false 100 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',EMAIL_ADDRESS,-1,-1;WEBSITE "Website" true true false 150 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',WEBSITE,-1,-1;OFFICE_HOURS "Office Hours" true true false 75 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',OFFICE_HOURS,-1,-1;OFFICE_PHONE "Office Phone #" true true false 60 Text 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',OFFICE_PHONE,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',GlobalID,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#,'+CRAWFORD_COUNTY_MUNI_INTERNAL+',SHAPE.STArea(),-1,-1;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\public_web@ccsde.sde\\CCSDE.PUBLIC_WEB.Boundaries\\CCSDE.PUBLIC_WEB.CRAWFORD_MUNICIPAL_BOUNDARIES_WEB,SHAPE.STLength(),-1,-1', "")
    CCMuniBoundRelate_Web_result = arcpy.GetCount_management(CRAWFORD_COUNTY_MUNI_WEB_RELATE)
    print (('{} has {} records'.format(CRAWFORD_COUNTY_MUNI_WEB_RELATE, CCMuniBoundRelate_Web_result[0])))
except:
    print ("\n Unable to append Crawford County Municipal Boundaries Relate - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Crawford County Municipal Boundaries Relate - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Crawford County Municipal Boundaries Relate - PUBLIC_WEB from CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Crawford County Municipal Boundaries Relate - PUBLIC_WEB from CRAW_INTERNAL completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Crawford County Municipal Boundaries Relate - PUBLIC_WEB from CRAW_INTERNAL completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Address Points FC - PUBLIC_WEB from Address Points Web Relate FC - PUBLIC_WEB")
write_log("\n Updating Address Points FC - PUBLIC_WEB from Address Points Web Relate FC - PUBLIC_WEB", logfile)

try:
    # Delete rows from Address Points Web Relate FC - PUBLIC_WEB
    arcpy.DeleteRows_management(ADDRESS_POINTS_WEB_RELATE)
except:
    print ("\n Unable to delete rows from Address Points Web Relate FC - PUBLIC_WEB")
    write_log("Unable to delete rows from Address Points Web Relate FC - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Address Points Web Relate FC - PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:    
    # Append Address Points FC - PUBLIC_WEB from Address Points Web Relate FC - PUBLIC_WEB
    arcpy.management.Append(ADDRESS_POINTS_WEB, ADDRESS_POINTS_WEB_RELATE, "NO_TEST", r'AD_STRU_NUM "UNIQUE STRUCTURE NUMBER" true true false 8 Double 8 38,First,#,'+ADDRESS_POINTS_WEB+',UniqueStructureNumber,-1,-1;AD_ADD_DATE "ADD DATE" true true false 8 Date 0 0,First,#,'+ADDRESS_POINTS_WEB+',Effective,-1,-1;AD_HSENUMBER "HOUSE NUMBER" true true false 8 Double 8 38,First,#,'+ADDRESS_POINTS_WEB+',Add_Number,-1,-1;AD_ADD_EXT "ADDRESS EXT" true true false 5 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',Unit,0,75;AD_ADD_SUF "ADDRESS SUFFIX" true true false 10 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',AddNum_Suf,0,15;AD_PRE_MOD "PREFIX MODIFIER" true true false 15 Text 0 0,First,#;AD_PRE_DIR "PREFIX DIRECTIONAL" true true false 4 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',St_PreDir,0,9;AD_STREETNAME "STREET NAME" true true false 50 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',St_Name,0,60;AD_STREET_SUF "STREET SUFFIX" true true false 5 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',St_PosTyp,0,50;AD_POST_DIR "POST DIRECTIONAL" true true false 4 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',St_PosDir,0,9;AD_POST_MOD "POST MODIFIER" true true false 100 Text 0 0,First,#;AD_STREET "STREET FULL NAME" true true false 50 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',St_FullName,0,160;AD_MUNI "MUNICIPALITY" true true false 50 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',Inc_Muni,0,100;AD_ST_MUNI "STREET | MUNICIPALITY" true true false 80 Text 0 0,First,#;AD_HSE_STREET "911 ADDRESS" true true false 120 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',FullAddress,0,200;AD_LAST_NAME "LAST NAME" true true false 80 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',LastName,0,150;AD_FIRST_NAME "FIRST NAME" true true false 60 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',FirstName,0,150;AD_RR_TYPE "RURAL ROUTE TYPE" true true false 2 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',Old_RRType,0,2;AD_RR_NUM "RURAL ROUTE #" true true false 5 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',Old_RRNumber,0,5;AD_RR_BOX "RURAL ROUTE BOX" true true false 7 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',Old_RRBox,0,7;AD_PO_BOX "PO BOX" true true false 7 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',Post_Box,0,7;AD_POST_OFFICE "POST OFFICE" true true false 22 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',Post_Comm,0,40;AD_STATE "STATE" true true false 2 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',State,0,2;AD_ZIPCODE "ZIPCODE" true true false 8 Double 8 38,First,#,'+ADDRESS_POINTS_WEB+',Post_Code,0,255;AD_TYPE "ADDRESS TYPE" true true false 8 Double 8 38,First,#,'+ADDRESS_POINTS_WEB+',AddrType,-1,-1;AD_OLD_ADD "OLD ADDRESS" true true false 120 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',Old_Address,0,160;AD_PUB_EXEMPT "PUBLIC WEB EXEMPT" true true false 1 Text 0 0,First,#;AD_COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0,First,#,'+ADDRESS_POINTS_WEB+',CountyName,0,50;AD_COUNTY_FIPS "COUNTY FIPS" true true false 8 Double 8 38,First,#,'+ADDRESS_POINTS_WEB+',CountyFIPS,-1,-1;AD_UPD_CODE "UPDATE CODE" true true false 8 Double 8 38,First,#,'+ADDRESS_POINTS_WEB+',UpdateCode,-1,-1;AD_EDIT_DATE "EDIT DATE" true true false 8 Date 0 0,First,#,'+ADDRESS_POINTS_WEB+',DateUpdate,-1,-1;AD_ESN "ESN" true true false 2 Short 0 5,First,#,'+ADDRESS_POINTS_WEB+',ESN,-1,-1;AD_TEMP_ADDR_EXPIRATION "TEMP ADDRESS EXPIRATION" true true false 8 Date 0 0,First,#,'+ADDRESS_POINTS_WEB+',Expire,-1,-1;GlobalID "GlobalID" false false true 38 GlobalID 0 0,First,#,'+ADDRESS_POINTS_WEB+',GlobalID,-1,-1', '', '')
    AddressPoint_WebRelate_result = arcpy.GetCount_management(ADDRESS_POINTS_WEB_RELATE)
    print (('{} has {} records'.format(ADDRESS_POINTS_WEB_RELATE, AddressPoint_WebRelate_result[0])))
    write_log('{} has {} records'.format(ADDRESS_POINTS_WEB_RELATE, AddressPoint_WebRelate_result[0]), logfile)
except:
    print ("\n Unable to append Address Points FC - PUBLIC_WEB from Address Points Web Relate FC - PUBLIC_WEB")
    write_log("Unable to append Address Points FC - PUBLIC_WEB from Address Points Web Relate FC - PUBLIC_WEB", logfile)
    logging.exception('Got exception on append Address Points FC - PUBLIC_WEB from Address Points Web Relate FC - PUBLIC_WEB logged at: ' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Address Points FC - PUBLIC_WEB from Address Points Web Relate FC - PUBLIC_WEB completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Address Points FC - PUBLIC_WEB from Address Points Web Relate FC - PUBLIC_WEB completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("===========================================================")
print (("       ALL BOUNDARY UPDATES HAVE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("       ALL BOUNDARY UPDATES HAVE COMPLETED: " + str(Day) + " " + str(end_time), logfile)
write_log("===========================================================",logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)

write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
