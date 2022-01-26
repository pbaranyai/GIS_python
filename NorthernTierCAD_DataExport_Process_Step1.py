# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NortherTierCAD_DataExport_Process - Step 1.py
#  
# Description: 
# This tool will create a FGDB (Northern_Tier_County_Data_YYYYMMDD.gdb), then process local Crawford County Data into the schema required for
# the usage of the Northern Tier CAD.  It will also copy the Northern_Tier_County_Data_YYYYMMDD.gdb into PA_NG911_Export_YYYYMMDD.gdb, and alter the data to meet NG911 standards)  
#
# After this tool is completed, you must connect to the Elk Co. VPN to run the next step
#
# STEP 1 of 2
# Author: Phil Baranyai/Crawford County GIS Manager
# Created on: 2019-02-28 
# Updated on 2021-12-09
# Works in ArcGIS Pro
# ---------------------------------------------------------------------------

import sys
import arcpy
import datetime
import os
import traceback
import logging

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"\\CCFILE\\anybody\\GIS\\GIS_LOGS\\911\\NorthernTierCAD_DataExport.log"  # Run Log
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

# Define Work Paths for FGDB:
NORTHERN_TIER_CAD_FLDR = r"\\CCFILE\\anybody\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier"
NORTHERN_TIER_COUNTY_DATA_XML = r"\\CCFILE\\anybody\\GIS\\NorthernTierCAD_GIS\\XML_Workspace\\NORTHERN_TIER_COUNTY_DATA.XML"
NORTHERN_TIER_CAD_FGDB_OLD = NORTHERN_TIER_CAD_FLDR+ "\\Northern_Tier_County_Data_YYYYMMDD.gdb"
PA_NG911_EXPORT_FLDR = r"\\CCFILE\\anybody\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier\\PA_NG911_Exports"
PA_NG911_EXPORT_FGDB_OLD = PA_NG911_EXPORT_FLDR + "\\PA_NG911_Export_YYYYMMDD.gdb"

start_time = time.time()

print ("=====================================================================================================================")
print ("Checking for existing NorthernTier FGDB & PA_NG911 FGDB, delete and rebuild fresh if exists.")
print ("Works in ArcGIS Pro")
print ("=====================================================================================================================")

write_log("=====================================================================================================================", logfile)
write_log("\n Checking for existing NorthernTier FGDB & PA_NG911 FGDB, delete and rebuild fresh if exists.", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("=====================================================================================================================", logfile)

try:
    # Pre-clean old FGDBs, if exists (if old Northern_Tier_County_Data_YYYYMMDD.gdb or PA_NG911_Export_YYYYMMDD.gdb exists and was never renamed, the program will delete it, so it will be able to run without failure, henceforth providing the newest data)
    if arcpy.Exists(NORTHERN_TIER_CAD_FGDB_OLD):
        arcpy.Delete_management(NORTHERN_TIER_CAD_FGDB_OLD, "Workspace")
        print ("Northern_Tier_County_Data_YYYYMMDD.gdb found - FGDB deleted")
        write_log("Northern_Tier_County_Data_YYYYMMDD.gdb found - FGDB deleted", logfile)
    if arcpy.Exists(PA_NG911_EXPORT_FGDB_OLD):
        arcpy.Delete_management(PA_NG911_EXPORT_FGDB_OLD, "Workspace")
        print ("PA_NG911_Export_YYYYMMDD.gdb found - FGDB deleted")
        write_log("PA_NG911_Export_YYYYMMDD.gdb found - FGDB deleted", logfile)
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

#Database Connection Folder
Database_Connections = r"\\CCFILE\\anybody\\GIS\\ArcAutomations\\Database_Connections"

# Define Work Paths for Databases:
NORTHERN_TIER_CAD_FLDR = r"R:\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier"
NORTHERN_TIER_CAD_FGDB = NORTHERN_TIER_CAD_FLDR + "\\Northern_Tier_County_Data_YYYYMMDD.gdb"
NORTHERN_TIER_CAD_FGDB_CC = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County"
DELETE_FILES = NORTHERN_TIER_CAD_FGDB + "\\DELETE_FILES"
PUBLIC_SAFETY_DB = Database_Connections + "\\PUBLIC_SAFETY@ccsde.sde"

print ("Importing XML workspace to Northern Tier FGDB for schema structure")
write_log("Importing XML workspace to Northern Tier FGDB for schema structure", logfile)

try:
    # Import XML Workspace for NT FGDB Schema (if the Northern Tier GIS sub-committee agrees to more changes, this XML will need to be updated)
    arcpy.ImportXMLWorkspaceDocument_management(NORTHERN_TIER_CAD_FGDB, NORTHERN_TIER_COUNTY_DATA_XML, "SCHEMA_ONLY", "")
    print ("Northern_Tier_County_Data_YYYYMMDD FGDB schema import completed")
except:
    print ("\n Unable to import XML workspace file")
    write_log("Unable to import XML workspace file", logfile)
    logging.exception('Got exception on import XML workspace file')
    raise
    sys.exit ()

# Local variables:
ADDRESS_POINTS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.Site_Structure_Address_Points_INTERNAL"
ALS_ZONES_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL"
BLS_COVERAGE_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.BLS_COVERAGE_INTERNAL"
COUNTY_ADJ_MUNI_BOUND_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.COUNTY_ADJ_MUNI_BOUND_INTERNAL"
ESZ_PS = PUBLIC_SAFETY_DB + "\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ESZ_ALL"
FIRE_DEPT_COVERAGE_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.FIRE_DEPT_COVERAGE_INTERNAL"
FIRE_GRIDS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.FIRE_GRIDS_INTERNAL"
HYDRANTS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Utilities\\CRAW_INTERNAL.HYDRANTS"
LANDMARKS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.LANDMARKS_INTERNAL"
MILE_MARKERS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.MILE_MARKERS_INTERNAL"
POLICE_DEPT_COVERAGE_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL"
RAILROADS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Transportation\\CCSDE.CRAW_INTERNAL.RAILROADS_INTERNAL"
STREET_CENTERLINE_PS = PUBLIC_SAFETY_DB + "\\CCSDE.PUBLIC_SAFETY.Street_Centerlines"
STREET_CENTERLINE = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.Street_Centerlines_INTERNAL"
TAX_PARCELS_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.TAX_PARCELS_INTERNAL"
ZIPCODES_INTERNAL = PUBLIC_SAFETY_DB + "\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL"
NORTHERN_TIER_COUNTY_DATA_XML = "R:\\GIS\\NorthernTierCAD_GIS\\XML_Workspace\\NORTHERN_TIER_COUNTY_DATA.XML"

###Layer Files
COUNTY_ADJ_MUNI_LAYER = "COUNTY_ADJ_MUNI_LAYER"
FIRE_DEPT_COVERAGE_INTERNAL_LYR = "FIRE_DEPT_COVERAGE_INTERNAL_LYR"
STREET_CENTERLINE_Layer = "CL_Zipcode_JOIN_DELETE_Layer"

###Temporary variables
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
Trails_CrawfordCo = NORTHERN_TIER_CAD_FGDB_CC + "\\Trails_CrawfordCo"

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
    arcpy.management.Append(ADDRESS_POINTS_INTERNAL, NTAddressPoint_CrawfordCo, "NO_TEST", r'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',DiscrpAgID,0,75;DateUpdate "DateUpdate" true true false 8 Date 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',DateUpdate,-1,-1;Effective "Effective" true true false 8 Date 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Effective,-1,-1;Expire "Expire" true true false 8 Date 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Expire,-1,-1;Site_NGUID "Site_NGUID" true true false 254 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Site_NGUID,0,254;Country "Country" true true false 2 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Country,0,2;State "State" true true false 2 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',State,0,2;County "County" true true false 40 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',CountyName,0,50;AddCode "AddCode" true true false 506 Text 0 0,First,#;AddDataURI "AddDataURI" true true false 254 Text 0 0,First,#;Inc_Muni "Inc_Muni" true true false 100 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Inc_Muni,0,100;Uninc_Comm "Uninc_Comm" true true false 100 Text 0 0,First,#;Nbrhd_Comm "Nbrhd_Comm" true true false 100 Text 0 0,First,#;AddNum_Pre "AddNum_Pre" true true false 50 Text 0 0,First,#;Add_Number "Add_Number" true true false 4 Long 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Add_Number,-1,-1;AddNum_Suf "AddNum_Suf" true true false 15 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',AddNum_Suf,0,15;St_PreMod "St_PreMod" true true false 15 Text 0 0,First,#;St_PreDir "ST_PreDir" true true false 9 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',St_PreDir,0,9;St_PreTyp "St_PreTyp" true true false 50 Text 0 0,First,#;St_PreSep "St_PreSep" true true false 20 Text 0 0,First,#;St_Name "St_Name" true true false 60 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',St_Name,0,60;St_PosTyp "St_PosTyp" true true false 50 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',St_PosTyp,0,50;St_PosDir "St_PosDir" true true false 9 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',St_PosDir,0,9;St_PosMod "St_PosMod" true true false 25 Text 0 0,First,#;LSt_PreDir "LSt_PreDir" true true false 2 Text 0 0,First,#;LSt_Name "LSt_Name" true true false 75 Text 0 0,First,#;LSt_Type "LSt_Type" true true false 4 Text 0 0,First,#;LStPosDir "LStPosDir" true true false 2 Text 0 0,First,#;ESN "ESN" true true false 5 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',ESN,-1,-1;MSAGComm "MSAGComm" true true false 30 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Inc_Muni,0,100;Post_Comm "Post_Comm" true true false 40 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Post_Comm,0,40;Post_Code "Post_Code" true true false 7 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Post_Code,0,255;Post_Code4 "Post_Code4" true true false 4 Text 0 0,First,#;Building "Building" true true false 75 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Building,0,75;Floor "Floor" true true false 75 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Floor,0,75;Unit "Unit" true true false 75 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Unit,0,75;Room "Room" true true false 75 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Room,0,75;Seat "Seat" true true false 75 Text 0 0,First,#;Addtl_Loc "Addtl_Loc" true true false 225 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',AddNum_Suf,0,15;LandmkName "LandmkName" true true false 150 Text 0 0,First,#;Mile_Post "Mile_Post" true true false 150 Text 0 0,First,#;Place_Type "Place_Type" true true false 50 Text 0 0,First,#;Placement "Placement" true true false 25 Text 0 0,First,#;Long "Long" true true false 8 Double 0 0,First,#;Lat "Lat" true true false 8 Double 0 0,First,#;Elev "Elev" true true false 4 Long 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',Elevation,-1,-1;JOIN_ID "JOIN_ID" true true false 4 Long 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',UniqueStructureNumber,-1,-1;FullName "FullName" true true false 80 Text 0 0,First,#,'+ADDRESS_POINTS_INTERNAL+',FullAddress,0,200', '', '')
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
    arcpy.analysis.SpatialJoin(STREET_CENTERLINE, ZIPCODES_INTERNAL, CL_Zipcode_JOIN_DELETE, "JOIN_ONE_TO_ONE", "KEEP_ALL", r'CL_UniqueID "Unique ID" true true false 4 Long 0 10,First,#,'+STREET_CENTERLINE+',CL_UniqueID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0,First,#,'+STREET_CENTERLINE+',DiscrpAgID,0,75;DateUpdate "Date record last updated" true true false 8 Date 0 0,First,#,'+STREET_CENTERLINE+',DateUpdate,-1,-1;DateAdded "Date record was added" true true false 8 Date 0 0,First,#,'+STREET_CENTERLINE+',DateAdded,-1,-1;RCL_NGUID "Road Centerline NENA Globaly Unique ID" true true false 254 Text 0 0,First,#,'+STREET_CENTERLINE+',RCL_NGUID,0,254;FromAddr_L "Left FROM Address" true true false 4 Long 0 10,First,#,'+STREET_CENTERLINE+',FromAddr_L,-1,-1;ToAddr_L "Left TO Address" true true false 4 Long 0 10,First,#,'+STREET_CENTERLINE+',ToAddr_L,-1,-1;FromAddr_R "Right FROM Address" true true false 4 Long 0 10,First,#,'+STREET_CENTERLINE+',FromAddr_R,-1,-1;ToAddr_R "Right TO Address" true true false 4 Long 0 10,First,#,'+STREET_CENTERLINE+',ToAddr_R,-1,-1;Parity_L "Parity Left" true true false 1 Text 0 0,First,#,'+STREET_CENTERLINE+',Parity_L,0,1;Parity_R "Parity Right" true true false 1 Text 0 0,First,#,'+STREET_CENTERLINE+',Parity_R,0,1;ParityAll "Parity of centerline segment" true true false 1 Text 0 0,First,#,'+STREET_CENTERLINE+',ParityAll,0,1;St_PreDir "Street Name Pre Directional" true true false 9 Text 0 0,First,#,'+STREET_CENTERLINE+',St_PreDir,0,9;St_Name "Street Name" true true false 60 Text 0 0,First,#,'+STREET_CENTERLINE+',St_Name,0,60;St_PostTyp "Street Name Post Type" true true false 50 Text 0 0,First,#,'+STREET_CENTERLINE+',St_PostTyp,0,50;St_PosDir "Street Name Post Directional" true true false 9 Text 0 0,First,#,'+STREET_CENTERLINE+',St_PosDir,0,9;St_FullName "Street Full Name" true true false 160 Text 0 0,First,#,'+STREET_CENTERLINE+',St_FullName,0,160;ESN_L "ESN Left" true true false 5 Text 0 0,First,#,'+STREET_CENTERLINE+',ESN_L,0,5;ESN_R "ESN Right" true true false 5 Text 0 0,First,#,'+STREET_CENTERLINE+',ESN_R,0,5;Country_L "Country Left" true true false 2 Text 0 0,First,#,'+STREET_CENTERLINE+',Country_L,0,2;Country_R "Country Right" true true false 2 Text 0 0,First,#,'+STREET_CENTERLINE+',Country_R,0,2;State_L "State Left" true true false 2 Text 0 0,First,#,'+STREET_CENTERLINE+',State_L,0,2;State_R "State Right" true true false 2 Text 0 0,First,#,'+STREET_CENTERLINE+',State_R,0,2;County_L "County Left" true true false 40 Text 0 0,First,#,'+STREET_CENTERLINE+',County_L,0,40;County_R "County Right" true true false 40 Text 0 0,First,#,'+STREET_CENTERLINE+',County_R,0,40;County_R_FIPS "County FIPS Code Right" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',County_R_FIPS,-1,-1;County_L_FIPS "County FIPS Code Left" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',County_L_FIPS,-1,-1;IncMuni "Incorporated Municipality" true true false 100 Text 0 0,First,#,'+STREET_CENTERLINE+',IncMuni,0,100;IncMuni_L "Incorporated Municipality Left" true true false 100 Text 0 0,First,#,'+STREET_CENTERLINE+',IncMuni_L,0,100;IncMuni_R "Incorporated Municipality Right" true true false 100 Text 0 0,First,#,'+STREET_CENTERLINE+',IncMuni_R,0,100;IncMuniFIPS_L "Incorporated Municipality FIPS Code Left" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',IncMuniFIPS_L,-1,-1;IncMuniFIPS_R "Incorporated Municipality FIPS Code Right" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',IncMuniFIPS_R,-1,-1;OneWay "One Way" true true false 2 Text 0 0,First,#,'+STREET_CENTERLINE+',OneWay,0,2;SpeedLimit "Speed Limit (MPH)" true true false 2 Short 0 5,First,#,'+STREET_CENTERLINE+',SpeedLimit,-1,-1;TF_RoutingCost "To-From Routing Cost" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',TF_RoutingCost,-1,-1;FT_RoutingCost "From-To Routing Cost" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',FT_RoutingCost,-1,-1;RouteNumber "Route Number" true true false 25 Text 0 0,First,#,'+STREET_CENTERLINE+',RouteNumber,0,25;LegislativeRouteNumber "Legislative Route Number" true true false 30 Text 0 0,First,#,'+STREET_CENTERLINE+',LegislativeRouteNumber,0,30;AddressCount "# of addresses assigned to segment" true true false 2 Short 0 5,First,#,'+STREET_CENTERLINE+',AddressCount,-1,-1;AddressRange "Address Range assigned to segment" true true false 15 Text 0 0,First,#,'+STREET_CENTERLINE+',AddressRange,0,15;Tile "Grid Tile ID" true true false 10 Text 0 0,First,#,'+STREET_CENTERLINE+',Tile,0,10;ZElev_F "Z Elevation From" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',ZElev_F,-1,-1;ZElev_T "Z Elevation To" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',ZElev_T,-1,-1;ConstructionStatus "Construction Status" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',ConstructionStatus,-1,-1;MaintenanceOwner "Maintenance Owner" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',MaintenanceOwner,-1,-1;SurfaceType "Surface Type" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',SurfaceType,-1,-1;WeightLimit "Weight Limit (Tons)" true true false 2 Short 0 5,First,#,'+STREET_CENTERLINE+',WeightLimit,-1,-1;HeightLimit "Height Limit (Feet)" true true false 2 Short 0 5,First,#,'+STREET_CENTERLINE+',HeightLimit,-1,-1;Divided "Is roadway divded?" true true false 1 Text 0 0,First,#,'+STREET_CENTERLINE+',Divided,0,1;OverWater "Is segment over water?" true true false 1 Text 0 0,First,#,'+STREET_CENTERLINE+',OverWater,0,1;InCounty "Is segment within Crawford County?" true true false 1 Text 0 0,First,#,'+STREET_CENTERLINE+',InCounty,0,1;CFCC "Census Feature Class Code" true true false 6 Text 0 0,First,#,'+STREET_CENTERLINE+',CFCC,0,6;MTFCC "Map/Tiger Feature Class Code" true true false 6 Text 0 0,First,#,'+STREET_CENTERLINE+',MTFCC,0,6;F_CrossStreet "FROM Cross Street" true true false 160 Text 0 0,First,#,'+STREET_CENTERLINE+',F_CrossStreet,0,160;T_CrossStreet "TO Cross Street" true true false 160 Text 0 0,First,#,'+STREET_CENTERLINE+',T_CrossStreet,0,160;UpdateCode "Update Code" true true false 8 Double 8 38,First,#,'+STREET_CENTERLINE+',UpdateCode,-1,-1;UpdateUser "UpdateUser" true true false 75 Text 0 0,First,#,'+STREET_CENTERLINE+',UpdateUser,0,75;RoadClass "Road Classification" true true false 255 Text 0 0,First,#,'+STREET_CENTERLINE+',RoadClass,0,255;GlobalID "GlobalID" false false false 38 GlobalID 0 0,First,#,'+STREET_CENTERLINE+',GlobalID,-1,-1;POST_OFFICE "POST OFFICE" true true false 50 Text 0 0,First,#,R:\GIS\ArcAutomations\Database_Connections\PUBLIC_SAFETY@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,POST_OFFICE,0,50;ZIPCODE "ZIPCODE" true true false 8 Double 8 38,First,#,R:\GIS\ArcAutomations\Database_Connections\PUBLIC_SAFETY@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,ZIPCODE,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0,First,#,R:\GIS\ArcAutomations\Database_Connections\PUBLIC_SAFETY@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,COUNTY_NAME,0,50;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38,First,#,R:\GIS\ArcAutomations\Database_Connections\PUBLIC_SAFETY@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE_DATE" true true false 8 Date 0 0,First,#,R:\GIS\ArcAutomations\Database_Connections\PUBLIC_SAFETY@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,UPDATE_DATE,-1,-1;GLOBALID_1 "GLOBALID" false false false 38 GlobalID 0 0,First,#,R:\GIS\ArcAutomations\Database_Connections\PUBLIC_SAFETY@ccsde.sde\CCSDE.CRAW_INTERNAL.Boundaries\CCSDE.CRAW_INTERNAL.ZIPCODES_INTERNAL,GLOBALID,-1,-1', "HAVE_THEIR_CENTER_IN", None, '')
except:
    print ("\n Unable to Spatial Join CL and Zipcode - creating CL_Zipcode_JOIN_DELETE")
    write_log("Unable to Spatial Join CL and Zipcode - creating CL_Zipcode_JOIN_DELETE", logfile)
    logging.exception('Got exception on Spatial Join CL and Zipcode - creating CL_Zipcode_JOIN_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Make Feature Layer -- STREET_CENTERLINE_Layer (make a temporary layer of centerline, to manipulate in steps below)
    arcpy.management.MakeFeatureLayer(CL_Zipcode_JOIN_DELETE, STREET_CENTERLINE_Layer, "ConstructionStatus <> 1", None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Join_Count Join_Count VISIBLE NONE;TARGET_FID TARGET_FID VISIBLE NONE;CL_UniqueID CL_UniqueID VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;DateUpdate DateUpdate VISIBLE NONE;DateAdded DateAdded VISIBLE NONE;RCL_NGUID RCL_NGUID VISIBLE NONE;FromAddr_L FromAddr_L VISIBLE NONE;ToAddr_L ToAddr_L VISIBLE NONE;FromAddr_R FromAddr_R VISIBLE NONE;ToAddr_R ToAddr_R VISIBLE NONE;Parity_L Parity_L VISIBLE NONE;Parity_R Parity_R VISIBLE NONE;ParityAll ParityAll VISIBLE NONE;St_PreDir St_PreDir VISIBLE NONE;St_Name St_Name VISIBLE NONE;St_PostTyp St_PostTyp VISIBLE NONE;St_PosDir St_PosDir VISIBLE NONE;St_FullName St_FullName VISIBLE NONE;ESN_L ESN_L VISIBLE NONE;ESN_R ESN_R VISIBLE NONE;Country_L Country_L VISIBLE NONE;Country_R Country_R VISIBLE NONE;State_L State_L VISIBLE NONE;State_R State_R VISIBLE NONE;County_L County_L VISIBLE NONE;County_R County_R VISIBLE NONE;County_R_FIPS County_R_FIPS VISIBLE NONE;County_L_FIPS County_L_FIPS VISIBLE NONE;IncMuni IncMuni VISIBLE NONE;IncMuni_L IncMuni_L VISIBLE NONE;IncMuni_R IncMuni_R VISIBLE NONE;IncMuniFIPS_L IncMuniFIPS_L VISIBLE NONE;IncMuniFIPS_R IncMuniFIPS_R VISIBLE NONE;OneWay OneWay VISIBLE NONE;SpeedLimit SpeedLimit VISIBLE NONE;TF_RoutingCost TF_RoutingCost VISIBLE NONE;FT_RoutingCost FT_RoutingCost VISIBLE NONE;RouteNumber RouteNumber VISIBLE NONE;LegislativeRouteNumber LegislativeRouteNumber VISIBLE NONE;AddressCount AddressCount VISIBLE NONE;AddressRange AddressRange VISIBLE NONE;Tile Tile VISIBLE NONE;ZElev_F ZElev_F VISIBLE NONE;ZElev_T ZElev_T VISIBLE NONE;ConstructionStatus ConstructionStatus VISIBLE NONE;MaintenanceOwner MaintenanceOwner VISIBLE NONE;SurfaceType SurfaceType VISIBLE NONE;WeightLimit WeightLimit VISIBLE NONE;HeightLimit HeightLimit VISIBLE NONE;Divided Divided VISIBLE NONE;OverWater OverWater VISIBLE NONE;InCounty InCounty VISIBLE NONE;CFCC CFCC VISIBLE NONE;MTFCC MTFCC VISIBLE NONE;F_CrossStreet F_CrossStreet VISIBLE NONE;T_CrossStreet T_CrossStreet VISIBLE NONE;UpdateCode UpdateCode VISIBLE NONE;UpdateUser UpdateUser VISIBLE NONE;RoadClass RoadClass VISIBLE NONE;POST_OFFICE POST_OFFICE VISIBLE NONE;ZIPCODE ZIPCODE VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;UPDATE_DATE UPDATE_DATE VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE")
except:
    print ("\n Unable to Make Feature Layer -- STREET_CENTERLINE_Layer - Calc ALL COSTS to FT COST FIELD")
    write_log("Unable to Make Feature Layer -- STREET_CENTERLINE_Layer - Calc ALL COSTS to FT COST FIELD", logfile)
    logging.exception('Got exception on Make Feature Layer -- STREET_CENTERLINE_Layer - Calc ALL COSTS to FT COST FIELD logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calc ALL COSTS to FT COST FIELD (iterate through centerline layer file, calculate any costs from the TF_COST field over to the FT cost field if the One way is TF, otherwise the correct cost already exists in the FT cost field - which will be calculated in append in steps below)
    CENTERLINE_FIELDS = ['OneWay', 'FT_RoutingCost', 'TF_RoutingCost']
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
    arcpy.conversion.FeatureClassToFeatureClass(STREET_CENTERLINE_Layer, DELETE_FILES, "STREET_CENTERLINE_Layer_OUTPUT", '', 'Join_Count "Join_Count" true true false 4 Long 0 0,First,#,STREET_CENTERLINE_Layer,Join_Count,-1,-1;TARGET_FID "TARGET_FID" true true false 4 Long 0 0,First,#,STREET_CENTERLINE_Layer,TARGET_FID,-1,-1;CL_UniqueID "Unique ID" true true false 4 Long 0 0,First,#,STREET_CENTERLINE_Layer,CL_UniqueID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0,First,#,STREET_CENTERLINE_Layer,DiscrpAgID,0,75;DateUpdate "Date record last updated" true true false 8 Date 0 0,First,#,STREET_CENTERLINE_Layer,DateUpdate,-1,-1;DateAdded "Date record was added" true true false 8 Date 0 0,First,#,STREET_CENTERLINE_Layer,DateAdded,-1,-1;RCL_NGUID "Road Centerline NENA Globaly Unique ID" true true false 254 Text 0 0,First,#,STREET_CENTERLINE_Layer,RCL_NGUID,0,254;FromAddr_L "Left FROM Address" true true false 4 Long 0 0,First,#,STREET_CENTERLINE_Layer,FromAddr_L,-1,-1;ToAddr_L "Left TO Address" true true false 4 Long 0 0,First,#,STREET_CENTERLINE_Layer,ToAddr_L,-1,-1;FromAddr_R "Right FROM Address" true true false 4 Long 0 0,First,#,STREET_CENTERLINE_Layer,FromAddr_R,-1,-1;ToAddr_R "Right TO Address" true true false 4 Long 0 0,First,#,STREET_CENTERLINE_Layer,ToAddr_R,-1,-1;Parity_L "Parity Left" true true false 1 Text 0 0,First,#,STREET_CENTERLINE_Layer,Parity_L,0,1;Parity_R "Parity Right" true true false 1 Text 0 0,First,#,STREET_CENTERLINE_Layer,Parity_R,0,1;ParityAll "Parity of centerline segment" true true false 1 Text 0 0,First,#,STREET_CENTERLINE_Layer,ParityAll,0,1;St_PreDir "Street Name Pre Directional" true true false 9 Text 0 0,First,#,STREET_CENTERLINE_Layer,St_PreDir,0,9;St_Name "Street Name" true true false 60 Text 0 0,First,#,STREET_CENTERLINE_Layer,St_Name,0,60;St_PostTyp "Street Name Post Type" true true false 50 Text 0 0,First,#,STREET_CENTERLINE_Layer,St_PostTyp,0,50;St_PosDir "Street Name Post Directional" true true false 9 Text 0 0,First,#,STREET_CENTERLINE_Layer,St_PosDir,0,9;St_FullName "Street Full Name" true true false 160 Text 0 0,First,#,STREET_CENTERLINE_Layer,St_FullName,0,160;ESN_L "ESN Left" true true false 5 Text 0 0,First,#,STREET_CENTERLINE_Layer,ESN_L,0,5;ESN_R "ESN Right" true true false 5 Text 0 0,First,#,STREET_CENTERLINE_Layer,ESN_R,0,5;Country_L "Country Left" true true false 2 Text 0 0,First,#,STREET_CENTERLINE_Layer,Country_L,0,2;Country_R "Country Right" true true false 2 Text 0 0,First,#,STREET_CENTERLINE_Layer,Country_R,0,2;State_L "State Left" true true false 2 Text 0 0,First,#,STREET_CENTERLINE_Layer,State_L,0,2;State_R "State Right" true true false 2 Text 0 0,First,#,STREET_CENTERLINE_Layer,State_R,0,2;County_L "County Left" true true false 40 Text 0 0,First,#,STREET_CENTERLINE_Layer,County_L,0,40;County_R "County Right" true true false 40 Text 0 0,First,#,STREET_CENTERLINE_Layer,County_R,0,40;County_R_FIPS "County FIPS Code Right" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,County_R_FIPS,-1,-1;County_L_FIPS "County FIPS Code Left" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,County_L_FIPS,-1,-1;IncMuni "Incorporated Municipality" true true false 100 Text 0 0,First,#,STREET_CENTERLINE_Layer,IncMuni,0,100;IncMuni_L "Incorporated Municipality Left" true true false 100 Text 0 0,First,#,STREET_CENTERLINE_Layer,IncMuni_L,0,100;IncMuni_R "Incorporated Municipality Right" true true false 100 Text 0 0,First,#,STREET_CENTERLINE_Layer,IncMuni_R,0,100;IncMuniFIPS_L "Incorporated Municipality FIPS Code Left" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,IncMuniFIPS_L,-1,-1;IncMuniFIPS_R "Incorporated Municipality FIPS Code Right" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,IncMuniFIPS_R,-1,-1;OneWay "One Way" true true false 2 Text 0 0,First,#,STREET_CENTERLINE_Layer,OneWay,0,2;SpeedLimit "Speed Limit (MPH)" true true false 2 Short 0 0,First,#,STREET_CENTERLINE_Layer,SpeedLimit,-1,-1;TF_RoutingCost "To-From Routing Cost" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,TF_RoutingCost,-1,-1;FT_RoutingCost "From-To Routing Cost" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,FT_RoutingCost,-1,-1;RouteNumber "Route Number" true true false 25 Text 0 0,First,#,STREET_CENTERLINE_Layer,RouteNumber,0,25;LegislativeRouteNumber "Legislative Route Number" true true false 30 Text 0 0,First,#,STREET_CENTERLINE_Layer,LegislativeRouteNumber,0,30;AddressCount "# of addresses assigned to segment" true true false 2 Short 0 0,First,#,STREET_CENTERLINE_Layer,AddressCount,-1,-1;AddressRange "Address Range assigned to segment" true true false 15 Text 0 0,First,#,STREET_CENTERLINE_Layer,AddressRange,0,15;Tile "Grid Tile ID" true true false 10 Text 0 0,First,#,STREET_CENTERLINE_Layer,Tile,0,10;ZElev_F "Z Elevation From" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,ZElev_F,-1,-1;ZElev_T "Z Elevation To" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,ZElev_T,-1,-1;ConstructionStatus "Construction Status" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,ConstructionStatus,-1,-1;MaintenanceOwner "Maintenance Owner" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,MaintenanceOwner,-1,-1;SurfaceType "Surface Type" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,SurfaceType,-1,-1;WeightLimit "Weight Limit (Tons)" true true false 2 Short 0 0,First,#,STREET_CENTERLINE_Layer,WeightLimit,-1,-1;HeightLimit "Height Limit (Feet)" true true false 2 Short 0 0,First,#,STREET_CENTERLINE_Layer,HeightLimit,-1,-1;Divided "Is roadway divded?" true true false 1 Text 0 0,First,#,STREET_CENTERLINE_Layer,Divided,0,1;OverWater "Is segment over water?" true true false 1 Text 0 0,First,#,STREET_CENTERLINE_Layer,OverWater,0,1;InCounty "Is segment within Crawford County?" true true false 1 Text 0 0,First,#,STREET_CENTERLINE_Layer,InCounty,0,1;CFCC "Census Feature Class Code" true true false 6 Text 0 0,First,#,STREET_CENTERLINE_Layer,CFCC,0,6;MTFCC "Map/Tiger Feature Class Code" true true false 6 Text 0 0,First,#,STREET_CENTERLINE_Layer,MTFCC,0,6;F_CrossStreet "FROM Cross Street" true true false 160 Text 0 0,First,#,STREET_CENTERLINE_Layer,F_CrossStreet,0,160;T_CrossStreet "TO Cross Street" true true false 160 Text 0 0,First,#,STREET_CENTERLINE_Layer,T_CrossStreet,0,160;UpdateCode "Update Code" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,UpdateCode,-1,-1;UpdateUser "UpdateUser" true true false 75 Text 0 0,First,#,STREET_CENTERLINE_Layer,UpdateUser,0,75;RoadClass "Road Classification" true true false 255 Text 0 0,First,#,STREET_CENTERLINE_Layer,RoadClass,0,255;POST_OFFICE "POST OFFICE" true true false 50 Text 0 0,First,#,STREET_CENTERLINE_Layer,POST_OFFICE,0,50;ZIPCODE "ZIPCODE" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,ZIPCODE,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0,First,#,STREET_CENTERLINE_Layer,COUNTY_NAME,0,50;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE_DATE" true true false 8 Date 0 0,First,#,STREET_CENTERLINE_Layer,UPDATE_DATE,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0,First,#,STREET_CENTERLINE_Layer,Shape_Length,-1,-1', '')
except:
    print ("\n Unable to Output STREET_CENTERLINE_Layer to DELETE_FILE, to append to Centerline_CrawfordCo - Northern Tier FGDB")
    write_log("Unable to Output STREET_CENTERLINE_Layer to DELETE_FILE, to append to Centerline_CrawfordCo - Northern Tier FGDB", logfile)
    logging.exception('Got exception on Output STREET_CENTERLINE_Layer to DELETE_FILE, to append to Centerline_CrawfordCo - Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append STREET_CENTERLINE_Layer to Centerline_CrawfordCo - Northern Tier FGDB (append Crawford centerline to staging FGDB created in steps above)
    arcpy.management.Append(STREET_CENTERLINE_Layer_OUTPUT, Centerline_CrawfordCo, "NO_TEST", r'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',DiscrpAgID,0,75;DateUpdate "DateUpdate" true true false 8 Date 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',DateUpdate,-1,-1;Effective "Effective" true true false 8 Date 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',DateAdded,-1,-1;Expire "Expire" true true false 8 Date 0 0,First,#;RCL_NGUID "RCL_NGUID" true true false 254 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',RCL_NGUID,0,254;AdNumPre_L "AdNumPre_L" true true false 15 Text 0 0,First,#;AdNumPre_R "AdNumPre_R" true true false 15 Text 0 0,First,#;FromAddr_L "FromAddr_L" true true false 4 Long 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',FromAddr_L,-1,-1;ToAddr_L "ToAddr_L" true true false 4 Long 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',ToAddr_L,-1,-1;FromAddr_R "FromAddr_R" true true false 4 Long 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',FromAddr_R,-1,-1;ToAddr_R "ToAddr_R" true true false 4 Long 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',ToAddr_R,-1,-1;Parity_L "Parity_L" true true false 1 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',Parity_L,0,1;Parity_R "Parity_R" true true false 1 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',Parity_R,0,1;St_PreMod "St_PreMod" true true false 15 Text 0 0,First,#;St_PreDir "St_PreDir" true true false 9 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',St_PreDir,0,9;St_PreTyp "St_PreTyp" true true false 50 Text 0 0,First,#;St_PreSep "St_PreSep" true true false 20 Text 0 0,First,#;St_Name "St_Name" true true false 60 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',St_Name,0,60;St_PosTyp "St_PosTyp" true true false 50 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',St_PostTyp,0,50;St_PosDir "St_PosDir" true true false 9 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',St_PosDir,0,9;St_PosMod "St_PosMod" true true false 25 Text 0 0,First,#;LSt_PreDir "LSt_PreDir" true true false 2 Text 0 0,First,#;LSt_Name "LSt_Name" true true false 75 Text 0 0,First,#;LSt_Type "LSt_Type" true true false 4 Text 0 0,First,#;LStPosDir "LStPosDir" true true false 2 Text 0 0,First,#;ESN_L "ESN_L" true true false 5 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',ESN_L,0,5;ESN_R "ESN_R" true true false 5 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',ESN_R,0,5;MSAGComm_L "MSAGComm_L" true true false 30 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',IncMuni_L,0,100;MSAGComm_R "MSAGComm_R" true true false 30 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',IncMuni_R,0,100;Country_L "Country_L" true true false 2 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',Country_L,0,2;Country_R "Country_R" true true false 2 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',Country_R,0,2;State_L "State_L" true true false 2 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',State_L,0,2;State_R "State_R" true true false 2 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',State_R,0,2;County_L "County_L" true true false 40 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',County_L,0,40;County_R "County_R" true true false 40 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',County_R,0,40;AddCode_L "AddCode_L" true true false 6 Text 0 0,First,#;AddCode_R "AddCode_R" true true false 6 Text 0 0,First,#;IncMuni_L "IncMuni_L" true true false 100 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',IncMuni_L,0,100;IncMuni_R "IncMuni_R" true true false 100 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',IncMuni_R,0,100;UnincCom_L "UnicCom_L" true true false 100 Text 0 0,First,#;UnincCom_R "Uninc" true true false 100 Text 0 0,First,#;NbrhdCom_L "NbrhdCom_L" true true false 100 Text 0 0,First,#;NbrhdCom_R "NbrhdCom_R" true true false 100 Text 0 0,First,#;PostCode_L "PostCode_L" true true false 7 Text 0 0,First,#;PostCode_R "PostCode_R" true true false 7 Text 0 0,First,#;PostComm_L "PostComm_L" true true false 40 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',ZIPCODE,-1,-1;PostComm_R "PostComm_R" true true false 40 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',ZIPCODE,-1,-1;RoadClass "RoadClass" true true false 15 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',RoadClass,0,255;OneWay "OneWay" true true false 2 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',OneWay,0,2;SpeedLimit "SpeedLimit" true true false 2 Short 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',SpeedLimit,-1,-1;Valid_L "Valid_L" true true false 1 Text 0 0,First,#;Valid_R "Valid_R" true true false 1 Text 0 0,First,#;Time "Time" true true false 8 Double 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',FT_RoutingCost,-1,-1;Max_Height "Max_Height" true true false 8 Double 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',HeightLimit,-1,-1;Max_Weight "Max_Weight" true true false 8 Double 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',WeightLimit,-1,-1;T_ZLev "T_ZLev" true true false 2 Short 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',ZElev_T,-1,-1;F_ZLev "F_ZLev" true true false 2 Short 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',ZElev_F,-1,-1;JOIN_ID "JOIN_ID" true true false 4 Long 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',CL_UniqueID,-1,-1;FullName "FullName" true true false 80 Text 0 0,First,#,'+STREET_CENTERLINE_Layer_OUTPUT+',St_FullName,0,160', '', '')
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
Crawford_Road_Class = ["INTERSTATE", "RAMP", "MAJOR ARTERIAL", "MINOR ARTERIAL", "COLLECTOR", "LOCAL", "SERVICE", "4 WHEEL DRIVE", "RECREATION", "RESOURCE", "OTHER", "UNKNOWN", "MINOR COLLECTOR"]
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
    print ("\n Unable to Make Feature Layer_BLSResponse")
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
    print ("\n Unable to Intersect ALS Zones with BLS Coverage")
    write_log("Unable to Intersect ALS Zones with BLS Coverage", logfile)
    logging.exception('Got exception on Intersect ALS Zones with BLS Coverage logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Spatial Join - BLS Coverage Internal / ALS Zones Internal  (spatial join ALS to BLS, to get data from fields of both features)
    arcpy.SpatialJoin_analysis(Intersect_analysis_feature_output, ALS_ZONES_INTERNAL, DELETE_FILES + "//BLS_ALS_INTERSECT_Spatial_Join", "JOIN_ONE_TO_ONE", "KEEP_ALL", 'ALS_ID "ALS UNQUIE ID #" true true false 8 Double 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',ALS_ID,-1,-1;ALS_NAME "ALS SERVICE NAME" true true false 75 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',ALS_NAME,-1,-1;UPDATE_DATE "UPDATE DATE" true true false 8 Date 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',UPDATE_DATE,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',COUNTY_FIPS,-1,-1;FID_ALS_ZONES_INTERNAL "FID_ALS_ZONES_INTERNAL" true true false 4 Long 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',FID_ALS_ZONES_INTERNAL,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',DiscrpAgID_1,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',STATE_1,-1,-1;EMS_DEPT "BLS/EMS DEPARTMENT" true true false 50 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',EMS_DEPT,-1,-1;EMS_NUM "BLS/EMS DEPARTMENT #" true true false 10 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',EMS_NUM,-1,-1;EMS_EMSID "EMS ID CODE" true true false 10 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',EMS_EMSID,-1,-1;COUNTY_NAME_1 "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',COUNTY_NAME_1,-1,-1;COUNTY_FIPS_1 "COUNTY FIPS CODE" true true false 8 Double 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',COUNTY_FIPS_1,-1,-1;FID_BLS_COVERAGE_INTERNAL "FID_BLS_COVERAGE_INTERNAL" true true false 4 Long 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',FID_BLS_COVERAGE_INTERNAL,-1,-1;DiscrpAgID_1 "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',DiscrpAgID_1,-1,-1;STATE_1 "State" true true false 2 Text 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',STATE_1,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',SHAPE_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,'+ALS_JOIN_DELETE_Intersect_DELETE+',SHAPE_Area,-1,-1;ALS_ID_1 "ALS UNQUIE ID #" true true false 8 Double 8 38 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,ALS_ID,-1,-1;ALS_NAME_1 "ALS SERVICE NAME" true true false 75 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,ALS_NAME,-1,-1;UPDATE_DATE_1 "UPDATE DATE" true true false 8 Date 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,UPDATE_DATE,-1,-1;COUNTY_NAME_12 "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS_12 "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,COUNTY_FIPS,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,GLOBALID,-1,-1;DiscrpAgID_12 "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,DiscrpAgID,-1,-1;STATE_12 "State" true true false 2 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,STATE,-1,-1;SHAPE_STArea__ "SHAPE_STArea__" false false true 0 Double 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE_STLength__ "SHAPE_STLength__" false false true 0 Double 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL,SHAPE.STLength(),-1,-1', "HAVE_THEIR_CENTER_IN", "", "")
except:
    print ("\n Unable to Spatial Join - BLS Coverage Internal / ALS Zones Internal")
    write_log("Unable to Spatial Join - BLS Coverage Internal / ALS Zones Internal", logfile)
    logging.exception('Got exception on Spatial Join - BLS Coverage Internal / ALS Zones Internal logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Add Description Field to EMSDistricts
    arcpy.AddField_management(BLS_ALS_INTERSECT_Spatial_Join, "Description", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print ("\n Unable to Add Description Field to EMSDistricts")
    write_log("Unable to Add Description Field to EMSDistricts", logfile)
    logging.exception('Got exception on Add Description Field to EMSDistricts logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Add ID Field to EMSDistricts
    arcpy.AddField_management(BLS_ALS_INTERSECT_Spatial_Join, "ID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print ("\n Unable to Add ID Field to EMSDistricts")
    write_log("Unable to Add ID Field to EMSDistricts", logfile)
    logging.exception('Got exception on Add ID Field to EMSDistricts logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Add ID_TEMP Field to EMSDistricts (ID is source data is text format, need to calculate into integer, temp field added)
    arcpy.AddField_management(BLS_ALS_INTERSECT_Spatial_Join, "ID_TEMP", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print ("\n Unable to Add ID_TEMP Field to EMSDistricts")
    write_log("Unable to Add ID_TEMP Field to EMSDistricts", logfile)
    logging.exception('Got exception on Add ID_TEMP Field to EMSDistricts logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Calculate Field - EMSDistricts Description (calculate first 12 digits of ALS_NAME - EMS_NUM into field)
    arcpy.CalculateField_management(BLS_ALS_INTERSECT_Spatial_Join, "Description", '"{} - {}".format(!ALS_NAME![0:12], !EMS_NUM!)', "PYTHON", "")
except:
    print ("\n Unable to Calculate Field - EMSDistricts Description")
    write_log("Unable to Calculate Field - EMSDistricts Description", logfile)
    logging.exception('Got exception on Unable to Calculate Field - EMSDistricts Description logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calculate Field - EMSDistricts ID_TEMP
    arcpy.CalculateField_management(BLS_ALS_INTERSECT_Spatial_Join, "ID_TEMP",'!ALS_ID!', "PYTHON", "")
except:
    print ("\n Unable to Calculate Field - EMSDistricts ID_TEMP")
    write_log("Unable to Calculate Field - EMSDistricts ID_TEMP", logfile)
    logging.exception('Got exception on Unable to Calculate Field - EMSDistricts ID_TEMP logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()


try:
    # Calculate Field - EMSDistricts ID (calculate 2 + the last 5 digits of ID_TEMP + EMS_ID)
    arcpy.CalculateField_management(BLS_ALS_INTERSECT_Spatial_Join, "ID", '"2"+str(!ID_TEMP!)[5:]+str(!EMS_EMSID!)', "PYTHON", "")
except:
    print ("\n Unable to Calculate Field - EMSDistricts ID")
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
    print ("\n Unable to Append BLS_ALS_INTERSECT_Spatial_Join to EMS Districts to Northern Tier FGDB")
    write_log("Unable to Append BLS_ALS_INTERSECT_Spatial_Join to EMS Districts to Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append BLS_ALS_INTERSECT_Spatial_Join to EMS Districts to Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("       BLS-ALS Coverage to EMS Districts append completed")
write_log("       BLS-ALS Coverage to EMS Districts append completed", logfile)


print ("\n Append Fire Department Coverage from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Append Fire Department Coverage from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Fire Dept Coverage to Delete Files (create temporary fire dept feature in delete files FDS for manipulation into fire dept for CAD)
    arcpy.FeatureClassToFeatureClass_conversion(FIRE_DEPT_COVERAGE_INTERNAL, DELETE_FILES, "FIRE_DEPT_COVERAGE_DELETE", "", 'FIRE_DEPT "FIRE DEPARTMENT" true true false 50 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',FIRE_DEPT,-1,-1;FIRE_FDID "FIRE DEPARTMENT FDID CODE" true true false 15 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',FIRE_FDID,-1,-1;FIRE_NUM "FIRE DEPARTMENT #" true true false 10 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',FIRE_NUM,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',COUNTY_FIPS,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',GLOBALID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',STATE,-1,-1;SHAPE_STArea__ "SHAPE_STArea__" false false true 0 Double 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',SHAPE.STArea(),-1,-1;SHAPE_STLength__ "SHAPE_STLength__" false false true 0 Double 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',SHAPE.STLength(),-1,-1', "")
except:
    print ("\n Unable to export Fire Dept Coverage to Delete Files")
    write_log("Unable to export Fire Dept Coverage to Delete Files", logfile)
    logging.exception('Got exception on export Fire Dept Coverage to Delete Files logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Add ID Field to FireDept_COVERAGE_DELETE
    arcpy.AddField_management(FIRE_DEPT_COVERAGE_DELETE, "ID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print ("\n Unable to Add ID Field to FireDept_COVERAGE_DELETE")
    write_log("Unable to Add ID Field to FireDept_COVERAGE_DELETE", logfile)
    logging.exception('Got exception on Add ID Field to FireDept_COVERAGE_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
   
try:
    # Calculate ID Field FIRE_DEPT_COVERAGE_DELETE (calculate 20+FIRE_FDID into field)
    arcpy.CalculateField_management(FIRE_DEPT_COVERAGE_DELETE, "ID", '"20"+ !FIRE_FDID!', "PYTHON", "")
except:
    print ("\n Unable to Calculate ID Field FIRE_DEPT_COVERAGE_DELETE")
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
    print ("\n Unable to Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to Northern Tier FGDB")
    write_log("Unable to Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
   
print ("       Fire Department Coverage to Fire Department append completed")
write_log("       Fire Department Coverage to Fire Department append completed", logfile)


print ("\n Process Fire Department Coverage & Fire Grids from CRAW_INTERNAL as Fire Response and append to Northern Tier FGDB")
write_log("\n Process Fire Department Coverage & Fire Grids from CRAW_INTERNAL as Fire Response and append to Northern Tier FGDB", logfile)

try:
    # Make Feature Layer from Fire Department Internal (create temporary fire dept layer for manipulation into fire response for CAD)
    FIRE_DEPT_COVERAGE_INTERNAL_LYR = arcpy.MakeFeatureLayer_management(FIRE_DEPT_COVERAGE_INTERNAL, "FIRE_DEPT_COVERAGE_INTERNAL_LYR", "", "", "FIRE_DEPT FIRE_DEPT VISIBLE NONE;FIRE_FDID FIRE_FDID VISIBLE NONE;FIRE_NUM FIRE_NUM VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;GLOBALID GLOBALID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;STATE STATE VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print ("\n Unable to Make Feature Layer from Fire Department Internal")
    write_log("Unable to Make Feature Layer from Fire Department Internal", logfile)
    logging.exception('Got exception on Make Feature Layer from Fire Department Internal logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Spatial Join Fire Dept Internal Layer and Fire Grids (spatial join fire dept coverage and fire grids, to break up fire departments into grid sized areas)
    arcpy.SpatialJoin_analysis(FIRE_GRIDS_INTERNAL, FIRE_DEPT_COVERAGE_INTERNAL_LYR, FIRE_GRIDS_JOIN_DELETE, "JOIN_ONE_TO_ONE", "KEEP_ALL", 'Description "Description" true true false 50 Text 0 0 ,First,#,'+FIRE_GRIDS_INTERNAL+',Description,-1,-1;ID "ID" true true false 4 Long 0 10 ,First,#,'+FIRE_GRIDS_INTERNAL+',ID,-1,-1;FG_UNIQUE_ID "FG_UNIQUE_ID" true true false 4 Long 0 10 ,First,#,'+FIRE_GRIDS_INTERNAL+',FG_UNIQUE_ID,-1,-1;EDIT_DATE "EDIT_DATE" true true false 8 Date 0 0 ,First,#,'+FIRE_GRIDS_INTERNAL+',EDIT_DATE,-1,-1;Shape_STArea__ "Shape_STArea__" false false true 0 Double 0 0 ,First,#,'+FIRE_GRIDS_INTERNAL+',Shape.STArea(),-1,-1;Shape_STLength__ "Shape_STLength__" false false true 0 Double 0 0 ,First,#,'+FIRE_GRIDS_INTERNAL+',Shape.STLength(),-1,-1;FIRE_DEPT "FIRE DEPARTMENT" true true false 50 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,FIRE_DEPT,-1,-1;FIRE_FDID "FIRE DEPARTMENT FDID CODE" true true false 15 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,FIRE_FDID,-1,-1;FIRE_NUM "FIRE DEPARTMENT #" true true false 10 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,FIRE_NUM,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,COUNTY_FIPS,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,GLOBALID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,STATE,-1,-1;SHAPE_STArea_1 "SHAPE_STArea_1" false true true 0 Double 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,SHAPE.STArea(),-1,-1;SHAPE_STLength_1 "SHAPE_STLength_1" false true true 0 Double 0 0 ,First,#,FIRE_DEPT_COVERAGE_INTERNAL_LYR,SHAPE.STLength(),-1,-1', "INTERSECT", "", "")
except:
    print ("\n Unable to Spatial Join Fire Dept Internal Layer and Fire Grids")
    write_log("Unable to Spatial Join Fire Dept Internal Layer and Fire Grids", logfile)
    logging.exception('Got exception on Spatial Join Fire Dept Internal Layer and Fire Grids logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Add CAD_ID Field to FIRE_GRIDS_JOIN_DELETE
    arcpy.AddField_management(FIRE_GRIDS_JOIN_DELETE, "CAD_ID", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print ("\n Unable to Add CAD_ID Field to FIRE_GRIDS_JOIN_DELETE")
    write_log("Unable to Add CAD_ID Field to FIRE_GRIDS_JOIN_DELETE", logfile)
    logging.exception('Got exception on Add CAD_ID Field to FIRE_GRIDS_JOIN_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Process: Calculate Field CAD_ID
    arcpy.CalculateField_management(FIRE_GRIDS_JOIN_DELETE, "CAD_ID", "!ID!", "PYTHON", "")
except:
    print ("\n Unable to Calculate Field CAD_ID")
    write_log("Unable to Calculate Field CAD_ID", logfile)
    logging.exception('Got exception on Calculate Field CAD_ID logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Add CAD_Description Field to FIRE_GRIDS_JOIN_DELETE
    arcpy.AddField_management(FIRE_GRIDS_JOIN_DELETE, "CAD_DESCRIPTION", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print ("\n Unable to Add CAD_Description Field to FIRE_GRIDS_JOIN_DELETE")
    write_log("Unable to Add CAD_Description Field to FIRE_GRIDS_JOIN_DELETE", logfile)
    logging.exception('Got exception on Add CAD_Description Field to FIRE_GRIDS_JOIN_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Calculate CAD Description Field
    arcpy.CalculateField_management(FIRE_GRIDS_JOIN_DELETE, "CAD_DESCRIPTION", '"20"+"-"+ !Description!', "PYTHON", "")
except:
    print ("\n Unable to Calculate CAD Description Field")
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
    print ("\n Unable to Append FIRE_GRIDS_JOIN_DELETE to Fire Response in Northern Tier FGDB")
    write_log("Unable to Append FIRE_GRIDS_JOIN_DELETE to Fire Response in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append FIRE_GRIDS_JOIN_DELETE to Fire Response in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
print ("       Fire Department-Fire Grids coverage to Fire Response append completed")
write_log("       Fire Department-Fire Grids coverage to Fire Response append completed", logfile)


print ("\n Append Police Department Coverage from CRAW_INTERNAL to Northern Tier FGDB Police Department")
write_log("\n Append Police Department Coverage from CRAW_INTERNAL to Northern Tier FGDB Police Department", logfile)

try:
    # Export PoliceDept Internal to PoliceDept Delete (create temporary police dept feature in delete_file FDS for manipulation into police department for CAD)
    arcpy.FeatureClassToFeatureClass_conversion(POLICE_DEPT_COVERAGE_INTERNAL, DELETE_FILES, "POLICE_DEPT_COVERAGE_DELETE", "POLICE_DEPT <> 'PA STATE POLICE - CORRY' OR COUNTY_FIPS = 42039", 'POLICE_DEPT "POLICE DEPARTMENT" true true false 50 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',POLICE_DEPT,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',COUNTY_FIPS,-1,-1;POLICE_ID "POLICE_ID" true true false 4 Long 0 10 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',POLICE_ID,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',GLOBALID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',STATE,-1,-1;SHAPE_STArea__ "SHAPE_STArea__" false false true 0 Double 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',SHAPE.STArea(),-1,-1;SHAPE_STLength__ "SHAPE_STLength__" false false true 0 Double 0 0 ,First,#,'+POLICE_DEPT_COVERAGE_INTERNAL+',SHAPE.STLength(),-1,-1', "")
except:
    print ("\n Unable to Export PoliceDept Internal to PoliceDept Delete")
    write_log("Unable to Export PoliceDept Internal to PoliceDept Delete", logfile)
    logging.exception('Got exception on Export PoliceDept Internal to PoliceDept Delete logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Add PoliceDeptID Field to POLICE_DEPT_COVERAGE_DELETE
    arcpy.AddField_management(POLICE_DEPT_COVERAGE_DELETE, "ID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print ("\n Unable to Add PoliceDeptID Field to POLICE_DEPT_COVERAGE_DELETE")
    write_log("Unable to Add PoliceDeptID Field to POLICE_DEPT_COVERAGE_DELETE", logfile)
    logging.exception('Got exception on Add PoliceDeptID Field to POLICE_DEPT_COVERAGE_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Calculate Field - PoliceDept ID (calculate 20+POLICE_ID into field)
    arcpy.CalculateField_management(POLICE_DEPT_COVERAGE_DELETE, "ID", '"20{}".format(!POLICE_ID!)', "PYTHON", "")
except:
    print ("\n Unable to Calculate Field - PoliceDept ID")
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
    print ("\n Unable to Calculate Description Field - ORI CODES")
    write_log("Unable to Calculate Description Field - ORI CODES", logfile)
    logging.exception('Got exception on Calculate Description Field - ORI CODES logged at:'  + str(Day) + " " + str(Time))
    raise
    pass
    sys.exit ()

try:
    # Dissolve POLICE_DEPT_COVERAGE_DELETE to elminate separate features
    arcpy.Dissolve_management(POLICE_DEPT_COVERAGE_DELETE, DELETE_FILES + "//POLICE_DEPT_COVERAGE_DELETE_DISSOLVE", "POLICE_DEPT;COUNTY_NAME;COUNTY_FIPS;POLICE_ID;DiscrpAgID;STATE;ID", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to Dissolve POLICE_DEPT_COVERAGE_DELETE to elminate separate features")
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
    print ("\n Unable to Append POLICE_DEPT_COVERAGE_DELETE_DISSOLVE to Police Department in Northern Tier FGDB")
    write_log("Unable to Append POLICE_DEPT_COVERAGE_DELETE_DISSOLVE to Police Department in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append POLICE_DEPT_COVERAGE_DELETE_DISSOLVE to Police Department in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
print ("      Police Department coverage to Police Department append completed")
write_log("      Police Department coverage to Police Department append completed", logfile)

print ("\n Append Police Department Coverage from CRAW_INTERNAL to Northern Tier FGDB Police Response")
write_log("\n Append Police Department Coverage from CRAW_INTERNAL to Northern Tier FGDB Police Response", logfile)

try:
    # Dissolve POLICE_DEPT_COVERAGE_INTERNAL to eliminate separate features
    arcpy.Dissolve_management(POLICE_DEPT_COVERAGE_INTERNAL, DELETE_FILES + "//POLICE_RESPONSE_DISSOLVE", "POLICE_DEPT;COUNTY_NAME;COUNTY_FIPS;POLICE_ID;DiscrpAgID;STATE", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to Dissolve POLICE_DEPT_COVERAGE_INTERNAL to eliminate separate features")
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
    print ("\n Unable to Append POLICE_DEPT_COVERAGE_INTERNAL to Police Response in Northern Tier FGDB")
    write_log("Unable to Append POLICE_DEPT_COVERAGE_INTERNAL to Police Response in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append POLICE_DEPT_COVERAGE_INTERNAL to Police Response in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
print ("      Police Department coverage to Police Response append completed")
write_log("      Police Department coverage to Police Response append completed", logfile)


print ("\n Process Municipal Boundaries with Police Department Coverage in Police Reporting and then append to Northern Tier FGDB")
write_log("\n Process Municipal Boundaries with Police Department Coverage in Police Reporting and then append to Northern Tier FGDB", logfile)

try:
    # Spatial Join COUNTY_ADJ_MUNI_BOUND_INTERNAL to POLICE_DEPT_COVERAGE_INTERNAL (spatial join county adjusted muni boundaries with police dept coverage to break up into municipal sized police zones for CAD police reporting)
    arcpy.SpatialJoin_analysis(COUNTY_ADJ_MUNI_BOUND_INTERNAL, POLICE_DEPT_COVERAGE_INTERNAL, POLICE_REPORT_JOIN_DELETE, "JOIN_ONE_TO_ONE", "KEEP_ALL", 'MUNI_NAME "MUNICIPALITY NAME" true true false 50 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',MUNI_NAME,-1,-1;MUNI_FIPS "MUNICIPALITY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',MUNI_FIPS,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE DATE" true true false 8 Date 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',UPDATE_DATE,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',GLOBALID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',STATE,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',DiscrpAgID,-1,-1;COUNTRY "Country" true true false 2 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',COUNTRY,-1,-1;SHAPE_STArea__ "SHAPE_STArea__" false false true 0 Double 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',SHAPE.STArea(),-1,-1;SHAPE_STLength__ "SHAPE_STLength__" false false true 0 Double 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',SHAPE.STLength(),-1,-1;POLICE_DEPT "POLICE DEPARTMENT" true true false 50 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,POLICE_DEPT,-1,-1;COUNTY_NAME_1 "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS_1 "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,COUNTY_FIPS,-1,-1;POLICE_ID "POLICE_ID" true true false 4 Long 0 10 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,POLICE_ID,-1,-1;GLOBALID_1 "GLOBALID_1" false false false 38 GlobalID 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,GLOBALID,-1,-1;DiscrpAgID_1 "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,DiscrpAgID,-1,-1;STATE_1 "State" true true false 2 Text 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,STATE,-1,-1;SHAPE_STArea_1 "SHAPE_STArea_1" false false true 0 Double 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE_STLength_1 "SHAPE_STLength_1" false false true 0 Double 0 0 ,First,#,Database Connections\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Public_Safety\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL,SHAPE.STLength(),-1,-1', "INTERSECT", "", "")
except:
    print ("\n Unable to Spatial Join COUNTY_ADJ_MUNI_BOUND_INTERNAL to POLICE_DEPT_COVERAGE_INTERNAL")
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
    print ("\n Unable to Append POLICE_REPORT_JOIN_DELETE to Police Reporting in Northern Tier FGDB")
    write_log("Unable to Append POLICE_REPORT_JOIN_DELETE to Police Reporting in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append POLICE_REPORT_JOIN_DELETE to Police Reporting in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Police Department coverage-Municipal Boundary to Police Reporting append completed")
write_log("       Police Department coverage-Municipal Boundary to Police Reporting append completed", logfile)


print ("\n Append Hydrants from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Append Hydrants from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append HYDRANTS_DELETE to Hydrants in Northern Tier FGDB (append hydrants, data modified, into staging FGDB)
    arcpy.Append_management(HYDRANTS_INTERNAL, Hydrants_CrawfordCo, "NO_TEST", 'ID "ID" true true false 4 Long 0 0 ,First,#,'+HYDRANTS_INTERNAL+',ID,-1,-1;NWS_ADDRESS_ID "NWS_ADDRESS_ID" true true false 4 Long 0 0 ,First,#,'+HYDRANTS_INTERNAL+',ADDRESS_ID,-1,-1;NWS_HYDRANT_ID "NWS_HYDRANT_ID" true true false 4 Long 0 0 ,First,#,'+HYDRANTS_INTERNAL+',HYDRANT_ID,-1,-1;NWS_HYDRANT_NUMBER "NWS_HYDRANT_NUMBER" true true false 20 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',LOCAL_HYDRANT_NUMBER,-1,-1;NWS_HYDRANT_LOCATIONDESCRIPTION "NWS_HYDRANT_LOCATIONDESCRIPTION" true true false 50 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',HYDRANT_LOCATION_DESCRIPTION,-1,-1;NWS_HYDRANT_SERIAL_NUMBER "NWS_HYDRANT_SERIAL_NUMBER" true true false 20 Text 0 0 ,First,#;NWS_HYDRANT_IN_SERVICE "NWS_HYDRANT_IN_SERVICE" true true false 3 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',HYDRANT_IN_SERVICE,-1,-1;NWS_HYDRANT_COLOR "NWS_HYDRANT_COLOR" true true false 30 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',HYDRANT_COLOR,-1,-1;SIZE "SIZE" true true false 50 Text 0 0 ,First,#;TYPE "TYPE" true true false 50 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',TYPE,-1,-1;GPM "GPM" true true false 50 Text 0 0 ,First,#,'+HYDRANTS_INTERNAL+',GPM,-1,-1', subtype="")
    Hydrants_result = arcpy.GetCount_management(Hydrants_CrawfordCo)
    print ('{} has {} records'.format(Hydrants_CrawfordCo, Hydrants_result[0]))
    write_log('{} has {} records'.format(Hydrants_CrawfordCo, Hydrants_result[0]), logfile)
except:
    print ("\n Unable to Append HYDRANTS_INTERNAL to Hydrants in Northern Tier FGDB")
    write_log("Unable to Append Append HYDRANTS_INTERNAL to Hydrants in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append Append HYDRANTS_INTERNAL to Hydrants in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("      Hydrants append completed")
write_log("      Hydrants append completed", logfile)


print ("\n Append Landmarks from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Append Landmarks from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append LANDMARKS_INTERNAL to Landmarks in Northern Tier FGDB (append landmarks, unchanged, into staging FGDB)
    arcpy.Append_management(LANDMARKS_INTERNAL, Landmarks_CrawfordCo, "NO_TEST",'DiscrpAgID "Agency ID" true true false 75 Text 0 0 ,First,#,'+LANDMARKS_INTERNAL+',LANDMARK_NAME,-1,-1;DateUpdate "Date Updated" true true false 8 Date 0 0 ,First,#,'+LANDMARKS_INTERNAL+',UPDATE_DATE,-1,-1;Effective "Effective Date" true true false 8 Date 0 0 ,First,#;Expire "Expiration Date" true true false 8 Date 0 0 ,First,#;LMNP_NGUID "Landmark Name GID" true true false 254 Text 0 0 ,First,#,'+LANDMARKS_INTERNAL+',LANDMARK_NAME,-1,-1;Site_NGUID "Site GID" true true false 254 Text 0 0 ,First,#,'+LANDMARKS_INTERNAL+',LANDMARK_NAME,-1,-1;ACLMNNGUID "Complete Landmark Name GID" true true false 254 Text 0 0 ,First,#,'+LANDMARKS_INTERNAL+',LANDMARK_NAME,-1,-1;LMNamePart "Landmark Name Part" true true false 150 Text 0 0 ,First,#,'+LANDMARKS_INTERNAL+',LANDMARK_NAME,-1,-1;LMNP_Order "Landmark Name Part Order" true true false 1 Text 0 0 ,First,#', "")
except:
    print ("\n Unable to Append LANDMARKS_INTERNAL to Landmarks in Northern Tier FGDB")
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
    print ("\n Unable to Calculate Landmarks DiscrpAgID field in Northern Tier FGDB")
    write_log("Unable to Calculate Landmarks DiscrpAgID field in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Calculate Landmarks DiscrpAgID field in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Landmarks append completed")
write_log("       Landmarks append completed", logfile)


print ("\n Append Mile Markers from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Append Mile Markers from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append MILE_MARKERS_INTERNAL to MilePosts in Northern Tier FGDB (append Mile Markers, unchanged, into staging FGDB)
    arcpy.Append_management(MILE_MARKERS_INTERNAL, MilePosts_CrawfordCo, "NO_TEST", 'DiscrpAgID "Agency ID" true true false 75 Text 0 0 ,First,#,'+MILE_MARKERS_INTERNAL+',MARKER_NAME,-1,-1;DateUpdate "Date Updated" true true false 8 Date 0 0 ,First,#;MileMNGUID "Mile Post GID" true true false 254 Text 0 0 ,First,#,'+MILE_MARKERS_INTERNAL+',MARKER_NAME,-1,-1;MileM_Unit "MP Unit" true true false 15 Text 0 0 ,First,#,'+MILE_MARKERS_INTERNAL+',MILE_POST,-1,-1;MileMValue "MP Measurement" true true false 8 Double 0 0 ,First,#;MileM_Rte "MP Route Name" true true false 100 Text 0 0 ,First,#,'+MILE_MARKERS_INTERNAL+',STREET_NAME,-1,-1;MileM_Type "MP Type" true true false 15 Text 0 0 ,First,#;MileM_Ind "MP Indicator" true true false 1 Text 0 0 ,First,#', "")
    MilePosts_result = arcpy.GetCount_management(MilePosts_CrawfordCo)
    print ('{} has {} records'.format(MilePosts_CrawfordCo, MilePosts_result[0]))
    write_log('{} has {} records'.format(MilePosts_CrawfordCo, MilePosts_result[0]), logfile)
except:
    print ("\n Unable to Append MILE_MARKERS_INTERNAL to MilePosts in Northern Tier FGDB")
    write_log("Unable to Append MILE_MARKERS_INTERNAL to MilePosts in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append MILE_MARKERS_INTERNAL to MilePosts in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Mile Markers to Mile Posts append completed")
write_log("       Mile Markers to Mile Posts append completed", logfile)


print ("\n Append Municipalities from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Append Municipalities from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append COUNTY_ADJ_MUNI_BOUND_INTERNAL to Municipalities in Northern Tier FGDB (append county adjusted municipal boundaries, unchanged, into staging FGDB)
    arcpy.Append_management(COUNTY_ADJ_MUNI_BOUND_INTERNAL, Municipalities_CrawfordCo, "NO_TEST", 'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',DiscrpAgID,-1,-1;DateUpdate "DateUpdate" true true false 8 Date 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',UPDATE_DATE,-1,-1;Effective "Effective" true true false 8 Date 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',UPDATE_DATE,-1,-1;Expire "Expire" true true false 8 Date 0 0 ,First,#;Shape_Leng "Shape_Leng" true true false 8 Double 0 0 ,First,#;IncM_NGUID "IncM_NGUID" true true false 254 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',MUNI_FIPS,-1,-1;Country "Country" true true false 2 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',COUNTRY,-1,-1;State "State" true true false 2 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',STATE,-1,-1;County "County" true true false 75 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',COUNTY_NAME,-1,-1;AddCode "AddCode" true true false 6 Text 0 0 ,First,#;Inc_Muni "Inc_Muni" true true false 100 Text 0 0 ,First,#,'+COUNTY_ADJ_MUNI_BOUND_INTERNAL+',MUNI_NAME,-1,-1;Shape_Length "Shape_Length" false true true 8 Double 0 0 ,First,#;Shape_Area "Shape_Area" false true true 8 Double 0 0 ,First,#', "")
    Municipalities_result = arcpy.GetCount_management(Municipalities_CrawfordCo)
    print ('{} has {} records'.format(Municipalities_CrawfordCo, Municipalities_result[0]))
    write_log('{} has {} records'.format(Municipalities_CrawfordCo, Municipalities_result[0]), logfile)
except:
    print ("\n Unable to Append COUNTY_ADJ_MUNI_BOUND_INTERNAL to Municipalities in Northern Tier FGDB")
    write_log("Unable to Append COUNTY_ADJ_MUNI_BOUND_INTERNAL to Municipalities in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Append COUNTY_ADJ_MUNI_BOUND_INTERNAL to Municipalities in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("       Municipalities append completed")
write_log("       Municipalities append completed", logfile)

print ("\n Append Tax Parcels from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Append Tax Parcels from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append TAX_PARCELS_INTERNAL to Parcels in Northern Tier FGDB (append tax parcels, unchanged, into staging FGDB)
    arcpy.Append_management(TAX_PARCELS_INTERNAL, Parcels_CrawfordCo, "NO_TEST", 'ParcelID "ParcelID" true true false 25 Text 0 0 ,First,#;Map_Num "Map_Num" true true false 50 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',CAMA_PIN,-1,-1;Own "Own" true true false 100 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',REM_OWN_NAME,-1,-1;Add_Number "Add_Number" true true false 4 Long 0 0 ,First,#;AddNum_Suf "AddNum_Suf" true true false 15 Text 0 0 ,First,#;St_PreDir "St_PreDir" true true false 9 Text 0 0 ,First,#;St_Name "St_Name" true true false 60 Text 0 0 ,First,#;St_PostType "St_PostType" true true false 50 Text 0 0 ,First,#;St_PostDir "St_PostDir" true true false 9 Text 0 0 ,First,#;City "City" true true false 50 Text 0 0 ,First,#;Add_State "Add_State" true true false 2 Text 0 0 ,First,#;Zip "Zip" true true false 10 Text 0 0 ,First,#;Muni "Muni" true true false 100 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',SEC_MUNI_NAME,-1,-1;County "County" true true false 75 Text 0 0 ,First,#;State "State" true true false 2 Text 0 0 ,First,#;Contry "Contry" true true false 2 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#', "")
except:
    print ("\n Unable to Append TAX_PARCELS_INTERNAL to Parcels in Northern Tier FGDB")
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
    print ("\n Unable to Calculate Parcels County/State/Contry field in Northern Tier FGDB")
    write_log("Unable to Calculate Parcels County/State/Contry field in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Calculate Parcels County/State/Contry field in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("       Tax Parcels to Parcels append completed")
write_log("       Tax Parcels to Parcels append completed", logfile)

print ("\n Append Railroads from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Append Railroads from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Append RAILROADS_INTERNAL to Railroads in Northern Tier FGDB (append railroads, unchanged, into staging FGDB)
    arcpy.Append_management(RAILROADS_INTERNAL, Railroads_CrawfordCo, "NO_TEST", 'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0 ,First,#;DateUpdate "DateUpdate" true true false 8 Date 0 0 ,First,#,'+RAILROADS_INTERNAL+',UPDATE_DATE,-1,-1;RS_NGUID "RS_NGUID" true true false 254 Text 0 0 ,First,#;RLOWN "RLOWN" true true false 100 Text 0 0 ,First,#,'+RAILROADS_INTERNAL+',OPERATIONS_OWNER,-1,-1;RLOP "RLOP" true true false 100 Text 0 0 ,First,#,'+RAILROADS_INTERNAL+',OPERATIONS_OWNER,-1,-1;Trck_Right "Trck_Right" true true false 100 Text 0 0 ,First,#,'+RAILROADS_INTERNAL+',TRACK_RIGHTS,-1,-1;RMPL "RMPL" true true false 8 Double 0 0 ,First,#;RMPH "RMPH" true true false 8 Double 0 0 ,First,#;Muni "Muni" true true false 100 Text 0 0 ,First,#,'+RAILROADS_INTERNAL+',MUNI_NAME,-1,-1;County "County" true true false 75 Text 0 0 ,First,#,'+RAILROADS_INTERNAL+',COUNTY_NAME,-1,-1;State "State" true true false 2 Text 0 0 ,First,#;Contry "Contry" true true false 2 Text 0 0 ,First,#;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#', "")
except:
    print ("\n Unable to Append RAILROADS_INTERNAL to Railroads in Northern Tier FGDB")
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
    print ("\n Unable to Calculate DiscrpAgID/State/Contry field in Northern Tier FGDB")
    write_log("Unable to Calculate Parcels DiscrpAgID/State/Contry field to CRAWFORD in Northern Tier FGDB", logfile)
    logging.exception('Got exception on Calculate Parcels DiscrpAgID/State/Contry field to CRAWFORD in Northern Tier FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()    

print ("      Railroads append completed")
write_log("      Railroads append completed", logfile)


print ("\n Append County Adjusted Municipal Boundaries from CRAW_INTERNAL to Northern Tier FGDB")
write_log("\n Append County Adjusted Municipal Boundaries from CRAW_INTERNAL to Northern Tier FGDB", logfile)

try:
    # Make Feature Layer - Crawford Adjusted Muni (make temporary layer field of county adjusted muni boundaries for manipulation in steps below)
    arcpy.MakeFeatureLayer_management(COUNTY_ADJ_MUNI_BOUND_INTERNAL, COUNTY_ADJ_MUNI_LAYER, "", "", "MUNI_NAME MUNI_NAME VISIBLE NONE;MUNI_FIPS MUNI_FIPS VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;UPDATE_DATE UPDATE_DATE VISIBLE NONE;GLOBALID GLOBALID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;STATE STATE VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;COUNTRY COUNTRY VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print ("\n Unable to Make Feature Layer - Crawford Adjusted Muni")
    write_log("Unable to Make Feature Layer - Crawford Adjusted Muni", logfile)
    logging.exception('Got exception on Make Feature Layer - Crawford Adjusted Muni logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Dissolve COUNTY_ADJ_MUNI_LAYER into County shape (dissolve all county adjusted muni boundaries into 1 polygon to make county polygon)
    arcpy.Dissolve_management(COUNTY_ADJ_MUNI_LAYER, MUNI_DISSOLVE, "COUNTY_NAME;COUNTY_FIPS;STATE;DiscrpAgID;COUNTRY", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to Dissolve COUNTY_ADJ_MUNI_LAYER into County shape")
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
    print ("\n Unable to Append COUNTY_ADJ_MUNI_BOUND_DISSOLVE to Counties in Northern Tier FGDB")
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
    print ("\n Unable to calculate DateUpdate & Effective fields in Counties_CrawfordCo FC")
    write_log("Unable to calculate DateUpdate & Effective fields in Counties_CrawfordCo FC", logfile)
    logging.exception('Got exception on calculate DateUpdate & Effective fields in Counties_CrawfordCo FC logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("       County Adjusted Municipal Boundaries to Counties append completed")
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

print ("\n ****Preparing PA NG911 Export FGDB*****")
write_log("\n ****Preparing PA NG911 Export FGDB*****", logfile)

try:
    # Create PA_NG911_Export_YYYYMMDD geodatabase
    arcpy.management.CreateFileGDB(PA_NG911_EXPORT_FLDR, "PA_NG911_Export_YYYYMMDD", "CURRENT")
    print ("\n PA_NG911_Export_YYYYMMDD geodatabase created")
    write_log("\n PA_NG911_Export_YYYYMMDD geodatabase created",logfile)
except:
    print ("\n Unable to create PA_NG911_Export_YYYYMMDD geodatabase")
    write_log("\n Unable to create PA_NG911_Export_YYYYMMDD geodatabase", logfile)
    logging.exception('Got exception on creation of PA_NG911_Export_YYYYMMDD geodatabase logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

# Define Work Paths for NG911 Database:
PA_NG911_FGDB = PA_NG911_EXPORT_FLDR + "\\PA_NG911_Export_YYYYMMDD.gdb"
Ambulance_Company_NG911 = PA_NG911_FGDB + "\\Ambulance_Company_CrawfordCo"
Centerline_NG911 = PA_NG911_FGDB + "\\Centerline_CrawfordCo"
Counties_NG911 = PA_NG911_FGDB + "\\Counties_CrawfordCo"
EMS_Districts_NG911 = PA_NG911_FGDB + "\\EMS_Districts_CrawfordCo"
Fire_Department_NG911 = PA_NG911_FGDB + "\\Fire_Department_CrawfordCo"
Fire_Response_NG911 = PA_NG911_FGDB + "\\Fire_Response_CrawfordCo"
Hydrants_NG911 = PA_NG911_FGDB + "\\NWS_Hydrants_CrawfordCo"
Landmarks_NG911 = PA_NG911_FGDB + "\\Landmarks_CrawfordCo"
MilePosts_NG911 = PA_NG911_FGDB + "\\MilePosts_CrawfordCo"
Municipalities_NG911 = PA_NG911_FGDB + "\\Municipalities_CrawfordCo"
AddressPoint_NG911 = PA_NG911_FGDB + "\\AddressPoint_CrawfordCo"
Police_Department_NG911 = PA_NG911_FGDB + "\\Police_Department_CrawfordCo"
Police_Reporting_NG911 = PA_NG911_FGDB + "\\Police_Reporting_CrawfordCo"
Railroads_NG911 = PA_NG911_FGDB + "\\Railroads_CrawfordCo"
DELETE_FILES_NG911 = PA_NG911_FGDB + "\\DELETE_FILES"
ESZ_DISSOLVE = DELETE_FILES_NG911 + "\\ESZ_DISSOLVE_DELETE"

print ("\n Copy data from Northern Tier FGDB to PA_NG911_Export FGDB for alterations")
write_log ("\n Copy data from Northern Tier FGDB to PA_NG911_Export FGDB for alterations",logfile)

NT_FC_LIST = [NTAddressPoint_CrawfordCo,Ambulance_Company_CrawfordCo,Centerline_CrawfordCo,Counties_CrawfordCo,EMS_Districts_CrawfordCo,Fire_Department_CrawfordCo,Fire_Response_CrawfordCo,Landmarks_CrawfordCo,MilePosts_CrawfordCo,Municipalities_CrawfordCo,Hydrants_CrawfordCo,Police_Department_CrawfordCo,Police_Reporting_CrawfordCo,Police_Response_CrawfordCo,Railroads_CrawfordCo]

try:
    # Copy some of the data from Northern Tier FGDB to PA NG911 FGDB
    arcpy.conversion.FeatureClassToGeodatabase(NT_FC_LIST, PA_NG911_FGDB)
    print ("\n Feature classes copied over to PA_NG911 FGDB")
    write_log("\n  Feature classes copied over to PA_NG911 FGDB",logfile)
except:
    print ("\n Unable to copy feature classes from Northern Tier FGDB to PA_NG911 FGDB")
    write_log("\n Unable to copy feature classes from Northern Tier FGDB to PA_NG911 FGDB", logfile)
    logging.exception('Got exception on copy feature classes from Northern Tier FGDB to PA_NG911 FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Add Full_Street_Name field to Address Points
    arcpy.management.AddField(AddressPoint_NG911, "Full_Street_Name", "TEXT", None, None, None, "Full Street Name", "NULLABLE", "NON_REQUIRED", '')
    print ("\n   Full_Street_Name field added to address points")
    write_log("\n  Full_Street_Name field added to address points",logfile)
except:
    print ("\n Unable to add Full_Street_Name field to Address Points")
    write_log("\n Unable to add Full_Street_Name field to Address Points", logfile)
    logging.exception('Got exception on add Full_Street_Name field to Address Points logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()


try:
    # Delete rows from Address Points - NG911 FC and append from Northern Tier CAD address points to populate legacy street names
    arcpy.management.DeleteRows(AddressPoint_NG911)
    arcpy.management.Append(NTAddressPoint_CrawfordCo, AddressPoint_NG911, "NO_TEST", r'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',DiscrpAgID,0,75;DateUpdate "DateUpdate" true true false 8 Date 0 0,First,#,'+NTAddressPoint_CrawfordCo+',DateUpdate,-1,-1;Effective "Effective" true true false 8 Date 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Effective,-1,-1;Expire "Expire" true true false 8 Date 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Expire,-1,-1;Site_NGUID "Site_NGUID" true true false 254 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Site_NGUID,0,254;Country "Country" true true false 2 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Country,0,2;State "State" true true false 2 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',State,0,2;County "County" true true false 40 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',County,0,40;AddCode "AddCode" true true false 506 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',AddCode,0,506;AddDataURI "AddDataURI" true true false 254 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',AddDataURI,0,254;Inc_Muni "Inc_Muni" true true false 100 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Inc_Muni,0,100;Uninc_Comm "Uninc_Comm" true true false 100 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Uninc_Comm,0,100;Nbrhd_Comm "Nbrhd_Comm" true true false 100 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Nbrhd_Comm,0,100;AddNum_Pre "AddNum_Pre" true true false 50 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',AddNum_Pre,0,50;Add_Number "Add_Number" true true false 4 Long 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Add_Number,-1,-1;AddNum_Suf "AddNum_Suf" true true false 15 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',AddNum_Suf,0,15;St_PreMod "St_PreMod" true true false 15 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_PreMod,0,15;St_PreDir "ST_PreDir" true true false 9 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_PreDir,0,9;St_PreTyp "St_PreTyp" true true false 50 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_PreTyp,0,50;St_PreSep "St_PreSep" true true false 20 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_PreSep,0,20;St_Name "St_Name" true true false 60 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_Name,0,60;St_PosTyp "St_PosTyp" true true false 50 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_PosTyp,0,50;St_PosDir "St_PosDir" true true false 9 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_PosDir,0,9;St_PosMod "St_PosMod" true true false 25 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_PosMod,0,25;LSt_PreDir "LSt_PreDir" true true false 2 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_PreDir,0,9;LSt_Name "LSt_Name" true true false 75 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_Name,0,60;LSt_Type "LSt_Type" true true false 4 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_PosTyp,0,50;LStPosDir "LStPosDir" true true false 2 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',St_PosDir,0,9;ESN "ESN" true true false 5 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',ESN,0,5;MSAGComm "MSAGComm" true true false 30 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',MSAGComm,0,30;Post_Comm "Post_Comm" true true false 40 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Post_Comm,0,40;Post_Code "Post_Code" true true false 7 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Post_Code,0,7;Post_Code4 "Post_Code4" true true false 4 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Post_Code4,0,4;Building "Building" true true false 75 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Building,0,75;Floor "Floor" true true false 75 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Floor,0,75;Unit "Unit" true true false 75 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Unit,0,75;Room "Room" true true false 75 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Room,0,75;Seat "Seat" true true false 75 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Seat,0,75;Addtl_Loc "Addtl_Loc" true true false 225 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Addtl_Loc,0,225;LandmkName "LandmkName" true true false 150 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',LandmkName,0,150;Mile_Post "Mile_Post" true true false 150 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Mile_Post,0,150;Place_Type "Place_Type" true true false 50 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Place_Type,0,50;Placement "Placement" true true false 25 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Placement,0,25;Long "Long" true true false 8 Double 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Long,-1,-1;Lat "Lat" true true false 8 Double 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Lat,-1,-1;Elev "Elev" true true false 4 Long 0 0,First,#,'+NTAddressPoint_CrawfordCo+',Elev,-1,-1;JOIN_ID "JOIN_ID" true true false 4 Long 0 0,First,#,'+NTAddressPoint_CrawfordCo+',JOIN_ID,-1,-1;FullName "FullName" true true false 80 Text 0 0,First,#,'+NTAddressPoint_CrawfordCo+',FullName,0,80;Full_Street_Name "Full Street Name" true true false 255 Text 0 0,First,#', '', '')
    print ("\n   Replaced rows in Address Points to populate Legacy Street Names")
    write_log("\n  Replaced rows in Address Points to populate Legacy Street Names",logfile)
except:
    print ("\n Unable to replace rows in Address Points to populate Legacy Street Names")
    write_log("\n Unable to replace rows in Address Points to populate Legacy Street Names", logfile)
    logging.exception('Got exception on replace rows in Address Points to populate Legacy Street Names logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()


try:
    # Delete rows from Street Centerline - NG911 FC and append from Northern Tier CAD Street Centerline to populate legacy street names
    arcpy.management.DeleteRows(Centerline_NG911)
    arcpy.management.Append(Centerline_CrawfordCo, Centerline_NG911, "NO_TEST", r'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0,First,#,'+Centerline_CrawfordCo+',DiscrpAgID,0,75;DateUpdate "DateUpdate" true true false 8 Date 0 0,First,#,'+Centerline_CrawfordCo+',DateUpdate,-1,-1;Effective "Effective" true true false 8 Date 0 0,First,#,'+Centerline_CrawfordCo+',Effective,-1,-1;Expire "Expire" true true false 8 Date 0 0,First,#,'+Centerline_CrawfordCo+',Expire,-1,-1;RCL_NGUID "RCL_NGUID" true true false 254 Text 0 0,First,#,'+Centerline_CrawfordCo+',RCL_NGUID,0,254;AdNumPre_L "AdNumPre_L" true true false 15 Text 0 0,First,#,'+Centerline_CrawfordCo+',AdNumPre_L,0,15;AdNumPre_R "AdNumPre_R" true true false 15 Text 0 0,First,#,'+Centerline_CrawfordCo+',AdNumPre_R,0,15;FromAddr_L "FromAddr_L" true true false 4 Long 0 0,First,#,'+Centerline_CrawfordCo+',FromAddr_L,-1,-1;ToAddr_L "ToAddr_L" true true false 4 Long 0 0,First,#,'+Centerline_CrawfordCo+',ToAddr_L,-1,-1;FromAddr_R "FromAddr_R" true true false 4 Long 0 0,First,#,'+Centerline_CrawfordCo+',FromAddr_R,-1,-1;ToAddr_R "ToAddr_R" true true false 4 Long 0 0,First,#,'+Centerline_CrawfordCo+',ToAddr_R,-1,-1;Parity_L "Parity_L" true true false 1 Text 0 0,First,#,'+Centerline_CrawfordCo+',Parity_L,0,1;Parity_R "Parity_R" true true false 1 Text 0 0,First,#,'+Centerline_CrawfordCo+',Parity_R,0,1;St_PreMod "St_PreMod" true true false 15 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_PreMod,0,15;St_PreDir "St_PreDir" true true false 9 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_PreDir,0,9;St_PreTyp "St_PreTyp" true true false 50 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_PreTyp,0,50;St_PreSep "St_PreSep" true true false 20 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_PreSep,0,20;St_Name "St_Name" true true false 60 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_Name,0,60;St_PosTyp "St_PosTyp" true true false 50 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_PosTyp,0,50;St_PosDir "St_PosDir" true true false 9 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_PosDir,0,9;St_PosMod "St_PosMod" true true false 25 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_PosMod,0,25;LSt_PreDir "LSt_PreDir" true true false 2 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_PreDir,0,9;LSt_Name "LSt_Name" true true false 75 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_Name,0,60;LSt_Type "LSt_Type" true true false 4 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_PosTyp,0,50;LStPosDir "LStPosDir" true true false 2 Text 0 0,First,#,'+Centerline_CrawfordCo+',St_PosDir,0,9;ESN_L "ESN_L" true true false 5 Text 0 0,First,#,'+Centerline_CrawfordCo+',ESN_L,0,5;ESN_R "ESN_R" true true false 5 Text 0 0,First,#,'+Centerline_CrawfordCo+',ESN_R,0,5;MSAGComm_L "MSAGComm_L" true true false 30 Text 0 0,First,#,'+Centerline_CrawfordCo+',MSAGComm_L,0,30;MSAGComm_R "MSAGComm_R" true true false 30 Text 0 0,First,#,'+Centerline_CrawfordCo+',MSAGComm_R,0,30;Country_L "Country_L" true true false 2 Text 0 0,First,#,'+Centerline_CrawfordCo+',Country_L,0,2;Country_R "Country_R" true true false 2 Text 0 0,First,#,'+Centerline_CrawfordCo+',Country_R,0,2;State_L "State_L" true true false 2 Text 0 0,First,#,'+Centerline_CrawfordCo+',State_L,0,2;State_R "State_R" true true false 2 Text 0 0,First,#,'+Centerline_CrawfordCo+',State_R,0,2;County_L "County_L" true true false 40 Text 0 0,First,#,'+Centerline_CrawfordCo+',County_L,0,40;County_R "County_R" true true false 40 Text 0 0,First,#,'+Centerline_CrawfordCo+',County_R,0,40;AddCode_L "AddCode_L" true true false 6 Text 0 0,First,#,'+Centerline_CrawfordCo+',AddCode_L,0,6;AddCode_R "AddCode_R" true true false 6 Text 0 0,First,#,'+Centerline_CrawfordCo+',AddCode_R,0,6;IncMuni_L "IncMuni_L" true true false 100 Text 0 0,First,#,'+Centerline_CrawfordCo+',IncMuni_L,0,100;IncMuni_R "IncMuni_R" true true false 100 Text 0 0,First,#,'+Centerline_CrawfordCo+',IncMuni_R,0,100;UnincCom_L "UnicCom_L" true true false 100 Text 0 0,First,#,'+Centerline_CrawfordCo+',UnincCom_L,0,100;UnincCom_R "Uninc" true true false 100 Text 0 0,First,#,'+Centerline_CrawfordCo+',UnincCom_R,0,100;NbrhdCom_L "NbrhdCom_L" true true false 100 Text 0 0,First,#,'+Centerline_CrawfordCo+',NbrhdCom_L,0,100;NbrhdCom_R "NbrhdCom_R" true true false 100 Text 0 0,First,#,'+Centerline_CrawfordCo+',NbrhdCom_R,0,100;PostCode_L "PostCode_L" true true false 7 Text 0 0,First,#,'+Centerline_CrawfordCo+',PostCode_L,0,7;PostCode_R "PostCode_R" true true false 7 Text 0 0,First,#,'+Centerline_CrawfordCo+',PostCode_R,0,7;PostComm_L "PostComm_L" true true false 40 Text 0 0,First,#,'+Centerline_CrawfordCo+',PostComm_L,0,40;PostComm_R "PostComm_R" true true false 40 Text 0 0,First,#,'+Centerline_CrawfordCo+',PostComm_R,0,40;RoadClass "RoadClass" true true false 15 Text 0 0,First,#,'+Centerline_CrawfordCo+',RoadClass,0,15;OneWay "OneWay" true true false 2 Text 0 0,First,#,'+Centerline_CrawfordCo+',OneWay,0,2;SpeedLimit "SpeedLimit" true true false 2 Short 0 0,First,#,'+Centerline_CrawfordCo+',SpeedLimit,-1,-1;Valid_L "Valid_L" true true false 1 Text 0 0,First,#,'+Centerline_CrawfordCo+',Valid_L,0,1;Valid_R "Valid_R" true true false 1 Text 0 0,First,#,'+Centerline_CrawfordCo+',Valid_R,0,1;Time "Time" true true false 8 Double 0 0,First,#,'+Centerline_CrawfordCo+',Time,-1,-1;Max_Height "Max_Height" true true false 8 Double 0 0,First,#,'+Centerline_CrawfordCo+',Max_Height,-1,-1;Max_Weight "Max_Weight" true true false 8 Double 0 0,First,#,'+Centerline_CrawfordCo+',Max_Weight,-1,-1;T_ZLev "T_ZLev" true true false 2 Short 0 0,First,#,'+Centerline_CrawfordCo+',T_ZLev,-1,-1;F_ZLev "F_ZLev" true true false 2 Short 0 0,First,#,'+Centerline_CrawfordCo+',F_ZLev,-1,-1;JOIN_ID "JOIN_ID" true true false 4 Long 0 0,First,#,'+Centerline_CrawfordCo+',JOIN_ID,-1,-1;FullName "FullName" true true false 80 Text 0 0,First,#,'+Centerline_CrawfordCo+',FullName,0,80', '', "FullName <> 'DONATION HILL RD'")
    print ("\n   Replaced rows in Street Centerline to populate Legacy Street Names")
    write_log("\n  Replaced rows in Street Centerline to populate Legacy Street Names",logfile)
except:
    print ("\n Unable to replace rows in Street Centerline to populate Legacy Street Names")
    write_log("\n Unable to replace rows in Street Centerline to populate Legacy Street Names", logfile)
    logging.exception('Got exception on replace rows in Street Centerline to populate Legacy Street Names logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("\n  Convert Pre & Post Directional as well as Post Type in Centerline FC within PA NG911 FGDB")
write_log ("\n  Convert Pre & Post Directional as well as Post Type in Centerline FC within PA NG911 FGDB",logfile)

# Convert Centerline Pre & Post Directional as well as Post Type (iterate through centerline export and convert fields from Crawford County system to NG911 standards)
Directionals_ABRV = ["E", "N", "S", "W", "NW", "SW", "NE", "SE"]
Directionals_NG911 = ["EAST", "NORTH", "SOUTH", "WEST", "NORTHWEST", "SOUTHWEST", "NORTHEAST", "SOUTHEAST"]
PostType_ABRV = ["ALY","AVE","BCH","BLVD","CIR","CLB","CP","CT","DR","EXT","HOLW","HTS","HWY","KNL","LK","LN","LNDG","MDWS","MNR","PKWY","PL","PLZ","PT","RD","RDG","RTE","SQ","ST","TER","TRL","XING"]
PostType_NG911 = ["ALLEY","AVENUE","BEACH","BOULEVARD","CIRCLE","CLUB","CAMP","COURT","DRIVE","EXTENSION","HOLLOW","HEIGHTS","HIGHWAY","KNOLL","LAKE","LANE","LANDING","MEADOWS","MANOR","PARKWAY","PLACE","PLAZA","POINT","ROAD","RIDGE","ROUTE","SQUARE","STREET","TERRACE","TRAIL","CROSSING"]
    
try:    
    with arcpy.da.UpdateCursor(Centerline_NG911, 'St_PreDir') as cursor:
        for row in cursor:
            if row[0] in Directionals_ABRV:
                row[0] = Directionals_NG911[Directionals_ABRV.index(row[0])]
                cursor.updateRow(row)
            else:
                pass
        del row 
        del cursor
        print ("    Centerline Pre directional field converted to NG911 standards...")
    with arcpy.da.UpdateCursor(Centerline_NG911, 'St_PosDir') as cursor:
        for row in cursor:
            if row[0] in Directionals_ABRV:
                row[0] = Directionals_NG911[Directionals_ABRV.index(row[0])]
                cursor.updateRow(row)
            else:
                pass
        del row 
        del cursor
        print ("    Centerline Post directional field converted to NG911 standards...")
except:
    print ("\n Unable to convert Centerline Directional Fields")
    write_log("Unable to convert Centerline Directional Fields", logfile)
    logging.exception('Got exception on convert Centerline Directional Fields logged at:'  + str(Day) + " " + str(Time))
    raise
    pass
    sys.exit ()

try:    
    with arcpy.da.UpdateCursor(Centerline_NG911, 'St_PosTyp') as cursor:
        for row in cursor:
            if row[0] in PostType_ABRV:
                row[0] = PostType_NG911[PostType_ABRV.index(row[0])]
                cursor.updateRow(row)
            else:
                pass
        del row 
        del cursor
        print ("    Centerline post type field converted to NG911 standards...")
except:
    print ("\n Unable to convert Centerline Post Type Field")
    write_log("Unable to convert Centerline Post Type Field", logfile)
    logging.exception('Got exception on convert Centerline Post Type Field logged at:'  + str(Day) + " " + str(Time))
    raise
    pass
    sys.exit ()

print ("\n  Convert Pre & Post Directional as well as Post Type in Adress Point FC within PA NG911 FGDB")
write_log ("\n  Convert Pre & Post Directional as well as Post Type in Address Point FC within PA NG911 FGDB",logfile)

try:    
    with arcpy.da.UpdateCursor(AddressPoint_NG911, 'St_PreDir') as cursor:
        for row in cursor:
            if row[0] in Directionals_ABRV:
                row[0] = Directionals_NG911[Directionals_ABRV.index(row[0])]
                cursor.updateRow(row)
            else:
                pass
        del row 
        del cursor
        print ("    Address Points street pre directional field converted to NG911 standards...")
    with arcpy.da.UpdateCursor(AddressPoint_NG911, 'St_PosDir') as cursor:
        for row in cursor:
            if row[0] in Directionals_ABRV:
                row[0] = Directionals_NG911[Directionals_ABRV.index(row[0])]
                cursor.updateRow(row)
            else:
                pass
        del row 
        del cursor
        print ("    Address Points street post directional fields converted to NG911 standards...")
except:
    print ("\n Unable to convert Address Points Street Directional Fields")
    write_log("Unable to convert Address Points Street Directional Fields", logfile)
    logging.exception('Got exception on convert Address Points Street Directional Fields logged at:'  + str(Day) + " " + str(Time))
    raise
    pass
    sys.exit ()

try:    
    with arcpy.da.UpdateCursor(AddressPoint_NG911, 'St_PosTyp') as cursor:
        for row in cursor:
            if row[0] in PostType_ABRV:
                row[0] = PostType_NG911[PostType_ABRV.index(row[0])]
                cursor.updateRow(row)
            else:
                pass
        del row 
        del cursor
        print ("    Address Points street post type field converted to NG911 standards...")
except:
    print ("\n Unable to convert Address Points Street Post Type Field")
    write_log("Unable to convert Address Points Street Post Type Field", logfile)
    logging.exception('Got exception on convert Address Points Street Post Type Field logged at:'  + str(Day) + " " + str(Time))
    raise
    pass
    sys.exit ()

print ("\n Update Full Street Name field in Centerline FC within PA_NG911_Export FGDB")
write_log ("\n Update Full Street Name field in Centerline FC within PA_NG911_Export FGDB",logfile)

try:
    # Field Calculate Full Street Name field in Centerline (NG911 FGDB)
    arcpy.management.CalculateField(Centerline_NG911, "FullName", "ifelse(!St_PreDir!,!St_Name!,!St_PosTyp!,!St_PosDir!)", "PYTHON3", """def ifelse(St_PreDir,St_Name,St_PosTyp,St_PosDir):
    if (St_PreDir and St_PosDir) is not None:
        return St_PreDir+" "+St_Name+" "+St_PosTyp+" "+St_PosDir
    elif (not St_PreDir) and (St_PosTyp and St_PosDir) is not None:
        return St_Name+" "+St_PosTyp+" "+St_PosDir
    elif not (St_PreDir and St_PosTyp) and (St_Name and St_PosDir) is not None:
        return St_Name+" "+St_PosDir
    elif not St_PosDir and (St_PreDir and St_Name and St_PosTyp) is not None:
        return St_PreDir+" "+St_Name+" "+St_PosTyp
    elif not (St_PreDir and St_PosDir) and (St_Name and St_PosTyp) is not None:
        return St_Name+" "+St_PosTyp
    elif not (St_PosTyp and St_PosDir) and (St_PreDir and St_Name) is not None:
        return St_PreDir+" "+St_Name
    else:
        return St_Name""", "TEXT", "NO_ENFORCE_DOMAINS")
    print ("\n     Full Street Name field updated in Centerline FC within PA_NG911_Export FGDB")
    write_log ("\n     Full Street Name field updated in Centerline FC within PA_NG911_Export FGDB",logfile)
except:
    print ("\n Unable to calculate Full Street Name field for Centerlines within PA_NG911 FGDB")
    write_log("\n Unable to calculate Full Street Name field for Centerlines within PA_NG911 FGDB", logfile)
    logging.exception('Got exception on calculate Full Street Name field for Centerlines within PA_NG911 FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("\n Update Full Street Name field in Centerline FC within PA_NG911_Export FGDB")
write_log ("\n Update Full Street Name field in Centerline FC within PA_NG911_Export FGDB",logfile)

try:
    # Field Calculate Full Street Name field in Address Points (NG911 FGDB)
    arcpy.management.CalculateField(AddressPoint_NG911, "Full_Street_Name", "ifelse(!St_PreDir!,!St_Name!,!St_PosTyp!,!St_PosDir!)", "PYTHON3", """def ifelse(St_PreDir,St_Name,St_PosTyp,St_PosDir):
    if (St_PreDir and St_PosDir) is not None:
        return St_PreDir+" "+St_Name+" "+St_PosTyp+" "+St_PosDir
    elif (not St_PreDir) and (St_PosTyp and St_PosDir) is not None:
        return St_Name+" "+St_PosTyp+" "+St_PosDir
    elif not (St_PreDir and St_PosTyp) and (St_Name and St_PosDir) is not None:
        return St_Name+" "+St_PosDir
    elif not St_PosDir and (St_PreDir and St_Name and St_PosTyp) is not None:
        return St_PreDir+" "+St_Name+" "+St_PosTyp
    elif not (St_PreDir and St_PosDir) and (St_Name and St_PosTyp) is not None:
        return St_Name+" "+St_PosTyp
    elif not (St_PosTyp and St_PosDir) and (St_PreDir and St_Name) is not None:
        return St_PreDir+" "+St_Name
    else:
        return St_Name""", "TEXT", "NO_ENFORCE_DOMAINS")
    print ("\n     Full Street Name field updated in Address Point FC within PA_NG911_Export FGDB")
    write_log ("\n     Full Street Name field updated in Address Point FC within PA_NG911_Export FGDB",logfile)
except:
    print ("\n Unable to calculate Full Street Name field for Address Points within PA_NG911 FGDB")
    write_log("\n Unable to calculate Full Street Name field for Address Points within PA_NG911 FGDB", logfile)
    logging.exception('Got exception on calculate Full Street Name field for Address Points within PA_NG911 FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("\n Update Full Name field in Address Points FC within PA_NG911_Export FGDB")
write_log ("\n Update Full Name field in Address Points FC within PA_NG911_Export FGDB",logfile)

try:
    # Field Calculate Full Street Name field in Centerline (NG911 FGDB)
    arcpy.management.CalculateField(AddressPoint_NG911, "FullName", "ifelse(!Unit!,!Building!,!Add_Number!,!AddNum_Suf!,!Full_Street_Name!)", "PYTHON3", """def ifelse(Unit,Building,Add_Number,AddNum_Suf,Full_Street_Name):
    if not (Unit) and AddNum_Suf is not None:
        return str(Add_Number)+" "+AddNum_Suf+" "+Full_Street_Name
    elif (Unit and AddNum_Suf) is not None:
        return str(Add_Number)+" "+AddNum_Suf+" "+Full_Street_Name+" Unit: "+Unit
    elif not (AddNum_Suf) and Unit is not None:
        return str(Add_Number)+" "+Full_Street_Name+" Unit: "+Unit
    elif not (AddNum_Suf) and (Building and Unit) is not None:
        return str(Add_Number)+" "+Full_Street_Name+" Building: "+Building+" | Unit: "+Unit
    elif not (Building) and (AddNum_Suf and Unit) is not None:
        return str(Add_Number)+" "+AddNum_Suf+" "+Full_Street_Name+" Unit: "+Unit
    else:
        return str(Add_Number)+" "+Full_Street_Name""", "TEXT", "NO_ENFORCE_DOMAINS")

    print ("\n     Full Name field updated in Address Points FC within PA_NG911_Export FGDB")
    write_log ("\n     Full Name field updated in Address Points FC within PA_NG911_Export FGDB",logfile)
except:
    print ("\n Unable to calculate Full Name field updated in Address Points FC within PA_NG911 FGDB")
    write_log("\n Unable to calculate Full Name field updated in Address Points FC within PA_NG911 FGDB", logfile)
    logging.exception('Got exception on calculate Full Name field updated in Address Points FC within PA_NG911 FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Create DELETE_FILES FDS - for temp geoprocessing files
    arcpy.management.CreateFeatureDataset(PA_NG911_FGDB, "DELETE_FILES", 'PROJCS["NAD_1983_StatePlane_Pennsylvania_North_FIPS_3701_Feet",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",1968500.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",-77.75],PARAMETER["Standard_Parallel_1",40.88333333333333],PARAMETER["Standard_Parallel_2",41.95],PARAMETER["Latitude_Of_Origin",40.16666666666666],UNIT["Foot_US",0.3048006096012192]];-118829700 -96587800 3048.00609601219;-100000 10000;-100000 10000;3.28083333333333E-03;0.001;0.001;IsHighPrecision')
    print ("\n DELETE_FILES FDS created within PA_NG911_Export_YYYYMMDD geodatabase")
    write_log("\n DELETE_FILES FDS created within PA_NG911_Export_YYYYMMDD geodatabase",logfile)
except:
    print ("\n Unable to create DELETE_FILES FDS within PA_NG911_Export_YYYYMMDD geodatabase")
    write_log("\n Unable to create DELETE_FILES FDS within PA_NG911_Export_YYYYMMDD geodatabase", logfile)
    logging.exception('Got exception on creation of DELETE_FILES FDS within PA_NG911_Export_YYYYMMDD geodatabase logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Delete rows - Counties FC
    arcpy.management.DeleteRows(Counties_NG911)
    print ("\n Deleted rows in Counties_NG911 FC")
    write_log("\n Deleted rows in Counties_NG911 FC",logfile)
except:
    print ("\n Unable to Delete rows in Counties_NG911 FC")
    write_log("\n Unable to Delete rows in Counties_NG911 FC", logfile)
    logging.exception('Got exception on Delete rows in Counties_NG911 FC logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve ESZ Layer for new County Boundary
    arcpy.management.Dissolve(ESZ_PS, DELETE_FILES_NG911+"\\ESZ_DISSOLVE_DELETE", "COUNTY_NAME", None, "MULTI_PART", "DISSOLVE_LINES")
    print ("\n Dissolved ESZ FC into temp file")
    write_log("\n Dissolved ESZ FC into temp file",logfile)
except:
    print ("\n Unable to dissolve ESZ FC into temp file")
    write_log("\n Unable to dissolve ESZ FC into temp file", logfile)
    logging.exception('Got exception on dissolve ESZ FC into temp file" logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Temp ESZ dissolved FC into Counties_NG911
    arcpy.management.Append(ESZ_DISSOLVE, Counties_NG911, "NO_TEST", r'Shape_Leng "Shape_Leng" true true false 8 Double 0 0,First,#,'+ESZ_DISSOLVE+',SHAPE_Length,-1,-1;DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0,First,#;DateUpdate "DateUpdate" true true false 8 Date 0 0,First,#;Effective "Effective" true true false 8 Date 0 0,First,#;Expire "Expire" true true false 8 Date 0 0,First,#;CntyNGUID "CntyNGUID" true true false 254 Text 0 0,First,#;Country "Country" true true false 2 Text 0 0,First,#;State "State" true true false 2 Text 0 0,First,#;County "County" true true false 75 Text 0 0,First,#,'+ESZ_DISSOLVE+',COUNTY_NAME,0,50', '', "COUNTY_NAME = 'CRAWFORD'")
    print ("\n Appended Temp ESZ dissolved FC into Counties_NG911")
    write_log("\n Appended Temp ESZ dissolved FC into Counties_NG911",logfile)
except:
    print ("\n Unable to Append Temp ESZ dissolved FC into Counties_NG911")
    write_log("\n Unable to Append Temp ESZ dissolved FC into Counties_NG911", logfile)
    logging.exception('Got exception on Append Temp ESZ dissolved FC into Counties_NG911" logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calculate DateUpdate, Effective fields, DiscrpAgID, Country, State, CntyNGUID in Counties_NG911 FC
    arcpy.management.CalculateField(Counties_NG911, "DateUpdate", "datetime.datetime.now( )", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
    arcpy.management.CalculateField(Counties_NG911, "Effective", "datetime.datetime.now( )", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
    arcpy.management.CalculateField(Counties_NG911, "DiscrpAgID", '"crawford.state.pa.us"', "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
    arcpy.management.CalculateField(Counties_NG911, "CntyNGUID", '"42039"', "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
    arcpy.management.CalculateField(Counties_NG911, "Country", '"US"', "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
    arcpy.management.CalculateField(Counties_NG911, "State", '"PA"', "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")

    print("  DateUpdate, Effective, DiscrpAgID, Country, State & CntyNGUID fields updated...")
except:
    print ("\n Unable to calculate DateUpdate, Effective, DiscrpAgID, Country, State & CntyNGUID fields in Counties_CrawfordCo FC")
    write_log("Unable to calculate DateUpdate, Effective, DiscrpAgID, Country, State & CntyNGUID fields in Counties_CrawfordCo FC", logfile)
    logging.exception('Got exception on calculate DateUpdate, Effective, DiscrpAgID, Country, State & CntyNGUID fields in Counties_CrawfordCo FC logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("\n Replace Fire Department Coverage from Northern Tier FGDB from CRAW_INTERNAL excluding Spartansburg coverage in Erie County")
write_log("\n Replace Fire Department Coverage from Northern Tier FGDB from CRAW_INTERNAL excluding Spartansburg coverage in Erie County", logfile)

try:
    # Delete rows - Counties FC
    arcpy.management.DeleteRows(Fire_Department_NG911)
    print ("\n Deleted rows in Fire_Department_NG911 FC")
    write_log("\n Deleted rows in Fire_Department_NG911 FC",logfile)
except:
    print ("\n Unable to Delete rows in Fire_Department_NG911 FC")
    write_log("\n Unable to Delete rows in Fire_Department_NG911 FC", logfile)
    logging.exception('Got exception on Delete rows in Fire_Department_NG911 FC logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Fire Dept Coverage to Delete Files (create temporary fire dept feature in delete files FDS for manipulation into fire dept for NG911)
    FIRE_DEPT_COVERAGE_DELETE_NG911 = arcpy.conversion.FeatureClassToFeatureClass(FIRE_DEPT_COVERAGE_INTERNAL, DELETE_FILES_NG911, "FIRE_DEPT_COVERAGE_DELETE_NG911", "COUNTY_NAME = 'CRAWFORD'", r'FIRE_DEPT "FIRE DEPARTMENT" true true false 50 Text 0 0,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',FIRE_DEPT,0,50;FIRE_FDID "FIRE DEPARTMENT FDID CODE" true true false 15 Text 0 0,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',FIRE_FDID,0,15;FIRE_NUM "FIRE DEPARTMENT #" true true false 10 Text 0 0,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',FIRE_NUM,0,10;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',COUNTY_NAME,0,50;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',COUNTY_FIPS,-1,-1;GLOBALID "GLOBALID" false false true 38 GlobalID 0 0,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',GLOBALID,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',DiscrpAgID,0,75;STATE "State" true true false 2 Text 0 0,First,#,'+FIRE_DEPT_COVERAGE_INTERNAL+',STATE,0,2', '')
except:
    print ("\n Unable to export Fire Dept Coverage to Delete Files_NG911")
    write_log("Unable to export Fire Dept Coverage to Delete Files_NG911", logfile)
    logging.exception('Got exception on export Fire Dept Coverage to Delete Files_NG911 logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Add ID Field to FireDept_COVERAGE_DELETE
    arcpy.AddField_management(FIRE_DEPT_COVERAGE_DELETE_NG911, "ID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
except:
    print ("\n Unable to Add ID Field to FireDept_COVERAGE_DELETE")
    write_log("Unable to Add ID Field to FireDept_COVERAGE_DELETE", logfile)
    logging.exception('Got exception on Add ID Field to FireDept_COVERAGE_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
   
try:
    # Calculate ID Field FIRE_DEPT_COVERAGE_DELETE (calculate 20+FIRE_FDID into field)
    arcpy.CalculateField_management(FIRE_DEPT_COVERAGE_DELETE_NG911, "ID", '"20"+ !FIRE_FDID!', "PYTHON", "")
except:
    print ("\n Unable to Calculate ID Field FIRE_DEPT_COVERAGE_DELETE")
    write_log("Unable to Calculate ID Field FIRE_DEPT_COVERAGE_DELETE", logfile)
    logging.exception('Got exception on Calculate ID Field FIRE_DEPT_COVERAGE_DELETE logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
 
try:
    # Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to NG911 FGDB (append fire dept coverage manipulated from steps above to staging FGDB)
    arcpy.Append_management(FIRE_DEPT_COVERAGE_DELETE_NG911, Fire_Department_NG911, "NO_TEST", 'Description "Description" true true false 50 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',FIRE_DEPT,-1,-1;ID "ID" true true false 4 Long 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',ID,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',Shape_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',Shape_Area,-1,-1;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,'+FIRE_DEPT_COVERAGE_DELETE+',STATE,-1,-1', "")
except:
    print ("\n Unable to Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to NG911 FGDB")
    write_log("Unable to Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to NG911 FGDB", logfile)
    logging.exception('Got exception on Append FIRE_DEPT_COVERAGE_DELETE to Fire Department to NG911 FGDB logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()
   
print ("       Fire Department Coverage to Fire Department append completed")
write_log("       Fire Department Coverage to Fire Department append completed", logfile)

try:
    # Delete **Delete Files** feature dataset to save room (temporary files aren't needed for step 2 of process and take up additional room on file server when archiving prior exports)
    arcpy.Delete_management(DELETE_FILES_NG911)
    print ("\n Delete Files feature dataset has been deleted from PA NG911 FGDB")
except:
    print ("\n Unable to delete **Delete Files** feature dataset from PA NG911 FGDB")
    write_log("Unable to delete **Delete Files** feature dataset from PA NG911 FGDB", logfile)
    logging.exception('Got exception on delete **Delete Files** feature dataset from PA NG911 FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()


print ("       Waiting for script to release schema lock on FGDB...taking a 3 minute intermission, please wait")
write_log("       Waiting for script to release schema lock on FGDB...taking a 3 minute intermission, please wait",logfile)

#Wait 180 seconds (3 minutes) to release lock from FGDB
time.sleep(180)

print ("\n Renaming PA_NG911_Export_YYYYMMDD.gdb to PA_NG911_Export_" + date + ".gdb")
write_log("\n Renaming PA_NG911_Export_YYYYMMDD.gdb to PA_NG911_Export_" + date + ".gdb",logfile)

try:
    # Rename PA_NG911_Export_YYYYMMDD.gdb to FGDB with current date as file name (rename the YYYYMMDD portion of the FGDB name name to the current date in the same format)
    arcpy.management.Rename(PA_NG911_FGDB, r"\\CCFILE\\anybody\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier\\PA_NG911_Exports\\PA_NG911_Export_" + date + ".gdb", "Workspace")
except: 
    print ("\n Unable to rename PA_NG911_Export_YYYYMMDD.gdb to PA_NG911_Export_" + date + ".gdb")
    write_log("Unable to rename PA_NG911_Export_YYYYMMDD.gdb to  PA_NG911_Export_" + date + ".gdb", logfile)
    logging.exception('Got exception on rename PA_NG911_Export_YYYYMMDD.gdb to  PA_NG911_Export_" + date + ".gdb logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Renaming PA_NG911_Export_YYYYMMDD.gdb to PA_NG911_Export_" + date + ".gdb completed")
write_log("     Renaming PA_NG911_Export_YYYYMMDD.gdb to PA_NG911_Export_" + date + ".gdb completed",logfile)
    
end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("\n===================================================================")
print ("Northern Tier CAD Data Export to local staging DB & PA_NG911_Export FGDB completed: " + str(Day) + " " + str(end_time))
print (time.strftime("\n %H:%M:%S", time.gmtime(elapsed_time)))
print ("===================================================================")
write_log("\n Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)

print ("\n                   Northern Tier CAD Data Export to local staging DB & PA_NG911_Export FGDB completed // Connect Elk County VPN and run STEP 2 to process to Elk Staging DB")
print ("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+")
write_log("\n                   Northern Tier CAD Data Export to local staging DB & PA_NG911_Export FGDB completed // Connect Elk County VPN and run STEP 2 to process to Elk Staging DB", logfile)
write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+", logfile)

del arcpy
sys.exit()


