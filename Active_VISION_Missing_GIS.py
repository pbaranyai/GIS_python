# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Active_VISION_Missing_GIS.py
# Created on: 2021-07-19
# Updated on 2022-01-26
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
#
# Description: 
# Geocode the VIS_REALMAST_TBL (active records only), filter out unmatched records and export to R:\GIS\Assessment\Reports as excel file
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
logfile = r"R:\\GIS\\GIS_LOGS\\Assessment\\Active_VISION_Missing_GIS.log"  
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
AUTOWORKSPACE = Database_Connections + "\\auto_workspace@ccsde.sde"
ASMT_REPORT_FLDR = r"\\CCFILE\\anybody\\GIS\\Assessment\\Reports"
LOCATOR_WKSP = r"\\CCFILE\\anybody\\GIS\\CurrentWebsites\\Locators\\Intranet_Locators"

# Local variables:
MISSING_GIS_REPORT = ASMT_REPORT_FLDR + "\\Active_VISION_Missing_GIS.xls"
MISSING_GIS_GEOCODE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.Assessment\\CCSDE.AUTO_WORKSPACE.Active_VISION_Missing_GIS_Geocode"
CC_PARCEL_LOC = LOCATOR_WKSP + "\\CAMA_PID_Locator"

# Local variables - tables:
VISIDATA_TEMP = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISIDATA_TEMP"

start_time = time.time()

print ("============================================================================")
print ("Creating Active VISION record missing from GIS Report: "+ str(Day) + " " + str(Time))
print ("Located at: R:\GIS\Assessment\Reports")
print ("Works in ArcGIS Pro")
print ("============================================================================")
write_log("============================================================================", logfile)
write_log("Creating Active VISION record missing from GIS Report: "+ str(Day) + " " + str(Time), logfile)
write_log("Located at: R:\GIS\Assessment\Reports", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Deleting excel file & Geocoding all VISION records")
write_log("\n Deleting excel file & Geocoding all VISION records",logfile)

try:
    # Delete excel file so it can be replaced
    if arcpy.Exists(MISSING_GIS_REPORT):
        os.remove(MISSING_GIS_REPORT)
        print (MISSING_GIS_REPORT + " found - table deleted")
        write_log(MISSING_GIS_REPORT + " found - table deleted", logfile)
except:
    print ("\n Unable to delete "+MISSING_GIS_REPORT+", need to delete existing FGDB manually and/or close program locking the tables")
    write_log("\n Unable to delete "+MISSING_GIS_REPORT+", need to delete existing FGDB manually and/or close program locking the tables", logfile)
    logging.exception('Got exception on Unable to delete '+MISSING_GIS_REPORT+', need to delete existing FGDB manually and/or close program locking the tables logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Delete rows from MISSING_GIS_GEOCODE in AUTOWORKSPACE (prep existing FC, by cleaning out rows)
    arcpy.DeleteRows_management(MISSING_GIS_GEOCODE)
except:
    print ("\n Unable to delete rows from MISSING_GIS_GEOCODE")
    write_log("\n Unable to delete rows from MISSING_GIS_GEOCODE", logfile)
    logging.exception('Got exception on delete rows from MISSING_GIS_GEOCODE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Geocode VIS_REALMAST_TBL in AUTOWORKSPACE against CC_PARCEL_Locator, into "memory"
    VIS_REALMAST_GEOCODE = arcpy.geocoding.GeocodeAddresses(VISIDATA_TEMP, CC_PARCEL_LOC, "'Single Line Input' REM_PID VISIBLE NONE", "in_memory/VIS_REALMAST_GEOCODE", "STATIC", None, '', None, "ALL")
    print ("\n Geocoding REALMAST Table into memory")
    write_log ("\n Geocoding REALMAST Table into memory", logfile)
except:
    print ("\n Unable to Geocode VIS_REALMAST_TBL in AUTOWORKSPACE against CC_PARCEL_Locator, into memory")
    write_log("\n Unable to Geocode VIS_REALMAST_TBL in AUTOWORKSPACE against CC_PARCEL_Locator, into memory", logfile)
    logging.exception('Got exception on Geocode VIS_REALMAST_TBL in AUTOWORKSPACE against CC_PARCEL_Locator, into memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append VISIDATA_TEMP_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT
    arcpy.management.Append(VIS_REALMAST_GEOCODE, MISSING_GIS_GEOCODE, "NO_TEST", r'REM_MNC "REM_MNC" true false false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_MNC,-1,-1;REM_PID "PID Number" true false false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_PID,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_PIN,0,35;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_OWN_NAME,0,85;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_PRCL_LOCN,0,50;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_PRCL_LOCN_CITY,0,18;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_PRCL_LOCN_STT,0,2;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_PRCL_LOCN_ZIP,0,12;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_ALT_PRCL_ID,0,35;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_MBLU_MAP,0,7;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_MBLU_MAP_CUT,0,3;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_MBLU_BLOCK,0,7;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_MBLU_BLOCK_CUT,0,3;REM_MBLU_LOT "Lot" true true false 7 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_MBLU_LOT,0,7;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_MBLU_LOT_CUT,0,3;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_MBLU_UNIT,0,7;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_MBLU_UNIT_CUT,0,3;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_CMPLX_NAME,0,30;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_BLDG_NAME,0,60;REM_USE_CODE "Use Code" true true false 4 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_USE_CODE,0,4;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_USRFLD,0,6;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_USRFLD_DESC,0,40;PID_TEXT "PID Text format" true true false 15 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PID_TEXT,0,15;REM_PARCEL_STATUS "Parcel Status in CAMA" true true false 1 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_PARCEL_STATUS,0,1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_LND_USE_CODE,0,4;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_LND_USE_DESC,0,40;LND_DSTRCT "District Number" true true false 6 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_LND_DSTRCT,0,6;MUNI_NAME "Municipality Name" true true false 75 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_MUNI_NAME,0,75;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_PF_LOCN,0,15;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_PF_LOCN_DESC,0,50;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_USRFLD_09,0,30;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_USRFLD_10,0,30;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_CMPLX_DESC,0,30;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_CENSUS,0,20;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_PRC_TTL_ASSESS,-1,-1;OWN_ID "OWN_ID" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_OWN_NAME1,0,85;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_OWN_NAME2,0,85;ROW_PID "ROW_PID" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_OWN_LINE,0,255;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_MAD_MAIL_NAME1,0,85;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_MAD_MAIL_NAME2,0,85;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_MAD_MAIL_ADDR1,0,50;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_MAD_MAIL_CITY,0,30;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_MAD_MAIL_STATE,0,20;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_MAD_MAIL_ZIP,0,20;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_MAD_MAIL_ADDR2,0,50;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_SLH_BOOK,0,15;SLH_PAGE "Deed Page" true true false 15 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_SLH_PAGE,0,15;SLH_PRICE "Sale Price" true true false 8 Double 8 38,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_SLH_CURRENT_OWNER,-1,-1;REM_INET_SUPPRESS_1 "Internet Suppression" true true false 4 Long 0 10,First,#,"in_memory/VIS_REALMAST_GEOCODE",USER_REM_INET_SUPPRESS_1,-1,-1;Match "Match" true true false 255 Text 0 0,First,#,"in_memory/VIS_REALMAST_GEOCODE",Status,0,1', '', '')
    print ("\n   Appending VISIDATA_TEMP_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT")
    write_log ("\n   Appending VISIDATA_TEMP_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT", logfile)
except:
    print ("\n Unable to Append VISIDATA_TEMP_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT")
    write_log("\n Unable to Append VISIDATA_TEMP_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT", logfile)
    logging.exception('Got exception on Append VISIDATA_TEMP_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for (keeps in_memory from getting overloaded or corrupted)
    arcpy.Delete_management("in_memory")
except:
    print ("\n Unable to clear VIS_REALMAST_GEOCODE from in_memory")
    write_log("Unable to clear VIS_REALMAST_GEOCODE from in_memory", logfile)
    logging.exception('Got exception on clear VIS_REALMAST_GEOCODE from in_memory logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Make Feature Layer of MISSING_GIS_GEOCODE, selecting only unmatched records
    Unmatched_Geocoded_VISION_Records = arcpy.management.MakeFeatureLayer(MISSING_GIS_GEOCODE, "Unmatched_Geocoded_VISION_Records", "Match = 'U'", None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;REM_MNC REM_MNC VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;PID_TEXT PID_TEXT VISIBLE NONE;REM_PARCEL_STATUS REM_PARCEL_STATUS VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;MUNI_NAME MUNI_NAME VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_ID OWN_ID VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;ROW_PID ROW_PID VISIBLE NONE;ROW_OWN_ID ROW_OWN_ID VISIBLE NONE;ROW_LINE_NUM ROW_LINE_NUM VISIBLE NONE;ROW_OWN_PCT ROW_OWN_PCT VISIBLE NONE;ROW_PRIMARY ROW_PRIMARY VISIBLE NONE;ROW_CREATE_DATE ROW_CREATE_DATE VISIBLE NONE;ROW_MAD_ID ROW_MAD_ID VISIBLE NONE;ROW_MAD_ISPRIMARY ROW_MAD_ISPRIMARY VISIBLE NONE;OWN_LINE OWN_LINE VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;MAD_MAIL_ADDR2 MAD_MAIL_ADDR2 VISIBLE NONE;MAD_ID MAD_ID VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;REM_INET_SUPPRESS_1 REM_INET_SUPPRESS_1 VISIBLE NONE;Match Match VISIBLE NONE")
except:
    print ("\n Unable to Append VISIDATA_TEMP_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT")
    write_log("\n Unable to Append VISIDATA_TEMP_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT", logfile)
    logging.exception('Got exception on VISIDATA_TEMP_GEOCODE VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Export unmatched records to excel
    arcpy.TableToExcel_conversion(Unmatched_Geocoded_VISION_Records, MISSING_GIS_REPORT, "ALIAS", "DESCRIPTION")
    print ("\n Exporting unmatched records report to: R:\GIS\Assessment\Reports")
    write_log("\n Exporting unmatched records report to: R:\GIS\Assessment\Reports", logfile)
except:
    print ("\n Unable to Export unmatched records to excel")
    write_log("\n Unable to Export unmatched records to excel", logfile)
    logging.exception('Got exception on Export unmatched records to excel logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("         Exporting update table to excel file at R:\GIS\Assessment\Reports completed")
write_log("         Exporting update table to excel file at R:\GIS\Assessment\Reports completed", logfile)


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n Active VISION record missing from GIS REPORT HAS BEEN UPDATED: " + str(Day) + " " + str(end_time))
write_log("\n Active VISION record missing from GIS REPORT HAS BEEN UPDATED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
