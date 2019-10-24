# ---------------------------------------------------------------------------
# TopologyExport.py
# Created on: 2019-03-05 
# Updated on 2019-03-05
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Export topology errors out to feature classes
# ---------------------------------------------------------------------------


# Set the necessary product code (sets neccesary ArcGIS product license needed for tools running)
import arceditor

# Import arcpy module
import arcpy

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Set topology path
SectionTopology = r"R:\\GIS\\Planning\\Zoning_Maps_Topology20190715.gdb\\Zoning\\Zoning_Topology"

print ("Begining Export")

# Export Topology Errors (set path-------------------->                                                             -----> and errors path)
arcpy.ExportTopologyErrors_management(SectionTopology, r"R:\\GIS\\Planning\\Zoning_Maps_Topology20190715.gdb\\Zoning", "Zoning_Topology_errors")

print ("Export completed")

del arcpy
