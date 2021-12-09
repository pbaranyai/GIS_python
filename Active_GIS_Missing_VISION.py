# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Active_GIS_Missing_VISION.py
# Created on: 2021-09-30 
# Updated on 2021-09-30
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Report any new assessment request or building permit submissions that are currently active - export to excel.
#
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import datetime
import os
import traceback
import logging

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\Assessment\\Active_GIS_Missing_VISION.log"  
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
VISION_VIEW = Database_Connections+ "\\Vision_Database.sde"
CRAW_INTERNAL = Database_Connections+ "\\craw_internal@ccsde.sde"
ASMT_REPORT_FLDR = r"\\CCFILE\\anybody\\GIS\\Assessment\\Reports"
ASMT_REPORT_WORKSPACE = r"\\CCFILE\\anybody\\GIS\\Assessment\\Workspace"
ASMT_TEMP_FGDB = ASMT_REPORT_WORKSPACE + "\\Assessment_GISReport_TempFGDB.gdb"

# Local variables:
REALMAST_VISION = VISION_VIEW + "\\VISION.REAL_PROP.REALMAST"
TAX_PARCELS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.TAX_PARCELS_INTERNAL"
BUILDING_ONLY_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.BUILDING_ONLY_JOINED_INTERNAL"
ActiveGISRecords_Tbl = ASMT_TEMP_FGDB + "\\ActiveGISRecords"
ActiveGIS_Not_In_VISION_Excel = ASMT_REPORT_FLDR + "\\Active_GIS_Not_In_VISION.xls"
REALMAST_CO_TEMP_REPORT = ASMT_TEMP_FGDB + "\\REALMAST_CO_TEMP_REPORT"

start_time = time.time()

print ("============================================================================")
print ("Begining Active GIS Not in VISION report run: "+ str(Day) + " " + str(Time))
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Begining Active GIS Not in VISION report run: "+ str(Day) + " " + str(Time), logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

try:
    # Clean up temp files by deleting them (to stop excel sheets from filling up the folder, it will delete the old report before running a new one)
    if arcpy.Exists(ActiveGIS_Not_In_VISION_Excel):
        os.remove(ActiveGIS_Not_In_VISION_Excel)
        print (ActiveGIS_Not_In_VISION_Excel + " found - table deleted at " + time.strftime("%I:%M:%S %p", time.localtime()))
        write_log(ActiveGIS_Not_In_VISION_Excel + " found - table deleted at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to delete Active GIS Not in VISION excel sheets, need to delete existing excel file manually and/or close program locking the file at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Unable to delete Active GIS Not in VISION excel sheets, need to delete existing excel file manually and/or close program locking the file at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on delete Active GIS Not in VISION excel sheets logged at:'+ time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Ensure ASMT_TEMP_FGDB doesn't exist, if so, delete it
    if arcpy.Exists(ASMT_TEMP_FGDB):
        arcpy.Delete_management(ASMT_TEMP_FGDB)
        print ("ASMT_TEMP_FGDB found - FGDB deleted")
        write_log("ASMT_TEMP_FGDB found - FGDB deleted", logfile)
except:
    print ("\n Unable to delete ASMT_TEMP_FGDB, need to delete existing FGDB manually and/or close program locking the FGDB")
    write_log("Unable to delete ASMT_TEMP_FGDB, need to delete existing FGDB manually and/or close program locking the FGDB", logfile)
    logging.exception('Got exception on delete ASMT_TEMP_FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Create new File GDB called Assessment_Report_TempFGDB.gdb (creating new temporary FGDB for each run, to avoid corruption)
    ASMT_TEMP_FGDB = arcpy.CreateFileGDB_management(ASMT_REPORT_WORKSPACE, "Assessment_GISReport_TempFGDB", "CURRENT")
except:
    print ("\n Unable to create new Assessment_GISReport_TempFGDB.gdb, need to close program locking the FGDB workspace")
    write_log("Unable to create new Assessment_GISReport_TempFGDB.gdb, need to close program locking the FGDB workspace", logfile)
    logging.exception('Got exception on create Assessment_GISReport_TempFGDB.gdb logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make temp table from TAX PARCELS - Internal (just PID field)
    ActiveGISRecords = arcpy.conversion.TableToTable(TAX_PARCELS_INTERNAL, ASMT_TEMP_FGDB, "ActiveGISRecords", '', r'CAMA_PIN "MBLU (Map Block Lot Unit)" true true false 50 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',CAMA_PIN,0,50;MAP "Map" true true false 50 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',MAP,0,50;PARCEL "Parcel" true true false 50 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',PARCEL,0,50;LOT "Lot" true true false 50 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',LOT,0,50;PLANS_AVAILABLE "Plans Available" true true false 5 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',PLANS_AVAILABLE,0,5;SEC_MUNI_NAME "Municipal Name" true true false 50 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',SEC_MUNI_NAME,0,50;PID "PID Number" true true false 4 Long 0 10,First,#,'+TAX_PARCELS_INTERNAL+',PID,-1,-1;REM_PID "PID Number" true true false 4 Long 0 10,First,#,'+TAX_PARCELS_INTERNAL+',REM_PID,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_PIN,0,35;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_OWN_NAME,0,85;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_PRCL_LOCN,0,50;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_PRCL_LOCN_CITY,0,18;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_PRCL_LOCN_STT,0,2;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_PRCL_LOCN_ZIP,0,12;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_ALT_PRCL_ID,0,35;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_MBLU_MAP,0,7;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_MBLU_MAP_CUT,0,3;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_MBLU_BLOCK,0,7;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_MBLU_BLOCK_CUT,0,3;REM_MBLU_LOT "Lot" true true false 7 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_MBLU_LOT,0,7;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_MBLU_LOT_CUT,0,3;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_MBLU_UNIT,0,7;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_MBLU_UNIT_CUT,0,3;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10,First,#,'+TAX_PARCELS_INTERNAL+',REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5,First,#,'+TAX_PARCELS_INTERNAL+',REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_CMPLX_NAME,0,30;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_BLDG_NAME,0,60;REM_USE_CODE "Use Code" true true false 4 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_USE_CODE,0,4;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_USRFLD,0,6;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',REM_USRFLD_DESC,0,40;PID_TEXT "PID Text format" true true false 15 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',PID_TEXT,0,15;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',LND_USE_CODE,0,4;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',LND_USE_DESC,0,40;LND_DSTRCT "District Number" true true false 6 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',LND_DSTRCT,0,6;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',PRC_PF_LOCN,0,15;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',PRC_PF_LOCN_DESC,0,50;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',PRC_USRFLD_09,0,30;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',PRC_USRFLD_10,0,30;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10,First,#,'+TAX_PARCELS_INTERNAL+',PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',PRC_CMPLX_DESC,0,30;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',PRC_CENSUS,0,20;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',PRC_TTL_ASSESS,-1,-1;OWN_ID "OWN_ID" true true false 4 Long 0 10,First,#,'+TAX_PARCELS_INTERNAL+',OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',OWN_NAME1,0,85;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',OWN_NAME2,0,85;ROW_PID "ROW_PID" true true false 4 Long 0 10,First,#,'+TAX_PARCELS_INTERNAL+',ROW_PID,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5,First,#,'+TAX_PARCELS_INTERNAL+',ROW_OWN_PCT,-1,-1;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',MAD_MAIL_NAME1,0,85;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',MAD_MAIL_NAME2,0,85;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',MAD_MAIL_ADDR1,0,50;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',MAD_MAIL_CITY,0,30;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',MAD_MAIL_STATE,0,20;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',MAD_MAIL_ZIP,0,20;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',MAD_MAIL_ADDR2,0,50;SLH_PID "Sales History PID" true true false 4 Long 0 10,First,#,'+TAX_PARCELS_INTERNAL+',SLH_PID,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0,First,#,'+TAX_PARCELS_INTERNAL+',SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',SLH_BOOK,0,15;SLH_PAGE "Deed Page" true true false 15 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',SLH_PAGE,0,15;SLH_PRICE "Sale Price" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5,First,#,'+TAX_PARCELS_INTERNAL+',SLH_CURRENT_OWNER,-1,-1;GIS_ACRES "GIS Calculated Acres - not legal" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',GIS_ACRES,-1,-1;LANDEX_URL "Landex URL" true true false 600 Text 0 0,First,#,'+TAX_PARCELS_INTERNAL+',LANDEX_URL,0,600;LONGITUDE_X "Longitude_X" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',LONGITUDE_X,-1,-1;LATITUDE_Y "Latitude_Y" true true false 8 Double 8 38,First,#,'+TAX_PARCELS_INTERNAL+',LATITUDE_Y,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0,First,#,'+TAX_PARCELS_INTERNAL+',GlobalID,-1,-1', '')
    print("\n Temp table of TAX PARCELS - Internal created at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Temp table of TAX PARCELS - Internal created at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Make temp table from TAX PARCELS - Internal at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Unable to Make temp table from TAX PARCELS - Internal at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on Make temp table from TAX PARCELS - Internal logged at:'  + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Make table view of Building Only Internal
    BuildingOnly_View = arcpy.management.MakeTableView(BUILDING_ONLY_INTERNAL, "BuildingOnly_View", '', None, "REM_PID REM_PID VISIBLE NONE;CAMA_PIN CAMA_PIN VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;PID_TEXT PID_TEXT VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;ROW_PID ROW_PID VISIBLE NONE;ROW_OWN_PCT ROW_OWN_PCT VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;MAD_MAIL_ADDR2 MAD_MAIL_ADDR2 VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;LONGITUDE_X LONGITUDE_X VISIBLE NONE;LATITUDE_Y LATITUDE_Y VISIBLE NONE;MUNI_NAME MUNI_NAME VISIBLE NONE;Shape Shape VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;GlobalID GlobalID VISIBLE NONE")
    print ("\n   Make table view of Building Only Internal completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n   Make table view of Building Only Internal completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Make table view of Building Only Internal at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Unable to Make table view of Building Only Internal at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on Make table view of Building Only Internal logged at:'  + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Append Building Only View into ActiveGISRecords_Tbl
    arcpy.management.Append(BuildingOnly_View, ActiveGISRecords_Tbl, "NO_TEST", r'PID "PID" true false false 10 Long 0 10,First,#,BuildingOnly_View,REM_PID,-1,-1;REM_PID "REM_PID" true false false 10 Long 0 10,First,#,BuildingOnly_View,REM_PID,-1,-1;REM_PIN "REM_PIN" true false false 35 Text 0 0,First,#,BuildingOnly_View,REM_PIN,0,35', '', '')
    print ("\n   Append Building Only View into ActiveGISRecords_Tbl completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n   Append Building Only View into ActiveGISRecords_Tbl completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Append Building Only View into ActiveGISRecords_Tbl at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Unable to Append Building Only View into ActiveGISRecords_Tbl at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on Append Building Only View into ActiveGISRecords_Tbl logged at:'  + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Add Match field to ActiveGISRecords_Tbl
    arcpy.Delete_management(BuildingOnly_View, "") # Deleting temporary view to save processing
    arcpy.management.AddField(ActiveGISRecords_Tbl, "Match", "TEXT", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')
    print ("\n   Add Match field to ActiveGISRecords_Tbl completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n   Add Match field to ActiveGISRecords_Tbl completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Add Match field to ActiveGISRecords_Tbl at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Unable to Add Match field to ActiveGISRecords_Tbl at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on Add Match field to ActiveGISRecords_Tbl logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Make temp table of VISION.REALMAST table (active records only)
    REALMAST_CO_TEMP_REPORT = arcpy.conversion.TableToTable(REALMAST_VISION, ASMT_TEMP_FGDB, "REALMAST_CO_TEMP_REPORT", "REM_PARCEL_STATUS = 'A'", r'REM_MNC "REM_MNC" false false false 4 Long 0 9,First,#,'+REALMAST_VISION+',REM_MNC,-1,-1;REM_PID "REM_PID" false false false 4 Long 0 9,First,#,'+REALMAST_VISION+',REM_PID,-1,-1;REM_PIN "REM_PIN" false true false 35 Text 0 0,First,#,'+REALMAST_VISION+',REM_PIN,0,35;REM_OWN_NAME "REM_OWN_NAME" false true false 85 Text 0 0,First,#,'+REALMAST_VISION+',REM_OWN_NAME,0,85;REM_ACCT_NUM "REM_ACCT_NUM" false true false 30 Text 0 0,First,#,'+REALMAST_VISION+',REM_ACCT_NUM,0,30;REM_PRCL_LOCN "REM_PRCL_LOCN" false true false 50 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN,0,50;REM_PRCL_LOCN_STR_PFX "REM_PRCL_LOCN_STR_PFX" false true false 5 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_STR_PFX,0,5;REM_PRCL_LOCN_STREET "REM_PRCL_LOCN_STREET" false true false 40 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_STREET,0,40;REM_PRCL_LOCN_STR_SFX "REM_PRCL_LOCN_STR_SFX" false true false 5 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_STR_SFX,0,5;REM_PRCL_LOCN_NUM "REM_PRCL_LOCN_NUM" false true false 4 Long 0 9,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_NUM,-1,-1;REM_PRCL_LOCN_NUM_CHAR "REM_PRCL_LOCN_NUM_CHAR" false true false 15 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_NUM_CHAR,0,15;REM_PRCL_LOCN_CITY "REM_PRCL_LOCN_CITY" false true false 18 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_CITY,0,18;REM_PRCL_LOCN_STT "REM_PRCL_LOCN_STT" false true false 2 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_STT,0,2;REM_PRCL_LOCN_ZIP "REM_PRCL_LOCN_ZIP" false true false 12 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_ZIP,0,12;REM_PRCL_LOCN_APT "REM_PRCL_LOCN_APT" false true false 12 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_APT,0,12;REM_ALT_PRCL_ID "REM_ALT_PRCL_ID" false true false 35 Text 0 0,First,#,'+REALMAST_VISION+',REM_ALT_PRCL_ID,0,35;REM_PRCL_STATUS_DATE "REM_PRCL_STATUS_DATE" false true false 8 Date 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "REM_MBLU_MAP" false true false 7 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_MAP,0,7;REM_MBLU_MAP_CUT "REM_MBLU_MAP_CUT" false true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_MAP_CUT,0,3;REM_MBLU_BLOCK "REM_MBLU_BLOCK" false true false 7 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_BLOCK,0,7;REM_MBLU_BLOCK_CUT "REM_MBLU_BLOCK_CUT" false true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_BLOCK_CUT,0,3;REM_MBLU_LOT "REM_MBLU_LOT" false true false 7 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_LOT,0,7;REM_MBLU_LOT_CUT "REM_MBLU_LOT_CUT" false true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_LOT_CUT,0,3;REM_MBLU_UNIT "REM_MBLU_UNIT" false true false 7 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_UNIT,0,7;REM_MBLU_UNIT_CUT "REM_MBLU_UNIT_CUT" false true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_UNIT_CUT,0,3;REM_STATUS_DATE "REM_STATUS_DATE" false true false 8 Date 0 0,First,#,'+REALMAST_VISION+',REM_STATUS_DATE,-1,-1;REM_INTRNL_NOTE "REM_INTRNL_NOTE" false true false 30 Text 0 0,First,#,'+REALMAST_VISION+',REM_INTRNL_NOTE,0,30;REM_CARD_QUEUE "REM_CARD_QUEUE" false true false 12 Text 0 0,First,#,'+REALMAST_VISION+',REM_CARD_QUEUE,0,12;REM_GROWTH "REM_GROWTH" false true false 4 Long 0 9,First,#,'+REALMAST_VISION+',REM_GROWTH,-1,-1;REM_CHANGED_BY "REM_CHANGED_BY" false true false 30 Text 0 0,First,#,'+REALMAST_VISION+',REM_CHANGED_BY,0,30;REM_GIS_ID "REM_GIS_ID" false true false 30 Text 0 0,First,#,'+REALMAST_VISION+',REM_GIS_ID,0,30;REM_INET_SUPPRESS "REM_INET_SUPPRESS" false true false 4 Long 0 9,First,#,'+REALMAST_VISION+',REM_INET_SUPPRESS,-1,-1;REM_TEMP_PID "REM_TEMP_PID" false true false 4 Long 0 9,First,#,'+REALMAST_VISION+',REM_TEMP_PID,-1,-1;REM_IS_CONDO_MAIN "REM_IS_CONDO_MAIN" false true false 2 Short 0 1,First,#,'+REALMAST_VISION+',REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "REM_CMPLX_NAME" false true false 40 Text 0 0,First,#,'+REALMAST_VISION+',REM_CMPLX_NAME,0,40;REM_PROCESS "REM_PROCESS" false true false 12 Text 0 0,First,#,'+REALMAST_VISION+',REM_PROCESS,0,12;REM_STREET_IDX "REM_STREET_IDX" false true false 1 Text 0 0,First,#,'+REALMAST_VISION+',REM_STREET_IDX,0,1;REM_OWN_IDX "REM_OWN_IDX" false true false 1 Text 0 0,First,#,'+REALMAST_VISION+',REM_OWN_IDX,0,1;REM_ACCT_IDX "REM_ACCT_IDX" false true false 2 Text 0 0,First,#,'+REALMAST_VISION+',REM_ACCT_IDX,0,2;REM_KEY "REM_KEY" false true false 25 Text 0 0,First,#,'+REALMAST_VISION+',REM_KEY,0,25;REM_BLDG_NAME "REM_BLDG_NAME" false true false 60 Text 0 0,First,#,'+REALMAST_VISION+',REM_BLDG_NAME,0,60;REM_ASSOC_PARCEL_ID "REM_ASSOC_PARCEL_ID" false true false 30 Text 0 0,First,#,'+REALMAST_VISION+',REM_ASSOC_PARCEL_ID,0,30;REM_ASSOC_PCT "REM_ASSOC_PCT" false true false 8 Double 2 7,First,#,'+REALMAST_VISION+',REM_ASSOC_PCT,-1,-1;REM_CMPLX_NUM "REM_CMPLX_NUM" false true false 35 Text 0 0,First,#,'+REALMAST_VISION+',REM_CMPLX_NUM,0,35;REM_USE_CODE "REM_USE_CODE" false true false 6 Text 0 0,First,#,'+REALMAST_VISION+',REM_USE_CODE,0,6;REM_USE_TYPE "REM_USE_TYPE" false true false 4 Text 0 0,First,#,'+REALMAST_VISION+',REM_USE_TYPE,0,4;REM_LEGAL_AREA "REM_LEGAL_AREA" false true false 8 Double 4 19,First,#,'+REALMAST_VISION+',REM_LEGAL_AREA,-1,-1;REM_PRCL_ID "REM_PRCL_ID" false true false 20 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_ID,0,20;REM_INTRNL_SUPPRESS "REM_INTRNL_SUPPRESS" false true false 4 Long 0 9,First,#,'+REALMAST_VISION+',REM_INTRNL_SUPPRESS,-1,-1;REM_ENTITY "REM_ENTITY" false true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_ENTITY,0,3;REM_IS_SKELETAL "REM_IS_SKELETAL" false true false 2 Short 0 1,First,#,'+REALMAST_VISION+',REM_IS_SKELETAL,-1,-1;REM_CROSS_STREET_1 "REM_CROSS_STREET_1" false true false 25 Text 0 0,First,#,'+REALMAST_VISION+',REM_CROSS_STREET_1,0,25;REM_CROSS_STREET_2 "REM_CROSS_STREET_2" false true false 25 Text 0 0,First,#,'+REALMAST_VISION+',REM_CROSS_STREET_2,0,25;REM_PRCL_LOCN_NUM_HIGH "REM_PRCL_LOCN_NUM_HIGH" false true false 4 Long 0 9,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_NUM_HIGH,-1,-1;REM_PRCL_LOCN_NUM_CHAR_HIGH "REM_PRCL_LOCN_NUM_CHAR_HIGH" false true false 15 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_NUM_CHAR_HIGH,0,15;REM_BLDG_CLASS "REM_BLDG_CLASS" false true false 6 Text 0 0,First,#,'+REALMAST_VISION+',REM_BLDG_CLASS,0,6;REM_BLDG_CLASS_DESC "REM_BLDG_CLASS_DESC" false true false 40 Text 0 0,First,#,'+REALMAST_VISION+',REM_BLDG_CLASS_DESC,0,40;REM_ST_CODE "REM_ST_CODE" false true false 8 Double 0 11,First,#,'+REALMAST_VISION+',REM_ST_CODE,-1,-1;REM_IS_SUB_MAIN "REM_IS_SUB_MAIN" false true false 2 Short 0 1,First,#,'+REALMAST_VISION+',REM_IS_SUB_MAIN,-1,-1;REM_PARCEL_STATUS "REM_PARCEL_STATUS" false false false 1 Text 0 0,First,#,'+REALMAST_VISION+',REM_PARCEL_STATUS,0,1;REM_MBLU_MAP_DESC "REM_MBLU_MAP_DESC" false true false 40 Text 0 0,First,#,'+REALMAST_VISION+',REM_MBLU_MAP_DESC,0,40;REM_FIELD_REVIEW "REM_FIELD_REVIEW" false true false 2 Short 0 1,First,#,'+REALMAST_VISION+',REM_FIELD_REVIEW,-1,-1;REM_CREATE_STAMP "REM_CREATE_STAMP" false true false 8 Double 0 18,First,#,'+REALMAST_VISION+',REM_CREATE_STAMP,-1,-1;REM_USER_ID "REM_USER_ID" false true false 30 Text 0 0,First,#,'+REALMAST_VISION+',REM_USER_ID,0,30;REM_CREATE_DATE "REM_CREATE_DATE" false true false 8 Date 0 0,First,#,'+REALMAST_VISION+',REM_CREATE_DATE,-1,-1;REM_LAST_UPDATE "REM_LAST_UPDATE" false true false 8 Date 0 0,First,#,'+REALMAST_VISION+',REM_LAST_UPDATE,-1,-1;REM_TAX_ID "REM_TAX_ID" false true false 20 Text 0 0,First,#,'+REALMAST_VISION+',REM_TAX_ID,0,20;REM_SUBMNC "REM_SUBMNC" false true false 4 Long 0 9,First,#,'+REALMAST_VISION+',REM_SUBMNC,-1,-1;REM_PRCL_LOCN_COUNTRY "REM_PRCL_LOCN_COUNTRY" false true false 50 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_COUNTRY,0,50;REM_PRCL_LOCN_COUNTY "REM_PRCL_LOCN_COUNTY" false true false 50 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_COUNTY,0,50;REM_PRCL_LOCN_POST_DIRECTION "REM_PRCL_LOCN_POST_DIRECTION" false true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_POST_DIRECTION,0,3;REM_PRCL_LOCN_PRE_DIRECTION "REM_PRCL_LOCN_PRE_DIRECTION" false true false 3 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_PRE_DIRECTION,0,3;REM_PRCL_LOCN_STREET_TYPE "REM_PRCL_LOCN_STREET_TYPE" false true false 10 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_STREET_TYPE,0,10;REM_PRCL_LOCN_APT_TYPE "REM_PRCL_LOCN_APT_TYPE" false true false 25 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_APT_TYPE,0,25;REM_USRFLD "REM_USRFLD" false true false 6 Text 0 0,First,#,'+REALMAST_VISION+',REM_USRFLD,0,6;REM_USRFLD_DESC "REM_USRFLD_DESC" false true false 40 Text 0 0,First,#,'+REALMAST_VISION+',REM_USRFLD_DESC,0,40;REM_PRCL_LOCN_ADDRESS_ID "REM_PRCL_LOCN_ADDRESS_ID" false true false 100 Text 0 0,First,#,'+REALMAST_VISION+',REM_PRCL_LOCN_ADDRESS_ID,0,100', '')
    print ("\n   Make temp table of VISION.REALMAST table (active records only) completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n   Make temp table of VISION.REALMAST table (active records only) completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Make temp table of VISION.REALMAST table (active records only) at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Unable to Make temp table of VISION.REALMAST table (active records only) at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on Make temp table of VISION.REALMAST table (active records only) logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Join active REALMAST VISION table to Active GIS records
    arcpy.management.AddJoin(ActiveGISRecords_Tbl, "PID", REALMAST_CO_TEMP_REPORT, "REM_PID", "KEEP_ALL")
    print ("\n   Join active REALMAST VISION table to Active GIS records completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n   Join active REALMAST VISION table to Active GIS records completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Join active REALMAST VISION table to Active GIS records at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Unable to Join active REALMAST VISION table to Active GIS records at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on Join active REALMAST VISION table to Active GIS records logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Calculate Match field if PIDs match between tables
    arcpy.management.CalculateField(ActiveGISRecords_Tbl, "Match", "calc(!PID!,!REM_PID!)", "PYTHON3", """def calc(PID, REM_PID):
    if PID == REM_PID:
        return 'Yes'
    else:
        return 'No'""", "TEXT", "NO_ENFORCE_DOMAINS")
    print ("\n   Calculate Match field if PIDs match between tables completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n   Calculate Match field if PIDs match between tables completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Calculate Match field if PIDs match between tables at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Unable to Calculate Match field if PIDs match between tables at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on Calculate Match field if PIDs match between tables logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Make table view of ActiveGISRecords table where Match = No and PID > 0
    ActiveGISRecords_View = arcpy.management.MakeTableView(ActiveGISRecords_Tbl, "ActiveGISRecords_View", "ActiveGISRecords.Match = 'No' And ActiveGISRecords.PID > 0", None, "ActiveGISRecords.OID ActiveGISRecords.OID VISIBLE NONE;ActiveGISRecords.PID ActiveGISRecords.PID VISIBLE NONE;ActiveGISRecords.Match ActiveGISRecords.Match VISIBLE NONE;ActiveGISRecords.ActiveGIST ActiveGISRecords.ActiveGIST VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_MNC VISION.REAL_PROP.REALMAST.REM_MNC VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PID VISION.REAL_PROP.REALMAST.REM_PID VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PIN VISION.REAL_PROP.REALMAST.REM_PIN VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_OWN_NAME VISION.REAL_PROP.REALMAST.REM_OWN_NAME VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_ACCT_NUM VISION.REAL_PROP.REALMAST.REM_ACCT_NUM VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_STR_PFX VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_STR_PFX VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_STREET VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_STREET VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_STR_SFX VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_STR_SFX VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_NUM VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_NUM VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_NUM_CHAR VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_NUM_CHAR VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_CITY VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_CITY VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_STT VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_STT VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_ZIP VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_ZIP VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_APT VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_APT VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_ALT_PRCL_ID VISION.REAL_PROP.REALMAST.REM_ALT_PRCL_ID VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_STATUS_DATE VISION.REAL_PROP.REALMAST.REM_PRCL_STATUS_DATE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_MBLU_MAP VISION.REAL_PROP.REALMAST.REM_MBLU_MAP VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_MBLU_MAP_CUT VISION.REAL_PROP.REALMAST.REM_MBLU_MAP_CUT VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_MBLU_BLOCK VISION.REAL_PROP.REALMAST.REM_MBLU_BLOCK VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_MBLU_BLOCK_CUT VISION.REAL_PROP.REALMAST.REM_MBLU_BLOCK_CUT VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_MBLU_LOT VISION.REAL_PROP.REALMAST.REM_MBLU_LOT VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_MBLU_LOT_CUT VISION.REAL_PROP.REALMAST.REM_MBLU_LOT_CUT VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_MBLU_UNIT VISION.REAL_PROP.REALMAST.REM_MBLU_UNIT VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_MBLU_UNIT_CUT VISION.REAL_PROP.REALMAST.REM_MBLU_UNIT_CUT VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_STATUS_DATE VISION.REAL_PROP.REALMAST.REM_STATUS_DATE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_INTRNL_NOTE VISION.REAL_PROP.REALMAST.REM_INTRNL_NOTE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_CARD_QUEUE VISION.REAL_PROP.REALMAST.REM_CARD_QUEUE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_GROWTH VISION.REAL_PROP.REALMAST.REM_GROWTH VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_CHANGED_BY VISION.REAL_PROP.REALMAST.REM_CHANGED_BY VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_GIS_ID VISION.REAL_PROP.REALMAST.REM_GIS_ID VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_INET_SUPPRESS VISION.REAL_PROP.REALMAST.REM_INET_SUPPRESS VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_TEMP_PID VISION.REAL_PROP.REALMAST.REM_TEMP_PID VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_IS_CONDO_MAIN VISION.REAL_PROP.REALMAST.REM_IS_CONDO_MAIN VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_CMPLX_NAME VISION.REAL_PROP.REALMAST.REM_CMPLX_NAME VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PROCESS VISION.REAL_PROP.REALMAST.REM_PROCESS VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_STREET_IDX VISION.REAL_PROP.REALMAST.REM_STREET_IDX VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_OWN_IDX VISION.REAL_PROP.REALMAST.REM_OWN_IDX VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_ACCT_IDX VISION.REAL_PROP.REALMAST.REM_ACCT_IDX VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_KEY VISION.REAL_PROP.REALMAST.REM_KEY VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_BLDG_NAME VISION.REAL_PROP.REALMAST.REM_BLDG_NAME VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_ASSOC_PARCEL_ID VISION.REAL_PROP.REALMAST.REM_ASSOC_PARCEL_ID VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_ASSOC_PCT VISION.REAL_PROP.REALMAST.REM_ASSOC_PCT VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_CMPLX_NUM VISION.REAL_PROP.REALMAST.REM_CMPLX_NUM VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_USE_CODE VISION.REAL_PROP.REALMAST.REM_USE_CODE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_USE_TYPE VISION.REAL_PROP.REALMAST.REM_USE_TYPE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_LEGAL_AREA VISION.REAL_PROP.REALMAST.REM_LEGAL_AREA VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_ID VISION.REAL_PROP.REALMAST.REM_PRCL_ID VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_INTRNL_SUPPRESS VISION.REAL_PROP.REALMAST.REM_INTRNL_SUPPRESS VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_ENTITY VISION.REAL_PROP.REALMAST.REM_ENTITY VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_IS_SKELETAL VISION.REAL_PROP.REALMAST.REM_IS_SKELETAL VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_CROSS_STREET_1 VISION.REAL_PROP.REALMAST.REM_CROSS_STREET_1 VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_CROSS_STREET_2 VISION.REAL_PROP.REALMAST.REM_CROSS_STREET_2 VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_NUM_HIGH VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_NUM_HIGH VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_NUM_CHAR_HIGH VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_NUM_CHAR_HIGH VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_BLDG_CLASS VISION.REAL_PROP.REALMAST.REM_BLDG_CLASS VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_BLDG_CLASS_DESC VISION.REAL_PROP.REALMAST.REM_BLDG_CLASS_DESC VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_ST_CODE VISION.REAL_PROP.REALMAST.REM_ST_CODE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_IS_SUB_MAIN VISION.REAL_PROP.REALMAST.REM_IS_SUB_MAIN VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PARCEL_STATUS VISION.REAL_PROP.REALMAST.REM_PARCEL_STATUS VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_MBLU_MAP_DESC VISION.REAL_PROP.REALMAST.REM_MBLU_MAP_DESC VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_FIELD_REVIEW VISION.REAL_PROP.REALMAST.REM_FIELD_REVIEW VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_CREATE_STAMP VISION.REAL_PROP.REALMAST.REM_CREATE_STAMP VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_USER_ID VISION.REAL_PROP.REALMAST.REM_USER_ID VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_CREATE_DATE VISION.REAL_PROP.REALMAST.REM_CREATE_DATE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_LAST_UPDATE VISION.REAL_PROP.REALMAST.REM_LAST_UPDATE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_TAX_ID VISION.REAL_PROP.REALMAST.REM_TAX_ID VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_SUBMNC VISION.REAL_PROP.REALMAST.REM_SUBMNC VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_COUNTRY VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_COUNTRY VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_COUNTY VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_COUNTY VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_POST_DIRECTION VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_POST_DIRECTION VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_PRE_DIRECTION VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_PRE_DIRECTION VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_STREET_TYPE VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_STREET_TYPE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_APT_TYPE VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_APT_TYPE VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_USRFLD VISION.REAL_PROP.REALMAST.REM_USRFLD VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_USRFLD_DESC VISION.REAL_PROP.REALMAST.REM_USRFLD_DESC VISIBLE NONE;VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_ADDRESS_ID VISION.REAL_PROP.REALMAST.REM_PRCL_LOCN_ADDRESS_ID VISIBLE NONE;VISION.REAL_PROP.REALMAST.ESRI_OID VISION.REAL_PROP.REALMAST.ESRI_OID VISIBLE NONE")
    print ("\n   Make table view of ActiveGISRecords table where Match = No and PID > 0 completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n   Make table view of ActiveGISRecords table where Match = No and PID > 0 completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Make table view of ActiveGISRecords table where Match = No and PID > 0 at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Unable to Make table view of ActiveGISRecords table where Match = No and PID > 0 at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on Make table view of ActiveGISRecords table where Match = No and PID > 0 logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Export ActiveGISRecords_View out as Excel sheet in reports folder
    arcpy.conversion.TableToExcel(ActiveGISRecords_View, ActiveGIS_Not_In_VISION_Excel, "ALIAS", "CODE")
    arcpy.Delete_management(ActiveGISRecords_View, "") # Deleting temporary view to save processing
    print ("\n   Export ActiveGISRecords_View out as Excel sheet in reports folder completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n   Export ActiveGISRecords_View out as Excel sheet in reports folder completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
except:
    print ("\n Unable to Export ActiveGISRecords_View out as Excel sheet in reports folder at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Unable to Export ActiveGISRecords_View out as Excel sheet in reports folder at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on Export ActiveGISRecords_View out as Excel sheet in reports folder logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

##try:
##    # Deleting temporary FGDB used in above processing
##    if arcpy.Exists(ASMT_TEMP_FGDB):
##        arcpy.Delete_management(ASMT_TEMP_FGDB)
##        print ("ASMT_TEMP_FGDB found - FGDB deleted")
##        write_log("ASMT_TEMP_FGDB found - FGDB deleted", logfile)
##except:
##    print ("\n Unable to delete ASMT_TEMP_FGDB, need to delete existing FGDB manually and/or close program locking the FGDB")
##    write_log("Unable to delete ASMT_TEMP_FGDB, need to delete existing FGDB manually and/or close program locking the FGDB", logfile)
##    logging.exception('Got exception on delete ASMT_TEMP_FGDB logged at:' + str(Day) + " " + str(Time))
##    raise
##    sys.exit ()


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n Active GIS Not in VISION report REPORT COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n Active GIS Not in VISION report COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
