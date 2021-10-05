# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# PS_Survey_Report.py
# Created on: 2019-07-01 
# Updated on 2021-09-21
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Report any new surveys that haven't been acknoledged via the data.
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
logfile = r"R:\\GIS\\GIS_LOGS\\911\\PS_SurveyReport.log"  
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
AGOL_EDIT_PUB_PS = Database_Connections + "\\agol_edit_pub@ccsde.sde"
PS_Report_Fldr = r"R:\\GIS\\Public Safety\\Reports"

# Local variables:
NEW_ADDR_REQUESTS = AGOL_EDIT_PUB_PS + "\\CCSDE.AGOL_EDIT_PUB.ADDRESS_NEW_REQUESTS_AGOL_EDIT_PUB"
BUSINESS_DIRECTORY = AGOL_EDIT_PUB_PS + "\\CCSDE.AGOL_EDIT_PUB.BUSINESS_DIRECTORY_AGOL_EDIT_PUB"
BusinessDirectory_Excel = PS_Report_Fldr + "\\Business_Directory.xls"

start_time = time.time()

print ("============================================================================")
print ("Begining Public Safety Survey reports run: "+ str(Day) + " " + str(Time))
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Begining Public Safety Survey reports run: "+ str(Day) + " " + str(Time), logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

try:
    # Clean up BusinessDirectory_Excel by deleting it (to stop excel sheets from filling up the folder, it will delete the old report before running a new one)
    if arcpy.Exists(BusinessDirectory_Excel):
        os.remove(BusinessDirectory_Excel)
        print (BusinessDirectory_Excel + " found - table deleted")
        write_log(BusinessDirectory_Excel + " found - table deleted", logfile)
except:
    print ("\n Unable to delete Excel_reports, need to delete existing excel file manually and/or close program locking the file")
    write_log("\n Unable to delete Excel_reports, need to delete existing excel file manually and/or close program locking the file", logfile)
    logging.exception('Got exception on delete Excel_reports logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make temp table from Business Directory FC in PublicSafety_TempFGDB (make a temporary table in memory to save space on the drive and the trouble of deleting it later, selection only the records that have the field CAD_UPDATED set to N)
    BusinessDirectory_TBL = arcpy.MakeTableView_management(BUSINESS_DIRECTORY, "BusinessDirectory_TBL", "CAD_UPDATED = 'N'", "", "CREATED_DATE CREATED_DATE VISIBLE NONE;EDIT_DATE EDIT_DATE VISIBLE NONE;BUSINESS_NAME BUSINESS_NAME VISIBLE NONE;STREET_ADDRESS STREET_ADDRESS VISIBLE NONE;POST_OFFICE POST_OFFICE VISIBLE NONE;STATE STATE VISIBLE NONE;ZIPCODE ZIPCODE VISIBLE NONE;MUNICIPALITY MUNICIPALITY VISIBLE NONE;PHONE_NUMBER PHONE_NUMBER VISIBLE NONE;WEBSITE WEBSITE VISIBLE NONE;HOURS_OF_OPERATION HOURS_OF_OPERATION VISIBLE NONE;CONTACT_NAME CONTACT_NAME VISIBLE NONE;CONTACT_PHONE_NUMBER CONTACT_PHONE_NUMBER VISIBLE NONE;CAD_UPDATED CAD_UPDATED VISIBLE NONE;GIS_UPDATED GIS_UPDATED VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;GlobalID GlobalID VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;NEW_UPDATE NEW_UPDATE VISIBLE NONE;COMMENTS COMMENTS VISIBLE NONE;CONTACT_NAME_2 CONTACT_NAME_2 VISIBLE NONE;CONTACT_PHONE_2 CONTACT_PHONE_2 VISIBLE NONE;CONTACT_NAME_3 CONTACT_NAME_3 VISIBLE NONE;CONTACT_PHONE_3 CONTACT_PHONE_3 VISIBLE NONE;FAX_NUMBER FAX_NUMBER VISIBLE NONE")
except:
    print ("\n Unable to make table view from Business Directory FC")
    write_log("\n Unable to make table view from Business Directory FC", logfile)
    logging.exception('Got exception on make table view from Business Directory FC logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Export table to excel (export temporary table out as excel workbook)
    BusinessDirectory_Excel = arcpy.TableToExcel_conversion(BusinessDirectory_TBL, "R:/GIS/Public Safety/Reports/Business_Directory.xls", "ALIAS", "DESCRIPTION")
    print ("\n   Table exported out as R:/GIS/Public Safety/Reports/Business_Directory.xls")
    write_log("\n   Table exported out as R:/GIS/Public Safety/Reports/Business_Directory.xls",logfile)
except:
    print ("\n Unable to export Business Directory table to excel in R:/GIS/Public Safety/Reports folder")
    write_log("\n Unable to export Business Directory table to excel in R:/GIS/Public Safety/Reports folder", logfile)
    logging.exception('Got exception on export Business Directory table to excel in R:/GIS/Public Safety/Reports folder logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

Table_Views = [BusinessDirectory_TBL]

try:
    # Delete views and temp files used in process (deletes temporary files from workspace)
    for Views in Table_Views:
        delete_input = Views
        arcpy.Delete_management(delete_input, "")
    print ("\n   Table_Views deleted...")
    write_log("\n   Table_Views deleted...",logfile)
except:
    print ("\n Unable to delete Table_Views")
    write_log("\n Unable to delete Table_Views", logfile)
    logging.exception('Got exception on delete Table_Views logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n Public Safety Survey reports COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n Public Safety Survey reports COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
