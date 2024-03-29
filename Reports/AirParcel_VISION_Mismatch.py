# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# AirParcel_VISION_Mismatch.py
# Created on: 2022-02-03
# Updated on 2022-02-03
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
#
# Description: 
# Spatial join AirParcels to TaxParcels, add match field, calculate match from AirParcel Block # & TaxParcel Block #, sort out non-matches and export to R:\GIS\Assessment\Reports as excel file
#
# ---------------------------------------------------------------------------

# Import modules
import sys, arcpy,datetime,os,logging,time

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\Assessment\\AirParcel_VISION_Mismatch.log"  
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
    sys.exit ()

#Database Connection Folder
Database_Connections = r"\\FILELOCATION\\GIS\\ArcAutomations\\Database_Connections"

#Database variables:
LANDRECORDS = Database_Connections + "\\craw_internal@ccsde.sde\CCSDE.CRAW_INTERNAL.Land_Records"
ASMT_REPORT_FLDR = r"\\FILELOCATION\\GIS\\Assessment\\Reports"
ASMT_REPORT_WORKSPACE = r"\\FILELOCATION\\GIS\\Assessment\\Workspace"
ASMT_TEMP_FGDB = ASMT_REPORT_WORKSPACE + "\\Assessment_GISReport_TempFGDB.gdb"

# Local variables:
AIRPARCELS = LANDRECORDS + "\\CCSDE.CRAW_INTERNAL.TaxParcel_Air_INTERNAL"
TAXPARCELS = LANDRECORDS + "\\CCSDE.CRAW_INTERNAL.TAX_PARCELS_INTERNAL"
MISMATCH_AIRPARCELS_VISION_REPORT = ASMT_REPORT_FLDR + "\\Mismatched_AirParcels_VISION.xls"
AirParcel_TaxParcel_Join = ASMT_TEMP_FGDB + "\\AirParcel_TaxParcel_Join"

start_time = time.time()

print ("============================================================================")
print ("Creating Mismatched VISION Air Parcels Report: "+ str(Day) + " " + str(Time))
print ("Located at: "+ASMT_REPORT_FLDR)
print ("Works in ArcGIS Pro")
print ("============================================================================")
write_log("============================================================================", logfile)
write_log("Creating Mismatched VISION Air Parcels Report: "+ str(Day) + " " + str(Time), logfile)
write_log("Located at: "+ASMT_REPORT_FLDR, logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Deleting excel file & Geocoding all VISION records")
write_log("\n Deleting excel file & Geocoding all VISION records",logfile)

try:
    # Delete excel file so it can be replaced
    if arcpy.Exists(MISMATCH_AIRPARCELS_VISION_REPORT):
        os.remove(MISMATCH_AIRPARCELS_VISION_REPORT)
        print (MISMATCH_AIRPARCELS_VISION_REPORT + " found - table deleted")
        write_log(MISMATCH_AIRPARCELS_VISION_REPORT + " found - table deleted", logfile)
    if arcpy.Exists(AirParcel_TaxParcel_Join):
        arcpy.management.Delete(AirParcel_TaxParcel_Join, '')
        print (AirParcel_TaxParcel_Join + " found - table deleted")
        write_log(AirParcel_TaxParcel_Join + " found - table deleted", logfile)
except:
    print ("\n Unable to delete "+MISMATCH_AIRPARCELS_VISION_REPORT+", need to delete existing FGDB manually and/or close program locking the tables")
    write_log("\n Unable to delete "+MISMATCH_AIRPARCELS_VISION_REPORT+", need to delete existing FGDB manually and/or close program locking the tables", logfile)
    logging.exception('Got exception on Unable to delete '+MISMATCH_AIRPARCELS_VISION_REPORT+', need to delete existing FGDB manually and/or close program locking the tables logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Spatial join Air Parcels to Tax Parcels - output FC is in ASMT_TEMP_FGDB
    AirParcel_TaxParcel_Join = arcpy.analysis.SpatialJoin(AIRPARCELS, TAXPARCELS, AirParcel_TaxParcel_Join, "JOIN_ONE_TO_ONE", "KEEP_ALL", r'PID "PID Number" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',PID,-1,-1,'+TAXPARCELS+',PID,-1,-1;CAMA_PIN "MBLU (Map Block Lot Unit) #" true true false 100 Text 0 0,First,#,'+AIRPARCELS+',CAMA_PIN,0,100,'+TAXPARCELS+',CAMA_PIN,0,50;Type "Type of air parcel" true true false 255 Text 0 0,First,#,'+AIRPARCELS+',Type,0,255;Elevation "Elevation (in feet)" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',Elevation,-1,-1;Building "Building designation (if needed)" true true false 255 Text 0 0,First,#,'+AIRPARCELS+',Building,0,255;Floor "Floor (if needed)" true true false 100 Text 0 0,First,#,'+AIRPARCELS+',Floor,0,100;Unit "Unit (if needed)" true true false 100 Text 0 0,First,#,'+AIRPARCELS+',Unit,0,100;Landex_URL_Choice "Landex URL (choose one)" true true false 100 Text 0 0,First,#,'+AIRPARCELS+',Landex_URL_Choice,0,100;created_user "created_user" true true false 255 Text 0 0,First,#,'+AIRPARCELS+',created_user,0,255;created_date "created_date" true true false 8 Date 0 0,First,#,'+AIRPARCELS+',created_date,-1,-1;last_edited_user "last_edited_user" true true false 255 Text 0 0,First,#,'+AIRPARCELS+',last_edited_user,0,255;last_edited_date "last_edited_date" true true false 8 Date 0 0,First,#,'+AIRPARCELS+',last_edited_date,-1,-1;REM_MNC "REM_MNC" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',REM_MNC,-1,-1;REM_PID "PID Number" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',REM_PID,-1,-1,'+TAXPARCELS+',REM_PID,-1,-1;REM_PIN "UPI Number" true true false 35 Text 0 0,First,#,'+AIRPARCELS+',REM_PIN,0,35,'+TAXPARCELS+',REM_PIN,0,35;REM_OWN_NAME "Owner Name" true true false 85 Text 0 0,First,#,'+AIRPARCELS+',REM_OWN_NAME,0,85,'+TAXPARCELS+',REM_OWN_NAME,0,85;REM_PRCL_LOCN "Parcel Location" true true false 50 Text 0 0,First,#,'+AIRPARCELS+',REM_PRCL_LOCN,0,50,'+TAXPARCELS+',REM_PRCL_LOCN,0,50;REM_PRCL_LOCN_CITY "Parcel Location City" true true false 18 Text 0 0,First,#,'+AIRPARCELS+',REM_PRCL_LOCN_CITY,0,18,'+TAXPARCELS+',REM_PRCL_LOCN_CITY,0,18;REM_PRCL_LOCN_STT "Parcel Location State" true true false 2 Text 0 0,First,#,'+AIRPARCELS+',REM_PRCL_LOCN_STT,0,2,'+TAXPARCELS+',REM_PRCL_LOCN_STT,0,2;REM_PRCL_LOCN_ZIP "Parcel Location Zipcode" true true false 12 Text 0 0,First,#,'+AIRPARCELS+',REM_PRCL_LOCN_ZIP,0,12,'+TAXPARCELS+',REM_PRCL_LOCN_ZIP,0,12;REM_ALT_PRCL_ID "Old IBM Number" true true false 35 Text 0 0,First,#,'+AIRPARCELS+',REM_ALT_PRCL_ID,0,35,'+TAXPARCELS+',REM_ALT_PRCL_ID,0,35;REM_PRCL_STATUS_DATE "Parcel Status date - CAMA Software" true true false 8 Date 0 0,First,#,'+AIRPARCELS+',REM_PRCL_STATUS_DATE,-1,-1,'+TAXPARCELS+',REM_PRCL_STATUS_DATE,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0,First,#,'+AIRPARCELS+',REM_MBLU_MAP,0,7,'+TAXPARCELS+',REM_MBLU_MAP,0,7;REM_MBLU_MAP_CUT "Map Cut - Not Used" true true false 3 Text 0 0,First,#,'+AIRPARCELS+',REM_MBLU_MAP_CUT,0,3,'+TAXPARCELS+',REM_MBLU_MAP_CUT,0,3;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0,First,#,'+AIRPARCELS+',REM_MBLU_BLOCK,0,7,'+TAXPARCELS+',REM_MBLU_BLOCK,0,7;REM_MBLU_BLOCK_CUT "Block Cut - Not Used" true true false 3 Text 0 0,First,#,'+AIRPARCELS+',REM_MBLU_BLOCK_CUT,0,3,'+TAXPARCELS+',REM_MBLU_BLOCK_CUT,0,3;REM_MBLU_LOT "Lot" true true false 7 Text 0 0,First,#,'+AIRPARCELS+',REM_MBLU_LOT,0,7,'+TAXPARCELS+',REM_MBLU_LOT,0,7;REM_MBLU_LOT_CUT "Lot Cut - Not Used" true true false 3 Text 0 0,First,#,'+AIRPARCELS+',REM_MBLU_LOT_CUT,0,3,'+TAXPARCELS+',REM_MBLU_LOT_CUT,0,3;REM_MBLU_UNIT "Unit" true true false 7 Text 0 0,First,#,'+AIRPARCELS+',REM_MBLU_UNIT,0,7,'+TAXPARCELS+',REM_MBLU_UNIT,0,7;REM_MBLU_UNIT_CUT "Unit Cut - Not Used" true true false 3 Text 0 0,First,#,'+AIRPARCELS+',REM_MBLU_UNIT_CUT,0,3,'+TAXPARCELS+',REM_MBLU_UNIT_CUT,0,3;REM_STATUS_DATE "Status Date - CAMA software" true true false 8 Date 0 0,First,#,'+AIRPARCELS+',REM_STATUS_DATE,-1,-1,'+TAXPARCELS+',REM_STATUS_DATE,-1,-1;REM_INET_SUPPRESS "Internet Suppression" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',REM_INET_SUPPRESS,-1,-1,'+TAXPARCELS+',REM_INET_SUPPRESS,-1,-1;REM_IS_CONDO_MAIN "Is Condo Main Parcel" true true false 2 Short 0 5,First,#,'+AIRPARCELS+',REM_IS_CONDO_MAIN,-1,-1,'+TAXPARCELS+',REM_IS_CONDO_MAIN,-1,-1;REM_CMPLX_NAME "Complex Name" true true false 30 Text 0 0,First,#,'+AIRPARCELS+',REM_CMPLX_NAME,0,30,'+TAXPARCELS+',REM_CMPLX_NAME,0,30;REM_BLDG_NAME "Acreage and Description" true true false 60 Text 0 0,First,#,'+AIRPARCELS+',REM_BLDG_NAME,0,60,'+TAXPARCELS+',REM_BLDG_NAME,0,60;REM_USE_CODE "Use Code" true true false 4 Text 0 0,First,#,'+AIRPARCELS+',REM_USE_CODE,0,4,'+TAXPARCELS+',REM_USE_CODE,0,4;REM_LEGAL_AREA "Legal Area" true true false 8 Double 8 38,First,#,'+AIRPARCELS+',REM_LEGAL_AREA,-1,-1,'+TAXPARCELS+',REM_LEGAL_AREA,-1,-1;REM_LAST_UPDATE "Last Update - CAMA software" true true false 8 Date 0 0,First,#,'+AIRPARCELS+',REM_LAST_UPDATE,-1,-1,'+TAXPARCELS+',REM_LAST_UPDATE,-1,-1;REM_USRFLD "6 digit PID" true true false 6 Text 0 0,First,#,'+AIRPARCELS+',REM_USRFLD,0,6,'+TAXPARCELS+',REM_USRFLD,0,6;REM_USRFLD_DESC "Control Number" true true false 40 Text 0 0,First,#,'+AIRPARCELS+',REM_USRFLD_DESC,0,40,'+TAXPARCELS+',REM_USRFLD_DESC,0,40;PID_TEXT "PID Text format" true true false 15 Text 0 0,First,#,'+AIRPARCELS+',PID_TEXT,0,15,'+TAXPARCELS+',PID_TEXT,0,15;REM_PARCEL_STATUS "Parcel Status in CAMA" true true false 1 Text 0 0,First,#,'+AIRPARCELS+',REM_PARCEL_STATUS,0,1;LND_USE_CODE "Land Use Code" true true false 4 Text 0 0,First,#,'+AIRPARCELS+',LND_USE_CODE,0,4,'+TAXPARCELS+',LND_USE_CODE,0,4;LND_USE_DESC "Land Use Description" true true false 40 Text 0 0,First,#,'+AIRPARCELS+',LND_USE_DESC,0,40,'+TAXPARCELS+',LND_USE_DESC,0,40;LND_DSTRCT "District Number" true true false 6 Text 0 0,First,#,'+AIRPARCELS+',LND_DSTRCT,0,6,'+TAXPARCELS+',LND_DSTRCT,0,6;MUNI_NAME "Municipality Name" true true false 75 Text 0 0,First,#,'+AIRPARCELS+',MUNI_NAME,0,75;PRC_PF_LOCN "School District Code" true true false 15 Text 0 0,First,#,'+AIRPARCELS+',PRC_PF_LOCN,0,15,'+TAXPARCELS+',PRC_PF_LOCN,0,15;PRC_PF_LOCN_DESC "School District" true true false 50 Text 0 0,First,#,'+AIRPARCELS+',PRC_PF_LOCN_DESC,0,50,'+TAXPARCELS+',PRC_PF_LOCN_DESC,0,50;PRC_USRFLD_09 "User Field 9 - Not Used" true true false 30 Text 0 0,First,#,'+AIRPARCELS+',PRC_USRFLD_09,0,30,'+TAXPARCELS+',PRC_USRFLD_09,0,30;PRC_USRFLD_10 "User Field 10 - Not Used" true true false 30 Text 0 0,First,#,'+AIRPARCELS+',PRC_USRFLD_10,0,30,'+TAXPARCELS+',PRC_USRFLD_10,0,30;PRC_TTL_ASSESS_BLDG "Total Building Assessment" true true false 8 Double 8 38,First,#,'+AIRPARCELS+',PRC_TTL_ASSESS_BLDG,-1,-1,'+TAXPARCELS+',PRC_TTL_ASSESS_BLDG,-1,-1;PRC_TTL_ASSESS_IMPROVEMENTS "Total Improvements Assessment" true true false 8 Double 8 38,First,#,'+AIRPARCELS+',PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1,'+TAXPARCELS+',PRC_TTL_ASSESS_IMPROVEMENTS,-1,-1;PRC_TTL_ASSESS_LND "Total Land Assessment" true true false 8 Double 8 38,First,#,'+AIRPARCELS+',PRC_TTL_ASSESS_LND,-1,-1,'+TAXPARCELS+',PRC_TTL_ASSESS_LND,-1,-1;PRC_TTL_ASSESS_OB "Total Out Building Assessment" true true false 8 Double 8 38,First,#,'+AIRPARCELS+',PRC_TTL_ASSESS_OB,-1,-1,'+TAXPARCELS+',PRC_TTL_ASSESS_OB,-1,-1;PRC_VALUE "Parcel Value" true true false 8 Double 8 38,First,#,'+AIRPARCELS+',PRC_VALUE,-1,-1,'+TAXPARCELS+',PRC_VALUE,-1,-1;PRC_CMPLX_PID "Complex PID" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',PRC_CMPLX_PID,-1,-1,'+TAXPARCELS+',PRC_CMPLX_PID,-1,-1;PRC_CMPLX_DESC "Complex Description" true true false 30 Text 0 0,First,#,'+AIRPARCELS+',PRC_CMPLX_DESC,0,30,'+TAXPARCELS+',PRC_CMPLX_DESC,0,30;PRC_CENSUS "Census - Not Used" true true false 20 Text 0 0,First,#,'+AIRPARCELS+',PRC_CENSUS,0,20,'+TAXPARCELS+',PRC_CENSUS,0,20;PRC_TTL_MRKT_ASSESS "Total Market Assessment" true true false 8 Double 8 38,First,#,'+AIRPARCELS+',PRC_TTL_MRKT_ASSESS,-1,-1,'+TAXPARCELS+',PRC_TTL_MRKT_ASSESS,-1,-1;PRC_TTL_ASSESS "Total Assessment" true true false 8 Double 8 38,First,#,'+AIRPARCELS+',PRC_TTL_ASSESS,-1,-1,'+TAXPARCELS+',PRC_TTL_ASSESS,-1,-1;OWN_ID "OWN_ID" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',OWN_ID,-1,-1,'+TAXPARCELS+',OWN_ID,-1,-1;OWN_NAME1 "OWN_NAME1" true true false 85 Text 0 0,First,#,'+AIRPARCELS+',OWN_NAME1,0,85,'+TAXPARCELS+',OWN_NAME1,0,85;OWN_NAME2 "OWN_NAME2" true true false 85 Text 0 0,First,#,'+AIRPARCELS+',OWN_NAME2,0,85,'+TAXPARCELS+',OWN_NAME2,0,85;ROW_PID "ROW_PID" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',ROW_PID,-1,-1,'+TAXPARCELS+',ROW_PID,-1,-1;ROW_OWN_ID "ROW_OWN_ID" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',ROW_OWN_ID,-1,-1;ROW_LINE_NUM "ROW_LINE_NUM" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',ROW_LINE_NUM,-1,-1;ROW_OWN_PCT "ROW_OWN_PCT" true true false 2 Short 0 5,First,#,'+AIRPARCELS+',ROW_OWN_PCT,-1,-1,'+TAXPARCELS+',ROW_OWN_PCT,-1,-1;ROW_PRIMARY "ROW_PRIMARY" true true false 2 Short 0 5,First,#,'+AIRPARCELS+',ROW_PRIMARY,-1,-1;ROW_CREATE_DATE "ROW_CREATE_DATE" true true false 8 Date 0 0,First,#,'+AIRPARCELS+',ROW_CREATE_DATE,-1,-1;ROW_MAD_ID "ROW_MAD_ID" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',ROW_MAD_ID,-1,-1;ROW_MAD_ISPRIMARY "ROW_MAD_ISPRIMARY" true true false 2 Short 0 5,First,#,'+AIRPARCELS+',ROW_MAD_ISPRIMARY,-1,-1;OWN_LINE "OWN_LINE" true true false 255 Text 0 0,First,#,'+AIRPARCELS+',OWN_LINE,0,255;MAD_MAIL_NAME1 "Tax Bill Mailing Address Name 1" true true false 85 Text 0 0,First,#,'+AIRPARCELS+',MAD_MAIL_NAME1,0,85,'+TAXPARCELS+',MAD_MAIL_NAME1,0,85;MAD_MAIL_NAME2 "Tax Bill Mailing Address Name 2" true true false 85 Text 0 0,First,#,'+AIRPARCELS+',MAD_MAIL_NAME2,0,85,'+TAXPARCELS+',MAD_MAIL_NAME2,0,85;MAD_MAIL_ADDR1 "Tax Bill Mailing Address 1" true true false 50 Text 0 0,First,#,'+AIRPARCELS+',MAD_MAIL_ADDR1,0,50,'+TAXPARCELS+',MAD_MAIL_ADDR1,0,50;MAD_MAIL_CITY "Tax Bill Mailing Address City" true true false 30 Text 0 0,First,#,'+AIRPARCELS+',MAD_MAIL_CITY,0,30,'+TAXPARCELS+',MAD_MAIL_CITY,0,30;MAD_MAIL_STATE "Tax Bill Mailing Address State" true true false 20 Text 0 0,First,#,'+AIRPARCELS+',MAD_MAIL_STATE,0,20,'+TAXPARCELS+',MAD_MAIL_STATE,0,20;MAD_MAIL_ZIP "Tax Bill Mailing Address Zipcode" true true false 20 Text 0 0,First,#,'+AIRPARCELS+',MAD_MAIL_ZIP,0,20,'+TAXPARCELS+',MAD_MAIL_ZIP,0,20;MAD_MAIL_ADDR2 "Tax Bill Mailing Address 2" true true false 50 Text 0 0,First,#,'+AIRPARCELS+',MAD_MAIL_ADDR2,0,50,'+TAXPARCELS+',MAD_MAIL_ADDR2,0,50;MAD_ID "Mailing Address VISION ID" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',MAD_ID,-1,-1;SLH_PID "Sales History PID" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',SLH_PID,-1,-1,'+TAXPARCELS+',SLH_PID,-1,-1;SLH_LINE_NUM "Sales History Line Number" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',SLH_LINE_NUM,-1,-1;SLH_SALE_DATE "Sale Date" true true false 8 Date 0 0,First,#,'+AIRPARCELS+',SLH_SALE_DATE,-1,-1,'+TAXPARCELS+',SLH_SALE_DATE,-1,-1;SLH_BOOK "Deed Book / Instrument Number" true true false 15 Text 0 0,First,#,'+AIRPARCELS+',SLH_BOOK,0,15,'+TAXPARCELS+',SLH_BOOK,0,15;SLH_PAGE "Deed Page" true true false 15 Text 0 0,First,#,'+AIRPARCELS+',SLH_PAGE,0,15,'+TAXPARCELS+',SLH_PAGE,0,15;SLH_PRICE "Sale Price" true true false 8 Double 8 38,First,#,'+AIRPARCELS+',SLH_PRICE,-1,-1,'+TAXPARCELS+',SLH_PRICE,-1,-1;SLH_CURRENT_OWNER "Sales History Current Owner Designation" true true false 2 Short 0 5,First,#,'+AIRPARCELS+',SLH_CURRENT_OWNER,-1,-1,'+TAXPARCELS+',SLH_CURRENT_OWNER,-1,-1;REM_INET_SUPPRESS_1 "Internet Suppression" true true false 4 Long 0 10,First,#,'+AIRPARCELS+',REM_INET_SUPPRESS_1,-1,-1;LANDEX_URL "Landex URL" true true false 600 Text 0 0,First,#,'+AIRPARCELS+',LANDEX_URL,0,600,'+TAXPARCELS+',LANDEX_URL,0,600;GlobalID "GlobalID" false false true 38 GlobalID 0 0,First,#,'+AIRPARCELS+',GlobalID,-1,-1,'+TAXPARCELS+',GlobalID,-1,-1;MAP "Map" true true false 50 Text 0 0,First,#,'+TAXPARCELS+',MAP,0,50;PARCEL "Parcel" true true false 50 Text 0 0,First,#,'+TAXPARCELS+',PARCEL,0,50;LOT "Lot" true true false 50 Text 0 0,First,#,'+TAXPARCELS+',LOT,0,50;PLANS_AVAILABLE "Plans Available" true true false 5 Text 0 0,First,#,'+TAXPARCELS+',PLANS_AVAILABLE,0,5;SEC_MUNI_NAME "Municipal Name" true true false 50 Text 0 0,First,#,'+TAXPARCELS+',SEC_MUNI_NAME,0,50;GIS_ACRES "GIS Calculated Acres - not legal" true true false 8 Double 8 38,First,#,'+TAXPARCELS+',GIS_ACRES,-1,-1;LONGITUDE_X "Longitude_X" true true false 8 Double 8 38,First,#,'+TAXPARCELS+',LONGITUDE_X,-1,-1;LATITUDE_Y "Latitude_Y" true true false 8 Double 8 38,First,#,'+TAXPARCELS+',LATITUDE_Y,-1,-1', "LARGEST_OVERLAP", None, '')
    print ("\n Air Parcels spatial joined to Tax Parcels")
    write_log("\n Air Parcels spatial joined to Tax Parcels" ,logfile)
except:
    print ("\n Unable to Spatial join Air Parcels to Tax Parcels")
    write_log("\n Unable to Spatial join Air Parcels to Tax Parcels", logfile)
    logging.exception('Got exception on Spatial join Air Parcels to Tax Parcels logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Add Match field to AirParcel_TaxParcel_Join
    arcpy.management.AddField(AirParcel_TaxParcel_Join, "Match", "TEXT", None, None, None, "Match?", "NULLABLE", "NON_REQUIRED", '')
    print ("\n Match field added to AirParcel_TaxParcel_Join")
    write_log ("\n Match field added to AirParcel_TaxParcel_Join", logfile)
except:
    print ("\n Unable to add Match field added to AirParcel_TaxParcel_Join")
    write_log("\n Unable to add Match field added to AirParcel_TaxParcel_Join", logfile)
    logging.exception('Got exception on add Match field added to AirParcel_TaxParcel_Join logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Field calc value is Air Parcel & Tax Parcel BLOCK fields match or not
    arcpy.management.CalculateField(AirParcel_TaxParcel_Join, "Match", "calc(!REM_MBLU_BLOCK!,!PARCEL!)", "PYTHON3", """def calc(REM_MBLU_BLOCK, PARCEL):
    if REM_MBLU_BLOCK == PARCEL :
        return 'Yes'
    else:
        return 'No'""", "TEXT", "NO_ENFORCE_DOMAINS")
    print ("\n   Field calculated value is Air Parcel & Tax Parcel BLOCK fields match or not")
    write_log ("\n   Field calculated value is Air Parcel & Tax Parcel BLOCK fields match or not", logfile)
except:
    print ("\n Unable to Field calc value is Air Parcel & Tax Parcel BLOCK fields match or not")
    write_log("\n Unable to Field calc value is Air Parcel & Tax Parcel BLOCK fields match or not", logfile)
    logging.exception('Got exception on Field calc value is Air Parcel & Tax Parcel BLOCK fields match or not logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make temp table view - selecting only unmatched records
    Unmatched_AirParcel_View = arcpy.management.MakeTableView(AirParcel_TaxParcel_Join, "Unmatched_AirParcel_View", "Match = 'No'", None, "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Join_Count Join_Count VISIBLE NONE;TARGET_FID TARGET_FID VISIBLE NONE;PID PID VISIBLE NONE;CAMA_PIN CAMA_PIN VISIBLE NONE;Type Type VISIBLE NONE;Elevation Elevation VISIBLE NONE;Building Building VISIBLE NONE;Floor Floor VISIBLE NONE;Unit Unit VISIBLE NONE;Landex_URL_Choice Landex_URL_Choice VISIBLE NONE;created_user created_user VISIBLE NONE;created_date created_date VISIBLE NONE;last_edited_user last_edited_user VISIBLE NONE;last_edited_date last_edited_date VISIBLE NONE;REM_MNC REM_MNC VISIBLE NONE;REM_PID REM_PID VISIBLE NONE;REM_PIN REM_PIN VISIBLE NONE;REM_OWN_NAME REM_OWN_NAME VISIBLE NONE;REM_PRCL_LOCN REM_PRCL_LOCN VISIBLE NONE;REM_PRCL_LOCN_CITY REM_PRCL_LOCN_CITY VISIBLE NONE;REM_PRCL_LOCN_STT REM_PRCL_LOCN_STT VISIBLE NONE;REM_PRCL_LOCN_ZIP REM_PRCL_LOCN_ZIP VISIBLE NONE;REM_ALT_PRCL_ID REM_ALT_PRCL_ID VISIBLE NONE;REM_PRCL_STATUS_DATE REM_PRCL_STATUS_DATE VISIBLE NONE;REM_MBLU_MAP REM_MBLU_MAP VISIBLE NONE;REM_MBLU_MAP_CUT REM_MBLU_MAP_CUT VISIBLE NONE;REM_MBLU_BLOCK REM_MBLU_BLOCK VISIBLE NONE;REM_MBLU_BLOCK_CUT REM_MBLU_BLOCK_CUT VISIBLE NONE;REM_MBLU_LOT REM_MBLU_LOT VISIBLE NONE;REM_MBLU_LOT_CUT REM_MBLU_LOT_CUT VISIBLE NONE;REM_MBLU_UNIT REM_MBLU_UNIT VISIBLE NONE;REM_MBLU_UNIT_CUT REM_MBLU_UNIT_CUT VISIBLE NONE;REM_STATUS_DATE REM_STATUS_DATE VISIBLE NONE;REM_INET_SUPPRESS REM_INET_SUPPRESS VISIBLE NONE;REM_IS_CONDO_MAIN REM_IS_CONDO_MAIN VISIBLE NONE;REM_CMPLX_NAME REM_CMPLX_NAME VISIBLE NONE;REM_BLDG_NAME REM_BLDG_NAME VISIBLE NONE;REM_USE_CODE REM_USE_CODE VISIBLE NONE;REM_LEGAL_AREA REM_LEGAL_AREA VISIBLE NONE;REM_LAST_UPDATE REM_LAST_UPDATE VISIBLE NONE;REM_USRFLD REM_USRFLD VISIBLE NONE;REM_USRFLD_DESC REM_USRFLD_DESC VISIBLE NONE;PID_TEXT PID_TEXT VISIBLE NONE;REM_PARCEL_STATUS REM_PARCEL_STATUS VISIBLE NONE;LND_USE_CODE LND_USE_CODE VISIBLE NONE;LND_USE_DESC LND_USE_DESC VISIBLE NONE;LND_DSTRCT LND_DSTRCT VISIBLE NONE;MUNI_NAME MUNI_NAME VISIBLE NONE;PRC_PF_LOCN PRC_PF_LOCN VISIBLE NONE;PRC_PF_LOCN_DESC PRC_PF_LOCN_DESC VISIBLE NONE;PRC_USRFLD_09 PRC_USRFLD_09 VISIBLE NONE;PRC_USRFLD_10 PRC_USRFLD_10 VISIBLE NONE;PRC_TTL_ASSESS_BLDG PRC_TTL_ASSESS_BLDG VISIBLE NONE;PRC_TTL_ASSESS_IMPROVEMENTS PRC_TTL_ASSESS_IMPROVEMENTS VISIBLE NONE;PRC_TTL_ASSESS_LND PRC_TTL_ASSESS_LND VISIBLE NONE;PRC_TTL_ASSESS_OB PRC_TTL_ASSESS_OB VISIBLE NONE;PRC_VALUE PRC_VALUE VISIBLE NONE;PRC_CMPLX_PID PRC_CMPLX_PID VISIBLE NONE;PRC_CMPLX_DESC PRC_CMPLX_DESC VISIBLE NONE;PRC_CENSUS PRC_CENSUS VISIBLE NONE;PRC_TTL_MRKT_ASSESS PRC_TTL_MRKT_ASSESS VISIBLE NONE;PRC_TTL_ASSESS PRC_TTL_ASSESS VISIBLE NONE;OWN_ID OWN_ID VISIBLE NONE;OWN_NAME1 OWN_NAME1 VISIBLE NONE;OWN_NAME2 OWN_NAME2 VISIBLE NONE;ROW_PID ROW_PID VISIBLE NONE;ROW_OWN_ID ROW_OWN_ID VISIBLE NONE;ROW_LINE_NUM ROW_LINE_NUM VISIBLE NONE;ROW_OWN_PCT ROW_OWN_PCT VISIBLE NONE;ROW_PRIMARY ROW_PRIMARY VISIBLE NONE;ROW_CREATE_DATE ROW_CREATE_DATE VISIBLE NONE;ROW_MAD_ID ROW_MAD_ID VISIBLE NONE;ROW_MAD_ISPRIMARY ROW_MAD_ISPRIMARY VISIBLE NONE;OWN_LINE OWN_LINE VISIBLE NONE;MAD_MAIL_NAME1 MAD_MAIL_NAME1 VISIBLE NONE;MAD_MAIL_NAME2 MAD_MAIL_NAME2 VISIBLE NONE;MAD_MAIL_ADDR1 MAD_MAIL_ADDR1 VISIBLE NONE;MAD_MAIL_CITY MAD_MAIL_CITY VISIBLE NONE;MAD_MAIL_STATE MAD_MAIL_STATE VISIBLE NONE;MAD_MAIL_ZIP MAD_MAIL_ZIP VISIBLE NONE;MAD_MAIL_ADDR2 MAD_MAIL_ADDR2 VISIBLE NONE;MAD_ID MAD_ID VISIBLE NONE;SLH_PID SLH_PID VISIBLE NONE;SLH_LINE_NUM SLH_LINE_NUM VISIBLE NONE;SLH_SALE_DATE SLH_SALE_DATE VISIBLE NONE;SLH_BOOK SLH_BOOK VISIBLE NONE;SLH_PAGE SLH_PAGE VISIBLE NONE;SLH_PRICE SLH_PRICE VISIBLE NONE;SLH_CURRENT_OWNER SLH_CURRENT_OWNER VISIBLE NONE;REM_INET_SUPPRESS_1 REM_INET_SUPPRESS_1 VISIBLE NONE;LANDEX_URL LANDEX_URL VISIBLE NONE;MAP MAP VISIBLE NONE;PARCEL PARCEL VISIBLE NONE;LOT LOT VISIBLE NONE;PLANS_AVAILABLE PLANS_AVAILABLE VISIBLE NONE;SEC_MUNI_NAME SEC_MUNI_NAME VISIBLE NONE;GIS_ACRES GIS_ACRES VISIBLE NONE;LONGITUDE_X LONGITUDE_X VISIBLE NONE;LATITUDE_Y LATITUDE_Y VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;Match Match VISIBLE NONE")
    print ("\n Make temp table view - selecting only unmatched records completed")
    write_log ("\n Make temp table view - selecting only unmatched records completed", logfile)
except:
    print ("\n Unable to Make temp table view - selecting only unmatched records")
    write_log("\n Unable to Make temp table view - selecting only unmatched records", logfile)
    logging.exception('Got exception on Make temp table view - selecting only unmatched records logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Export unmatched records to excel
    arcpy.conversion.TableToExcel(Unmatched_AirParcel_View, MISMATCH_AIRPARCELS_VISION_REPORT, "ALIAS", "CODE")
    print ("\n Exporting mismatched records report to: "+ASMT_REPORT_FLDR) 
    write_log("\n Exporting mismatched records report to: "+ASMT_REPORT_FLDR, logfile)
except:
    print ("\n Unable to Export mismatched records to excel")
    write_log("\n Unable to Export mismatched records to excel", logfile)
    logging.exception('Got exception on Export mismatched records to excel logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("         Exporting update table to excel file at "+ASMT_REPORT_FLDR+" completed")
write_log("         Exporting update table to excel file at "+ASMT_REPORT_FLDR+" completed", logfile)

try:
    # Clear Unmatched_AirParcel_View temp table
    arcpy.Delete_management(Unmatched_AirParcel_View)
except:
    print ("\n Unable to clear Unmatched_AirParcel_View temp table")
    write_log("Unable to clear Unmatched_AirParcel_View temp table", logfile)
    logging.exception('Got exception on clear Unmatched_AirParcel_View temp table logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()


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
