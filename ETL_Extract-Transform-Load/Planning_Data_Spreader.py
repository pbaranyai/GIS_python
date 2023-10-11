# ---------------------------------------------------------------------------
# Planning_Data_Spreader.py
# Created on: 2019-10-01 
# Updated on 2021-10-22
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL as needed:
#
# Zoning Districts
# Crawford County LERTA zones
# Local Municipal LERTA zones
# Schoool District LERTA zones
# Crawford County Submarkets
# Crawford County Subregions
# Act 13 Projects
# BARA_SBA Locations
# CDBG Projects
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import datetime
import os
import logging

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\Planning\\Planning_Data_Spreader.log"  
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
Database_Connections = r"\\FILELOCATION\\GIS\\ArcAutomations\\Database_Connections"

# Database variables:
CRAW_INTERNAL = Database_Connections + "\\craw_internal@ccsde.sde"
PLANNING = Database_Connections + "\\PLANNING@ccsde.sde"

# Local variables:
CC_LERTA_PLANNING = PLANNING + "\\CCSDE.PLANNING.Investment_Incentive_Zones\\CCSDE.PLANNING.Crawford_County_LERTA_Zones"
MUNI_LERTA_PLANNING = PLANNING + "\\CCSDE.PLANNING.Investment_Incentive_Zones\\CCSDE.PLANNING.Local_Municipal_LERTA_Zones"
SCHOOL_LERTA_PLANNING = PLANNING + "\\CCSDE.PLANNING.Investment_Incentive_Zones\\CCSDE.PLANNING.School_District_LERTA_Zones"
CC_LERTA_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Planning\\CCSDE.CRAW_INTERNAL.Crawford_County_LERTA_Zones"
MUNI_LERTA_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Planning\\CCSDE.CRAW_INTERNAL.Local_Municipal_LERTA_Zones"
SCHOOL_LERTA_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Planning\\CCSDE.CRAW_INTERNAL.School_District_LERTA_Zones"
ZONING_PLANNING = PLANNING + "\\CCSDE.PLANNING.Zoning\\CCSDE.PLANNING.Crawford_County_Zoning_Districts"
ZONING_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ZONING_DISTRICTS_INTERNAL"
CC_SUBMARKETS_PLANNING = PLANNING + "\\CCSDE.PLANNING.Jurisdictional\\CCSDE.PLANNING.CC_Submarkets"
CC_SUBMARKETS_INTERNAL = CRAW_INTERNAL + "\\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.CC_Submarkets"
CC_SUBREGIONS_PLANNING = PLANNING+ "\\CCSDE.PLANNING.Jurisdictional\\CCSDE.PLANNING.CrawfordCountySubregions"
CC_SUBREGIONS_INTERNAL = CRAW_INTERNAL + "\\\CCSDE.CRAW_INTERNAL.Boundaries\\CCSDE.CRAW_INTERNAL.CrawfordCountySubregions"
ACT13_PROJECTS_PLANNING = PLANNING + "\\CCSDE.PLANNING.Comm_Dev_Projects\\CCSDE.PLANNING.Act13_Projects"
BARA_SBA_PLANNING = PLANNING + "\\CCSDE.PLANNING.Comm_Dev_Projects\\CCSDE.PLANNING.BARA_SBA_Locations"
CDBG_PROJECTS_PLANNING = PLANNING + "\\CCSDE.PLANNING.Comm_Dev_Projects\\CCSDE.PLANNING.CDBG_Projects"
ACT13_PROJECTS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Planning\\CCSDE.CRAW_INTERNAL.Act13_Projects"
BARA_SBA_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Planning\\CCSDE.CRAW_INTERNAL.BARA_SBA_Locations"
CDBG_PROJECTS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Planning\\CCSDE.CRAW_INTERNAL.CDBG_Projects"

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
print ("Act 13 Projects")
print ("BARA_SBA Locations")
print ("CDBG Projects")
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
write_log("Act 13 Projects",logfile)
write_log("BARA_SBA Locations",logfile)
write_log("CDBG Projects",logfile)
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

print ("\n Updating Crawford County LERTA zones - CRAW_INTERNAL from AGOL_EDIT")
write_log("\n Updating Crawford County LERTA zones - CRAW_INTERNAL from AGOL_EDIT: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Crawford County LERTA zones - CRAW_INTERNAL
    arcpy.DeleteRows_management(CC_LERTA_INTERNAL)
except:
    print ("\n Unable to delete rows from Crawford County LERTA zones - CRAW_INTERNAL")
    write_log("Unable to delete rows from Crawford County LERTA zones - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Crawford County LERTA zones - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Crawford County LERTA zones - CRAW_INTERNAL from PLANNING
    arcpy.Append_management(CC_LERTA_PLANNING, CC_LERTA_INTERNAL, "NO_TEST", 'COUNTY_FIPS "County FIPS" true true false 30 Text 0 0 ,First,#,'+CC_LERTA_PLANNING+',COUNTY_FIPS,-1,-1;COUNTY_NAME "County Name" true true false 30 Text 0 0 ,First,#,'+CC_LERTA_PLANNING+',COUNTY_NAME,-1,-1;ORDINANCE "Ordinance" true true false 150 Text 0 0 ,First,#,'+CC_LERTA_PLANNING+',ORDINANCE,-1,-1;LERTA_TERMS "LERTA Terms" true true false 300 Text 0 0 ,First,#,'+CC_LERTA_PLANNING+',LERTA_TERMS,-1,-1;LERTA_STATUS "LERTA Status" true true false 8 Double 8 38 ,First,#,'+CC_LERTA_PLANNING+',LERTA_STATUS,-1,-1;SUNSET_DATE "Sunset Date" true true false 8 Date 0 0 ,First,#,'+CC_LERTA_PLANNING+',SUNSET_DATE,-1,-1;HYPERLINK "Weblink" true true false 400 Text 0 0 ,First,#,'+CC_LERTA_PLANNING+',HYPERLINK,-1,-1;CONTACT "Contact" true true false 50 Text 0 0 ,First,#,'+CC_LERTA_PLANNING+',CONTACT,-1,-1;CONTACT_PHONE "Contact Phone" true true false 50 Text 0 0 ,First,#,'+CC_LERTA_PLANNING+',CONTACT_PHONE,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+CC_LERTA_PLANNING+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+CC_LERTA_PLANNING+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+CC_LERTA_PLANNING+',Shape.STLength(),-1,-1', "")
    CC_LERTA_INTERNAL_result = arcpy.GetCount_management(CC_LERTA_INTERNAL)
    print ('{} has {} records'.format(CC_LERTA_INTERNAL, CC_LERTA_INTERNAL_result[0]))
except:
    print ("\n Unable to append Crawford County LERTA zones - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append Crawford County LERTA zones - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append Crawford County LERTA zones - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Crawford County LERTA zones - CRAW_INTERNAL from AGOL_EDIT completed")
write_log("       Updating Crawford County LERTA zones - CRAW_INTERNAL from AGOL_EDIT completed", logfile)

print ("\n Updating Local Municipal LERTA zones - CRAW_INTERNAL from AGOL_EDIT")
write_log("\n Updating Local Municipal LERTA zones - CRAW_INTERNAL from AGOL_EDIT: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Local Municipal LERTA zones - CRAW_INTERNAL
    arcpy.DeleteRows_management(MUNI_LERTA_INTERNAL)
except:
    print ("\n Unable to delete rows from Local Municipal LERTA zones - CRAW_INTERNAL")
    write_log("Unable to delete rows from Local Municipal LERTA zones - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Local Municipal LERTA zones - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Local Municipal LERTA zones - CRAW_INTERNAL from PLANNING
    arcpy.Append_management(MUNI_LERTA_PLANNING, MUNI_LERTA_INTERNAL, "NO_TEST", 'Municipality "Municipality" true false false 50 Text 0 0 ,First,#,'+MUNI_LERTA_PLANNING+',Municipality,-1,-1;Muni_FIPS "Muni_FIPS" true true false 8 Double 8 38 ,First,#,'+MUNI_LERTA_PLANNING+',Muni_FIPS,-1,-1;ORDINANCE "ORDINANCE" true true false 150 Text 0 0 ,First,#,'+MUNI_LERTA_PLANNING+',ORDINANCE,-1,-1;LERTA_TERMS "LERTA_TERMS" true true false 300 Text 0 0 ,First,#,'+MUNI_LERTA_PLANNING+',LERTA_TERMS,-1,-1;LERTA_STATUS "LERTA_STATUS" true true false 8 Double 8 38 ,First,#,'+MUNI_LERTA_PLANNING+',LERTA_STATUS,-1,-1;SUNSET_DATE "SUNSET_DATE" true true false 8 Date 0 0 ,First,#,'+MUNI_LERTA_PLANNING+',SUNSET_DATE,-1,-1;HYPERLINK "HYPERLINK" true true false 400 Text 0 0 ,First,#,'+MUNI_LERTA_PLANNING+',HYPERLINK,-1,-1;CONTACT "CONTACT" true true false 50 Text 0 0 ,First,#,'+MUNI_LERTA_PLANNING+',CONTACT,-1,-1;CONTACT_PHONE "CONTACT_PHONE" true true false 50 Text 0 0 ,First,#,'+MUNI_LERTA_PLANNING+',CONTACT_PHONE,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+MUNI_LERTA_PLANNING+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+MUNI_LERTA_PLANNING+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+MUNI_LERTA_PLANNING+',Shape.STLength(),-1,-1', "")
    MUNI_LERTA_INTERNAL_result = arcpy.GetCount_management(MUNI_LERTA_INTERNAL)
    print ('{} has {} records'.format(MUNI_LERTA_INTERNAL, MUNI_LERTA_INTERNAL_result[0]))
except:
    print ("\n Unable to append Local Municipal LERTA zones - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append Local Municipal LERTA zones - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append Local Municipal LERTA zones - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Local Municipal LERTA zones - CRAW_INTERNAL from AGOL_EDIT completed")
write_log("       Updating Local Municipal LERTA zones - CRAW_INTERNAL from AGOL_EDIT completed", logfile)

print ("\n Updating School District LERTA zones - CRAW_INTERNAL from AGOL_EDIT")
write_log("\n Updating School District LERTA zones - CRAW_INTERNAL from AGOL_EDIT: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from School District LERTA zones - CRAW_INTERNAL
    arcpy.DeleteRows_management(SCHOOL_LERTA_INTERNAL)
except:
    print ("\n Unable to delete rows from School District LERTA zones - CRAW_INTERNAL")
    write_log("Unable to delete rows from School District LERTA zones - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from School District LERTA zones - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append School District LERTA zones - CRAW_INTERNAL from PLANNING
    arcpy.Append_management(SCHOOL_LERTA_PLANNING, SCHOOL_LERTA_INTERNAL, "NO_TEST", 'School_District_Name "School_District_Name" true true false 255 Text 0 0 ,First,#,'+SCHOOL_LERTA_PLANNING+',School_District_Name,-1,-1;School_District_Code "School District Code" true true false 8 Double 8 38 ,First,#,'+SCHOOL_LERTA_PLANNING+',School_District_Code,-1,-1;ORDINANCE "Ordinance" true true false 150 Text 0 0 ,First,#,'+SCHOOL_LERTA_PLANNING+',ORDINANCE,-1,-1;LERTA_TERMS "LERTA Terms" true true false 300 Text 0 0 ,First,#,'+SCHOOL_LERTA_PLANNING+',LERTA_TERMS,-1,-1;LERTA_STATUS "LERTA Status" true true false 8 Double 8 38 ,First,#,'+SCHOOL_LERTA_PLANNING+',LERTA_STATUS,-1,-1;SUNSET_DATE "Sunset Date" true true false 8 Date 0 0 ,First,#,'+SCHOOL_LERTA_PLANNING+',SUNSET_DATE,-1,-1;HYPERLINK "Weblink" true true false 400 Text 0 0 ,First,#,'+SCHOOL_LERTA_PLANNING+',HYPERLINK,-1,-1;CONTACT "Contact" true true false 50 Text 0 0 ,First,#,'+SCHOOL_LERTA_PLANNING+',CONTACT,-1,-1;CONTACT_PHONE "Contact Phone" true true false 50 Text 0 0 ,First,#,'+SCHOOL_LERTA_PLANNING+',CONTACT_PHONE,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+SCHOOL_LERTA_PLANNING+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+SCHOOL_LERTA_PLANNING+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+SCHOOL_LERTA_PLANNING+',Shape.STLength(),-1,-1', "")
    SCHOOL_LERTA_WEB_result = arcpy.GetCount_management(SCHOOL_LERTA_INTERNAL)
    print ('{} has {} records'.format(SCHOOL_LERTA_INTERNAL, SCHOOL_LERTA_WEB_result[0]))
except:
    print ("\n Unable to append School District LERTA zones - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append School District LERTA zones - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append School District LERTA zones - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating School District LERTA zones - CRAW_INTERNAL from AGOL_EDIT completed")
write_log("       Updating School District LERTA zones - CRAW_INTERNAL from AGOL_EDIT completed", logfile)

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
    logging.exception('Got exception on append CraBARA_SBA_PLANNINGwford County Subregions - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Crawford County Subregions - CRAW_INTERNAL from PLANNING completed")
write_log("       Updating Crawford County Subregions - CRAW_INTERNAL from PLANNING completed", logfile)

print ("\n Updating Act 13 Projects - CRAW_INTERNAL from PLANNING")
write_log("\n Updating Act 13 Projects - CRAW_INTERNAL from PLANNING: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Act 13 Projects - CRAW_INTERNAL
    arcpy.DeleteRows_management(ACT13_PROJECTS_INTERNAL)
except:
    print ("\n Unable to delete rows from  Act 13 Projects - CRAW_INTERNAL")
    write_log("Unable to delete rows from  Act 13 Projects - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from  Act 13 Projects - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append Act 13 Projects - CRAW_INTERNAL from PLANNING
    arcpy.management.Append(ACT13_PROJECTS_PLANNING, ACT13_PROJECTS_INTERNAL, "NO_TEST", r'NAME "Project Name" true true false 1000 Text 0 0,First,#,'+ACT13_PROJECTS_PLANNING+',NAME,0,1000;TYPE "Type of Project" true true false 300 Text 0 0,First,#,'+ACT13_PROJECTS_PLANNING+',TYPE,0,300;YEAR "Year" true true false 4 Long 0 10,First,#,'+ACT13_PROJECTS_PLANNING+',YEAR,-1,-1;RECIPIENT "Recipient" true true false 1000 Text 0 0,First,#,'+ACT13_PROJECTS_PLANNING+',RECIPIENT,0,1000;AMOUNT "Amount" true true false 4 Long 0 10,First,#,'+ACT13_PROJECTS_PLANNING+',AMOUNT,-1,-1;PURPOSE "Purpose" true true false 4000 Text 0 0,First,#,'+ACT13_PROJECTS_PLANNING+',PURPOSE,0,4000;Latitude "Latitude" true true false 8 Double 8 38,First,#,'+ACT13_PROJECTS_PLANNING+',Latitude,-1,-1;Longitude "Longitude" true true false 8 Double 8 38,First,#,'+ACT13_PROJECTS_PLANNING+',Longitude,-1,-1;LOCATION "Location" true true false 300 Text 0 0,First,#,'+ACT13_PROJECTS_PLANNING+',LOCATION,0,300;DATE_ADDED "Date Added" true true false 8 Date 0 0,First,#,'+ACT13_PROJECTS_PLANNING+',DATE_ADDED,-1,-1;DATE_EDITED "Date Last Edited" true true false 8 Date 0 0,First,#,'+ACT13_PROJECTS_PLANNING+',DATE_EDITED,-1,-1', '', '')
    ACT13Projects_result = arcpy.GetCount_management(ACT13_PROJECTS_INTERNAL)
    print ('{} has {} records'.format(ACT13_PROJECTS_INTERNAL, ACT13Projects_result[0]))
except:
    print ("\n Unable to append Act 13 Projects - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append Act 13 Projects - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append Act 13 Projects - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Act 13 Projects - CRAW_INTERNAL from PLANNING completed")
write_log("       Updating Act 13 Projects - CRAW_INTERNAL from PLANNING completed", logfile)

print ("\n Updating BARA_SBA Locations - CRAW_INTERNAL from PLANNING")
write_log("\n Updating BARA_SBA Locations - CRAW_INTERNAL from PLANNING: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from BARA_SBA Locations - CRAW_INTERNAL
    arcpy.DeleteRows_management(BARA_SBA_INTERNAL)
except:
    print ("\n Unable to delete rows from BARA_SBA Locations - CRAW_INTERNAL")
    write_log("Unable to delete rows from BARA_SBA Locations - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from BARA_SBA Locations - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append BARA_SBA Locations - CRAW_INTERNAL from PLANNING
    arcpy.management.Append(BARA_SBA_PLANNING, BARA_SBA_INTERNAL, "NO_TEST", r'TYPE "Type" true true false 10 Text 0 0,First,#,'+BARA_SBA_PLANNING+',TYPE,0,10;TYPE_2 "Type 2" true true false 50 Text 0 0,First,#,'+BARA_SBA_PLANNING+',TYPE_2,0,50;NAME "Business Name" true true false 200 Text 0 0,First,#,'+BARA_SBA_PLANNING+',NAME,0,200;STREET "Street Address" true true false 150 Text 0 0,First,#,'+BARA_SBA_PLANNING+',STREET,0,150;CITY "City" true true false 100 Text 0 0,First,#,'+BARA_SBA_PLANNING+',CITY,0,100;STATE "State" true true false 2 Text 0 0,First,#,'+BARA_SBA_PLANNING+',STATE,0,2;ZIP "Zipcode" true true false 8 Double 8 38,First,#,'+BARA_SBA_PLANNING+',ZIP,-1,-1;MUNICIPALITY "Municipality Name" true true false 100 Text 0 0,First,#,'+BARA_SBA_PLANNING+',MUNICIPALITY,0,100;MUNI_FIPS "Municipal FIPS code" true true false 8 Double 8 38,First,#,'+BARA_SBA_PLANNING+',MUNI_FIPS,-1,-1;COUNTY_FIPS "County FIPS code" true true false 8 Double 8 38,First,#,'+BARA_SBA_PLANNING+',COUNTY_FIPS,-1,-1;PRE_COVID_JOBS "Pre-COVID Jobs" true true false 2 Short 0 5,First,#,'+BARA_SBA_PLANNING+',PRE_COVID_JOBS,-1,-1;FALL_2020_JOBS "Fall 2020 Jobs" true true false 2 Short 0 5,First,#,'+BARA_SBA_PLANNING+',FALL_2020_JOBS,-1,-1;JOB_RETENTION_1YEAR "Job Retention - 1 year" true true false 2 Short 0 5,First,#,'+BARA_SBA_PLANNING+',JOB_RETENTION_1YEAR,-1,-1;AWARD "Award" true true false 8 Double 8 38,First,#,'+BARA_SBA_PLANNING+',AWARD,-1,-1', '', '')
    BARALocations_result = arcpy.GetCount_management(BARA_SBA_INTERNAL)
    print ('{} has {} records'.format(BARA_SBA_INTERNAL, BARALocations_result[0]))
except:
    print ("\n Unable to append BARA_SBA Locations - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append BARA_SBA Locations - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append BARA_SBA Locations - CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating BARA_SBA Locations - CRAW_INTERNAL from PLANNING completed")
write_log("       Updating BARA_SBA Locations - CRAW_INTERNAL from PLANNING completed", logfile)


print ("\n Updating CDBG Projects - CRAW_INTERNAL from PLANNING")
write_log("\n Updating CDBG Projects - CRAW_INTERNAL from PLANNING: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from CDBG Projects - CRAW_INTERNAL
    arcpy.DeleteRows_management(CDBG_PROJECTS_INTERNAL)
except:
    print ("\n Unable to delete rows from CDBG Projects - CRAW_INTERNAL")
    write_log("Unable to delete rows from CDBG Projects - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from CDBG Projects - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:   
    # Append CDBG Projects - CRAW_INTERNAL from PLANNING
    arcpy.management.Append(CDBG_PROJECTS_PLANNING, CDBG_PROJECTS_INTERNAL, "NO_TEST", r'NAME "Project Name" true true false 40 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',NAME,0,40;TYPE "Project Type" true true false 50 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',TYPE,0,50;LOCATION "Project Location" true true false 50 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',LOCATION,0,50;YEAR "Project Year" true true false 50 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',YEAR,0,50;Amount "Project Amount" true true false 4 Long 0 10,First,#,'+CDBG_PROJECTS_INTERNAL+',Amount,-1,-1;Add_Date "Add date" true true false 8 Date 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',Add_Date,-1,-1;Edit_Date "Last edit date" true true false 8 Date 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',Edit_Date,-1,-1;STATUS "Status" true true false 8 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',STATUS,0,8;MATRIX_CODE "Matrix Code" true true false 5 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',MATRIX_CODE,0,5;LMI_SERVED "LMI served" true true false 2 Short 0 5,First,#,'+CDBG_PROJECTS_INTERNAL+',LMI_SERVED,-1,-1;NAT_OBJ "National Objective Categories" true true false 25 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',NAT_OBJ,0,25;ALLOCATION "Allocation" true true false 10 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',ALLOCATION,0,10;DESCRIPTION "Description" true true false 200 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',DESCRIPTION,0,200;ERR_TYPE "ERR Type" true true false 50 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',ERR_TYPE,0,50;ERR_DATE "ERR Date" true true false 8 Date 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',ERR_DATE,-1,-1;CONTRACTOR "Contractor" true true false 50 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',CONTRACTOR,0,50;CONTRACTOR_WBE "Contractor WBE" true true false 5 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',CONTRACTOR_WBE,0,5;CONTRACTOR_MBE "Contractor MBE" true true false 5 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',CONTRACTOR_MBE,0,5;CONTRACTOR_SEC3 "Contractor Sec 3" true true false 5 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',CONTRACTOR_SEC3,0,5;CONTRACTOR_NOTES "Contractor Notes" true true false 200 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',CONTRACTOR_NOTES,0,200;SUBCONTRACTOR "Subcontractor" true true false 50 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',SUBCONTRACTOR,0,50;SUBCONTRACTOR_WBE "Subcontractor WBE" true true false 5 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',SUBCONTRACTOR_WBE,0,5;SUBCONTRACTOR_MBE "Subcontractor MBE" true true false 5 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',SUBCONTRACTOR_MBE,0,5;SUBCONTRACTOR_SEC3 "Subcontractor Sec 3" true true false 5 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',SUBCONTRACTOR_SEC3,0,5;SUBCONTRACTOR_NOTES "Subcontractor Notes" true true false 200 Text 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',SUBCONTRACTOR_NOTES,0,200;COMPLETION_DATE "Completion Date" true true false 8 Date 0 0,First,#,'+CDBG_PROJECTS_INTERNAL+',COMPLETION_DATE,-1,-1', '', '')
    CDBGProjects_result = arcpy.GetCount_management(CDBG_PROJECTS_INTERNAL)
    print ('{} has {} records'.format(CDBG_PROJECTS_INTERNAL, CDBGProjects_result[0]))
except:
    print ("\n Unable to append CDBG Projects - CRAW_INTERNAL from PLANNING")
    write_log("Unable to append CDBG Projects - CRAW_INTERNAL from PLANNING", logfile)
    logging.exception('Got exception on append CDBG Projects- CRAW_INTERNAL from PLANNING logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating CDBG Projects - CRAW_INTERNAL from PLANNING completed")
write_log("       Updating CDBG Projects - CRAW_INTERNAL from PLANNING completed", logfile)


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
