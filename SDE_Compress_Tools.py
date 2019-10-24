# ---------------------------------------------------------------------------
# SDE_Compress_Tools.py
#
# Description:
# This tool will first check for all database versions that contain "CCSDE.sde" in the name (excluding external database views), 
# retrieve a list of connected users, disconnect all users, then block new incoming connections to the database versions.
#
# It will then get a list of all public versions, then reconcile, post, then delete them.
#
# It will then, compress the SDE database, once that has completed. 
#
# It will then allow new database connections again.  Check R:\GIS\GIS_LOGS\GIS\Version_Log.log for the list of public versions that
# need rebuilt manually.
#
# It will finally check for a list of all datasets with each database connection, and rebuild the indexes and re-analyze them.
#
#
# Author: Phil Baranyai/Crawford County GIS Manager
# Created: 5/16/2019
# Last Edited: 7/16/2019
# ---------------------------------------------------------------------------

import sys
import arcpy
from arcpy import env
import datetime
import os
import traceback
import logging
import __builtin__

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\SDE_Compress.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Setup Version logging (configure version logging location, type, and filemode -- overwrite every run)
Version_logfile = r"R:\\GIS\\GIS_LOGS\\GIS\\Version_Log.log"
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
    # Set the necessary product code
    import arcinfo
except:
    print ("No ArcInfo (ArcAdvanced) license available")
    write_log("!!No ArcInfo (ArcAdvanced) license available!!", logfile)
    logging.exception('Got exception on importing ArcInfo (ArcAdvanced) license logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit()

try:
    # delete old database versions log (if exists)
    if arcpy.Exists(Version_logfile):
        arcpy.Delete_management(Version_logfile, "Log")
        print (Version_logfile + " found - log deleted")
        write_log(Version_logfile + " found - log deleted", logfile)
except:
    print ("\n Unable to delete Version_logfile, need to delete existing FGDB manually and/or close program locking the tables")
    write_log("\n Unable to create new Version_logfile, need to delete existing FGDB manually and/or close program locking the tables", logfile)
    logging.exception('Got exception on delete Version_logfile logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()    

# Get list of database connections
def sdeConnections():
    appdata = os.getenv('APPDATA')
    arcgisVersion = "10.7"
    #arcgisVersion = arcpy.GetInstallInfo()['Version']
    arcCatalogPath = os.path.join(appdata ,'ESRI',u'Desktop'+arcgisVersion, 'ArcCatalog')
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
print ("============================================================================")
write_log ("============================================================================", logfile)
write_log ("Checking for Database Connections: "+ str(Day) + " " + str(Time), logfile)
write_log ("============================================================================", logfile)

DB_LIST.sort(reverse = False)
for DBConnection in DB_LIST:
    print ((DBConnection))
    write_log(DBConnection, logfile)

# Set the connections folder -- Toggle depending on which machine the script is runnning, default should be CCORBWEAVER
DB_Connections = r'C:\\Users\\arcadmin\\AppData\\Roaming\\ESRI\\Desktop10.7\\ArcCatalog'   #--CCORBWEAVER
#DB_Connections = r'C:\\Users\\pbaranyai\\AppData\\Roaming\\ESRI\\Desktop10.7\\ArcCatalog'  #--GIS01

# Set the workspaces
arcpy.env.workspace = DB_Connections + '\\SDE@ccsde.sde'
workspace = arcpy.env.workspace
defaultVersion = "sde.DEFAULT"

# Set database connection variables
AGOL_EDIT_CONNECTION = DB_Connections + "\\agol_edit@ccsde.sde"
AGOL_EDIT_PUB_CONNECTION = DB_Connections + "\\agol_edit_pub@ccsde.sde"
AST_CONNECTION = DB_Connections + "\\AST@ccsde.sde"
CONSV_DIST_CONNECTION = DB_Connections + "\\CONSV_DIST@ccsde.sde"
GIS_CONNECTION = DB_Connections + "\\GIS@ccsde.sde"
PLAN_CONNECTION = DB_Connections + "\\PLANNING@ccsde.sde"
PS_CONNECTION = DB_Connections + "\\PUBLIC_SAFETY@ccsde.sde"
SDE_CONNECTION = DB_Connections + "\\SDE@ccsde.sde"

print ("\n============================================================================")
print ("Checking for Connected users:")
print ("============================================================================")
write_log ("\n============================================================================", logfile)
write_log ("Checking for Connected users:", logfile)
write_log ("============================================================================", logfile)

# Get a list of connected users.
try:
    userList = arcpy.ListUsers(SDE_CONNECTION)
    print ("\n")
    userList.sort(reverse = False)
    for USERS in userList:
        print ((USERS))
        write_log(USERS, logfile)
except:
    print ("Unable to get list of connected users")
    write_log("\n Unable to get list of connected users", logfile)
    logging.exception('Got exception on get list of connected users logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

write_log("\n============================================================================", logfile)
write_log("Preparing to compress SDE database", logfile)
write_log("Will compress the following:", logfile)

DB_LIST.sort(reverse = False)
for DBConnection in DB_LIST:
    print ((DBConnection))
    write_log(DBConnection, logfile)
write_log("============================================================================", logfile)

print ("\n Blocking new connections to database, then disconnecting all users")
write_log("\n Blocking new connections to database, then disconnecting all users", logfile)

try:
    # Block new connections to the database.
    arcpy.AcceptConnections(SDE_CONNECTION, False)
except:
    print ("\n Unable to block new connections to the database")
    write_log("Unable to block new connections to the database", logfile)
    logging.exception('Got exception on block new connections to the database logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Disconnect all users from the database.
    arcpy.DisconnectUser(SDE_CONNECTION, "ALL")
except:
    print ("\n Unable to disconnect all users from the database")
    write_log("Unable to disconnect all users from the database", logfile)
    logging.exception('Got exception on disconnect all users from the database logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Blocking new connections to database, then disconnecting all users completed")
write_log("       Blocking new connections to database, then disconnecting all users completed", logfile)

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
    logging.exception('Got exception on obtain a list of versions from database logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Execute the ReconcileVersions tool.
    arcpy.ReconcileVersions_management(SDE_CONNECTION, "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION", Version_logfile)
    print ("\n  Log of reconcile and post written to "+Version_logfile)
    write_log("\n  Log of reconcile and post written to "+Version_logfile,logfile)
except:
    print ("\n Unable to reconcile and post versions from database, then delete them")
    write_log("Unable to reconcile and post versions from database, then delete them", logfile)
    logging.exception('Got exception on reconcile and post versions from database, then delete them logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Reconcile and Post all public database versions, then deletion of versions completed")
write_log("       Reconcile and Post all public database versions, then deletion of versions completed", logfile)

print ("\n Compression of SDE database")
write_log("\n Compression of SDE database", logfile)

try:
    # Run the compress tool.
    arcpy.Compress_management('Database Connections\\SDE@ccsde.sde')
except:
    print ("\n Unable to compress SDE database")
    write_log("Unable to compress SDE database", logfile)
    logging.exception('Got exception on compress SDE database logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Compression of SDE database completed")
write_log("       Compression of SDE database completed", logfile)

print "\n Allow incoming connections to database again"
write_log("\n Allow incoming connections to database again", logfile)

try:
    # Allow the database to begin accepting connections again
    arcpy.AcceptConnections(SDE_CONNECTION, True)
except:
    print ("\n Unable to allow incoming connections to database again")
    write_log("Unable to allow incoming connections to database again", logfile)
    logging.exception('Got exception on allow incoming connections to database again logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Allow incoming connections to database again completed")
write_log("       Allow incoming connections to database again completed", logfile)

print ("\n Rebuild indexes on all datasets")
write_log("\n Rebuild indexes on all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # First, get all the stand alone tables, feature classes and rasters.
    dataList = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListRasters()

    # Next, for feature datasets get all of the datasets and featureclasses
    # from the list and add them to the master list.
    for dataset in arcpy.ListDatasets("", "Feature"):
        arcpy.env.workspace = os.path.join(workspace,dataset)
        dataList += arcpy.ListFeatureClasses() + [os.path.join(dataset, d) for d in arcpy.ListDatasets()]

    # reset the workspace
    arcpy.env.workspace = workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user.lower()

    # remove any datasets that are not owned by the connected user.
    userDataList = [ds for ds in dataList if ds.lower().find(".%s." % userName) > -1]

    # Execute rebuild indexes
    # Note: to use the "SYSTEM" option the workspace user must be an administrator.
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ((dataList))
    write_log(dataList,logfile)
except:
    print ("\n Unable to rebuild indexes on all datasets")
    write_log("Unable to rebuild indexes on all datasets", logfile)
    logging.exception('Got exception on rebuild indexes on all datasets logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuild indexes on all datasets completed")
write_log("       Rebuild indexes on all datasets completed", logfile)

print ("\n Analyze all datasets")
write_log("\n Analyze all datasets", logfile)

try:
    # First, get all the stand alone tables, feature classes and rasters.
    dataList = arcpy.ListTables() + arcpy.ListFeatureClasses() + arcpy.ListRasters()

    # Next, for feature datasets get all of the datasets and featureclasses from the list and add them to the master list.
    for dataset in arcpy.ListDatasets("", "Feature"):
        arcpy.env.workspace = os.path.join(workspace,dataset)
        dataList += arcpy.ListFeatureClasses() + [os.path.join(dataset, d) for d in arcpy.ListDatasets()]

    # reset the workspace
    arcpy.env.workspace = workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user.lower()

    # remove any datasets that are not owned by the connected user.
    userDataList = [ds for ds in dataList if ds.lower().find(".%s." % userName) > -1]

    # Execute analyze datasets
    # Note: to use the "SYSTEM" option the workspace user must be an administrator.
    arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", dataList, "ANALYZE_BASE","ANALYZE_DELTA","ANALYZE_ARCHIVE")
    print ((dataList))
    write_log(dataList, logfile)
except:
    print ("\n Unable to analyze all datasets")
    write_log("Unable to analyze all datasets", logfile)
    logging.exception('Got exception on analyze all datasets logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Analyze all datasets completed")
write_log("       Analyze all datasets completed", logfile)

print ("\n Rebuild versions that existed prior to SDE compress")
write_log("\n Rebuild versions that existed prior to SDE compress", logfile)

# Database Versions that are not currently used are commented out - as they were causing issues during the rebuild.  If they are used in the future, uncomment them out, also be sure to start the cursor with an "if", not an "elif"
try:
    for version in versionList:
##        if version.startswith("agol_edit"):
##            arcpy.CreateVersion_management(AGOL_EDIT_CONNECTION,defaultVersion, version[10:], "PUBLIC")
##            print ("Created version {0}".format(version))
##            write_log("Created version {0}".format(version),logfile)
##        elif version.startswith("agol_edit_pub"):
##            arcpy.CreateVersion_management(AGOL_EDIT_PUB_CONNECTION,defaultVersion, version[14:], "PUBLIC")
##            print ("Created version {0}".format(version))
##            write_log("Created version {0}".format(version),logfile)
##        elif version.startswith("CONSV_DIST"):
##            arcpy.CreateVersion_management(CONSV_DIST_CONNECTION,defaultVersion, version[11:], "PUBLIC")
##            print ("Created version {0}".format(version))
##            write_log("Created version {0}".format(version),logfile)
        if version.startswith("GIS"):
            arcpy.CreateVersion_management(GIS_CONNECTION,defaultVersion, version[4:], "PUBLIC")
            print ("Created version {0}".format(version))
            write_log("Created version {0}".format(version),logfile)
        elif version.startswith("PUBLIC_SAFETY"):
            arcpy.CreateVersion_management(PS_CONNECTION,defaultVersion, version[14:], "PUBLIC")
            print ("Created version {0}".format(version))
            write_log("Created version {0}".format(version),logfile)
        elif version.startswith("AST"):
            arcpy.CreateVersion_management(AST_CONNECTION,defaultVersion, version[4:], "PUBLIC")
            print ("Created version {0}".format(version))
            write_log("Created version {0}".format(version),logfile)
        elif version.startswith("PLANNING"):
            arcpy.CreateVersion_management(PLAN_CONNECTION,defaultVersion, version[9:], "PUBLIC")
            print ("Created version {0}".format(version))
            write_log("Created version {0}".format(version),logfile)
        else:
            pass
        del version
except:
    print ("\n Unable to rebuild versions")
    write_log("Unable to rebuild versions", logfile)
    logging.exception('Got exception on rebuild versions logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuild versions completed")
write_log("       Rebuild versions completed", logfile)


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL SDE COMPRESS PROCESSES HAVE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL SDE COMPRESS PROCESSES HAVE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
