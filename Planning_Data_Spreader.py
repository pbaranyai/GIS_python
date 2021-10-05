# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Planning_Data_Spreader.py
# Created on: 2019-10-01 
# Updated on 2021-09-21
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# Zoning Districts
# Crawford County LERTA zones
# Local Municipal LERTA zones
# Schoool District LERTA zones
# Crawford County Submarkets
# Crawford County Subregions
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import datetime
import os
import traceback
import logging

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\Planning\\Planning_Data_Spreader.log"  
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

#Database Connection Folder
Database_Connections = r"\\CCFILE\\anybody\\GIS\\ArcAutomations\\Database_Connections"

# Database variables:
CRAW_INTERNAL = Database_Connections + "\\craw_internal@ccsde.sde"
PLANNING = Database_Connections + "\\PLANNING@ccsde.sde"
PUBLIC_WEB = Database_Connections + "\\public_web@ccsde.sde"
AGOL_EDIT = Database_Connections + "\\agol_edit@ccsde.sde"

# Local variables:
CC_LERTA_AGOL = AGOL_EDIT + "\\CCSDE.AGOL_EDIT.Investment_Incentive_Zones\\CCSDE.AGOL_EDIT.Crawford_County_LERTA_Zones"
MUNI_LERTA_AGOL = AGOL_EDIT + "\\CCSDE.AGOL_EDIT.Investment_Incentive_Zones\\CCSDE.AGOL_EDIT.Local_Municipal_LERTA_Zones"
SCHOOL_LERTA_AGOL = AGOL_EDIT + "\\CCSDE.AGOL_EDIT.Investment_Incentive_Zones\\CCSDE.AGOL_EDIT.School_District_LERTA_Zones"
CC_LERTA_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Investment_Incentive_Zones\\CCSDE.PUBLIC_WEB.Crawford_County_LERTA_Zones"
MUNI_LERTA_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Investment_Incentive_Zones\\CCSDE.PUBLIC_WEB.Local_Municipal_LERTA_Zones"
SCHOOL_LERTA_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Investment_Incentive_Zones\\CCSDE.PUBLIC_WEB.School_District_LERTA_Zones"
ZONING_PLANNING = PLANNING + "\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts"
ZONING_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL"
ZONING_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Land_Records\\CCSDE.PUBLIC_WEB.ZONING_DISTRICTS_WEB"
CC_SUBMARKETS_PLANNING = PLANNING + "\\CCSDE.PLANNING.Jurisdictional\\CCSDE.PLANNING.CC_Submarkets"
CC_SUBMARKETS_INTERNAL = CRAW_INTERNAL + "\\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.CC_Submarkets"
CC_SUBMARKETS_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Boundaries\\CCSDE.PUBLIC_WEB.CC_Submarkets"
CC_SUBREGIONS_PLANNING = PLANNING+ "\\CCSDE.PLANNING.Jurisdictional\\CCSDE.PLANNING.CrawfordCountySubregions"
CC_SUBREGIONS_INTERNAL = CRAW_INTERNAL + "\\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.CrawfordCountySubregions"
CC_SUBREGIONS_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Boundaries\\CCSDE.PUBLIC_WEB.CrawfordCountySubregions"

start_time = time.time()

print ("============================================================================")
print ("Updating Planning Datasets: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nZoning Districts Feature Class")
print ("Crawford County LERTA zones Feature Class")
print ("Local Municipal LERTA zones Feature Class")
print ("School District LERTA zones Feature Class")
print ("Crawford County Submarkets Feature Class")
print ("Crawford County Subregions Feature Class")
print ("\n From source to CRAW_INTERNAL/AGOL_EDIT -> PUBLIC_WEB (where applicable)")
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Planning Datasets: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nZoning Districts Feature Class", logfile)
write_log("Crawford County LERTA zones Feature Class", logfile)
write_log("Local Municipal LERTA zones Feature Class", logfile)
write_log("School District LERTA zones Feature Class", logfile)
write_log("Crawford County Submarkets Feature Class", logfile)
write_log("Crawford County Subregions Feature Class", logfile)
write_log("\n From source to CRAW_INTERNAL/AGOL_EDIT -> PUBLIC_WEB (where applicable)", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Zoning Districts - CRAW_INTERNAL from PLANNING")
write_log("\n Updating Zoning Districts - CRAW_INTERNAL from PLANNING: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Zoning Districts - CRAW_INTERNAL
    arcpy.DeleteRows_management(ZONING_INTERNAL)
except:
    print ("\n Unable to delete rows from Zoning Districts - CRAW_INTERNAL")
    write_log("Unable to delete rows from Zoning Districts - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Zoning Districts - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Zoning Districts - CRAW_INTERNAL from PLANNING
    arcpy.Append_management(ZONING_PLANNING, ZONING_INTERNAL, "NO_TEST", 'FIPS "FIPS" true true false 8 Double 8 38 ,First,#,'+ZONING_PLANNING+',FIPS,-1,-1;MUNI_NAME "MUNICIPALITY" true true false 50 Text 0 0 ,First,#,'+ZONING_PLANNING+',MUNI_NAME,-1,-1;ZONING "ZONING" true true false 100 Text 0 0 ,First,#,'+ZONING_PLANNING+',ZONING,-1,-1;ORDINANCE "ORDINANCE" true true false 150 Text 0 0 ,First,#,'+ZONING_PLANNING+',ORDINANCE,-1,-1;ENACTED "ENACTED" true true false 50 Text 0 0 ,First,#,'+ZONING_PLANNING+',ENACTED,-1,-1;LAST_AMENDED "LAST AMENDED" true true false 50 Text 0 0 ,First,#,'+ZONING_PLANNING+',LAST_AMENDED,-1,-1;EDITED "EDITED" true true false 8 Date 0 0 ,First,#,'+ZONING_PLANNING+',EDITED,-1,-1;GlobalID "GlobalID" false false true 38 GlobalID 0 0 ,First,#;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+ZONING_PLANNING+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+ZONING_PLANNING+',Shape.STLength(),-1,-1', "")
    Zoning_Dist_Internal_result = arcpy.GetCount_management(ZONING_INTERNAL)
    print ('{} has {} records'.format(ZONING_INTERNAL, Zoning_Dist_Internal_result[0]))
except:
    print ("\n Unable to append Zoning Districts - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append Zoning Districts - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append Zoning Districts - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Zoning Districts - CRAW_INTERNAL from PLANNING completed")
write_log("       Updating Zoning Districts - CRAW_INTERNAL from PLANNING completed", logfile)

print ("\n Updating Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL", logfile)

try:
    # Delete Rows from Zoning Districts - PUBLIC_WEB
    arcpy.DeleteRows_management(ZONING_WEB)
except:
    print ("\n Unable to delete rows from Zoning Districts - PUBLIC_WEB")
    write_log("Unable to delete rows from Zoning Districts - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Zoning Districts - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:  
    # Append Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(ZONING_INTERNAL, ZONING_WEB, "NO_TEST", 'FIPS "FIPS" true true false 8 Double 8 38 ,First,#,'+ZONING_INTERNAL+',FIPS,-1,-1;MUNI_NAME "MUNICIPALITY" true true false 50 Text 0 0 ,First,#,'+ZONING_INTERNAL+',MUNI_NAME,-1,-1;ZONING "ZONING" true true false 100 Text 0 0 ,First,#,'+ZONING_INTERNAL+',ZONING,-1,-1;ORDINANCE "ORDINANCE" true true false 150 Text 0 0 ,First,#,'+ZONING_INTERNAL+',ORDINANCE,-1,-1;ENACTED "ENACTED" true true false 50 Text 0 0 ,First,#,'+ZONING_INTERNAL+',ENACTED,-1,-1;LAST_AMENDED "LAST AMENDED" true true false 50 Text 0 0 ,First,#,'+ZONING_INTERNAL+',LAST_AMENDED,-1,-1;EDITED "EDITED" true true false 8 Date 0 0 ,First,#,'+ZONING_INTERNAL+',EDITED,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+ZONING_INTERNAL+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+ZONING_INTERNAL+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+ZONING_INTERNAL+',Shape.STLength(),-1,-1', "")
    Zoning_Dist_Web_result = arcpy.GetCount_management(ZONING_WEB)
    print ('{} has {} records'.format(ZONING_WEB, Zoning_Dist_Web_result[0]))
except:
    print ("\n Unable to append Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Zoning Districts - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

print ("\n Updating Crawford County LERTA zones - PUBLIC_WEB from AGOL_EDIT")
write_log("\n Updating Crawford County LERTA zones - PUBLIC_WEB from AGOL_EDIT: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Crawford County LERTA zones - PUBLIC_WEB
    arcpy.DeleteRows_management(CC_LERTA_WEB)
except:
    print ("\n Unable to delete rows from Crawford County LERTA zones - PUBLIC_WEB")
    write_log("Unable to delete rows from Crawford County LERTA zones - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Crawford County LERTA zones - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Crawford County LERTA zones - PUBLIC_WEB from AGOL_EDIT
    arcpy.Append_management(CC_LERTA_AGOL, CC_LERTA_WEB, "NO_TEST", 'COUNTY_FIPS "County FIPS" true true false 30 Text 0 0 ,First,#,'+CC_LERTA_AGOL+',COUNTY_FIPS,-1,-1;COUNTY_NAME "County Name" true true false 30 Text 0 0 ,First,#,'+CC_LERTA_AGOL+',COUNTY_NAME,-1,-1;ORDINANCE "Ordinance" true true false 150 Text 0 0 ,First,#,'+CC_LERTA_AGOL+',ORDINANCE,-1,-1;LERTA_TERMS "LERTA Terms" true true false 300 Text 0 0 ,First,#,'+CC_LERTA_AGOL+',LERTA_TERMS,-1,-1;LERTA_STATUS "LERTA Status" true true false 8 Double 8 38 ,First,#,'+CC_LERTA_AGOL+',LERTA_STATUS,-1,-1;SUNSET_DATE "Sunset Date" true true false 8 Date 0 0 ,First,#,'+CC_LERTA_AGOL+',SUNSET_DATE,-1,-1;HYPERLINK "Weblink" true true false 400 Text 0 0 ,First,#,'+CC_LERTA_AGOL+',HYPERLINK,-1,-1;CONTACT "Contact" true true false 50 Text 0 0 ,First,#,'+CC_LERTA_AGOL+',CONTACT,-1,-1;CONTACT_PHONE "Contact Phone" true true false 50 Text 0 0 ,First,#,'+CC_LERTA_AGOL+',CONTACT_PHONE,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+CC_LERTA_AGOL+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+CC_LERTA_AGOL+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+CC_LERTA_AGOL+',Shape.STLength(),-1,-1', "")
    CC_LERTA_WEB_result = arcpy.GetCount_management(CC_LERTA_WEB)
    print ('{} has {} records'.format(CC_LERTA_WEB, CC_LERTA_WEB_result[0]))
except:
    print ("\n Unable to append Crawford County LERTA zones - PUBLIC_WEB from AGOL_EDIT")
    write_log("Unable to append Crawford County LERTA zones - PUBLIC_WEB from AGOL_EDIT", logfile)
    logging.exception('Got exception on append Crawford County LERTA zones - PUBLIC_WEB from AGOL_EDIT logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Crawford County LERTA zones - PUBLIC_WEB from AGOL_EDIT completed")
write_log("       Updating Crawford County LERTA zones - PUBLIC_WEB from AGOL_EDIT completed", logfile)

print ("\n Updating Local Municipal LERTA zones - PUBLIC_WEB from AGOL_EDIT")
write_log("\n Updating Local Municipal LERTA zones - PUBLIC_WEB from AGOL_EDIT: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Local Municipal LERTA zones - PUBLIC_WEB
    arcpy.DeleteRows_management(MUNI_LERTA_WEB)
except:
    print ("\n Unable to delete rows from Local Municipal LERTA zones - PUBLIC_WEB")
    write_log("Unable to delete rows from Local Municipal LERTA zones - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Local Municipal LERTA zones - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Local Municipal LERTA zones - PUBLIC_WEB from AGOL_EDIT
    arcpy.Append_management(MUNI_LERTA_AGOL, MUNI_LERTA_WEB, "NO_TEST", 'Municipality "Municipality" true false false 50 Text 0 0 ,First,#,'+MUNI_LERTA_AGOL+',Municipality,-1,-1;Muni_FIPS "Muni_FIPS" true true false 8 Double 8 38 ,First,#,'+MUNI_LERTA_AGOL+',Muni_FIPS,-1,-1;ORDINANCE "ORDINANCE" true true false 150 Text 0 0 ,First,#,'+MUNI_LERTA_AGOL+',ORDINANCE,-1,-1;LERTA_TERMS "LERTA_TERMS" true true false 300 Text 0 0 ,First,#,'+MUNI_LERTA_AGOL+',LERTA_TERMS,-1,-1;LERTA_STATUS "LERTA_STATUS" true true false 8 Double 8 38 ,First,#,'+MUNI_LERTA_AGOL+',LERTA_STATUS,-1,-1;SUNSET_DATE "SUNSET_DATE" true true false 8 Date 0 0 ,First,#,'+MUNI_LERTA_AGOL+',SUNSET_DATE,-1,-1;HYPERLINK "HYPERLINK" true true false 400 Text 0 0 ,First,#,'+MUNI_LERTA_AGOL+',HYPERLINK,-1,-1;CONTACT "CONTACT" true true false 50 Text 0 0 ,First,#,'+MUNI_LERTA_AGOL+',CONTACT,-1,-1;CONTACT_PHONE "CONTACT_PHONE" true true false 50 Text 0 0 ,First,#,'+MUNI_LERTA_AGOL+',CONTACT_PHONE,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+MUNI_LERTA_AGOL+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+MUNI_LERTA_AGOL+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+MUNI_LERTA_AGOL+',Shape.STLength(),-1,-1', "")
    MUNI_LERTA_WEB_result = arcpy.GetCount_management(MUNI_LERTA_WEB)
    print ('{} has {} records'.format(MUNI_LERTA_WEB, MUNI_LERTA_WEB_result[0]))
except:
    print ("\n Unable to append Local Municipal LERTA zones - PUBLIC_WEB from AGOL_EDIT")
    write_log("Unable to append Local Municipal LERTA zones - PUBLIC_WEB from AGOL_EDIT", logfile)
    logging.exception('Got exception on append Local Municipal LERTA zones - PUBLIC_WEB from AGOL_EDIT logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Local Municipal LERTA zones - PUBLIC_WEB from AGOL_EDIT completed")
write_log("       Updating Local Municipal LERTA zones - PUBLIC_WEB from AGOL_EDIT completed", logfile)

print ("\n Updating School District LERTA zones - PUBLIC_WEB from AGOL_EDIT")
write_log("\n Updating School District LERTA zones - PUBLIC_WEB from AGOL_EDIT: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from School District LERTA zones - PUBLIC_WEB
    arcpy.DeleteRows_management(SCHOOL_LERTA_WEB)
except:
    print ("\n Unable to delete rows from School District LERTA zones - PUBLIC_WEB")
    write_log("Unable to delete rows from School District LERTA zones - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from School District LERTA zones - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append School District LERTA zones - PUBLIC_WEB from AGOL_EDIT
    arcpy.Append_management(SCHOOL_LERTA_AGOL, SCHOOL_LERTA_WEB, "NO_TEST", 'School_District_Name "School_District_Name" true true false 255 Text 0 0 ,First,#,'+SCHOOL_LERTA_AGOL+',School_District_Name,-1,-1;School_District_Code "School District Code" true true false 8 Double 8 38 ,First,#,'+SCHOOL_LERTA_AGOL+',School_District_Code,-1,-1;ORDINANCE "Ordinance" true true false 150 Text 0 0 ,First,#,'+SCHOOL_LERTA_AGOL+',ORDINANCE,-1,-1;LERTA_TERMS "LERTA Terms" true true false 300 Text 0 0 ,First,#,'+SCHOOL_LERTA_AGOL+',LERTA_TERMS,-1,-1;LERTA_STATUS "LERTA Status" true true false 8 Double 8 38 ,First,#,'+SCHOOL_LERTA_AGOL+',LERTA_STATUS,-1,-1;SUNSET_DATE "Sunset Date" true true false 8 Date 0 0 ,First,#,'+SCHOOL_LERTA_AGOL+',SUNSET_DATE,-1,-1;HYPERLINK "Weblink" true true false 400 Text 0 0 ,First,#,'+SCHOOL_LERTA_AGOL+',HYPERLINK,-1,-1;CONTACT "Contact" true true false 50 Text 0 0 ,First,#,'+SCHOOL_LERTA_AGOL+',CONTACT,-1,-1;CONTACT_PHONE "Contact Phone" true true false 50 Text 0 0 ,First,#,'+SCHOOL_LERTA_AGOL+',CONTACT_PHONE,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+SCHOOL_LERTA_AGOL+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+SCHOOL_LERTA_AGOL+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+SCHOOL_LERTA_AGOL+',Shape.STLength(),-1,-1', "")
    SCHOOL_LERTA_WEB_result = arcpy.GetCount_management(SCHOOL_LERTA_WEB)
    print ('{} has {} records'.format(SCHOOL_LERTA_WEB, SCHOOL_LERTA_WEB_result[0]))
except:
    print ("\n Unable to append School District LERTA zones - PUBLIC_WEB from AGOL_EDIT")
    write_log("Unable to append School District LERTA zones - PUBLIC_WEB from AGOL_EDIT", logfile)
    logging.exception('Got exception on append School District LERTA zones - PUBLIC_WEB from AGOL_EDIT logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating School District LERTA zones - PUBLIC_WEB from AGOL_EDIT completed")
write_log("       Updating School District LERTA zones - PUBLIC_WEB from AGOL_EDIT completed", logfile)

print ("\n Updating Crawford County Submarkets - CRAW_INTERNAL from PLANNING")
write_log("\n Updating Crawford County Submarkets - CRAW_INTERNAL from PLANNING: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Crawford County Submarkets - CRAW_INTERNAL
    arcpy.DeleteRows_management(CC_SUBMARKETS_INTERNAL)
except:
    print ("\n Unable to delete rows from Crawford County Submarkets - CRAW_INTERNAL")
    write_log("Unable to delete rows from Crawford County Submarkets - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Crawford County Submarkets - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Crawford County Submarkets - CRAW_INTERNAL from PLANNING
    arcpy.Append_management(CC_SUBMARKETS_PLANNING, CC_SUBMARKETS_INTERNAL, "NO_TEST", 'Name "Submarket Name" true true false 50 Text 0 0 ,First,#,'+CC_SUBMARKETS_PLANNING+',Name,-1,-1;Subregion "County Subregion" true true false 50 Text 0 0 ,First,#,'+CC_SUBMARKETS_PLANNING+',Subregion,-1,-1;Population "Population" true true false 2 Short 0 5 ,First,#,'+CC_SUBMARKETS_PLANNING+',Population,-1,-1;Employed_Workers "Employed Workers" true true false 2 Short 0 5 ,First,#,'+CC_SUBMARKETS_PLANNING+',Employed_Workers,-1,-1;Date_Created "Date Created" true true false 8 Date 0 0 ,First,#,'+CC_SUBMARKETS_PLANNING+',Date_Created,-1,-1;Date_Edited "Date Edited" true true false 8 Date 0 0 ,First,#,'+CC_SUBMARKETS_PLANNING+',Date_Edited,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+CC_SUBMARKETS_PLANNING+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+CC_SUBMARKETS_PLANNING+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+CC_SUBMARKETS_PLANNING+',Shape.STLength(),-1,-1', "")
    CC_SUBMARKETS_INTERNAL_result = arcpy.GetCount_management(CC_SUBMARKETS_INTERNAL)
    print ('{} has {} records'.format(CC_SUBMARKETS_INTERNAL, CC_SUBMARKETS_INTERNAL_result[0]))
except:
    print ("\n Unable to append Crawford County Submarkets - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append Crawford County Submarkets - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append Crawford County Submarkets - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Crawford County Submarkets - CRAW_INTERNAL from PLANNING completed")
write_log("       Updating Crawford County Submarkets - CRAW_INTERNAL from PLANNING completed", logfile)

print ("\n Updating Crawford County Submarkets - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Crawford County Submarkets - PUBLIC_WEB from CRAW_INTERNAL: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Crawford County Submarkets - PUBLIC_WEB
    arcpy.DeleteRows_management(CC_SUBMARKETS_WEB)
except:
    print ("\n Unable to delete rows from Crawford County Submarkets - PUBLIC_WEB")
    write_log("Unable to delete rows from Crawford County Submarkets - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Crawford County Submarkets - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Crawford County Submarkets - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(CC_SUBMARKETS_INTERNAL, CC_SUBMARKETS_WEB, "NO_TEST", 'Name "Submarket Name" true true false 50 Text 0 0 ,First,#,'+CC_SUBMARKETS_INTERNAL+',Name,-1,-1;Subregion "County Subregion" true true false 50 Text 0 0 ,First,#,'+CC_SUBMARKETS_INTERNAL+',Subregion,-1,-1;Population "Population" true true false 2 Short 0 5 ,First,#,'+CC_SUBMARKETS_INTERNAL+',Population,-1,-1;Employed_Workers "Employed Workers" true true false 2 Short 0 5 ,First,#,'+CC_SUBMARKETS_INTERNAL+',Employed_Workers,-1,-1;Date_Created "Date Created" true true false 8 Date 0 0 ,First,#,'+CC_SUBMARKETS_INTERNAL+',Date_Created,-1,-1;Date_Edited "Date Edited" true true false 8 Date 0 0 ,First,#,'+CC_SUBMARKETS_INTERNAL+',Date_Edited,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+CC_SUBMARKETS_INTERNAL+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+CC_SUBMARKETS_INTERNAL+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+CC_SUBMARKETS_INTERNAL+',Shape.STLength(),-1,-1', "")
    CC_SUBMARKETS_WEB_result = arcpy.GetCount_management(CC_SUBMARKETS_WEB)
    print ('{} has {} records'.format(CC_SUBMARKETS_WEB, CC_SUBMARKETS_WEB_result[0]))
except:
    print ("\n Unable to append Crawford County Submarkets - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Crawford County Submarkets - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Crawford County Submarkets - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Crawford County Submarkets - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Crawford County Submarkets - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

print ("\n Updating Crawford County Submarkets - CRAW_INTERNAL from PLANNING")
write_log("\n Updating Crawford County Submarkets - CRAW_INTERNAL from PLANNING: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Crawford County Subregions - CRAW_INTERNAL
    arcpy.DeleteRows_management(CC_SUBREGIONS_INTERNAL)
except:
    print ("\n Unable to delete rows from Crawford County Subregions - CRAW_INTERNAL")
    write_log("Unable to delete rows from Crawford County Subregions - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Crawford County Subregions - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Crawford County Subregions - CRAW_INTERNAL from PLANNING
    arcpy.Append_management(CC_SUBREGIONS_PLANNING, CC_SUBREGIONS_INTERNAL, "NO_TEST", 'Subregion "County Subregion" true true false 50 Text 0 0 ,First,#,'+CC_SUBREGIONS_PLANNING+',Subregion,-1,-1;Date_Created "MIN_Date_Created" true true false 8 Date 0 0 ,First,#,'+CC_SUBREGIONS_PLANNING+',Date_Created,-1,-1;Date_Edited "MIN_Date_Edited" true true false 8 Date 0 0 ,First,#,'+CC_SUBREGIONS_PLANNING+',Date_Edited,-1,-1;Employed_Workers "SUM_Employed_Workers" true true false 8 Double 8 38 ,First,#,'+CC_SUBREGIONS_PLANNING+',Employed_Workers,-1,-1;Population "SUM_Population" true true false 8 Double 8 38 ,First,#,'+CC_SUBREGIONS_PLANNING+',Population,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+CC_SUBREGIONS_PLANNING+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+CC_SUBREGIONS_PLANNING+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+CC_SUBREGIONS_PLANNING+',Shape.STLength(),-1,-1', "")
    CC_SUBREGIONS_INTERNAL_result = arcpy.GetCount_management(CC_SUBREGIONS_INTERNAL)
    print ('{} has {} records'.format(CC_SUBREGIONS_INTERNAL, CC_SUBREGIONS_INTERNAL_result[0]))
except:
    print ("\n Unable to append Crawford County Subregions - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append Crawford County Subregions - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append Crawford County Subregions - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Crawford County Subregions - CRAW_INTERNAL from PLANNING completed")
write_log("       Updating Crawford County Subregions - CRAW_INTERNAL from PLANNING completed", logfile)

print ("\n Updating Crawford County Submarkets - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Crawford County Submarkets - PUBLIC_WEB from CRAW_INTERNAL: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Crawford County Subregions - PUBLIC_WEB
    arcpy.DeleteRows_management(CC_SUBREGIONS_WEB)
except:
    print ("\n Unable to delete rows from Crawford County Subregions - PUBLIC_WEB")
    write_log("Unable to delete rows from Crawford County Subregions - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Crawford County Subregions - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Crawford County Subregions - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(CC_SUBREGIONS_INTERNAL, CC_SUBREGIONS_WEB, "NO_TEST", 'Subregion "County Subregion" true true false 50 Text 0 0 ,First,#,'+CC_SUBREGIONS_INTERNAL+',Subregion,-1,-1;Date_Created "MIN_Date_Created" true true false 8 Date 0 0 ,First,#,'+CC_SUBREGIONS_INTERNAL+',Date_Created,-1,-1;Date_Edited "MIN_Date_Edited" true true false 8 Date 0 0 ,First,#,'+CC_SUBREGIONS_INTERNAL+',Date_Edited,-1,-1;Employed_Workers "SUM_Employed_Workers" true true false 8 Double 8 38 ,First,#,'+CC_SUBREGIONS_INTERNAL+',Employed_Workers,-1,-1;Population "SUM_Population" true true false 8 Double 8 38 ,First,#,'+CC_SUBREGIONS_INTERNAL+',Population,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+CC_SUBREGIONS_INTERNAL+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+CC_SUBREGIONS_INTERNAL+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+CC_SUBREGIONS_INTERNAL+',Shape.STLength(),-1,-1', "")
    CC_SUBREGIONS_WEB_result = arcpy.GetCount_management(CC_SUBREGIONS_WEB)
    print ('{} has {} records'.format(CC_SUBREGIONS_WEB, CC_SUBREGIONS_WEB_result[0]))
except:
    print ("\n Unable to append Crawford County Subregions - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Crawford County Subregions - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Crawford County Subregions - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Crawford County Subregions - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Crawford County Subregions - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL PLANNING DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL PLANNING DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
