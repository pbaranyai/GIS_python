# ---------------------------------------------------------------------------
# DetectRelationshipClasses_SDE.py
#
# Description:
# Catalogs and reports relationship classes within SDE
#
# Author: Phil Baranyai
# Created on: 2022-12-20 
# Updated on 2022-12-20
# ---------------------------------------------------------------------------

import arcpy, os, sys, logging, datetime
from arcpy import env


SDEConnection = "SDEConnectionName"


# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = r"\\LOGFILE PATH\\"+SDEConnection+"_RelationshipClass_Inventory.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)


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

start_time = time.time()
print ("============================================================================")
print ("Creating Relationship Class Inventory for "+SDEConnection+" as of: "+ str(Day) + " " + str(Time))
print ("============================================================================")
write_log ("============================================================================", logfile)
write_log ("Creating Relationship Class Inventory for "+SDEConnection+" as of: "+ str(Day) + " " + str(Time), logfile)
write_log ("============================================================================", logfile)

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

arcpy.env.workspace = r"\\CONNECTIONFILE PATH\\SDEConnectionFiles"
#inWorkspace = arcpy.env.workspace

workspaces = arcpy.ListWorkspaces(SDEConnection+"*SDE.sde", "SDE")


def detectRelationship(): 
     rc_list = [c.name for c in arcpy.Describe(item).children if c.datatype == "RelationshipClass"]
     rc_list 
     for rc in rc_list: 
         rc_path = item + "\\" + rc 
         des_rc = arcpy.Describe(rc_path) 
         origin = des_rc.originClassNames 
         destination = des_rc.destinationClassNames
         Cardinality = des_rc.cardinality
         KeyType = des_rc.keyType
         RelateFields = des_rc.originClassKeys
         print ("Relationship Class: %s \n Origin: %s \n Desintation: %s \n Cardinality: %s \n KeyType: %s \n Relate Fields: %s" %(rc, origin, destination, Cardinality, KeyType, RelateFields))
         write_log(("Relationship Class: %s \n Origin: %s \n Desintation: %s \n Cardinality: %s \n KeyType: %s \n Relate Fields: %s" %(rc, origin, destination, Cardinality, KeyType, RelateFields)),logfile)

for item in workspaces:
    print('\n'+item)
    write_log('\n'+item,logfile)
    try:
        detectRelationship()

    except:
        print("\n Error detecting relationships - did not capture all relationships")
        write_log("\n Error detecting relationships - did not capture all relationships", logfile)
        logging.exception('Got exception on detect relationshps logged at:' + str(Day) + " " + str(Time))
        continue

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n RELATIONSHIP CLASS INVENTORY LIST HAS COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n RELATIONSHIP CLASS INVENTORY LIST HAS COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
del logging
del datetime
sys.exit()
