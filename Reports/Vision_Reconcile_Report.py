# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Vision_Reconcile_Report.py
# Created on: 2019-06-20
# Updated on 2021-09-21
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
#
# Description: 
#  Extract PID, CAMA_PIN, and PRC_TTL_ASSESS fields from current VISION_OTHER_TBL in AUTO_WORKSPACE DB connection, then join PRC_TTL_ASSESS from VISION.REAL_PROP.PARCEL table,
#   finally calculate difference between assessment values, eliminate zero values, then export to R:\GIS\Assessment as excel file
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
logfile = r"R:\\GIS\\GIS_LOGS\\Assessment\\Vision_Reconcile_Report.log"  
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
VISION_VIEW = Database_Connections + "\\Vision_Database.sde"
ASMT_REPORT_FLDR = r"\\CCFILE\\anybody\\GIS\\Assessment\\Reports"

# Local variables:
PARCEL_VISION = VISION_VIEW + "\\VISION.REAL_PROP.PARCEL"
ASMT_REPORT= ASMT_REPORT_FLDR + "\\Total_Assessment_Reconcile_Report.xls"
ASMT_RECONCILE_TBL = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_TTLASSMT_RECONCILE_TBL"
ASMT_TEMP_FGDB = ASMT_REPORT_FLDR + "\\Assessment_Report_TempFGDB.gdb"


# Local variables - tables:
VISION_OTHER_TBL_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VISION_OTHER_TBL"

start_time = time.time()

print ("============================================================================")
print ("Creating Total Assessment Reconcile Report: "+ str(Day) + " " + str(Time))
print ("Located at: R:\GIS\Assessment\Assmt_Reconcile_Report")
print ("Works in ArcGIS Pro")
print ("============================================================================")
write_log("============================================================================", logfile)
write_log("Creating Total Assessment Reconcile Report: "+ str(Day) + " " + str(Time), logfile)
write_log("Located at: R:\GIS\Assessment\Assmt_Reconcile_Report", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Updating ASMT_RECONCILE_TBL in AUTOWORKSPACE")
write_log("\n Updating ASMT_RECONCILE_TBL in AUTOWORKSPACE",logfile)

try:
    # Delete rows from ASMT_RECONCILE_TBL in AUTOWORKSPACE (prep existing table, by cleaning out rows)
    arcpy.DeleteRows_management(ASMT_RECONCILE_TBL)
except:
    print ("\n Unable to delete rows from ASMT_RECONCILE_TBL")
    write_log("\n Unable to delete rows from ASMT_RECONCILE_TBL", logfile)
    logging.exception('Got exception on delete rows from ASMT_RECONCILE_TBL logged at:' + str(Day) + " " + str(Time))
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
    ASMT_TEMP_FGDB = arcpy.CreateFileGDB_management(ASMT_REPORT_FLDR, "Assessment_Report_TempFGDB", "CURRENT")
except:
    print ("\n Unable to create new Assessment_Report_TempFGDB.gdb, need to close program locking the FGDB workspace")
    write_log("Unable to create new Assessment_Report_TempFGDB.gdb, need to close program locking the FGDB workspace", logfile)
    logging.exception('Got exception on create Assessment_Report_TempFGDB.gdb logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make temp table of VISION_VIEW in ASMT_TEMP_FGDB (export REAL_PROP.PARCEL table to temp FGDB for manipulation in steps below, only PID and TTL_ASSESS fields)
    VISION_PARCEL_TBL_TEMP = arcpy.TableToTable_conversion(PARCEL_VISION, ASMT_TEMP_FGDB, "PARCEL_TBL_TEMP", "", 'PRC_PID "PRC_PID" false false false 4 Long 0 9 ,First,#,'+PARCEL_VISION+',PRC_PID,-1,-1;PRC_TTL_15 "PRC_TTL_15" false true false 8 Double 0 12 ,First,#,'+PARCEL_VISION+',PRC_TTL_ASSESS,-1,-1;PRC_COST_D "PRC_COST_D" false true false 8 Date 0 0 ,First,#,'+PARCEL_VISION+',PRC_COST_DATE,-1,-1', "")
    print ("  ASMT_RECONCILE_TBL cleared, joining most current Assessment values...")
    write_log("  ASMT_RECONCILE_TBL cleared, joining most current Assessment values...",logfile)
except:
    print ("\n Unable to make temp table of VISION_VIEW in ASMT_TEMP_FGDB")
    write_log("\n Unable to make temp table of VISION_VIEW in ASMT_TEMP_FGDB", logfile)
    logging.exception('Got exception on make temp table of VISION_VIEW in ASMT_TEMP_FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Join PRC_TTL_ASSESS field from PARCEL_VISION to VISION_OTHER_TBL (join VISION OTHER table to temp PARCEL table from above) 
    arcpy.JoinField_management(VISION_PARCEL_TBL_TEMP, "PRC_PID", VISION_OTHER_TBL_SDE, "REM_PID", "REM_PRCL_STATUS_DATE;REM_MBLU_MAP;REM_MBLU_BLOCK;REM_MBLU_LOT;PRC_TTL_ASSESS")
    print ("   PRC_TTL_ASSESS field joined to ASMT_RECONCILE_TBL_VIEW, appending to ASMT_RECONCILE_TBL...")
    write_log("   PRC_TTL_ASSESS field joined to ASMT_RECONCILE_TBL_VIEW, appending to ASMT_RECONCILE_TBL...",logfile)
except:
    print ("\n Unable to join PRC_TTL_ASSESS field from PARCEL_VISION to VISION_OTHER_TBL_VIEW")
    write_log("\n Unable to join PRC_TTL_ASSESS field from PARCEL_VISION to VISION_OTHER_TBL_VIEW", logfile)
    logging.exception('Got exception on join PRC_TTL_ASSESS field from PARCEL_VISION to VISION_OTHER_TBL_VIEW logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append VISION_OTHER_TBL_VIEW to ASMT_RECONCILE_TBL (append tables joined above to ASMT_RECONCILE_TBL in AUTOWORKSPACE)
    arcpy.management.Append(VISION_PARCEL_TBL_TEMP,ASMT_RECONCILE_TBL, "NO_TEST", r'REM_PID "PID - Control #" true false false 4 Long 0 10,First,#,R:\\GIS\\Assessment\\Reports\\Assessment_Report_TempFGDB.gdb\\PARCEL_TBL_TEMP,PRC_PID,-1,-1;REM_MBLU_MAP "Map" true true false 7 Text 0 0,First,#,R:\\GIS\\Assessment\\Reports\\Assessment_Report_TempFGDB.gdb\\PARCEL_TBL_TEMP,REM_MBLU_MAP,0,7;REM_MBLU_BLOCK "Block" true true false 7 Text 0 0,First,#,R:\\GIS\\Assessment\\Reports\\Assessment_Report_TempFGDB.gdb\\PARCEL_TBL_TEMP,REM_MBLU_BLOCK,0,7;REM_MBLU_LOT "Lot" true true false 7 Text 0 0,First,#,R:\\GIS\\Assessment\\Reports\\Assessment_Report_TempFGDB.gdb\\PARCEL_TBL_TEMP,REM_MBLU_LOT,0,7;WEEKLY_ASSESSMENT_TOTAL "Weekly Assessment Total" true true false 8 Double 8 38,First,#,R:\\GIS\\Assessment\\Reports\\Assessment_Report_TempFGDB.gdb\\PARCEL_TBL_TEMP,PRC_TTL_ASSESS,-1,-1;WEEKLY_ASSESSMENT_DATE "Weekly Assessment Date" true true false 8 Date 0 0,First,#,R:\\GIS\\Assessment\\Reports\\Assessment_Report_TempFGDB.gdb\\PARCEL_TBL_TEMP,REM_PRCL_STATUS_DATE,-1,-1;CURRENT_ASSESSMENT_TOTAL "Current Assessment Total" true true false 8 Double 8 38,First,#,R:\\GIS\\Assessment\\Reports\\Assessment_Report_TempFGDB.gdb\\PARCEL_TBL_TEMP,PRC_TTL_15,-1,-1;CURRENT_ASSESSMENT_DATE "Current Assessment Date" true true false 8 Date 0 0,First,#,R:\\GIS\\Assessment\\Reports\\Assessment_Report_TempFGDB.gdb\\PARCEL_TBL_TEMP,PRC_COST_D,-1,-1;TOTAL_ASSESSMENT_DIFFERENCE "Total Assessment Difference" true true false 8 Double 8 38,First,#', '', "")#"PRC_COST_D = CURRENT_DATE()")
    print ("VISION_PARCEL_TBL_TEMP appended to ASMT_RECONCILE_TBL")
except:
    print ("\n Unable to append VISION_OTHER_TBL_VIEW to ASMT_RECONCILE_TBL")
    write_log("\n Unable to append VISION_OTHER_TBL_VIEW to ASMT_RECONCILE_TBL", logfile)
    logging.exception('Got exception on append VISION_OTHER_TBL_VIEW to ASMT_RECONCILE_TBL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("         Updating ASMT_RECONCILE_TBL in AUTOWORKSPACE completed")
write_log("         Updating ASMT_RECONCILE_TBL in AUTOWORKSPACE completed", logfile)

print ("\n Calculating TOTAL_ASSESSMENT_DIFFERENCE field in ASMT_RECONCILE_TBL in AUTOWORKSPACE, then removing records with zero or null value in that field")
write_log("\n Calculating TOTAL_ASSESSMENT_DIFFERENCE field in ASMT_RECONCILE_TBL in AUTOWORKSPACE, then removing records with zero or null value in that field",logfile)

try:
    # Remove any records not changed "today" (date of script run)
    #Calculate CURRENT_ASSESSMENT_TOTAL subtracted from WEEKLY_ASSESSMENT_TOTAL and put value in TOTAL_ASSESSMENT_DIFFERENCE fields in ASMT_RECONCILE_TBL (iterate through rows and calculate difference between values from date of report run vs date of last parcel creation, generally from weekend prior to report run)
    ASMT_FIELDS = ['WEEKLY_ASSESSMENT_TOTAL','CURRENT_ASSESSMENT_TOTAL','TOTAL_ASSESSMENT_DIFFERENCE','CURRENT_ASSESSMENT_DATE']
    today=datetime.date.today()
    with arcpy.da.UpdateCursor(ASMT_RECONCILE_TBL,ASMT_FIELDS) as cursor:
        for row in cursor:
            if row[3] == None:
                cursor.deleteRow()
                pass
            elif row[3].date() != today:
                cursor.deleteRow()
                pass
            elif row[3].date() == today:
                if row[0] is not None:
                    row[2] = row[1] - row[0]
                    cursor.updateRow(row)
                if row[0] is None:
                    row[2] = row[1]
                    cursor.updateRow(row)
            else:
                pass
        del row
        del cursor
        print ("  PRIOR DAY RECORDS REMOVED & TOTAL_ASSESSMENT_DIFFERENCE field calculated...")
        write_log("  PRIOR DAY RECORDS REMOVED & TOTAL_ASSESSMENT_DIFFERENCE field calculated...",logfile)
except:
    print ("\n Unable to remove prior day records & calculate CURRENT_ASSESSMENT_TOTAL subtracted from WEEKLY_ASSESSMENT_TOTAL and put value in TOTAL_ASSESSMENT_DIFFERENCE fields in ASMT_RECONCILE_TBL")
    write_log("\n Unable to remove prior day records & calculate CURRENT_ASSESSMENT_TOTAL subtracted from WEEKLY_ASSESSMENT_TOTAL and put value in TOTAL_ASSESSMENT_DIFFERENCE fields in ASMT_RECONCILE_TBL", logfile)
    logging.exception('Got exception on remove prior day records & calculate CURRENT_ASSESSMENT_TOTAL subtracted from WEEKLY_ASSESSMENT_TOTAL and put value in TOTAL_ASSESSMENT_DIFFERENCE fields in ASMT_RECONCILE_TBL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()

try:
    # Remove records with a zero or None (null) value in the TOTAL_ASSESSMENT_DIFFERENCE field (iterate through records, remove any will a zero or null value, otherwise, no assessment changes)
    with arcpy.da.UpdateCursor(ASMT_RECONCILE_TBL,'TOTAL_ASSESSMENT_DIFFERENCE') as delcursor:
        for delrow in delcursor:
            if delrow[0] == 0 or delrow[0] == None:
                delcursor.deleteRow()
            else:
                pass
        del delrow
        del delcursor
        print ("   Records with zero value in TOTAL_ASSESSMENT_DIFFERENCE field, removed from table...")
        write_log("   Records with zero value in TOTAL_ASSESSMENT_DIFFERENCE field, removed from table...",logfile)
except:
    print ("\n Unable to remove records with a zero value in the TOTAL_ASSESSMENT_DIFFERENCE field")
    write_log("\n Unable to remove records with a zero value in the TOTAL_ASSESSMENT_DIFFERENCE field", logfile)
    logging.exception('Got exception on remove records with a zero value in the TOTAL_ASSESSMENT_DIFFERENCE field logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()
    
print ("         Calculating TOTAL_ASSESSMENT_DIFFERENCE field in ASMT_RECONCILE_TBL in AUTOWORKSPACE, then removing records with zero or null value in that field completed")
write_log("         Calculating TOTAL_ASSESSMENT_DIFFERENCE field in ASMT_RECONCILE_TBL in AUTOWORKSPACE, then removing records with zero or null value in that field completed", logfile)

print ("\n Exporting update table to excel file at R:\GIS\Assessment\Reports")
write_log("\n Exporting update table to excel file at R:\GIS\AssessmentReports",logfile)

try:
    # Delete excel report from prior run (delete excel workbook if it exists, as to not fill folder full of excel reports or cause the program to fail)
    if arcpy.Exists(ASMT_REPORT):
        os.remove(ASMT_REPORT)
        print (ASMT_REPORT + " found - table deleted")
        write_log(ASMT_REPORT + " found - table deleted", logfile)
except:
    print ("\n Unable to delete Total_Assessment_Reconcile_Report.xls, need to delete existing excel file manually and/or close program locking the file")
    write_log("\n Unable to delete Total_Assessment_Reconcile_Report.xls, need to delete existing excel file manually and/or close program locking the file", logfile)
    logging.exception('Got exception on delete Total_Assessment_Reconcile_Report.xls logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
try:
    # Exporting ASMT_RECONCILE_TBL to excel in R:\GIS\Assessment\Assmt_Reconcile_Report folder
    arcpy.TableToExcel_conversion(ASMT_RECONCILE_TBL, ASMT_REPORT, "ALIAS", "CODE") 
except:
    print ("\n Unable to export ASMT_RECONCILE_TBL to excel in R:\GIS\Assessment\Reports folder")
    write_log("\n Unable to export ASMT_RECONCILE_TBL to excel in R:\GIS\Assessment\Reports folder", logfile)
    logging.exception('Got exception on export ASMT_RECONCILE_TBL to excel in R:\GIS\Assessment\Reports folder field logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()

print ("         Exporting update table to excel file at R:\GIS\Assessment\Reports completed")
write_log("         Exporting update table to excel file at R:\GIS\Assessment\Reports completed", logfile)

try:
    # Clean up temp files by deleting them (delete temp FGDB used in above steps as they are no longer needed)
    if arcpy.Exists(ASMT_TEMP_FGDB):
        arcpy.Delete_management(ASMT_TEMP_FGDB, "Workspace")
        print ("ASMT_TEMP_FGDB found - FGDB deleted")
        write_log("ASMT_TEMP_FGDB found - FGDB deleted", logfile)
except:
    print ("\n Unable to delete ASMT_TEMP_FGDB, need to delete existing FGDB manually and/or close program locking the FGDB")
    write_log("Unable to delete ASMT_TEMP_FGDB, need to delete existing FGDB manually and/or close program locking the FGDB", logfile)
    logging.exception('Got exception on delete ASMT_TEMP_FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n TOTAL ASSESSMENT VALUE RECONCILE REPORT IS UPDATED: " + str(Day) + " " + str(end_time))
write_log("\n TOTAL ASSESSMENT VALUE RECONCILE REPORT IS UPDATED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
