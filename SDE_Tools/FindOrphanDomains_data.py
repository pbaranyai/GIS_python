# ---------------------------------------------------------------------------
# FindOrphanDomains_data.py
#
# Description:
# Once a database name is entered in the SDEConnection variable, a text log file is created for the following items.
#
# Finds orphan domains used in SDE feature classes and tables that are used in fields not registered as domains in Geodatabase
#
# Author: Phil Baranyai
# Created on: 2022-12-19 
# Updated on 2022-12-19
# ---------------------------------------------------------------------------

# import required modules
import arcpy, os, logging, datetime
from arcpy import env


# get the SDE connection as a variable
SDEConnection = "SDE Connection Name"


# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = r"\\LOG FILE PATH\\"+SDEConnection+"_OrphanDomains_Data.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
def write_log(text, file):
    f = open(file, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return

arcpy.env.workspace = r"\\SDE CONNECTION FILE PATH\\SDEConnectionFiles"
workspaces = arcpy.ListWorkspaces(SDEConnection+"*_SDE.sde", "SDE")

# create an empty list that we'll populate with the orphaned domains
orphanedDomains = []

# create an empty list that we'll populate with all the domains in your workspace
allDomains = []

# create an empty list that we'll populate with the applied (non-orphaned) domains in your workspace
appliedDomains = []

start_time = time.time()
print ("============================================================================")
print ("Creating list of orphaned domains from feature classes and tables within "+SDEConnection+" as of: "+ str(Day) + " " + str(Time))
print ("============================================================================")
write_log ("============================================================================", logfile)
write_log ("Creating list of orphaned domains from feature classes and tables within "+SDEConnection+" as of: "+ str(Day) + " " + str(Time), logfile)
write_log ("============================================================================", logfile)

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# define a function to list the domain names applied to a table or FC
def ListAppliedDomains(table): # could also be a feature class
    """
    Returns a list of domain names applied in the FC or table
    """
    # create empty list of domain names
    appliedDomains = []

    # add any applied domains to the list
    for f in arcpy.ListFields(table):
        if f.domain != "":
            appliedDomains.append(f.domain)

    return appliedDomains


# list the domain objects in your SDE workspaces
for WKSP in workspaces:
    env.workspace = WKSP
    datasets = arcpy.ListDatasets()
    domainObjects = arcpy.da.ListDomains(WKSP)
    print(WKSP+" has {} domains.".format(str(len(domainObjects))))
    write_log(WKSP+" has {} domains.".format(str(len(domainObjects))),logfile)

# add the names to the list
for domain in domainObjects:
    allDomains.append(domain.name)

# clean up the list of domain objects now that we are done with it
del domainObjects

# list all the feature classes and tables in your SDE workspace
allFcsAndTables = []
for WKSP in workspaces:
    env.workspace = WKSP
    walk = arcpy.da.Walk(workspaces, datatype=["FeatureClass", "Table"])

    for dirpath, dirname, filenames in walk:
        for filename in filenames:
            allFcsAndTables.append(os.path.join(dirpath, filename))

# clean up the walk object
del walk

# go through the tables and feature classes and populate the list of applied domains
for dSET in workspaces:
    for item in allFcsAndTables:
        usedDomains = ListAppliedDomains(item+" --> "+dSET)
        for d in usedDomains:
            appliedDomains.append(d)

# populate the list of orphaned domains based on the 'all domains' that are not in applied domains
for dSET in datasets:
    for item in allDomains:
        if item not in appliedDomains:
            orphanedDomains.append(item+" --> "+dSET)

# report the result
print("\n The following domains are NOT in use in your workspace!")
write_log("\n The following domains are NOT in use in your workspace!", logfile)


for item in orphanedDomains:
    print(item)
    write_log(item,logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ORPHAN DOMAIN LIST WITHIN FC & TABLES HAS COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ORPHAN DOMAIN LIST WITHIN FC & TABLES HAS COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy, logging, datetime, os
sys.exit()
