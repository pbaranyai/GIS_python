# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NortherTierCAD_DataExport_Process - Step 1.py
#  
# Description: 
# This tool will create a FGDB (Northern_Tier_County_Data_YYYYMMDD.gdb), then process local Crawford County Data into the schema required for
# the usage of the Northern Tier CAD.  
#
# After this tool is completed, you must connect to the Elk Co. VPN to run the next step
#
# STEP 1 of 2
# Author: Phil Baranyai/Crawford County GIS Manager
# Created: 2/28/2019
# Last Edited: 06/1/2021 - Updated with missing NG911 fields for multiple datasets.
# ---------------------------------------------------------------------------

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
logfile = r"R:\\GIS\\GIS_LOGS\\911\\NorthernTierCAD_DataExport.log"  # Run Log
logging.basicConfig(filename=logfile, filemode='w', level=logging.DEBUG)

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())

try:
    # Write Logfile (define logfile write process, each step will append to the log)
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
    write_log("No ArcEditor (ArcStandard) license available", logfile)
    logging.exception('Got exception on importing ArcEditor (ArcStandard) license logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()

# Define Work Paths for FGDB:
NORTHERN_TIER_CAD_FLDR = "R:\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier"
NORTHERN_TIER_COUNTY_DATA_XML = "R:\\GIS\\NorthernTierCAD_GIS\\XML_Workspace\\NORTHERN_TIER_COUNTY_DATA.XML"
NORTHERN_TIER_CAD_FGDB_OLD = "R:\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier\\Northern_Tier_County_Data_YYYYMMDD.gdb"

start_time = time.time()

print ("=====================================================================================================================")
print ("Checking for existing NorthernTier FGDB, delete and rebuild fresh if exists.")
print ("=====================================================================================================================")
write_log("\n Checking for existing NorthernTier FGDB, delete and rebuild fresh if exists.", logfile)

try:
    # Pre-clean old FGDB, if exists (if old Northern_Tier_County_Data_YYYYMMDD.gdb exists and was never renamed, the program will delete it, so it will be able to run without failure, henceforth providing the newest data)
    if arcpy.Exists(NORTHERN_TIER_CAD_FGDB_OLD):
        arcpy.Delete_management(NORTHERN_TIER_CAD_FGDB_OLD, "Workspace")
        print ("Northern_Tier_County_Data_YYYYMMDD.gdb found - FGDB deleted")
        write_log("Northern_Tier_County_Data_YYYYMMDD.gdb found - FGDB deleted", logfile)
except:
    print ("\n Unable to delete Northern_Tier_County_Data_YYYYMMDD.gdb, need to delete existing FGDB manually and/or close program locking the FGDB")
    write_log("Unable to create new Northern_Tier_County_Data_YYYYMMDD , need to delete existing FGDB manually and/or close program locking the FGDB", logfile)
    logging.exception('Got exception on delete Northern_Tier_County_Data_YYYYMMDD.gdb logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("Creating fresh version of Northern_Tier_County_Data_YYYYMMDD FGDB")
write_log("Creating fresh version of Northern_Tier_County_Data_YYYYMMDD FGDB", logfile)

try:
    # Create new File GDB called Northern_Tier_County_Data_YYYYMMDD.gdb (creates new FGDB each time to avoid corruption)
    arcpy.CreateFileGDB_management(NORTHERN_TIER_CAD_FLDR, "Northern_Tier_County_Data_YYYYMMDD", "CURRENT")
except:
    print ("\n Unable to create new Northern_Tier_County_Data_YYYYMMDD.gdb, need to close program locking the FGDB workspace")
    write_log("Unable to create new Northern_Tier_County_Data_YYYYMMDD.gdb, need to close program locking the FGDB workspace", logfile)
    logging.exception('Got exception on create Northern_Tier_County_Data_' + date + '.gdb logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

# Define Work Paths for Databases:
NORTHERN_TIER_CAD_FLDR = r"R:\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier"
NORTHERN_TIER_CAD_FGDB = NORTHERN_TIER_CAD_FLDR + "\\Northern_Tier_County_Data_YYYYMMDD.gdb"
NORTHERN_TIER_CAD_FGDB_CC = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County"
DELETE_FILES = NORTHERN_TIER_CAD_FGDB + "\\DELETE_FILES"
PUBLIC_SAFETY_DB = "Database Connections\\PUBLIC_SAFETY@ccsde.sde"

print ("Importing XML workspace to Northern Tier FGDB for schema structure")
write_log("Importing XML workspace to Northern Tier FGDB for schema structure", logfile)

try:
    # Import XML Workspace for NT FGDB Schema (if the Northern Tier GIS sub-committee agrees to more changes, this XML will need to be updated)
    arcpy.ImportXMLWorkspaceDocument_management(NORTHERN_TIER_CAD_FGDB, NORTHERN_TIER_COUNTY_DATA_XML, "SCHEMA_ONLY", "")
    print "Northern_Tier_County_Data_YYYYMMDD FGDB schema import completed"
except:
    print ("\n Unable to import XML workspace file")
    write_log("Unable to import XML workspace file", logfile)
    logging.exception('Got exception on import XML workspace file')
    raise
    sys.exit ()

# Local variables:
ADDRESS_POINTS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ADDRESS_POINTS_INTERNAL"
ALS_ZONES_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL"
BLS_COVERAGE_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.BLS_COVERAGE_INTERNAL"
COUNTY_ADJ_MUNI_BOUND_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL"
FIRE_DEPT_COVERAGE_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.FIRE_DEPT_COVERAGE_INTERNAL"
FIRE_GRIDS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.FIRE_GRIDS_INTERNAL"
HYDRANTS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS"
LANDMARKS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.LANDMARKS_INTERNAL"
MILE_MARKERS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL"
POLICE_DEPT_COVERAGE_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL"
RAILROADS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL"
STREET_CENTERLINE_PS = PUBLIC_SAFETY_DB + "\\CCSDE.PUBLIC_SAFETY.STREET_CENTERLINE"
STREET_CENTERLINE = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.STREET_CENTERLINE_INTERNAL"
TAX_PARCELS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.TAX_PARCELS_INTERNAL"
ZIPCODES_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL"
NORTHERN_TIER_COUNTY_DATA_XML = "R:\\GIS\\NorthernTierCAD_GIS\\XML_Workspace\\NORTHERN_TIER_COUNTY_DATA.XML"

#Layer Files
COUNTY_ADJ_MUNI_LAYER = "COUNTY_ADJ_MUNI_LAYER"
FIRE_DEPT_COVERAGE_INTERNAL_LYR = "FIRE_DEPT_COVERAGE_INTERNAL_LYR"
STREET_CENTERLINE_Layer = "CL_Zipcode_JOIN_DELETE_Layer"

#Temporary variables
ALS_JOIN_DELETE_Intersect_DELETE = DELETE_FILES + "\\ALS_JOIN_DELETE_Intersect_DELETE"
BLS_ALS_INTERSECT_Spatial_Join = DELETE_FILES + "\\BLS_ALS_INTERSECT_Spatial_Join"
BLS_COVERAGE_DELETE = DELETE_FILES + "\\BLS_COVERAGE_DELETE"
CL_Zipcode_JOIN_DELETE = DELETE_FILES + "\\CL_Zipcode_JOIN_DELETE"
MUNI_DISSOLVE = DELETE_FILES + "\\MUNI_DISSOLVE"
FIRE_GRIDS_JOIN_DELETE = DELETE_FILES + "\\FIRE_GRIDS_JOIN_DELETE"
POLICE_DEPT_COVERAGE_DELETE = DELETE_FILES + "\\POLICE_DEPT_COVERAGE_DELETE"
POLICE_REPORT_JOIN_DELETE = DELETE_FILES + "\\POLICE_REPORT_JOIN_DELETE"
FIRE_DEPT_COVERAGE_DELETE = DELETE_FILES + "\\FIRE_DEPT_COVERAGE_DELETE"
POLICE_DEPT_COVERAGE_DELETE_DISSOLVE = DELETE_FILES + "\\POLICE_DEPT_COVERAGE_DELETE_DISSOLVE"
POLICE_RESPONSE_DISSOLVE = DELETE_FILES + "\\POLICE_RESPONSE_DISSOLVE"
STREET_CENTERLINE_Layer_OUTPUT = DELETE_FILES + "\\STREET_CENTERLINE_Layer_OUTPUT"

#Staging variables
Ambulance_Company_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Ambulance_Company_CrawfordCo"
Centerline_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Centerline_CrawfordCo"
Counties_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Counties_CrawfordCo"
EMS_Districts_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\EMS_Districts_CrawfordCo"
Fire_Department_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Fire_Department_CrawfordCo"
Fire_Response_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Fire_Response_CrawfordCo"
Hydrants_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\NWS_Hydrants_CrawfordCo"
Landmarks_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Landmarks_CrawfordCo"
MilePosts_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\MilePosts_CrawfordCo"
Municipalities_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Municipalities_CrawfordCo"
NTAddressPoint_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\AddressPoint_CrawfordCo"
Parcels_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Parcels_CrawfordCo"
Police_Department_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Police_Department_CrawfordCo"
Police_Reporting_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Police_Reporting_CrawfordCo"
Police_Response_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Police_Response_CrawfordCo"
Railroads_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Railroads_CrawfordCo"

print ("\n")
print (" ===============================================================================================================")
print (" ===============================================================================================================")
print (" Begining Crawford County to Northern Tier CAD data conversion: " + str(Day) + " " + str(Time))
print (" ===============================================================================================================")
print (" ===============================================================================================================")
write_log("\n Begining Crawford County to Northern Tier CAD data conversion: " + str(Day) + " " + str(Time), logfile)

print ("\n Appending Address Points from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Appending Address Points from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append_AddressPoint_CrawfordCo (append Crawford Address points to staging FGDB created in steps above)
    arcpy.Append_management(ADDRESS_POINTS_INTERNAL, NTAddressPoint_CrawfordCo, "NO_TEST", 'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_DiscrpAgID,-1,-1;DateUpdate "DateUpdate" true true false 8 Date 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_EDIT_DATE,-1,-1;Effective "Effective" true true false 8 Date 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_ADD_DATE,-1,-1;Expire "Expire" true true false 8 Date 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_TEMP_ADDR_EXPIRATION,-1,-1;Site_NGUID "Site_NGUID" true true false 254 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_CAD_NGUID,-1,-1;Country "Country" true true false 2 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_COUNTRY,-1,-1;State "State" true true false 2 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_STATE,-1,-1;County "County" true true false 40 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_COUNTY_NAME,-1,-1;AddCode "AddCode" true true false 506 Text 0 0 ,First,#;AddDataURI "AddDataURI" true true false 254 Text 0 0 ,First,#;Inc_Muni "Inc_Muni" true true false 100 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_MUNI,-1,-1;Uninc_Comm "Uninc_Comm" true true false 100 Text 0 0 ,First,#;Nbrhd_Comm "Nbrhd_Comm" true true false 100 Text 0 0 ,First,#;AddNum_Pre "AddNum_Pre" true true false 50 Text 0 0 ,First,#;Add_Number "Add_Number" true true false 4 Long 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_HSENUMBER,-1,-1;AddNum_Suf "AddNum_Suf" true true false 15 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_ADD_SUF,-1,-1;St_PreMod "St_PreMod" true true false 15 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_POST_MOD,-1,-1;St_PreDir "ST_PreDir" true true false 9 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_PRE_DIR,-1,-1;St_PreTyp "St_PreTyp" true true false 50 Text 0 0 ,First,#;St_PreSep "St_PreSep" true true false 20 Text 0 0 ,First,#;St_Name "St_Name" true true false 60 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_STREETNAME,-1,-1;St_PosTyp "St_PosTyp" true true false 50 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_STREET_SUF,-1,-1;St_PosDir "St_PosDir" true true false 9 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_POST_DIR,-1,-1;St_PosMod "St_PosMod" true true false 25 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_POST_MOD,-1,-1;LSt_PreDir "LSt_PreDir" true true false 2 Text 0 0 ,First,#;LSt_Name "LSt_Name" true true false 75 Text 0 0 ,First,#;LSt_Type "LSt_Type" true true false 4 Text 0 0 ,First,#;LStPosDir "LStPosDir" true true false 2 Text 0 0 ,First,#;ESN "ESN" true true false 5 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_ESN,-1,-1;MSAGComm "MSAGComm" true true false 30 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_MUNI,-1,-1;Post_Comm "Post_Comm" true true false 40 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_POST_OFFICE,-1,-1;Post_Code "Post_Code" true true false 7 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_ZIPCODE,-1,-1;Post_Code4 "Post_Code4" true true false 4 Text 0 0 ,First,#;Building "Building" true true false 75 Text 0 0 ,First,#;Floor "Floor" true true false 75 Text 0 0 ,First,#;Unit "Unit" true true false 75 Text 0 0 ,First,#;Room "Room" true true false 75 Text 0 0 ,First,#;Seat "Seat" true true false 75 Text 0 0 ,First,#;Addtl_Loc "Addtl_Loc" true true false 225 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_ADD_EXT,-1,-1;LandmkName "LandmkName" true true false 150 Text 0 0 ,First,#;Mile_Post "Mile_Post" true true false 150 Text 0 0 ,First,#;Place_Type "Place_Type" true true false 50 Text 0 0 ,First,#;Placement "Placement" true true false 25 Text 0 0 ,First,#;Long "Long" true true false 8 Double 0 0 ,First,#;Lat "Lat" true true false 8 Double 0 0 ,First,#;Elev "Elev" true true false 4 Long 0 0 ,First,#;JOIN_ID "JOIN_ID" true true false 4 Long 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_STRU_NUM,-1,-1;FullName "FullName" true true false 80 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_HSE_STREET,-1,-1', "")
    address_result = arcpy.GetCount_management(NTAddressPoint_CrawfordCo)
    print ('{} has {} records'.format(NTAddressPoint_CrawfordCo, address_result[0]))
    write_log('{} has {} records'.format(NTAddressPoint_CrawfordCo, address_result[0]), logfile)
except:
    print ("\n Unable to append Address Points from CRAW_INTERNAL to Northern Tier FGDB")
    write_log("Unable to append Address Points from CRAW_INTERNAL to Northern Tier FGDB", logfile)
    logging.exception('Got exception on append Address Points from CRAW_INTERNAL to Northern Tier FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("       Address Point append completed")
write_log("       Address Point append completed", logfile)

print ("\n Processing BLS Coverage from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Processing BLS Coverage from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Export BLS_COVERAGE_INTERNAL to BLS_COVERAGE_DELETE (export BLS coverage to temp file for further manipulation in steps below, excluding out departments based in other Northern Tier counties)
    arcpy.FeatureClassToFeatureClass_conversion(BLS_COVERAGE_INTERNAL, DELETE_FILES, "BLS_COVERAGE_DELETE", "EMS_NUM NOT IN ( '37', '38')", 'EMS_DEPT "BLS/EMS DEPARTMENT" true true false 50 Text 0 0 ,First,#,'+BLS_COVERAGE_INTERNAL+',EMS_DEPT,-1,-1;EMS_NUM "BLS/EMS DEPARTMENT #" true true false 10 Text 0 0 ,First,#,'+BLS_COVERAGE_INTERNAL+',EMS_NUM,-1,-1;EMS_EMSID "EMS ID CODE" true true false 10 Text 0 0 ,First,#,'+BLS_COVERAGE_INTERNAL+',EMS_EMSID,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+BLS_COVERAGE_INTERNAL+',COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+BLS_COVERAGE_INTERNAL+',COUNTY_FIPS,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,'+BLS_COVERAGE_INTERNAL+',GLOBALID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+BLS_COVERAGE_INTERNAL+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+BLS_COVERAGE_INTERNAL+',STATE,-1,-1;SHAPE_STArea__ "SHAPE_STArea__" false false true 0 Double 0 0 ,First,#,'+BLS_COVERAGE_INTERNAL+',SHAPE.STArea(),-1,-1;SHAPE_STLength__ "SHAPE_STLength__" false false true 0 Double 0 0 ,First,#,'+BLS_COVERAGE_INTERNAL+',SHAPE.STLength(),-1,-1', "")
except:
    print ("\n Unable to Export BLS_COVERAGE_INTERNAL to BLS_COVERAGE_DELETE")
    write_log("Unable to Export BLS_COVERAGE_INTERNAL to BLS_COVERAGE_DELETE", logfile)
    logging.exception('Got exception on Export BLS_COVERAGE_INTERNAL to BLS_COVERAGE_DELETE logged at: ' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try: 
    # Add ID Field to BLS_COVERAGE_DELETE
    arcpy.AddField_management(BLS_COVERAGE_DELETE, "ID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print ("\n Unable to Add ID Field to BLS_COVERAGE_DELETE")
    write_log("Unable to Add ID Field to BLS_COVERAGE_DELETE", logfile)
    logging.exception('Got exception on Add ID Field to BLS_COVERAGE_DELETE logged at: ' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Calculate ID Field in BLS_COVERAGE_DELETE (ID field is required by CAD, adds county code - 20 to the EMS department number)
    arcpy.CalculateField_management(BLS_COVERAGE_DELETE, "ID", '"20"+""+ !EMS_EMSID!', "PYTHON", "")
except:
    print ("\n Unable to Calculate ID Field in BLS_COVERAGE_DELETE")
    write_log("Unable to Calculate ID Field in BLS_COVERAGE_DELETE", logfile)
    logging.exception('Got exception on Calculate ID Field in BLS_COVERAGE_DELETE logged at: ' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Append BLS_COVERAGE_DELETE to Ambulance_Company in Northern Tier FGDB (append Crawford BLS polygons to staging FGDB created in steps above)
    arcpy.Append_management(BLS_COVERAGE_DELETE, Ambulance_Company_CrawfordCo, "NO_TEST", 'Description "Description" true true false 50 Text 0 0 ,First,#,'+BLS_COVERAGE_DELETE+',EMS_DEPT,-1,-1;ID "ID" true true false 4 Long 0 0 ,First,#,'+BLS_COVERAGE_DELETE+',ID,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,'+BLS_COVERAGE_DELETE+',Shape_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,'+BLS_COVERAGE_DELETE+',Shape_Area,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+BLS_COVERAGE_DELETE+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+BLS_COVERAGE_DELETE+',STATE,-1,-1', "")
    Ambulance_Company_result = arcpy.GetCount_management(Ambulance_Company_CrawfordCo)
    print ('{} has {} records'.format(Ambulance_Company_CrawfordCo, Ambulance_Company_result[0]))
    write_log('{} has {} records'.format(Ambulance_Company_CrawfordCo, Ambulance_Company_result[0]), logfile)
    
except:
    print ("\n Unable to Append BLS_COVERAGE_DELETE to Ambulance_Company in Northern Tier FGDB")
    write_log("Unable to Append BLS_COVERAGE_DELETE to Ambulance_Company in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append BLS_COVERAGE_DELETE to Ambulance_Company in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       BLS Coverage to Ambulance Company append completed")
write_log("       BLS Coverage to Ambulance Company append completed", logfile)

print ("\n Processing Street Centerline from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Processing Street Centerline from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try: 
    # Spatial Join CL and Zipcode - creating CL_Zipcode_JOIN_DELETE (join centerline and zipcode as CAD needs the zipcode of centerlines and it's not carried at the county level)
    arcpy.SpatialJoin_analysis(STREET_CENTERLINE_PS, ZIPCODES_INTERNAL, CL_Zipcode_JOIN_DELETE, "JOIN_ONE_TO_ONE", "KEEP_ALL", 'CL_UNIQUEID "UNIQUE ID" true true false 4 Long 0 10 ,First,#,'+STREET_CENTERLINE_PS+',CL_UNIQUEID,-1,-1;CL_PRE_MOD "PRE MODIFIER" true true false 15 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_PRE_MOD,-1,-1;CL_PRE_DIR "PRE DIRECTIONAL" true true false 4 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_PRE_DIR,-1,-1;CL_PRE_TYPE "PRE TYPE" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_PRE_TYPE,-1,-1;CL_NAME "NAME" true true false 75 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_NAME,-1,-1;CL_SUFFIX "SUFFIX" true true false 6 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_SUFFIX,-1,-1;CL_POST_DIR "POST DIRECTIONAL" true true false 4 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_POST_DIR,-1,-1;CL_POST_MOD "POST MODIFIER" true true false 100 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_POST_MOD,-1,-1;CL_FULL_NAME "FULL NAME" true true false 100 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_FULL_NAME,-1,-1;CL_MUNI "MUNICIPALITY" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_MUNI,-1,-1;CL_MUNI_L "MUNICIPALITY LEFT" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_MUNI_L,-1,-1;CL_MUNI_R "MUNICIPALITY RIGHT" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_MUNI_R,-1,-1;CL_STATE_L "STATE LEFT" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_STATE_L,-1,-1;CL_STATE_R "STATE RIGHT" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_STATE_R,-1,-1;CL_FIPS_L "FIPS LEFT" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_FIPS_L,-1,-1;CL_FIPS_R "FIPS RIGHT" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_FIPS_R,-1,-1;CL_RTNO "ROUTE NUMBER" true true false 4 Long 0 10 ,First,#,'+STREET_CENTERLINE_PS+',CL_RTNO,-1,-1;CL_ST_MUNI "STREET | MUNI" true true false 120 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_ST_MUNI,-1,-1;CL_ESN_L "ESN L" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_ESN_L,-1,-1;CL_ESN_R "ESN R" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_ESN_R,-1,-1;CL_L_LO "LEFT LOW #" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_L_LO,-1,-1;CL_L_HI "LEFT HIGH #" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_L_HI,-1,-1;CL_R_LO "RIGHT LOW #" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_R_LO,-1,-1;CL_R_HI "RIGHT HIGH #" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_R_HI,-1,-1;CL_RANGE "ADDRESS RANGE" true true false 13 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_RANGE,-1,-1;CL_TILE "TILE #" true true false 6 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_TILE,-1,-1;CL_ONE_WAY "ONE WAY" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_ONE_WAY,-1,-1;CL_Z_ELEV_F "Z ELEVATION FROM" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_Z_ELEV_F,-1,-1;CL_Z_ELEV_T "Z ELEVATION TO" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_Z_ELEV_T,-1,-1;CL_CONST_STATUS "CONSTRUCTION STATUS" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_CONST_STATUS,-1,-1;CL_OWNER "OWNER" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_OWNER,-1,-1;CL_SURF_TYPE "SURFACE TYPE" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_SURF_TYPE,-1,-1;CL_WEIGHT_LMT "WEIGHT LIMIT" true true false 2 Short 0 5 ,First,#,'+STREET_CENTERLINE_PS+',CL_WEIGHT_LMT,-1,-1;CL_HEIGHT_LMT "HEIGHT LIMIT" true true false 2 Short 0 5 ,First,#,'+STREET_CENTERLINE_PS+',CL_HEIGHT_LMT,-1,-1;CL_SPEED_LMT "SPEED LIMIT" true true false 2 Short 0 5 ,First,#,'+STREET_CENTERLINE_PS+',CL_SPEED_LMT,-1,-1;CL_FT_COST "FROM-TO COST" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_FT_COST,-1,-1;CL_TF_COST "TO_FROM COST" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_TF_COST,-1,-1;CL_DIVIDED "ROADWAY DIVIDED" true true false 1 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_DIVIDED,-1,-1;CL_IN_WATER "IN WATER" true true false 1 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_IN_WATER,-1,-1;CL_IN_COUNTY "IN COUNTY" true true false 1 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_IN_COUNTY,-1,-1;CL_CFCC "CFCC" true true false 6 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_CFCC,-1,-1;CL_MTFCC "MTFCC" true true false 6 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_MTFCC,-1,-1;CL_RD_CLASS "ROAD CLASS" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_RD_CLASS,-1,-1;CL_P_LL "PARITY LEFT LOW #" true true false 1 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_P_LL,-1,-1;CL_P_LH "PARITY LEFT HIGH #" true true false 1 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_P_LH,-1,-1;CL_P_RL "PARITY RIGHT LOW #" true true false 1 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_P_RL,-1,-1;CL_P_RH "PARITY RIGHT HIGH #" true true false 1 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_P_RH,-1,-1;CL_P_ALL "PARITY ALL" true true false 4 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_P_ALL,-1,-1;CL_LO_CROSS "LOW CROSS STREET" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_LO_CROSS,-1,-1;CL_HI_CROSS "HIGH CROSS STREET" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_HI_CROSS,-1,-1;CL_UPD_CODE "UPDATE CODE" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_UPD_CODE,-1,-1;CL_ADD_DATE "ADD DATE" false true false 8 Date 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_ADD_DATE,-1,-1;CL_UPD_DATE "UPDATE DATE" false true false 8 Date 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_UPD_DATE,-1,-1;CL_UPD_USER "UPDATE USER" false true false 100 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_UPD_USER,-1,-1;CL_COUNTY_NAME_L "COUNTY NAME LEFT" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_COUNTY_NAME_L,-1,-1;CL_COUNTY_NAME_R "COUNTY NAME RIGHT" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_COUNTY_NAME_R,-1,-1;CL_COUNTY_FIPS_L "COUNTY FIPS LEFT" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_COUNTY_FIPS_L,-1,-1;CL_COUNTY_FIPS_R "COUNTY FIPS RIGHT" true true false 8 Double 8 38 ,First,#,'+STREET_CENTERLINE_PS+',CL_COUNTY_FIPS_R,-1,-1;CL_CAD_NTID "CAD NTID" true true false 254 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_CAD_NTID,-1,-1;CL_ADDRESS_COUNT "ADDRESS COUNT" true true false 4 Long 0 10 ,First,#,'+STREET_CENTERLINE_PS+',CL_ADDRESS_COUNT,-1,-1;CL_DiscrpAGID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_DiscrpAGID,-1,-1;CL_COUNTRY_L "Country Left" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_COUNTRY_L,-1,-1;CL_COUNTRY_R "Country Right" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_PS+',CL_COUNTRY_R,-1,-1;SHAPE_STLength__ "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,'+STREET_CENTERLINE_PS+',SHAPE.STLength(),-1,-1;POST_OFFICE "POST OFFICE" true true false 50 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,POST_OFFICE,-1,-1;ZIPCODE "ZIPCODE" true true false 8 Double 8 38 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,ZIPCODE,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,UPDATE_DATE,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,GLOBALID,-1,-1;SHAPE_STArea__ "SHAPE_STArea__" false false true 0 Double 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE_STLength_1 "SHAPE_STLength_1" false false true 0 Double 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,SHAPE.STLength(),-1,-1', "HAVE_THEIR_CENTER_IN", "", "")
except:
    print ("\n Unable to Spatial Join CL and Zipcode - creating CL_Zipcode_JOIN_DELETE")
    write_log("Unable to Spatial Join CL and Zipcode - creating CL_Zipcode_JOIN_DELETE", logfile)
    logging.exception('Got exception on Spatial Join CL and Zipcode - creating CL_Zipcode_JOIN_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Make Feature Layer -- STREET_CENTERLINE_Layer (make a temporary layer of centerline, to manipulate in steps below)
    arcpy.MakeFeatureLayer_management(CL_Zipcode_JOIN_DELETE, STREET_CENTERLINE_Layer, "CL_CONST_STATUS <> 1 OR CL_CONST_STATUS IS NULL", "", "OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;Join_Count Join_Count VISIBLE NONE;TARGET_FID TARGET_FID VISIBLE NONE;CL_UNIQUEID CL_UNIQUEID VISIBLE NONE;CL_PRE_MOD CL_PRE_MOD VISIBLE NONE;CL_PRE_DIR CL_PRE_DIR VISIBLE NONE;CL_PRE_TYPE CL_PRE_TYPE VISIBLE NONE;CL_NAME CL_NAME VISIBLE NONE;CL_SUFFIX CL_SUFFIX VISIBLE NONE;CL_POST_DIR CL_POST_DIR VISIBLE NONE;CL_POST_MOD CL_POST_MOD VISIBLE NONE;CL_FULL_NAME CL_FULL_NAME VISIBLE NONE;CL_MUNI CL_MUNI VISIBLE NONE;CL_MUNI_L CL_MUNI_L VISIBLE NONE;CL_MUNI_R CL_MUNI_R VISIBLE NONE;CL_STATE_L CL_STATE_L VISIBLE NONE;CL_STATE_R CL_STATE_R VISIBLE NONE;CL_FIPS_L CL_FIPS_L VISIBLE NONE;CL_FIPS_R CL_FIPS_R VISIBLE NONE;CL_RTNO CL_RTNO VISIBLE NONE;CL_ST_MUNI CL_ST_MUNI VISIBLE NONE;CL_ESN_L CL_ESN_L VISIBLE NONE;CL_ESN_R CL_ESN_R VISIBLE NONE;CL_L_LO CL_L_LO VISIBLE NONE;CL_L_HI CL_L_HI VISIBLE NONE;CL_R_LO CL_R_LO VISIBLE NONE;CL_R_HI CL_R_HI VISIBLE NONE;CL_RANGE CL_RANGE VISIBLE NONE;CL_TILE CL_TILE VISIBLE NONE;CL_ONE_WAY CL_ONE_WAY VISIBLE NONE;CL_Z_ELEV_F CL_Z_ELEV_F VISIBLE NONE;CL_Z_ELEV_T CL_Z_ELEV_T VISIBLE NONE;CL_CONST_STATUS CL_CONST_STATUS VISIBLE NONE;CL_OWNER CL_OWNER VISIBLE NONE;CL_SURF_TYPE CL_SURF_TYPE VISIBLE NONE;CL_WEIGHT_LMT CL_WEIGHT_LMT VISIBLE NONE;CL_HEIGHT_LMT CL_HEIGHT_LMT VISIBLE NONE;CL_SPEED_LMT CL_SPEED_LMT VISIBLE NONE;CL_FT_COST CL_FT_COST VISIBLE NONE;CL_TF_COST CL_TF_COST VISIBLE NONE;CL_DIVIDED CL_DIVIDED VISIBLE NONE;CL_IN_WATER CL_IN_WATER VISIBLE NONE;CL_IN_COUNTY CL_IN_COUNTY VISIBLE NONE;CL_CFCC CL_CFCC VISIBLE NONE;CL_MTFCC CL_MTFCC VISIBLE NONE;CL_RD_CLASS CL_RD_CLASS VISIBLE NONE;CL_P_LL CL_P_LL VISIBLE NONE;CL_P_LH CL_P_LH VISIBLE NONE;CL_P_RL CL_P_RL VISIBLE NONE;CL_P_RH CL_P_RH VISIBLE NONE;CL_P_ALL CL_P_ALL VISIBLE NONE;CL_LO_CROSS CL_LO_CROSS VISIBLE NONE;CL_HI_CROSS CL_HI_CROSS VISIBLE NONE;CL_UPD_CODE CL_UPD_CODE VISIBLE NONE;CL_ADD_DATE CL_ADD_DATE VISIBLE NONE;CL_UPD_DATE CL_UPD_DATE VISIBLE NONE;CL_UPD_USER CL_UPD_USER VISIBLE NONE;CL_COUNTY_NAME_L CL_COUNTY_NAME_L VISIBLE NONE;CL_COUNTY_NAME_R CL_COUNTY_NAME_R VISIBLE NONE;CL_COUNTY_FIPS_L CL_COUNTY_FIPS_L VISIBLE NONE;CL_COUNTY_FIPS_R CL_COUNTY_FIPS_R VISIBLE NONE;CL_CAD_NTID CL_CAD_NTID VISIBLE NONE;CL_ADDRESS_COUNT CL_ADDRESS_COUNT VISIBLE NONE;CL_DiscrpAGID CL_DiscrpAGID VISIBLE NONE;CL_COUNTRY_L CL_COUNTRY_L VISIBLE NONE;CL_COUNTRY_R CL_COUNTRY_R VISIBLE NONE;POST_OFFICE POST_OFFICE VISIBLE NONE;ZIPCODE ZIPCODE VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;UPDATE_DATE UPDATE_DATE VISIBLE NONE;SHAPE_STLength_1 SHAPE_STLength_1 VISIBLE NONE;SHAPE_Length SHAPE_Length VISIBLE NONE")
except:
    print ("\n Unable to Make Feature Layer -- STREET_CENTERLINE_Layer - Calc ALL COSTS to FT COST FIELD")
    write_log("Unable to Make Feature Layer -- STREET_CENTERLINE_Layer - Calc ALL COSTS to FT COST FIELD", logfile)
    logging.exception('Got exception on Make Feature Layer -- STREET_CENTERLINE_Layer - Calc ALL COSTS to FT COST FIELD logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calc ALL COSTS to FT COST FIELD (iterate through centerline layer file, calculate any costs from the TF_COST field over to the FT cost field if the One way is TF, otherwise the correct cost already exists in the FT cost field - which will be calculated in append in steps below)
    CENTERLINE_FIELDS = ['CL_ONE_WAY', 'CL_FT_COST', 'CL_TF_COST']
    cursor = arcpy.da.UpdateCursor(STREET_CENTERLINE_Layer, CENTERLINE_FIELDS)
    for row in cursor:
        if (row[0] == 'B' or row[0] is None or row[0] == 'FT' or row[0] == 'N'):
            pass
        if (row[0] == 'TF'):
            row[1] = row[2]
            cursor.updateRow(row)
    del row 
    del cursor
    print ("   Centerline one-way and routing costs calculated...")
except:
    print ("\n Unable to calculate one-way and routing costs")
    write_log("Unable to calculate one-way and routing costs", logfile)
    logging.exception('Got exception on calculate one-way and routing costs logged at:'  + str(Day) + " " + str(Time))
    raise
    pass
    sys.exit ()

try:
    # Output STREET_CENTERLINE_Layer to DELETE_FILE, to append to Centerline_CrawfordCo - Northern Tier FGDB (append Crawford centerline to staging FGDB created in steps above)
    arcpy.FeatureClassToFeatureClass_conversion(STREET_CENTERLINE_Layer, DELETE_FILES, "STREET_CENTERLINE_Layer_OUTPUT", "", 'Join_Count "Join_Count" true true false 4 Long 0 0 ,First,#,STREET_CENTERLINE_Layer,Join_Count,-1,-1;TARGET_FID "TARGET_FID" true true false 4 Long 0 0 ,First,#,STREET_CENTERLINE_Layer,TARGET_FID,-1,-1;CL_UNIQUEID "UNIQUE ID" true true false 4 Long 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_UNIQUEID,-1,-1;CL_PRE_MOD "PRE MODIFIER" true true false 15 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_PRE_MOD,-1,-1;CL_PRE_DIR "PRE DIRECTIONAL" true true false 4 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_PRE_DIR,-1,-1;CL_PRE_TYPE "PRE TYPE" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_PRE_TYPE,-1,-1;CL_NAME "NAME" true true false 75 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_NAME,-1,-1;CL_SUFFIX "SUFFIX" true true false 6 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_SUFFIX,-1,-1;CL_POST_DIR "POST DIRECTIONAL" true true false 4 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_POST_DIR,-1,-1;CL_POST_MOD "POST MODIFIER" true true false 100 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_POST_MOD,-1,-1;CL_FULL_NAME "FULL NAME" true true false 100 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_FULL_NAME,-1,-1;CL_MUNI "MUNICIPALITY" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_MUNI,-1,-1;CL_MUNI_L "MUNICIPALITY LEFT" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_MUNI_L,-1,-1;CL_MUNI_R "MUNICIPALITY RIGHT" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_MUNI_R,-1,-1;CL_STATE_L "STATE LEFT" true true false 2 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_STATE_L,-1,-1;CL_STATE_R "STATE RIGHT" true true false 2 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_STATE_R,-1,-1;CL_FIPS_L "FIPS LEFT" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_FIPS_L,-1,-1;CL_FIPS_R "FIPS RIGHT" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_FIPS_R,-1,-1;CL_RTNO "ROUTE NUMBER" true true false 4 Long 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_RTNO,-1,-1;CL_ST_MUNI "STREET | MUNI" true true false 120 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_ST_MUNI,-1,-1;CL_ESN_L "ESN L" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_ESN_L,-1,-1;CL_ESN_R "ESN R" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_ESN_R,-1,-1;CL_L_LO "LEFT LOW #" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_L_LO,-1,-1;CL_L_HI "LEFT HIGH #" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_L_HI,-1,-1;CL_R_LO "RIGHT LOW #" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_R_LO,-1,-1;CL_R_HI "RIGHT HIGH #" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_R_HI,-1,-1;CL_RANGE "ADDRESS RANGE" true true false 13 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_RANGE,-1,-1;CL_TILE "TILE #" true true false 6 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_TILE,-1,-1;CL_ONE_WAY "ONE WAY" true true false 2 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_ONE_WAY,-1,-1;CL_Z_ELEV_F "Z ELEVATION FROM" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_Z_ELEV_F,-1,-1;CL_Z_ELEV_T "Z ELEVATION TO" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_Z_ELEV_T,-1,-1;CL_CONST_STATUS "CONSTRUCTION STATUS" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_CONST_STATUS,-1,-1;CL_OWNER "OWNER" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_OWNER,-1,-1;CL_SURF_TYPE "SURFACE TYPE" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_SURF_TYPE,-1,-1;CL_WEIGHT_LMT "WEIGHT LIMIT" true true false 2 Short 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_WEIGHT_LMT,-1,-1;CL_HEIGHT_LMT "HEIGHT LIMIT" true true false 2 Short 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_HEIGHT_LMT,-1,-1;CL_SPEED_LMT "SPEED LIMIT" true true false 2 Short 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_SPEED_LMT,-1,-1;CL_FT_COST "FROM-TO COST" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_FT_COST,-1,-1;CL_TF_COST "TO_FROM COST" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_TF_COST,-1,-1;CL_DIVIDED "ROADWAY DIVIDED" true true false 1 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_DIVIDED,-1,-1;CL_IN_WATER "IN WATER" true true false 1 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_IN_WATER,-1,-1;CL_IN_COUNTY "IN COUNTY" true true false 1 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_IN_COUNTY,-1,-1;CL_CFCC "CFCC" true true false 6 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_CFCC,-1,-1;CL_MTFCC "MTFCC" true true false 6 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_MTFCC,-1,-1;CL_RD_CLASS "ROAD CLASS" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_RD_CLASS,-1,-1;CL_P_LL "PARITY LEFT LOW #" true true false 1 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_P_LL,-1,-1;CL_P_LH "PARITY LEFT HIGH #" true true false 1 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_P_LH,-1,-1;CL_P_RL "PARITY RIGHT LOW #" true true false 1 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_P_RL,-1,-1;CL_P_RH "PARITY RIGHT HIGH #" true true false 1 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_P_RH,-1,-1;CL_P_ALL "PARITY ALL" true true false 4 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_P_ALL,-1,-1;CL_LO_CROSS "LOW CROSS STREET" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_LO_CROSS,-1,-1;CL_HI_CROSS "HIGH CROSS STREET" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_HI_CROSS,-1,-1;CL_UPD_CODE "UPDATE CODE" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_UPD_CODE,-1,-1;CL_ADD_DATE "ADD DATE" true true false 8 Date 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_ADD_DATE,-1,-1;CL_UPD_DATE "UPDATE DATE" true true false 8 Date 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_UPD_DATE,-1,-1;CL_UPD_USER "UPDATE USER" true true false 100 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_UPD_USER,-1,-1;CL_COUNTY_NAME_L "COUNTY NAME LEFT" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_COUNTY_NAME_L,-1,-1;CL_COUNTY_NAME_R "COUNTY NAME RIGHT" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_COUNTY_NAME_R,-1,-1;CL_COUNTY_FIPS_L "COUNTY FIPS LEFT" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_COUNTY_FIPS_L,-1,-1;CL_COUNTY_FIPS_R "COUNTY FIPS RIGHT" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_COUNTY_FIPS_R,-1,-1;CL_CAD_NTID "CAD NTID" true true false 254 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_CAD_NTID,-1,-1;CL_ADDRESS_COUNT "ADDRESS COUNT" true true false 4 Long 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_ADDRESS_COUNT,-1,-1;CL_DiscrpAGID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_DiscrpAGID,-1,-1;CL_COUNTRY_L "Country Left" true true false 2 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_COUNTRY_L,-1,-1;CL_COUNTRY_R "Country Right" true true false 2 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_COUNTRY_R,-1,-1;POST_OFFICE "POST OFFICE" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,POST_OFFICE,-1,-1;ZIPCODE "ZIPCODE" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,ZIPCODE,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE_DATE" true true false 8 Date 0 0 ,First,#,STREET_CENTERLINE_Layer,UPDATE_DATE,-1,-1;SHAPE_STLength_1 "SHAPE_STLength_1" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,SHAPE_STLength_1,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,SHAPE_Length,-1,-1', "")
except:
    print ("\n Unable to Output STREET_CENTERLINE_Layer to DELETE_FILE, to append to Centerline_CrawfordCo - Northern Tier FGDB")
    write_log("Unable to Output STREET_CENTERLINE_Layer to DELETE_FILE, to append to Centerline_CrawfordCo - Northern Tier FGDB", logfile)
    logging.exception('Got exception on Output STREET_CENTERLINE_Layer to DELETE_FILE, to append to Centerline_CrawfordCo - Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append STREET_CENTERLINE_Layer to Centerline_CrawfordCo - Northern Tier FGDB (append Crawford centerline to staging FGDB created in steps above)
#    arcpy.Append_management(STREET_CENTERLINE_Layer, Centerline_CrawfordCo, "NO_TEST", 'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_DiscrpAGID,-1,-1;DateUpdate "DateUpdate" true true false 8 Date 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_UPD_DATE,-1,-1;Effective "Effective" true true false 8 Date 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_ADD_DATE,-1,-1;Expire "Expire" true true false 8 Date 0 0 ,First,#;RCL_NGUID "RCL_NGUID" true true false 254 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_CAD_NTID,-1,-1;AdNumPre_L "AdNumPre_L" true true false 15 Text 0 0 ,First,#;AdNumPre_R "AdNumPre_R" true true false 15 Text 0 0 ,First,#;FromAddr_L "FromAddr_L" true true false 4 Long 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_L_LO,-1,-1;ToAddr_L "ToAddr_L" true true false 4 Long 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_L_HI,-1,-1;FromAddr_R "FromAddr_R" true true false 4 Long 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_R_LO,-1,-1;ToAddr_R "ToAddr_R" true true false 4 Long 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_R_HI,-1,-1;Parity_L "Parity_L" true true false 1 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_P_LL,-1,-1;Parity_R "Parity_R" true true false 1 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_P_RL,-1,-1;St_PreMod "St_PreMod" true true false 15 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_PRE_MOD,-1,-1;St_PreDir "St_PreDir" true true false 9 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_PRE_DIR,-1,-1;St_PreTyp "St_PreTyp" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_PRE_TYPE,-1,-1;St_PreSep "St_PreSep" true true false 20 Text 0 0 ,First,#;St_Name "St_Name" true true false 60 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_NAME,-1,-1;St_PosTyp "St_PosTyp" true true false 50 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_SUFFIX,-1,-1;St_PosDir "St_PosDir" true true false 9 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_POST_DIR,-1,-1;St_PosMod "St_PosMod" true true false 25 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_POST_MOD,-1,-1;LSt_PreDir "LSt_PreDir" true true false 2 Text 0 0 ,First,#;LSt_Name "LSt_Name" true true false 75 Text 0 0 ,First,#;LSt_Type "LSt_Type" true true false 4 Text 0 0 ,First,#;LStPosDir "LStPosDir" true true false 2 Text 0 0 ,First,#;ESN_L "ESN_L" true true false 5 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_ESN_L,-1,-1;ESN_R "ESN_R" true true false 5 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_ESN_R,-1,-1;MSAGComm_L "MSAGComm_L" true true false 30 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_MUNI_L,-1,-1;MSAGComm_R "MSAGComm_R" true true false 30 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_MUNI_R,-1,-1;Country_L "Country_L" true true false 2 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_COUNTRY_L,-1,-1;Country_R "Country_R" true true false 2 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_COUNTRY_R,-1,-1;State_L "State_L" true true false 2 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_STATE_L,-1,-1;State_R "State_R" true true false 2 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_STATE_R,-1,-1;County_L "County_L" true true false 40 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_COUNTY_NAME_L,-1,-1;County_R "County_R" true true false 40 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_COUNTY_NAME_R,-1,-1;AddCode_L "AddCode_L" true true false 6 Text 0 0 ,First,#;AddCode_R "AddCode_R" true true false 6 Text 0 0 ,First,#;IncMuni_L "IncMuni_L" true true false 100 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_MUNI_L,-1,-1;IncMuni_R "IncMuni_R" true true false 100 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_MUNI_R,-1,-1;UnincCom_L "UnicCom_L" true true false 100 Text 0 0 ,First,#;UnincCom_R "Uninc" true true false 100 Text 0 0 ,First,#;NbrhdCom_L "NbrhdCom_L" true true false 100 Text 0 0 ,First,#;NbrhdCom_R "NbrhdCom_R" true true false 100 Text 0 0 ,First,#;PostCode_L "PostCode_L" true true false 7 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,ZIPCODE,-1,-1;PostCode_R "PostCode_R" true true false 7 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,ZIPCODE,-1,-1;PostComm_L "PostComm_L" true true false 40 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,POST_OFFICE,-1,-1;PostComm_R "PostComm_R" true true false 40 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,POST_OFFICE,-1,-1;RoadClass "RoadClass" true true false 15 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_RD_CLASS,-1,-1;OneWay "OneWay" true true false 2 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_ONE_WAY,-1,-1;SpeedLimit "SpeedLimit" true true false 2 Short 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_SPEED_LMT,-1,-1;Valid_L "Valid_L" true true false 1 Text 0 0 ,First,#;Valid_R "Valid_R" true true false 1 Text 0 0 ,First,#;Time "Time" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_FT_COST,-1,-1;Max_Height "Max_Height" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_HEIGHT_LMT,-1,-1;Max_Weight "Max_Weight" true true false 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_WEIGHT_LMT,-1,-1;T_ZLev "T_ZLev" true true false 2 Short 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_Z_ELEV_T,-1,-1;F_ZLev "F_ZLev" true true false 2 Short 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_Z_ELEV_F,-1,-1;JOIN_ID "JOIN_ID" true true false 4 Long 0 0 ,First,#;FullName "FullName" true true false 80 Text 0 0 ,First,#,STREET_CENTERLINE_Layer,CL_FULL_NAME,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0 ,First,#,STREET_CENTERLINE_Layer,SHAPE_Length,-1,-1', "")
    arcpy.Append_management(STREET_CENTERLINE_Layer_OUTPUT, Centerline_CrawfordCo, "NO_TEST", 'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_DiscrpAGID,-1,-1;DateUpdate "DateUpdate" true true false 8 Date 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_UPD_DATE,-1,-1;Effective "Effective" true true false 8 Date 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_ADD_DATE,-1,-1;Expire "Expire" true true false 8 Date 0 0 ,First,#;RCL_NGUID "RCL_NGUID" true true false 254 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_CAD_NTID,-1,-1;AdNumPre_L "AdNumPre_L" true true false 15 Text 0 0 ,First,#;AdNumPre_R "AdNumPre_R" true true false 15 Text 0 0 ,First,#;FromAddr_L "FromAddr_L" true true false 4 Long 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_L_LO,-1,-1;ToAddr_L "ToAddr_L" true true false 4 Long 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_L_HI,-1,-1;FromAddr_R "FromAddr_R" true true false 4 Long 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_R_LO,-1,-1;ToAddr_R "ToAddr_R" true true false 4 Long 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_R_HI,-1,-1;Parity_L "Parity_L" true true false 1 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_P_LL,-1,-1;Parity_R "Parity_R" true true false 1 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_P_RL,-1,-1;St_PreMod "St_PreMod" true true false 15 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_PRE_MOD,-1,-1;St_PreDir "St_PreDir" true true false 9 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_PRE_DIR,-1,-1;St_PreTyp "St_PreTyp" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_PRE_TYPE,-1,-1;St_PreSep "St_PreSep" true true false 20 Text 0 0 ,First,#;St_Name "St_Name" true true false 60 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_NAME,-1,-1;St_PosTyp "St_PosTyp" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_SUFFIX,-1,-1;St_PosDir "St_PosDir" true true false 9 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_POST_DIR,-1,-1;St_PosMod "St_PosMod" true true false 25 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_POST_MOD,-1,-1;LSt_PreDir "LSt_PreDir" true true false 2 Text 0 0 ,First,#;LSt_Name "LSt_Name" true true false 75 Text 0 0 ,First,#;LSt_Type "LSt_Type" true true false 4 Text 0 0 ,First,#;LStPosDir "LStPosDir" true true false 2 Text 0 0 ,First,#;ESN_L "ESN_L" true true false 5 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_ESN_L,-1,-1;ESN_R "ESN_R" true true false 5 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_ESN_R,-1,-1;MSAGComm_L "MSAGComm_L" true true false 30 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_MUNI_L,-1,-1;MSAGComm_R "MSAGComm_R" true true false 30 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_MUNI_R,-1,-1;Country_L "Country_L" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_COUNTRY_L,-1,-1;Country_R "Country_R" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_COUNTRY_R,-1,-1;State_L "State_L" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_STATE_L,-1,-1;State_R "State_R" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_STATE_R,-1,-1;County_L "County_L" true true false 40 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_COUNTY_NAME_L,-1,-1;County_R "County_R" true true false 40 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_COUNTY_NAME_R,-1,-1;AddCode_L "AddCode_L" true true false 6 Text 0 0 ,First,#;AddCode_R "AddCode_R" true true false 6 Text 0 0 ,First,#;IncMuni_L "IncMuni_L" true true false 100 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_MUNI_L,-1,-1;IncMuni_R "IncMuni_R" true true false 100 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_MUNI_R,-1,-1;UnincCom_L "UnicCom_L" true true false 100 Text 0 0 ,First,#;UnincCom_R "Uninc" true true false 100 Text 0 0 ,First,#;NbrhdCom_L "NbrhdCom_L" true true false 100 Text 0 0 ,First,#;NbrhdCom_R "NbrhdCom_R" true true false 100 Text 0 0 ,First,#;PostCode_L "PostCode_L" true true false 7 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',ZIPCODE,-1,-1;PostCode_R "PostCode_R" true true false 7 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',ZIPCODE,-1,-1;PostComm_L "PostComm_L" true true false 40 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',POST_OFFICE,-1,-1;PostComm_R "PostComm_R" true true false 40 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',POST_OFFICE,-1,-1;RoadClass "RoadClass" true true false 15 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_RD_CLASS,-1,-1;OneWay "OneWay" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_ONE_WAY,-1,-1;SpeedLimit "SpeedLimit" true true false 2 Short 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_SPEED_LMT,-1,-1;Valid_L "Valid_L" true true false 1 Text 0 0 ,First,#;Valid_R "Valid_R" true true false 1 Text 0 0 ,First,#;Time "Time" true true false 8 Double 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_FT_COST,-1,-1;Max_Height "Max_Height" true true false 8 Double 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_HEIGHT_LMT,-1,-1;Max_Weight "Max_Weight" true true false 8 Double 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_WEIGHT_LMT,-1,-1;T_ZLev "T_ZLev" true true false 2 Short 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_Z_ELEV_T,-1,-1;F_ZLev "F_ZLev" true true false 2 Short 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_Z_ELEV_F,-1,-1;JOIN_ID "JOIN_ID" true true false 4 Long 0 0 ,First,#;FullName "FullName" true true false 80 Text 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_FULL_NAME,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0 ,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',SHAPE_Length,-1,-1', "")
    Centerline_result = arcpy.GetCount_management(Centerline_CrawfordCo)
    print ('{} has {} records'.format(Centerline_CrawfordCo, Centerline_result[0]))
    write_log('{} has {} records'.format(Centerline_CrawfordCo, Centerline_result[0]), logfile)
except:
    print ("\n Unable to append STREET_CENTERLINE_Layer to Centerline_CrawfordCo - Northern Tier FGDB")
    write_log("Unable to append STREET_CENTERLINE_Layer to Centerline_CrawfordCo - Northern Tier FGDB", logfile)
    logging.exception('Got exception on append STREET_CENTERLINE_Layer to Centerline_CrawfordCo - Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

# Convert Road Classification (iterate through centerline export and convert road classification from Crawford County system to Northern Tier System)
Crawford_Road_Class = ["1", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
NT_Road_Class = ["Interstate", "Other Road", "US Highway", "State Highway", "State Road", "Local Road", "Other Road", "Other Road", "Other Road", "Other Road", "Other Road", "Other Road", "State Road"]
    
try:    
    with arcpy.da.UpdateCursor(Centerline_CrawfordCo, 'RoadClass') as cursor:
        for row in cursor:
            if row[0] in Crawford_Road_Class:
                row[0] = NT_Road_Class[Crawford_Road_Class.index(row[0])]
                cursor.updateRow(row)
            elif row[0] is None:
                row[0] = "Local Road"
                cursor.updateRow(row)
            else:
                pass
        del row 
        del cursor
        print ("    Road classification converted to Northern Tier standards...")
except:
    print ("\n Unable to convert Road Classification")
    write_log("Unable to convert Road Classification", logfile)
    logging.exception('Got exception on convert Road Classification logged at:'  + str(Day) + " " + str(Time))
    raise
    pass
    sys.exit ()

print ("       Street Centerline append completed")
write_log("       Street Centerline append completed", logfile)

print ("\n Process BLS & ALS layers from CRAW_INTERNAL to create EMS Districts and append to Northern Tier FGDB")
write_log("\n Process BLS & ALS layers from CRAW_INTERNAL to create EMS Districts and append to Northern Tier FGDB", logfile)

try:
    # Make Feature Layer_BLSResponse (make a temporary layer file of BLS coverage, so it can be manipulated)
    BLS_COVERAGE_INTERNAL_Layer = arcpy.MakeFeatureLayer_management(BLS_COVERAGE_INTERNAL, "BLS_COVERAGE_INTERNAL_Layer", "", "", "EMS_DEPT EMS_DEPT VISIBLE NONE;EMS_NUM EMS_NUM VISIBLE NONE;EMS_EMSID EMS_EMSID VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;GLOBALID GLOBALID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;STATE STATE VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print "\n Unable to Make Feature Layer_BLSResponse"
    write_log("Unable to Make Feature Layer_BLSResponse", logfile)
    logging.exception('Got exception on Make Feature Layer_BLSResponse logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

# Set temp variables for next step 
Intersect_analysis_feature_list = [ALS_ZONES_INTERNAL, "BLS_COVERAGE_INTERNAL_Layer"]
Intersect_analysis_feature_output = DELETE_FILES + "\\ALS_JOIN_DELETE_Intersect_DELETE"

try:
    # Intersect ALS Zones with BLS Coverage (intersect BLS and ALS coverages, to break up ALS into BLS sized polygons, to serve the EMS districts FC in CAD)
    arcpy.Intersect_analysis(Intersect_analysis_feature_list, Intersect_analysis_feature_output, "ALL", "", "INPUT")
except:
    print "\n Unable to Intersect ALS Zones with BLS Coverage"
    write_log("Unable to Intersect ALS Zones with BLS Coverage", logfile)
    logging.exception('Got exception on Intersect ALS Zones with BLS Coverage logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Spatial Join - BLS Coverage Internal / ALS Zones Internal  (spatial join ALS to BLS, to get data from fields of both features)
    arcpy.SpatialJoin_analysis(Intersect_analysis_feature_output, ALS_ZONES_INTERNAL, DELETE_FILES + "//BLS_ALS_INTERSECT_Spatial_Join", "JOIN_ONE_TO_ONE", "KEEP_ALL", 'ALS_ID "ALS UNQUIE ID #" true true false 8 Double 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',ALS_ID,-1,-1;ALS_NAME "ALS SERVICE NAME" true true false 75 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',ALS_NAME,-1,-1;UPDATE_DATE "UPDATE DATE" true true false 8 Date 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',UPDATE_DATE,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',COUNTY_FIPS,-1,-1;FID_ALS_ZONES_INTERNAL "FID_ALS_ZONES_INTERNAL" true true false 4 Long 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',FID_ALS_ZONES_INTERNAL,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',DiscrpAgID_1,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',STATE_1,-1,-1;EMS_DEPT "BLS/EMS DEPARTMENT" true true false 50 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',EMS_DEPT,-1,-1;EMS_NUM "BLS/EMS DEPARTMENT #" true true false 10 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',EMS_NUM,-1,-1;EMS_EMSID "EMS ID CODE" true true false 10 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',EMS_EMSID,-1,-1;COUNTY_NAME_1 "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',COUNTY_NAME_1,-1,-1;COUNTY_FIPS_1 "COUNTY FIPS CODE" true true false 8 Double 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',COUNTY_FIPS_1,-1,-1;FID_BLS_COVERAGE_INTERNAL "FID_BLS_COVERAGE_INTERNAL" true true false 4 Long 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',FID_BLS_COVERAGE_INTERNAL,-1,-1;DiscrpAgID_1 "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',DiscrpAgID_1,-1,-1;STATE_1 "State" true true false 2 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',STATE_1,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',SHAPE_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',SHAPE_Area,-1,-1;ALS_ID_1 "ALS UNQUIE ID #" true true false 8 Double 8 38 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,ALS_ID,-1,-1;ALS_NAME_1 "ALS SERVICE NAME" true true false 75 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,ALS_NAME,-1,-1;UPDATE_DATE_1 "UPDATE DATE" true true false 8 Date 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,UPDATE_DATE,-1,-1;COUNTY_NAME_12 "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS_12 "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,COUNTY_FIPS,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,GLOBALID,-1,-1;DiscrpAgID_12 "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,DiscrpAgID,-1,-1;STATE_12 "State" true true false 2 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,STATE,-1,-1;SHAPE_STArea__ "SHAPE_STArea__" false false true 0 Double 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE_STLength__ "SHAPE_STLength__" false false true 0 Double 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,SHAPE.STLength(),-1,-1', "HAVE_THEIR_CENTER_IN", "", "")
except:
    print "\n Unable to Spatial Join - BLS Coverage Internal / ALS Zones Internal"
    write_log("Unable to Spatial Join - BLS Coverage Internal / ALS Zones Internal", logfile)
    logging.exception('Got exception on Spatial Join - BLS Coverage Internal / ALS Zones Internal logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Add Description Field to EMSDistricts
    arcpy.AddField_management(BLS_ALS_INTERSECT_Spatial_Join, "Description", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print "\n Unable to Add Description Field to EMSDistricts"
    write_log("Unable to Add Description Field to EMSDistricts", logfile)
    logging.exception('Got exception on Add Description Field to EMSDistricts logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Add ID Field to EMSDistricts
    arcpy.AddField_management(BLS_ALS_INTERSECT_Spatial_Join, "ID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print "\n Unable to Add ID Field to EMSDistricts"
    write_log("Unable to Add ID Field to EMSDistricts", logfile)
    logging.exception('Got exception on Add ID Field to EMSDistricts logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Add ID_TEMP Field to EMSDistricts (ID is source data is text format, need to calculate into integer, temp field added)
    arcpy.AddField_management(BLS_ALS_INTERSECT_Spatial_Join, "ID_TEMP", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print "\n Unable to Add ID_TEMP Field to EMSDistricts"
    write_log("Unable to Add ID_TEMP Field to EMSDistricts", logfile)
    logging.exception('Got exception on Add ID_TEMP Field to EMSDistricts logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Calculate Field - EMSDistricts Description (calculate first 12 digits of ALS_NAME - EMS_NUM into field)
    arcpy.CalculateField_management(BLS_ALS_INTERSECT_Spatial_Join, "Description", '"{} - {}".format(!ALS_NAME![0:12], !EMS_NUM!)', "PYTHON", "")
except:
    print "\n Unable to Calculate Field - EMSDistricts Description"
    write_log("Unable to Calculate Field - EMSDistricts Description", logfile)
    logging.exception('Got exception on Unable to Calculate Field - EMSDistricts Description logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calculate Field - EMSDistricts ID_TEMP
    arcpy.CalculateField_management(BLS_ALS_INTERSECT_Spatial_Join, "ID_TEMP",'!ALS_ID!', "PYTHON", "")
except:
    print "\n Unable to Calculate Field - EMSDistricts ID_TEMP"
    write_log("Unable to Calculate Field - EMSDistricts ID_TEMP", logfile)
    logging.exception('Got exception on Unable to Calculate Field - EMSDistricts ID_TEMP logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()


try:
    # Calculate Field - EMSDistricts ID (calculate 2 + the last 5 digits of ID_TEMP + EMS_ID)
    arcpy.CalculateField_management(BLS_ALS_INTERSECT_Spatial_Join, "ID", '"2"+str(!ID_TEMP!)[5:]+str(!EMS_EMSID!)', "PYTHON", "")
except:
    print "\n Unable to Calculate Field - EMSDistricts ID"
    write_log("Unable to Calculate Field - EMSDistricts ID", logfile)
    logging.exception('Got exception on Unable to Calculate Field - EMSDistricts ID logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Append BLS_ALS_INTERSECT_Spatial_Join to EMS Districts to Northern Tier FGDB (append BLS coverage manipulated from steps above to staging FGDB)
    arcpy.Append_management(BLS_ALS_INTERSECT_Spatial_Join, EMS_Districts_CrawfordCo, "NO_TEST", 'Description "Description" true true false 50 Text 0 0 ,First,#,'+BLS_ALS_INTERSECT_Spatial_Join+',Description,-1,-1;ID "ID" true true false 4 Long 0 0 ,First,#,'+BLS_ALS_INTERSECT_Spatial_Join+',ID,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,'+BLS_ALS_INTERSECT_Spatial_Join+',SHAPE_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,'+BLS_ALS_INTERSECT_Spatial_Join+',SHAPE_Area,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+BLS_ALS_INTERSECT_Spatial_Join+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+BLS_ALS_INTERSECT_Spatial_Join+',STATE,-1,-1', "")
    EMS_Districts_result = arcpy.GetCount_management(EMS_Districts_CrawfordCo)
    print ('{} has {} records'.format(EMS_Districts_CrawfordCo, EMS_Districts_result[0]))
    write_log('{} has {} records'.format(EMS_Districts_CrawfordCo, EMS_Districts_result[0]), logfile)
except:
    print "\n Unable to Append BLS_ALS_INTERSECT_Spatial_Join to EMS Districts to Northern Tier FGDB"
    write_log("Unable to Append BLS_ALS_INTERSECT_Spatial_Join to EMS Districts to Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append BLS_ALS_INTERSECT_Spatial_Join to EMS Districts to Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print "       BLS-ALS Coverage to EMS Districts append completed"
write_log("       BLS-ALS Coverage to EMS Districts append completed", logfile)


print "\n Append Fire Department Coverage from CRAW_INTERNAL to Northern Tier FGDB"
write_log("\n Append Fire Department Coverage from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Fire Dept Coverage to Delete Files (create temporary fire dept feature in delete files FDS for manipulation into fire dept for CAD)
    arcpy.FeatureClassToFeatureClass_conversion(FIRE_DEPT_COVERAGE_INTERNAL, DELETE_FILES, "FIRE_DEPT_COVERAGE_DELETE", "", 'FIRE_DEPT "FIRE DEPARTMENT" true true false 50 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',FIRE_DEPT,-1,-1;FIRE_FDID "FIRE DEPARTMENT FDID CODE" true true false 15 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',FIRE_FDID,-1,-1;FIRE_NUM "FIRE DEPARTMENT #" true true false 10 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',FIRE_NUM,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',COUNTY_FIPS,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',GLOBALID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',STATE,-1,-1;SHAPE_STArea__ "SHAPE_STArea__" false false true 0 Double 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',SHAPE.STArea(),-1,-1;SHAPE_STLength__ "SHAPE_STLength__" false false true 0 Double 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',SHAPE.STLength(),-1,-1', "")
except:
    print "\n Unable to export Fire Dept Coverage to Delete Files"
    write_log("Unable to export Fire Dept Coverage to Delete Files", logfile)
    logging.exception('Got exception on export Fire Dept Coverage to Delete Files logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Add ID Field to FireDept_COVERAGE_DELETE
    arcpy.AddField_management(FIRE_DEPT_COVERAGE_DELETE, "ID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print "\n Unable to Add ID Field to FireDept_COVERAGE_DELETE"
    write_log("Unable to Add ID Field to FireDept_COVERAGE_DELETE", logfile)
    logging.exception('Got exception on Add ID Field to FireDept_COVERAGE_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
   
try:
    # Calculate ID Field FIRE_DEPT_COVERAGE_DELETE (calculate 20+FIRE_FDID into field)
    arcpy.CalculateField_management(FIRE_DEPT_COVERAGE_DELETE, "ID", '"20"+ !FIRE_FDID!', "PYTHON", "")
except:
    print "\n Unable to Calculate ID Field FIRE_DEPT_COVERAGE_DELETE"
    write_log("Unable to Calculate ID Field FIRE_DEPT_COVERAGE_DELETE", logfile)
    logging.exception('Got exception on Calculate ID Field FIRE_DEPT_COVERAGE_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to Northern Tier FGDB (append fire dept coverage manipulated from steps above to staging FGDB)
    arcpy.Append_management(FIRE_DEPT_COVERAGE_DELETE, Fire_Department_CrawfordCo, "NO_TEST", 'Description "Description" true true false 50 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',FIRE_DEPT,-1,-1;ID "ID" true true false 4 Long 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',ID,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',Shape_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',Shape_Area,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',STATE,-1,-1', "")
    Fire_Department_result = arcpy.GetCount_management(Fire_Department_CrawfordCo)
    print ('{} has {} records'.format(Fire_Department_CrawfordCo, Fire_Department_result[0]))
    write_log('{} has {} records'.format(Fire_Department_CrawfordCo, Fire_Department_result[0]), logfile)
except:
    print "\n Unable to Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to Northern Tier FGDB"
    write_log("Unable to Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
   
print "       Fire Department Coverage to Fire Department append completed"
write_log("       Fire Department Coverage to Fire Department append completed", logfile)


print "\n Process Fire Department Coverage & Fire Grids from CRAW_INTERNAL as Fire Response and append to Northern Tier FGDB"
write_log("\n Process Fire Department Coverage & Fire Grids from CRAW_INTERNAL as Fire Response and append to Northern Tier FGDB", logfile)

try:
    # Make Feature Layer from Fire Department Internal (create temporary fire dept layer for manipulation into fire response for CAD)
    FIRE_DEPT_COVERAGE_INTERNAL_LYR = arcpy.MakeFeatureLayer_management(FIRE_DEPT_COVERAGE_INTERNAL, "FIRE_DEPT_COVERAGE_INTERNAL_LYR", "", "", "FIRE_DEPT FIRE_DEPT VISIBLE NONE;FIRE_FDID FIRE_FDID VISIBLE NONE;FIRE_NUM FIRE_NUM VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;GLOBALID GLOBALID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;STATE STATE VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print "\n Unable to Make Feature Layer from Fire Department Internal"
    write_log("Unable to Make Feature Layer from Fire Department Internal", logfile)
    logging.exception('Got exception on Make Feature Layer from Fire Department Internal logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Spatial Join Fire Dept Internal Layer and Fire Grids (spatial join fire dept coverage and fire grids, to break up fire departments into grid sized areas)
    arcpy.SpatialJoin_analysis(FIRE_GRIDS_INTERNAL, FIRE_DEPT_COVERAGE_INTERNAL_LYR, FIRE_GRIDS_JOIN_DELETE, "JOIN_ONE_TO_ONE", "KEEP_ALL", 'Description "Description" true true false 50 Text 0 0 ,First,#,'+FIRE_GRIDS_INTERNAL+',Description,-1,-1;ID "ID" true true false 4 Long 0 10 ,First,#,'+FIRE_GRIDS_INTERNAL+',ID,-1,-1;FG_UNIQUE_ID "FG_UNIQUE_ID" true true false 4 Long 0 10 ,First,#,'+FIRE_GRIDS_INTERNAL+',FG_UNIQUE_ID,-1,-1;EDIT_DATE "EDIT_DATE" true true false 8 Date 0 0 ,First,#,'+FIRE_GRIDS_INTERNAL+',EDIT_DATE,-1,-1;Shape_STArea__ "Shape_STArea__" false false true 0 Double 0 0 ,First,#,'+FIRE_GRIDS_INTERNAL+',Shape.STArea(),-1,-1;Shape_STLength__ "Shape_STLength__" false false true 0 Double 0 0 ,First,#,'+FIRE_GRIDS_INTERNAL+',Shape.STLength(),-1,-1;FIRE_DEPT "FIRE DEPARTMENT" true true false 50 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,FIRE_DEPT,-1,-1;FIRE_FDID "FIRE DEPARTMENT FDID CODE" true true false 15 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,FIRE_FDID,-1,-1;FIRE_NUM "FIRE DEPARTMENT #" true true false 10 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,FIRE_NUM,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,COUNTY_FIPS,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,GLOBALID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,STATE,-1,-1;SHAPE_STArea_1 "SHAPE_STArea_1" false true true 0 Double 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,SHAPE.STArea(),-1,-1;SHAPE_STLength_1 "SHAPE_STLength_1" false true true 0 Double 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,SHAPE.STLength(),-1,-1', "INTERSECT", "", "")
except:
    print "\n Unable to Spatial Join Fire Dept Internal Layer and Fire Grids"
    write_log("Unable to Spatial Join Fire Dept Internal Layer and Fire Grids", logfile)
    logging.exception('Got exception on Spatial Join Fire Dept Internal Layer and Fire Grids logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Add CAD_ID Field to FIRE_GRIDS_JOIN_DELETE
    arcpy.AddField_management(FIRE_GRIDS_JOIN_DELETE, "CAD_ID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print "\n Unable to Add CAD_ID Field to FIRE_GRIDS_JOIN_DELETE"
    write_log("Unable to Add CAD_ID Field to FIRE_GRIDS_JOIN_DELETE", logfile)
    logging.exception('Got exception on Add CAD_ID Field to FIRE_GRIDS_JOIN_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Process: Calculate Field CAD_ID
    arcpy.CalculateField_management(FIRE_GRIDS_JOIN_DELETE, "CAD_ID", "!ID!", "PYTHON", "")
except:
    print "\n Unable to Calculate Field CAD_ID"
    write_log("Unable to Calculate Field CAD_ID", logfile)
    logging.exception('Got exception on Calculate Field CAD_ID logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Add CAD_Description Field to FIRE_GRIDS_JOIN_DELETE
    arcpy.AddField_management(FIRE_GRIDS_JOIN_DELETE, "CAD_DESCRIPTION", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print "\n Unable to Add CAD_Description Field to FIRE_GRIDS_JOIN_DELETE"
    write_log("Unable to Add CAD_Description Field to FIRE_GRIDS_JOIN_DELETE", logfile)
    logging.exception('Got exception on Add CAD_Description Field to FIRE_GRIDS_JOIN_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Calculate CAD Description Field
    arcpy.CalculateField_management(FIRE_GRIDS_JOIN_DELETE, "CAD_DESCRIPTION", '"20"+"-"+ !Description!', "PYTHON", "")
except:
    print "\n Unable to Calculate CAD Description Field"
    write_log("Unable to Calculate CAD Description Field", logfile)
    logging.exception('Got exception on Calculate CAD Description Field logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Append FIRE_GRIDS_JOIN_DELETE to Fire Response in Northern Tier FGDB (append fire dept coverage manipulated from steps above to staging FGDB)
    arcpy.Append_management(FIRE_GRIDS_JOIN_DELETE, Fire_Response_CrawfordCo, "NO_TEST", 'Description "Description" true true false 50 Text 0 0 ,First,#,'+FIRE_GRIDS_JOIN_DELETE+',Description,-1,-1;ID "ID" true true false 4 Long 0 0 ,First,#,'+FIRE_GRIDS_JOIN_DELETE+',ID,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,'+FIRE_GRIDS_JOIN_DELETE+',Shape_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,'+FIRE_GRIDS_JOIN_DELETE+',Shape_Area,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+FIRE_GRIDS_JOIN_DELETE+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+FIRE_GRIDS_JOIN_DELETE+',STATE,-1,-1', "")
    Fire_Response_result = arcpy.GetCount_management(Fire_Response_CrawfordCo)
    print ('{} has {} records'.format(Fire_Response_CrawfordCo, Fire_Response_result[0]))
    write_log('{} has {} records'.format(Fire_Response_CrawfordCo, Fire_Response_result[0]), logfile)
except:
    print "\n Unable to Append FIRE_GRIDS_JOIN_DELETE to Fire Response in Northern Tier FGDB"
    write_log("Unable to Append FIRE_GRIDS_JOIN_DELETE to Fire Response in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append FIRE_GRIDS_JOIN_DELETE to Fire Response in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
print "       Fire Department-Fire Grids coverage to Fire Response append completed"
write_log("       Fire Department-Fire Grids coverage to Fire Response append completed", logfile)


print "\n Append Police Department Coverage from CRAW_INTERNAL to Northern Tier FGDB Police Department"
write_log("\n Append Police Department Coverage from CRAW_INTERNAL to Northern Tier FGDB Police Department", logfile)

try:
    # Export PoliceDept Internal to PoliceDept Delete (create temporary police dept feature in delete_file FDS for manipulation into police department for CAD)
    arcpy.FeatureClassToFeatureClass_conversion(POLICE_DEPT_COVERAGE_INTERNAL, DELETE_FILES, "POLICE_DEPT_COVERAGE_DELETE", "POLICE_DEPT <> 'PA STATE POLICE - CORRY' OR COUNTY_FIPS = 42039", 'POLICE_DEPT "POLICE DEPARTMENT" true true false 50 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',POLICE_DEPT,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',COUNTY_FIPS,-1,-1;POLICE_ID "POLICE_ID" true true false 4 Long 0 10 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',POLICE_ID,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',GLOBALID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',STATE,-1,-1;SHAPE_STArea__ "SHAPE_STArea__" false false true 0 Double 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',SHAPE.STArea(),-1,-1;SHAPE_STLength__ "SHAPE_STLength__" false false true 0 Double 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',SHAPE.STLength(),-1,-1', "")
except:
    print "\n Unable to Export PoliceDept Internal to PoliceDept Delete"
    write_log("Unable to Export PoliceDept Internal to PoliceDept Delete", logfile)
    logging.exception('Got exception on Export PoliceDept Internal to PoliceDept Delete logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Add PoliceDeptID Field to POLICE_DEPT_COVERAGE_DELETE
    arcpy.AddField_management(POLICE_DEPT_COVERAGE_DELETE, "ID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print "\n Unable to Add PoliceDeptID Field to POLICE_DEPT_COVERAGE_DELETE"
    write_log("Unable to Add PoliceDeptID Field to POLICE_DEPT_COVERAGE_DELETE", logfile)
    logging.exception('Got exception on Add PoliceDeptID Field to POLICE_DEPT_COVERAGE_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Calculate Field - PoliceDept ID (calculate 20+POLICE_ID into field)
    arcpy.CalculateField_management(POLICE_DEPT_COVERAGE_DELETE, "ID", '"20{}".format(!POLICE_ID!)', "PYTHON", "")
except:
    print "\n Unable to Calculate Field - PoliceDept ID"
    write_log("Unable to Calculate Field - PoliceDept ID", logfile)
    logging.exception('Got exception on Calculate Field - PoliceDept ID logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

# Calculate Description Field - ORI CODES (iterate through records, change police dept names into ORIs in POLICE_DEPT field, using dictonaries below)
Police_ID_Pre = ["PA STATE POLICE - MEADVILLE", "PA STATE POLICE - CORRY", "CAMBRIDGE SPRINGS POLICE", "COCHRANTON POLICE", "CONNEAUT LAKE REGIONAL POLICE", "LINESVILLE POLICE", "MEADVILLE CITY POLICE", "VERNON POLICE", "WEST MEAD POLICE", "TITUSVILLE CITY POLICE", "CAMBRIDGE SPRINGS POLICE"]
Police_ID_Post = ["PAPSP5500", "PAPSP1400", "PA200300", "PA200500", "PA201800", "PA200800", "PA200100", "PA201100", "PA201400", "PA200200", "PA0200300"]
    
try:    
    with arcpy.da.UpdateCursor(POLICE_DEPT_COVERAGE_DELETE, 'POLICE_DEPT') as cursor:
        for row in cursor:
            if row[0] in Police_ID_Pre:
                row[0] = Police_ID_Post[Police_ID_Pre.index(row[0])]
                cursor.updateRow(row)
        del row 
        del cursor
except:
    print "\n Unable to Calculate Description Field - ORI CODES"
    write_log("Unable to Calculate Description Field - ORI CODES", logfile)
    logging.exception('Got exception on Calculate Description Field - ORI CODES logged at:'  + str(Day) + " " + str(Time))
    raise
    pass
    sys.exit ()

try:
    # Dissolve POLICE_DEPT_COVERAGE_DELETE to elminate separate features
    arcpy.Dissolve_management(POLICE_DEPT_COVERAGE_DELETE, DELETE_FILES + "//POLICE_DEPT_COVERAGE_DELETE_DISSOLVE", "POLICE_DEPT;COUNTY_NAME;COUNTY_FIPS;POLICE_ID;DiscrpAgID;STATE;ID", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print "\n Unable to Dissolve POLICE_DEPT_COVERAGE_DELETE to elminate separate features"
    write_log("Unable to Dissolve POLICE_DEPT_COVERAGE_DELETE to elminate separate features", logfile)
    logging.exception('Got exception on Dissolve POLICE_DEPT_COVERAGE_DELETE to elminate separate features logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append POLICE_DEPT_COVERAGE_DELETE_DISSOLVE to Police Department in Northern Tier FGDB (append police dept coverage manipulated from steps above to staging FGDB)
    arcpy.Append_management(POLICE_DEPT_COVERAGE_DELETE_DISSOLVE, Police_Department_CrawfordCo, "NO_TEST", 'Description "Description" true true false 50 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_DELETE_DISSOLVE+',POLICE_DEPT,-1,-1;ID "ID" true true false 4 Long 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_DELETE_DISSOLVE+',ID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_DELETE_DISSOLVE+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_DELETE_DISSOLVE+',STATE,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_DELETE_DISSOLVE+',Shape_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_DELETE_DISSOLVE+',Shape_Area,-1,-1', "")
    Police_Department_result = arcpy.GetCount_management(Police_Department_CrawfordCo)
    print ('{} has {} records'.format(Police_Department_CrawfordCo, Police_Department_result[0]))
    write_log('{} has {} records'.format(Police_Department_CrawfordCo, Police_Department_result[0]), logfile)
except:
    print "\n Unable to Append POLICE_DEPT_COVERAGE_DELETE_DISSOLVE to Police Department in Northern Tier FGDB"
    write_log("Unable to Append POLICE_DEPT_COVERAGE_DELETE_DISSOLVE to Police Department in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append POLICE_DEPT_COVERAGE_DELETE_DISSOLVE to Police Department in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
print "      Police Department coverage to Police Department append completed"
write_log("      Police Department coverage to Police Department append completed", logfile)

print "\n Append Police Department Coverage from CRAW_INTERNAL to Northern Tier FGDB Police Response"
write_log("\n Append Police Department Coverage from CRAW_INTERNAL to Northern Tier FGDB Police Response", logfile)

try:
    # Dissolve POLICE_DEPT_COVERAGE_INTERNAL to eliminate separate features
    arcpy.Dissolve_management(POLICE_DEPT_COVERAGE_INTERNAL, DELETE_FILES + "//POLICE_RESPONSE_DISSOLVE", "POLICE_DEPT;COUNTY_NAME;COUNTY_FIPS;POLICE_ID;DiscrpAgID;STATE", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print "\n Unable to Dissolve POLICE_DEPT_COVERAGE_INTERNAL to eliminate separate features"
    write_log("Unable to Dissolve POLICE_DEPT_COVERAGE_INTERNAL to eliminate separate features", logfile)
    logging.exception('Got exception on Dissolve POLICE_DEPT_COVERAGE_INTERNAL to eliminate separate features logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append POLICE_DEPT_COVERAGE_INTERNAL to Police Response in Northern Tier FGDB (append police dept coverage, unchanged, into staging FGDB)
    arcpy.Append_management(POLICE_RESPONSE_DISSOLVE, Police_Response_CrawfordCo, "NO_TEST", 'Description "Description" true true false 50 Text 0 0 ,First,#,'+POLICE_RESPONSE_DISSOLVE+',POLICE_DEPT,-1,-1;ID "ID" true true false 4 Long 0 0 ,First,#,'+POLICE_RESPONSE_DISSOLVE+',POLICE_ID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+POLICE_RESPONSE_DISSOLVE+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+POLICE_RESPONSE_DISSOLVE+',STATE,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,'+POLICE_RESPONSE_DISSOLVE+',SHAPE_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,'+POLICE_RESPONSE_DISSOLVE+',SHAPE_Area,-1,-1', "")
    Police_Response_result = arcpy.GetCount_management(Police_Response_CrawfordCo)
    print ('{} has {} records'.format(Police_Response_CrawfordCo, Police_Response_result[0]))
    write_log('{} has {} records'.format(Police_Response_CrawfordCo, Police_Response_result[0]), logfile)
except:
    print "\n Unable to Append POLICE_DEPT_COVERAGE_INTERNAL to Police Response in Northern Tier FGDB"
    write_log("Unable to Append POLICE_DEPT_COVERAGE_INTERNAL to Police Response in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append POLICE_DEPT_COVERAGE_INTERNAL to Police Response in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
print "      Police Department coverage to Police Response append completed"
write_log("      Police Department coverage to Police Response append completed", logfile)


print "\n Process Municipal Boundaries with Police Department Coverage in Police Reporting and then append to Northern Tier FGDB"
write_log("\n Process Municipal Boundaries with Police Department Coverage in Police Reporting and then append to Northern Tier FGDB", logfile)

try:
    # Spatial Join COUNTY_ADJ_MUNI_BOUND_INTERNAL to POLICE_DEPT_COVERAGE_INTERNAL (spatial join county adjusted muni boundaries with police dept coverage to break up into municipal sized police zones for CAD police reporting)
    arcpy.SpatialJoin_analysis(COUNTY_ADJ_MUNI_BOUND_INTERNAL, POLICE_DEPT_COVERAGE_INTERNAL, POLICE_REPORT_JOIN_DELETE, "JOIN_ONE_TO_ONE", "KEEP_ALL", 'MUNI_NAME "MUNICIPALITY NAME" true true false 50 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',MUNI_NAME,-1,-1;MUNI_FIPS "MUNICIPALITY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',MUNI_FIPS,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE DATE" true true false 8 Date 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',UPDATE_DATE,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',GLOBALID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',STATE,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',DiscrpAgID,-1,-1;COUNTRY "Country" true true false 2 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',COUNTRY,-1,-1;SHAPE_STArea__ "SHAPE_STArea__" false false true 0 Double 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',SHAPE.STArea(),-1,-1;SHAPE_STLength__ "SHAPE_STLength__" false false true 0 Double 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',SHAPE.STLength(),-1,-1;POLICE_DEPT "POLICE DEPARTMENT" true true false 50 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,POLICE_DEPT,-1,-1;COUNTY_NAME_1 "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS_1 "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,COUNTY_FIPS,-1,-1;POLICE_ID "POLICE_ID" true true false 4 Long 0 10 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,POLICE_ID,-1,-1;GLOBALID_1 "GLOBALID_1" false false false 38 GlobalID 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,GLOBALID,-1,-1;DiscrpAgID_1 "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,DiscrpAgID,-1,-1;STATE_1 "State" true true false 2 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,STATE,-1,-1;SHAPE_STArea_1 "SHAPE_STArea_1" false false true 0 Double 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE_STLength_1 "SHAPE_STLength_1" false false true 0 Double 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,SHAPE.STLength(),-1,-1', "INTERSECT", "", "")
except:
    print "\n Unable to Spatial Join COUNTY_ADJ_MUNI_BOUND_INTERNAL to POLICE_DEPT_COVERAGE_INTERNAL"
    write_log("Unable to Spatial Join COUNTY_ADJ_MUNI_BOUND_INTERNAL to POLICE_DEPT_COVERAGE_INTERNAL", logfile)
    logging.exception('Got exception on Spatial Join COUNTY_ADJ_MUNI_BOUND_INTERNAL to POLICE_DEPT_COVERAGE_INTERNAL logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append POLICE_REPORT_JOIN_DELETE to Police Reporting in Northern Tier FGDB (append police dept coverage manipulated from steps above to staging FGDB)
    arcpy.Append_management(POLICE_REPORT_JOIN_DELETE, Police_Reporting_CrawfordCo, "NO_TEST", 'Description "Description" true true false 50 Text 0 0 ,First,#,'+POLICE_REPORT_JOIN_DELETE+',POLICE_DEPT,-1,-1;ID "ID" true true false 4 Long 0 0 ,First,#,'+POLICE_REPORT_JOIN_DELETE+',POLICE_ID,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,'+POLICE_REPORT_JOIN_DELETE+',SHAPE_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,'+POLICE_REPORT_JOIN_DELETE+',SHAPE_Area,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+POLICE_REPORT_JOIN_DELETE+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+POLICE_REPORT_JOIN_DELETE+',STATE,-1,-1', "")
    Police_Reporting_result = arcpy.GetCount_management(Police_Reporting_CrawfordCo)
    print ('{} has {} records'.format(Police_Reporting_CrawfordCo, Police_Reporting_result[0]))
    write_log('{} has {} records'.format(Police_Reporting_CrawfordCo, Police_Reporting_result[0]), logfile)
except:
    print "\n Unable to Append POLICE_REPORT_JOIN_DELETE to Police Reporting in Northern Tier FGDB"
    write_log("Unable to Append POLICE_REPORT_JOIN_DELETE to Police Reporting in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append POLICE_REPORT_JOIN_DELETE to Police Reporting in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print "       Police Department coverage-Municipal Boundary to Police Reporting append completed"
write_log("       Police Department coverage-Municipal Boundary to Police Reporting append completed", logfile)


print "\n Append Hydrants from CRAW_INTERNAL to Northern Tier FGDB"
write_log("\n Append Hydrants from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append HYDRANTS_DELETE to Hydrants in Northern Tier FGDB (append hydrants, data modified, into staging FGDB)
    arcpy.Append_management(HYDRANTS_INTERNAL, Hydrants_CrawfordCo, "NO_TEST", 'ID "ID" true true false 4 Long 0 0 ,First,#,'+HYDRANTS_INTERNAL+',ID,-1,-1;NWS_ADDRESS_ID "NWS_ADDRESS_ID" true true false 4 Long 0 0 ,First,#,'+HYDRANTS_INTERNAL+',ADDRESS_ID,-1,-1;NWS_HYDRANT_ID "NWS_HYDRANT_ID" true true false 4 Long 0 0 ,First,#,'+HYDRANTS_INTERNAL+',HYDRANT_ID,-1,-1;NWS_HYDRANT_NUMBER "NWS_HYDRANT_NUMBER" true true false 20 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',LOCAL_HYDRANT_NUMBER,-1,-1;NWS_HYDRANT_LOCATIONDESCRIPTION "NWS_HYDRANT_LOCATIONDESCRIPTION" true true false 50 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',HYDRANT_LOCATION_DESCRIPTION,-1,-1;NWS_HYDRANT_SERIAL_NUMBER "NWS_HYDRANT_SERIAL_NUMBER" true true false 20 Text 0 0 ,First,#;NWS_HYDRANT_IN_SERVICE "NWS_HYDRANT_IN_SERVICE" true true false 3 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',HYDRANT_IN_SERVICE,-1,-1;NWS_HYDRANT_COLOR "NWS_HYDRANT_COLOR" true true false 30 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',HYDRANT_COLOR,-1,-1;SIZE "SIZE" true true false 50 Text 0 0 ,First,#;TYPE "TYPE" true true false 50 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',TYPE,-1,-1;GPM "GPM" true true false 50 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',GPM,-1,-1', subtype="")
    Hydrants_result = arcpy.GetCount_management(Hydrants_CrawfordCo)
    print ('{} has {} records'.format(Hydrants_CrawfordCo, Hydrants_result[0]))
    write_log('{} has {} records'.format(Hydrants_CrawfordCo, Hydrants_result[0]), logfile)
except:
    print "\n Unable to Append HYDRANTS_INTERNAL to Hydrants in Northern Tier FGDB"
    write_log("Unable to Append Append HYDRANTS_INTERNAL to Hydrants in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append Append HYDRANTS_INTERNAL to Hydrants in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print "      Hydrants append completed"
write_log("      Hydrants append completed", logfile)


print "\n Append Landmarks from CRAW_INTERNAL to Northern Tier FGDB"
write_log("\n Append Landmarks from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append LANDMARKS_INTERNAL to Landmarks in Northern Tier FGDB (append landmarks, unchanged, into staging FGDB)
    arcpy.Append_management(LANDMARKS_INTERNAL, Landmarks_CrawfordCo, "NO_TEST",'DiscrpAgID "Agency ID" true true false 75 Text 0 0 ,First,#,'+LANDMARKS_INTERNAL+',LANDMARK_NAME,-1,-1;DateUpdate "Date Updated" true true false 8 Date 0 0 ,First,#,'+LANDMARKS_INTERNAL+',UPDATE_DATE,-1,-1;Effective "Effective Date" true true false 8 Date 0 0 ,First,#;Expire "Expiration Date" true true false 8 Date 0 0 ,First,#;LMNP_NGUID "Landmark Name GID" true true false 254 Text 0 0 ,First,#,'+LANDMARKS_INTERNAL+',LANDMARK_NAME,-1,-1;Site_NGUID "Site GID" true true false 254 Text 0 0 ,First,#,'+LANDMARKS_INTERNAL+',LANDMARK_NAME,-1,-1;ACLMNNGUID "Complete Landmark Name GID" true true false 254 Text 0 0 ,First,#,'+LANDMARKS_INTERNAL+',LANDMARK_NAME,-1,-1;LMNamePart "Landmark Name Part" true true false 150 Text 0 0 ,First,#,'+LANDMARKS_INTERNAL+',LANDMARK_NAME,-1,-1;LMNP_Order "Landmark Name Part Order" true true false 1 Text 0 0 ,First,#', "")
except:
    print "\n Unable to Append LANDMARKS_INTERNAL to Landmarks in Northern Tier FGDB"
    write_log("Unable to Append LANDMARKS_INTERNAL to Landmarks in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append LANDMARKS_INTERNAL to Landmarks in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calculate Landmarks DiscrpAgID field (With landmarks within staging FGDB)
    arcpy.CalculateField_management(Landmarks_CrawfordCo, "DiscrpAgID", "'crawford.state.pa.us'", "PYTHON", "")
    Landmarks_result = arcpy.GetCount_management(Landmarks_CrawfordCo)
    print ('{} has {} records'.format(Landmarks_CrawfordCo, Landmarks_result[0]))
    write_log('{} has {} records'.format(Landmarks_CrawfordCo, Landmarks_result[0]), logfile)
except:
    print "\n Unable to Calculate Landmarks DiscrpAgID field in Northern Tier FGDB"
    write_log("Unable to Calculate Landmarks DiscrpAgID field in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Calculate Landmarks DiscrpAgID field in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print "       Landmarks append completed"
write_log("       Landmarks append completed", logfile)


print "\n Append Mile Markers from CRAW_INTERNAL to Northern Tier FGDB"
write_log("\n Append Mile Markers from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append MILE_MARKERS_INTERNAL to MilePosts in Northern Tier FGDB (append Mile Markers, unchanged, into staging FGDB)
    arcpy.Append_management(MILE_MARKERS_INTERNAL, MilePosts_CrawfordCo, "NO_TEST", 'DiscrpAgID "Agency ID" true true false 75 Text 0 0 ,First,#,'+MILE_MARKERS_INTERNAL+',MARKER_NAME,-1,-1;DateUpdate "Date Updated" true true false 8 Date 0 0 ,First,#;MileMNGUID "Mile Post GID" true true false 254 Text 0 0 ,First,#,'+MILE_MARKERS_INTERNAL+',MARKER_NAME,-1,-1;MileM_Unit "MP Unit" true true false 15 Text 0 0 ,First,#,'+MILE_MARKERS_INTERNAL+',MILE_POST,-1,-1;MileMValue "MP Measurement" true true false 8 Double 0 0 ,First,#;MileM_Rte "MP Route Name" true true false 100 Text 0 0 ,First,#,'+MILE_MARKERS_INTERNAL+',STREET_NAME,-1,-1;MileM_Type "MP Type" true true false 15 Text 0 0 ,First,#;MileM_Ind "MP Indicator" true true false 1 Text 0 0 ,First,#', "")
    MilePosts_result = arcpy.GetCount_management(MilePosts_CrawfordCo)
    print ('{} has {} records'.format(MilePosts_CrawfordCo, MilePosts_result[0]))
    write_log('{} has {} records'.format(MilePosts_CrawfordCo, MilePosts_result[0]), logfile)
except:
    print "\n Unable to Append MILE_MARKERS_INTERNAL to MilePosts in Northern Tier FGDB"
    write_log("Unable to Append MILE_MARKERS_INTERNAL to MilePosts in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append MILE_MARKERS_INTERNAL to MilePosts in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print "       Mile Markers to Mile Posts append completed"
write_log("       Mile Markers to Mile Posts append completed", logfile)


print "\n Append Municipalities from CRAW_INTERNAL to Northern Tier FGDB"
write_log("\n Append Municipalities from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append COUNTY_ADJ_MUNI_BOUND_INTERNAL to Municipalities in Northern Tier FGDB (append county adjusted municipal boundaries, unchanged, into staging FGDB)
    arcpy.Append_management(COUNTY_ADJ_MUNI_BOUND_INTERNAL, Municipalities_CrawfordCo, "NO_TEST", 'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',DiscrpAgID,-1,-1;DateUpdate "DateUpdate" true true false 8 Date 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',UPDATE_DATE,-1,-1;Effective "Effective" true true false 8 Date 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',UPDATE_DATE,-1,-1;Expire "Expire" true true false 8 Date 0 0 ,First,#;Shape_Leng "Shape_Leng" true true false 8 Double 0 0 ,First,#;IncM_NGUID "IncM_NGUID" true true false 254 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',MUNI_FIPS,-1,-1;Country "Country" true true false 2 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',COUNTRY,-1,-1;State "State" true true false 2 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',STATE,-1,-1;County "County" true true false 75 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',COUNTY_NAME,-1,-1;AddCode "AddCode" true true false 6 Text 0 0 ,First,#;Inc_Muni "Inc_Muni" true true false 100 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',MUNI_NAME,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0 ,First,#;Shape_Area "Shape_Area" false true true 8 Double 0 0 ,First,#', "")
    Municipalities_result = arcpy.GetCount_management(Municipalities_CrawfordCo)
    print ('{} has {} records'.format(Municipalities_CrawfordCo, Municipalities_result[0]))
    write_log('{} has {} records'.format(Municipalities_CrawfordCo, Municipalities_result[0]), logfile)
except:
    print "\n Unable to Append COUNTY_ADJ_MUNI_BOUND_INTERNAL to Municipalities in Northern Tier FGDB"
    write_log("Unable to Append COUNTY_ADJ_MUNI_BOUND_INTERNAL to Municipalities in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append COUNTY_ADJ_MUNI_BOUND_INTERNAL to Municipalities in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print "       Municipalities append completed"
write_log("       Municipalities append completed", logfile)


print "\n Append Tax Parcels from CRAW_INTERNAL to Northern Tier FGDB"
write_log("\n Append Tax Parcels from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append TAX_PARCELS_INTERNAL to Parcels in Northern Tier FGDB (append tax parcels, unchanged, into staging FGDB)
    arcpy.Append_management(TAX_PARCELS_INTERNAL, Parcels_CrawfordCo, "NO_TEST", 'ParcelID "ParcelID" true true false 25 Text 0 0 ,First,#;Map_Num "Map_Num" true true false 50 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',CAMA_PIN,-1,-1;Own "Own" true true false 100 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',REM_OWN_NAME,-1,-1;Add_Number "Add_Number" true true false 4 Long 0 0 ,First,#;AddNum_Suf "AddNum_Suf" true true false 15 Text 0 0 ,First,#;St_PreDir "St_PreDir" true true false 9 Text 0 0 ,First,#;St_Name "St_Name" true true false 60 Text 0 0 ,First,#;St_PostType "St_PostType" true true false 50 Text 0 0 ,First,#;St_PostDir "St_PostDir" true true false 9 Text 0 0 ,First,#;City "City" true true false 50 Text 0 0 ,First,#;Add_State "Add_State" true true false 2 Text 0 0 ,First,#;Zip "Zip" true true false 10 Text 0 0 ,First,#;Muni "Muni" true true false 100 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',SEC_MUNI_NAME,-1,-1;County "County" true true false 75 Text 0 0 ,First,#;State "State" true true false 2 Text 0 0 ,First,#;Contry "Contry" true true false 2 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#', "")
except:
    print "\n Unable to Append TAX_PARCELS_INTERNAL to Parcels in Northern Tier FGDB"
    write_log("Unable to Append TAX_PARCELS_INTERNAL to Parcels in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append TAX_PARCELS_INTERNAL to Parcels in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calculate County/State/Contry field (With tax parcels within staging FGDB)
    arcpy.CalculateField_management(Parcels_CrawfordCo, "County", "'CRAWFORD'", "PYTHON", "")
    arcpy.CalculateField_management(Parcels_CrawfordCo, "State", "'PA'", "PYTHON", "")
    arcpy.CalculateField_management(Parcels_CrawfordCo, "Contry", "'US'", "PYTHON", "")
    Parcels_result = arcpy.GetCount_management(Parcels_CrawfordCo)
    print ('{} has {} records'.format(Parcels_CrawfordCo, Parcels_result[0]))
    write_log('{} has {} records'.format(Parcels_CrawfordCo, Parcels_result[0]), logfile)
except:
    print "\n Unable to Calculate Parcels County/State/Contry field in Northern Tier FGDB"
    write_log("Unable to Calculate Parcels County/State/Contry field in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Calculate Parcels County/State/Contry field in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print "       Tax Parcels to Parcels append completed"
write_log("       Tax Parcels to Parcels append completed", logfile)


print "\n Append Railroads from CRAW_INTERNAL to Northern Tier FGDB"
write_log("\n Append Railroads from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append RAILROADS_INTERNAL to Railroads in Northern Tier FGDB (append railroads, unchanged, into staging FGDB)
    arcpy.Append_management(RAILROADS_INTERNAL, Railroads_CrawfordCo, "NO_TEST", 'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0 ,First,#;DateUpdate "DateUpdate" true true false 8 Date 0 0 ,First,#,'+RAILROADS_INTERNAL+',UPDATE_DATE,-1,-1;RS_NGUID "RS_NGUID" true true false 254 Text 0 0 ,First,#;RLOWN "RLOWN" true true false 100 Text 0 0 ,First,#,'+RAILROADS_INTERNAL+',OPERATIONS_OWNER,-1,-1;RLOP "RLOP" true true false 100 Text 0 0 ,First,#,'+RAILROADS_INTERNAL+',OPERATIONS_OWNER,-1,-1;Trck_Right "Trck_Right" true true false 100 Text 0 0 ,First,#,'+RAILROADS_INTERNAL+',TRACK_RIGHTS,-1,-1;RMPL "RMPL" true true false 8 Double 0 0 ,First,#;RMPH "RMPH" true true false 8 Double 0 0 ,First,#;Muni "Muni" true true false 100 Text 0 0 ,First,#,'+RAILROADS_INTERNAL+',MUNI_NAME,-1,-1;County "County" true true false 75 Text 0 0 ,First,#,'+RAILROADS_INTERNAL+',COUNTY_NAME,-1,-1;State "State" true true false 2 Text 0 0 ,First,#;Contry "Contry" true true false 2 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#', "")
except:
    print "\n Unable to Append RAILROADS_INTERNAL to Railroads in Northern Tier FGDB"
    write_log("Unable to Append RAILROADS_INTERNAL to Railroads in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append RAILROADS_INTERNAL to Railroads in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calculate DiscrpAgID/State/Contry field (With railroads within staging FGDB)
    arcpy.CalculateField_management(Railroads_CrawfordCo, "DiscrpAgID", "'crawford.state.pa.us'", "PYTHON", "")
    arcpy.CalculateField_management(Railroads_CrawfordCo, "State", "'PA'", "PYTHON", "")
    arcpy.CalculateField_management(Railroads_CrawfordCo, "Contry", "'US'", "PYTHON", "")
    Railroads_result = arcpy.GetCount_management(Railroads_CrawfordCo)
    print ('{} has {} records'.format(Railroads_CrawfordCo, Railroads_result[0]))
    write_log('{} has {} records'.format(Railroads_CrawfordCo, Railroads_result[0]), logfile)
except:
    print "\n Unable to Calculate DiscrpAgID/State/Contry field in Northern Tier FGDB"
    write_log("Unable to Calculate Parcels DiscrpAgID/State/Contry field to CRAWFORD in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Calculate Parcels DiscrpAgID/State/Contry field to CRAWFORD in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()    

print "      Railroads append completed"
write_log("      Railroads append completed", logfile)


print "\n Append County Adjusted Municipal Boundaries from CRAW_INTERNAL to Northern Tier FGDB"
write_log("\n Append County Adjusted Municipal Boundaries from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Make Feature Layer - Crawford Adjusted Muni (make temporary layer field of county adjusted muni boundaries for manipulation in steps below)
    arcpy.MakeFeatureLayer_management(COUNTY_ADJ_MUNI_BOUND_INTERNAL, COUNTY_ADJ_MUNI_LAYER, "", "", "MUNI_NAME MUNI_NAME VISIBLE NONE;MUNI_FIPS MUNI_FIPS VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;UPDATE_DATE UPDATE_DATE VISIBLE NONE;GLOBALID GLOBALID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;STATE STATE VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;COUNTRY COUNTRY VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print "\n Unable to Make Feature Layer - Crawford Adjusted Muni"
    write_log("Unable to Make Feature Layer - Crawford Adjusted Muni", logfile)
    logging.exception('Got exception on Make Feature Layer - Crawford Adjusted Muni logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Dissolve COUNTY_ADJ_MUNI_LAYER into County shape (dissolve all county adjusted muni boundaries into 1 polygon to make county polygon)
    arcpy.Dissolve_management(COUNTY_ADJ_MUNI_LAYER, MUNI_DISSOLVE, "COUNTY_NAME;COUNTY_FIPS;STATE;DiscrpAgID;COUNTRY", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print "\n Unable to Dissolve COUNTY_ADJ_MUNI_LAYER into County shape"
    write_log("Unable to Dissolve COUNTY_ADJ_MUNI_LAYER into County shape", logfile)
    logging.exception('Got exception on Dissolve COUNTY_ADJ_MUNI_LAYER into County shape logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append COUNTY_ADJ_MUNI_BOUND_DISSOLVE to Counties in Northern Tier FGDB (append county adjusted muni boundaries manipulated from steps above to staging FGDB)
    arcpy.Append_management(MUNI_DISSOLVE, Counties_CrawfordCo, "NO_TEST", 'Shape_Leng "Shape_Leng" true true false 8 Double 0 0 ,First,#;DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0 ,First,#,'+MUNI_DISSOLVE+',DiscrpAgID,-1,-1;DateUpdate "DateUpdate" true true false 8 Date 0 0 ,First,#;Effective "Effective" true true false 8 Date 0 0 ,First,#;Expire "Expire" true true false 8 Date 0 0 ,First,#;CntyNGUID "CntyNGUID" true true false 254 Text 0 0 ,First,#,'+MUNI_DISSOLVE+',COUNTY_FIPS,-1,-1;Country "Country" true true false 2 Text 0 0 ,First,#,'+MUNI_DISSOLVE+',COUNTRY,-1,-1;State "State" true true false 2 Text 0 0 ,First,#,'+MUNI_DISSOLVE+',STATE,-1,-1;County "County" true true false 75 Text 0 0 ,First,#,'+MUNI_DISSOLVE+',COUNTY_NAME,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0 ,First,#,'+MUNI_DISSOLVE+',SHAPE_Length,-1,-1;Shape_Area "Shape_Area" false true true 8 Double 0 0 ,First,#,'+MUNI_DISSOLVE+',SHAPE_Area,-1,-1', "")
    Counties_result = arcpy.GetCount_management(Counties_CrawfordCo)
    print ('{} has {} records'.format(Counties_CrawfordCo, Counties_result[0]))
    write_log('{} has {} records'.format(Counties_CrawfordCo, Counties_result[0]), logfile)
except:
    print "\n Unable to Append COUNTY_ADJ_MUNI_BOUND_DISSOLVE to Counties in Northern Tier FGDB"
    write_log("Unable to Append COUNTY_ADJ_MUNI_BOUND_DISSOLVE to Counties in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append COUNTY_ADJ_MUNI_BOUND_DISSOLVE to Counties in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calculate DateUpdate & Effective fields in Counties_CrawfordCo FC
    arcpy.CalculateField_management(Counties_CrawfordCo, "DateUpdate", "datetime.datetime.now( )", "PYTHON", "")
    arcpy.CalculateField_management(Counties_CrawfordCo, "Effective", "datetime.datetime.now( )", "PYTHON", "")
    print("  DateUpdate & Effective fields updated...")
except:
    print "\n Unable to calculate DateUpdate & Effective fields in Counties_CrawfordCo FC"
    write_log("Unable to calculate DateUpdate & Effective fields in Counties_CrawfordCo FC", logfile)
    logging.exception('Got exception on calculate DateUpdate & Effective fields in Counties_CrawfordCo FC logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print "       County Adjusted Municipal Boundaries to Counties append completed"
write_log("       County Adjusted Municipal Boundaries to Counties append completed", logfile)

try:
    # Delete **Delete Files** feature dataset to save room (temporary files aren't needed for step 2 of process and take up additional room on file server when archiving prior exports)
    arcpy.Delete_management(DELETE_FILES)
    print ("\n Delete Files feature dataset has been deleted")
except:
    print ("\n Unable to delete **Delete Files** feature dataset")
    write_log("Unable to delete **Delete Files** feature dataset", logfile)
    logging.exception('Got exception on delete **Delete Files** feature dataset logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print "\n==================================================================="
print "Northern Tier CAD Data Export to local staging DB completed: " + str(Day) + " " + str(end_time)
print time.strftime("\n %H:%M:%S", time.gmtime(elapsed_time))
print "==================================================================="
write_log("\n Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)

print "\n                   Northern Tier CAD Data Export to local staging DB completed // Connect Elk County VPN and run STEP 2 to process to Elk Staging DB"
print "\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+"
write_log("\n                   Northern Tier CAD Data Export to local staging DB completed // Connect Elk County VPN and run STEP 2 to process to Elk Staging DB", logfile)
write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+", logfile)

del arcpy
sys.exit()


