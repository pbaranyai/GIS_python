# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Parcel_Builder.py
# Created on: 2019-05-09 
# Updated on 2021-09-22
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
#
# Description: 
#  Build feature classes from AST workspace -> AUTO_WORKSPACE, and join in VISION tables:
#
# Building/Trailer Only
# Tax Parcels
# Blocks
# Inserts
# Sections
# Meadville Blocks
# Titusville Blocks
# ---------------------------------------------------------------------------

# Import modules
from __future__ import print_function, unicode_literals, absolute_import
import sys
import arcpy
import collections
import datetime
import os
import traceback
import logging
from arcpy import env

try:
    import urllib2  # Python 2
except ImportError:
    import urllib.request as urllib2  # Python 3

# Stop geoprocessing log history in metadata
arcpy.SetLogHistory(False)

# Setup error logging
logfile = r"R:\\GIS\\GIS_LOGS\\Assessment\\Parcel_Builder.log"  
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())

try:
    # Write Logfile
    def write_log(text, file):
        f = open(file, 'a')           # 'a' will append to an existing file if it exists
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    print ("\n Unable to write log file")
    write_log("Unable to write log file", logfile)
    sys.exit ()

#Database Connection Folder
Database_Connections = r"\\CCFILE\\anybody\\GIS\\ArcAutomations\\Database_Connections"

#Database variables:
AST = Database_Connections + "\\AST@ccsde.sde"
AUTOWORKSPACE = Database_Connections + "\\auto_workspace@ccsde.sde"
AUTOWORKSPACE_AST = Database_Connections + "\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment"
PUBLIC_WEB = Database_Connections + "\\public_web@ccsde.sde"


# Local variables:
BLOCKS_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Blocks"
BLOCKS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Blocks"
BUILDING_ONLY = AST + "\\AST.Crawford_Parcels\\AST.Building_Only"
BUILDING_ONLY_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Building_Only_Joined"
HARDLINES_AST = AST + "\\AST.Crawford_Parcels\\AST.Hardlines"
MAP_INSERTS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Map_Inserts"
MAP_INSERTS_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Map_Inserts"
MAP_SECTIONS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Map_Sections"
MAP_SECTIONS_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Map_Sections"
MDVL_BLOCKS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Meadville_Blocks"
MDVL_BLOCKS_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Meadville_Blocks"
PIN_AST = AST + "\\AST.Crawford_Parcels\\AST.PIN"
TAXPARCEL_JOINED_OLD_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Tax_Parcels_Joined_Old"
TAXPARCEL_JOINED_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Tax_Parcels_Joined"
TSVL_BLOCKS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Titusville_Blocks"
TSVL_BLOCKS_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Titusville_Blocks"
CAMA_RECORDS_TBL = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Assessment_CAMA_Records_Table"

# Local variable - tables
VISION_BLDGPERM_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_BLDGPERM_TBL"
VISION_LAND_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_LAND_TBL"
VISION_MAILADDRESS_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_MAILADDRESS_TBL"
VISION_OWNER_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_OWNER_TBL"
VISION_PARCEL_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_PARCEL_TBL"
VISION_REAL_OWNERSHIP_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_REAL_OWNERSHIP_TBL"
VISION_REALMAST_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL"
VISION_SALES_HISTORY_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_SALES_HISTORY_TBL"
VISION_OTHER_TBL_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL"
VISION_OWNER_TBL_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL"
VISION_TEMP_JOIN_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_TEMP_JOIN_TBL"
VISION_OWNER_TBL_WEBTemp = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL_WEBTemp"
VISIDATA_TEMP = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISIDATA_Temp"

start_time = time.time()

print ("============================================================================")
print ("Updating Assessment Datasets: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nBuilding/Trailer Only Feature Class") 
print ("Tax Parcels Feature Class")
print ("Blocks Feature Class")
print ("Inserts Feature Class")
print ("Sections Feature Class")
print ("Meadville Blocks Feature Class")
print ("Titusville Blocks Feature Class")
print ("Works in ArcGIS Pro")
print ("============================================================================")
write_log("============================================================================", logfile)
write_log("Updating Assessment Datasets: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nBuilding/Trailer Only Feature Class", logfile)
write_log("Tax Parcels Feature Class", logfile)
write_log("Blocks Feature Class", logfile)  
write_log("Inserts Feature Class", logfile) 
write_log("Sections Feature Class", logfile) 
write_log("Meadville Blocks Feature Class", logfile)
write_log("Titusville Blocks Feature Class", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Archiving Tax_Parcel_Joined to Tax_Parcel_Joined_Old - AUTO_WORKSPACE")
write_log("\n Archiving Tax_Parcel_Joined to Tax_Parcel_Joined_Old - AUTO_WORKSPACE: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Tax_Parcel_Joined_Old - AUTO_WORKSPACE, rename the current Tax_Parcel_Joined as old.
    if arcpy.Exists(TAXPARCEL_JOINED_OLD_AUTOWKSP):
        arcpy.Delete_management(TAXPARCEL_JOINED_OLD_AUTOWKSP, "FeatureClass")
    if arcpy.Exists(TAXPARCEL_JOINED_AUTOWKSP):
        arcpy.Rename_management(TAXPARCEL_JOINED_AUTOWKSP, TAXPARCEL_JOINED_OLD_AUTOWKSP, "FeatureClass")
except:
    print ("\n Unable to archive Tax_Parcel_Joined to Tax_Parcel_Joined_Old - AUTO_WORKSPACE")
    write_log("\n Unable to archive Tax_Parcel_Joined to Tax_Parcel_Joined_Old - AUTO_WORKSPACE", logfile)
    logging.exception('Got exception on archive Tax_Parcel_Joined to Tax_Parcel_Joined_Old - AUTO_WORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Archiving Tax_Parcel_Joined to Tax_Parcel_Joined_Old - AUTO_WORKSPACE completed")
write_log("       Archiving Tax_Parcel_Joined to Tax_Parcel_Joined_Old - AUTO_WORKSPACE completed", logfile)

print ("\n Creating Tax Parcels from Hardlines and PINs - Tax_Parcel_Joined - AUTO_WORKSPACE")
write_log("\n Creating Tax Parcels from Hardlines and PINs - Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)

try:
    # Create tax parcels from hardlines (TAX_PARCEL_TEMP) - creating polygons from hardlines
    TAX_PARCEL_TEMP = arcpy.FeatureToPolygon_management(HARDLINES_AST, "in_memory/TAX_PARCEL_TEMP", "","NO_ATTRIBUTES", "")
except:
    print ("\n Unable to create tax parcels from hardlines (TAX_PARCEL_TEMP)")
    write_log("\n Unable to create tax parcels from hardlines (TAX_PARCEL_TEMP)", logfile)
    logging.exception('Got exception on Unable to create tax parcels from hardlines (TAX_PARCEL_TEMP) logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Join TAX_PARCEL_TEMP to PIN feature class - joining in basic information (including PID) to polygons created via hardlines.  Once PID is part of polygon, will be able to join vision records to polygons to make parcels.
    TAX_PARCEL_TEMP_JOIN = arcpy.SpatialJoin_analysis(TAX_PARCEL_TEMP, PIN_AST, "in_memory/TAX_PARCEL_TEMP_JOIN", "JOIN_ONE_TO_ONE", "KEEP_ALL", 'SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#,in_memory/TAX_PARCEL_TEMP,SHAPE_Length,-1,-1;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#,in_memory/TAX_PARCEL_TEMP,SHAPE_Area,-1,-1;CAMA_PIN "CAMA_PIN" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,CAMA_PIN,-1,-1;MAP "MAP" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,MAP,-1,-1;PARCEL "PARCEL" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,PARCEL,-1,-1;LOT "LOT" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,LOT,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,GLOBALID,-1,-1;ID_PIN "ID_PIN" true true false 2 Short 0 5 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,ID_PIN,-1,-1;MAPTYPE "MAPTYPE" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,MAPTYPE,-1,-1;CITY "CITY" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,CITY,-1,-1;MEADVILLE "MEADVILLE" true true false 10 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,MEADVILLE,-1,-1;TITUSVILLE "TITUSVILLE" true true false 10 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,TITUSVILLE,-1,-1;EDITOR "EDITOR" false true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,EDITOR,-1,-1;DATEMODIFY "DATEMODIFY" false true false 8 Date 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,DATEMODIFY,-1,-1;LANDEX_URL_TYPE "Landex URL Type" true true false 20 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,LANDEX_URL_TYPE,-1,-1;PLANS_AVAILABLE "Plans Available" true true false 5 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,PLANS_AVAILABLE,-1,-1;BLK_MAP "Block Map" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,BLK_MAP,-1,-1;BLK_PARCEL "Block Parcel" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,BLK_PARCEL,-1,-1;BLK_MAPTYPE "Block Maptype" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,BLK_MAPTYPE,-1,-1;INS_MAP "Insert Map" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,INS_MAP,-1,-1;INS_DESCRIPTION "Insert Description" true true false 255 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,INS_DESCRIPTION,-1,-1;INS_SECTION_MAP "Insert Section Map" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,INS_SECTION_MAP,-1,-1;INS_SCALE "Insert Scale" true true false 8 Double 8 38 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,INS_SCALE,-1,-1;INS_ROTATION "Insert Rotation" true true false 8 Double 8 38 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,INS_ROTATION,-1,-1;SEC_MAP "Section Map" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,SEC_MAP,-1,-1;SEC_MUNI_NAME "Municipal Name" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,SEC_MUNI_NAME,-1,-1;SEC_ANGLE "Section Angle" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,SEC_ANGLE,-1,-1;SEC_SCALE "Section Scale" true true false 8 Double 8 38 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,SEC_SCALE,-1,-1;SEC_ROTATION "Section Rotation" true true false 8 Double 8 38 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,SEC_ROTATION,-1,-1;SEC_WARD "Section Ward" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,SEC_WARD,-1,-1;MDVL_BLK_MAP "Meadville Block Map" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,MDVL_BLK_MAP,-1,-1;MDVL_BLK_PARCEL "Meadvile Block Parcel" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,MDVL_BLK_PARCEL,-1,-1;MDVL_BLK_MAPTYPE "Meadvile Block Maptype" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,MDVL_BLK_MAPTYPE,-1,-1;TSVL_BLK_MAP "Titusville Block Map" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,TSVL_BLK_MAP,-1,-1;TSVL_BLK_PARCEL "Titusville Block Parcel" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,TSVL_BLK_PARCEL,-1,-1;TSVL_BLK_MAPTYPE "Titusville Block Maptype" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,TSVL_BLK_MAPTYPE,-1,-1;TSVL_BLK_ID "Titusville Block ID" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,TSVL_BLK_ID,-1,-1;UPI "UPI #" true true false 60 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,UPI,-1,-1;PID "PID" true true false 4 Long 0 10 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,PID,-1,-1;LONGITUDE_X "Longitude-X" true true false 8 Double 8 38 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,LONGITUDE_X,-1,-1;LATITUDE_Y "Latitude-Y" true true false 8 Double 8 38 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.PIN,LATITUDE_Y,-1,-1', "INTERSECT", "", "")
except:
    print ("\n Unable to Join TAX_PARCEL_TEMP to PIN feature class")
    write_log("\n Unable to Join TAX_PARCEL_TEMP to PIN feature class", logfile)
    logging.exception('Got exception on Join TAX_PARCEL_TEMP to PIN feature class logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Delete excess fields from TAX_PARCEL_TEMP_JOIN  (Delete extra fields from AST.PIN)
    arcpy.DeleteField_management(TAX_PARCEL_TEMP_JOIN, "Join_Count;TARGET_FID;EDITOR")
except:
    print ("\n Unable to delete excess fields from TAX_PARCEL_TEMP_JOIN")
    write_log("\n Unable to delete excess fields from TAX_PARCEL_TEMP_JOIN", logfile)
    logging.exception('Got exception on delete excess fields from TAX_PARCEL_TEMP_JOIN logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Dissolve TAX_PARCEL_TEMP_JOIN - in_memory to Tax_Parcel_Joined - AUTO_WORKSPACE  (joins parcels that are hooked together by softline hooks - dissolved by identical data in fields)
    arcpy.Dissolve_management(TAX_PARCEL_TEMP_JOIN, TAXPARCEL_JOINED_AUTOWKSP, "CAMA_PIN;MAP;PARCEL;LOT;ID_PIN;MAPTYPE;CITY;MEADVILLE;TITUSVILLE;LANDEX_URL_TYPE;PLANS_AVAILABLE;BLK_MAP;BLK_PARCEL;BLK_MAPTYPE;INS_MAP;INS_DESCRIPTION;INS_SECTION_MAP;INS_SCALE;INS_ROTATION;SEC_MAP;SEC_MUNI_NAME;SEC_ANGLE;SEC_SCALE;SEC_ROTATION;SEC_WARD;MDVL_BLK_MAP;MDVL_BLK_PARCEL;MDVL_BLK_MAPTYPE;TSVL_BLK_MAP;TSVL_BLK_PARCEL;TSVL_BLK_MAPTYPE;TSVL_BLK_ID;PID", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to Dissolve TAX_PARCEL_TEMP_JOIN - in_memory to Tax_Parcel_Joined - AUTO_WORKSPACE")
    write_log("\n Unable to Dissolve TAX_PARCEL_TEMP_JOIN - in_memory to Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)
    logging.exception('Got exception on Dissolve TAX_PARCEL_TEMP_JOIN - in_memory to Tax_Parcel_Joined - AUTO_WORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for next process
    arcpy.Delete_management("in_memory")
except:
    print ("\n Unable to clear TAX_PARCEL_TEMP from in_memory")
    write_log("\n Unable to clear TAX_PARCEL_TEMP from in_memory", logfile)
    logging.exception('Got exception on clear TAX_PARCEL_TEMP from in_memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Creating Tax Parcels from Hardlines and PINs - Tax_Parcel_Joined - AUTO_WORKSPACE completed")
write_log("       Creating Tax Parcels from Hardlines and PINs - Tax_Parcel_Joined - AUTO_WORKSPACE completed", logfile)

print ("\n Joining VISION tables to Tax_Parcel_Joined - AUTO_WORKSPACE")
write_log("\n Joining VISION tables to Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)

try:
    # Join VISIDATA_TEMP to Tax_Parcel_Joined - AUTO_WORKSPACE  (joins vision data from above steps to polygons created by hardlines)
    arcpy.management.JoinField(TAXPARCEL_JOINED_AUTOWKSP, "PID", VISIDATA_TEMP, "REM_PID", None)
    print ("   VISION_OWNER_TBL joined to Tax_Parcel_Joined...")
    write_log("   VISION_OWNER_TBL joined to Tax_Parcel_Joined...", logfile)
except:
    print ("\n Unable to join VISIDATA_TEMP to Tax_Parcel_Joined - AUTO_WORKSPACE")
    write_log("\n Unable to join VISIDATA_TEMP to Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)
    logging.exception('Got exception on join VISIDATA_TEMP to Tax_Parcel_Joined - AUTO_WORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Add GIS_ACRES field to Tax_Parcel_Joined - AUTO_WORKSPACE 
    arcpy.AddField_management(TAXPARCEL_JOINED_AUTOWKSP, "GIS_ACRES", "DOUBLE", "", "", "", "GIS Calculated Acres - not legal", "NULLABLE", "NON_REQUIRED", "")
    print ("    GIS Acres field added to Tax Parcel Joined - AUTO_WORKSPACE")
    write_log("    GIS Acres field added to Tax Parcel Joined - AUTO_WORKSPACE",logfile)
except:
    print ("\n Unable to Add GIS_ACRES field to Tax_Parcel_Joined - AUTO_WORKSPACE")
    write_log("\n Unable to Add GIS_ACRES field to Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)
    logging.exception('Got exception on Add GIS_ACRES field to Tax_Parcel_Joined - AUTO_WORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
try:
    # Calculate GIS_ACRES field in Tax_Parcel_Joined - AUTO_WORKSPACE from polygon shape acres  (adds GIS acres field - for QA/QC process of checking actual acreage from vision against polygon acreage.  will not be 100%, however large variances can be caught)
    arcpy.CalculateField_management(TAXPARCEL_JOINED_AUTOWKSP, "GIS_ACRES", "!shape.area@acres!", "PYTHON", "")
    TaxParcel_result = arcpy.GetCount_management(TAXPARCEL_JOINED_AUTOWKSP)
    print ('    {} has {} records calculated'.format(TAXPARCEL_JOINED_AUTOWKSP, TaxParcel_result[0]))
    write_log('    {} has {} records calculated'.format(TAXPARCEL_JOINED_AUTOWKSP, TaxParcel_result[0]), logfile)
except:
    print ("\n Unable to Calculate GIS_ACRES field in Tax_Parcel_Joined - AUTO_WORKSPACE from polygon shape acres")
    write_log("\n Unable to Calculate GIS_ACRES field in Tax_Parcel_Joined - AUTO_WORKSPACE from polygon shape acres", logfile)
    logging.exception('Got exception on Calculate GIS_ACRES field in Tax_Parcel_Joined - AUTO_WORKSPACE from polygon shape acres logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Add Landex_URL field to Tax_Parcel_Joined - AUTO_WORKSPACE
    arcpy.AddField_management(TAXPARCEL_JOINED_AUTOWKSP, "LANDEX_URL", "TEXT", "", "", "600", "Landex URL", "NULLABLE", "NON_REQUIRED", "")
    print ("     Landex URL field added to Tax Parcel Joined - AUTO_WORKSPACE")
    write_log("     Landex URL field added to Tax Parcel Joined - AUTO_WORKSPACE",logfile)
except:
    print ("\n Unable to Add Landex_URL field to Tax_Parcel_Joined - AUTO_WORKSPACE")
    write_log("\n Unable to Add Landex_URL field to Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)
    logging.exception('Got exception on Add Landex_URL field to Tax_Parcel_Joined - AUTO_WORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
try:
    # Calculate Landex URL Field in Tax_Parcel_Joined - AUTO_WORKSPACE (calculates custom URL per record for landex use based on fields from parcels)
    URLFIELDS = ['LANDEX_URL','SLH_BOOK','SLH_PAGE',str('REM_MBLU_MAP'),str('REM_MBLU_BLOCK'),str('REM_MBLU_LOT'),'PID','LANDEX_URL_TYPE']
    cursor =  arcpy.da.UpdateCursor(TAXPARCEL_JOINED_AUTOWKSP,URLFIELDS)
    for row in cursor:
        if  row[6] == None:
            continue
        if (row[7] == 'Book_Page' and row[6] > 0):
            row[0] = "http://172.16.154.36/SearchResultsList.asp?bookNumber={}&pageNumber={}&submit=SEARCH&forwardRequest=SearchResultsList.asp&displayPage=1&displayItemsPerPage=50&maximumMatches=1000&getCustomerData=TRUE".format(row[1],row[2])
            cursor.updateRow(row)
        if  row[6] == None:
            continue
        if (row[7] == 'UPI' and row[6] > 0):
            row[0] = "http://172.16.154.36/SearchResultsList.asp?parcelNumber1=20&parcelNumber2={}&parcelNumber3={}&parcelNumber4={}&parcelNumber5={}&submit=SEARCH&parcelNumberFieldCount=5&parcelNumberFormat=2+4+3+17+6+&forwardRequest=SearchResultsList.asp&displayPage=1&displayItemsPerPage=50&maximumMatches=1000&getCustomerData=TRUE".format(row[3],row[4],row[5],row[6])
            cursor.updateRow(row)
        if (row[7] == None):
            row = ""
            pass
        else:
            pass
    del row 
    del cursor
    print ("      Landex URL field calculated")
    write_log("      Landex URL field calculated",logfile)
except:
    print ("\n Unable to calculate Landex URL Field in Tax_Parcel_Joined - AUTO_WORKSPACE")
    write_log("\n Unable to calculate Landex URL Field in Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)
    logging.exception('Got exception on calculate Landex URL Field in Tax_Parcel_Joined - AUTO_WORKSPACE with MBLU logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()

print ("       Joining VISION tables to Tax_Parcel_Joined - AUTO_WORKSPACE completed")
write_log("       Joining VISION tables to Tax_Parcel_Joined - AUTO_WORKSPACE completed", logfile)

print ("\n Joining Lat/Long fields to Tax_Parcel_Joined - AUTO_WORKSPACE from PIN - AST")
write_log("\n Joining Lat/Long fields to Tax_Parcel_Joined - AUTO_WORKSPACE from PIN - AST", logfile)

try:
    # Joining Lat/Long fields to Tax_Parcel_Joined - AUTO_WORKSPACE from PIN - AST
    arcpy.JoinField_management(TAXPARCEL_JOINED_AUTOWKSP, "PID", PIN_AST, "PID", "LONGITUDE_X;LATITUDE_Y")
    print ("     Lat/Long fields joined to Tax Parcel Joined - AUTO_WORKSPACE from PIN - AST")
    write_log("     Lat/Long fields joined to Tax Parcel Joined - AUTO_WORKSPACE from PIN - AST",logfile)
except:
    print ("\n Unable to Add Lat/Long fields joined to Tax Parcel Joined - AUTO_WORKSPACE from PIN - AST")
    write_log("\n Unable to Add Lat/Long fields joined to Tax Parcel Joined - AUTO_WORKSPACE from PIN - AST", logfile)
    logging.exception('Got exception on Add Lat/Long fields joined to Tax Parcel Joined - AUTO_WORKSPACE from PIN - AST logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("        Joining Lat/Long fields to Tax_Parcel_Joined - AUTO_WORKSPACE from PIN - AST completed")
write_log("        Joining Lat/Long fields to Tax_Parcel_Joined - AUTO_WORKSPACE from PIN - AST completed", logfile)

print ("\n Creating BUILDING_ONLY_JOINED - AUTOWORKSPACE from BUILDING_ONLY - AST & VISION tables")
write_log("\n Creating BUILDING_ONLY_JOINED - AUTOWORKSPACE from BUILDING_ONLY - AST & VISION tables", logfile)

try:
    # Delete rows from Building_Only_Joined
    arcpy.DeleteRows_management(BUILDING_ONLY_AUTOWKSP)
except:
    print ("\n Unable to delete rows from Building_Only_Joined")
    write_log("\n Unable to delete rows from Building_Only_Joined", logfile)
    logging.exception('Got exception on delete rows from Building_Only_Joined logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Make temporary feature class from Building/Trailer Only (creates temporary file of building only points from assessment workspace)
    Building_Only_Temp = arcpy.FeatureClassToFeatureClass_conversion(BUILDING_ONLY, AUTOWORKSPACE_AST, "Building_Only_Temp", "", 'REM_PID "REM_PID" true true false 8 Double 8 38 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Building_Only,REM_PID,-1,-1;EDITOR "EDITOR" false true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Building_Only,EDITOR,-1,-1;DATEMODIFY "DATEMODIFY" false true false 8 Date 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Building_Only,DATEMODIFY,-1,-1;CAMA_PIN "CAMA_PIN" true true false 50 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Building_Only,CAMA_PIN,-1,-1;LONGITUDE_X "Longitude-X" true true false 8 Double 8 38 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Building_Only,LONGITUDE_X,-1,-1;LATITUDE_Y "Latitude-Y" true true false 8 Double 8 38 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Building_Only,LATITUDE_Y,-1,-1', "")
except:
    print ("\n Unable to make temporary feature class from Building/Trailer Only")
    write_log("\n Unable to make temporary feature class from Building/Trailer Only", logfile)
    logging.exception('Got exception on make temporary feature class from Building/Trailer Only logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Join Building_Only_Temp to VISIDATA_TEMP (joins building only points from assessment workspace to vision data)
    arcpy.JoinField_management(Building_Only_Temp, "REM_PID", VISIDATA_TEMP, "REM_PID", "REM_PIN;REM_OWN_NAME;REM_PRCL_LOCN;REM_PRCL_LOCN_CITY;REM_PRCL_LOCN_STT;REM_PRCL_LOCN_ZIP;REM_ALT_PRCL_ID;REM_PRCL_STATUS_DATE;REM_MBLU_MAP;REM_MBLU_MAP_CUT;REM_MBLU_BLOCK;REM_MBLU_BLOCK_CUT;REM_MBLU_LOT;REM_MBLU_LOT_CUT;REM_MBLU_UNIT;REM_MBLU_UNIT_CUT;REM_STATUS_DATE;REM_INET_SUPPRESS;REM_IS_CONDO_MAIN;REM_CMPLX_NAME;REM_BLDG_NAME;REM_USE_CODE;REM_LEGAL_AREA;REM_LAST_UPDATE;REM_USRFLD;REM_USRFLD_DESC;PID_TEXT;LND_USE_CODE;LND_USE_DESC;LND_DSTRCT;MUNI_NAME;PRC_PF_LOCN;PRC_PF_LOCN_DESC;PRC_USRFLD_09;PRC_USRFLD_10;PRC_TTL_ASSESS_BLDG;PRC_TTL_ASSESS_IMPROVEMENTS;PRC_TTL_ASSESS_LND;PRC_TTL_ASSESS_OB;PRC_VALUE;PRC_CMPLX_PID;PRC_CMPLX_DESC;PRC_CENSUS;PRC_TTL_MRKT_ASSESS;PRC_TTL_ASSESS;OWN_ID;OWN_NAME1;OWN_NAME2;ROW_PID;ROW_OWN_ID;ROW_LINE_NUM;ROW_OWN_PCT;ROW_PRIMARY;ROW_CREATE_DATE;ROW_MAD_ID;ROW_MAD_ISPRIMARY;OWN_LINE;MAD_MAIL_NAME1;MAD_MAIL_NAME2;MAD_MAIL_ADDR1;MAD_MAIL_CITY;MAD_MAIL_STATE;MAD_MAIL_ZIP;MAD_MAIL_ADDR2;MAD_ID;SLH_PID;SLH_LINE_NUM;SLH_SALE_DATE;SLH_BOOK;SLH_PAGE;SLH_PRICE;SLH_CURRENT_OWNER")
    print ("  VISIDATA_TEMP joined to Building_Only_Temp...")
    write_log("  VISIDATA_TEMP joined to Building_Only_Temp...", logfile)
except:
    print ("\n Unable to join Building_Only_Temp to VISIDATA_TEMP")
    write_log("\n Unable to join Building_Only_Temp to VISIDATA_TEMP", logfile)
    logging.exception('Got exception on join Building_Only_Temp to VISIDATA_TEMP logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append from Building_Only_Temp to Building_Only_Joined (appends temporary file of buidling only points and vision data to "real" feature class)
    arcpy.Append_management(Building_Only_Temp, BUILDING_ONLY_AUTOWKSP, "NO_TEST", 'REM_PID "REM_PID" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PID,-1,-1;EDITOR "EDITOR" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,EDITOR,-1,-1;DATEMODIFY "DATEMODIFY" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,DATEMODIFY,-1,-1;CAMA_PIN "CAMA_PIN" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,CAMA_PIN,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PIN,-1,-1;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "Lot" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_BLDG_NAME,-1,-1;REM_USE_CODE "Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_USE_CODE,-1,-1;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_USRFLD,-1,-1;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_USRFLD_DESC,-1,-1;PID_TEXT "PID Text format" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PID_TEXT,-1,-1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,LND_USE_CODE,-1,-1;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,LND_DSTRCT,-1,-1;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_PF_LOCN,-1,-1;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_PF_LOCN_DESC,-1,-1;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_ASSESS,-1,-1;OWN_ID "OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,OWN_NAME2,-1,-1;ROW_PID "ROW_PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,OWN_LINE,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_ADDR2,-1,-1;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_BOOK,-1,-1;SLH_PAGE "Deed Page" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_PAGE,-1,-1;SLH_PRICE "Sale Price" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_CURRENT_OWNER,-1,-1;LONGITUDE_X "Longitude_X" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,LONGITUDE_X,-1,-1;LATITUDE_Y "Latitude_Y" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,LATITUDE_Y,-1,-1;MUNI_NAME "Municipality Name" true true false 75 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MUNI_NAME,-1,-1', "")
    BuildingOnly_result = arcpy.GetCount_management(BUILDING_ONLY_AUTOWKSP)
    print ('{} has {} records'.format(BUILDING_ONLY_AUTOWKSP, BuildingOnly_result[0]))
    write_log('{} has {} records'.format(BUILDING_ONLY_AUTOWKSP, BuildingOnly_result[0]), logfile)
except:
    print ("\n Unable to append from Building_Only_Join_Layer to Building_Only_Joined")
    write_log("\n Unable to append from Building_Only_Join_Layer to Building_Only_Joined", logfile)
    logging.exception('Got exception on append from Building_Only_Join_Layer to Building_Only_Joined logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Delete Building_Only_Temp (cleanup temporary files from workspace)
    arcpy.Delete_management(Building_Only_Temp)
    print ("   Building_Only_Temp deleted...")
    write_log("   Building_Only_Temp deleted...",logfile)
except:
    print ("\n Unable to delete Building_Only_Temp")
    write_log("\n Unable to delete Building_Only_Temp", logfile)
    logging.exception('Got exception on delete Building_Only_Temp logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Creating BUILDING_ONLY_JOINED - AUTOWORKSPACE from BUILDING_ONLY - AST & VISION tables completed")
write_log("       Creating BUILDING_ONLY_JOINED - AUTOWORKSPACE from BUILDING_ONLY - AST & VISION tables completed", logfile)

## The following steps are for creation of Blocks, Inserts, Sections, Meadville Blocks, and Titusville Blocks -- used for tax map automation/printing ##

print ("\n Creating Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE")
write_log("\n Creating Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)

try:
    # Delete rows Blocks - AUTOWORKSPACE
    arcpy.DeleteRows_management(BLOCKS_AST)
except:
    print ("\n Unable to delete rows Blocks - AUTOWORKSPACE")
    write_log("Unable to delete rows Blocks - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on delete rows Blocks - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting BLK_MAP IS NOT NULL) // (make temporary feature of tax parcels - which contains information to create blocks in following steps)
    PARCEL_BLOCK_View = arcpy.MakeFeatureLayer_management(TAXPARCEL_JOINED_AUTOWKSP, "PARCEL_BLOCK_View", "BLK_MAP IS NOT NULL", "", "OBJECTID OBJECTID VISIBLE NONE;CAMA_PIN CAMA_PIN VISIBLE NONE;MAP MAP VISIBLE NONE;PARCEL PARCEL VISIBLE NONE;LOT LOT VISIBLE NONE;ID_PIN ID_PIN VISIBLE NONE;MAPTYPE MAPTYPE VISIBLE NONE;CITY CITY VISIBLE NONE;MEADVILLE MEADVILLE VISIBLE NONE;TITUSVILLE TITUSVILLE VISIBLE NONE;BLK_MAP BLK_MAP VISIBLE NONE;BLK_PARCEL BLK_PARCEL VISIBLE NONE;BLK_MAPTYPE BLK_MAPTYPE VISIBLE NONE;INS_MAP INS_MAP VISIBLE NONE;INS_DESCRIPTION INS_DESCRIPTION VISIBLE NONE;INS_SECTION_MAP INS_SECTION_MAP VISIBLE NONE;INS_SCALE INS_SCALE VISIBLE NONE;INS_ROTATION INS_ROTATION VISIBLE NONE;SEC_MAP SEC_MAP VISIBLE NONE;SEC_MUNI_NAME SEC_MUNI_NAME VISIBLE NONE;SEC_ANGLE SEC_ANGLE VISIBLE NONE;SEC_SCALE SEC_SCALE VISIBLE NONE;SEC_ROTATION SEC_ROTATION VISIBLE NONE;SEC_WARD SEC_WARD VISIBLE NONE;MDVL_BLK_MAP MDVL_BLK_MAP VISIBLE NONE;MDVL_BLK_PARCEL MDVL_BLK_PARCEL VISIBLE NONE;MDVL_BLK_MAPTYPE MDVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_MAP TSVL_BLK_MAP VISIBLE NONE;TSVL_BLK_PARCEL TSVL_BLK_PARCEL VISIBLE NONE;TSVL_BLK_MAPTYPE TSVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_ID TSVL_BLK_ID VISIBLE NONE;PID PID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;GIS_ACRES GIS_ACRES VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print ("\n Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting BLK_MAP IS NOT NULL)")
    write_log("Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting BLK_MAP IS NOT NULL)", logfile)
    logging.exception('Got exception on make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting BLK_MAP IS NOT NULL) logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve PARCEL_BLOCK_View (dissolves like features in tax parcels, keeping only fields needed for blocks)
    arcpy.Dissolve_management(PARCEL_BLOCK_View, "in_memory/Blocks_Dissolve", "BLK_MAP;BLK_PARCEL;BLK_MAPTYPE", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to Dissolve PARCEL_BLOCK_View")
    write_log("Unable to Dissolve PARCEL_BLOCK_View", logfile)
    logging.exception('Got exception on Dissolve PARCEL_BLOCK_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append PARCEL_BLOCK_View to Blocks - AUTOWORKSPACE (append temporary layer created from steps above into "real" feature class)
   arcpy.Append_management("in_memory/Blocks_Dissolve", BLOCKS_AST, "NO_TEST", 'MAP "MAP" true true false 50 Text 0 0 ,First,#,"in_memory/Blocks_Dissolve",BLK_MAP,-1,-1;PARCEL "PARCEL" true true false 50 Text 0 0 ,First,#,"in_memory/Blocks_Dissolve",BLK_PARCEL,-1,-1;MAPTYPE "MAPTYPE" true true false 50 Text 0 0 ,First,#,"in_memory/Blocks_Dissolve",BLK_MAPTYPE,-1,-1;EDITOR "EDITOR" true true false 50 Text 0 0 ,First,#;DATEMODIFY "DATEMODIFY" true true false 8 Date 0 0 ,First,#;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#', "")
   BLOCKS_result = arcpy.GetCount_management(BLOCKS_AST)
   print ('{} has {} records'.format(BLOCKS_AST, BLOCKS_result[0]))
   write_log('{} has {} records'.format(BLOCKS_AST, BLOCKS_result[0]), logfile)
except:
    print ("\n Unable to Append PARCEL_BLOCK_View to Blocks - AUTOWORKSPACE")
    write_log("Unable to Append PARCEL_BLOCK_View to Blocks - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on Append PARCEL_BLOCK_View to Blocks - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" & PARCEL_BLOCK_View for next process
    arcpy.Delete_management("in_memory")
    arcpy.Delete_management(PARCEL_BLOCK_View)  
except:
    print ("\n Unable to clear Blocks_Dissolve from in_memory & PARCEL_BLOCK_View")
    write_log("Unable to clear Blocks_Dissolve from in_memory & PARCEL_BLOCK_View", logfile)
    logging.exception('Got exception on clear Blocks_Dissolve from in_memory & PARCEL_BLOCK_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Creating Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE completed")
write_log("       Creating Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE completed", logfile)

print ("\n Creating Map Inserts - AST from Tax_Parcel_Joined - AUTO_WORKSPACE")
write_log("\n Creating Map Inserts - AST from Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)

try:
    # delete rows Map Inserts - AUTOWORKSPACE
    arcpy.DeleteRows_management(MAP_INSERTS_AST)
except:
    print ("\n Unable to delete rows Map Inserts - AUTOWORKSPACE")
    write_log("Unable to delete rows Map Inserts - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on delete rows Map Inserts - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting INS_MAP IS NOT NULL) // (make temporary feature of tax parcels - which contains information to create inserts in following steps)
    PARCEL_INSERT_View = arcpy.MakeFeatureLayer_management(TAXPARCEL_JOINED_AUTOWKSP, "PARCEL_INSERT_View", "INS_MAP IS NOT NULL", "", "OBJECTID OBJECTID VISIBLE NONE;CAMA_PIN CAMA_PIN VISIBLE NONE;MAP MAP VISIBLE NONE;PARCEL PARCEL VISIBLE NONE;LOT LOT VISIBLE NONE;ID_PIN ID_PIN VISIBLE NONE;MAPTYPE MAPTYPE VISIBLE NONE;CITY CITY VISIBLE NONE;MEADVILLE MEADVILLE VISIBLE NONE;TITUSVILLE TITUSVILLE VISIBLE NONE;BLK_MAP BLK_MAP VISIBLE NONE;BLK_PARCEL BLK_PARCEL VISIBLE NONE;BLK_MAPTYPE BLK_MAPTYPE VISIBLE NONE;INS_MAP INS_MAP VISIBLE NONE;INS_DESCRIPTION INS_DESCRIPTION VISIBLE NONE;INS_SECTION_MAP INS_SECTION_MAP VISIBLE NONE;INS_SCALE INS_SCALE VISIBLE NONE;INS_ROTATION INS_ROTATION VISIBLE NONE;SEC_MAP SEC_MAP VISIBLE NONE;SEC_MUNI_NAME SEC_MUNI_NAME VISIBLE NONE;SEC_ANGLE SEC_ANGLE VISIBLE NONE;SEC_SCALE SEC_SCALE VISIBLE NONE;SEC_ROTATION SEC_ROTATION VISIBLE NONE;SEC_WARD SEC_WARD VISIBLE NONE;MDVL_BLK_MAP MDVL_BLK_MAP VISIBLE NONE;MDVL_BLK_PARCEL MDVL_BLK_PARCEL VISIBLE NONE;MDVL_BLK_MAPTYPE MDVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_MAP TSVL_BLK_MAP VISIBLE NONE;TSVL_BLK_PARCEL TSVL_BLK_PARCEL VISIBLE NONE;TSVL_BLK_MAPTYPE TSVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_ID TSVL_BLK_ID VISIBLE NONE;PID PID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;GIS_ACRES GIS_ACRES VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print ("\n Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting INS_MAP IS NOT NULL)")
    write_log("Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting INS_MAP IS NOT NULL)", logfile)
    logging.exception('Got exception on make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting INS_MAP IS NOT NULL) logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve PARCEL_INSERT_View (dissolves like features in tax parcels, keeping only fields needed for inserts)
    Inserts_Dissolve = arcpy.Dissolve_management(PARCEL_INSERT_View, "in_memory/Inserts_Dissolve", "INS_MAP;INS_DESCRIPTION;INS_SECTION_MAP;INS_SCALE;INS_ROTATION", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to Dissolve PARCEL_INSERT_View")
    write_log("Unable to Dissolve PARCEL_INSERT_View", logfile)
    logging.exception('Got exception on Dissolve PARCEL_INSERT_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append PARCEL_INSERT_View to Inserts - AUTOWORKSPACE (append temporary layer created from steps above into "real" feature class)
   arcpy.Append_management("in_memory/Inserts_Dissolve", MAP_INSERTS_AST, "NO_TEST", 'MAP "MAP" true true false 50 Text 0 0 ,First,#,"in_memory/Inserts_Dissolve",INS_MAP,-1,-1;INSERT_DESCRIPTION "INSERT_DESCRIPTION" true true false 255 Text 0 0 ,First,#,"in_memory/Inserts_Dissolve",INS_DESCRIPTION,-1,-1;EDITOR "EDITOR" true true false 50 Text 0 0 ,First,#;DATE_MODIFY "DATE_MODIFY" true true false 8 Date 0 0 ,First,#;SECTION_MAP "SECTION_MAP" true true false 15 Text 0 0 ,First,#,"in_memory/Inserts_Dissolve",INS_SECTION_MAP,-1,-1;SCALE "SCALE" true true false 8 Double 8 38 ,First,#,"in_memory/Inserts_Dissolve",INS_SCALE,-1,-1;ROTATION "ROTATION" true true false 8 Double 8 38 ,First,#,"in_memory/Inserts_Dissolve",INS_ROTATION,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#', "")
   INSERTS_result = arcpy.GetCount_management(MAP_INSERTS_AST)
   print ('{} has {} records'.format(MAP_INSERTS_AST, INSERTS_result[0]))
   write_log('{} has {} records'.format(MAP_INSERTS_AST, INSERTS_result[0]), logfile)
except:
    print ("\n Unable to Append PPARCEL_INSERT_View to Inserts - AUTOWORKSPACE")
    write_log("Unable to PARCEL_INSERT_View to Inserts - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on Append PARCEL_INSERT_View to Inserts - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" & PARCEL_INSERT_View for next process
    arcpy.Delete_management("in_memory")
    arcpy.Delete_management(PARCEL_INSERT_View)
except:
    print ("\n Unable to clear Inserts_Dissolve from in_memory & PARCEL_INSERT_View")
    write_log("Unable to clear Inserts_Dissolve from in_memory & PARCEL_INSERT_View", logfile)
    logging.exception('Got exception on clear Inserts_Dissolve from in_memory & PARCEL_INSERT_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Creating Map Inserts - AST from Tax_Parcel_Joined - AUTO_WORKSPACE completed")
write_log("       Creating Map Inserts - AST from Tax_Parcel_Joined - AUTO_WORKSPACE completed", logfile)

print ("\n Creating Map Sections - AST from Tax_Parcel_Joined - AUTO_WORKSPACE")
write_log("\n Creating Map Sections - AST from Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)

try:
    # delete rows Map Sections - AUTOWORKSPACE
    arcpy.DeleteRows_management(MAP_SECTIONS_AST)
except:
    print ("\n Unable to delete rows Map Sections - AUTOWORKSPACE")
    write_log("Unable to delete rows Map Sections - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on delete rows Map Inserts - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MAP IS NOT NULL) // (make temporary feature of tax parcels - which contains information to create sections in following steps)
    PARCEL_SECTION_View = arcpy.MakeFeatureLayer_management(TAXPARCEL_JOINED_AUTOWKSP, "PARCEL_SECTION_View", "SEC_MAP IS NOT NULL", "", "OBJECTID OBJECTID VISIBLE NONE;CAMA_PIN CAMA_PIN VISIBLE NONE;MAP MAP VISIBLE NONE;PARCEL PARCEL VISIBLE NONE;LOT LOT VISIBLE NONE;ID_PIN ID_PIN VISIBLE NONE;MAPTYPE MAPTYPE VISIBLE NONE;CITY CITY VISIBLE NONE;MEADVILLE MEADVILLE VISIBLE NONE;TITUSVILLE TITUSVILLE VISIBLE NONE;BLK_MAP BLK_MAP VISIBLE NONE;BLK_PARCEL BLK_PARCEL VISIBLE NONE;BLK_MAPTYPE BLK_MAPTYPE VISIBLE NONE;INS_MAP INS_MAP VISIBLE NONE;INS_DESCRIPTION INS_DESCRIPTION VISIBLE NONE;INS_SECTION_MAP INS_SECTION_MAP VISIBLE NONE;INS_SCALE INS_SCALE VISIBLE NONE;INS_ROTATION INS_ROTATION VISIBLE NONE;SEC_MAP SEC_MAP VISIBLE NONE;SEC_MUNI_NAME SEC_MUNI_NAME VISIBLE NONE;SEC_ANGLE SEC_ANGLE VISIBLE NONE;SEC_SCALE SEC_SCALE VISIBLE NONE;SEC_ROTATION SEC_ROTATION VISIBLE NONE;SEC_WARD SEC_WARD VISIBLE NONE;MDVL_BLK_MAP MDVL_BLK_MAP VISIBLE NONE;MDVL_BLK_PARCEL MDVL_BLK_PARCEL VISIBLE NONE;MDVL_BLK_MAPTYPE MDVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_MAP TSVL_BLK_MAP VISIBLE NONE;TSVL_BLK_PARCEL TSVL_BLK_PARCEL VISIBLE NONE;TSVL_BLK_MAPTYPE TSVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_ID TSVL_BLK_ID VISIBLE NONE;PID PID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;GIS_ACRES GIS_ACRES VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print ("\n Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MAP IS NOT NULL)")
    write_log("Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MAP IS NOT NULL)", logfile)
    logging.exception('Got exception on make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MAP IS NOT NULL) logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve PARCEL_SECTION_View (dissolves like features in tax parcels, keeping only fields needed for sections)
    arcpy.Dissolve_management(PARCEL_SECTION_View, "in_memory/Sections_Dissolve", "SEC_MAP;SEC_MUNI_NAME;SEC_ANGLE;SEC_SCALE;SEC_ROTATION;SEC_WARD", "", "MULTI_PART", "DISSOLVE_LINES") 
except:
    print ("\n Unable to Dissolve PARCEL_SECTION_View")
    write_log("Unable to Dissolve PARCEL_SECTION_View", logfile)
    logging.exception('Got exception on Dissolve PARCEL_SECTION_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append PARCEL_SECTION_View to Sections - AUTOWORKSPACE (append temporary layer created from steps above into "real" feature class)
    arcpy.Append_management("in_memory/Sections_Dissolve", MAP_SECTIONS_AST, "NO_TEST", 'MAP "MAP" true true false 50 Text 0 0 ,First,#,"in_memory/Sections_Dissolve",SEC_MAP,-1,-1;MUNI_NAME "MUNI_NAME" true true false 50 Text 0 0 ,First,#,"in_memory/Sections_Dissolve",SEC_MUNI_NAME,-1,-1;ANGLE "ANGLE" true true false 50 Text 0 0 ,First,#,"in_memory/Sections_Dissolve",SEC_ANGLE,-1,-1;SCALE "SCALE" true true false 8 Double 8 38 ,First,#,"in_memory/Sections_Dissolve",SEC_SCALE,-1,-1;ROTATION "ROTATION" true true false 8 Double 8 38 ,First,#,"in_memory/Sections_Dissolve",SEC_ROTATION,-1,-1;WARD "WARD" true true false 50 Text 0 0 ,First,#,"in_memory/Sections_Dissolve",SEC_WARD,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#', "")
    SECTIONS_result = arcpy.GetCount_management(MAP_SECTIONS_AST)
    print ('{} has {} records'.format(MAP_SECTIONS_AST, SECTIONS_result[0]))
    write_log('{} has {} records'.format(MAP_SECTIONS_AST, SECTIONS_result[0]), logfile)
except:
    print ("\n Unable to Append PARCEL_SECTION_View to Sections - AUTOWORKSPACE")
    write_log("Unable to PARCEL_SECTION_View to Sections - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on Append PARCEL_SECTION_View to Sections - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for next process & PARCEL_SECTION_View
    arcpy.Delete_management("in_memory")
    arcpy.Delete_management(PARCEL_SECTION_View)
except:
    print ("\n Unable to clear Sections_Dissolve from in_memory & PARCEL_SECTION_View")
    write_log("Unable to clear Sections_Dissolve from in_memory & PARCEL_SECTION_View", logfile)
    logging.exception('Got exception on clear Sections_Dissolve from in_memory & PARCEL_SECTION_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Creating Map Sections - AST from Tax_Parcel_Joined - AUTO_WORKSPACE completed")
write_log("       Creating Map Sections - AST from Tax_Parcel_Joined - AUTO_WORKSPACE completed", logfile)

print ("\n Creating Meadville Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE")
write_log("\n Creating Meadville Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)

try:
    # delete rows Meadville Blocks - AUTOWORKSPACE
    arcpy.DeleteRows_management(MDVL_BLOCKS_AST)
except:
    print ("\n Unable to delete rows Meadville Blocks - AUTOWORKSPACE")
    write_log("Unable to delete rows Meadville Blocks - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on delete rows Meadville Blocks - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = MEADVILLE CITY) // (make temporary feature of tax parcels - which contains information to create Meadville blocks in following steps)
    MDVL_BLOCKS_View = arcpy.MakeFeatureLayer_management(TAXPARCEL_JOINED_AUTOWKSP, "MDVL_BLOCKS_View", "SEC_MUNI_NAME = 'MEADVILLE CITY'", "", "OBJECTID OBJECTID VISIBLE NONE;CAMA_PIN CAMA_PIN VISIBLE NONE;MAP MAP VISIBLE NONE;PARCEL PARCEL VISIBLE NONE;LOT LOT VISIBLE NONE;ID_PIN ID_PIN VISIBLE NONE;MAPTYPE MAPTYPE VISIBLE NONE;CITY CITY VISIBLE NONE;MEADVILLE MEADVILLE VISIBLE NONE;TITUSVILLE TITUSVILLE VISIBLE NONE;BLK_MAP BLK_MAP VISIBLE NONE;BLK_PARCEL BLK_PARCEL VISIBLE NONE;BLK_MAPTYPE BLK_MAPTYPE VISIBLE NONE;INS_MAP INS_MAP VISIBLE NONE;INS_DESCRIPTION INS_DESCRIPTION VISIBLE NONE;INS_SECTION_MAP INS_SECTION_MAP VISIBLE NONE;INS_SCALE INS_SCALE VISIBLE NONE;INS_ROTATION INS_ROTATION VISIBLE NONE;SEC_MAP SEC_MAP VISIBLE NONE;SEC_MUNI_NAME SEC_MUNI_NAME VISIBLE NONE;SEC_ANGLE SEC_ANGLE VISIBLE NONE;SEC_SCALE SEC_SCALE VISIBLE NONE;SEC_ROTATION SEC_ROTATION VISIBLE NONE;SEC_WARD SEC_WARD VISIBLE NONE;MDVL_BLK_MAP MDVL_BLK_MAP VISIBLE NONE;MDVL_BLK_PARCEL MDVL_BLK_PARCEL VISIBLE NONE;MDVL_BLK_MAPTYPE MDVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_MAP TSVL_BLK_MAP VISIBLE NONE;TSVL_BLK_PARCEL TSVL_BLK_PARCEL VISIBLE NONE;TSVL_BLK_MAPTYPE TSVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_ID TSVL_BLK_ID VISIBLE NONE;PID PID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;GIS_ACRES GIS_ACRES VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print ("\n Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = MEADVILLE CITY)")
    write_log("Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = MEADVILLE CITY)", logfile)
    logging.exception('Got exception on make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = MEADVILLE CITY) logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve MDVL_BLOCKS_View (dissolves like features in tax parcels, keeping only fields needed for Meadville blocks)
    arcpy.Dissolve_management(MDVL_BLOCKS_View, "in_memory/MDVL_Blocks_Dissolve", "SEC_MUNI_NAME;MDVL_BLK_MAP;MDVL_BLK_PARCEL;MDVL_BLK_MAPTYPE", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to Dissolve MDVL_BLOCKS_View")
    write_log("Unable to Dissolve MDVL_BLOCKS_View", logfile)
    logging.exception('Got exception on Dissolve MDVL_BLOCKS_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append MDVL_BLOCKS_View to Sections - AUTOWORKSPACE (append temporary layer created from steps above into "real" feature class)
    arcpy.Append_management("in_memory/MDVL_Blocks_Dissolve", MDVL_BLOCKS_AST, "NO_TEST", 'MAP "MAP" true true false 50 Text 0 0 ,First,#,"in_memory/MDVL_Blocks_Dissolve",MDVL_BLK_MAP,-1,-1;MUNI_NAME "MUNI_NAME" true true false 50 Text 0 0 ,First,#,"in_memory/MDVL_Blocks_Dissolve",SEC_MUNI_NAME,-1,-1;PARCEL "PARCEL" true true false 50 Text 0 0 ,First,#,"in_memory/MDVL_Blocks_Dissolve",MDVL_BLK_PARCEL,-1,-1;MAPTYPE "MAPTYPE" true true false 50 Text 0 0 ,First,#,"in_memory/MDVL_Blocks_Dissolve",MDVL_BLK_MAPTYPE,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#', "")
    MDVL_BLOCKS_result = arcpy.GetCount_management(MDVL_BLOCKS_AST)
    print ('{} has {} records'.format(MDVL_BLOCKS_AST, MDVL_BLOCKS_result[0]))
    write_log('{} has {} records'.format(MDVL_BLOCKS_AST, MDVL_BLOCKS_result[0]), logfile)
except:
    print ("\n Unable to Append MDVL_BLOCKS_View to Sections - AUTOWORKSPACE")
    write_log("Unable to MDVL_BLOCKS_View to Sections - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on Append MDVL_BLOCKS_View to Sections - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for next process & MDVL_BLOCKS_View
    arcpy.Delete_management("in_memory")
    arcpy.Delete_management(MDVL_BLOCKS_View)
except:
    print ("\n Unable to clear MDVL_Blocks_Dissolve from in_memory & MDVL_BLOCKS_View")
    write_log("Unable to clear MDVL_Blocks_Dissolve from in_memory & MDVL_BLOCKS_View", logfile)
    logging.exception('Got exception on clear MDVL_Blocks_Dissolve from in_memory & MDVL_BLOCKS_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Creating Meadville Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE completed")
write_log("       Creating Meadville Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE completed", logfile)

print ("\n Creating Titusville Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE")
write_log("\n Creating Titusville Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE", logfile)

try:
    # delete rows Titusville Blocks - AUTOWORKSPACE
    arcpy.DeleteRows_management(TSVL_BLOCKS_AST)
except:
    print ("\n Unable to delete rows Titusville Blocks - AUTOWORKSPACE")
    write_log("Unable to delete rows Titusville Blocks - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on delete rows Titusville Blocks - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = TITUSVILLE CITY) // (make temporary feature of tax parcels - which contains information to create Titusville blocks in following steps)
    TSVL_BLOCKS_View = arcpy.MakeFeatureLayer_management(TAXPARCEL_JOINED_AUTOWKSP, "TSVL_BLOCKS_View", "SEC_MUNI_NAME = 'TITUSVILLE CITY'", "", "OBJECTID OBJECTID VISIBLE NONE;CAMA_PIN CAMA_PIN VISIBLE NONE;MAP MAP VISIBLE NONE;PARCEL PARCEL VISIBLE NONE;LOT LOT VISIBLE NONE;ID_PIN ID_PIN VISIBLE NONE;MAPTYPE MAPTYPE VISIBLE NONE;CITY CITY VISIBLE NONE;MEADVILLE MEADVILLE VISIBLE NONE;TITUSVILLE TITUSVILLE VISIBLE NONE;BLK_MAP BLK_MAP VISIBLE NONE;BLK_PARCEL BLK_PARCEL VISIBLE NONE;BLK_MAPTYPE BLK_MAPTYPE VISIBLE NONE;INS_MAP INS_MAP VISIBLE NONE;INS_DESCRIPTION INS_DESCRIPTION VISIBLE NONE;INS_SECTION_MAP INS_SECTION_MAP VISIBLE NONE;INS_SCALE INS_SCALE VISIBLE NONE;INS_ROTATION INS_ROTATION VISIBLE NONE;SEC_MAP SEC_MAP VISIBLE NONE;SEC_MUNI_NAME SEC_MUNI_NAME VISIBLE NONE;SEC_ANGLE SEC_ANGLE VISIBLE NONE;SEC_SCALE SEC_SCALE VISIBLE NONE;SEC_ROTATION SEC_ROTATION VISIBLE NONE;SEC_WARD SEC_WARD VISIBLE NONE;MDVL_BLK_MAP MDVL_BLK_MAP VISIBLE NONE;MDVL_BLK_PARCEL MDVL_BLK_PARCEL VISIBLE NONE;MDVL_BLK_MAPTYPE MDVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_MAP TSVL_BLK_MAP VISIBLE NONE;TSVL_BLK_PARCEL TSVL_BLK_PARCEL VISIBLE NONE;TSVL_BLK_MAPTYPE TSVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_ID TSVL_BLK_ID VISIBLE NONE;PID PID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;GIS_ACRES GIS_ACRES VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print ("\n Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = TITUSVILLE CITY)")
    write_log("Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = TITUSVILLE CITY)", logfile)
    logging.exception('Got exception on make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = TITUSVILLE CITY) logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve TSVL_BLOCKS_View (dissolves like features in tax parcels, keeping only fields needed for Titusville blocks)
    arcpy.Dissolve_management(TSVL_BLOCKS_View,"in_memory/TSVL_Blocks_Dissolve", "SEC_MUNI_NAME;TSVL_BLK_MAP;TSVL_BLK_PARCEL;TSVL_BLK_MAPTYPE;TSVL_BLK_ID", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to Dissolve TSVL_BLOCKS_View")
    write_log("Unable to Dissolve TSVL_BLOCKS_View", logfile)
    logging.exception('Got exception on Dissolve TSVL_BLOCKS_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append TSVL_BLOCKS_View to Sections - AUTOWORKSPACE (append temporary layer created from steps above into "real" feature class)
    arcpy.Append_management("in_memory/TSVL_Blocks_Dissolve", TSVL_BLOCKS_AST, "NO_TEST", 'OBJECTID "OBJECTID" true true false 4 Long 0 10 ,First,#;MAP "MAP" true true false 50 Text 0 0 ,First,#,"in_memory/TSVL_Blocks_Dissolve",TSVL_BLK_MAP,-1,-1;MUNI_NAME "MUNI_NAME" true true false 50 Text 0 0 ,First,#,"in_memory/TSVL_Blocks_Dissolve",SEC_MUNI_NAME,-1,-1;PARCEL "PARCEL" true true false 50 Text 0 0 ,First,#,"in_memory/TSVL_Blocks_Dissolve",TSVL_BLK_PARCEL,-1,-1;MAPTYPE "MAPTYPE" true true false 50 Text 0 0 ,First,#,"in_memory/TSVL_Blocks_Dissolve",TSVL_BLK_MAPTYPE,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#', "")
    TSVL_BLOCKS_result = arcpy.GetCount_management(TSVL_BLOCKS_AST)
    print ('{} has {} records'.format(TSVL_BLOCKS_AST, TSVL_BLOCKS_result[0]))
    write_log('{} has {} records'.format(TSVL_BLOCKS_AST, TSVL_BLOCKS_result[0]), logfile)
except:
    print ("\n Unable to Append TSVL_BLOCKS_View to Sections - AUTOWORKSPACE")
    write_log("Unable to TSVL_BLOCKS_View to Sections - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on Append TSVL_BLOCKS_View to Sections - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for next process & TSVL_BLOCKS_View
    arcpy.Delete_management("in_memory")
    arcpy.Delete_management(TSVL_BLOCKS_View)
except:
    print ("\n Unable to clear TSVL_Blocks_Dissolve from in_memory & TSVL_BLOCKS_View")
    write_log("Unable to clear TSVL_Blocks_Dissolve from in_memory & TSVL_BLOCKS_View", logfile)
    logging.exception('Got exception on clear TSVL_Blocks_Dissolve from in_memory & TSVL_BLOCKS_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Creating Titusville Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE completed")
write_log("       Creating Titusville Blocks - AST from Tax_Parcel_Joined - AUTO_WORKSPACE completed", logfile)
    
end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL ASSESSMENT DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL ASSESSMENT DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
