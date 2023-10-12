# ---------------------------------------------------------------------------
# New_address_report.py
# Created on: 2019-07-01 
# Updated on 2019-07-01
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Report any new address requests between user chosen start date and current date.
#
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import datetime
import os
import logging

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\911\\New_address_report.log"  
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
AGOL_EDIT_PUB_PS = "Database Connections\\agol_edit_pub@ccsde.sde"
PS_Report_Fldr = r"\\FILELOCATION\\GIS\\Public Safety\\Reports"

# Local variables:
NEW_ADDR_REQUESTS = AGOL_EDIT_PUB_PS + "\\CCSDE.AGOL_EDIT_PUB.ADDRESS_NEW_REQUESTS_AGOL_EDIT_PUB"
Address_Excel = PS_Report_Fldr + "\\New_address_requests.xls"
PS_TEMP_FGDB = PS_Report_Fldr + "\\PublicSafety_TempFGDB.gdb"

start_time = time.time()

print ("============================================================================")
print ("Begining new address request report run: "+ str(Day) + " " + str(Time))
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Begining new address request report run: "+ str(Day) + " " + str(Time), logfile)
write_log("============================================================================", logfile)

try:
    # Clean up temp files by deleting them (to stop excel sheets from filling up the folder, it will delete the old report before running a new one)
    if arcpy.Exists(Address_Excel):
        os.remove(Address_Excel)
        print (Address_Excel + " found - table deleted")
        write_log(Address_Excel + " found - table deleted", logfile)
except:
    print ("\n Unable to delete Total_Assessment_Reconcile_Report.xls, need to delete existing excel file manually and/or close program locking the file")
    write_log("\n Unable to delete Total_Assessment_Reconcile_Report.xls, need to delete existing excel file manually and/or close program locking the file", logfile)
    logging.exception('Got exception on delete Total_Assessment_Reconcile_Report.xls logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make temp table from NEW_ADDR_REQUESTS FC in PublicSafety_TempFGDB (make a temporary table in memory to save space on the drive and the trouble of deleting it later, selection only the records that have the field AD_REQUEST_ADDRESSED set to N)
    New_Address_Request_TBL = arcpy.MakeTableView_management(NEW_ADDR_REQUESTS, "New_Address_Request_TBL", "AD_REQUEST_ADDRESSED = 'N'", "", "AD_LAST_NAME AD_LAST_NAME VISIBLE NONE;AD_FIRST_NAME AD_FIRST_NAME VISIBLE NONE;AD_MAIL_ADDRESS AD_MAIL_ADDRESS VISIBLE NONE;AD_MAIL_CITY AD_MAIL_CITY VISIBLE NONE;AD_MAIL_ZIP AD_MAIL_ZIP VISIBLE NONE;AD_MUNI AD_MUNI VISIBLE NONE;AD_EMAIL AD_EMAIL VISIBLE NONE;AD_STREET_ACCESS AD_STREET_ACCESS VISIBLE NONE;AD_RES_UNITS AD_RES_UNITS VISIBLE NONE;AD_COM_UNITS AD_COM_UNITS VISIBLE NONE;AD_REQUEST_DATE AD_REQUEST_DATE VISIBLE NONE;AD_REQUEST_ADDRESSED AD_REQUEST_ADDRESSED VISIBLE NONE;NOTES NOTES VISIBLE NONE;AD_TYPE AD_TYPE VISIBLE NONE;AD_MAIL_STATE AD_MAIL_STATE VISIBLE NONE;AD_REQUEST_EDIT AD_REQUEST_EDIT VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;GlobalID GlobalID VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;PHONE_NUMBER PHONE_NUMBER VISIBLE NONE")
except:
    print ("\n Unable to make table view from NEW_ADDR_REQUESTS FC")
    write_log("\n Unable to make table view from NEW_ADDR_REQUESTS FC", logfile)
    logging.exception('Got exception on make table view from NEW_ADDR_REQUESTS FC logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Export table to excel (export temporary table out as excel workbook)
    Address_Excel = arcpy.TableToExcel_conversion(New_Address_Request_TBL, "R:/GIS/Public Safety/Reports/New_address_requests.xls", "ALIAS", "CODE")
    print ("\n   Table exported out as "+Address_Excel)
    write_log("\n   Table exported out as "+Address_Excel,logfile)
except:
    print ("\n Unable to export table to excel in "+PS_Report_Fldr+" folder")
    write_log("\n Unable to export table to excel in "+PS_Report_Fldr+" folder", logfile)
    logging.exception('Got exception on export table to excel in "+PS_Report_Fldr+" folder logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n NEW ADDRESS REQUEST REPORT COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n NEW ADDRESS REQUEST REPORT COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
