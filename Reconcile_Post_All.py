# ---------------------------------------------------------------------------
# Reconcile_Post_All.py
#
# Description:
# This tool will first check for all database versions that contain "CCSDE.sde" in the name (excluding external database views), 
# it will then get a list of all public versions, then reconcile, post, then delete them.
#
# Author: Phil Baranyai/Crawford County GIS Manager
# Created on: 2021-08-30 
# Updated on 2021-09-21
# Works in ArcGIS Pro
# ---------------------------------------------------------------------------


from __future__ import print_function, unicode_literals, absolute_import
import sys
import arcpy
from arcpy import env
import datetime
import os
import traceback
import logging

try:
    import urllib2  # Python 2
except ImportError:
    import urllib.request as urllib2  # Python 3


# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Reconcile_Post_All.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Setup Version logging (configure version logging location, type, and filemode -- overwrite every run)
Version_logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\RPA_Version_Log.log"
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
    # delete old database versions log (if exists)
    if arcpy.Exists(Version_logfile):
        arcpy.Delete_management(Version_logfile, "Log")
        print (Version_logfile + " found - log deleted")
        write_log(Version_logfile + " found - log deleted", logfile)
except:
    print ("\n Unable to delete Version_logfile, need to delete file manually and/or close program locking the tables")
    write_log("\n Unable to create new Version_logfile, need to delete file manually and/or close program locking the tables", logfile)
    logging.exception('Got exception on delete Version_logfile logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()    

# Get list of database connections
def sdeConnections():
    appdata = os.getenv('APPDATA')
    #arcgisVersion = "10.7"
    arcgisVersion = arcpy.GetInstallInfo()['Version']
    #arcCatalogPath = os.path.join(appdata ,'ESRI',u'Desktop'+arcgisVersion, 'ArcCatalog')
    arcCatalogPath = "E:\\ArcGIS_Pro\\Projects\\ArcServer"
    sdeConnections = []
    for file in os.listdir(arcCatalogPath):
        fileIsSdeConnection = file.lower().endswith("ccsde.sde")
        if fileIsSdeConnection:
            sdeConnections.append(os.path.join(arcCatalogPath, file))
          #  sdeConnections.append(os.path.join("{}\n".format(arcCatalogPath, file)))
    return sdeConnections

DB_LIST = sdeConnections()

start_time = time.time()
print ("============================================================================")
print ("Checking for Database Connections: "+ str(Day) + " " + str(Time))
print ("Works in ArcGIS Pro")
print ("============================================================================")
write_log ("============================================================================", logfile)
write_log ("Checking for Database Connections: "+ str(Day) + " " + str(Time), logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log ("============================================================================", logfile)

DB_LIST.sort(reverse = False)
for DBConnection in DB_LIST:
    print ((DBConnection))
    write_log(DBConnection, logfile)

# Set the connections folder 
DB_Connections = r"\\CCFILE\\anybody\\GIS\\ArcAutomations\\Database_Connections"  

# Set the workspaces
arcpy.env.workspace = DB_Connections + '\\SDE@ccsde.sde'
workspace = arcpy.env.workspace
defaultVersion = "sde.DEFAULT"

# Set database connection variables
AST_CONNECTION = DB_Connections + "\\AST@ccsde.sde"
CONSV_DIST_CONNECTION = DB_Connections + "\\CONSV_DIST@ccsde.sde"
GIS_CONNECTION = DB_Connections + "\\GIS@ccsde.sde"
PLAN_CONNECTION = DB_Connections + "\\PLANNING@ccsde.sde"
PUB_OD_CONNECTION = DB_Connections + "\\public_od@ccsde.sde"
PS_CONNECTION = DB_Connections + "\\PUBLIC_SAFETY@ccsde.sde"
HS_CONNECTION = DB_Connections + "\\HUMAN_SERVICES@ccsde.sde"
SDE_CONNECTION = DB_Connections + "\\SDE@ccsde.sde"

print ("\n============================================================================")
print ("Checking for Connected users:")
print ("============================================================================")
write_log ("\n============================================================================", logfile)
write_log ("Checking for Connected users:", logfile)
write_log ("============================================================================", logfile)


DB_LIST.sort(reverse = False)
for DBConnection in DB_LIST:
    print ((DBConnection))
    write_log(DBConnection, logfile)
write_log("============================================================================", logfile)



print ("\n Reconcile and Post all public database versions, then deletion of versions")
write_log("\n Reconcile and Post all public database versions, then deletion of versions", logfile)

try:
    # Get a list of versions to pass into the ReconcileVersions tool.
    versionList = arcpy.ListVersions(SDE_CONNECTION)
    print ("List of versions that will be reconciled and posted before compress: ")
    versionList.sort(reverse = False)
    for USERS in versionList:
        print ((USERS))
        write_log(USERS, logfile)
except:
    print ("\n Unable to obtain a list of versions from database")
    write_log("Unable to obtain a list of versions from database", logfile)
    logging.exception('Got exception on obtain a list of versions from database logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Execute the ReconcileVersions tool.
    arcpy.management.ReconcileVersions(SDE_CONNECTION, "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "", Version_logfile)
    print ("\n  Log of reconcile and post written to "+Version_logfile)
    write_log("\n  Log of reconcile and post written to "+Version_logfile,logfile)
except:
    print ("\n Unable to reconcile and post versions from database, then delete them")
    write_log("Unable to reconcile and post versions from database, then delete them", logfile)
    logging.exception('Got exception on reconcile and post versions from database, then delete them logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("\n       Reconcile and Post all public database versions, completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("\n       Reconcile and Post all public database versions, completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL PUBLIC VERSIONS HAVE BEEN RECONCILED/POSTED: " + str(Day) + " " + str(end_time))
write_log("\n ALL PUBLIC VERSIONS HAVE BEEN RECONCILED/POSTED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
