# ---------------------------------------------------------------------------
# TopologyExport.py
# Created on: 2019-03-05 
# Updated on 2021-09-22
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Export topology errors out to feature classes
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy,time,datetime,logging,os,sys

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%Y-%m-%d", time.localtime())
Time = time.strftime("%H%M", time.localtime())
start_time = time.time()
elapsed_time = time.time() - start_time

# Setup export path to *script location* log folder
try:
    LogDirectory = os.getcwd()+"\\log"
    logdirExists = os.path.exists(LogDirectory)
    if not logdirExists:
        os.makedirs(LogDirectory)
        print(LogDirectory+" was not found, so it was created")
except:
    print('\n Unable to create log folder within '+os.getcwd()+' folder')
    sys.exit()

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = LogDirectory +"\\Topology_Export_Log.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
def write_log(text, file):
    f = open(file, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return


print ("============================================================================")
print (("Exporting Topology: "+ str(Day) + " " + str(Time)))
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Exporting Topology: "+ str(Day) + " " + str(Time), logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Set topology path
SectionTopology = r"\\FILELOCATION\\GIS\\Planning\\Zoning_Maps_Topology20190715.gdb\\Zoning\\Zoning_Topology"

print ("Begining Export")

# Export Topology Errors (set path-------------------->                                                             -----> and errors path)
arcpy.ExportTopologyErrors_management(SectionTopology, r"\\FILELOCATION\\GIS\\Planning\\Zoning_Maps_Topology20190715.gdb\\Zoning", "Zoning_Topology_errors")

print ("Export completed")
sys.exit()
