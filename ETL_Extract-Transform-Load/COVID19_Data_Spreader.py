# ---------------------------------------------------------------------------
# COVID19_Data_Spreader.py
# Created on: 2020-04-09 
# Updated on 2020-04-09
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from AGOL_EDIT_PUB (survey submissions) to PUBLIC_WEB as needed:
#
# ADDR_UNIT_TBL  
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
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
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\COVID19_Data_Spreader.log"  
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
AGOL_EDIT_PUB = "Database Connections\\agol_edit_pub@ccsde.sde"
PUBLIC_WEB = "Database Connections\\public_web@ccsde.sde"

# Local variables:
COVID_SURVEY = AGOL_EDIT_PUB + "\\CCSDE.AGOL_EDIT_PUB.Special_Events\\CCSDE.AGOL_EDIT_PUB.BUSINESS_STATUS_COVID_SURVEY"
COVID_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Special_Events\\CCSDE.PUBLIC_WEB.BUSINESS_STATUS_COVID19"


start_time = time.time()

print ("============================================================================")
print (("Updating Land Records: "+ str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\nBusiness Status COVID19")
print ("\n From AGOL_EDIT_PUB to PUBLIC_WEB (where applicable)")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Land Records: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nBusiness Status COVID19", logfile)  
write_log("\n From AGOL_EDIT_PUB to PUBLIC_WEB (where applicable)", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Business Status COVID19 - PUBLIC_WEB from Business Status COVID19 Survey - AGOL_EDIT_PUB")
write_log("\n Updating Business Status COVID19 - PUBLIC_WEB from Business Status COVID19 Survey - AGOL_EDIT_PUB: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete rows from Business Status COVID19 - PUBLIC_WEB
    arcpy.DeleteRows_management(COVID_WEB)
except:
    print ("\n Unable to delete rows from Business Status COVID19 - PUBLIC_WEB")
    write_log("Unable to delete rows from Business Status COVID19 - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Business Status COVID19 - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Make feature layer from Business Status COVID19 Survey - AGOL_EDIT_PUB // while filtering out REVIEWED = 'Y' (make temporary layer in memory, filtering out REVIEWED = 'Y', as they have been approved by staff from public submission from Survey123.
    BUSINESS_STATUS_COVID19_LAYER = arcpy.MakeFeatureLayer_management(COVID_SURVEY, "BUSINESS_STATUS_COVID19_LAYER", "REVIEWED = 'Y'", "", "BUSINESS_NAME BUSINESS_NAME VISIBLE NONE;BUSINESS_STREET_ADDRESS BUSINESS_STREET_ADDRESS VISIBLE NONE;BUSINESS_POST_OFFICE_ADDRESS BUSINESS_POST_OFFICE_ADDRESS VISIBLE NONE;BUSINESS_ZIPCODE_ADDRESS BUSINESS_ZIPCODE_ADDRESS VISIBLE NONE;BUSINESS_PHONE_NUMBER BUSINESS_PHONE_NUMBER VISIBLE NONE;BUSINESS_WEBSITE BUSINESS_WEBSITE VISIBLE NONE;BUSINESS_SUBMITTER_NAME BUSINESS_SUBMITTER_NAME VISIBLE NONE;BUSINESS_SUBMITTER_POSITION BUSINESS_SUBMITTER_POSITION VISIBLE NONE;BUSINESS_HOURS BUSINESS_HOURS VISIBLE NONE;SPECIAL_INSTRUCTIONS SPECIAL_INSTRUCTIONS VISIBLE NONE;BUSINESS_STATUS BUSINESS_STATUS VISIBLE NONE;BUSINESS_TYPE BUSINESS_TYPE VISIBLE NONE;PUBLIC_INTERACTION_TYPE PUBLIC_INTERACTION_TYPE VISIBLE NONE;COMMENTS COMMENTS VISIBLE NONE;REVIEWED REVIEWED VISIBLE NONE;DATE_ADDED DATE_ADDED VISIBLE NONE;DATE_EDITED DATE_EDITED VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;GlobalID GlobalID VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;BUSINESS_STATE BUSINESS_STATE VISIBLE NONE")
except:
    print ("\n Unable to make feature layer from Business Status COVID19 Survey - AGOL_EDIT_PUB // while filtering out REVIEWED = 'Y'")
    write_log("Unable to make feature layer from Business Status COVID19 Survey - AGOL_EDIT_PUB // while filtering out REVIEWED = 'Y'", logfile)
    logging.exception('Got exception on make feature layer from Business Status COVID19 Survey - AGOL_EDIT_PUB // while filtering out REVIEWED = Y logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Append Business Status COVID19 - PUBLIC_WEB from Business Status COVID19 Survey - AGOL_EDIT_PUB
    arcpy.Append_management(BUSINESS_STATUS_COVID19_LAYER, COVID_WEB, "NO_TEST", 'BUSINESS_NAME "Business Name" true true false 150 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_NAME,-1,-1;BUSINESS_STREET_ADDRESS "Business Street Address" true true false 75 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_STREET_ADDRESS,-1,-1;BUSINESS_POST_OFFICE_ADDRESS "Business address post office" true true false 50 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_POST_OFFICE_ADDRESS,-1,-1;BUSINESS_ZIPCODE_ADDRESS "Business address zipcode" true true false 8 Double 8 38 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_ZIPCODE_ADDRESS,-1,-1;BUSINESS_PHONE_NUMBER "Business phone number" true true false 50 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_PHONE_NUMBER,-1,-1;BUSINESS_WEBSITE "Business website" true true false 200 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_WEBSITE,-1,-1;BUSINESS_SUBMITTER_NAME "Name of person submitting survey" true true false 75 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_SUBMITTER_NAME,-1,-1;BUSINESS_SUBMITTER_POSITION "Position in company of submitter" true true false 75 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_SUBMITTER_POSITION,-1,-1;BUSINESS_HOURS "Business Hours" true true false 100 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_HOURS,-1,-1;SPECIAL_INSTRUCTIONS "Special Instructions" true true false 300 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,SPECIAL_INSTRUCTIONS,-1,-1;BUSINESS_STATUS "Business Status" true true false 50 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_STATUS,-1,-1;BUSINESS_TYPE "Business Type" true true false 75 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_TYPE,-1,-1;PUBLIC_INTERACTION_TYPE "Type of public interaction" true true false 50 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,PUBLIC_INTERACTION_TYPE,-1,-1;COMMENTS "Additional Comments" true true false 300 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,COMMENTS,-1,-1;REVIEWED "Reviewed by staff?" true true false 3 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,REVIEWED,-1,-1;DATE_ADDED "Date Added" true true false 8 Date 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,DATE_ADDED,-1,-1;DATE_EDITED "Date Edited" true true false 8 Date 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,DATE_EDITED,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,GlobalID,-1,-1;BUSINESS_STATE "Business State" true true false 50 Text 0 0 ,First,#,BUSINESS_STATUS_COVID19_LAYER,BUSINESS_STATE,-1,-1', "")
    BUSSTAT_COVID19_result = arcpy.GetCount_management(COVID_WEB)
    print (('{} has {} records'.format(COVID_WEB, BUSSTAT_COVID19_result[0])))
    write_log('{} has {} records'.format(COVID_WEB, BUSSTAT_COVID19_result[0]), logfile)
except:
    print ("\n Unable to append Business Status COVID19 - PUBLIC_WEB from Business Status COVID19 Survey - AGOL_EDIT_PUB")
    write_log("Unable to append Business Status COVID19 - PUBLIC_WEB from Business Status COVID19 Survey - AGOL_EDIT_PUB", logfile)
    logging.exception('Got exception on append Business Status COVID19 - PUBLIC_WEB from Business Status COVID19 Survey - AGOL_EDIT_PUB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Business Status COVID19 - PUBLIC_WEB from Business Status COVID19 Survey - AGOL_EDIT_PUB completed")
write_log("       Updating Business Status COVID19 - PUBLIC_WEB from Business Status COVID19 Survey - AGOL_EDIT_PUB completed", logfile)

try:
    # Delete BUSINESS_STATUS_COVID19_LAYER
    arcpy.Delete_management(BUSINESS_STATUS_COVID19_LAYER)
except:
    print ("\n Unable to Delete BUSINESS_STATUS_COVID19_LAYER")
    write_log("Unable to Delete BUSINESS_STATUS_COVID19_LAYER", logfile)
    logging.exception('Got exception on Delete BUSINESS_STATUS_COVID19_LAYER logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()  

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n ALL COVID19 UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("\n ALL COVID19 UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print (("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
