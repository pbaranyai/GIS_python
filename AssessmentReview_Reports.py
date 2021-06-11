# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# AssessmentReview_Reports.py
# Created on: 2019-08-21 
# Updated on 2019-08-21
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
import __builtin__

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\Assessment\\AssessmentReview_Reports.log"  
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
AGOL_EDIT_PUB_ASMT = "Database Connections\\agol_edit_pub@ccsde.sde\\CCSDE.AGOL_EDIT_PUB.Assessment"
ASMT_REPORT_FLDR = r"R:\\GIS\\Assessment\\Reports"

# Local variables:
NEW_ASMT_REVIEW_REQUESTS = AGOL_EDIT_PUB_ASMT + "\\CCSDE.AGOL_EDIT_PUB.PUBLIC_ASSESSMENT_REVIEW_REQUEST_AGOL_EDIT"
Asmt_Review_Excel = ASMT_REPORT_FLDR + "\\Assessment_Review_requests.xls"
ASMT_TEMP_FGDB = ASMT_REPORT_FLDR + "\\ASMT_TempFGDB.gdb"
Asmt_Review_Excel = "R:/GIS/Assessment/Reports/Assessment_Review_requests.xls"

start_time = time.time()

print ("============================================================================")
print ("Begining Assessment request report run: "+ str(Day) + " " + str(Time))
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Begining Assessment request report run: "+ str(Day) + " " + str(Time), logfile)
write_log("============================================================================", logfile)

try:
    # Clean up temp files by deleting them (to stop excel sheets from filling up the folder, it will delete the old report before running a new one)
    if arcpy.Exists(Asmt_Review_Excel):
        os.remove(Asmt_Review_Excel)
        print (Asmt_Review_Excel + " found - table deleted")
        write_log(Asmt_Review_Excel + " found - table deleted", logfile)
except:
    print ("\n Unable to delete Assessment Review excel sheets, need to delete existing excel file manually and/or close program locking the file")
    write_log("\n Unable to delete Assessment Review excel sheets, need to delete existing excel file manually and/or close program locking the file", logfile)
    logging.exception('Got exception on delete Assessment Review excel sheets logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make temp table from NEW_ASMT_REVIEW_REQUESTS FC make a temporary table in memory to save space on the drive and the trouble of deleting it later, selection only the records that have the field FIELD_WORK_COMPLETED set to N)
    ASMT_REVIEW_REQUEST_TBL = arcpy.MakeTableView_management(NEW_ASMT_REVIEW_REQUESTS, "ASMT_REVIEW_REQUEST_TBL", "BUILDING_PERMIT_CAMA_COMPLETED = 'N'", "", "REQUEST_SUBMIT_DATE REQUEST_SUBMIT_DATE VISIBLE NONE;SUBMITTING_ENTITY SUBMITTING_ENTITY VISIBLE NONE;BUILDING_PERMIT_QUESTION BUILDING_PERMIT_QUESTION VISIBLE NONE;CONTACT_NAME CONTACT_NAME VISIBLE NONE;CONTACT_PHONE CONTACT_PHONE VISIBLE NONE;CONTACT_EMAIL CONTACT_EMAIL VISIBLE NONE;MUNICIPALITY MUNICIPALITY VISIBLE NONE;LOCATION_ADDRESS_TYPED LOCATION_ADDRESS_TYPED VISIBLE NONE;PARCEL_NUMBER PARCEL_NUMBER VISIBLE NONE;REVIEW_PURPOSE REVIEW_PURPOSE VISIBLE NONE;PROPERTY_OWNER_Y_N PROPERTY_OWNER_Y_N VISIBLE NONE;GENERAL_COMMENTS GENERAL_COMMENTS VISIBLE NONE;DEMO_COMPLETION_DATE DEMO_COMPLETION_DATE VISIBLE NONE;CONSTRUCTION_TYPE CONSTRUCTION_TYPE VISIBLE NONE;BUILDING_PERMIT_PID BUILDING_PERMIT_PID VISIBLE NONE;BUILDIING_PERMIT_MBLU BUILDIING_PERMIT_MBLU VISIBLE NONE;BUILDING_PERMIT_DATE BUILDING_PERMIT_DATE VISIBLE NONE;BUILDING_PERMIT_TYPE BUILDING_PERMIT_TYPE VISIBLE NONE;BUILDING_PERMIT_SIZE BUILDING_PERMIT_SIZE VISIBLE NONE;BUILDING_PERMIT_EST_COMPLETE_DA BUILDING_PERMIT_EST_COMPLETE_DA VISIBLE NONE;BUILDING_PERMIT_CONSTRUCTION_CO BUILDING_PERMIT_CONSTRUCTION_CO VISIBLE NONE;BUILDING_PERMIT_CAMA_COMPLETED BUILDING_PERMIT_CAMA_COMPLETED VISIBLE NONE;FIELD_WORK_COMPLETED FIELD_WORK_COMPLETED VISIBLE NONE;UPDATED_DATE UPDATED_DATE VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;GlobalID GlobalID VISIBLE NONE;REVIEW_PURPOSE_CITIZEN REVIEW_PURPOSE_CITIZEN VISIBLE NONE;COMMERCIAL_CONST_COMMENTS COMMERCIAL_CONST_COMMENTS VISIBLE NONE;DEMOLITION_COMMENTS DEMOLITION_COMMENTS VISIBLE NONE;COMMERCL_CONST_COMPLETE_DATE COMMERCL_CONST_COMPLETE_DATE VISIBLE NONE;RESIDENT_CONST_COMPLETE_DATE RESIDENT_CONST_COMPLETE_DATE VISIBLE NONE;RESIDENT_CONST_OTHER RESIDENT_CONST_OTHER VISIBLE NONE;RESIDENT_CONST_TYPE RESIDENT_CONST_TYPE VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE")
    print("\n Temp table of New Assessment Review Requests survey results created in memory...")
    write_log("\n Temp table of New Assessment Review Requests survey results created in memory...",logfile)
except:
    print ("\n Unable to make assessment review table view from NEW_ASMT_REVIEW_REQUESTS FC")
    write_log("\n Unable to make assessment review table view from NEW_ASMT_REVIEW_REQUESTS FC", logfile)
    logging.exception('Got exception on make assessment review table view from NEW_ASMT_REVIEW_REQUESTS FC logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Export ASMT_REVIEW_REQUEST_TBL table to excel (export temporary table out as excel workbook)
    Asmt_Review_Excel = arcpy.TableToExcel_conversion(ASMT_REVIEW_REQUEST_TBL, Asmt_Review_Excel, "ALIAS", "DESCRIPTION")
    print ("\n   Table exported out as R:/GIS/Assessment/AssessmentReview_Reports/Assessment_Review_requests.xls")
    write_log("\n   Table exported out as R:/GIS/Assessment/AssessmentReview_Reports/Assessment_Review_requests.xls",logfile)
except:
    print ("\n Unable to export table to excel in R:/GIS/Assessment/AssessmentReview_Reports folder")
    write_log("\n Unable to export table to excel in R:/GIS/Assessment/AssessmentReview_Reports folder", logfile)
    logging.exception('Got exception on export table to excel in R:/GIS/Assessment/AssessmentReview_Reports folder logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n NEW ASSESSMENT REVIEW REQUEST REPORT COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n NEW ASSESSMENT REVIEW REQUEST REPORT COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
