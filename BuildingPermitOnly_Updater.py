# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# BuildingPermitOnly_Updater.py
# Created on: 2019-05-09 
# Updated on 2021-07-18
#
# Author: Phil Baranyai/GIS Manager
#
#
# Description: 
#  Build feature classes from AST workspace -> AUTO_WORKSPACE, and join in VISION tables:
#
# Building Permits
# Assessment Only CAMA table
#
# Updates ALL VISION tables and Building permits.
#
# This tool updates VISION records M-F for Assessment Dashboard, & Building Permits.   Separate tool
# updates parcels runs Saturdays from hardlines and uses the most current VISION tables from this tool.
# 
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import collections
import datetime
import os
import traceback
import logging
from arcpy import env

# Stop geoprocessing log history in metadata
arcpy.SetLogHistory(False)

# Setup error logging
logfile = r"R:\\GIS\\GIS_LOGS\\Assessment\\BuildingPermitOnly_Updater.log"  
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
Database_Connections = r"\\CCFILE\\anybody\\GIS\\ArcAutomations\\Database_Connections"

#Database variables:
AST = Database_Connections + "\\AST@ccsde.sde"
AUTOWORKSPACE = Database_Connections + "\\auto_workspace@ccsde.sde"
AUTOWORKSPACE_AST = Database_Connections + "\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment"
VISION_VIEW = Database_Connections + "\\Vision_Database.sde"
CRAW_INTERNAL = Database_Connections + "\\craw_internal@ccsde.sde"
PUBLIC_WEB = Database_Connections + "\\public_web@ccsde.sde"
LOCATOR_WKSP = r"\\CCFILE\\anybody\\GIS\\CurrentWebsites\\Locators\\Intranet_Locators"
AST_REPORTS_FLDR = r"\\CCFILE\\anybody\\GIS\\Assessment\\Reports"

# Local variables:
BLDG_PRMT_AST = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.Building_Permit_Base"
BLDGPERM_TBL_VISION = VISION_VIEW + "\\VISION.REAL_PROP.BLDGPERM"
BLDGPERM_TBL_AUTOWKSP = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.BLDGPERM_TBL"
BUILDING_PERMIT_JOINED_AUTOWKSP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.Building_Permit_Joined"
BUILDING_PERMITS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.BUILDING_PERMITS_INTERNAL"
BUILDING_PERMIT_TEMP = AUTOWORKSPACE_AST + "\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP"
BUILDING_PERMIT_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Land_Records\\CCSDE.PUBLIC_WEB.BUILDING_PERMITS_WEB"
EXEMPTS_VISION = VISION_VIEW + "\\VISION.REAL_PROP.EXEMPTS"
LAND_VISION = VISION_VIEW + "\\VISION.REAL_PROP.LAND"
MAILADDRESS_VISION = VISION_VIEW + "\\VISION.COMMON.MAILADDRESS"
OWNER_VISION = VISION_VIEW + "\\VISION.COMMON.OWNER"
PARCEL_VISION = VISION_VIEW + "\\VISION.REAL_PROP.PARCEL"
REALOWNERSHIP_VISION = VISION_VIEW + "\\VISION.REAL_PROP.REAL_OWNERSHIP"
REALMAST_VISION = VISION_VIEW + "\\VISION.REAL_PROP.REALMAST"
SALESHISTORY_VISION = VISION_VIEW + "\\VISION.REAL_PROP.SALEHIST"
VISITHISTORY_VISON = VISION_VIEW + "\\VISION.REAL_PROP.VISITHST"
CAMA_RECORDS_TBL = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Assessment_CAMA_Records_Table"
CC_PARCEL_LOC = LOCATOR_WKSP + "\\CAMA_PID_Locator"
UNMATCHED_PERMITS_EXCEL = AST_REPORTS_FLDR + "\\Unmatched_GIS_Building_Permits.xls"


# Local variable - tables
VISION_BLDGPERM_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_BLDGPERM_TBL"
VISIDATA_TEMP = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISIDATA_Temp"
VISION_EXEMPTS_TBL_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_EXEMPTS_TBL"
VISION_OTHER_TBL_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL"
VISION_OWNER_TBL_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL"
VISION_LAND_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_LAND_TBL"
VISION_MAILADDRESS_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_MAILADDRESS_TBL"
VISION_OWNER_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_OWNER_TBL"
VISION_PARCEL_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_PARCEL_TBL"
VISION_REAL_OWNERSHIP_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_REAL_OWNERSHIP_TBL"
VISION_REALMAST_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL"
VISION_SALES_HISTORY_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_SALES_HISTORY_TBL"
VISION_TEMP_JOIN_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_TEMP_JOIN_TBL"
VISION_OWNER_TBL_WEBTemp = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_OWNER_TBL_WEBTemp"
CURRENT_OWNER_TBL_CO_Temp = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.CURRENT_OWNER_TBL_CO_Temp"
VISION_BLDGPERM_SDE_GC = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_BLDGPERM_SDE_GC"

start_time = time.time()

print ("============================================================================")
print ("Updating Assessment Datasets: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nBuilding Permits Feature Class")
print ("All Assessment CAMA tables")
print ("============================================================================")
write_log("============================================================================", logfile)
write_log("Updating Assessment Datasets: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nBuilding Permits Feature Class", logfile)
write_log("All Assessment CAMA tables", logfile)
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
    if arcpy.Exists(BUILDING_PERMIT_TEMP):
        arcpy.Delete_management(CURRENT_OWNER_TBL_CO_Temp, "Table")
        print (CURRENT_OWNER_TBL_CO_Temp + " found - table deleted")
        write_log(CURRENT_OWNER_TBL_CO_Temp + " found - table deleted", logfile)
    if arcpy.Exists(BUILDING_PERMIT_TEMP):
        arcpy.Delete_management(VISION_BLDGPERM_SDE_GC, "Table")
        print (VISION_BLDGPERM_SDE_GC + " found - table deleted")
        write_log(VISION_BLDGPERM_SDE_GC + " found - table deleted", logfile)
    if arcpy.Exists(UNMATCHED_PERMITS_EXCEL):
        os.remove(UNMATCHED_PERMITS_EXCEL)
        print (UNMATCHED_PERMITS_EXCEL + " found - table deleted")
        write_log(UNMATCHED_PERMITS_EXCEL + " found - table deleted", logfile)
except:
    print ("\n Unable to delete VISION_OWNER_TBL_WEBTemp, VISION_OWNER_TBL_SDE or VISION_OTHER_TBL_SDE, need to delete existing FGDB manually and/or close program locking the tables")
    write_log("\n Unable to create new VISION_OWNER_TBL_WEBTemp, VISION_OWNER_TBL_SDE or VISION_OTHER_TBL_SDE, need to delete existing FGDB manually and/or close program locking the tables", logfile)
    logging.exception('Got exception on delete VISION_OWNER_TBL_WEBTemp, VISION_OWNER_TBL_SDE or VISION_OTHER_TBL_SDE logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

VISION_ESRI_TABLES = [VISION_BLDGPERM_SDE,VISION_LAND_SDE,VISION_MAILADDRESS_SDE,VISION_OWNER_SDE,VISION_PARCEL_SDE,VISION_REAL_OWNERSHIP_SDE,VISION_REALMAST_SDE,VISION_SALES_HISTORY_SDE,VISION_EXEMPTS_TBL_SDE]

try:
    # Delete rows from ESRI/Vision temp tables, program will obtain fresh data from live vision view
    print ("\n  Cleaning out VISION-ESRI tables")
    write_log("\n  Cleaning out VISION-ESRI tables", logfile)
    for Table in VISION_ESRI_TABLES:
        delete_input = Table
        arcpy.DeleteRows_management(delete_input)
    print ("   VISION-ESRI tables cleaned out at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("   VISION-ESRI tables cleaned out at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to delete rows from Vision ESRI tables")
    write_log("\n Unable to delete rows from Vision ESRI tables", logfile)
    logging.exception('Got exception on delete rows from Vision ESRI tables logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append data from live VISION view tables to SDE tables AUTO_WORKSPACE
    print ("\n    Appending data from VISION tables to SDE tables...")
    write_log("\n    Appending data from VISION tables to SDE tables...",logfile)
    arcpy.Append_management(BLDGPERM_TBL_VISION, VISION_BLDGPERM_SDE, "NO_TEST", 'BPE_PID "BPE_PID" true false false 4 Long 0 10 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_PID,-1,-1;BPE_PERMIT_ID "BPE_PERMIT_ID" true true false 20 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_PERMIT_ID,-1,-1;BPE_FISCAL_YR "BPE_FISCAL_YR" true false false 2 Short 0 5 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_FISCAL_YR,-1,-1;BPE_APP_DATE "BPE_APP_DATE" true true false 8 Date 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_APP_DATE,-1,-1;BPE_ISSUE_DATE "BPE_ISSUE_DATE" true true false 8 Date 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_ISSUE_DATE,-1,-1;BPE_INSPECT_DATE "BPE_INSPECT_DATE" true true false 8 Date 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_INSPECT_DATE,-1,-1;BPE_AMOUNT "BPE_AMOUNT" true true false 4 Long 0 10 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_AMOUNT,-1,-1;BPE_FEE "BPE_FEE" true true false 4 Long 0 10 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_FEE,-1,-1;BPE_APPLICANT "BPE_APPLICANT" true true false 50 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_APPLICANT,-1,-1;BPE_LICENCE "BPE_LICENCE" true true false 20 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_LICENCE,-1,-1;BPE_COMPANY "BPE_COMPANY" true true false 50 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_COMPANY,-1,-1;BPE_AREA "BPE_AREA" true true false 20 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_AREA,-1,-1;BPE_REF "BPE_REF" true true false 20 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_REF,-1,-1;BPE_DESC "BPE_DESC" true true false 40 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_TYPE,-1,-1;BPE_PCT_COMPLETE "BPE_PCT_COMPLETE" true true false 4 Long 0 10 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_PCT_COMPLETE,-1,-1;BPE_DATE_COMPLETE "BPE_DATE_COMPLETE" true true false 8 Date 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_DATE_COMPLETE,-1,-1;BPE_COMMENT "BPE_COMMENT" true true false 750 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_COMMENT,-1,-1;BPE_USRFLD_01 "BPE_USRFLD_01" true true false 100 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_USRFLD_01,-1,-1;BPE_USRFLD_02 "BPE_USRFLD_02" true true false 100 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_USRFLD_02,-1,-1;BPE_USRFLD_03 "BPE_USRFLD_03" true true false 100 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_USRFLD_03,-1,-1;BPE_USRFLD_04 "BPE_USRFLD_04" true true false 100 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_USRFLD_04,-1,-1;BPE_USRFLD_05 "BPE_USRFLD_05" true true false 100 Text 0 0 ,First,#,'+BLDGPERM_TBL_VISION+',BPE_USRFLD_05,-1,-1;PERMIT_LINK "PERMIT_LINK" true true false 100 Text 0 0 ,First,#', "")
    print ("     BLDGPERM table appended at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("     BLDGPERM table appended at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    arcpy.Append_management(LAND_VISION, VISION_LAND_SDE, "NO_TEST", 'LND_PID "LND_PID" true false false 4 Long 0 10 ,First,#,'+LAND_VISION+',LND_PID,-1,-1;LND_LINE_ID "LND_LINE_ID" true false false 4 Long 0 10 ,First,#,'+LAND_VISION+',LND_LINE_ID,-1,-1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0 ,First,#,'+LAND_VISION+',LND_USE_CODE,-1,-1;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0 ,First,#,'+LAND_VISION+',LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,'+LAND_VISION+',LND_DSTRCT,-1,-1;MUNI_NAME "Municipality Name" true true false 75 Text 0 0 ,First,#,'+LAND_VISION+',LND_DSTRCT,-1,-1', "")
    print ("     LAND table appended at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("     LAND table appended at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    arcpy.Append_management(MAILADDRESS_VISION, VISION_MAILADDRESS_SDE, "NO_TEST", 'MAD_MNC "MAD_MNC" true false false 4 Long 0 10 ,First,#,'+MAILADDRESS_VISION+',MAD_MNC,-1,-1;MAD_MAIL_NAME1 "MAD_MAIL_NAME1" true true false 85 Text 0 0 ,First,#,'+MAILADDRESS_VISION+',MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "MAD_MAIL_NAME2" true true false 85 Text 0 0 ,First,#,'+MAILADDRESS_VISION+',MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "MAD_MAIL_ADDR1" true true false 50 Text 0 0 ,First,#,'+MAILADDRESS_VISION+',MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "MAD_MAIL_CITY" true true false 30 Text 0 0 ,First,#,'+MAILADDRESS_VISION+',MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "MAD_MAIL_STATE" true true false 20 Text 0 0 ,First,#,'+MAILADDRESS_VISION+',MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "MAD_MAIL_ZIP" true true false 20 Text 0 0 ,First,#,'+MAILADDRESS_VISION+',MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "MAD_MAIL_ADDR2" true true false 50 Text 0 0 ,First,#,'+MAILADDRESS_VISION+',MAD_MAIL_ADDR2,-1,-1;MAD_ID "MAD_ID" true false false 4 Long 0 10 ,First,#,'+MAILADDRESS_VISION+',MAD_ID,-1,-1', "")
    print ("     MAILADDRESS table appended at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("     MAILADDRESS table appended at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    arcpy.Append_management(OWNER_VISION, VISION_OWNER_SDE, "NO_TEST", 'OWN_ID "OWN_ID" true false false 4 Long 0 0 ,First,#,'+OWNER_VISION+',OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,'+OWNER_VISION+',OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,'+OWNER_VISION+',OWN_NAME2,-1,-1', "")
    print ("     OWNER table appended at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("     OWNER table appended at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    VIS_EXEMPTS_TBL_View = arcpy.MakeTableView_management(EXEMPTS_VISION, "VIS_EXEMPTS_TBL_View", "EXE_CODE = 'E' OR EXE_CODE = 'F' OR EXE_CODE = 'H'", "", "EXE_MNC EXE_MNC VISIBLE NONE;EXE_PID EXE_PID VISIBLE NONE;EXE_LINE_NUM EXE_LINE_NUM VISIBLE NONE;EXE_YR EXE_YR VISIBLE NONE;EXE_CODE EXE_CODE VISIBLE NONE;EXE_TYPE EXE_TYPE VISIBLE NONE;EXE_AMT EXE_AMT VISIBLE NONE;EXE_STATUS_DATE EXE_STATUS_DATE VISIBLE NONE;EXE_START_DATE EXE_START_DATE VISIBLE NONE;EXE_END_DATE EXE_END_DATE VISIBLE NONE;EXE_USRFLD_01 EXE_USRFLD_01 VISIBLE NONE;EXE_USRFLD_01_DESC EXE_USRFLD_01_DESC VISIBLE NONE;EXE_USRFLD_02 EXE_USRFLD_02 VISIBLE NONE;EXE_USRFLD_02_DESC EXE_USRFLD_02_DESC VISIBLE NONE;EXE_USRFLD_03 EXE_USRFLD_03 VISIBLE NONE;EXE_USRFLD_03_DESC EXE_USRFLD_03_DESC VISIBLE NONE;EXE_USRFLD_04 EXE_USRFLD_04 VISIBLE NONE;EXE_USRFLD_04_DESC EXE_USRFLD_04_DESC VISIBLE NONE;EXE_USRFLD_05 EXE_USRFLD_05 VISIBLE NONE;EXE_USRFLD_05_DESC EXE_USRFLD_05_DESC VISIBLE NONE;EXE_USRFLD_06 EXE_USRFLD_06 VISIBLE NONE;EXE_USRFLD_06_DESC EXE_USRFLD_06_DESC VISIBLE NONE;EXE_CREATE_DATE EXE_CREATE_DATE VISIBLE NONE;EXE_LAST_UPDATE EXE_LAST_UPDATE VISIBLE NONE;ESRI_OID ESRI_OID VISIBLE NONE")
    arcpy.Append_management(VIS_EXEMPTS_TBL_View, VISION_EXEMPTS_TBL_SDE, "NO_TEST", 'EXE_PID "EXE_PID" true false false 4 Long 0 10 ,First,#,VIS_EXEMPTS_TBL_View,EXE_PID,-1,-1;EXE_LINE_NUM "EXE_LINE_NUM" true false false 4 Long 0 10 ,First,#,VIS_EXEMPTS_TBL_View,EXE_LINE_NUM,-1,-1;EXE_YR "EXE_YR" true true false 4 Long 0 10 ,First,#,VIS_EXEMPTS_TBL_View,EXE_YR,-1,-1;EXE_CODE "EXE_CODE" true true false 6 Text 0 0 ,First,#,VIS_EXEMPTS_TBL_View,EXE_CODE,-1,-1;EXE_TYPE "EXE_TYPE" true true false 30 Text 0 0 ,First,#,VIS_EXEMPTS_TBL_View,EXE_TYPE,-1,-1;EXE_LAST_UPDATE "EXE_LAST_UPDATE" true true false 8 Date 0 0 ,First,#,VIS_EXEMPTS_TBL_View,EXE_LAST_UPDATE,-1,-1', "")
    print ("      EXEMPTS table appended at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("      EXEMPTS table appended at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    # In the append for the Parcel table, the fields match, except for PRC_PF_LOCN & PRC_PF_LOCN_DESC, they were altered to pull from PRCP_PF_10 & PRC_PF_10_DESC (respectively)
    arcpy.Append_management(PARCEL_VISION, VISION_PARCEL_SDE, "NO_TEST", 'PRC_PID "PRC_PID" true false false 4 Long 0 10 ,First,#,'+PARCEL_VISION+',PRC_PID,-1,-1;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0 ,First,#,'+PARCEL_VISION+',PRC_PF_10,-1,-1;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0 ,First,#,'+PARCEL_VISION+',PRC_PF_10_DESC,-1,-1;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0 ,First,#,'+PARCEL_VISION+',PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0 ,First,#,'+PARCEL_VISION+',PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38 ,First,#,'+PARCEL_VISION+',PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38 ,First,#,'+PARCEL_VISION+',PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38 ,First,#,'+PARCEL_VISION+',PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38 ,First,#,'+PARCEL_VISION+',PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38 ,First,#,'+PARCEL_VISION+',PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10 ,First,#,'+PARCEL_VISION+',PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0 ,First,#,'+PARCEL_VISION+',PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0 ,First,#,'+PARCEL_VISION+',PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38 ,First,#,'+PARCEL_VISION+',PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38 ,First,#,'+PARCEL_VISION+',PRC_TTL_ASSESS,-1,-1', "")
    print ("     PARCEL table appended at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("     PARCEL table appended at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    arcpy.Append_management(REALOWNERSHIP_VISION, VISION_REAL_OWNERSHIP_SDE, "NO_TEST", 'ROW_PID "ROW_PID" true false false 4 Long 0 10 ,First,#,'+REALOWNERSHIP_VISION+',ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true false false 4 Long 0 10 ,First,#,'+REALOWNERSHIP_VISION+',ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true false false 4 Long 0 10 ,First,#,'+REALOWNERSHIP_VISION+',ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,'+REALOWNERSHIP_VISION+',ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5 ,First,#,'+REALOWNERSHIP_VISION+',ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0 ,First,#,'+REALOWNERSHIP_VISION+',ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true false false 4 Long 0 10 ,First,#,'+REALOWNERSHIP_VISION+',ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5 ,First,#,'+REALOWNERSHIP_VISION+',ROW_MAD_ISPRIMARY,-1,-1; "OWN_LINE" true true false 255 Text 0 0 ,First,#', "")
    print ("     REALOWNERSHIP table appended at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("     REALOWNERSHIP table appended at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    # In the append,for the REALMAST table, the field match, except PID_TEXT, it's connected to REM_PID.  Also, it's filtered out to active parcels only.
    arcpy.management.Append(REALMAST_VISION, VISION_REALMAST_SDE, "NO_TEST", r'REM_MNC "REM_MNC" true false false 4 Long 0 10,First,#,'+REALMAST_VISION+',REM_MNC,-1,-1;REM_PID "PID Number" true false false 4 Long 0 10,First,#,'+REALMAST_VISION+',REM_PID,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0,First,#,'+REALMAST_VISION+',REM_PIN,0,35;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0,First,#,'+REALMAST_VISION+',REM_OWN_NAME,0,85;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN,0,50;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_CITY,0,18;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_STT,0,2;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_ZIP,0,12;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0,First,#,'+REALMAST_VISION+',REM_ALT_PRCL_ID,0,35;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_MAP,0,7;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_MAP_CUT,0,3;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_BLOCK,0,7;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_BLOCK_CUT,0,3;REM_MBLU_LOT "Lot" true true false 7 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_LOT,0,7;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_LOT_CUT,0,3;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_UNIT,0,7;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_UNIT_CUT,0,3;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0,First,#,'+REALMAST_VISION+',REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10,First,#,'+REALMAST_VISION+',REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5,First,#,'+REALMAST_VISION+',REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0,First,#,'+REALMAST_VISION+',REM_CMPLX_NAME,0,40;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0,First,#,'+REALMAST_VISION+',REM_BLDG_NAME,0,60;REM_USE_CODE "Use Code" true true false 4 Text 0 0,First,#,'+REALMAST_VISION+',REM_USE_CODE,0,6;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38,First,#,'+REALMAST_VISION+',REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0,First,#,'+REALMAST_VISION+',REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0,First,#,'+REALMAST_VISION+',REM_USRFLD,0,6;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0,First,#,'+REALMAST_VISION+',REM_USRFLD_DESC,0,40;PID_TEXT "PID Text format" true true false 15 Text 0 0,First,#,'+REALMAST_VISION+',REM_PID,-1,-1;REM_PARCEL_STATUS "Parcel Status in CAMA" true true false 1 Text 0 0,First,#,'+REALMAST_VISION+',REM_PARCEL_STATUS,0,1', '', "REM_PARCEL_STATUS = 'A'")
    print ("     REALMAST table appended at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("     REALMAST table appended at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    arcpy.Append_management(SALESHISTORY_VISION, VISION_SALES_HISTORY_SDE, "NO_TEST", 'SLH_PID "SLH_PID" true false false 4 Long 0 0 ,First,#,'+SALESHISTORY_VISION+',SLH_PID,-1,-1;SLH_LINE_NUM "SLH_LINE_NUM" true false false 4 Long 0 0 ,First,#,'+SALESHISTORY_VISION+',SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "SLH_SALE_DATE" true true false 8 Date 0 0 ,First,#,'+SALESHISTORY_VISION+',SLH_SALE_DATE,-1,-1;SLH_BOOK "SLH_BOOK" true true false 15 Text 0 0 ,First,#,'+SALESHISTORY_VISION+',SLH_BOOK,-1,-1;SLH_PAGE "SLH_PAGE" true true false 15 Text 0 0 ,First,#,'+SALESHISTORY_VISION+',SLH_PAGE,-1,-1;SLH_PRICE "SLH_PRICE" true true false 8 Double 0 0 ,First,#,'+SALESHISTORY_VISION+',SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "SLH_CURRENT_OWNER" true true false 2 Short 0 0 ,First,#,'+SALESHISTORY_VISION+',SLH_CURRENT_OWNER,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#;SLH_PID_JOIN "SLH_PID_JOIN" true true false 4 Long 0 0 ,First,#,'+SALESHISTORY_VISION+',SLH_PID,-1,-1', "")
    print ("     SALESHISTORY table appended at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("     SALESHISTORY table appended at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to append data from VISION tables to SDE tables")
    write_log("\n Unable to append data from VISION tables to SDE tables", logfile)
    logging.exception('Got exception on append data from VISION tables to SDE tables logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # delete VIS_EXEMPTS_TBL_View to free up memory and space
    arcpy.Delete_management(VIS_EXEMPTS_TBL_View)
except:
    print ("\n Unable to delete VIS_EXEMPTS_TBL_View")
    write_log("\n Unable to delete VIS_EXEMPTS_TBL_View", logfile)
    logging.exception('Got exception on delete VIS_EXEMPTS_TBL_View logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

# Convert district numbers to Municipal names in LAND_VISION table
Land_District = ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69"]
Muni_Name = ["ATHENS TWP", "BEAVER TWP", "BLOOMFIELD TWP", "BLOOMING VALLEY BORO", "CAMBRIDGE TWP", "CAMBRIDGE SPRINGS BORO", "CENTERVILLE BORO", "COCHRANTON BORO", "CONNEAUT TWP", "CONNEAUTVILLE BORO", "CONNEAUT LAKE BORO", "CUSSEWAGO TWP", "FAIRFIELD TWP", "EAST FAIRFIELD TWP", "EAST FALLOWFIELD TWP", "WEST FALLOWFIELD TWP", "GREENWOOD TWP", "HAYFIELD TWP", "HYDETOWN BORO", "LINESVILLE BORO", "EAST MEAD TWP", "WEST MEAD TWP", "MEADVILLE CITY", "MEADVILLE CITY", "MEADVILLE CITY", "MEADVILLE CITY", "MEADVILLE CITY", "OIL CREEK TWP", "PINE TWP", "RANDOLPH TWP", "RICHMOND TWP", "ROCKDALE TWP", "ROME TWP", "SADSBURY TWP", "SAEGERTOWN BORO", "NORTH SHENANGO TWP", "SOUTH SHENANGO TWP", "WEST SHENANGO TWP", "SPARTA TWP", "SPARTANSBURG BORO", "SPRING TWP", "SPRINGBORO BORO", "STEUBEN TWP", "SUMMERHILL TWP", "SUMMIT TWP", "TITUSVILLE CITY", "TITUSVILLE CITY", "TITUSVILLE CITY", "TITUSVILLE CITY", "TOWNVILLE BORO", "TROY TWP", "UNION TWP", "VENANGO TWP", "VENANGO BORO", "VERNON TWP", "WAYNE TWP", "WOODCOCK TWP", "WOODCOCK BORO", "TITUSVILLE CITY"]
    
try:    
    with arcpy.da.UpdateCursor(VISION_LAND_SDE, 'MUNI_NAME') as cursor:
        for row in cursor:
            if row[0] in Land_District:
                row[0] = Muni_Name[Land_District.index(row[0])]
                cursor.updateRow(row)
            else:
                pass
        del row 
        del cursor
        print ("    Land Districts converted to Municipal names at " + time.strftime("%I:%M:%S %p", time.localtime()))
        write_log("    Land Districts converted to Municipal names at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to convert land district codes to municipal names in LAND_VISION table")
    write_log("Unable to convert land district codes to municipal names in LAND_VISION table", logfile)
    logging.exception('Got exception on convert land district codes to municipal names in LAND_VISION table logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    pass
    sys.exit ()

# Convert building permit codes to descriptions in BLDGPERM table
BuildingPmtCode = ["", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "62", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "84", "86", "87", "83", "85", "88", "61", "AD", "CM", "NC", "RS","89", "90", "92", "93","94","95","96","97"]
BuildingPmtDesc = ["UNSPECIFIED", "UNSPECIFIED", "REVIEW REQUESTED", "ADDITION", "ADDITION TO BUSINESS", "ADDITION TO GARAGE", "ADDITION TO HOSPITAL", "ADDITION TO PORCH", "AGRICULTURAL BUILDING", "BANK", "BARN", "COMMERCIAL BASEMENT", "BASEMENT DWELLING", "RESIDENTIAL BASEMENT", "CARPORT", "CELL TOWER", "CHURCH", "DECK", "DEMOLISH - OTHER", "DEMOLISH MULTI-RESIDENTIAL STRUCTURE", "DEMOLISH SINGLE FAMILY DWELLING", "DWELLING & GARAGE", "DWELLING", "DOUBLEWIDE MOBILE HOME", "ENCLOSED PORCH", "ENTRY WAY", "FENCE", "GARAGE", "GARAGE & BREEZEWAY", "COMMERCIAL GARAGE", "GAZEBO", "GREENHOUSE", "HANDICAPPED ACCESSABLE RAMP", "HOSPITAL", "INDUSTRIAL BUILDING", "LEAN TO", "MOBILE HOME", "MOBILE HOME STORAGE", "MODULAR DWELLING", "MULTI-RESIDENTIAL STRUCTURE", "OFFICE", "PARKING LOT/PARKING GARAGE", "PATIO", "PAVILION", "PAVING", "PICNIC SHELTER", "POLE BUILDING", "ABOVE GROUND POOL", "INGROUND POOL", "PORCH", "PUBLIC WORKS", "REMOVE DUE TO FIRE DAMAGE", "REPAIR DWELLING", "REPAIR OUTBUILDING", "ROOF", "SCHOOL", "ADDITION TO SCHOOL", "SERVICE STATION", "SHED", "ADDITION TO STORAGE BUILDING", "REPAIR BUSINESS", "REPAIR GARAGE", "SEASONAL STRUCTURE", "WORK SHOP", "CONCRETE PAD", "CARPORT", "ADDITION TO AGRICULTURAL BUILDING", "STORE", "WAREHOUSE", "COMMERCIAL ADDITION", "NON-ASSESSIBLE STRUCTURE", "REMODEL COMMERICAL STRUCTURE", "REMODEL RESIDENTIAL STRUCTURE", "STORAGE BUILDING", "KILN", "IMPROVEMENTS", "CLUB", "SAWMILL", "COVERALL", "CABIN/COTTAGE", "SIGN", "DRIVEWAY", "STAIRWAY", "CARWASH", "ZONING PERMIT", "911 NOTIFICATION", "PICTOMETRY CHECK", "CONSTRUCTION WITH NO PERMIT", "MISCELLANEOUS", "ADDITION", "COMMERCIAL", "NEW CONSTRUCTION", "RESIDENTIAL","SOLAR FARM","REPORTED STORM DAMAGE","ALTERATIONS","LIMITED SCOPE OPINION","CONTINUED REVIEW","MOBILE HOME REMOVAL","MOBILE HOME PARK","MOBILE HOME ADDED"]
    
try:    
    with arcpy.da.UpdateCursor(VISION_BLDGPERM_SDE, 'BPE_DESC') as cursor:
        for row in cursor:
            if row[0] in BuildingPmtCode:
                row[0] = BuildingPmtDesc[BuildingPmtCode.index(row[0])]
                cursor.updateRow(row)
            elif row[0] is None:
                row[0] = "UNSPECIFIED"
                cursor.updateRow(row)
            else:
                pass
        del row 
        del cursor
        print ("    Building Permit codes converted to descriptions at " + time.strftime("%I:%M:%S %p", time.localtime()))
        write_log("    Building Permit codes converted to descriptions at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Convert building permit codes to descriptions in BLDGPERM table")
    write_log("Unable to Convert building permit codes to descriptions in BLDGPERM table", logfile)
    logging.exception('Got exception on Convert building permit codes to descriptions in BLDGPERM table logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    pass
    sys.exit ()

try:
    print ("\n      Calculating PERMIT_LINK field in BLDGPERM_TBL_VISION at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n      Calculating PERMIT_LINK field in BLDGPERM_TBL_VISION at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    # Calculate PERMIT_LINK field in BLDGPERM_TBL_VISION, used to join to building permit feature class later in program.
    arcpy.CalculateField_management(VISION_BLDGPERM_SDE, "PERMIT_LINK", '"{}-{}".format(!BPE_PID! , !BPE_PERMIT_ID!)', "PYTHON_9.3", "")
except:
    print ("\n Unable to Calculate PERMIT_LINK field in BLDGPERM_TBL_VISION")
    write_log("\n Unable to Calculate PERMIT_LINK field in BLDGPERM_TBL_VISION", logfile)
    logging.exception('Got exception on Calculate PERMIT_LINK field in BLDGPERM_TBL_VISION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Remove spaces (before and after values) in all fields of REALMAST table (as they cause errors in processing)
    print ("       Removing spaces from fields in REALMAST Table at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("       Removing spaces from fields in REALMAST Table at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
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
    logging.exception('Got exception on remove spaces from fields in REALMAST Table logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()     

try:
    # Remove leading zeros from sales history book and page fields (as they will cause the URL fields to fail)
    print ("        Removing leading zeros from fields in SALES_HISTORY Table Book and Page fields at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("        Removing leading zeros from fields in SALES_HISTORY Table Book and Page fields at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
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
    logging.exception('Got exception on remove leading zeros from fields in SALES_HISTORY Table Book and Page fields logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()  

print ("         Updating ESRI/Vision temp tables from VISION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("         Updating ESRI/Vision temp tables from VISION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Calculating OWN_LINE fields in VISION_REAL_OWNERSHIP_SDE and VISION_SALES_HISTORY_SDE tables")
write_log("\n Calculating OWN_LINE fields in VISION_REAL_OWNERSHIP_SDE and VISION_SALES_HISTORY_SDE tables", logfile)

try:
    # Calculate OWN_LINE fields in VISION_REAL_OWNERSHIP_SDE and VISION_SALES_HISTORY_SDE tables, used to link tables together in OWNER table later in program.
    arcpy.CalculateField_management(VISION_REAL_OWNERSHIP_SDE, "OWN_LINE", '"{}-{}".format( !ROW_PID! ,!ROW_LINE_NUM!)', "PYTHON_9.3", "")
    arcpy.CalculateField_management(VISION_SALES_HISTORY_SDE, "OWN_LINE", '"{}-{}".format( !SLH_PID! , !SLH_LINE_NUM!)', "PYTHON_9.3", "")
except:
    print ("\n Unable to append data from VISION tables to SDE tables")
    write_log("\n Unable to append data from VISION tables to SDE tables", logfile)
    logging.exception('Got exception on append data from VISION tables to SDE tables logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()    

print ("       Calculating OWN_LINE fields in VISION_REAL_OWNERSHIP_SDE and VISION_SALES_HISTORY_SDE tables completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Calculating OWN_LINE fields in VISION_REAL_OWNERSHIP_SDE and VISION_SALES_HISTORY_SDE tables completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Create VISION_OWNER_TBL from VIS_OWNER_TBL and join VIS_MAILADDRESS, VIS_REAL_OWNERSHIP, and VIS_SALES_HISTORY tables")
write_log("\n Create VISION_OWNER_TBL from VIS_OWNER_TBL and join VIS_MAILADDRESS, VIS_REAL_OWNERSHIP, and VIS_SALES_HISTORY tables", logfile)

try:
    # Create VISION_OWNER_TBL_SDE from VIS_OWNER_TBL (creates owner table, so that additional vision tables can be joined to it)
    arcpy.TableToTable_conversion(VISION_OWNER_SDE, AUTOWORKSPACE, "VISION_OWNER_TBL", "", 'OWN_ID "OWN_ID" true false false 4 Long 0 0 ,First,#,'+VISION_OWNER_SDE+',OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,'+VISION_OWNER_SDE+',OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,'+VISION_OWNER_SDE+',OWN_NAME2,-1,-1', "")
    print ("  VISION_OWNER_TBL created...")
    write_log("  VISION_OWNER_TBL created",logfile)
except:
    print ("\n Unable to Create VISION_OWNER_TBL from VIS_OWNER_TBL")
    write_log("\n Unable to Create VISION_OWNER_TBL from VIS_OWNER_TBL", logfile)
    logging.exception('Got exception on Create VISION_OWNER_TBL from VIS_OWNER_TBL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()
    
try:
    # Join OWNER table to MAILADDRESS, REALOWNERSHIP, and SALES_HISTORY tables
    arcpy.JoinField_management(VISION_OWNER_TBL_SDE, "OWN_ID", VISION_REAL_OWNERSHIP_SDE, "ROW_OWN_ID", "ROW_PID;ROW_OWN_ID;ROW_LINE_NUM;ROW_OWN_PCT;ROW_PRIMARY;ROW_CREATE_DATE;ROW_MAD_ID;ROW_MAD_ISPRIMARY;OWN_LINE")
    print ("   VISION_OWNER_TBL joined to VIS_REAL_OWNERSHIP_TBL at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("   VISION_OWNER_TBL joined to VIS_REAL_OWNERSHIP_TBL at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    arcpy.JoinField_management(VISION_OWNER_TBL_SDE, "ROW_MAD_ID", VISION_MAILADDRESS_SDE, "MAD_ID", "MAD_MAIL_NAME1;MAD_MAIL_NAME2;MAD_MAIL_ADDR1;MAD_MAIL_CITY;MAD_MAIL_STATE;MAD_MAIL_ZIP;MAD_MAIL_ADDR2;MAD_ID")
    print ("    VISION_OWNER_TBL joined to VIS_MAILADDRESS_TBL at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("    VISION_OWNER_TBL joined to VIS_MAILADDRESS_TBL at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    arcpy.JoinField_management(VISION_OWNER_TBL_SDE, "OWN_LINE", VISION_SALES_HISTORY_SDE, "OWN_LINE", "SLH_PID;SLH_LINE_NUM;SLH_SALE_DATE;SLH_BOOK;SLH_PAGE;SLH_PRICE;SLH_CURRENT_OWNER")
    print ("     VISION_OWNER_TBL joined to VIS_SALES_HISTORY_TBL at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("     VISION_OWNER_TBL joined to VIS_SALES_HISTORY_TBL at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to join VISION_OWNER_TBL view to MAILADDRESS, REALOWNERSHIP, and SALES_HISTORY tables views")
    write_log("\n Unable to join VISION_OWNER_TBL view to MAILADDRESS, REALOWNERSHIP, and SALES_HISTORY tables views", logfile)
    logging.exception('Got exception on join VISION_OWNER_TBL view to MAILADDRESS, REALOWNERSHIP, and SALES_HISTORY tables views logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Calculate SLH_PID field from ROW_PID field
    arcpy.CalculateField_management(VISION_OWNER_TBL_SDE, "SLH_PID", "!ROW_PID!", "PYTHON", "")
    print ("       Calculated SLH_PID field from ROW_PID field at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("       Calculated SLH_PID field from ROW_PID field at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Calculate SLH_PID field from ROW_PID field")
    write_log("\n Calculate SLH_PID field from ROW_PID field", logfile)
    logging.exception('Got exception on Calculate SLH_PID field from ROW_PID field logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Create VISION_OWNER_TBL_WEBTemp from VISION_OWNER_TBL_SDE and join in INET_SUPPRESS field from VIS_REALMAST_TBL (creates a web-friendly version of sales history based on internet supression field to filter out protected records)
    VISION_OWNER_TBL_WEBTemp = arcpy.MakeTableView_management(VISION_OWNER_TBL_SDE, "VISION_OWNER_TBL_WEBTemp", "", "", "OBJECTID OBJECTID VISIBLE NONE;OWN_ID OWN_ID VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;ROW_PID ROW_PID VISIBLE NONE;ROW_OWN_ID ROW_OWN_ID VISIBLE NONE;ROW_LINE_NUM ROW_LINE_NUM VISIBLE NONE;ROW_OWN_PCT ROW_OWN_PCT VISIBLE NONE;ROW_PRIMARY ROW_PRIMARY VISIBLE NONE;ROW_CREATE_DATE ROW_CREATE_DATE VISIBLE NONE;ROW_MAD_ID ROW_MAD_ID VISIBLE NONE;ROW_MAD_ISPRIMARY ROW_MAD_ISPRIMARY VISIBLE NONE;OWN_LINE OWN_LINE VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;MAD_MAIL_ADDR2 MAD_MAIL_ADDR2 VISIBLE NONE;MAD_ID MAD_ID VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_INET_SUPPRESS_1 REM_INET_SUPPRESS_1 VISIBLE NONE")
    arcpy.JoinField_management(VISION_OWNER_TBL_WEBTemp, "ROW_PID", VISION_REALMAST_SDE, "REM_PID", "REM_INET_SUPPRESS")
    arcpy.TableToTable_conversion(VISION_OWNER_TBL_WEBTemp, AUTOWORKSPACE, "VISION_OWNER_TBL_WEBTemp", "REM_INET_SUPPRESS IS NULL OR REM_INET_SUPPRESS = 0", 'OWN_ID "OWN_ID" true false false 4 Long 0 10 ,First,#,'+VISION_OWNER_TBL_SDE +',OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',OWN_NAME2,-1,-1;ROW_PID "ROW_PID" true true false 4 Long 0 10 ,First,#,'+VISION_OWNER_TBL_SDE +',ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10 ,First,#,'+VISION_OWNER_TBL_SDE +',ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10 ,First,#,'+VISION_OWNER_TBL_SDE +',ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,'+VISION_OWNER_TBL_SDE +',ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5 ,First,#,'+VISION_OWNER_TBL_SDE +',ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10 ,First,#,'+VISION_OWNER_TBL_SDE +',ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5 ,First,#,'+VISION_OWNER_TBL_SDE +',ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',OWN_LINE,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',MAD_MAIL_ADDR2,-1,-1;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10 ,First,#,'+VISION_OWNER_TBL_SDE +',MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10 ,First,#,'+VISION_OWNER_TBL_SDE +',SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10 ,First,#,'+VISION_OWNER_TBL_SDE +',SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',SLH_BOOK,-1,-1;SLH_PAGE "Deed Page" true true false 15 Text 0 0 ,First,#,'+VISION_OWNER_TBL_SDE +',SLH_PAGE,-1,-1;SLH_PRICE "Sale Price" true true false 8 Double 8 38 ,First,#,'+VISION_OWNER_TBL_SDE +',SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5 ,First,#,'+VISION_OWNER_TBL_SDE +',SLH_CURRENT_OWNER,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,'+VISION_OWNER_TBL_SDE +',REM_INET_SUPPRESS,-1,-1',"")
    print ("      VISION_OWNER_TBL_WEBTemp created from filtered version of VISION_OWNER_TBL...")
    write_log("      VISION_OWNER_TBL_WEBTemp created from filtered version of VISION_OWNER_TBL...",logfile)
except:
    print ("\n Unable to Create VISION_OWNER_TBL_WEBTemp from VISION_OWNER_TBL_SDE and join in INET_SUPPRESS field from VIS_REALMAST_TBL (filtering out REM_INET_SUPPRESS IS NULL OR REM_INET_SUPPRESS = 0)")
    write_log("\n Unable to Create VISION_OWNER_TBL_WEBTemp from VISION_OWNER_TBL_SDE and join in INET_SUPPRESS field from VIS_REALMAST_TBL (filtering out REM_INET_SUPPRESS IS NULL OR REM_INET_SUPPRESS = 0)", logfile)
    logging.exception('Got exception on Create VISION_OWNER_TBL_WEBTemp from VISION_OWNER_TBL_SDE and join in INET_SUPPRESS field from VIS_REALMAST_TBL (filtering out REM_INET_SUPPRESS IS NULL OR REM_INET_SUPPRESS = 0) logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Create VISION_OWNER_TBL from VIS_OWNER_TBL and join VIS_MAILADDRESS, VIS_REAL_OWNERSHIP, and VIS_SALES_HISTORY tables completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Create VISION_OWNER_TBL from VIS_OWNER_TBL and join VIS_MAILADDRESS, VIS_REAL_OWNERSHIP, and VIS_SALES_HISTORY tables completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Create VISION_OTHER_TBL and join LAND and PARCEL tables to it")
write_log("\n Create VISION_OTHER_TBL and join LAND and PARCEL tables to it", logfile)

try:
    # Create VISION_OTHER_TBL_SDE from VISION_REALMAST_SDE (creates other table, so that additional vision tables can be joined to it)
    arcpy.TableToTable_conversion(VISION_REALMAST_SDE, AUTOWORKSPACE, "VISION_OTHER_TBL", "", 'REM_MNC "REM_MNC" true false false 4 Long 0 10 ,First,#,'+VISION_REALMAST_SDE +',REM_MNC,-1,-1;REM_PID "PID Number" true false false 4 Long 0 10 ,First,#,'+VISION_REALMAST_SDE +',REM_PID,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_PIN,-1,-1;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "Lot" true true false 7 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,'+VISION_REALMAST_SDE +',REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5 ,First,#,'+VISION_REALMAST_SDE +',REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_BLDG_NAME,-1,-1;REM_USE_CODE "Use Code" true true false 4 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_USE_CODE,-1,-1;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38 ,First,#,'+VISION_REALMAST_SDE +',REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_USRFLD,-1,-1;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_USRFLD_DESC,-1,-1;PID_TEXT "PID Text format" true true false 15 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',PID_TEXT,-1,-1;REM_PARCEL_STATUS "Parcel Status in CAMA" true true false 1 Text 0 0 ,First,#,'+VISION_REALMAST_SDE +',REM_PARCEL_STATUS,-1,-1', "")
    print ("  VISION_OTHER_TBL created at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("  VISION_OTHER_TBL created at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Create VISION_OWNER_TBL from VIS_OWNER_TBL")
    write_log("\n Unable to Create VISION_OWNER_TBL from VIS_OWNER_TBL", logfile)
    logging.exception('Got exception on Create VISION_OWNER_TBL from VIS_OWNER_TBL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Make table view of VIS_LAND_TBL selecting out LND_LINE = 1 only (filters out duplicate land records keeps only current owner)
    VIS_LAND_TBL_View = arcpy.MakeTableView_management(VISION_LAND_SDE, "VIS_LAND_TBL_View", "LND_LINE_ID = 1", "", "OBJECTID OBJECTID VISIBLE NONE;LND_PID LND_PID VISIBLE NONE;LND_LINE_ID LND_LINE_ID VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;MUNI_NAME MUNI_NAME VISIBLE NONE")
except:
    print ("\n Unable to Make table view of VIS_LAND_TBL selecting out LND_LINE = 1 only")
    write_log("\n Unable to Make table view of VIS_LAND_TBL selecting out LND_LINE = 1 only", logfile)
    logging.exception('Got exception on Make table view of VIS_LAND_TBL selecting out LND_LINE = 1 only logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Join OTHER table view to LAND and PARCEL tables
    arcpy.JoinField_management(VISION_OTHER_TBL_SDE, "REM_PID", VIS_LAND_TBL_View, "LND_PID", "LND_USE_CODE;LND_USE_DESC;LND_DSTRCT;MUNI_NAME")
    print ("   VIS_LAND_TBL_View joined to VISION_OTHER_TBL at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("   VIS_LAND_TBL_View joined to VISION_OTHER_TBL at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    arcpy.JoinField_management(VISION_OTHER_TBL_SDE, "REM_PID", VISION_PARCEL_SDE, "PRC_PID", "PRC_PF_LOCN;PRC_PF_LOCN_DESC;PRC_USRFLD_09;PRC_USRFLD_10;PRC_TTL_ASSESS_BLDG;PRC_TTL_ASSESS_IMPROVEMENTS;PRC_TTL_ASSESS_LND;PRC_TTL_ASSESS_OB;PRC_VALUE;PRC_CMPLX_PID;PRC_CMPLX_DESC;PRC_CENSUS;PRC_TTL_MRKT_ASSESS;PRC_TTL_ASSESS")
    print ("    VIS_PARCEL_TBL joined to VISION_OTHER_TBL at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("    VIS_PARCEL_TBL joined to VISION_OTHER_TBL at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Join VISION_OTHER_TBL to LAND table view and PARCEL table")
    write_log("\n Unable to Join VISION_OTHER_TBL to LAND table view and PARCEL table", logfile)
    logging.exception('Got exception on Join VISION_OTHER_TBL to LAND table view and PARCEL table logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # delete VIS_LAND_TBL_View to free up memory and space
    arcpy.Delete_management(VIS_LAND_TBL_View)
except:
    print ("\n Unable to delete VIS_LAND_TBL_View")
    write_log("\n Unable to delete VIS_LAND_TBL_View", logfile)
    logging.exception('Got exception on delete VIS_LAND_TBL_View logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Calculate Real Estate ID # in VISION_OTHER_TBL table
    arcpy.CalculateField_management(VISION_OTHER_TBL_SDE, "REM_USRFLD", "!REM_PID!", "PYTHON", "")
    arcpy.CalculateField_management(VISION_OTHER_TBL_SDE, "REM_USRFLD", "!REM_USRFLD!.zfill(6)", "PYTHON", "")
    arcpy.CalculateField_management(VISION_OTHER_TBL_SDE, "REM_USRFLD_DESC", '"{}-0-{}".format(!LND_DSTRCT!, !REM_USRFLD!)', "PYTHON", "")
    print ("  Real Estate ID #s calculated in VISION_OTHER_TBL")
    write_log("  Real Estate ID #s calculated in VISION_OTHER_TBL",logfile)
except:
    print ("\n Unable to calculate Real Estate ID #s in VISION_OTHER_TBL")
    write_log("\n Unable to calculate Real Estate ID #s in VISION_OTHER_TBL", logfile)
    logging.exception('Got exception on calculate Real Estate ID #s in VISION_OTHER_TBL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()    
    
print ("       Create VISION_OTHER_TBL and join LAND and PARCEL tables to it completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Create VISION_OTHER_TBL and join LAND and PARCEL tables to it completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Creating temporary table (VISIDATA_TEMP) from VISION_OTHER_TBL_SDE & VISION_OWNER_TBL_SDE tables")
write_log("\n Creating temporary table (VISIDATA_TEMP) from VISION_OTHER_TBL_SDE & VISION_OWNER_TBL_SDE tables: " +time.strftime("%I:%M:%S %p", time.localtime()), logfile)

try:
    # Create VISIDATA_TEMP table from VISION_OTHER_TBL (VISIDATA temp will become OTHER table and OWNER table joined, will be used for multiple join tools in program below)
    VISIDATA_TEMP = arcpy.conversion.TableToTable(VISION_OTHER_TBL_SDE, AUTOWORKSPACE, "VISIDATA_TEMP", '', r'REM_MNC "REM_MNC" true false false 4 Long 0 10,First,#,'+VISION_OTHER_TBL_SDE +',REM_MNC,-1,-1;REM_PID "PID Number" true false false 4 Long 0 10,First,#,'+VISION_OTHER_TBL_SDE +',REM_PID,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_PIN,0,35;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_OWN_NAME,0,85;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_PRCL_LOCN,0,50;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_PRCL_LOCN_CITY,0,18;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_PRCL_LOCN_STT,0,2;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_PRCL_LOCN_ZIP,0,12;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_ALT_PRCL_ID,0,35;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_MBLU_MAP,0,7;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_MBLU_MAP_CUT,0,3;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_MBLU_BLOCK,0,7;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_MBLU_BLOCK_CUT,0,3;REM_MBLU_LOT "Lot" true true false 7 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_MBLU_LOT,0,7;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_MBLU_LOT_CUT,0,3;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_MBLU_UNIT,0,7;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_MBLU_UNIT_CUT,0,3;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10,First,#,'+VISION_OTHER_TBL_SDE +',REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5,First,#,'+VISION_OTHER_TBL_SDE +',REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_CMPLX_NAME,0,30;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_BLDG_NAME,0,60;REM_USE_CODE "Use Code" true true false 4 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_USE_CODE,0,4;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38,First,#,'+VISION_OTHER_TBL_SDE +',REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_USRFLD,0,6;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_USRFLD_DESC,0,40;PID_TEXT "PID Text format" true true false 15 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',PID_TEXT,0,15;REM_PARCEL_STATUS "Parcel Status in CAMA" true true false 1 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',REM_PARCEL_STATUS,0,1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',LND_USE_CODE,0,4;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',LND_USE_DESC,0,40;LND_DSTRCT "District Number" true true false 6 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',LND_DSTRCT,0,6;MUNI_NAME "Municipality Name" true true false 75 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',MUNI_NAME,0,75;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',PRC_PF_LOCN,0,15;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',PRC_PF_LOCN_DESC,0,50;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',PRC_USRFLD_09,0,30;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',PRC_USRFLD_10,0,30;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38,First,#,'+VISION_OTHER_TBL_SDE +',PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38,First,#,'+VISION_OTHER_TBL_SDE +',PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38,First,#,'+VISION_OTHER_TBL_SDE +',PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38,First,#,'+VISION_OTHER_TBL_SDE +',PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38,First,#,'+VISION_OTHER_TBL_SDE +',PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10,First,#,'+VISION_OTHER_TBL_SDE +',PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',PRC_CMPLX_DESC,0,30;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0,First,#,'+VISION_OTHER_TBL_SDE +',PRC_CENSUS,0,20;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38,First,#,'+VISION_OTHER_TBL_SDE +',PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38,First,#,'+VISION_OTHER_TBL_SDE +',PRC_TTL_ASSESS,-1,-1', '')
except:
    print ("\n Unable to create VISIDATA_TEMP table from VISION_OTHER_TBL")
    write_log("\n Unable to create VISIDATA_TEMP table from VISION_OTHER_TBL", logfile)
    logging.exception('Got exception on create VISIDATA_TEMP table from VISION_OTHER_TBL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Create CURRENT_OWNER_TBL_CO_Temp from  VISION_OWNER_TBL_SDE - filtering out current owner records (only for use in parcels, entire table is not altered as it becomes sales history table for relationship class)
    CURRENT_OWNER_TBL_CO_Temp = arcpy.conversion.TableToTable(VISION_OWNER_TBL_SDE, AUTOWORKSPACE, "CURRENT_OWNER_TBL_CO_Temp", "SLH_CURRENT_OWNER = 1 And ROW_PRIMARY = 1", r'OWN_ID "OWN_ID" true false false 4 Long 0 10,First,#,'+VISION_OWNER_TBL_SDE+',OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',OWN_NAME1,0,85;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',OWN_NAME2,0,85;ROW_PID "ROW_PID" true true false 4 Long 0 10,First,#,'+VISION_OWNER_TBL_SDE+',ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10,First,#,'+VISION_OWNER_TBL_SDE+',ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10,First,#,'+VISION_OWNER_TBL_SDE+',ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5,First,#,'+VISION_OWNER_TBL_SDE+',ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5,First,#,'+VISION_OWNER_TBL_SDE+',ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0,First,#,'+VISION_OWNER_TBL_SDE+',ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10,First,#,'+VISION_OWNER_TBL_SDE+',ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5,First,#,'+VISION_OWNER_TBL_SDE+',ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',OWN_LINE,0,255;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',MAD_MAIL_NAME1,0,85;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',MAD_MAIL_NAME2,0,85;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',MAD_MAIL_ADDR1,0,50;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',MAD_MAIL_CITY,0,30;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',MAD_MAIL_STATE,0,20;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',MAD_MAIL_ZIP,0,20;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',MAD_MAIL_ADDR2,0,50;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10,First,#,'+VISION_OWNER_TBL_SDE+',MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10,First,#,'+VISION_OWNER_TBL_SDE+',SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10,First,#,'+VISION_OWNER_TBL_SDE+',SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0,First,#,'+VISION_OWNER_TBL_SDE+',SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',SLH_BOOK,0,15;SLH_PAGE "Deed Page" true true false 15 Text 0 0,First,#,'+VISION_OWNER_TBL_SDE+',SLH_PAGE,0,15;SLH_PRICE "Sale Price" true true false 8 Double 8 38,First,#,'+VISION_OWNER_TBL_SDE+',SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5,First,#,'+VISION_OWNER_TBL_SDE+',SLH_CURRENT_OWNER,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10,First,#,'+VISION_OWNER_TBL_SDE+',REM_INET_SUPPRESS,-1,-1', '')
except:
    print ("\n Unable to create CURRENT_OWNER_TBL_CO_Temp from  VISION_OWNER_TBL_SDE - filtering out current records only")
    write_log("\n Unable to create CURRENT_OWNER_TBL_CO_Temp from  VISION_OWNER_TBL_SDE - filtering out current records only", logfile)
    logging.exception('Got exception on create create CURRENT_OWNER_TBL_CO_Temp from  VISION_OWNER_TBL_SDE - filtering out current records only logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Join CURRENT_OWNER_TBL_CO_Temp to VISIDATA_TEMP
    arcpy.management.JoinField(VISIDATA_TEMP, "REM_PID", CURRENT_OWNER_TBL_CO_Temp, "ROW_PID", "SLH_BOOK;SLH_PAGE;REM_INET_SUPPRESS;MAD_ID;OWN_ID;OWN_LINE;OWN_NAME1;OWN_NAME2;ROW_CREATE_DATE;ROW_LINE_NUM;ROW_MAD_ID;ROW_MAD_ISPRIMARY;ROW_OWN_ID;ROW_OWN_PCT;ROW_PID;ROW_PRIMARY;SLH_SALE_DATE;SLH_PRICE;SLH_CURRENT_OWNER;SLH_LINE_NUM;SLH_PID;MAD_MAIL_ADDR1;MAD_MAIL_ADDR2;MAD_MAIL_CITY;MAD_MAIL_NAME1;MAD_MAIL_NAME2;MAD_MAIL_STATE;MAD_MAIL_ZIP")
    print ("  CURRENT_OWNER_TBL_CO_Temp joined to VISIDATA_TEMP...")
    write_log("  CURRENT_OWNER_TBL_CO_Temp joined to VISIDATA_TEMP...", logfile)
except:
    print ("\n Unable to join CURRENT_OWNER_TBL_CO_Temp to VISIDATA_TEMP")
    write_log("\n Unable to join CURRENT_OWNER_TBL_CO_Temp to VISIDATA_TEMP", logfile)
    logging.exception('Got exception on join CURRENT_OWNER_TBL_CO_Temp to VISIDATA_TEMP logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Delete CURRENT_OWNER_TBL_CO_Temp from Autoworkspace
    arcpy.management.Delete(CURRENT_OWNER_TBL_CO_Temp, '')
    print ("  Deleting CURRENT_OWNER_TBL_CO_Temp from Autoworkspace...")
    write_log("  Deleting CURRENT_OWNER_TBL_CO_Temp from Autoworkspace...", logfile)
except:
    print ("\n Unable to delete CURRENT_OWNER_TBL_CO_Temp from Autoworkspace")
    write_log("\n Unable to delete CURRENT_OWNER_TBL_CO_Temp from Autoworkspace", logfile)
    logging.exception('Got exception on delete CURRENT_OWNER_TBL_CO_Temp from Autoworkspace logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Creating temporary table (VISIDATA_TEMP) from VISION_OTHER_TBL_SDE & VISION_OWNER_TBL_SDE tables completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Creating temporary table (VISIDATA_TEMP) from VISION_OTHER_TBL_SDE & VISION_OWNER_TBL_SDE tables completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("       Updating Assessment CAMA Records Table in PUBLIC_WEB from VISIDDATA_TEMP tables in AUTOWORKSPACE")
write_log("       Updating Assessment CAMA Records Table in PUBLIC_WEB from VISIDDATA_TEMP tables in AUTOWORKSPACE", logfile)

try:
    # Delete Rows in Assessment CAMA Records Table - PUBLIC_WEB
    arcpy.DeleteRows_management(CAMA_RECORDS_TBL)
    print ("  Deleting rows from Assessment CAMA Records Table - PUBLIC_WEB...")
    write_log("  Deleting rows from Assessment CAMA Records Table - PUBLIC_WEB...", logfile)
except:
    print ("\n Unable to Deleting rows from Assessment CAMA Records Table - PUBLIC_WEB")
    write_log("\n Unable to Deleting rows from Assessment CAMA Records Table - PUBLIC_WEB", logfile)
    logging.exception('Got exception on Deleting rows from Assessment CAMA Records Table - PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Rows in Assessment CAMA Records Table - PUBLIC Web from VISIDATA_TEMP - AUTOWORKSPACE 
    arcpy.Append_management(VISIDATA_TEMP, CAMA_RECORDS_TBL, "NO_TEST", 'REM_MNC "REM_MNC" true false false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_MNC,-1,-1;REM_PID "PID Number" true false false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_PID,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_PIN,-1,-1;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "Lot" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_BLDG_NAME,-1,-1;REM_USE_CODE "Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_USE_CODE,-1,-1;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_USRFLD,-1,-1;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_USRFLD_DESC,-1,-1;PID_TEXT "PID Text format" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PID_TEXT,-1,-1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,LND_USE_CODE,-1,-1;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,LND_DSTRCT,-1,-1;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_PF_LOCN,-1,-1;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_PF_LOCN_DESC,-1,-1;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,PRC_TTL_ASSESS,-1,-1;OWN_ID "OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,OWN_NAME2,-1,-1;ROW_PID "ROW_PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,OWN_LINE,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,MAD_MAIL_ADDR2,-1,-1;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,SLH_BOOK,-1,-1;SLH_PAGE "Deed Page" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,SLH_PAGE,-1,-1;SLH_PRICE "Sale Price" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,SLH_CURRENT_OWNER,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#;MUNI_NAME "MUNI_NAME" true true false 75 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,MUNI_NAME,-1,-1;REM_PARCEL_STATUS "Parcel Status in CAMA" true true false 1 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP,REM_PARCEL_STATUS,-1,-1', "")
    print ("  Appending rows from VISIDATA_TEMP - AUTOWORKSPACE to Assessment CAMA Records Table - PUBLIC_WEB...")
    write_log("  Appending rows from VISIDATA_TEMP - AUTOWORKSPACE to Assessment CAMA Records Table - PUBLIC_WEB...", logfile)
except:
    print ("\n Unable to Append rows from VISIDATA_TEMP - AUTOWORKSPACE to Assessment CAMA Records Table - PUBLIC_WEB")
    write_log("\n Unable to Append rows from VISIDATA_TEMP - AUTOWORKSPACE to Assessment CAMA Records Table - PUBLIC_WEB", logfile)
    logging.exception('Got exception on Appending rows from VISIDATA_TEMP - AUTOWORKSPACE to Assessment CAMA Records Table - PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Assessment CAMA Records Table in PUBLIC_WEB from VISIDDATA_TEMP tables in AUTOWORKSPACE completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Assessment CAMA Records Table in PUBLIC_WEB from VISIDDATA_TEMP tables in AUTOWORKSPACE completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Creating Building Permits Joined from BLDG_PRMT - AST & VISION tables")
write_log("\n Creating Building Permits Joined from BLDG_PRMT - AST & VISION tables", logfile)

print (" Joining BLDGPERM_VISION_VIEW with VISION_OTHER_TBL and VISION_OWNER_TBL...")
write_log(" Joining BLDGPERM_VISION_VIEW with VISION_OTHER_TBL and VISION_OWNER_TBL...", logfile)

try:
    # Delete rows from Building_Permits_Base - AUTOWORKSPACE\ASSESSMENT
    arcpy.DeleteRows_management(BLDG_PRMT_AST)
except:
    print ("\n Unable to delete rows from  Building_Permits_Base - AUTOWORKSPACE\ASSESSMENT")
    write_log("\n Unable to delete rows from  Building_Permits_Base - AUTOWORKSPACE\ASSESSMENT", logfile)
    logging.exception('Got exception on delete rows from  Building_Permits_Base - AUTOWORKSPACE\ASSESSMENT logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Create separate geocode table of active building permits by joining REALMAST field REM_PARCEL_STATUS to BLDG_PRMT_AST - AUTOWORKSPACE\ASSESSMENT, calling it VISION_BLDGPERM_SDE_GC
    VISION_BLDGPERM_SDE_GC = arcpy.conversion.TableToTable(VISION_BLDGPERM_SDE, AUTOWORKSPACE, "VISION_BLDGPERM_SDE_GC", '', r'BPE_PID "BPE_PID" true false false 4 Long 0 10,First,#,'+VISION_BLDGPERM_SDE+',BPE_PID,-1,-1;BPE_PERMIT_ID "BPE_PERMIT_ID" true true false 20 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_PERMIT_ID,0,20;BPE_FISCAL_YR "BPE_FISCAL_YR" true false false 2 Short 0 5,First,#,'+VISION_BLDGPERM_SDE+',BPE_FISCAL_YR,-1,-1;BPE_APP_DATE "BPE_APP_DATE" true true false 8 Date 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_APP_DATE,-1,-1;BPE_ISSUE_DATE "BPE_ISSUE_DATE" true true false 8 Date 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_ISSUE_DATE,-1,-1;BPE_INSPECT_DATE "BPE_INSPECT_DATE" true true false 8 Date 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_INSPECT_DATE,-1,-1;BPE_AMOUNT "BPE_AMOUNT" true true false 4 Long 0 10,First,#,'+VISION_BLDGPERM_SDE+',BPE_AMOUNT,-1,-1;BPE_FEE "BPE_FEE" true true false 4 Long 0 10,First,#,'+VISION_BLDGPERM_SDE+',BPE_FEE,-1,-1;BPE_APPLICANT "BPE_APPLICANT" true true false 50 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_APPLICANT,0,50;BPE_LICENCE "BPE_LICENCE" true true false 20 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_LICENCE,0,20;BPE_COMPANY "BPE_COMPANY" true true false 50 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_COMPANY,0,50;BPE_AREA "BPE_AREA" true true false 20 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_AREA,0,20;BPE_REF "BPE_REF" true true false 20 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_REF,0,20;BPE_DESC "BPE_DESC" true true false 40 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_DESC,0,40;BPE_PCT_COMPLETE "BPE_PCT_COMPLETE" true true false 4 Long 0 10,First,#,'+VISION_BLDGPERM_SDE+',BPE_PCT_COMPLETE,-1,-1;BPE_DATE_COMPLETE "BPE_DATE_COMPLETE" true true false 8 Date 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_DATE_COMPLETE,-1,-1;BPE_COMMENT "BPE_COMMENT" true true false 750 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_COMMENT,0,750;BPE_USRFLD_01 "BPE_USRFLD_01" true true false 100 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_USRFLD_01,0,100;BPE_USRFLD_02 "BPE_USRFLD_02" true true false 100 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_USRFLD_02,0,100;BPE_USRFLD_03 "BPE_USRFLD_03" true true false 100 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_USRFLD_03,0,100;BPE_USRFLD_04 "BPE_USRFLD_04" true true false 100 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_USRFLD_04,0,100;BPE_USRFLD_05 "BPE_USRFLD_05" true true false 100 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',BPE_USRFLD_05,0,100;PERMIT_LINK "PERMIT_LINK" true true false 100 Text 0 0,First,#,'+VISION_BLDGPERM_SDE+',PERMIT_LINK,0,100', '')
    arcpy.management.JoinField(VISION_BLDGPERM_SDE_GC, "BPE_PID", VISION_REALMAST_SDE, "REM_PID", "REM_PARCEL_STATUS")
except:
    print ("\n Unable to Create VISION_BLDGPERM_SDE_GC and join REM_PARCEL_STATUS field from VISION_BLDGPERM_SDE - AUTOWORKSPACE\ASSESSMENT")
    write_log("\n Unable to Create VISION_BLDGPERM_SDE_GC and join REM_PARCEL_STATUS field from VISION_BLDGPERM_SDE - AUTOWORKSPACE\ASSESSMENT", logfile)
    logging.exception('Got exception on Unable to Create VISION_BLDGPERM_SDE_GC and join REM_PARCEL_STATUS field from VISION_BLDGPERM_SDE - AUTOWORKSPACE\ASSESSMENT logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Create Building_Permit_Geocode "in_memory"
    Building_Permit_Geocode = arcpy.geocoding.GeocodeAddresses(VISION_BLDGPERM_SDE_GC, CC_PARCEL_LOC, "'Single Line Input' BPE_PID VISIBLE NONE", "in_memory/Building_Permit_Geocode", "STATIC", None, '', None, "ALL")
    print ("\n Creating Building_Permit_Geocode in_memory")
    write_log("\n Creating Building_Permit_Geocode in_memory",logfile)
except:
    print ("\n Unable to Create Building_Permit_Geocode in_memory")
    write_log("\n Unable to Create Building_Permit_Geocode in_memory", logfile)
    logging.exception('Got exception on Create Building_Permit_Geocode in_memory logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Building_Permit_Geocode "in_memory" into BLDGPERM_TBL_AUTOWKSP (selecting only REM_PARCEL_STATUS = A
    arcpy.management.Append(Building_Permit_Geocode, BLDG_PRMT_AST, "NO_TEST", r'REM_PID "PID" true true false 4 Long 0 10,First,#,in_memory/Building_Permit_Geocode,USER_BPE_PID,-1,-1;PERMIT_LINK "PID-PERMIT #" true true false 100 Text 0 0,First,#,in_memory/Building_Permit_Geocode,USER_PERMIT_LINK,0,100;EDITOR "EDITOR" true true false 255 Text 0 0,First,#;GEOCODE_STATUS "Status of Geocode" true true false 50 Text 0 0,First,#,in_memory/Building_Permit_Geocode,Status,0,1;REM_PARCEL_STATUS "Status in CAMA" true true false 1 Text 0 0,First,#,in_memory/Building_Permit_Geocode,USER_REM_PARCEL_STATUS,0,1', '', "USER_REM_PARCEL_STATUS = 'A'")
    print ("\n   Appending Building_Permit_Geocode in_memory into BLDGPERM_TBL_AUTOWKSP")
    write_log("\n   Appending Building_Permit_Geocode in_memory into BLDGPERM_TBL_AUTOWKSP",logfile)
except:
    print ("\n Unable to Appending Building_Permit_Geocode in_memory into BLDGPERM_TBL_AUTOWKSP")
    write_log("\n Unable to Appending Building_Permit_Geocode in_memory into BLDGPERM_TBL_AUTOWKSP", logfile)
    logging.exception('Got exception on Appending Building_Permit_Geocode in_memory into BLDGPERM_TBL_AUTOWKSP logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Delete VISION_BLDGPERM_SDE_GC temporary table
    arcpy.Delete_management(VISION_BLDGPERM_SDE_GC)
except:
    print ("\n Unable to Delete VISION_BLDGPERM_SDE_GC temporary table")
    write_log("Unable to Delete VISION_BLDGPERM_SDE_GC temporary table", logfile)
    logging.exception('Got exception on Delete VISION_BLDGPERM_SDE_GC temporary table logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for (keeps in_memory from getting overloaded or corrupted)
    arcpy.Delete_management("in_memory")
except:
    print ("\n Unable to clear Building_Permit_Geocode from in_memory")
    write_log("Unable to clear Building_Permit_Geocode from in_memory", logfile)
    logging.exception('Got exception on clear Building_Permit_Geocode from in_memory logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Select out unmatched building permits and export to excel sheet
    Unmatched_Building_Permits = arcpy.MakeFeatureLayer_management(BLDG_PRMT_AST, "Unmatched_Building_Permits", "GEOCODE_STATUS = 'U'", "", "OBJECTID OBJECTID VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;PERMIT_LINK PERMIT_LINK VISIBLE NONE;EDITOR EDITOR VISIBLE NONE;DATE_EDIT DATE_EDIT VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;GEOCODE_STATUS GEOCODE_STATUS VISIBLE NONE")
    arcpy.TableToExcel_conversion(Unmatched_Building_Permits, UNMATCHED_PERMITS_EXCEL, "ALIAS", "DESCRIPTION")
    print ("\n    Exported out unmatched GIS building permits list to: "+UNMATCHED_PERMITS_EXCEL)
    write_log ("\n    Exported out unmatched GIS building permits list to: "+UNMATCHED_PERMITS_EXCEL, logfile)
except:
    print ("\n Unable to Select out unmatched building permits and export to excel sheet")
    write_log("Unable to Select out unmatched building permits and export to excel sheet", logfile)
    logging.exception('Got exception on Select out unmatched building permits and export to excel sheet logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Create feature layer of matched or tied records from Building Permit Geocode
    Matched_Tied_Building_Permits = arcpy.MakeFeatureLayer_management(BLDG_PRMT_AST, "Matched_Tied_Building_Permits", "GEOCODE_STATUS = 'M' OR GEOCODE_STATUS = 'T'", "", "OBJECTID OBJECTID VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;PERMIT_LINK PERMIT_LINK VISIBLE NONE;EDITOR EDITOR VISIBLE NONE;DATE_EDIT DATE_EDIT VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;GEOCODE_STATUS GEOCODE_STATUS VISIBLE NONE")
    print ("\n   Create feature layer of matched or tied records from Building Permit Geocode")
    write_log("\n   Create feature layer of matched or tied records from Building Permit Geocode",logfile)
except:
    print ("\n Unable to Create feature layer of matched or tied records from Building Permit Geocode")
    write_log("\n Unable to Create feature layer of matched or tied records from Building Permit Geocode", logfile)
    logging.exception('Got exception on Create feature layer of matched or tied records from Building Permit Geocode logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Make temporary feature (BUILDING_PERMIT_TEMP) from BLDG_PRMT_AST (creates temporary file of building permit points from assessment workspace)
    BUILDING_PERMIT_TEMP = arcpy.FeatureClassToFeatureClass_conversion(Matched_Tied_Building_Permits, AUTOWORKSPACE_AST, "BUILDING_PERMIT_TEMP", "", 'REM_PID "PID" true true false 4 Long 0 10 ,First,#,Matched_Tied_Building_Permits,REM_PID,-1,-1;PERMIT_LINK "PID-PERMIT #" true true false 100 Text 0 0 ,First,#,Matched_Tied_Building_Permits,PERMIT_LINK,-1,-1;EDITOR "EDITOR" true true false 255 Text 0 0 ,First,#,Matched_Tied_Building_Permits,EDITOR,-1,-1;DATE_EDIT "DATE_EDIT" false true false 8 Date 0 0 ,First,#,Matched_Tied_Building_Permits,DATE_EDIT,-1,-1;GEOCODE_STATUS "Status of Geocode" true true false 50 Text 0 0 ,First,#,Matched_Tied_Building_Permits,GEOCODE_STATUS,-1,-1', "")
except:
    print ("\n Unable to make temporary feature (BUILDING_PERMIT_TEMP) from BLDG_PRMT_AST")
    write_log("\n Unable to make temporary feature (BUILDING_PERMIT_TEMP) from BLDG_PRMT_AST", logfile)
    logging.exception('Got exception on make temporary feature (BUILDING_PERMIT_TEMP) from BLDG_PRMT_AST logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Join BUILDING_PERMIT_TEMP & VISIDATA_TEMP (joins building permit points from assessment workspace to vision data {other and owner tables})
    arcpy.JoinField_management(BUILDING_PERMIT_TEMP, "REM_PID", VISIDATA_TEMP, "REM_PID", "REM_MNC;REM_PID;REM_PIN;REM_OWN_NAME;REM_PRCL_LOCN;REM_PRCL_LOCN_CITY;REM_PRCL_LOCN_STT;REM_PRCL_LOCN_ZIP;REM_ALT_PRCL_ID;REM_PRCL_STATUS_DATE;REM_MBLU_MAP;REM_MBLU_MAP_CUT;REM_MBLU_BLOCK;REM_MBLU_BLOCK_CUT;REM_MBLU_LOT;REM_MBLU_LOT_CUT;REM_MBLU_UNIT;REM_MBLU_UNIT_CUT;REM_STATUS_DATE;REM_INET_SUPPRESS;REM_IS_CONDO_MAIN;REM_CMPLX_NAME;REM_BLDG_NAME;REM_USE_CODE;REM_LEGAL_AREA;REM_LAST_UPDATE;REM_USRFLD;REM_USRFLD_DESC;PID_TEXT;LND_USE_CODE;LND_USE_DESC;LND_DSTRCT;MUNI_NAME;PRC_PF_LOCN;PRC_PF_LOCN_DESC;PRC_USRFLD_09;PRC_USRFLD_10;PRC_TTL_ASSESS_BLDG;PRC_TTL_ASSESS_IMPROVEMENTS;PRC_TTL_ASSESS_LND;PRC_TTL_ASSESS_OB;PRC_VALUE;PRC_CMPLX_PID;PRC_CMPLX_DESC;PRC_CENSUS;PRC_TTL_MRKT_ASSESS;PRC_TTL_ASSESS;OWN_ID;OWN_NAME1;OWN_NAME2;ROW_PID;ROW_OWN_ID;ROW_LINE_NUM;ROW_OWN_PCT;ROW_PRIMARY;ROW_CREATE_DATE;ROW_MAD_ID;ROW_MAD_ISPRIMARY;OWN_LINE;MAD_MAIL_NAME1;MAD_MAIL_NAME2;MAD_MAIL_ADDR1;MAD_MAIL_CITY;MAD_MAIL_STATE;MAD_MAIL_ZIP;MAD_MAIL_ADDR2;MAD_ID;SLH_PID;SLH_LINE_NUM;SLH_SALE_DATE;SLH_BOOK;SLH_PAGE;SLH_PRICE;SLH_CURRENT_OWNER")
    print ("  BUILDING_PERMIT_TEMP & VISIDATA_TEMP joined...")
    write_log("  BUILDING_PERMIT_TEMP & VISIDATA_TEMP joined...",logfile)
except:
    print ("\n Unable to join BUILDING_PERMIT_TEMP & VISIDATA_TEMP")
    write_log("\n Unable to join BUILDING_PERMIT_TEMP & VISIDATA_TEMP", logfile)
    logging.exception('Got exception on join BUILDING_PERMIT_TEMP & VISIDATA_TEMP logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Joining BLDGPERM_VISION_VIEW with VISION_OTHER_TBL and VISION_OWNER_TBL completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Joining BLDGPERM_VISION_VIEW with VISION_OTHER_TBL and VISION_OWNER_TBL completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

try:
    # Join BUILDING_PERMIT_TEMP & VISION_BLDGPERM_SDE (joins building permit points from assessment workspace to vision data {building permit table})
    arcpy.JoinField_management(BUILDING_PERMIT_TEMP, "PERMIT_LINK", VISION_BLDGPERM_SDE, "PERMIT_LINK","BPE_PID;BPE_PERMIT_ID;BPE_FISCAL_YR;BPE_APP_DATE;BPE_ISSUE_DATE;BPE_INSPECT_DATE;BPE_AMOUNT;BPE_FEE;BPE_APPLICANT;BPE_LICENCE;BPE_COMPANY;BPE_AREA;BPE_REF;BPE_DESC;BPE_PCT_COMPLETE;BPE_DATE_COMPLETE;BPE_COMMENT;BPE_USRFLD_01;BPE_USRFLD_02;BPE_USRFLD_03;BPE_USRFLD_04;BPE_USRFLD_05;PERMIT_LINK")
except:
    print ("\n Unable to join BUILDING_PERMIT_TEMP & VISION_BLDGPERM_SDE")
    write_log("\n Unable to join BUILDING_PERMIT_TEMP & VISION_BLDGPERM_SDE", logfile)
    logging.exception('Got exception on join BUILDING_PERMIT_TEMP & VISION_BLDGPERM_SDE logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
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
    logging.exception('Got exception on delete rows from Building_Permit_Joined - AST logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append BUILDING_PERMIT_TEMP to BUILDING_PERMIT_JOINED_AUTOWKSP (appends temporary file of building permit points and vision data to "real" feature class)
    arcpy.Append_management(BUILDING_PERMIT_TEMP, BUILDING_PERMIT_JOINED_AUTOWKSP, "NO_TEST", 'REM_PID "PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PID,-1,-1;PERMIT_LINK "PID-PERMIT #" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PERMIT_LINK,-1,-1;EDITOR "EDITOR" true true false 255 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,EDITOR,-1,-1;DATE_EDIT "DATE_EDIT" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,DATE_EDIT,-1,-1;REM_MNC "REM_MNC" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MNC,-1,-1;REM_PID_1 "PID Number" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PID_1,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PIN,-1,-1;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "Lot" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_BLDG_NAME,-1,-1;REM_USE_CODE "Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_USE_CODE,-1,-1;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_USRFLD,-1,-1;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,REM_USRFLD_DESC,-1,-1;PID_TEXT "PID Text format" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PID_TEXT,-1,-1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,LND_USE_CODE,-1,-1;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,LND_DSTRCT,-1,-1;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_PF_LOCN,-1,-1;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_PF_LOCN_DESC,-1,-1;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PRC_TTL_ASSESS,-1,-1;OWN_ID "OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,OWN_NAME2,-1,-1;ROW_PID "ROW_PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,OWN_LINE,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_MAIL_ADDR2,-1,-1;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_BOOK,-1,-1;SLH_PAGE "Deed Page" true true false 15 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_PAGE,-1,-1;SLH_PRICE "Sale Price" true true false 8 Double 8 38 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,SLH_CURRENT_OWNER,-1,-1;BPE_PID "BPE_PID" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_PID,-1,-1;BPE_PERMIT_ID "BPE_PERMIT_ID" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_PERMIT_ID,-1,-1;BPE_FISCAL_YR "BPE_FISCAL_YR" true true false 2 Short 0 5 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_FISCAL_YR,-1,-1;BPE_APP_DATE "BPE_APP_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_APP_DATE,-1,-1;BPE_ISSUE_DATE "BPE_ISSUE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_ISSUE_DATE,-1,-1;BPE_INSPECT_DATE "BPE_INSPECT_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_INSPECT_DATE,-1,-1;BPE_AMOUNT "BPE_AMOUNT" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_AMOUNT,-1,-1;BPE_FEE "BPE_FEE" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_FEE,-1,-1;BPE_APPLICANT "BPE_APPLICANT" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_APPLICANT,-1,-1;BPE_LICENCE "BPE_LICENCE" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_LICENCE,-1,-1;BPE_COMPANY "BPE_COMPANY" true true false 50 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_COMPANY,-1,-1;BPE_AREA "BPE_AREA" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_AREA,-1,-1;BPE_REF "BPE_REF" true true false 20 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_REF,-1,-1;BPE_DESC "BPE_DESC" true true false 40 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_DESC,-1,-1;BPE_PCT_COMPLETE "BPE_PCT_COMPLETE" true true false 4 Long 0 10 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_PCT_COMPLETE,-1,-1;BPE_DATE_COMPLETE "BPE_DATE_COMPLETE" true true false 8 Date 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_DATE_COMPLETE,-1,-1;BPE_COMMENT "BPE_COMMENT" true true false 750 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_COMMENT,-1,-1;BPE_USRFLD_01 "BPE_USRFLD_01" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_USRFLD_01,-1,-1;BPE_USRFLD_02 "BPE_USRFLD_02" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_USRFLD_02,-1,-1;BPE_USRFLD_03 "BPE_USRFLD_03" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_USRFLD_03,-1,-1;BPE_USRFLD_04 "BPE_USRFLD_04" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_USRFLD_04,-1,-1;BPE_USRFLD_05 "BPE_USRFLD_05" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,BPE_USRFLD_05,-1,-1;PERMIT_LINK_1 "PERMIT_LINK_1" true true false 100 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,PERMIT_LINK_1,-1,-1;MUNI_NAME "Municipality Name" true true false 75 Text 0 0 ,First,#,Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.BUILDING_PERMIT_TEMP,MUNI_NAME,-1,-1', "")
    BLDG_PMT_result = arcpy.GetCount_management(BUILDING_PERMIT_JOINED_AUTOWKSP)
    print ('{} has {} records'.format(BUILDING_PERMIT_JOINED_AUTOWKSP, BLDG_PMT_result[0]))
    write_log('{} has {} records'.format(BUILDING_PERMIT_JOINED_AUTOWKSP, BLDG_PMT_result[0]), logfile)
except:
    print ("\n Unable to append BUILDING_PERMIT_TEMP to BUILDING_PERMIT_JOINED_AUTOWKSP")
    write_log("\n Unable to append BUILDING_PERMIT_TEMP to BUILDING_PERMIT_JOINED_AUTOWKSP", logfile)
    logging.exception('Got exception on append BUILDING_PERMIT_TEMP to BUILDING_PERMIT_JOINED_AUTOWKSP logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()
    

print ("       Updating BUILDING_PERMIT_TEMP to BUILDING_PERMIT_JOINED_AUTOWKSP completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating BUILDING_PERMIT_TEMP to BUILDING_PERMIT_JOINED_AUTOWKSP completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating BUILDING_PERMIT_JOINED from AUTOWKSP to Craw Internal")
write_log("\n Updating BUILDING_PERMIT_JOINED from AUTOWKSP to Craw Internal", logfile)

try:
    # Delete rows from Building_Permit_Joined - Craw Internal
    arcpy.DeleteRows_management(BUILDING_PERMITS_INTERNAL)
except:
    print ("\n Unable to delete rows from Building_Permit_Joined - Craw Internal")
    write_log("\n Unable to delete rows from Building_Permit_Joined - Craw Internal", logfile)
    logging.exception('Got exception on delete rows from Building_Permit_Joined - Craw Internal logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append BUILDING_PERMITS - AUTOWKSP to BUILDING_PERMITS- Craw Internal 
    arcpy.Append_management(BUILDING_PERMIT_JOINED_AUTOWKSP, BUILDING_PERMITS_INTERNAL, "NO_TEST", 'REM_PID "PID Number" true true false 4 Long 0 10 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_PID,-1,-1;REM_PID_1 "PID Number" true true false 4 Long 0 10 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_PID_1,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_PIN,-1,-1;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "Lot" true true false 7 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_BLDG_NAME,-1,-1;REM_USE_CODE "Use Code" true true false 4 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_USE_CODE,-1,-1;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_USRFLD,-1,-1;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',REM_USRFLD_DESC,-1,-1;PID_TEXT "PID Text format" true true false 15 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PID_TEXT,-1,-1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',LND_USE_CODE,-1,-1;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',LND_DSTRCT,-1,-1;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_PF_LOCN,-1,-1;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_PF_LOCN_DESC,-1,-1;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',PRC_TTL_ASSESS,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',OWN_NAME2,-1,-1;ROW_PID "ROW_PID" true true false 4 Long 0 10 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',ROW_PID,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',ROW_OWN_PCT,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',MAD_MAIL_ADDR2,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',SLH_PID,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',SLH_BOOK,-1,-1;SLH_PAGE "Deed Page" true true false 15 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',SLH_PAGE,-1,-1;SLH_PRICE "Sale Price" true true false 8 Double 8 38 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',SLH_PRICE,-1,-1;BPE_PID "Building Permit PID Number" true true false 4 Long 0 10 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_PID,-1,-1;BPE_PERMIT_ID "Permit ID" true true false 20 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_PERMIT_ID,-1,-1;BPE_FISCAL_YR "Permit Fiscal Year" true true false 2 Short 0 5 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_FISCAL_YR,-1,-1;BPE_APP_DATE "Permit Application Date" true true false 8 Date 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_APP_DATE,-1,-1;BPE_ISSUE_DATE "Permit Issue Date" true true false 8 Date 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_ISSUE_DATE,-1,-1;BPE_INSPECT_DATE "Permit Inspection Date" true true false 8 Date 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_INSPECT_DATE,-1,-1;BPE_AMOUNT "Permit Amount" true true false 4 Long 0 10 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_AMOUNT,-1,-1;BPE_FEE "Permit Fee" true true false 4 Long 0 10 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_FEE,-1,-1;BPE_APPLICANT "Permit Applicant" true true false 50 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_APPLICANT,-1,-1;BPE_LICENCE "Permit License" true true false 20 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_LICENCE,-1,-1;BPE_COMPANY "Permit Company" true true false 50 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_COMPANY,-1,-1;BPE_AREA "Permit Area" true true false 20 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_AREA,-1,-1;BPE_REF "Permit Reference" true true false 20 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_REF,-1,-1;BPE_DESC "Permit Description" true true false 40 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_DESC,-1,-1;BPE_PCT_COMPLETE "Permit Percent Complete" true true false 4 Long 0 10 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_PCT_COMPLETE,-1,-1;BPE_DATE_COMPLETE "Permit Date Complete" true true false 8 Date 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_DATE_COMPLETE,-1,-1;BPE_COMMENT "Permit Comment" true true false 750 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_COMMENT,-1,-1;BPE_USRFLD_01 "Permit User Field 1 (Not used)" true true false 100 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_USRFLD_01,-1,-1;BPE_USRFLD_02 "Permit User Field 2 (Not used)" true true false 100 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_USRFLD_02,-1,-1;BPE_USRFLD_03 "Permit User Field 3 (Not used)" true true false 100 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_USRFLD_03,-1,-1;BPE_USRFLD_04 "Permit User Field 4 (Not used)" true true false 100 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_USRFLD_04,-1,-1;BPE_USRFLD_05 "Permit User Field 5 (Not used)" true true false 100 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',BPE_USRFLD_05,-1,-1;GlobalID "GlobalID" false false true 38 GlobalID 0 0 ,First,#;MUNI_NAME "Municipality Name" true true false 75 Text 0 0 ,First,#,'+BUILDING_PERMIT_JOINED_AUTOWKSP+',MUNI_NAME,-1,-1', "")
    BLDG_PMT_INTL_result = arcpy.GetCount_management(BUILDING_PERMITS_INTERNAL)
    print ('{} has {} records'.format(BUILDING_PERMITS_INTERNAL, BLDG_PMT_INTL_result[0]))
    write_log('{} has {} records'.format(BUILDING_PERMITS_INTERNAL, BLDG_PMT_INTL_result[0]), logfile)
except:
    print ("\n Unable to append BUILDING_PERMITS - AUTOWKSP to BUILDING_PERMITS- Craw Internal")
    write_log("\n Unable to append BUILDING_PERMITS - AUTOWKSP to BUILDING_PERMITS- Craw Internal", logfile)
    logging.exception('Got exception on append BUILDING_PERMITS - AUTOWKSP to BUILDING_PERMITS- Craw Internal logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating BUILDING_PERMITS - AUTOWKSP to BUILDING_PERMITS- Craw Internal completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating BUILDING_PERMITS - AUTOWKSP to BUILDING_PERMITS- Craw Internal completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating BUILDING_PERMIT_JOINED from Craw Internal to Public Web")
write_log("\n Updating BUILDING_PERMIT_JOINED from Craw Internal to Public Web", logfile)

try:
    # Delete rows from Building_Permit_Joined - Craw Internal
    arcpy.DeleteRows_management(BUILDING_PERMIT_WEB)
    print ("\n Building_Permit_Joined - Craw Internal rows deleted")
except:
    print ("\n Unable to delete rows from Building_Permit_Joined - Craw Internal")
    write_log("\n Unable to delete rows from Building_Permit_Joined - Craw Internal", logfile)
    logging.exception('Got exception on delete rows from Building_Permit_Joined - Craw Internal logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make feature layer of Building Permits - Craw Internal with following removed (BPE_DESC <> '911 NOTIFICATION' AND BPE_DESC <> 'PICTOMETRY CHECK' AND BPE_DESC <> 'LIMITED SCOPE OPINION' AND BPE_DESC <> 'SOLAR FARM' AND BPE_DESC <> 'REPORTED STORM DAMAGE' AND BPE_DESC <> 'CONTINUED REVIEW')
    BldgPerm_Web_Layer = arcpy.MakeFeatureLayer_management(BUILDING_PERMITS_INTERNAL, "BldgPerm_Web_Layer", "BPE_DESC <> '911 NOTIFICATION' AND BPE_DESC <> 'PICTOMETRY CHECK' AND BPE_DESC <> 'LIMITED SCOPE OPINION' AND BPE_DESC <> 'SOLAR FARM' AND BPE_DESC <> 'REPORTED STORM DAMAGE' AND BPE_DESC <> 'CONTINUED REVIEW'", "", "REM_PID REM_PID VISIBLE NONE;REM_PID_1 REM_PID_1 VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;PID_TEXT PID_TEXT VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;ROW_PID ROW_PID VISIBLE NONE;ROW_OWN_PCT ROW_OWN_PCT VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;MAD_MAIL_ADDR2 MAD_MAIL_ADDR2 VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;BPE_PID BPE_PID VISIBLE NONE;BPE_PERMIT_ID BPE_PERMIT_ID VISIBLE NONE;BPE_FISCAL_YR BPE_FISCAL_YR VISIBLE NONE;BPE_APP_DATE BPE_APP_DATE VISIBLE NONE;BPE_ISSUE_DATE BPE_ISSUE_DATE VISIBLE NONE;BPE_INSPECT_DATE BPE_INSPECT_DATE VISIBLE NONE;BPE_AMOUNT BPE_AMOUNT VISIBLE NONE;BPE_FEE BPE_FEE VISIBLE NONE;BPE_APPLICANT BPE_APPLICANT VISIBLE NONE;BPE_LICENCE BPE_LICENCE VISIBLE NONE;BPE_COMPANY BPE_COMPANY VISIBLE NONE;BPE_AREA BPE_AREA VISIBLE NONE;BPE_REF BPE_REF VISIBLE NONE;BPE_DESC BPE_DESC VISIBLE NONE;BPE_PCT_COMPLETE BPE_PCT_COMPLETE VISIBLE NONE;BPE_DATE_COMPLETE BPE_DATE_COMPLETE VISIBLE NONE;BPE_COMMENT BPE_COMMENT VISIBLE NONE;BPE_USRFLD_01 BPE_USRFLD_01 VISIBLE NONE;BPE_USRFLD_02 BPE_USRFLD_02 VISIBLE NONE;BPE_USRFLD_03 BPE_USRFLD_03 VISIBLE NONE;BPE_USRFLD_04 BPE_USRFLD_04 VISIBLE NONE;BPE_USRFLD_05 BPE_USRFLD_05 VISIBLE NONE;Shape Shape VISIBLE NONE;GlobalID GlobalID VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;MUNI_NAME MUNI_NAME VISIBLE NONE")
    print ("\n Feature layer of Building Permits - Craw Internal created")
except:
    print ("\n Unable to delete rows from Building_Permit_Joined - Craw Internal")
    write_log("\n Unable to delete rows from Building_Permit_Joined - Craw Internal", logfile)
    logging.exception('Got exception on delete rows from Building_Permit_Joined - Craw Internal logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append BUILDING_PERMITS - CRAW INTERNAL to BUILDING_PERMITS- WEB (appends redacted records to public facing feature class)
    arcpy.Append_management(BldgPerm_Web_Layer, BUILDING_PERMIT_WEB, "NO_TEST", 'REM_PID "PID Number" true true false 4 Long 0 10 ,First,#,BldgPerm_Web_Layer,REM_PID,-1,-1;REM_PID_1 "PID Number" true true false 4 Long 0 10 ,First,#,BldgPerm_Web_Layer,REM_PID_1,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_PIN,-1,-1;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_OWN_NAME,-1,-1;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_PRCL_LOCN,-1,-1;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_PRCL_LOCN_CITY,-1,-1;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_PRCL_LOCN_STT,-1,-1;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_PRCL_LOCN_ZIP,-1,-1;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_ALT_PRCL_ID,-1,-1;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0 ,First,#,BldgPerm_Web_Layer,REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_MBLU_MAP,-1,-1;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_MBLU_MAP_CUT,-1,-1;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_MBLU_BLOCK,-1,-1;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_MBLU_BLOCK_CUT,-1,-1;REM_MBLU_LOT "Lot" true true false 7 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_MBLU_LOT,-1,-1;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_MBLU_LOT_CUT,-1,-1;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_MBLU_UNIT,-1,-1;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_MBLU_UNIT_CUT,-1,-1;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0 ,First,#,BldgPerm_Web_Layer,REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10 ,First,#,BldgPerm_Web_Layer,REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5 ,First,#,BldgPerm_Web_Layer,REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_CMPLX_NAME,-1,-1;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_BLDG_NAME,-1,-1;REM_USE_CODE "Use Code" true true false 4 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_USE_CODE,-1,-1;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38 ,First,#,BldgPerm_Web_Layer,REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0 ,First,#,BldgPerm_Web_Layer,REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_USRFLD,-1,-1;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0 ,First,#,BldgPerm_Web_Layer,REM_USRFLD_DESC,-1,-1;PID_TEXT "PID Text format" true true false 15 Text 0 0 ,First,#,BldgPerm_Web_Layer,PID_TEXT,-1,-1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0 ,First,#,BldgPerm_Web_Layer,LND_USE_CODE,-1,-1;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0 ,First,#,BldgPerm_Web_Layer,LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,BldgPerm_Web_Layer,LND_DSTRCT,-1,-1;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0 ,First,#,BldgPerm_Web_Layer,PRC_PF_LOCN,-1,-1;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0 ,First,#,BldgPerm_Web_Layer,PRC_PF_LOCN_DESC,-1,-1;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0 ,First,#,BldgPerm_Web_Layer,PRC_USRFLD_09,-1,-1;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0 ,First,#,BldgPerm_Web_Layer,PRC_USRFLD_10,-1,-1;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38 ,First,#,BldgPerm_Web_Layer,PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38 ,First,#,BldgPerm_Web_Layer,PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38 ,First,#,BldgPerm_Web_Layer,PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38 ,First,#,BldgPerm_Web_Layer,PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38 ,First,#,BldgPerm_Web_Layer,PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10 ,First,#,BldgPerm_Web_Layer,PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0 ,First,#,BldgPerm_Web_Layer,PRC_CMPLX_DESC,-1,-1;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0 ,First,#,BldgPerm_Web_Layer,PRC_CENSUS,-1,-1;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38 ,First,#,BldgPerm_Web_Layer,PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38 ,First,#,BldgPerm_Web_Layer,PRC_TTL_ASSESS,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0 ,First,#,BldgPerm_Web_Layer,OWN_NAME1,-1,-1;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0 ,First,#,BldgPerm_Web_Layer,OWN_NAME2,-1,-1;ROW_PID "ROW_PID" true true false 4 Long 0 10 ,First,#,BldgPerm_Web_Layer,ROW_PID,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5 ,First,#,BldgPerm_Web_Layer,ROW_OWN_PCT,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0 ,First,#,BldgPerm_Web_Layer,MAD_MAIL_NAME1,-1,-1;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0 ,First,#,BldgPerm_Web_Layer,MAD_MAIL_NAME2,-1,-1;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0 ,First,#,BldgPerm_Web_Layer,MAD_MAIL_ADDR1,-1,-1;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0 ,First,#,BldgPerm_Web_Layer,MAD_MAIL_CITY,-1,-1;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0 ,First,#,BldgPerm_Web_Layer,MAD_MAIL_STATE,-1,-1;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0 ,First,#,BldgPerm_Web_Layer,MAD_MAIL_ZIP,-1,-1;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0 ,First,#,BldgPerm_Web_Layer,MAD_MAIL_ADDR2,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10 ,First,#,BldgPerm_Web_Layer,SLH_PID,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0 ,First,#,BldgPerm_Web_Layer,SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0 ,First,#,BldgPerm_Web_Layer,SLH_BOOK,-1,-1;SLH_PAGE "Deed Page" true true false 15 Text 0 0 ,First,#,BldgPerm_Web_Layer,SLH_PAGE,-1,-1;SLH_PRICE "Sale Price" true true false 8 Double 8 38 ,First,#,BldgPerm_Web_Layer,SLH_PRICE,-1,-1;BPE_PID "Building Permit PID Number" true true false 4 Long 0 10 ,First,#,BldgPerm_Web_Layer,BPE_PID,-1,-1;BPE_PERMIT_ID "Permit ID" true true false 20 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_PERMIT_ID,-1,-1;BPE_FISCAL_YR "Permit Fiscal Year" true true false 2 Short 0 5 ,First,#,BldgPerm_Web_Layer,BPE_FISCAL_YR,-1,-1;BPE_APP_DATE "Permit Application Date" true true false 8 Date 0 0 ,First,#,BldgPerm_Web_Layer,BPE_APP_DATE,-1,-1;BPE_ISSUE_DATE "Permit Issue Date" true true false 8 Date 0 0 ,First,#,BldgPerm_Web_Layer,BPE_ISSUE_DATE,-1,-1;BPE_INSPECT_DATE "Permit Inspection Date" true true false 8 Date 0 0 ,First,#,BldgPerm_Web_Layer,BPE_INSPECT_DATE,-1,-1;BPE_AMOUNT "Permit Amount" true true false 4 Long 0 10 ,First,#,BldgPerm_Web_Layer,BPE_AMOUNT,-1,-1;BPE_FEE "Permit Fee" true true false 4 Long 0 10 ,First,#,BldgPerm_Web_Layer,BPE_FEE,-1,-1;BPE_APPLICANT "Permit Applicant" true true false 50 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_APPLICANT,-1,-1;BPE_LICENCE "Permit License" true true false 20 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_LICENCE,-1,-1;BPE_COMPANY "Permit Company" true true false 50 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_COMPANY,-1,-1;BPE_AREA "Permit Area" true true false 20 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_AREA,-1,-1;BPE_REF "Permit Reference" true true false 20 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_REF,-1,-1;BPE_DESC "Permit Description" true true false 40 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_DESC,-1,-1;BPE_PCT_COMPLETE "Permit Percent Complete" true true false 4 Long 0 10 ,First,#,BldgPerm_Web_Layer,BPE_PCT_COMPLETE,-1,-1;BPE_DATE_COMPLETE "Permit Date Complete" true true false 8 Date 0 0 ,First,#,BldgPerm_Web_Layer,BPE_DATE_COMPLETE,-1,-1;BPE_COMMENT "Permit Comment" true true false 750 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_COMMENT,-1,-1;BPE_USRFLD_01 "Permit User Field 1 (Not used)" true true false 100 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_USRFLD_01,-1,-1;BPE_USRFLD_02 "Permit User Field 2 (Not used)" true true false 100 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_USRFLD_02,-1,-1;BPE_USRFLD_03 "Permit User Field 3 (Not used)" true true false 100 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_USRFLD_03,-1,-1;BPE_USRFLD_04 "Permit User Field 4 (Not used)" true true false 100 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_USRFLD_04,-1,-1;BPE_USRFLD_05 "Permit User Field 5 (Not used)" true true false 100 Text 0 0 ,First,#,BldgPerm_Web_Layer,BPE_USRFLD_05,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,BldgPerm_Web_Layer,GlobalID,-1,-1;MUNI_NAME "Municipality Name" true true false 75 Text 0 0 ,First,#,BldgPerm_Web_Layer,MUNI_NAME,-1,-1', "")
    BLDG_PMT_WEB_result = arcpy.GetCount_management(BUILDING_PERMIT_WEB)
    print ('{} has {} records'.format(BUILDING_PERMIT_WEB, BLDG_PMT_WEB_result[0]))
    write_log('{} has {} records'.format(BUILDING_PERMIT_WEB, BLDG_PMT_WEB_result[0]), logfile)
except:
    print ("\n Unable to append BUILDING_PERMITS - CRAW INTERNAL to BUILDING_PERMITS- WEB")
    write_log("\n Unable to append BUILDING_PERMITS - CRAW INTERNAL to BUILDING_PERMITS- WEB", logfile)
    logging.exception('Got exception on append BUILDING_PERMITS - CRAW INTERNAL to BUILDING_PERMITS- WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating BUILDING_PERMIT_JOINED from Craw Internal to Public Web completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating BUILDING_PERMIT_JOINED from Craw Internal to Public Web completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

BLDG_PERMIT_TEMP = [BUILDING_PERMIT_TEMP]

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
    logging.exception('Got exception on delete BLDG_PERMIT_TEMP files logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for (keeps in_memory from getting overloaded or corrupted)
    arcpy.Delete_management("in_memory")
except:
    print ("\n Unable to clear in_memory")
    write_log("Unable to clear in_memory", logfile)
    logging.exception('Got exception on clear in_memory logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL BUILDING PERMIT DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL BUILDING PERMIT DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)

write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
