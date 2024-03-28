# ---------------------------------------------------------------------------
# LandRecords_Data_Spreader.py
# Created on: 2019-03-05 
# Updated on 2021-09-21
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# AED_LOCATIONS  
# ALS_ZONES
# ATV_COVERAGE 
# BLS_COVERAGE
# EHS_FACILITIES
# FIRE_DEPARTMENT_COVERAGE
# FIRE_GRIDS
# LANDMARKS
# POLICE_DEPARTMENT_COVERAGE
# PUBLIC_SAFETY_DEPARTMENTS
# QRS_DEPARTMENT_COVERAGE
# RED_CROSS_SHELTERS
# RESCUE_DEPARTMENT_COVERAGE
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
# ---------------------------------------------------------------------------

# Import modules
import sys,arcpy,time,datetime,logging

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\GIS\\PublicSafety_Data_Spreader.log"  
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

#Database Connection Folder
Database_Connections = r"\\FILELOCATION\\GIS\\ArcAutomations\\Database_Connections"

# Database variables:
CRAW_INTERNAL = Database_Connections + "\\craw_internal@ccsde.sde"
PUBLIC_SAFETY = Database_Connections + "\\PUBLIC_SAFETY@ccsde.sde"

# Local variables:
AED_LOCATIONS_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS"
AED_LOCATIONS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.AED_LOCATIONS_INTERNAL"
ALS_ZONES_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ALS_ZONES"
ALS_ZONES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.ALS_ZONES_INTERNAL"
ATV_COVERAGE_PS = PUBLIC_SAFETY + "\\\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ATV_COVERAGES"
ATV_COVERAGE_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.ATV_COVERAGES_INTERNAL"
BLS_COVERAGE_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.BLS_COVERAGE_INTERNAL"
EHS_FACILITIES_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES"
EHS_FACILITIES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.EHS_FACILITIES_INTERNAL"
ESZ_ALL_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ESZ_ALL"
FIRE_DEPT_COVERAGE_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.FIRE_DEPT_COVERAGE_INTERNAL"
FIRE_GRIDS_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.FIRE_GRIDS"
FIRE_GRIDS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.FIRE_GRIDS_INTERNAL"
LANDMARKS_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.LANDMARKS"
LANDMARKS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.LANDMARKS_INTERNAL"
POLICE_DEPT_COVERAGE_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.POLICE_DEPT_COVERAGE_INTERNAL"
PUBLIC_SAFETY_DEPARTMENTS_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS"
PUBLIC_SAFETY_DEPARTMENTS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.PUBLIC_SAFETY_DEPT_INTERNAL"
QRS_DEPT_COVERAGE_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.QRS_DEPT_COVERAGE_INTERNAL"
RED_CROSS_SHELTERS_PS = PUBLIC_SAFETY + "\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS"
RED_CROSS_SHELTERS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.RED_CROSS_SHELTERS_INTERNAL"
RESCUE_DEPT_COVERAGE_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Public_Safety\\CCSDE.CRAW_INTERNAL.RESCUE_DEPT_COVERAGE_INTERNAL"

start_time = time.time()

print ("============================================================================")
print ("Updating Public Safety: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nAED Locations Feature Class")
print ("ALS Zones Feature Class")
print ("ATV Coverage Feature Class")
print ("BLS Coverage Feature Class")
print ("EHS Facilities Feature Class")
print ("Fire Department Coverage Feature Class")
print ("Fire Grids Feature Class")
print ("Landmarks Feature Class")
print ("Police Department Coverage Feature Class")
print ("Public Safety Departments Feature Class")
print ("QRS Department Coverage Feature Class")
print ("Red Cross Shelters Feature Class")
print ("Rescue Department Coverage Feature Class")
print ("\n From source to CRAW_INTERNAL (where applicable)")
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Public Safety: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nAED Locations Feature Class", logfile)  
write_log("ALS Zones Feature Class", logfile)
write_log("ATV Coverage Feature Class", logfile)
write_log("BLS Coverage Feature Class", logfile)
write_log("EHS Facilities Feature Class", logfile)
write_log("Fire Department Coverage Feature Class", logfile) 
write_log("Fire Grids Feature Class", logfile)
write_log("Landmarks Feature Class", logfile)
write_log("Police Department Coverage Feature Class", logfile)
write_log("Public Safety Departments Feature Class", logfile)
write_log("QRS Department Coverage Feature Class", logfile)
write_log("Red Cross Shelters Feature Class", logfile)
write_log("Rescue Department Coverage Feature Class", logfile)
write_log("\n From source to CRAW_INTERNAL (where applicable)", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Updating AED - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating AED - CRAW_INTERNAL from PUBLIC_SAFETY: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from AED - CRAW_INTERNAL
    arcpy.DeleteRows_management(AED_LOCATIONS_INTERNAL)
except:
    print ("\n Unable to delete rows from AED - CRAW_INTERNAL")
    write_log("Unable to delete rows from AED - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from AED - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Append AED - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(AED_LOCATIONS_PS, AED_LOCATIONS_INTERNAL, "NO_TEST", "ORGANIZATION_NAME \"ORGANIZATION NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS,ORGANIZATION_NAME,-1,-1;LOCATION_ONSITE \"LOCATION ONSITE\" true true false 100 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS,LOCATION_ONSITE,-1,-1;STREET_ADDRESS \"ADDRESS # & FULL STREET NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS,STREET_ADDRESS,-1,-1;POST_OFFICE \"POST OFFICE\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS,POST_OFFICE,-1,-1;ZIPCODE \"ZIPCODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS,ZIPCODE,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.AED_LOCATIONS,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    AED_Internal_result = arcpy.GetCount_management(AED_LOCATIONS_INTERNAL)
    print ('{} has {} records'.format(AED_LOCATIONS_INTERNAL, AED_Internal_result[0]))
    write_log('{} has {} records'.format(AED_LOCATIONS_INTERNAL, AED_Internal_result[0]), logfile)
except:
    print ("\n Unable to append AED - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append AED - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append AED - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating AED - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating AED - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating ATV Coverage - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating ATV Coverage from PUBLIC_SAFETY: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from ATV Coverage - CRAW_INTERNAL
    arcpy.DeleteRows_management(ATV_COVERAGE_INTERNAL)
except:
    print ("\n Unable to delete rows from ATV Coverage - CRAW_INTERNAL")
    write_log("Unable to delete rows from ATV Coverage - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from ATV Coverage - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Process: Append ATV Coverage - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(ATV_COVERAGE_PS, ATV_COVERAGE_INTERNAL, "NO_TEST", 'UNIT "UNIT #" true true false 10 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ATV_COVERAGES,UNIT,-1,-1;DEPARTMENT "DEPARTMENT NAME" true true false 100 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ATV_COVERAGES,DEPARTMENT,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ATV_COVERAGES,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ATV_COVERAGES,COUNTY_FIPS,-1,-1;UPDATE_DATE "UPDATE_DATE" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ATV_COVERAGES,UPDATE_DATE,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ATV_COVERAGES,SHAPE.STArea(),-1,-1;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ATV_COVERAGES,SHAPE.STLength(),-1,-1', "")
    ATV_Internal_result = arcpy.GetCount_management(ATV_COVERAGE_INTERNAL)
    print ('{} has {} records'.format(ATV_COVERAGE_INTERNAL, ATV_Internal_result[0]))
    write_log('{} has {} records'.format(ATV_COVERAGE_INTERNAL, ATV_Internal_result[0]), logfile)
except:
    print ("\n Unable to append ATV Coverage - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append ATV Coverage - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append ATV Coverage - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating ATV Coverage - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating ATV Coverage - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating LANDMARKS - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating LANDMARKS - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete Rows from LANDMARKS - CRAW_INTERNAL
    arcpy.DeleteRows_management(LANDMARKS_INTERNAL)
except:
    print ("\n Unable to delete rows from LANDMARKS - CRAW_INTERNAL")
    write_log("Unable to delete rows from LANDMARKS - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from LANDMARKS - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append LANDMARKS - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(LANDMARKS_PS, LANDMARKS_INTERNAL, "NO_TEST", "LANDMARK_NAME \"LANDMARK NAME\" true true false 75 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.LANDMARKS,LANDMARK_NAME,-1,-1;LM_TYPE \"LM_TYPE\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.LANDMARKS,LM_TYPE,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.LANDMARKS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.LANDMARKS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.LANDMARKS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.LANDMARKS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.LANDMARKS,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    Landmark_Internal_result = arcpy.GetCount_management(LANDMARKS_INTERNAL)
    print ('{} has {} records'.format(LANDMARKS_INTERNAL, Landmark_Internal_result[0]))
    write_log('{} has {} records'.format(LANDMARKS_INTERNAL, Landmark_Internal_result[0]), logfile)
except:
    print ("\n Unable to append LANDMARKS - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append LANDMARKS - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append LANDMARKS - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating LANDMARKS - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating LANDMARKS - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating RED CROSS SHELTERS - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating RED CROSS SHELTERS - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete Rows from RED CROSS SHELTERS - CRAW_INTERNAL
    arcpy.DeleteRows_management(RED_CROSS_SHELTERS_INTERNAL)
except:
    print ("\n Unable to delete rows from RED CROSS SHELTERS - CRAW_INTERNAL")
    write_log("Unable to delete rows from RED CROSS SHELTERS - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from RED CROSS SHELTERS - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append RED CROSS SHELTERS - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(RED_CROSS_SHELTERS_PS, RED_CROSS_SHELTERS_INTERNAL, "NO_TEST", "HSENUMBER \"ADDRESS #\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,HSENUMBER,-1,-1;STREET \"FULL STREET NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,STREET,-1,-1;POST_OFFICE \"POST OFFICE\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,POST_OFFICE,-1,-1;ZIPCODE \"ZIPCODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,ZIPCODE,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,MUNI_FIPS,-1,-1;FACILITY_NAME \"FACILITY NAME\" true true false 150 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,FACILITY_NAME,-1,-1;EVACUATION_CAP \"EVACUATION CAPACITY\" true true false 4 Long 0 10 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,EVACUATION_CAP,-1,-1;POST_EVAC_CAP \"POST EVACUATION CAPACITY\" true true false 4 Long 0 10 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,POST_EVAC_CAP,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.RED_CROSS_SHELTERS,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    RedCross_Internal_result = arcpy.GetCount_management(RED_CROSS_SHELTERS_INTERNAL)
    print ('{} has {} records'.format(RED_CROSS_SHELTERS_INTERNAL, RedCross_Internal_result[0]))
    write_log('{} has {} records'.format(RED_CROSS_SHELTERS_INTERNAL, RedCross_Internal_result[0]), logfile)
except:
    print ("\n Unable to append RED CROSS SHELTERS - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append RED CROSS SHELTERS - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append RED CROSS SHELTERS - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating RED CROSS SHELTERS - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating RED CROSS SHELTERS - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating ALS ZONES - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating ALS ZONES - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete Rows from ALS ZONES - CRAW_INTERNAL
    arcpy.DeleteRows_management(ALS_ZONES_INTERNAL)
except:
    print ("\n Unable to delete rows from ALS ZONES - CRAW_INTERNAL")
    write_log("Unable to delete rows from ALS ZONES - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from ALS ZONES - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append ALS ZONES - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(ALS_ZONES_PS, ALS_ZONES_INTERNAL, "NO_TEST", "ALS_ID \"ALS UNQUIE ID #\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ALS_ZONES,ALS_ID,-1,-1;ALS_NAME \"ALS SERVICE NAME\" true true false 75 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ALS_ZONES,ALS_NAME,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ALS_ZONES,UPDATE_DATE,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ALS_ZONES,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ALS_ZONES,COUNTY_FIPS,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ALS_ZONES,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.ALS_ZONES,SHAPE.STLength(),-1,-1", "")
    ALS_Internal_result = arcpy.GetCount_management(ALS_ZONES_INTERNAL)
    print ('{} has {} records'.format(ALS_ZONES_INTERNAL, ALS_Internal_result[0]))
    write_log('{} has {} records'.format(ALS_ZONES_INTERNAL, ALS_Internal_result[0]), logfile)
except:
    print ("\n Unable to append ALS ZONES - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append ALS ZONES - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append ALS ZONES - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating ALS ZONES - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating ALS ZONES - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating Fire Grids - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating Fire Grids - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete Rows from Fire Grids - CRAW_INTERNAL
    arcpy.DeleteRows_management(FIRE_GRIDS_INTERNAL)
except:
    print ("\n Unable to delete rows from Fire Grids - CRAW_INTERNAL")
    write_log("Unable to delete rows from Fire Grids - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Fire Grids - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append Fire Grids - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(FIRE_GRIDS_PS, FIRE_GRIDS_INTERNAL, "NO_TEST", "Description \"Description\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.FIRE_GRIDS,Description,-1,-1;ID \"ID\" true true false 4 Long 0 10 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.FIRE_GRIDS,ID,-1,-1;FG_UNIQUE_ID \"FG_UNIQUE_ID\" true true false 4 Long 0 10 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.FIRE_GRIDS,FG_UNIQUE_ID,-1,-1;EDIT_DATE \"EDIT_DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.FIRE_GRIDS,EDIT_DATE,-1,-1;Shape.STArea() \"Shape.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.FIRE_GRIDS,Shape.STArea(),-1,-1;Shape.STLength() \"Shape.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.FIRE_GRIDS,Shape.STLength(),-1,-1", "")
    FireGrids_Internal_result = arcpy.GetCount_management(FIRE_GRIDS_INTERNAL)
    print ('{} has {} records'.format(FIRE_GRIDS_INTERNAL, FireGrids_Internal_result[0]))
    write_log('{} has {} records'.format(FIRE_GRIDS_INTERNAL, FireGrids_Internal_result[0]), logfile)
except:
    print ("\n Unable to append Fire Grids - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append Fire Grids - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append Fire Grids - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Fire Grids - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating Fire Grids - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating Public Safety Departments - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating Public Safety Departments - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete Rows from PUBLIC_SAFETY_DEPTS - CRAW_INTERNAL
    arcpy.DeleteRows_management(PUBLIC_SAFETY_DEPARTMENTS_INTERNAL)
except:
    print ("\n Unable to delete rows from Public Safety Departments - CRAW_INTERNAL")
    write_log("Unable to delete rows from Public Safety Departments - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Public Safety Departments - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append PUBLIC SAFETY DEPTS - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(PUBLIC_SAFETY_DEPARTMENTS_PS, PUBLIC_SAFETY_DEPARTMENTS_INTERNAL, "NO_TEST", "DEPT_NAME \"DEPARTMENT NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,DEPT_NAME,-1,-1;FIRE_SVC \"FIRE SERVICE?\" true true false 1 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,FIRE_SVC,-1,-1;EMS_SVC \"EMS SERVICE?\" true true false 1 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,EMS_SVC,-1,-1;RESCUE_SVC \"RESCUE SERVICE?\" true true false 1 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,RESCUE_SVC,-1,-1;POLICE_SVC \"POLICE SERVICE?\" true true false 1 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,POLICE_SVC,-1,-1;HSENUMBER \"ADDRESS #\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,HSENUMBER,-1,-1;STREET \"FULL STREET NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,STREET,-1,-1;POST_OFFICE \"POST OFFICE\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,POST_OFFICE,-1,-1;ZIPCODE \"ZIPCODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,ZIPCODE,-1,-1;MUNI_NAME \"MUNICIPAL NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPAL FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY_FIPS\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,COUNTY_FIPS,-1,-1;WEBSITES \"WEBSITES\" true true false 100 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,WEBSITES,-1,-1;UPDATE_DATE \"UPDATE_DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.PUBLIC_SAFETY_DEPARTMENTS,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    PSDepts_Internal_result = arcpy.GetCount_management(PUBLIC_SAFETY_DEPARTMENTS_INTERNAL)
    print ('{} has {} records'.format(PUBLIC_SAFETY_DEPARTMENTS_INTERNAL, PSDepts_Internal_result[0]))
    write_log('{} has {} records'.format(PUBLIC_SAFETY_DEPARTMENTS_INTERNAL, PSDepts_Internal_result[0]), logfile)
except:
    print ("\n Unable to append Public Safety Departments - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append Public Safety Departments - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append Public Safety Departments - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Public Safety Departments - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating Public Safety Departments - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating EHS Facilities - CRAW_INTERNAL from PUBLIC_SAFETY")
write_log("\n Updating EHS Facilities - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)

try:
    # Delete Rows from EHS FACILITIES - CRAW_INTERNAL
    arcpy.DeleteRows_management(EHS_FACILITIES_INTERNAL)
except:
    print ("\n Unable to delete rows from EHS Facilities - CRAW_INTERNAL")
    write_log("Unable to delete rows from EHS Facilities - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from EHS Facilities - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append EHS FACILITIES - CRAW_INTERNAL from PUBLIC_SAFETY
    arcpy.Append_management(EHS_FACILITIES_PS, EHS_FACILITIES_INTERNAL, "NO_TEST", "HSENUMBER \"ADDRESS #\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,HSENUMBER,-1,-1;STREET_NAME \"FULL STREET NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,STREET_NAME,-1,-1;POST_OFFICE \"POST OFFICE\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,POST_OFFICE,-1,-1;ZIPCODE \"ZIPCODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,ZIPCODE,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,MUNI_FIPS,-1,-1;FACILITY_NAME \"FACILITY NAME\" true true false 75 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,FACILITY_NAME,-1,-1;LATITUDE \"LATITUDE\" true true false 20 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,LATITUDE,-1,-1;LONGITUDE \"LONGITUDE\" true true false 20 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,LONGITUDE,-1,-1;COUNTY_NAME \"COUNTY_NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY_FIPS\" true true false 8 Double 8 38 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,COUNTY_FIPS,-1,-1;UPDATE_DATE \"UPDATE_DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\PUBLIC_SAFETY@ccsde.sde\\CCSDE.PUBLIC_SAFETY.Public_Safety\\CCSDE.PUBLIC_SAFETY.EHS_FACILITIES,UPDATE_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    EHS_Internal_result = arcpy.GetCount_management(EHS_FACILITIES_INTERNAL)
    print ('{} has {} records'.format(EHS_FACILITIES_INTERNAL, EHS_Internal_result[0]))
    write_log('{} has {} records'.format(EHS_FACILITIES_INTERNAL, EHS_Internal_result[0]), logfile)
except:
    print ("\n Unable to append EHS Facilities - CRAW_INTERNAL from PUBLIC_SAFETY")
    write_log("Unable to append EHS Facilities - CRAW_INTERNAL from PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on append EHS Facilities - CRAW_INTERNAL from PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating EHS Facilities - CRAW_INTERNAL from PUBLIC_SAFETY completed")
write_log("       Updating EHS Facilities - CRAW_INTERNAL from PUBLIC_SAFETY completed", logfile)

print ("\n Updating Fire Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL)")
write_log("\n Updating Fire Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL)", logfile)

try:
    # Delete Rows from FIRE DEPT COVERAGE - CRAW_INTERNAL
    arcpy.DeleteRows_management(FIRE_DEPT_COVERAGE_INTERNAL)
except:
    print ("\n Unable to delete rows from Fire Department Coverage - CRAW_INTERNAL")
    write_log("Unable to delete rows from Fire Department Coverage - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Fire Department Coverage- CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve FIRE DEPT COVERAGE from PUBLIC_SAFETY // ESZ_ALL (dissolve ESZ_ALL polygons based on fire department fields to make fire department polygons)
    FIRE_DEPT_COVERAGE_DISSOLVE = arcpy.Dissolve_management(ESZ_ALL_PS, "in_memory/FIRE_DEPT_COVERAGE_DISSOLVE", "FIRE_DEPT;FIRE_FDID;FIRE_NUM;COUNTY_NAME;COUNTY_FIPS;DiscrpAgID;STATE", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to dissolve Fire Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY // ESZ_ALL")
    write_log("Unable to dissolve Fire Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY // ESZ_ALL", logfile)
    logging.exception('Got exception on dissolve Fire Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY // ESZ_ALL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make Feature layer from FIRE_DEPT_COVERAGE_DISSOLVE - in_memory (make temporary layer of dissolve from last step, to append in next step)
    FIRE_DEPT_DISSOLVE_Layer = arcpy.MakeFeatureLayer_management(FIRE_DEPT_COVERAGE_DISSOLVE, "FIRE_DEPT_DISSOLVE_Layer", "", "", "OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;FIRE_DEPT FIRE_DEPT VISIBLE NONE;FIRE_FDID FIRE_FDID VISIBLE NONE;FIRE_NUM FIRE_NUM VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;STATE STATE VISIBLE NONE;SHAPE_Length SHAPE_Length VISIBLE NONE;SHAPE_Area SHAPE_Area VISIBLE NONE")
except:
    print ("\n Unable to make Feature layer from FIRE_DEPT_COVERAGE_DISSOLVE - in_memory")
    write_log("Unable to make Feature layer from FIRE_DEPT_COVERAGE_DISSOLVE - in_memory", logfile)
    logging.exception('Got exception on make Feature layer from FIRE_DEPT_COVERAGE_DISSOLVE - in_memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Append FIRE DEPT COVERAGE- CRAW_INTERNAL from PUBLIC_SAFETY // ESZ_ALL (append from temporary layer created from last step)
    arcpy.Append_management(FIRE_DEPT_DISSOLVE_Layer, FIRE_DEPT_COVERAGE_INTERNAL, "NO_TEST", 'FIRE_DEPT "FIRE DEPARTMENT" true true false 50 Text 0 0 ,First,#,FIRE_DEPT_DISSOLVE_Layer,FIRE_DEPT,-1,-1;FIRE_FDID "FIRE DEPARTMENT FDID CODE" true true false 15 Text 0 0 ,First,#,FIRE_DEPT_DISSOLVE_Layer,FIRE_FDID,-1,-1;FIRE_NUM "FIRE DEPARTMENT #" true true false 10 Text 0 0 ,First,#,FIRE_DEPT_DISSOLVE_Layer,FIRE_NUM,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,FIRE_DEPT_DISSOLVE_Layer,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,FIRE_DEPT_DISSOLVE_Layer,COUNTY_FIPS,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,FIRE_DEPT_DISSOLVE_Layer,DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,FIRE_DEPT_DISSOLVE_Layer,STATE,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#', "")
    FireDept_Internal_result = arcpy.GetCount_management(FIRE_DEPT_COVERAGE_INTERNAL)
    print ('{} has {} records'.format(FIRE_DEPT_COVERAGE_INTERNAL, FireDept_Internal_result[0]))
    write_log('{} has {} records'.format(FIRE_DEPT_COVERAGE_INTERNAL, FireDept_Internal_result[0]), logfile)
except:
    print ("\n Unable to append Fire Department Coverage - CRAW_INTERNAL from FIRE_DEPT_DISSOLVE_Layer")
    write_log("Unable to append Fire Department Coverage - CRAW_INTERNAL from FIRE_DEPT_DISSOLVE_Layer", logfile)
    logging.exception('Got exception on append Fire Department Coverage - CRAW_INTERNAL from FIRE_DEPT_DISSOLVE_Layer logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for next process - BLS (keeps in_memory from getting overloaded or corrupted)
    arcpy.Delete_management("in_memory")
except:
    print ("\n Unable to clear FIRE_DEPT_COVERAGE_DISSOLVE from in_memory")
    write_log("Unable to clear FIRE_DEPT_COVERAGE_DISSOLVE from in_memory", logfile)
    logging.exception('Got exception on clear FIRE_DEPT_COVERAGE_DISSOLVE from in_memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Fire Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY completed")
write_log("       Updating Fire Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY completed", logfile)

print ("\n Updating BLS Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039")
write_log("\n Updating BLS Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039", logfile)

try:
    # Delete Rows from BLS DEPT COVERAGE - CRAW_INTERNAL
    arcpy.DeleteRows_management(BLS_COVERAGE_INTERNAL)
except:
    print ("\n Unable to delete rows from BLS Department Coverage - CRAW_INTERNAL")
    write_log("Unable to delete rows from BLS Department Coverage - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from BLS Department Coverage - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve BLS_Dept_Coverage from filtered layer of PUBLIC_SAFETY // ESZ_ALL (dissolve ESZ_ALL polygons based on BLS department fields to make BLS department polygons)
    BLS_COVERAGE_DISSOLVE = arcpy.Dissolve_management(ESZ_ALL_PS, "in_memory/BLS_COVERAGE_DISSOLVE", "EMS_DEPT;EMS_NUM;EMS_EMSID;COUNTY_NAME;COUNTY_FIPS;DiscrpAgID;STATE","", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to dissolve BLS Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY")
    write_log("Unable to dissolve BLS Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on dissolve BLS Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make feature layer from BLS_COVERAGE_DISSOLVE - in_memory, filtering only COUNTY_FIPS = 42039  (make temporary layer of dissolve filtering out 42039, to only include areas in Crawford County, from last step, to append in next step)
    BLS_COVERAGE_DISSOLVE_Layer = arcpy.MakeFeatureLayer_management(BLS_COVERAGE_DISSOLVE, "BLS_COVERAGE_DISSOLVE_Layer", "COUNTY_FIPS = 42039", "", "OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;EMS_DEPT EMS_DEPT VISIBLE NONE;EMS_NUM EMS_NUM VISIBLE NONE;EMS_EMSID EMS_EMSID VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;STATE STATE VISIBLE NONE;SHAPE_Length SHAPE_Length VISIBLE NONE;SHAPE_Area SHAPE_Area VISIBLE NONE")
except:
    print ("\n Unable to create feature layer from BLS_COVERAGE_DISSOLVE - in memory, filtering only COUNTY_FIPS = 42039")
    write_log("Unable to create feature layer from BLS_COVERAGE_DISSOLVE - in memory, filtering only COUNTY_FIPS = 42039", logfile)
    logging.exception('Got exception on create feature layer from BLS_COVERAGE_DISSOLVE - in memory, filtering only COUNTY_FIPS = 42039 logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Append BLS DEPT COVERAGE - CRAW_INTERNAL from PUBLIC_SAFETY // ESZ_ALL (append from temporary layer created from last step)
    arcpy.Append_management(BLS_COVERAGE_DISSOLVE_Layer, BLS_COVERAGE_INTERNAL, "NO_TEST", 'EMS_DEPT "BLS/EMS DEPARTMENT" true true false 50 Text 0 0 ,First,#,BLS_COVERAGE_DISSOLVE_Layer,EMS_DEPT,-1,-1;EMS_NUM "BLS/EMS DEPARTMENT #" true true false 10 Text 0 0 ,First,#,BLS_COVERAGE_DISSOLVE_Layer,EMS_NUM,-1,-1;EMS_EMSID "EMS ID CODE" true true false 10 Text 0 0 ,First,#,BLS_COVERAGE_DISSOLVE_Layer,EMS_EMSID,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,BLS_COVERAGE_DISSOLVE_Layer,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,BLS_COVERAGE_DISSOLVE_Layer,COUNTY_FIPS,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,BLS_COVERAGE_DISSOLVE_Layer,DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,BLS_COVERAGE_DISSOLVE_Layer,STATE,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#', "")
    BLSDept_Internal_result = arcpy.GetCount_management(BLS_COVERAGE_INTERNAL)
    print ('{} has {} records'.format(BLS_COVERAGE_INTERNAL, BLSDept_Internal_result[0]))
    write_log('{} has {} records'.format(BLS_COVERAGE_INTERNAL, BLSDept_Internal_result[0]), logfile)
except:
    print ("\n Unable to append BLS Department Coverage - CRAW_INTERNAL from BLS_COVERAGE_DISSOLVE Layer")
    write_log("Unable to append BLS Department Coverage - CRAW_INTERNAL from BLS_COVERAGE_DISSOLVE Layer", logfile)
    logging.exception('Got exception on append BLS Department Coverage - CRAW_INTERNAL from BLS_COVERAGE_DISSOLVE Layer logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for next process - QRS (keeps in_memory from getting overloaded or corrupted)
    arcpy.Delete_management("in_memory")
except:
    print ("\n Unable to clear BLS_COVERAGE_DISSOLVE from in_memory")
    write_log("Unable to clear BLS_COVERAGE_DISSOLVE from in_memory", logfile)
    logging.exception('Got exception on clear BLS_COVERAGE_DISSOLVE from in_memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("       Updating BLS Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY - processing only COUNTY_FIPS = 42039 completed")
write_log("       Updating BLS Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY - processing only COUNTY_FIPS = 42039 completed", logfile)

print ("\n Updating QRS Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039")
write_log("\n Updating QRS Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039", logfile)

try:
    # Delete Rows from QRS DEPT COVERAGE - CRAW_INTERNAL
    arcpy.DeleteRows_management(QRS_DEPT_COVERAGE_INTERNAL)
except:
    print ("\n Unable to delete rows from QRS DEPT COVERAGE - CRAW_INTERNAL")
    write_log("Unable to delete rows from QRS DEPT COVERAGE - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from QRS DEPT COVERAGE - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve_QRS_DEPT_COVERAGE from filtered layer of PUBLIC_SAFETY // ESZ_ALL (dissolve ESZ_ALL polygons based on QRS department fields to make QRS department polygons)
    QRS_DEPT_COVERAGE_DISSOLVE = arcpy.Dissolve_management(ESZ_ALL_PS, "in_memory/QRS_DEPT_COVERAGE_DISSOLVE", "QRS_FDID;COUNTY_NAME;COUNTY_FIPS;QRS_DEPT;QRS_NUM;DiscrpAgID;STATE", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to dissolve QRS Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY")
    write_log("Unable to dissolve QRS Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on dissolve QRS Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make Feature Layer from QRS_DEPT_COVERAGE_DISSOLVE - in_memory (make temporary layer of dissolve from last step, to append in next step)
    QRS_DEPT_DISSOLVE_Layer = arcpy.MakeFeatureLayer_management(QRS_DEPT_COVERAGE_DISSOLVE, "QRS_DEPT_DISSOLVE_Layer", "COUNTY_FIPS = 42039", "", "OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;QRS_FDID QRS_FDID VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;QRS_DEPT QRS_DEPT VISIBLE NONE;QRS_NUM QRS_NUM VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;STATE STATE VISIBLE NONE;SHAPE_Length SHAPE_Length VISIBLE NONE;SHAPE_Area SHAPE_Area VISIBLE NONE")
except:
    print ("\n Unable to make feature layer from QRS_DEPT_COVERAGE_DISSOLVE - in_memory")
    write_log("Unable to make feature layer from QRS_DEPT_COVERAGE_DISSOLVE - in_memory", logfile)
    logging.exception('Got exception on make feature layer from QRS_DEPT_COVERAGE_DISSOLVE - in_memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
try:
    # Append QRS DEPT COVERAGE - CRAW_INTERNAL from PUBLIC_SAFETY // ESZ_ALL (append from temporary layer created from last step)
    arcpy.Append_management(QRS_DEPT_DISSOLVE_Layer, QRS_DEPT_COVERAGE_INTERNAL, "NO_TEST", 'QRS_FDID "QUICK RESPONSE SERVICE DEPARTMENT FDID CODE" true true false 15 Text 0 0 ,First,#,QRS_DEPT_DISSOLVE_Layer,QRS_FDID,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,QRS_DEPT_DISSOLVE_Layer,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,QRS_DEPT_DISSOLVE_Layer,COUNTY_FIPS,-1,-1;QRS_DEPT "QUICK RESPONSE SERVICE DEPARTMENT NAME" true true false 50 Text 0 0 ,First,#,QRS_DEPT_DISSOLVE_Layer,QRS_DEPT,-1,-1;QRS_NUM "QUICK RESPONSE SERVICE DEPARTMENT #" true true false 10 Text 0 0 ,First,#,QRS_DEPT_DISSOLVE_Layer,QRS_NUM,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,QRS_DEPT_DISSOLVE_Layer,DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,QRS_DEPT_DISSOLVE_Layer,STATE,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#', "")
    QRSDept_Internal_result = arcpy.GetCount_management(QRS_DEPT_COVERAGE_INTERNAL)
    print ('{} has {} records'.format(QRS_DEPT_COVERAGE_INTERNAL, QRSDept_Internal_result[0]))
    write_log('{} has {} records'.format(QRS_DEPT_COVERAGE_INTERNAL, QRSDept_Internal_result[0]), logfile)
except:
    print ("\n Unable to append QRS Department Coverage - CRAW_INTERNAL from QRS_DEPT_COVERAGE_DISSOLVE")
    write_log("Unable to append QRS Department Coverage - CRAW_INTERNAL from QRS_DEPT_COVERAGE_DISSOLVE", logfile)
    logging.exception('Got exception on append QRS Department Coverage - CRAW_INTERNAL from QRS_DEPT_COVERAGE_DISSOLVE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for next process - Police (keeps in_memory from getting overloaded or corrupted)
    arcpy.Delete_management("in_memory")
except:
    print ("\n Unable to clear QRS_DEPT_COVERAGE_DISSOLVE from in_memory")
    write_log("Unable to clear QRS_DEPT_COVERAGE_DISSOLVE from in_memory", logfile)
    logging.exception('Got exception on clear QRS_DEPT_COVERAGE_DISSOLVE from in_memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("       Updating QRS Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039 completed")
write_log("       Updating QRS Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039 completed", logfile)

print ("\n Updating Police Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039 completed")
write_log("\n Updating Police Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039 completed", logfile)

try:
    # Delete Rows from POLICE DEPT COVERAGE - CRAW_INTERNAL
    arcpy.DeleteRows_management(POLICE_DEPT_COVERAGE_INTERNAL)
except:
    print ("\n Unable to delete rows from Police Department Coverage - CRAW_INTERNAL")
    write_log("Unable to delete rows from Police Department Coverage - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Police Department Coverage - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve_POLICE_DEPT_COVERAGE from filtered layer of PUBLIC_SAFETY // ESZ_ALL (dissolve ESZ_ALL polygons based on police department fields to make police department polygons)
    POLICE_DEPT_COVERAGE_DISSOLVE = arcpy.Dissolve_management(ESZ_ALL_PS, "in_memory/POLICE_DEPT_COVERAGE_DISSOLVE", "POLICE_DEPT;POLICE_DISTRICT;POLICE_ORI;COUNTY_NAME;COUNTY_FIPS;POLICE_ID;DiscrpAgID;STATE", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to dissolve Police Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY")
    write_log("Unable to dissolve Police Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on dissolve Police Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make Feature Layer from POLICE_DEPT_COVERAGE_DISSOLVE - in_memory (make temporary layer of dissolve from last step, to append in next step)
    POLICE_DEPT_DISSOLVE_Layer = arcpy.MakeFeatureLayer_management(POLICE_DEPT_COVERAGE_DISSOLVE, "POLICE_DEPT_DISSOLVE_Layer", "COUNTY_FIPS = 42039", "", "OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;POLICE_DEPT POLICE_DEPT VISIBLE NONE;POLICE_DISTRICT POLICE_DISTRICT VISIBLE NONE;POLICE_ORI POLICE_ORI VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;POLICE_ID POLICE_ID VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;STATE STATE VISIBLE NONE;SHAPE_Length SHAPE_Length VISIBLE NONE;SHAPE_Area SHAPE_Area VISIBLE NONE")
except:
    print ("\n Unable to make Feature Layer from POLICE_DEPT_COVERAGE_DISSOLVE - in_memory")
    write_log("Unable to make Feature Layer from POLICE_DEPT_COVERAGE_DISSOLVE - in_memory", logfile)
    logging.exception('Got exception on make Feature Layer from POLICE_DEPT_COVERAGE_DISSOLVE - in_memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append POLICE DEPT COVERAGE - CRAW_INTERNAL from PUBLIC_SAFETY // ESZ_ALL (append from temporary layer created from last step)
    arcpy.Append_management(POLICE_DEPT_DISSOLVE_Layer, POLICE_DEPT_COVERAGE_INTERNAL, "NO_TEST", 'POLICE_DEPT "POLICE DEPARTMENT" true true false 50 Text 0 0 ,First,#,POLICE_DEPT_DISSOLVE_Layer,POLICE_DEPT,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,POLICE_DEPT_DISSOLVE_Layer,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,POLICE_DEPT_DISSOLVE_Layer,COUNTY_FIPS,-1,-1;POLICE_ID "POLICE_ID" true true false 4 Long 0 10 ,First,#,POLICE_DEPT_DISSOLVE_Layer,POLICE_ID,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,POLICE_DEPT_DISSOLVE_Layer,DiscrpAgID,-1,-1;STATE "State" true true false 2 Text 0 0 ,First,#,POLICE_DEPT_DISSOLVE_Layer,STATE,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#', "")
    PoliceDept_Internal_result = arcpy.GetCount_management(POLICE_DEPT_COVERAGE_INTERNAL)
    print ('{} has {} records'.format(POLICE_DEPT_COVERAGE_INTERNAL, PoliceDept_Internal_result[0]))
    write_log('{} has {} records'.format(POLICE_DEPT_COVERAGE_INTERNAL, PoliceDept_Internal_result[0]), logfile)
except:
    print ("\n Unable to append Police Department Coverage - CRAW_INTERNAL from POLICE_DEPT_COVERAGE_DISSOLVE")
    write_log("Unable to append Police Department Coverage - CRAW_INTERNAL from POLICE_DEPT_COVERAGE_DISSOLVE", logfile)
    logging.exception('Got exception on append Police Department Coverage - CRAW_INTERNAL from POLICE_DEPT_COVERAGE_DISSOLVE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" for next process - Police (keeps in_memory from getting overloaded or corrupted)
    arcpy.Delete_management("in_memory")
except:
    print ("\n Unable to clear POLICE_DEPT_COVERAGE_DISSOLVE from in_memory")
    write_log("Unable to clear POLICE_DEPT_COVERAGE_DISSOLVE from in_memory", logfile)
    logging.exception('Got exception on clear POLICE_DEPT_COVERAGE_DISSOLVE from in_memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("       Updating Police Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039 completed")
write_log("       Updating Police Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039 completed", logfile)

print ("\n Updating Rescue Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039")
write_log("\n Updating Rescue Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039", logfile)

try:
    # Delete Rows from RESCUE DEPT COVERAGE - CRAW_INTERNAL
    arcpy.DeleteRows_management(RESCUE_DEPT_COVERAGE_INTERNAL)
except:
    print ("\n Unable to delete rows from Rescue Department Coverage - CRAW_INTERNAL")
    write_log("Unable to delete rows from Rescue Department Coverage - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Rescue Department Coverage - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Dissolve_RESCUE_DEPT_COVERAGE from filtered layer of PUBLIC_SAFETY // ESZ_ALL (dissolve ESZ_ALL polygons based on rescue department fields to make rescue department polygons)
    RESCUE_DEPT_COVERAGE_DISSOLVE = arcpy.Dissolve_management(ESZ_ALL_PS, "in_memory/RESCUE_DEPT_COVERAGE_DISSOLVE", "RESCUE_DEPT;RESCUE_NUM;COUNTY_NAME;COUNTY_FIPS;RESCUE_FDID;DiscrpAgID;STATE", "", "MULTI_PART", "DISSOLVE_LINES")
except:
    print ("\n Unable to dissolve Rescue Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY")
    write_log("Unable to dissolve Rescue Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY", logfile)
    logging.exception('Got exception on dissolve Rescue Department Coverage - CRAW_INTERNAL from ESZ_ALL - PUBLIC_SAFETY logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make Feature Layer from RESCUE_DEPT_COVERAGE_DISSOLVE - in_memory (make temporary layer of dissolve from last step, to append in next step)
    RESCUE_DEPT_DISSOLVE_Layer = arcpy.MakeFeatureLayer_management(RESCUE_DEPT_COVERAGE_DISSOLVE, "RESCUE_DEPT_DISSOLVE_Layer", "COUNTY_FIPS = 42039", "", "OBJECTID OBJECTID VISIBLE NONE;SHAPE SHAPE VISIBLE NONE;RESCUE_DEPT RESCUE_DEPT VISIBLE NONE;RESCUE_NUM RESCUE_NUM VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;COUNTY_FIPS COUNTY_FIPS VISIBLE NONE;RESCUE_FDID RESCUE_FDID VISIBLE NONE;DiscrpAgID DiscrpAgID VISIBLE NONE;STATE STATE VISIBLE NONE;SHAPE_Length SHAPE_Length VISIBLE NONE;SHAPE_Area SHAPE_Area VISIBLE NONE")
except:
    print ("\n Unable to make Feature Layer from RESCUE_DEPT_COVERAGE_DISSOLVE - in_memory, filtered for COUNTY_FIPS = 42039")
    write_log("Unable to make Feature Layer from RESCUE_DEPT_COVERAGE_DISSOLVE - in_memory, filtered for COUNTY_FIPS = 42039", logfile)
    logging.exception('Got exception on make Feature Layer from RESCUE_DEPT_COVERAGE_DISSOLVE - in_memory, filtered for COUNTY_FIPS = 42039 logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Process: Append RESCUE DEPT COVERAGE - CRAW_INTERNAL from PUBLIC_SAFETY // ESZ_ALL (append from temporary layer created from last step)
    arcpy.Append_management(RESCUE_DEPT_DISSOLVE_Layer, RESCUE_DEPT_COVERAGE_INTERNAL, "NO_TEST", 'RESCUE_DEPT "RESCUE DEPARTMENT" true true false 50 Text 0 0 ,First,#,RESCUE_DEPT_DISSOLVE_Layer,RESCUE_DEPT,-1,-1;RESCUE_NUM "RESCUE DEPARTMENT #" true true false 10 Text 0 0 ,First,#,RESCUE_DEPT_DISSOLVE_Layer,RESCUE_NUM,-1,-1;COUNTY_NAME "COUNTY NAME" true true false 50 Text 0 0 ,First,#,RESCUE_DEPT_DISSOLVE_Layer,COUNTY_NAME,-1,-1;COUNTY_FIPS "COUNTY FIPS CODE" true true false 8 Double 8 38 ,First,#,RESCUE_DEPT_DISSOLVE_Layer,COUNTY_FIPS,-1,-1;RESCUE_FDID "RESCUE_FDID" true true false 50 Text 0 0 ,First,#,RESCUE_DEPT_DISSOLVE_Layer,RESCUE_FDID,-1,-1;GLOBALID "GLOBALID" false false false 38 GlobalID 0 0 ,First,#;DiscrpAgID "Discrepancy Agency ID" true true false 75 Text 0 0 ,First,#,RESCUE_DEPT_DISSOLVE_Layer,DiscrpAgID,-1,-1;STATE "STATE" true true false 2 Text 0 0 ,First,#,RESCUE_DEPT_DISSOLVE_Layer,STATE,-1,-1;SHAPE.STArea() "SHAPE.STArea()" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() "SHAPE.STLength()" false false true 0 Double 0 0 ,First,#', "")
    RescueDept_Internal_result = arcpy.GetCount_management(RESCUE_DEPT_COVERAGE_INTERNAL)
    print ('{} has {} records'.format(RESCUE_DEPT_COVERAGE_INTERNAL, RescueDept_Internal_result[0]))
    write_log('{} has {} records'.format(RESCUE_DEPT_COVERAGE_INTERNAL, RescueDept_Internal_result[0]), logfile)
except:
    print ("\n Unable to append Rescue Department Coverage - CRAW_INTERNAL from RESCUE_DEPT_COVERAGE_DISSOLVE")
    write_log("Unable to append Rescue Department Coverage - CRAW_INTERNAL from RESCUE_DEPT_COVERAGE_DISSOLVE", logfile)
    logging.exception('Got exception on append Rescue Department Coverage - CRAW_INTERNAL from RESCUE_DEPT_COVERAGE_DISSOLVE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Clear "in_memory" from final process (keeps in_memory from getting overloaded or corrupted)
    arcpy.Delete_management("in_memory")
except:
    print ("\n Unable to clear RESCUE_DEPT_COVERAGE_DISSOLVE from in_memory")
    write_log("Unable to clear RESCUE_DEPT_COVERAGE_DISSOLVE from in_memory", logfile)
    logging.exception('Got exception on clear RESCUE_DEPT_COVERAGE_DISSOLVE from in_memory logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()
    
print ("       Updating Rescue Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039 completed")
write_log("       Updating Rescue Department Coverage - CRAW_INTERNAL from PUBLIC_SAFETY (ESZ_ALL) - processing only COUNTY_FIPS = 42039 completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL PUBLIC SAFETY UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL PUBLIC SAFETY UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
