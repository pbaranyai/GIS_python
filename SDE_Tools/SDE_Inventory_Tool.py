# ---------------------------------------------------------------------------
# SDEDataInventory.py
#
# Description:
# Once a database name is entered in the SDEConnection variable, a text log file is created for the following items.
#
# Datasets types:
#   Coverages, Feature, Geometric Network, Mosaic, Network, Parcel Fabric, Raster, Schematic, Terrain, TIN, & Topology
#  
# Feature Class types:
#   Annotation, Arc, Dimension, Edge, Junction, Label, Line, Multipatch, Multipoint, Node, Point, Polygon, Polyline, Region, Route, & Tic
# 
# Table types:
#   dBASE & INFO
#
# Raster types:
#   BMP, GIF, IMG, JP2, JPG, PNG, TIF, & GRID
#
# Author: Phil Baranyai
# Created on: 2022-12-16 
# Updated on 2022-12-16
# ---------------------------------------------------------------------------

import arcpy, os, sys, logging, datetime
from arcpy import env



SDEConnection = "SDE DB Name"


##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^##


# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = r"\\PATHNAME\\InventoryLogs\\"+SDEConnection+"_Inventory.log"
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
print ("Creating Inventory for "+SDEConnection+" as of: "+ str(Day) + " " + str(Time))
print ("============================================================================")
write_log ("============================================================================", logfile)
write_log ("Creating Inventory for "+SDEConnection+" as of: "+ str(Day) + " " + str(Time), logfile)
write_log ("============================================================================", logfile)


# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Path to SDE connectionfiles
arcpy.env.workspace = r"\\PATHNAME\\SDEConnectionFiles"
inWorkspace = arcpy.env.workspace

workspaces = arcpy.ListWorkspaces(SDEConnection+"*", "SDE")


for item in workspaces:
    print('\n'+item)
    write_log('\n'+item,logfile)
    env.workspace = item
    datasets = arcpy.ListDatasets()
    fcs = arcpy.ListFeatureClasses()
    tbls = arcpy.ListTables()
    rst = arcpy.ListRasters()
    for data in datasets:
        print('\t', "Datasets: "+data)
        write_log(("Datasets: "+data),logfile)
        datasetname=arcpy.ListFeatureClasses("*","",data)
        for fc_ds in datasetname:
        print('\t', "Feature Class within "+data+" dataset: "+fc_ds)
        write_log("Feature Class within "+data+" dataset: "+fc_ds, logfile)
    for fc in fcs:
        print('\t', "Standalone Feature Class: "+fc)
        write_log(("Standalone Feature Class: "+fc),logfile)
    for tbl in tbls:
        print('\t', "Table: "+tbl)
        write_log(("Table: "+tbl),logfile)
    for rasters in rst:
        print('\t', "Raster: "+rasters)
        write_log(("Raster: "+rasters),logfile)


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n INVENTORY LIST HAS COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n INVENTORY LIST HAS COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy, logging, datetime
sys.exit()
