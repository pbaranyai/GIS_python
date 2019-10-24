# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Parcel_Builder.py
# Created on: 2019-05-09 
# Updated on 2019-07-10
#
# Author: Phil Baranyai/GIS Manager
#
#
# Description: 
#  Build feature classes from AST workspace -> AUTO_WORKSPACE, and join in VISION tables:
#
# Building Permits  
# Building/Trailer Only
# Pictometry 2014 Flags
# Tax Parcels
# Blocks
# Inserts
# Sections
# Meadville Blocks
# Titusville Blocks
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import collections
import datetime
import os
import traceback
import logging
import __builtin__
from arcpy import env

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

try:
    # Set the necessary product code
    import arcinfo
except:
    print ("No ArcInfo (ArcAdvanced) license available")
    write_log("!!No ArcInfo (ArcAdvanced) license available!!", logfile)
    logging.exception('Got exception on importing ArcInfo (ArcAdvanced) license logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()

#Database variables:
AST = "Database Connections\\AST@ccsde.sde"
AUTOWORKSPACE = "Database Connections\\auto_workspace@ccsde.sde"
AUTOWORKSPACE_AST = "Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment"
VISION_VIEW = "Database Connections\\Vision_Database.sde"
##TEST_FGDB = "C:\\Users\\pbaranyai\\Desktop\\AssessmentTest.gdb"

# Local variables:
BLDG_PRMT_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.BLDG_PRMT"
BLDGPERM_TBL_VISION = VISION_VIEW + "\\VISION.REAL_PROP.BLDGPERM"
BLDGPERM_TBL_AUTOWKSP = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.BLDGPERM_TBL"
BUILDING_PERMIT_JOINED_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Building_Permit_Joined"
BUILDING_PERMIT_TEMP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP"
BLOCKS_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Blocks"
BLOCKS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Blocks"
BUILDING_ONLY = AST + "\\AST.Crawford_Parcels\\AST.Building_Only"
BUILDING_ONLY_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Building_Only_Joined"
HARDLINES_AST = AST + "\\AST.Crawford_Parcels\\AST.Hardlines"
LAND_VISION = VISION_VIEW + "\\VISION.REAL_PROP.LAND"
MAILADDRESS_VISION = VISION_VIEW + "\\VISION.COMMON.MAILADDRESS"
MAP_INSERTS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Map_Inserts"
MAP_INSERTS_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Map_Inserts"
MAP_SECTIONS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Map_Sections"
MAP_SECTIONS_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Map_Sections"
MDVL_BLOCKS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Meadville_Blocks"
MDVL_BLOCKS_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Meadville_Blocks"
OWNER_VISION = VISION_VIEW + "\\VISION.COMMON.OWNER"
PARCEL_VISION = VISION_VIEW + "\\VISION.REAL_PROP.PARCEL"
PICTOMETRY_2014_FLAGS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Pictometry2014_flags"
PICTOMETRY_2014_FLAGS_JOINED_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_Joined"
PIN_AST = AST + "\\AST.Crawford_Parcels\\AST.PIN"
REALOWNERSHIP_VISION = VISION_VIEW + "\\VISION.REAL_PROP.REAL_OWNERSHIP"
REALMAST_VISION = VISION_VIEW + "\\VISION.REAL_PROP.REALMAST"
SALESHISTORY_VISION = VISION_VIEW + "\\VISION.REAL_PROP.SALEHIST"
TAXPARCEL_JOINED_OLD_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Tax_Parcels_Joined_Old"
TAXPARCEL_JOINED_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Tax_Parcels_Joined"
TSVL_BLOCKS_AST = AST + "\\CCSDE.AST.Crawford_Parcels\\CCSDE.AST.Titusville_Blocks"
TSVL_BLOCKS_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Titusville_Blocks"
VISITHISTORY_VISON = VISION_VIEW + "\\VISION.REAL_PROP.VISITHST"

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
print ("\nBuilding Permits Feature Class")
print ("Building/Trailer Only Feature Class") 
print ("Pictometry_2014 Flags Feature Class")
print ("Tax Parcels Feature Class")
print ("Blocks Feature Class")
print ("Inserts Feature Class")
print ("Sections Feature Class")
print ("Meadville Blocks Feature Class")
print ("Titusville Blocks Feature Class")
print ("============================================================================")
write_log("============================================================================", logfile)
write_log("Updating Assessment Datasets: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nBuilding Permits Feature Class", logfile)
write_log("Building/Trailer Only Feature Class", logfile)
write_log("Pictometry_2014 Flags Feature Class", logfile)
write_log("Tax Parcels Feature Class", logfile)
write_log("Blocks Feature Class", logfile)  
write_log("Inserts Feature Class", logfile) 
write_log("Sections Feature Class", logfile) 
write_log("Meadville Blocks Feature Class", logfile)
write_log("Titusville Blocks Feature Class", logfile) 
write_log("============================================================================", logfile)

print ("\n Updating ESRI/Vision temp tables from VISION")
write_log("\n Updating ESRI/Vision temp tables from VISION: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete tables that are re-built further down in program
    if arcpy.Exists(VISION_OWNER_TBL_SDE):
        arcpy.Delete_management(VISION_OWNER_TBL_SDE, "Table")
        print (VISION_OWNER_TBL_SDE + " found - table deleted")
        write_log(VISION_OWNER_TBL_SDE + " found - table deleted", logfile)
    if arcpy.Exists(VISION_OTHER_TBL_SDE):
        arcpy.Delete_management(VISION_OTHER_TBL_SDE, "Table")
        print (VISION_OTHER_TBL_SDE + " found - table deleted")
        write_log(VISION_OTHER_TBL_SDE + " found - table deleted", logfile)
    if arcpy.Exists(VISION_OWNER_TBL_WEBTemp):
        arcpy.Delete_management(VISION_OWNER_TBL_WEBTemp, "Table")
        print (VISION_OWNER_TBL_WEBTemp + " found - table deleted")
        write_log(VISION_OWNER_TBL_WEBTemp + " found - table deleted", logfile)
    if arcpy.Exists(VISIDATA_TEMP):
        arcpy.Delete_management(VISIDATA_TEMP, "Table")
        print (VISIDATA_TEMP + " found - table deleted")
        write_log(VISIDATA_TEMP + " found - table deleted", logfile)
    if arcpy.Exists(BUILDING_PERMIT_TEMP):
        arcpy.Delete_management(BUILDING_PERMIT_TEMP, "Table")
        print (BUILDING_PERMIT_TEMP + " found - table deleted")
        write_log(BUILDING_PERMIT_TEMP + " found - table deleted", logfile)        
except:
    print ("\n Unable to delete VISION_OWNER_TBL_WEBTemp, VISION_OWNER_TBL_SDE or VISION_OTHER_TBL_SDE, need to delete existing FGDB manually and/or close program locking the tables")
    write_log("\n Unable to create new VISION_OWNER_TBL_WEBTemp, VISION_OWNER_TBL_SDE or VISION_OTHER_TBL_SDE, need to delete existing FGDB manually and/or close program locking the tables", logfile)
    logging.exception('Got exception on delete VISION_OWNER_TBL_WEBTemp, VISION_OWNER_TBL_SDE or VISION_OTHER_TBL_SDE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

VISION_ESRI_TABLES = [VISION_BLDGPERM_SDE,VISION_LAND_SDE,VISION_MAILADDRESS_SDE,VISION_OWNER_SDE,VISION_PARCEL_SDE,VISION_REAL_OWNERSHIP_SDE,VISION_REALMAST_SDE,VISION_SALES_HISTORY_SDE]

try:
    # Delete rows from ESRI/Vision temp tables, program will obtain fresh data from live vision view
    print ("\n  Cleaning out VISION-ESRI tables")
    write_log("\n  Cleaning out VISION-ESRI tables", logfile)
    for Table in VISION_ESRI_TABLES:
        delete_input = Table
        arcpy.DeleteRows_management(delete_input)
    print ("   VISION-ESRI tables cleaned out...")
    write_log("   VISION-ESRI tables cleaned out...",logfile)
except:
    print ("\n Unable to delete rows from Vision ESRI tables")
    write_log("\n Unable to delete rows from Vision ESRI tables", logfile)
    logging.exception('Got exception on delete rows from Vision ESRI tables logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append data from live VISION view tables to SDE tables AUTO_WORKSPACE
    print ("\n    Appending data from VISION tables to SDE tables...")
    write_log("\n    Appending data from VISION tables to SDE tables...",logfile)
    arcpy.Append_management(BLDGPERM_TBL_VISION, VISION_BLDGPERM_SDE, "NO_TEST", 'BPE_PID "BPE_PID" true false false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_PID,-1,-1;BPE_PERMIT_ID "BPE_PERMIT_ID" true true false 20 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_PERMIT_ID,-1,-1;BPE_FISCAL_YR "BPE_FISCAL_YR" true false false 2 Short 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_FISCAL_YR,-1,-1;BPE_APP_DATE "BPE_APP_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_APP_DATE,-1,-1;BPE_ISSUE_DATE "BPE_ISSUE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_ISSUE_DATE,-1,-1;BPE_INSPECT_DATE "BPE_INSPECT_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_INSPECT_DATE,-1,-1;BPE_AMOUNT "BPE_AMOUNT" true true false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_AMOUNT,-1,-1;BPE_FEE "BPE_FEE" true true false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_FEE,-1,-1;BPE_APPLICANT "BPE_APPLICANT" true true false 50 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_APPLICANT,-1,-1;BPE_LICENCE "BPE_LICENCE" true true false 20 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_LICENCE,-1,-1;BPE_COMPANY "BPE_COMPANY" true true false 50 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_COMPANY,-1,-1;BPE_AREA "BPE_AREA" true true false 20 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_AREA,-1,-1;BPE_REF "BPE_REF" true true false 20 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_REF,-1,-1;BPE_DESC "BPE_DESC" true true false 40 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_DESC,-1,-1;BPE_PCT_COMPLETE "BPE_PCT_COMPLETE" true true false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_PCT_COMPLETE,-1,-1;BPE_DATE_COMPLETE "BPE_DATE_COMPLETE" true true false 8 Date 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_DATE_COMPLETE,-1,-1;BPE_COMMENT "BPE_COMMENT" true true false 750 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_COMMENT,-1,-1;BPE_USRFLD_01 "BPE_USRFLD_01" true true false 100 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_USRFLD_01,-1,-1;BPE_USRFLD_02 "BPE_USRFLD_02" true true false 100 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_USRFLD_02,-1,-1;BPE_USRFLD_03 "BPE_USRFLD_03" true true false 100 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_USRFLD_03,-1,-1;BPE_USRFLD_04 "BPE_USRFLD_04" true true false 100 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_USRFLD_04,-1,-1;BPE_USRFLD_05 "BPE_USRFLD_05" true true false 100 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.BLDGPERM,BPE_USRFLD_05,-1,-1;PERMIT_LINK "PERMIT_LINK" true true false 100 Text 0 0 ,First,#', "")
    print ("     BLDGPERM table appended...")
    write_log("     BLDGPERM table appended...",logfile)
    arcpy.Append_management(LAND_VISION, VISION_LAND_SDE, "NO_TEST", 'LND_PID "LND_PID" true false false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.LAND,LND_PID,-1,-1;LND_LINE_ID "LND_LINE_ID" true false false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.LAND,LND_LINE_ID,-1,-1;LND_USE_CODE "LND_USE_CODE" true true false 4 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.LAND,LND_USE_CODE,-1,-1;LND_USE_DESC "LND_USE_DESC" true true false 40 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.LAND,LND_USE_DESC,-1,-1;LND_DSTRCT "LND_DSTRCT" true true false 6 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.LAND,LND_DSTRCT,-1,-1', "")
    print ("     LAND table appended...")
    write_log("     LAND table appended...",logfile)
    arcpy.Append_management(MAILADDRESS_VISION, VISION_MAILADDRESS_SDE, "NO_TEST", 'MAD_MNC "MAD_MNC" true false false 4 Long 0 10 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.MAILADDRESS,MAD_MNC,-1,-1;MAD_MAIL_NAME1 "MAD_MAIL_NAME1" true true false 85 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.MAILADDRESS,MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "MAD_MAIL_NAME2" true true false 85 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.MAILADDRESS,MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "MAD_MAIL_ADDR1" true true false 50 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.MAILADDRESS,MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "MAD_MAIL_CITY" true true false 30 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.MAILADDRESS,MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "MAD_MAIL_STATE" true true false 20 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.MAILADDRESS,MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "MAD_MAIL_ZIP" true true false 20 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.MAILADDRESS,MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "MAD_MAIL_ADDR2" true true false 50 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.MAILADDRESS,MAD_MAIL_ADDR2,-1,-1;MAD_ID "MAD_ID" true false false 4 Long 0 10 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.MAILADDRESS,MAD_ID,-1,-1', "")
    print ("     MAILADDRESS table appended...")
    write_log("     MAILADDRESS table appended...",logfile)
    arcpy.Append_management(OWNER_VISION, VISION_OWNER_SDE, "NO_TEST", 'OWN_ID "OWN_ID" true false false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.OWNER,OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.OWNER,OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.COMMON.OWNER,OWN_NAME2,-1,-1', "")
    print ("     OWNER table appended...")
    write_log("     OWNER table appended...",logfile)
    arcpy.Append_management(PARCEL_VISION, VISION_PARCEL_SDE, "NO_TEST", 'PRC_PID "PRC_PID" true false false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_PID,-1,-1;PRC_PF_LOCN "PRC_PF_LOCN" true true false 15 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_PF_LOCN,-1,-1;PRC_PF_LOCN_DESC "PRC_PF_LOCN_DESC" true true false 50 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_PF_LOCN_DESC,-1,-1;PRC_USRFLD_09 "PRC_USRFLD_09" true true false 30 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "PRC_USRFLD_10" true true false 30 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "PRC_TTL_ASSESS_BLDG" true true false 8 Double 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "PRC_TTL_ASSESS_IMPROVEMENTS" true true false 8 Double 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "PRC_TTL_ASSESS_LND" true true false 8 Double 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "PRC_TTL_ASSESS_OB" true true false 8 Double 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "PRC_VALUE" true true false 8 Double 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_VALUE,-1,-1;PRC_CMPLX_PID "PRC_CMPLX_PID" true true false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "PRC_CMPLX_DESC" true true false 30 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "PRC_CENSUS" true true false 20 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "PRC_TTL_MRKT_ASSESS" true true false 8 Double 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "PRC_TTL_ASSESS" true true false 8 Double 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.PARCEL,PRC_TTL_ASSESS,-1,-1', "")
    print ("     PARCEL table appended...")
    write_log("     PARCEL table appended...",logfile)
    arcpy.Append_management(REALOWNERSHIP_VISION, VISION_REAL_OWNERSHIP_SDE, "NO_TEST", 'ROW_PID "ROW_PID" true false false 4 Long 0 10 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REAL_OWNERSHIP,ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true false false 4 Long 0 10 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REAL_OWNERSHIP,ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true false false 4 Long 0 10 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REAL_OWNERSHIP,ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REAL_OWNERSHIP,ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REAL_OWNERSHIP,ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REAL_OWNERSHIP,ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true false false 4 Long 0 10 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REAL_OWNERSHIP,ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REAL_OWNERSHIP,ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#', "")
    print ("     REALOWNERSHIP table appended...")
    write_log("     REALOWNERSHIP table appended...",logfile)
    arcpy.Append_management(REALMAST_VISION, VISION_REALMAST_SDE, "NO_TEST", 'REM_MNC "REM_MNC" true false false 4 Long 0 10 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_MNC,-1,-1;REM_PID "REM_PID" true false false 4 Long 0 10 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_PID,-1,-1;REM_PIN "REM_PIN" true true false 35 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_PIN,-1,-1;REM_OWN_NAME "REM_OWN_NAME" true true false 85 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "REM_PRCL_LOCN" true true false 50 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "REM_PRCL_LOCN_CITY" true true false 18 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "REM_PRCL_LOCN_STT" true true false 2 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "REM_PRCL_LOCN_ZIP" true true false 12 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "REM_ALT_PRCL_ID" true true false 35 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "REM_PRCL_STATUS_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "REM_MBLU_MAP" true true false 7 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "REM_MBLU_MAP_CUT" true true false 3 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "REM_MBLU_BLOCK" true true false 7 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "REM_MBLU_BLOCK_CUT" true true false 3 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "REM_MBLU_LOT" true true false 7 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "REM_MBLU_LOT_CUT" true true false 3 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "REM_MBLU_UNIT" true true false 7 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "REM_MBLU_UNIT_CUT" true true false 3 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "REM_STATUS_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "REM_INET_SUPPRESS" true true false 4 Long 0 10 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "REM_IS_CONDO_MAIN" true true false 2 Short 0 5 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "REM_CMPLX_NAME" true true false 30 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "REM_BLDG_NAME" true true false 60 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_BLDG_NAME,-1,-1;REM_USE_CODE "REM_USE_CODE" true true false 4 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_USE_CODE,-1,-1;REM_LEGAL_AREA "REM_LEGAL_AREA" true true false 8 Double 8 38 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "REM_LAST_UPDATE" true true false 8 Date 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_LAST_UPDATE,-1,-1;REM_USRFLD "REM_USRFLD" true true false 6 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_USRFLD,-1,-1;REM_USRFLD_DESC "REM_USRFLD_DESC" true true false 40 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_USRFLD_DESC,-1,-1;PID_TEXT "PID_TEXT" true true false 15 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.REALMAST,REM_PID,-1,-1', "")
    print ("     REALMAST table appended...")
    write_log("     REALMAST table appended...",logfile)
    arcpy.Append_management(SALESHISTORY_VISION, VISION_SALES_HISTORY_SDE, "NO_TEST", 'SLH_PID "SLH_PID" true false false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.SALEHIST,SLH_PID,-1,-1;SLH_LINE_NUM "SLH_LINE_NUM" true false false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.SALEHIST,SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "SLH_SALE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.SALEHIST,SLH_SALE_DATE,-1,-1;SLH_BOOK "SLH_BOOK" true true false 15 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.SALEHIST,SLH_BOOK,-1,-1;SLH_PAGE "SLH_PAGE" true true false 15 Text 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.SALEHIST,SLH_PAGE,-1,-1;SLH_PRICE "SLH_PRICE" true true false 8 Double 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.SALEHIST,SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "SLH_CURRENT_OWNER" true true false 2 Short 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.SALEHIST,SLH_CURRENT_OWNER,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#;SLH_PID_JOIN "SLH_PID_JOIN" true true false 4 Long 0 0 ,First,#,Database Connections\\Vision_Database.sde\\VISION.REAL_PROP.SALEHIST,SLH_PID,-1,-1', "")
    print ("     SALESHISTORY table appended...")
    write_log("     SALESHISTORY table appended...",logfile)
except:
    print ("\n Unable to append data from VISION tables to SDE tables")
    write_log("\n Unable to append data from VISION tables to SDE tables", logfile)
    logging.exception('Got exception on append data from VISION tables to SDE tables logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    print ("\n      Calculating PERMIT_LINK field in BLDGPERM_TBL_VISION...")
    write_log("\n      Calculating PERMIT_LINK field in BLDGPERM_TBL_VISION...",logfile)
    # Calculate PERMIT_LINK field in BLDGPERM_TBL_VISION, used to join to building permit feature class later in program.
    arcpy.CalculateField_management(VISION_BLDGPERM_SDE, "PERMIT_LINK", '"{}-{}".format(!BPE_PID! , !BPE_PERMIT_ID!)', "PYTHON_9.3", "")
except:
    print ("\n Unable to Calculate PERMIT_LINK field in BLDGPERM_TBL_VISION")
    write_log("\n Unable to Calculate PERMIT_LINK field in BLDGPERM_TBL_VISION", logfile)
    logging.exception('Got exception on Calculate PERMIT_LINK field in BLDGPERM_TBL_VISION logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Remove spaces (before and after values) in all fields of REALMAST table (as they cause errors in processing)
    print ("       Removing spaces from fields in REALMAST Table...")
    write_log("       Removing spaces from fields in REALMAST Table...",logfile)
    AllFields = [i.name for i in arcpy.ListFields(VISION_REALMAST_SDE) if i.type=='String']
    with arcpy.da.UpdateCursor(VISION_REALMAST_SDE,AllFields) as cursor:
        for row in cursor:
            row=[i.strip() if i is not None else None for i in row]
            cursor.updateRow(row)
        del row 
        del cursor
except:
    print ("\n Unable to remove spaces from fields in REALMAST Table")
    write_log("\n Unable to remove spaces from fields in REALMAST Table", logfile)
    logging.exception('Got exception on remove spaces from fields in REALMAST Table logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()     

try:
    # Remove leading zeros from sales history book and page fields (as they will cause the URL fields to fail)
    print ("        Removing leading zeros from fields in SALES_HISTORY Table Book and Page fields...")
    write_log("        Removing leading zeros from fields in SALES_HISTORY Table Book and Page fields...",logfile)
    BKPG = ['SLH_BOOK', 'SLH_PAGE']
    with arcpy.da.UpdateCursor(VISION_SALES_HISTORY_SDE,BKPG) as cursor:
        for row in cursor:
            row=[BKPG.lstrip("0") if BKPG is not None else None for BKPG in row]
            cursor.updateRow(row)
        del row 
        del cursor
except:
    print ("\n Unable to remove leading zeros from fields in SALES_HISTORY Table Book and Page fields")
    write_log("\n Unable to remove leading zeros from fields in SALES_HISTORY Table Book and Page fields", logfile)
    logging.exception('Got exception on remove leading zeros from fields in SALES_HISTORY Table Book and Page fields logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()  

print ("         Updating ESRI/Vision temp tables from VISION completed")
write_log("         Updating ESRI/Vision temp tables from VISION completed", logfile)

print ("\n Calculating OWN_LINE fields in VISION_REAL_OWNERSHIP_SDE and VISION_SALES_HISTORY_SDE tables")
write_log("\n Calculating OWN_LINE fields in VISION_REAL_OWNERSHIP_SDE and VISION_SALES_HISTORY_SDE tables", logfile)

try:
    # Calculate OWN_LINE fields in VISION_REAL_OWNERSHIP_SDE and VISION_SALES_HISTORY_SDE tables, used to link tables together in OWNER table later in program.
    arcpy.CalculateField_management(VISION_REAL_OWNERSHIP_SDE, "OWN_LINE", '"{}-{}".format( !ROW_PID! ,!ROW_LINE_NUM!)', "PYTHON_9.3", "")
    arcpy.CalculateField_management(VISION_SALES_HISTORY_SDE, "OWN_LINE", '"{}-{}".format( !SLH_PID! , !SLH_LINE_NUM!)', "PYTHON_9.3", "")
except:
    print ("\n Unable to append data from VISION tables to SDE tables")
    write_log("\n Unable to append data from VISION tables to SDE tables", logfile)
    logging.exception('Got exception on append data from VISION tables to SDE tables logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()    

print ("       Calculating OWN_LINE fields in VISION_REAL_OWNERSHIP_SDE and VISION_SALES_HISTORY_SDE tables completed")
write_log("       Calculating OWN_LINE fields in VISION_REAL_OWNERSHIP_SDE and VISION_SALES_HISTORY_SDE tables completed", logfile)

print ("\n Create VISION_OWNER_TBL from VIS_OWNER_TBL and join VIS_MAILADDRESS, VIS_REAL_OWNERSHIP, and VIS_SALES_HISTORY tables")
write_log("\n Create VISION_OWNER_TBL from VIS_OWNER_TBL and join VIS_MAILADDRESS, VIS_REAL_OWNERSHIP, and VIS_SALES_HISTORY tables", logfile)

try:
    # Create VISION_OWNER_TBL_SDE from VIS_OWNER_TBL (creates owner table, so that additional vision tables can be joined to it)
    arcpy.TableToTable_conversion(VISION_OWNER_SDE, AUTOWORKSPACE, "VISION_OWNER_TBL", "", 'OWN_ID "OWN_ID" true false false 4 Long 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\VIS_OWNER_TBL,OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\VIS_OWNER_TBL,OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\VIS_OWNER_TBL,OWN_NAME2,-1,-1', "")
    print ("  VISION_OWNER_TBL created...")
    write_log("  VISION_OWNER_TBL created",logfile)
except:
    print ("\n Unable to Create VISION_OWNER_TBL from VIS_OWNER_TBL")
    write_log("\n Unable to Create VISION_OWNER_TBL from VIS_OWNER_TBL", logfile)
    logging.exception('Got exception on Create VISION_OWNER_TBL from VIS_OWNER_TBL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Join OWNER table view to MAILADDRESS, REALOWNERSHIP, and SALES_HISTORY tables
    arcpy.JoinField_management(VISION_OWNER_TBL_SDE, "OWN_ID", VISION_REAL_OWNERSHIP_SDE, "ROW_OWN_ID", "ROW_PID;ROW_OWN_ID;ROW_LINE_NUM;ROW_OWN_PCT;ROW_PRIMARY;ROW_CREATE_DATE;ROW_MAD_ID;ROW_MAD_ISPRIMARY;OWN_LINE")
    print ("   VIS_OWNER_TBL joined to VIS_REAL_OWNERSHIP_TBL...")
    write_log("   VIS_OWNER_TBL joined to VIS_REAL_OWNERSHIP_TBL...",logfile)
    arcpy.JoinField_management(VISION_OWNER_TBL_SDE, "ROW_MAD_ID", VISION_MAILADDRESS_SDE, "MAD_ID", "MAD_MAIL_NAME1;MAD_MAIL_NAME2;MAD_MAIL_ADDR1;MAD_MAIL_CITY;MAD_MAIL_STATE;MAD_MAIL_ZIP;MAD_MAIL_ADDR2;MAD_ID")
    print ("    VIS_OWNER_TBL joined to VIS_MAILADDRESS_TBL...")
    write_log("    VIS_OWNER_TBL joined to VIS_MAILADDRESS_TBL...",logfile)
    arcpy.JoinField_management(VISION_OWNER_TBL_SDE, "OWN_LINE", VISION_SALES_HISTORY_SDE, "OWN_LINE", "SLH_PID;SLH_LINE_NUM;SLH_SALE_DATE;SLH_BOOK;SLH_PAGE;SLH_PRICE;SLH_CURRENT_OWNER")
    print ("     VIS_OWNER_TBL joined to VIS_SALES_HISTORY_TBL...")
    write_log("     VIS_OWNER_TBL joined to VIS_SALES_HISTORY_TBL...",logfile)
except:
    print ("\n Unable to join VIS_OWNER_TBL view to MAILADDRESS, REALOWNERSHIP, and SALES_HISTORY tables views")
    write_log("\n Unable to join VIS_OWNER_TBL view to MAILADDRESS, REALOWNERSHIP, and SALES_HISTORY tables views", logfile)
    logging.exception('Got exception on join VIS_OWNER_TBL view to MAILADDRESS, REALOWNERSHIP, and SALES_HISTORY tables views logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calculate SLH_PID field from ROW_PID field
    arcpy.CalculateField_management(VISION_OWNER_TBL_SDE, "SLH_PID", "!ROW_PID!", "PYTHON", "")
    print ("       Calculated SLH_PID field from ROW_PID field...")
    write_log("       Calculated SLH_PID field from ROW_PID field...",logfile)
except:
    print ("\n Unable to Calculate SLH_PID field from ROW_PID field")
    write_log("\n Calculate SLH_PID field from ROW_PID field", logfile)
    logging.exception('Got exception on Calculate SLH_PID field from ROW_PID field logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Create VISION_OWNER_TBL_WEBTemp from VISION_OWNER_TBL_SDE and join in INET_SUPPRESS field from VIS_REALMAST_TBL (creates a web-friendly version of sales history based on internet supression field to filter out protected records)
    VISION_OWNER_TBL_WEBTemp = arcpy.MakeTableView_management(VISION_OWNER_TBL_SDE, "VISION_OWNER_TBL_WEBTemp", "", "", "OBJECTID OBJECTID VISIBLE NONE;OWN_ID OWN_ID VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;ROW_PID ROW_PID VISIBLE NONE;ROW_OWN_ID ROW_OWN_ID VISIBLE NONE;ROW_LINE_NUM ROW_LINE_NUM VISIBLE NONE;ROW_OWN_PCT ROW_OWN_PCT VISIBLE NONE;ROW_PRIMARY ROW_PRIMARY VISIBLE NONE;ROW_CREATE_DATE ROW_CREATE_DATE VISIBLE NONE;ROW_MAD_ID ROW_MAD_ID VISIBLE NONE;ROW_MAD_ISPRIMARY ROW_MAD_ISPRIMARY VISIBLE NONE;OWN_LINE OWN_LINE VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;MAD_MAIL_ADDR2 MAD_MAIL_ADDR2 VISIBLE NONE;MAD_ID MAD_ID VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_INET_SUPPRESS_1 REM_INET_SUPPRESS_1 VISIBLE NONE")
    arcpy.JoinField_management(VISION_OWNER_TBL_WEBTemp, "ROW_PID", VISION_REALMAST_SDE, "REM_PID", "REM_INET_SUPPRESS")
    arcpy.TableToTable_conversion(VISION_OWNER_TBL_WEBTemp, AUTOWORKSPACE, "VISION_OWNER_TBL_WEBTemp", "REM_INET_SUPPRESS IS NULL OR REM_INET_SUPPRESS = 0", 'OWN_ID "OWN_ID" true false false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,OWN_NAME2,-1,-1;ROW_PID "ROW_PID" true true false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,OWN_LINE,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,MAD_MAIL_ADDR2,-1,-1;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,SLH_BOOK,-1,-1;SLH_PAGE "Deed Page" true true false 15 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,SLH_PAGE,-1,-1;SLH_PRICE "Sale Price" true true false 8 Double 8 38 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,SLH_CURRENT_OWNER,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL,REM_INET_SUPPRESS,-1,-1',"")
    print ("      VISION_OWNER_TBL_WEBTemp created from filtered version of VISION_OWNER_TBL...")
    write_log("      VISION_OWNER_TBL_WEBTemp created from filtered version of VISION_OWNER_TBL...",logfile)
except:
    print ("\n Unable to Create VISION_OWNER_TBL_WEBTemp from VISION_OWNER_TBL_SDE and join in INET_SUPPRESS field from VIS_REALMAST_TBL (filtering out REM_INET_SUPPRESS IS NULL OR REM_INET_SUPPRESS = 0)")
    write_log("\n Unable to Create VISION_OWNER_TBL_WEBTemp from VISION_OWNER_TBL_SDE and join in INET_SUPPRESS field from VIS_REALMAST_TBL (filtering out REM_INET_SUPPRESS IS NULL OR REM_INET_SUPPRESS = 0)", logfile)
    logging.exception('Got exception on Create VISION_OWNER_TBL_WEBTemp from VISION_OWNER_TBL_SDE and join in INET_SUPPRESS field from VIS_REALMAST_TBL (filtering out REM_INET_SUPPRESS IS NULL OR REM_INET_SUPPRESS = 0) logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Create VISION_OWNER_TBL from VIS_OWNER_TBL and join VIS_MAILADDRESS, VIS_REAL_OWNERSHIP, and VIS_SALES_HISTORY tables completed")
write_log("       Create VISION_OWNER_TBL from VIS_OWNER_TBL and join VIS_MAILADDRESS, VIS_REAL_OWNERSHIP, and VIS_SALES_HISTORY tables completed", logfile)

print ("\n Create VISION_OTHER_TBL and join LAND and PARCEL tables to it")
write_log("\n Create VISION_OTHER_TBL and join LAND and PARCEL tables to it", logfile)

try:
    # Create VISION_OTHER_TBL_SDE from VISION_REALMAST_SDE (creates other table, so that additional vision tables can be joined to it)
    arcpy.TableToTable_conversion(VISION_REALMAST_SDE, AUTOWORKSPACE, "VISION_OTHER_TBL","", 'REM_MNC "REM_MNC" true false false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_MNC,-1,-1;REM_PID "REM_PID" true false false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_PID,-1,-1;REM_PIN "REM_PIN" true true false 35 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_PIN,-1,-1;REM_OWN_NAME "REM_OWN_NAME" true true false 85 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "REM_PRCL_LOCN" true true false 50 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "REM_PRCL_LOCN_CITY" true true false 18 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "REM_PRCL_LOCN_STT" true true false 2 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "REM_PRCL_LOCN_ZIP" true true false 12 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "REM_ALT_PRCL_ID" true true false 35 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "REM_PRCL_STATUS_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "REM_MBLU_MAP" true true false 7 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "REM_MBLU_MAP_CUT" true true false 3 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "REM_MBLU_BLOCK" true true false 7 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "REM_MBLU_BLOCK_CUT" true true false 3 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "REM_MBLU_LOT" true true false 7 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "REM_MBLU_LOT_CUT" true true false 3 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "REM_MBLU_UNIT" true true false 7 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "REM_MBLU_UNIT_CUT" true true false 3 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "REM_STATUS_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "REM_INET_SUPPRESS" true true false 4 Long 0 10 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "REM_IS_CONDO_MAIN" true true false 2 Short 0 5 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "REM_CMPLX_NAME" true true false 30 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "REM_BLDG_NAME" true true false 60 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_BLDG_NAME,-1,-1;REM_USE_CODE "REM_USE_CODE" true true false 4 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_USE_CODE,-1,-1;REM_LEGAL_AREA "REM_LEGAL_AREA" true true false 8 Double 8 38 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "REM_LAST_UPDATE" true true false 8 Date 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_LAST_UPDATE,-1,-1;REM_USRFLD "REM_USRFLD" true true false 6 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_USRFLD,-1,-1;REM_USRFLD_DESC "REM_USRFLD_DESC" true true false 40 Text 0 0 ,First,#,Database Connections\auto_workspace@ccsde.sde\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL,REM_USRFLD_DESC,-1,-1', "")
    print ("  VISION_OTHER_TBL created...")
    write_log("  VISION_OTHER_TBL created...",logfile)
except:
    print ("\n Unable to Create VISION_OWNER_TBL from VIS_OWNER_TBL")
    write_log("\n Unable to Create VISION_OWNER_TBL from VIS_OWNER_TBL", logfile)
    logging.exception('Got exception on Create VISION_OWNER_TBL from VIS_OWNER_TBL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make table view of VIS_LAND_TBL selecting out LND_LINE = 1 only (filters out duplicate land records keeps only current owner)
    VIS_LAND_TBL_View = arcpy.MakeTableView_management(VISION_LAND_SDE, "VIS_LAND_TBL_View", "LND_LINE_ID = 1", "", "OBJECTID OBJECTID VISIBLE NONE;LND_PID LND_PID VISIBLE NONE;LND_LINE_ID LND_LINE_ID VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE")
except:
    print ("\n Unable to Make table view of VIS_LAND_TBL selecting out LND_LINE = 1 only")
    write_log("\n Unable to Make table view of VIS_LAND_TBL selecting out LND_LINE = 1 only", logfile)
    logging.exception('Got exception on Make table view of VIS_LAND_TBL selecting out LND_LINE = 1 only logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Join OTHER table view to LAND and PARCEL tables
    arcpy.JoinField_management(VISION_OTHER_TBL_SDE, "REM_PID", VIS_LAND_TBL_View, "LND_PID", "LND_USE_CODE;LND_USE_DESC;LND_DSTRCT")
    print ("   VIS_LAND_TBL_View joined to VISION_OTHER_TBL...")
    write_log("   VIS_LAND_TBL_View joined to VISION_OTHER_TBL...", logfile)
    arcpy.JoinField_management(VISION_OTHER_TBL_SDE, "REM_PID", VISION_PARCEL_SDE, "PRC_PID", "PRC_PF_LOCN;PRC_PF_LOCN_DESC;PRC_USRFLD_09;PRC_USRFLD_10;PRC_TTL_ASSESS_BLDG;PRC_TTL_ASSESS_IMPROVEMENTS;PRC_TTL_ASSESS_LND;PRC_TTL_ASSESS_OB;PRC_VALUE;PRC_CMPLX_PID;PRC_CMPLX_DESC;PRC_CENSUS;PRC_TTL_MRKT_ASSESS;PRC_TTL_ASSESS")
    print ("    VIS_PARCEL_TBL joined to VISION_OTHER_TBL...")
    write_log("    VIS_PARCEL_TBL joined to VISION_OTHER_TBL...", logfile)
except:
    print ("\n Unable to Join VISION_OTHER_TBL to LAND table view and PARCEL table")
    write_log("\n Unable to Join VISION_OTHER_TBL to LAND table view and PARCEL table", logfile)
    logging.exception('Got exception on Join VISION_OTHER_TBL to LAND table view and PARCEL table logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # delete VIS_LAND_TBL_View to free up memory and space
    arcpy.Delete_management(VIS_LAND_TBL_View)
except:
    print ("\n Unable to delete VIS_LAND_TBL_View")
    write_log("\n Unable to delete VIS_LAND_TBL_View", logfile)
    logging.exception('Got exception on delete VIS_LAND_TBL_View logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Calculate Real Estate ID # in VISION_OTHER_TBL table
    arcpy.CalculateField_management(VISION_OTHER_TBL_SDE, "REM_USRFLD", "!REM_PID!", "PYTHON", "")
    arcpy.CalculateField_management(VISION_OTHER_TBL_SDE, "REM_USRFLD", "!REM_USRFLD!.zfill(6)", "PYTHON", "")
    arcpy.CalculateField_management(VISION_OTHER_TBL_SDE, "REM_USRFLD_DESC", '"{}-0-{}".format(!LND_DSTRCT!, !REM_USRFLD!)', "PYTHON", "")
##    CONTROL_NUM_CURSOR = arcpy.da.UpdateCursor(VISION_OTHER_TBL_SDE, ["REM_PID","REM_USRFLD", "REM_USRFLD_DESC"])
##    for row in ROW_LINE_CURSOR:
##        if row[0] = "":
##            row[1] = row[0]:
##                row[1] = CONTROL_NUM_CURSOR.CalculateField_management(row[1], "!REM_USRFLD!.zfill(6)", "PYTHON", "")
##                CONTROL_NUM_CURSOR.UpdateRow()
##            print ("PID calculated")
##        else:
##            pass
##    del row
##    del CONTROL_NUM_CURSOR
##    print (" Current owner sorted from CURRENT_OWNER_TBL_View...")

    print ("  Real Estate ID #s calculated in VISION_OTHER_TBL")
    write_log("  Real Estate ID #s calculated in VISION_OTHER_TBL",logfile)
except:
    print ("\n Unable to calculate Real Estate ID #s in VISION_OTHER_TBL")
    write_log("\n Unable to calculate Real Estate ID #s in VISION_OTHER_TBL", logfile)
    logging.exception('Got exception on calculate Real Estate ID #s in VISION_OTHER_TBL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()    
    
print "       Create VISION_OTHER_TBL and join LAND and PARCEL tables to it completed"
write_log("       Create VISION_OTHER_TBL and join LAND and PARCEL tables to it completed", logfile)

print ("\n Creating temporary table (VISIDATA_TEMP) from VISION_OTHER_TBL_SDE & VISION_OWNER_TBL_SDE tables")
write_log("\n Creating temporary table (VISIDATA_TEMP) from VISION_OTHER_TBL_SDE & VISION_OWNER_TBL_SDE tables: " + str(Day) + " " + str(Time), logfile)

try:
    # Create VISIDATA_TEMP table from VISION_OTHER_TBL (VISIDATA temp will become OTHER table and OWNER table joined, will be used for multiple join tools in program below)
    VISIDATA_TEMP = arcpy.TableToTable_conversion(VISION_OTHER_TBL_SDE, AUTOWORKSPACE, "VISIDATA_TEMP", "", 'REM_MNC "REM_MNC" true false false 4 Long 0 10 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_MNC,-1,-1;REM_PID "PID Number" true false false 4 Long 0 10 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_PID,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_PIN,-1,-1;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "Lot" true true false 7 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_BLDG_NAME,-1,-1;REM_USE_CODE "Use Code" true true false 4 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_USE_CODE,-1,-1;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_USRFLD,-1,-1;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,REM_USRFLD_DESC,-1,-1;PID_TEXT "PID Text format" true true false 15 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PID_TEXT,-1,-1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,LND_USE_CODE,-1,-1;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,LND_DSTRCT,-1,-1;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_PF_LOCN,-1,-1;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_PF_LOCN_DESC,-1,-1;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38 ,First,#,\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL,PRC_TTL_ASSESS,-1,-1', "")
except:
    print ("\n Unable to create VISIDATA_TEMP table from VISION_OTHER_TBL")
    write_log("\n Unable to create VISIDATA_TEMP table from VISION_OTHER_TBL", logfile)
    logging.exception('Got exception on create VISIDATA_TEMP table from VISION_OTHER_TBL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Create table view of VISION_OWNER_TBL_SDE - filtering out current owner records (only for use in parcels, entire table is not altered as it becomes sales history table for relationship class)
    CURRENT_OWNER_TBL_View = arcpy.MakeTableView_management(VISION_OWNER_TBL_SDE,"CURRENT_OWNER_TBL_View", "SLH_CURRENT_OWNER = 1", "", "OBJECTID OBJECTID VISIBLE NONE;OWN_ID OWN_ID VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;ROW_PID ROW_PID VISIBLE NONE;ROW_OWN_ID ROW_OWN_ID VISIBLE NONE;ROW_LINE_NUM ROW_LINE_NUM VISIBLE NONE;ROW_OWN_PCT ROW_OWN_PCT VISIBLE NONE;ROW_PRIMARY ROW_PRIMARY VISIBLE NONE;ROW_CREATE_DATE ROW_CREATE_DATE VISIBLE NONE;ROW_MAD_ID ROW_MAD_ID VISIBLE NONE;ROW_MAD_ISPRIMARY ROW_MAD_ISPRIMARY VISIBLE NONE;OWN_LINE OWN_LINE VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;MAD_MAIL_ADDR2 MAD_MAIL_ADDR2 VISIBLE NONE;MAD_ID MAD_ID VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE")
except:
    print ("\n Unable to create table view of VISION_OWNER_TBL_SDE - filtering out current records only")
    write_log("\n Unable to create table view of VISION_OWNER_TBL_SDE - filtering out current records only", logfile)
    logging.exception('Got exception on create table view of VISION_OWNER_TBL_SDE - filtering out current records only logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Join CURRENT_OWNER_TBL_View to VISIDATA_TEMP
    arcpy.JoinField_management(VISIDATA_TEMP, "REM_PID", CURRENT_OWNER_TBL_View, "ROW_PID", "OWN_ID;OWN_NAME1;OWN_NAME2;ROW_PID;ROW_OWN_ID;ROW_LINE_NUM;ROW_OWN_PCT;ROW_PRIMARY;ROW_CREATE_DATE;ROW_MAD_ID;ROW_MAD_ISPRIMARY;OWN_LINE;MAD_MAIL_NAME1;MAD_MAIL_NAME2;MAD_MAIL_ADDR1;MAD_MAIL_CITY;MAD_MAIL_STATE;MAD_MAIL_ZIP;MAD_MAIL_ADDR2;MAD_ID;SLH_PID;SLH_LINE_NUM;SLH_SALE_DATE;SLH_BOOK;SLH_PAGE;SLH_PRICE;SLH_CURRENT_OWNER")
    print ("  CURRENT_OWNER_TBL_View joined to VISIDATA_TEMP...")
    write_log("  CURRENT_OWNER_TBL_View joined to VISIDATA_TEMP...", logfile)
except:
    print ("\n Unable to join CURRENT_OWNER_TBL_View to VISIDATA_TEMP")
    write_log("\n Unable to join CURRENT_OWNER_TBL_View to VISIDATA_TEMP", logfile)
    logging.exception('Got exception on join CURRENT_OWNER_TBL_View to VISIDATA_TEMP logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Creating temporary table (VISIDATA_TEMP) from VISION_OTHER_TBL_SDE & VISION_OWNER_TBL_SDE tables completed")
write_log("       Creating temporary table (VISIDATA_TEMP) from VISION_OTHER_TBL_SDE & VISION_OWNER_TBL_SDE tables completed", logfile)

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
    arcpy.JoinField_management(TAXPARCEL_JOINED_AUTOWKSP, "PID", VISIDATA_TEMP, "REM_PID", "")
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
        if (row[7] == 'Book_Page' and row[6] > 0):
            row[0] = "http://172.16.154.36/SearchResultsList.asp?bookNumber={}&pageNumber={}&submit=SEARCH&forwardRequest=SearchResultsList.asp&displayPage=1&displayItemsPerPage=50&maximumMatches=1000&getCustomerData=TRUE".format(row[1],row[2])
            cursor.updateRow(row)
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
    print "      Landex URL field calculated"
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
    arcpy.JoinField_management(Building_Only_Temp, "REM_PID", VISIDATA_TEMP, "REM_PID", "REM_PIN;REM_OWN_NAME;REM_PRCL_LOCN;REM_PRCL_LOCN_CITY;REM_PRCL_LOCN_STT;REM_PRCL_LOCN_ZIP;REM_ALT_PRCL_ID;REM_PRCL_STATUS_DATE;REM_MBLU_MAP;REM_MBLU_MAP_CUT;REM_MBLU_BLOCK;REM_MBLU_BLOCK_CUT;REM_MBLU_LOT;REM_MBLU_LOT_CUT;REM_MBLU_UNIT;REM_MBLU_UNIT_CUT;REM_STATUS_DATE;REM_INET_SUPPRESS;REM_IS_CONDO_MAIN;REM_CMPLX_NAME;REM_BLDG_NAME;REM_USE_CODE;REM_LEGAL_AREA;REM_LAST_UPDATE;REM_USRFLD;REM_USRFLD_DESC;PID_TEXT;LND_USE_CODE;LND_USE_DESC;LND_DSTRCT;PRC_PF_LOCN;PRC_PF_LOCN_DESC;PRC_USRFLD_09;PRC_USRFLD_10;PRC_TTL_ASSESS_BLDG;PRC_TTL_ASSESS_IMPROVEMENTS;PRC_TTL_ASSESS_LND;PRC_TTL_ASSESS_OB;PRC_VALUE;PRC_CMPLX_PID;PRC_CMPLX_DESC;PRC_CENSUS;PRC_TTL_MRKT_ASSESS;PRC_TTL_ASSESS;OWN_ID;OWN_NAME1;OWN_NAME2;ROW_PID;ROW_OWN_ID;ROW_LINE_NUM;ROW_OWN_PCT;ROW_PRIMARY;ROW_CREATE_DATE;ROW_MAD_ID;ROW_MAD_ISPRIMARY;OWN_LINE;MAD_MAIL_NAME1;MAD_MAIL_NAME2;MAD_MAIL_ADDR1;MAD_MAIL_CITY;MAD_MAIL_STATE;MAD_MAIL_ZIP;MAD_MAIL_ADDR2;MAD_ID;SLH_PID;SLH_LINE_NUM;SLH_SALE_DATE;SLH_BOOK;SLH_PAGE;SLH_PRICE;SLH_CURRENT_OWNER")
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
    arcpy.Append_management(Building_Only_Temp, BUILDING_ONLY_AUTOWKSP, "NO_TEST", 'REM_PID "REM_PID" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PID,-1,-1;EDITOR "EDITOR" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,EDITOR,-1,-1;DATEMODIFY "DATEMODIFY" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,DATEMODIFY,-1,-1;CAMA_PIN "CAMA_PIN" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,CAMA_PIN,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PIN,-1,-1;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "Lot" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_BLDG_NAME,-1,-1;REM_USE_CODE "Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_USE_CODE,-1,-1;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_USRFLD,-1,-1;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,REM_USRFLD_DESC,-1,-1;PID_TEXT "PID Text format" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PID_TEXT,-1,-1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,LND_USE_CODE,-1,-1;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,LND_DSTRCT,-1,-1;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_PF_LOCN,-1,-1;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_PF_LOCN_DESC,-1,-1;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,PRC_TTL_ASSESS,-1,-1;OWN_ID "OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,OWN_NAME2,-1,-1;ROW_PID "ROW_PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,OWN_LINE,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_MAIL_ADDR2,-1,-1;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_BOOK,-1,-1;SLH_PAGE "Deed Page" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_PAGE,-1,-1;SLH_PRICE "Sale Price" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,SLH_CURRENT_OWNER,-1,-1;LONGITUDE_X "Longitude_X" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,LONGITUDE_X,-1,-1;LATITUDE_Y "Latitude_Y" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Building_Only_Temp,LATITUDE_Y,-1,-1', "")
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

print ("\n Creating Building Permits Joined from BLDG_PRMT - AST & VISION tables")
write_log("\n Creating Building Permits Joined from BLDG_PRMT - AST & VISION tables", logfile)


print (" Joining BLDGPERM_VISION_VIEW with VISION_OTHER_TBL and VISION_OWNER_TBL...")
write_log(" Joining BLDGPERM_VISION_VIEW with VISION_OTHER_TBL and VISION_OWNER_TBL...", logfile)

try:
    # Make temporary feature (BUILDING_PERMIT_TEMP) from BLDG_PRMT_AST (creates temporary file of building permit points from assessment workspace)
    BUILDING_PERMIT_TEMP = arcpy.FeatureClassToFeatureClass_conversion(BLDG_PRMT_AST, AUTOWORKSPACE_AST, "BUILDING_PERMIT_TEMP", "", 'REM_PID "PID" true true false 4 Long 0 10 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.BLDG_PRMT,REM_PID,-1,-1;PERMIT_LINK "PID-PERMIT #" true true false 100 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.BLDG_PRMT,PERMIT_LINK,-1,-1;EDITOR "EDITOR" false true false 255 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.BLDG_PRMT,EDITOR,-1,-1;DATE_EDIT "DATE_EDIT" false true false 8 Date 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.BLDG_PRMT,DATE_EDIT,-1,-1', "")

except:
    print ("\n Unable to make temporary feature (BUILDING_PERMIT_TEMP) from BLDG_PRMT_AST")
    write_log("\n Unable to make temporary feature (BUILDING_PERMIT_TEMP) from BLDG_PRMT_AST", logfile)
    logging.exception('Got exception on make temporary feature (BUILDING_PERMIT_TEMP) from BLDG_PRMT_AST logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Join BUILDING_PERMIT_TEMP & VISIDATA_TEMP (joins building permit points from assessment workspace to vision data {other and owner tables})
    arcpy.JoinField_management(BUILDING_PERMIT_TEMP, "REM_PID", VISIDATA_TEMP, "REM_PID", "REM_MNC;REM_PID;REM_PIN;REM_OWN_NAME;REM_PRCL_LOCN;REM_PRCL_LOCN_CITY;REM_PRCL_LOCN_STT;REM_PRCL_LOCN_ZIP;REM_ALT_PRCL_ID;REM_PRCL_STATUS_DATE;REM_MBLU_MAP;REM_MBLU_MAP_CUT;REM_MBLU_BLOCK;REM_MBLU_BLOCK_CUT;REM_MBLU_LOT;REM_MBLU_LOT_CUT;REM_MBLU_UNIT;REM_MBLU_UNIT_CUT;REM_STATUS_DATE;REM_INET_SUPPRESS;REM_IS_CONDO_MAIN;REM_CMPLX_NAME;REM_BLDG_NAME;REM_USE_CODE;REM_LEGAL_AREA;REM_LAST_UPDATE;REM_USRFLD;REM_USRFLD_DESC;PID_TEXT;LND_USE_CODE;LND_USE_DESC;LND_DSTRCT;PRC_PF_LOCN;PRC_PF_LOCN_DESC;PRC_USRFLD_09;PRC_USRFLD_10;PRC_TTL_ASSESS_BLDG;PRC_TTL_ASSESS_IMPROVEMENTS;PRC_TTL_ASSESS_LND;PRC_TTL_ASSESS_OB;PRC_VALUE;PRC_CMPLX_PID;PRC_CMPLX_DESC;PRC_CENSUS;PRC_TTL_MRKT_ASSESS;PRC_TTL_ASSESS;OWN_ID;OWN_NAME1;OWN_NAME2;ROW_PID;ROW_OWN_ID;ROW_LINE_NUM;ROW_OWN_PCT;ROW_PRIMARY;ROW_CREATE_DATE;ROW_MAD_ID;ROW_MAD_ISPRIMARY;OWN_LINE;MAD_MAIL_NAME1;MAD_MAIL_NAME2;MAD_MAIL_ADDR1;MAD_MAIL_CITY;MAD_MAIL_STATE;MAD_MAIL_ZIP;MAD_MAIL_ADDR2;MAD_ID;SLH_PID;SLH_LINE_NUM;SLH_SALE_DATE;SLH_BOOK;SLH_PAGE;SLH_PRICE;SLH_CURRENT_OWNER")
    print ("  BUILDING_PERMIT_TEMP & VISIDATA_TEMP joined...")
    write_log("  BUILDING_PERMIT_TEMP & VISIDATA_TEMP joined...",logfile)
except:
    print ("\n Unable to join BUILDING_PERMIT_TEMP & VISIDATA_TEMP")
    write_log("\n Unable to join BUILDING_PERMIT_TEMP & VISIDATA_TEMP", logfile)
    logging.exception('Got exception on join BUILDING_PERMIT_TEMP & VISIDATA_TEMP logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Joining BLDGPERM_VISION_VIEW with VISION_OTHER_TBL and VISION_OWNER_TBL completed")
write_log("       Joining BLDGPERM_VISION_VIEW with VISION_OTHER_TBL and VISION_OWNER_TBL completed", logfile)

try:
    # Join BUILDING_PERMIT_TEMP & VISION_BLDGPERM_SDE (joins building permit points from assessment workspace to vision data {building permit table})
    arcpy.JoinField_management(BUILDING_PERMIT_TEMP, "PERMIT_LINK", VISION_BLDGPERM_SDE, "PERMIT_LINK","BPE_PID;BPE_PERMIT_ID;BPE_FISCAL_YR;BPE_APP_DATE;BPE_ISSUE_DATE;BPE_INSPECT_DATE;BPE_AMOUNT;BPE_FEE;BPE_APPLICANT;BPE_LICENCE;BPE_COMPANY;BPE_AREA;BPE_REF;BPE_DESC;BPE_PCT_COMPLETE;BPE_DATE_COMPLETE;BPE_COMMENT;BPE_USRFLD_01;BPE_USRFLD_02;BPE_USRFLD_03;BPE_USRFLD_04;BPE_USRFLD_05;PERMIT_LINK")
except:
    print ("\n Unable to join BUILDING_PERMIT_TEMP & VISION_BLDGPERM_SDE")
    write_log("\n Unable to join BUILDING_PERMIT_TEMP & VISION_BLDGPERM_SDE", logfile)
    logging.exception('Got exception on join BUILDING_PERMIT_TEMP & VISION_BLDGPERM_SDE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("\n Updating BUILDING_PERMIT_JOINED_AUTOWKSP")
write_log("\n Updating BUILDING_PERMIT_JOINED_AUTOWKSP", logfile)

try:
    # Delete rows from Building_Permit_Joined - AUTOWORKSPACE\ASSESSMENT
    arcpy.DeleteRows_management(BUILDING_PERMIT_JOINED_AUTOWKSP)
except:
    print ("\n Unable to delete rows from Building_Permit_Joined - AST")
    write_log("\n Unable to delete rows from Building_Permit_Joined - AST", logfile)
    logging.exception('Got exception on delete rows from Building_Permit_Joined - AST logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append BUILDING_PERMIT_TEMP to BUILDING_PERMIT_JOINED_AUTOWKSP (appends temporary file of building permit points and vision data to "real" feature class)
    arcpy.Append_management(BUILDING_PERMIT_TEMP, BUILDING_PERMIT_JOINED_AUTOWKSP, "NO_TEST", 'REM_PID "PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PID,-1,-1;PERMIT_LINK "PID-PERMIT #" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PERMIT_LINK,-1,-1;EDITOR "EDITOR" true true false 255 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,EDITOR,-1,-1;DATE_EDIT "DATE_EDIT" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,DATE_EDIT,-1,-1;REM_MNC "REM_MNC" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MNC,-1,-1;REM_PID_1 "PID Number" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PID_1,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PIN,-1,-1;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "Lot" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_BLDG_NAME,-1,-1;REM_USE_CODE "Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_USE_CODE,-1,-1;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_USRFLD,-1,-1;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_USRFLD_DESC,-1,-1;PID_TEXT "PID Text format" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PID_TEXT,-1,-1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,LND_USE_CODE,-1,-1;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,LND_DSTRCT,-1,-1;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_PF_LOCN,-1,-1;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_PF_LOCN_DESC,-1,-1;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_ASSESS,-1,-1;OWN_ID "OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,OWN_NAME2,-1,-1;ROW_PID "ROW_PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,OWN_LINE,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_ADDR2,-1,-1;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_BOOK,-1,-1;SLH_PAGE "Deed Page" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_PAGE,-1,-1;SLH_PRICE "Sale Price" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_CURRENT_OWNER,-1,-1;BPE_PID "BPE_PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_PID,-1,-1;BPE_PERMIT_ID "BPE_PERMIT_ID" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_PERMIT_ID,-1,-1;BPE_FISCAL_YR "BPE_FISCAL_YR" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_FISCAL_YR,-1,-1;BPE_APP_DATE "BPE_APP_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_APP_DATE,-1,-1;BPE_ISSUE_DATE "BPE_ISSUE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_ISSUE_DATE,-1,-1;BPE_INSPECT_DATE "BPE_INSPECT_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_INSPECT_DATE,-1,-1;BPE_AMOUNT "BPE_AMOUNT" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_AMOUNT,-1,-1;BPE_FEE "BPE_FEE" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_FEE,-1,-1;BPE_APPLICANT "BPE_APPLICANT" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_APPLICANT,-1,-1;BPE_LICENCE "BPE_LICENCE" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_LICENCE,-1,-1;BPE_COMPANY "BPE_COMPANY" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_COMPANY,-1,-1;BPE_AREA "BPE_AREA" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_AREA,-1,-1;BPE_REF "BPE_REF" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_REF,-1,-1;BPE_DESC "BPE_DESC" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_DESC,-1,-1;BPE_PCT_COMPLETE "BPE_PCT_COMPLETE" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_PCT_COMPLETE,-1,-1;BPE_DATE_COMPLETE "BPE_DATE_COMPLETE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_DATE_COMPLETE,-1,-1;BPE_COMMENT "BPE_COMMENT" true true false 750 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_COMMENT,-1,-1;BPE_USRFLD_01 "BPE_USRFLD_01" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_USRFLD_01,-1,-1;BPE_USRFLD_02 "BPE_USRFLD_02" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_USRFLD_02,-1,-1;BPE_USRFLD_03 "BPE_USRFLD_03" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_USRFLD_03,-1,-1;BPE_USRFLD_04 "BPE_USRFLD_04" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_USRFLD_04,-1,-1;BPE_USRFLD_05 "BPE_USRFLD_05" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_USRFLD_05,-1,-1;PERMIT_LINK_1 "PERMIT_LINK_1" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PERMIT_LINK_1,-1,-1', "")
    BLDG_PMT_result = arcpy.GetCount_management(BUILDING_PERMIT_JOINED_AUTOWKSP)
    print ('{} has {} records'.format(BUILDING_PERMIT_JOINED_AUTOWKSP, BLDG_PMT_result[0]))
    write_log('{} has {} records'.format(BUILDING_PERMIT_JOINED_AUTOWKSP, BLDG_PMT_result[0]), logfile)
except:
    print ("\n Unable to append BUILDING_PERMIT_TEMP to BUILDING_PERMIT_JOINED_AUTOWKSP")
    write_log("\n Unable to append BUILDING_PERMIT_TEMP to BUILDING_PERMIT_JOINED_AUTOWKSP", logfile)
    logging.exception('Got exception on append BUILDING_PERMIT_TEMP to BUILDING_PERMIT_JOINED_AUTOWKSP logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    

print ("       Updating BUILDING_PERMIT_JOINED_AUTOWKSP")
write_log("       Updating BUILDING_PERMIT_JOINED_AUTOWKSP", logfile)

print ("\n Make feature layer of Pictometry Flags, join in BLDGPERM_VISION_View, then update Pictometry Flags Joined - AUTOWORKSPACE")
write_log("\n Make feature layer of Pictometry Flags, join in BLDGPERM_VISION_View, then update Pictometry Flags Joined - AUTOWORKSPACE", logfile)

try:
    # Make temporary feature from Pictometry2014_flags - AST (creates temporary file of 2014 Pictometry Flags points from assessment workspace)
    Pictometry2014_flags_TEMP = arcpy.FeatureClassToFeatureClass_conversion(PICTOMETRY_2014_FLAGS_AST, AUTOWORKSPACE_AST, "Pictometry2014_flags_TEMP", "", 'REM_PID "PID" true true false 4 Long 0 10 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Pictometry2014_flags,REM_PID,-1,-1;PERMIT_LINK "PID-PERMIT #" true true false 100 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Pictometry2014_flags,PERMIT_LINK,-1,-1;EDITOR "EDITOR" true true false 255 Text 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Pictometry2014_flags,EDITOR,-1,-1;EDIT_DATE "EDIT_DATE" false true false 8 Date 0 0 ,First,#,Database Connections\AST@ccsde.sde\CCSDE.AST.Crawford_Parcels\CCSDE.AST.Pictometry2014_flags,EDIT_DATE,-1,-1', "")
except:
    print ("\n Unable to make temporary feature from Pictometry2014_flags - AST")
    write_log("\n Unable to make temporary feature from Pictometry2014_flags - AST", logfile)
    logging.exception('Got exception on make temporary feature from Pictometry2014_flags - AST logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Join Pictometry2014_flags_TEMP to VISION_BLDGPERM_SDE (join building permit table to Pictometry flags FC)
    arcpy.JoinField_management(Pictometry2014_flags_TEMP, "REM_PID", VISION_BLDGPERM_SDE, "BPE_PID", "BPE_PID;BPE_PERMIT_ID;BPE_FISCAL_YR;BPE_APP_DATE;BPE_ISSUE_DATE;BPE_INSPECT_DATE;BPE_AMOUNT;BPE_FEE;BPE_APPLICANT;BPE_LICENCE;BPE_COMPANY;BPE_AREA;BPE_REF;BPE_DESC;BPE_PCT_COMPLETE;BPE_DATE_COMPLETE;BPE_COMMENT;BPE_USRFLD_01;BPE_USRFLD_02;BPE_USRFLD_03;BPE_USRFLD_04;BPE_USRFLD_05;PERMIT_LINK")
    print ("  Joining Pictometry flags - AST to VISION_BLDGPERM_SDE completed...")
    write_log("  Joining Pictometry flags - AST to VISION_BLDGPERM_SDE completed...",logfile)
except:
    print ("\n Unable to join Pictometry2014_flags_TEMP & VISION_BLDGPERM_SDE")
    write_log("\n Unable to join Pictometry2014_flags_TEMP & VISION_BLDGPERM_SDE", logfile)
    logging.exception('Got exception on join Pictometry2014_flags_TEMP & VISION_BLDGPERM_SDE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Join Pictometry2014_flags_TEMP to VISIDATA_TEMP (join visidata temp table that was created above to Pictometry flags FC)
    arcpy.JoinField_management(Pictometry2014_flags_TEMP, "REM_PID", VISIDATA_TEMP, "REM_PID", "REM_MNC;REM_PID;REM_PIN;REM_OWN_NAME;REM_PRCL_LOCN;REM_PRCL_LOCN_CITY;REM_PRCL_LOCN_STT;REM_PRCL_LOCN_ZIP;REM_ALT_PRCL_ID;REM_PRCL_STATUS_DATE;REM_MBLU_MAP;REM_MBLU_MAP_CUT;REM_MBLU_BLOCK;REM_MBLU_BLOCK_CUT;REM_MBLU_LOT;REM_MBLU_LOT_CUT;REM_MBLU_UNIT;REM_MBLU_UNIT_CUT;REM_STATUS_DATE;REM_INET_SUPPRESS;REM_IS_CONDO_MAIN;REM_CMPLX_NAME;REM_BLDG_NAME;REM_USE_CODE;REM_LEGAL_AREA;REM_LAST_UPDATE;REM_USRFLD;REM_USRFLD_DESC;PID_TEXT;LND_USE_CODE;LND_USE_DESC;LND_DSTRCT;PRC_PF_LOCN;PRC_PF_LOCN_DESC;PRC_USRFLD_09;PRC_USRFLD_10;PRC_TTL_ASSESS_BLDG;PRC_TTL_ASSESS_IMPROVEMENTS;PRC_TTL_ASSESS_LND;PRC_TTL_ASSESS_OB;PRC_VALUE;PRC_CMPLX_PID;PRC_CMPLX_DESC;PRC_CENSUS;PRC_TTL_MRKT_ASSESS;PRC_TTL_ASSESS;OWN_ID;OWN_NAME1;OWN_NAME2;ROW_PID;ROW_OWN_ID;ROW_LINE_NUM;ROW_OWN_PCT;ROW_PRIMARY;ROW_CREATE_DATE;ROW_MAD_ID;ROW_MAD_ISPRIMARY;OWN_LINE;MAD_MAIL_NAME1;MAD_MAIL_NAME2;MAD_MAIL_ADDR1;MAD_MAIL_CITY;MAD_MAIL_STATE;MAD_MAIL_ZIP;MAD_MAIL_ADDR2;MAD_ID;SLH_PID;SLH_LINE_NUM;SLH_SALE_DATE;SLH_BOOK;SLH_PAGE;SLH_PRICE;SLH_CURRENT_OWNER")
    print ("   Joining Pictometry flags - AST to VISIDATA_TEMP completed...")
    write_log("   Joining Pictometry flags - AST to VISIDATA_TEMP completed...",logfile)
except:
    print ("\n Unable to join Pictometry2014_flags_TEMP & VISIDATA_TEMP")
    write_log("\n Unable to join Pictometry2014_flags_TEMP & VISIDATA_TEMP", logfile)
    logging.exception('Got exception on join Pictometry2014_flags_TEMP & VISIDATA_TEMP logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Delete rows from Pictometry2014_flags_Joined - AUTOWORKSPACE
    arcpy.DeleteRows_management(PICTOMETRY_2014_FLAGS_JOINED_AUTOWKSP)
except:
    print ("\n Unable to delete rows from Pictometry2014_flags_Joined - AUTOWORKSPACE")
    write_log("\n Unable to delete rows from Pictometry2014_flags_Joined - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on delete rows from Pictometry2014_flags_Joined - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Pictometry2014_flags_TEMP to Pictometry2014_flags_Joined - AUTOWORKSPACE (appends temporary file of pictometry flags points and vision data to "real" feature class)
    arcpy.Append_management(Pictometry2014_flags_TEMP, PICTOMETRY_2014_FLAGS_JOINED_AUTOWKSP, "NO_TEST", 'REM_PID "PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_PID,-1,-1;PERMIT_LINK "PID-PERMIT #" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PERMIT_LINK,-1,-1;EDITOR "EDITOR" true true false 255 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,EDITOR,-1,-1;EDIT_DATE "EDIT_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,EDIT_DATE,-1,-1;BPE_PID "BPE_PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_PID,-1,-1;BPE_PERMIT_ID "BPE_PERMIT_ID" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_PERMIT_ID,-1,-1;BPE_FISCAL_YR "BPE_FISCAL_YR" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_FISCAL_YR,-1,-1;BPE_APP_DATE "BPE_APP_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_APP_DATE,-1,-1;BPE_ISSUE_DATE "BPE_ISSUE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_ISSUE_DATE,-1,-1;BPE_INSPECT_DATE "BPE_INSPECT_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_INSPECT_DATE,-1,-1;BPE_AMOUNT "BPE_AMOUNT" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_AMOUNT,-1,-1;BPE_FEE "BPE_FEE" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_FEE,-1,-1;BPE_APPLICANT "BPE_APPLICANT" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_APPLICANT,-1,-1;BPE_LICENCE "BPE_LICENCE" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_LICENCE,-1,-1;BPE_COMPANY "BPE_COMPANY" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_COMPANY,-1,-1;BPE_AREA "BPE_AREA" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_AREA,-1,-1;BPE_REF "BPE_REF" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_REF,-1,-1;BPE_DESC "BPE_DESC" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_DESC,-1,-1;BPE_PCT_COMPLETE "BPE_PCT_COMPLETE" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_PCT_COMPLETE,-1,-1;BPE_DATE_COMPLETE "BPE_DATE_COMPLETE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_DATE_COMPLETE,-1,-1;BPE_COMMENT "BPE_COMMENT" true true false 750 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_COMMENT,-1,-1;BPE_USRFLD_01 "BPE_USRFLD_01" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_USRFLD_01,-1,-1;BPE_USRFLD_02 "BPE_USRFLD_02" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_USRFLD_02,-1,-1;BPE_USRFLD_03 "BPE_USRFLD_03" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_USRFLD_03,-1,-1;BPE_USRFLD_04 "BPE_USRFLD_04" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_USRFLD_04,-1,-1;BPE_USRFLD_05 "BPE_USRFLD_05" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,BPE_USRFLD_05,-1,-1;PERMIT_LINK_1 "PERMIT_LINK_1" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PERMIT_LINK_1,-1,-1;REM_MNC "REM_MNC" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_MNC,-1,-1;REM_PID_1 "PID Number" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_PID_1,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_PIN,-1,-1;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "Lot" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_BLDG_NAME,-1,-1;REM_USE_CODE "Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_USE_CODE,-1,-1;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_USRFLD,-1,-1;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,REM_USRFLD_DESC,-1,-1;PID_TEXT "PID Text format" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PID_TEXT,-1,-1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,LND_USE_CODE,-1,-1;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,LND_DSTRCT,-1,-1;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_PF_LOCN,-1,-1;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_PF_LOCN_DESC,-1,-1;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,PRC_TTL_ASSESS,-1,-1;OWN_ID "OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,OWN_NAME2,-1,-1;ROW_PID "ROW_PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,OWN_LINE,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,MAD_MAIL_ADDR2,-1,-1;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,SLH_BOOK,-1,-1;SLH_PAGE "Deed Page" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,SLH_PAGE,-1,-1;SLH_PRICE "Sale Price" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Pictometry2014_flags_TEMP,SLH_CURRENT_OWNER,-1,-1', "")
    PictometryFlag_result = arcpy.GetCount_management(PICTOMETRY_2014_FLAGS_JOINED_AUTOWKSP)
    print ('{} has {} records'.format(PICTOMETRY_2014_FLAGS_JOINED_AUTOWKSP, PictometryFlag_result[0]))
    write_log('{} has {} records'.format(PICTOMETRY_2014_FLAGS_JOINED_AUTOWKSP, PictometryFlag_result[0]), logfile)
except:
    print ("\n Unable to append Pictometry2014_flags_TEMP to Pictometry2014_flags_Joined - AUTOWORKSPACE")
    write_log("\n Unable to append Pictometry2014_flags_TEMP to Pictometry2014_flags_Joined - AUTOWORKSPACE", logfile)
    logging.exception('Got exception on append Pictometry2014_flags_TEMP to Pictometry2014_flags_Joined - AUTOWORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()


BLDG_PERMIT_TEMP = [Pictometry2014_flags_TEMP, VISIDATA_TEMP, BUILDING_PERMIT_TEMP]

try:
    # Delete views and temp files used in process (deletes temporary files from workspace)
    for Views in BLDG_PERMIT_TEMP:
        delete_input = Views
        arcpy.Delete_management(delete_input, "")
    print ("   BLDG_PERMIT_TEMP files deleted...")
    write_log("   BLDG_PERMIT_TEMP files deleted...",logfile)
except:
    print ("\n Unable to delete BLDG_PERMIT_TEMP files")
    write_log("\n Unable to delete BLDG_PERMIT_TEMP files", logfile)
    logging.exception('Got exception on delete BLDG_PERMIT_TEMP files logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Make feature layer of Pictometry Flags, join in BLDGPERM_VISION_View, then update Pictometry Flags Joined - AUTOWORKSPACE completed")
write_log("       Make feature layer of Pictometry Flags, join in BLDGPERM_VISION_View, then update Pictometry Flags Joined - AUTOWORKSPACE completed", logfile)

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
    # make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = CITY OF MEADVILLE) // (make temporary feature of tax parcels - which contains information to create Meadville blocks in following steps)
    MDVL_BLOCKS_View = arcpy.MakeFeatureLayer_management(TAXPARCEL_JOINED_AUTOWKSP, "MDVL_BLOCKS_View", "SEC_MUNI_NAME = 'CITY OF MEADVILLE'", "", "OBJECTID OBJECTID VISIBLE NONE;CAMA_PIN CAMA_PIN VISIBLE NONE;MAP MAP VISIBLE NONE;PARCEL PARCEL VISIBLE NONE;LOT LOT VISIBLE NONE;ID_PIN ID_PIN VISIBLE NONE;MAPTYPE MAPTYPE VISIBLE NONE;CITY CITY VISIBLE NONE;MEADVILLE MEADVILLE VISIBLE NONE;TITUSVILLE TITUSVILLE VISIBLE NONE;BLK_MAP BLK_MAP VISIBLE NONE;BLK_PARCEL BLK_PARCEL VISIBLE NONE;BLK_MAPTYPE BLK_MAPTYPE VISIBLE NONE;INS_MAP INS_MAP VISIBLE NONE;INS_DESCRIPTION INS_DESCRIPTION VISIBLE NONE;INS_SECTION_MAP INS_SECTION_MAP VISIBLE NONE;INS_SCALE INS_SCALE VISIBLE NONE;INS_ROTATION INS_ROTATION VISIBLE NONE;SEC_MAP SEC_MAP VISIBLE NONE;SEC_MUNI_NAME SEC_MUNI_NAME VISIBLE NONE;SEC_ANGLE SEC_ANGLE VISIBLE NONE;SEC_SCALE SEC_SCALE VISIBLE NONE;SEC_ROTATION SEC_ROTATION VISIBLE NONE;SEC_WARD SEC_WARD VISIBLE NONE;MDVL_BLK_MAP MDVL_BLK_MAP VISIBLE NONE;MDVL_BLK_PARCEL MDVL_BLK_PARCEL VISIBLE NONE;MDVL_BLK_MAPTYPE MDVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_MAP TSVL_BLK_MAP VISIBLE NONE;TSVL_BLK_PARCEL TSVL_BLK_PARCEL VISIBLE NONE;TSVL_BLK_MAPTYPE TSVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_ID TSVL_BLK_ID VISIBLE NONE;PID PID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;GIS_ACRES GIS_ACRES VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print ("\n Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = CITY OF MEADVILLE)")
    write_log("Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = CITY OF MEADVILLE)", logfile)
    logging.exception('Got exception on make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = CITY OF MEADVILLE) logged at:' + str(Day) + " " + str(Time))
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
    # make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = CITY OF TITUSVILLE) // (make temporary feature of tax parcels - which contains information to create Titusville blocks in following steps)
    TSVL_BLOCKS_View = arcpy.MakeFeatureLayer_management(TAXPARCEL_JOINED_AUTOWKSP, "TSVL_BLOCKS_View", "SEC_MUNI_NAME = 'CITY OF TITUSVILLE'", "", "OBJECTID OBJECTID VISIBLE NONE;CAMA_PIN CAMA_PIN VISIBLE NONE;MAP MAP VISIBLE NONE;PARCEL PARCEL VISIBLE NONE;LOT LOT VISIBLE NONE;ID_PIN ID_PIN VISIBLE NONE;MAPTYPE MAPTYPE VISIBLE NONE;CITY CITY VISIBLE NONE;MEADVILLE MEADVILLE VISIBLE NONE;TITUSVILLE TITUSVILLE VISIBLE NONE;BLK_MAP BLK_MAP VISIBLE NONE;BLK_PARCEL BLK_PARCEL VISIBLE NONE;BLK_MAPTYPE BLK_MAPTYPE VISIBLE NONE;INS_MAP INS_MAP VISIBLE NONE;INS_DESCRIPTION INS_DESCRIPTION VISIBLE NONE;INS_SECTION_MAP INS_SECTION_MAP VISIBLE NONE;INS_SCALE INS_SCALE VISIBLE NONE;INS_ROTATION INS_ROTATION VISIBLE NONE;SEC_MAP SEC_MAP VISIBLE NONE;SEC_MUNI_NAME SEC_MUNI_NAME VISIBLE NONE;SEC_ANGLE SEC_ANGLE VISIBLE NONE;SEC_SCALE SEC_SCALE VISIBLE NONE;SEC_ROTATION SEC_ROTATION VISIBLE NONE;SEC_WARD SEC_WARD VISIBLE NONE;MDVL_BLK_MAP MDVL_BLK_MAP VISIBLE NONE;MDVL_BLK_PARCEL MDVL_BLK_PARCEL VISIBLE NONE;MDVL_BLK_MAPTYPE MDVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_MAP TSVL_BLK_MAP VISIBLE NONE;TSVL_BLK_PARCEL TSVL_BLK_PARCEL VISIBLE NONE;TSVL_BLK_MAPTYPE TSVL_BLK_MAPTYPE VISIBLE NONE;TSVL_BLK_ID TSVL_BLK_ID VISIBLE NONE;PID PID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;GIS_ACRES GIS_ACRES VISIBLE NONE;SHAPE.STArea() SHAPE.STArea() VISIBLE NONE;SHAPE.STLength() SHAPE.STLength() VISIBLE NONE")
except:
    print ("\n Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = CITY OF TITUSVILLE)")
    write_log("Unable to make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = CITY OF TITUSVILLE)", logfile)
    logging.exception('Got exception on make feature layer from TAXPARCEL_JOINED_AUTOWKSP (selecting SEC_MUNI_NAME = CITY OF TITUSVILLE) logged at:' + str(Day) + " " + str(Time))
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
