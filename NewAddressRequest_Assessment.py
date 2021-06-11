# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NewAddressRequest_Assessment.py
# Created on: 2020-08-10 
# Updated on 2020-08-19
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from AGOL_EDIT_PUB to AGOL_EDIT:
#  
# NewAddressRequests_Assessment
# 
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
# ---------------------------------------------------------------------------

import arcpy
import sys
import datetime
import os
import traceback
import logging

# Stop geoprocessing log history in metadata
arcpy.SetLogHistory(False)

# Setup error logging
logfile = r"R:\\GIS\\GIS_LOGS\\Assessment\\NewAddressRequests_Assessment.log"  
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())
today = datetime.date.today()

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
    sys.exit()

#Database variables:
CRAW_INTERNAL = "Database Connections\\craw_internal@ccsde.sde"
AGOL_EDIT_PUB_PS = "Database Connections\\agol_edit_pub@ccsde.sde\\CCSDE.AGOL_EDIT_PUB.Public_Safety"
AGOL_EDIT_AST = "Database Connections\\agol_edit@ccsde.sde\\CCSDE.AGOL_EDIT.Assessment"

# Local variables:
AddressRequest_PS = AGOL_EDIT_PUB_PS + "\\CCSDE.AGOL_EDIT_PUB.ADDRESS_NEW_REQUESTS_AGOL_EDIT_PUB"
AddressRequest_AST = AGOL_EDIT_AST + "\\CCSDE.AGOL_EDIT.NEW_ADDRESS_REQUESTS_AST"


start_time = time.time()

print ("============================================================================")
print (("Updating New address request assessment data feature classes: "+ str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\nNewAddressRequests_Assessment")
print ("\n From source to CRAW_INTERNAL")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating New address request assessment data feature classes: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nNewAddressRequests_Assessment", logfile)  
write_log("\n From source to CRAW_INTERNAL", logfile)
write_log("============================================================================", logfile)

print ("\n Updating New address requests - assessment - AGOL_EDIT from AGOL_EDIT_PUB")
write_log("\n Updating New address requests - assessment - AGOL_EDIT from AGOL_EDIT_PUB: " + str(Day) + " " + str(Time), logfile)

try:
    # Make layer file from New address requests AGOL_EDIT_PUB (selecting all records from yesterday)
    AddressRequest_Layer = arcpy.MakeFeatureLayer_management(AddressRequest_PS, "AddressRequest_Layer", "AD_REQUEST_DATE >=  CURRENT_TIMESTAMP - 1", "", "AD_LAST_NAME AD_LAST_NAME VISIBLE NONE;AD_FIRST_NAME AD_FIRST_NAME VISIBLE NONE;AD_MAIL_ADDRESS AD_MAIL_ADDRESS VISIBLE NONE;AD_MAIL_CITY AD_MAIL_CITY VISIBLE NONE;AD_MAIL_ZIP AD_MAIL_ZIP VISIBLE NONE;AD_MUNI AD_MUNI VISIBLE NONE;AD_EMAIL AD_EMAIL VISIBLE NONE;AD_STREET_ACCESS AD_STREET_ACCESS VISIBLE NONE;AD_RES_UNITS AD_RES_UNITS VISIBLE NONE;AD_COM_UNITS AD_COM_UNITS VISIBLE NONE;AD_REQUEST_DATE AD_REQUEST_DATE VISIBLE NONE;AD_REQUEST_ADDRESSED AD_REQUEST_ADDRESSED VISIBLE NONE;NOTES NOTES VISIBLE NONE;AD_TYPE AD_TYPE VISIBLE NONE;AD_MAIL_STATE AD_MAIL_STATE VISIBLE NONE;AD_REQUEST_EDIT AD_REQUEST_EDIT VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;GlobalID GlobalID VISIBLE NONE;PHONE_NUMBER PHONE_NUMBER VISIBLE NONE;TYPE_OF_REQUEST TYPE_OF_REQUEST VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;STAFF_COMMENTS STAFF_COMMENTS VISIBLE NONE")
    print ("\n Selected all new address requests from yesterday, preparing to append to New address requests - Assessment")
    write_log("Selected all new address requests from yesterday, preparing to append to New address requests - Assessment", logfile)
except:
    print ("\n Unable to Make layer file from New address requests AGOL_EDIT_PUB")
    write_log("Unable to Make layer file from New address requests AGOL_EDIT_PUB", logfile)
    logging.exception('Got exception on Make layer file  from New address requests AGOL_EDIT_PUB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append New address requests - assessment - AGOL_EDIT from AddressRequest_Layer
    arcpy.Append_management(AddressRequest_Layer, AddressRequest_AST, "NO_TEST", 'AD_LAST_NAME "Applicant Last Name or Business Name" true true false 80 Text 0 0 ,First,#,AddressRequest_Layer,AD_LAST_NAME,-1,-1;AD_FIRST_NAME "Applicant First Name" true true false 60 Text 0 0 ,First,#,AddressRequest_Layer,AD_FIRST_NAME,-1,-1;AD_MAIL_ADDRESS "Applicant Address (Number and Street)" true true false 50 Text 0 0 ,First,#,AddressRequest_Layer,AD_MAIL_ADDRESS,-1,-1;AD_MAIL_CITY "Applicant Address (City)" true true false 50 Text 0 0 ,First,#,AddressRequest_Layer,AD_MAIL_CITY,-1,-1;AD_MAIL_ZIP "Applicant Address (Zipcode)" true true false 50 Text 0 0 ,First,#,AddressRequest_Layer,AD_MAIL_ZIP,-1,-1;AD_MUNI "Municipality of new address" true true false 50 Text 0 0 ,First,#,AddressRequest_Layer,AD_MUNI,-1,-1;AD_EMAIL "Applicant email address" true true false 200 Text 0 0 ,First,#,AddressRequest_Layer,AD_EMAIL,-1,-1;AD_STREET_ACCESS "Street name that driveway will access" true true false 100 Text 0 0 ,First,#,AddressRequest_Layer,AD_STREET_ACCESS,-1,-1;AD_RES_UNITS "How many residentual units (apartments)?" true true false 2 Short 0 5 ,First,#,AddressRequest_Layer,AD_RES_UNITS,-1,-1;AD_COM_UNITS "How many commercial units (suites)?" true true false 2 Short 0 5 ,First,#,AddressRequest_Layer,AD_COM_UNITS,-1,-1;AD_REQUEST_DATE "Date of address request" true true false 8 Date 0 0 ,First,#,AddressRequest_Layer,AD_REQUEST_DATE,-1,-1;NOTES "Additional Notes (up to 1000 characters)" true true false 1000 Text 0 0 ,First,#,AddressRequest_Layer,NOTES,-1,-1;AD_TYPE "Site type of address requested" true true false 8 Double 8 38 ,First,#,AddressRequest_Layer,AD_TYPE,-1,-1;AD_MAIL_STATE "Applicant Address (State Abbreviation)" true true false 2 Text 0 0 ,First,#,AddressRequest_Layer,AD_MAIL_STATE,-1,-1;AD_REQUEST_EDIT "Last record update" false true false 8 Date 0 0 ,First,#,AddressRequest_Layer,AD_REQUEST_EDIT,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,AddressRequest_Layer,GlobalID,-1,-1;PHONE_NUMBER "Phone Number" true true false 255 Text 0 0 ,First,#,AddressRequest_Layer,PHONE_NUMBER,-1,-1;TYPE_OF_REQUEST "Type of Address Request" true true false 255 Text 0 0 ,First,#,AddressRequest_Layer,TYPE_OF_REQUEST,-1,-1;STAFF_COMMENTS "Crawford County Staff Comments" true true false 1000 Text 0 0 ,First,#,AddressRequest_Layer,STAFF_COMMENTS,-1,-1;COMPLETED "Has request been completed?" true true false 50 Text 0 0 ,First,#', "")
    AddressRequest_AST_result = arcpy.GetCount_management(AddressRequest_AST)
    print ('{} has {} records'.format(AddressRequest_AST, AddressRequest_AST_result[0]))
    write_log('{} has {} records'.format(AddressRequest_AST, AddressRequest_AST_result[0]),logfile)
except:
    print ("\n Unable to Append New address requests - assessment - AGOL_EDIT from AddressRequest_Layer")
    write_log("Unable to Append New address requests - assessment - AGOL_EDIT from AddressRequest_Layer", logfile)
    logging.exception('Got exception on Append New address requests - assessment - AGOL_EDIT from AddressRequest_Layer logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating New address requests - assessment - AGOL_EDIT from AGOL_EDIT_PUB completed")
write_log("       Updating New address requests - assessment - AGOL_EDIT from AGOL_EDIT_PUB completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n ALL NEW ADDRESS REQUEST-ASSESSMENT FEATURE CLASSES UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("\n ALL NEW ADDRESS REQUEST-ASSESSMENT FEATURE CLASSES UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print (("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)))
write_log("Elapsed time: " + str (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
