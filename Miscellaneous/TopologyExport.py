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

print ("============================================================================")
print (("Exporting Topology: "+ str(Day) + " " + str(Time)))
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Exporting Topology: "+ str(Day) + " " + str(Time), logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

# Import arcpy module
import arcpy

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Set topology path
SectionTopology = r"\\FILELOCATION\\GIS\\Planning\\Zoning_Maps_Topology20190715.gdb\\Zoning\\Zoning_Topology"

print ("Begining Export")

# Export Topology Errors (set path-------------------->                                                             -----> and errors path)
arcpy.ExportTopologyErrors_management(SectionTopology, r"\\FILELOCATION\\GIS\\Planning\\Zoning_Maps_Topology20190715.gdb\\Zoning", "Zoning_Topology_errors")

print ("Export completed")

del arcpy
