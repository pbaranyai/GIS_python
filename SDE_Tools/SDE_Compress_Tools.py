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
# Created on: 2019-05-16 
# Updated on 2021-09-13
# Works in ArcGIS Pro
# ---------------------------------------------------------------------------

import sys,arcpy, datetime,os,logging,time

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\GIS\\SDE_Compress.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Setup Version logging (configure version logging location, type, and filemode -- overwrite every run)
Version_logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\GIS\\Version_Log.log"
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

try:
    # delete old database versions log (if exists)
    if arcpy.Exists(Version_logfile):
        arcpy.Delete_management(Version_logfile, "Log")
        print (Version_logfile + " found - log deleted")
        write_log(Version_logfile + " found - log deleted", logfile)
except:
    print ("\n Unable to delete Version_logfile, need to delete existing FGDB manually and/or close program locking the tables")
    write_log("\n Unable to create new Version_logfile, need to delete existing FGDB manually and/or close program locking the tables", logfile)
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
DB_Connections = r"\\FILELOCATION\\GIS\\ArcAutomations\\Database_Connections"  

# Set the workspaces
arcpy.env.workspace = DB_Connections + '\\SDE@ccsde.sde'
workspace = arcpy.env.workspace
defaultVersion = "sde.DEFAULT"

# Set database connection variables
AGOL_EDIT_CONNECTION = DB_Connections + "\\agol_edit@ccsde.sde"
AGOL_EDIT_PUB_CONNECTION = DB_Connections + "\\agol_edit_pub@ccsde.sde"
AST_CONNECTION = DB_Connections + "\\AST@ccsde.sde"
AUTOWKSP_CONNECTION = DB_Connections + "\\auto_workspace@ccsde.sde"
CONSV_DIST_CONNECTION = DB_Connections + "\\CONSV_DIST@ccsde.sde"
CRAW_INTERNAL_CONNECTION = DB_Connections + "\\craw_internal@ccsde.sde"
GIS_CONNECTION = DB_Connections + "\\GIS@ccsde.sde"
PLAN_CONNECTION = DB_Connections + "\\PLANNING@ccsde.sde"
PUB_OD_CONNECTION = DB_Connections + "\\public_od@ccsde.sde"
PS_CONNECTION = DB_Connections + "\\PUBLIC_SAFETY@ccsde.sde"
PUBLIC_WEB_CONNECTION = DB_Connections + "\\public_web@ccsde.sde"
SDE_CONNECTION = DB_Connections + "\\SDE@ccsde.sde"
HS_CONNECTION = DB_Connections + "\\HUMAN_SERVICES@ccsde.sde"


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
    logging.exception('Got exception on get list of connected users logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
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
    logging.exception('Got exception on block new connections to the database logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Disconnect all users from the database.
    arcpy.DisconnectUser(SDE_CONNECTION, "ALL")
except:
    print ("\n Unable to disconnect all users from the database")
    write_log("Unable to disconnect all users from the database", logfile)
    logging.exception('Got exception on disconnect all users from the database logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Blocking new connections to database, then disconnecting all users completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Blocking new connections to database, then disconnecting all users completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

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
    arcpy.management.ReconcileVersions(SDE_CONNECTION, "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION", Version_logfile)
    print ("\n  Log of reconcile and post written to "+Version_logfile)
    write_log("\n  Log of reconcile and post written to "+Version_logfile,logfile)
except:
    print ("\n Unable to reconcile and post versions from database, then delete them")
    write_log("Unable to reconcile and post versions from database, then delete them", logfile)
    logging.exception('Got exception on reconcile and post versions from database, then delete them logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Reconcile and Post all public database versions, then deletion of versions completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Reconcile and Post all public database versions, then deletion of versions completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Compression of SDE database")
write_log("\n Compression of SDE database", logfile)

try:
    # Run the compress tool.
    arcpy.management.Compress(SDE_CONNECTION)
except:
    print ("\n Unable to compress SDE database")
    write_log("Unable to compress SDE database", logfile)
    logging.exception('Got exception on compress SDE database logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Compression of SDE database completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Compression of SDE database completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Allow incoming connections to database again")
write_log("\n Allow incoming connections to database again", logfile)

try:
    # Allow the database to begin accepting connections again
    arcpy.AcceptConnections(SDE_CONNECTION, True)
except:
    print ("\n Unable to allow incoming connections to database again")
    write_log("Unable to allow incoming connections to database again", logfile)
    logging.exception('Got exception on allow incoming connections to database again logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Allow incoming connections to database again completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Allow incoming connections to database again completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on AGOL_EDIT_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on AGOL_EDIT_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = AGOL_EDIT_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)

    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on AGOL_EDIT_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on AGOL_EDIT_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on AGOL_EDIT_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on AGOL_EDIT_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON AGOL_EDIT_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on AGOL_EDIT_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on AGOL_EDIT_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on AGOL_EDIT_PUB_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on AGOL_EDIT_PUB_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = AGOL_EDIT_PUB_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)

    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on AGOL_EDIT_PUB_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on AGOL_EDIT_PUB_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on AGOL_EDIT_PUB_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on AGOL_EDIT_PUB_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON AGOL_EDIT_PUB_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on AGOL_EDIT_PUB_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on AGOL_EDIT_PUB_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on AST_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on AST_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = AST_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
   
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on AST_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on AST_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on AST_CONNECTION at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on AST_CONNECTION at " + time.strftime("%I:%M:%S %p", time.localtime()), logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON AST_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on AST_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on AST_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on AUTOWKSP_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on AUTOWKSP_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = AUTOWKSP_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
   
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on AUTOWKSP_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on AUTOWKSP_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on AUTOWKSP_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on AUTOWKSP_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON AUTOWKSP_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on AUTOWKSP_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on AUTOWKSP_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on CONSV_DIST_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on CONSV_DIST_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = CONSV_DIST_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
   
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on CONSV_DIST_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on CONSV_DIST_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on CONSV_DIST_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on CONSV_DIST_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON CONSV_DIST_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on CONSV_DIST_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on CONSV_DIST_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on CRAW_INTERNAL_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on CRAW_INTERNAL_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = CRAW_INTERNAL_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
   
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on CRAW_INTERNAL_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on CRAW_INTERNAL_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on CRAW_INTERNAL_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on CRAW_INTERNAL_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON CRAW_INTERNAL_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on CRAW_INTERNAL_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on CRAW_INTERNAL_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on GIS_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on GIS_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = GIS_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
   
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on GIS_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on GIS_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on GIS_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on GIS_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON GIS_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on GIS_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on GIS_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on PLAN_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on PLAN_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = PLAN_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
   
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on PLAN_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on PLAN_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on PLAN_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on PLAN_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON PLAN_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on PLAN_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on PLAN_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on PUB_OD_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on PUB_OD_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = PUB_OD_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
   
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on PUB_OD_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on PUB_OD_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on PUB_OD_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on PUB_OD_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON PUB_OD_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on PUB_OD_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on PUB_OD_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on PS_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on PS_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = PS_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
   
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on PS_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on PS_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on PS_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on PS_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON PS_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on PS_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on PS_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on PUBLIC_WEB_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on PUBLIC_WEB_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = PUBLIC_WEB_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
   
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on PUBLIC_WEB_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on PUBLIC_WEB_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on PUBLIC_WEB_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on PUBLIC_WEB_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON PUBLIC_WEB_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on PUBLIC_WEB_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on PUBLIC_WEB_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on HUMAN_SERVICES_CONNECTION")
write_log("\n Rebuild indexes and analyze datasets on HUMAN_SERVICES_CONNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = HS_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
   
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "NO_SYSTEM", dataList, "ALL")
    print ("\n Rebuild index on HUMAN_SERVICES_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on HUMAN_SERVICES_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "NO_SYSTEM", dataList, "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
   
except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on HUMAN_SERVICES_CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on HUMAN_SERVICES_CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON HUMAN_SERVICES_CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on HUMAN_SERVICES_CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on HUMAN_SERVICES_CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild indexes and analyze datasets on all datasets on SDE CONNNECTION")
write_log("\n Rebuild indexes and analyze datasets on SDE CONNNECTION all datasets", logfile)

# Get a list of datasets owned by the admin user
try:
    # reset the workspace
    arcpy.env.workspace = SDE_CONNECTION
    workspace = arcpy.env.workspace

    # Get the user name for the workspace
    userName = arcpy.Describe(workspace).connectionProperties.user

    # Get a list of all the datasets the user has access to.
    # First, get all the stand alone tables, feature classes and rasters owned by the current user.
    dataList = arcpy.ListTables('*.' + userName + '.*') + arcpy.ListFeatureClasses('*.' + userName + '.*') + arcpy.ListRasters('*.' + userName + '.*')
    print (dataList)
    write_log((dataList),logfile)

    # Next, for feature datasets owned by the current user
    # get all of the featureclasses and add them to the master list.
    for dataset in arcpy.ListDatasets('*.' + userName + '.*'):
        dataList += arcpy.ListFeatureClasses(feature_dataset=dataset)
        print (dataList)
        write_log((dataList),logfile)
    
    # Pass in the list of datasets owned by the connected user to the rebuild indexes 
    # and update statistics on the data tables
    arcpy.RebuildIndexes_management(workspace, "SYSTEM", "", "ALL")
    print ("\n Rebuild index on SDE CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
    write_log("\n Rebuild index on SDE CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()),logfile)
    arcpy.AnalyzeDatasets_management(workspace, "SYSTEM", "", "NO_ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")

except:
    print ("\n Unable to rebuild indexes and analyze datasets on all datasets on SDE CONNECTION")
    write_log("Unable to rebuild indexes and analyze datasets on all datasets on SDE CONNECTION", logfile)
    logging.exception('Got exception on rebuild indexes and analyze datasets on all datasets ON SDE CONNECTION logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild indexes and analyze datasets on all datasets on SDE CONNECTION completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild indexes and analyze datasets on all datasets on SDE CONNECTION completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Rebuild versions that existed prior to SDE compress")
write_log("\n Rebuild versions that existed prior to SDE compress", logfile)

# Database Versions that are not currently used are commented out - as they were causing issues during the rebuild.  If they are used in the future, uncomment them out, also be sure to start the cursor with an "if", not an "elif"
try:
    for version in versionList:
        if version.startswith("GIS"):
            arcpy.management.CreateVersion(GIS_CONNECTION,defaultVersion, version[4:], "PUBLIC")
            print ("Created version {0}".format(version))
            write_log("Created version {0}".format(version),logfile)
        elif version.startswith("PUBLIC_SAFETY"):
            arcpy.management.CreateVersion(PS_CONNECTION,defaultVersion, version[14:], "PUBLIC")
            print ("Created version {0}".format(version))
            write_log("Created version {0}".format(version),logfile)
        elif version.startswith("AST"):
            arcpy.management.CreateVersion(AST_CONNECTION,defaultVersion, version[4:], "PUBLIC")
            print ("Created version {0}".format(version))
            write_log("Created version {0}".format(version),logfile)
        elif version.startswith("PLANNING"):
            arcpy.management.CreateVersion(PLAN_CONNECTION,defaultVersion, version[9:], "PUBLIC")
            print ("Created version {0}".format(version))
            write_log("Created version {0}".format(version),logfile)
        elif version.startswith("HUMAN_SERVICES"):
            arcpy.management.CreateVersion(HS_CONNECTION,defaultVersion, version[15:], "PUBLIC")
            print ("Created version {0}".format(version))
            write_log("Created version {0}".format(version),logfile)
        else:
            pass
        del version
except:
    print ("\n Unable to rebuild versions")
    write_log("Unable to rebuild versions", logfile)
    logging.exception('Got exception on rebuild versions logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Rebuild versions completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Rebuild versions completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL SDE COMPRESS PROCESSES HAVE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL SDE COMPRESS PROCESSES HAVE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
