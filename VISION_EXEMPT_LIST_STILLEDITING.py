# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# VISION_EXEMPT_LIST.py
# Created on: 2019-08-27 
# Updated on 2019-08-27
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Will eventually be part of the Parcel Builder script
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import datetime
import os
import traceback
import logging
import builtins

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\VISION_EXEMPTS_TEMP.log"  
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

# Database variables:
#AUTOWORKSPACE = "Database Connections\\auto_workspace@ccsde.sde"
AUTOWORKSPACE = "C:\\Users\\pbaranyai\\Desktop\\AssessmentTest.gdb"
AUTOWORKSPACE_AST = "Database Connections\\auto_workspace@ccsde.sde\\CCSDE.AUTO_WORKSPACE.Assessment"
VISION_VIEW = "Database Connections\\Vision_Database.sde"

# Local variables:
##GSS_TAXCLAIM_TBL = GSS + "\\dtaGSSCrawford.dbo.CollTaxSaleWeb"
VIS_EXEMPTS_TBL = AUTOWORKSPACE + "\\VIS_EXEMPTS_TBL"


start_time = time.time()

print ("============================================================================")
print (("Updating Land Records: "+ str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\nTax Claim Repository Building Only Feature Class")
print ("Tax Claim Upset/Judicial Sale Building Only Feature Class")
print ("Tax Claim Repository Tax Parcels Feature Class")
print ("Tax Claim Upset/Judicial Sale Tax Parcels Feature Class")
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Land Records: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nTax Claim Repository Building Only Feature Class", logfile)  
write_log("Tax Claim Upset/Judicial Sale Building Only Feature Class", logfile) 
write_log("Tax Claim Repository Tax Parcels Feature Class", logfile)
write_log("Tax Claim Upset/Judicial Sale Tax Parcels Feature Class", logfile) 
write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB -> PUBLIC_OD (where applicable)", logfile)
write_log("============================================================================", logfile)


try:
##    # Find highest value in EXE_LINE_NUM field
##    with arcpy.da.UpdateCursor(VIS_EXEMPTS_TBL,['EXE_PID','EXE_LINE_NUM']) as update_cursor:  
##        keep_list = list()  
##        PID = 'EXE_PID'  
##        LINE_ID = max('EXE_LINE_NUM')
##        for row in update_cursor:  
##            row_val = row.getValue(PID)
##            own_val = row.getValue(LINE_ID)
##            if row_val not in keep_list:  
##                keep_list.append(row_val)
##            if own_val not in keep_list:
##                keep_list.append(own_val)
##            elif row_val in keep_list:  
##                update_cursor.deleteRow(row)  
##            else:  
##                pass
##        print "Latest Exemptions kept, others deleted"
##        del row, update_cursor
    # Find highest value in EXE_LINE_NUM field
        rows = arcpy.da.UpdateCursor(VIS_EXEMPTS_TBL,['EXE_PID','EXE_LINE_NUM'])  
        keep_list = []
        for row in rows:
            if row.Group not in keep_list:
                keep_list.append(row.Group)
        del row
        out_dict = {}
        for row in rows:
            for g in groups:
                lst = []
                if row.Group == g:
                    lst.append(row.LINE_NUM)
                out_dict(g) = max(lst)
        del row, rows
        for group in out_dict:
            keep_list.append()
        print "Latest Exemptions kept, others deleted"
except:
    print ("\n Unable to Delete older exemptions")
    write_log("Unable to Delete older exemptions", logfile)
    logging.exception('Got exception on Delete older exemptions logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()  

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n ALL LAND RECORDS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("\n ALL LAND RECORDS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print (("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
