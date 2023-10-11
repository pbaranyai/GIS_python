# ---------------------------------------------------------------------------
# Elections_Data_Spreader.py
# Created on: 2019-03-05 
# Updated on 2021-09-21
# Works in ArcPro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# Crawford Municipal Election Districts  
# Crawford PA House Districts
# Crawford PA Senate Districts
# Crawford Polling Place Locations
# Crawford US Congress Districts
# Crawford US Senate Districts
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
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
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\GIS\\Elections_Data_Spreader.log"  
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

#Database variables:
CRAW_INTERNAL = Database_Connections+ "\\craw_internal@ccsde.sde"
GIS = Database_Connections + "\\GIS@ccsde.sde"
OPEN_DATA = Database_Connections + "\\public_od@ccsde.sde"
PUBLIC_WEB = Database_Connections + "\\public_web@ccsde.sde"

# Local variables:
MUNI_ELECTION_DIST_GIS = GIS + "\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS"
MUNI_ELECTION_DIST_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL"
MUNI_ELECTION_DIST_WEB_RELATE = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Elections\\CCSDE.PUBLIC_WEB.MUNI_ELECTION_DIST_RELATE"
PA_HOUSE_DISTRICTS_GIS = GIS + "\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_HOUSE_DISTRICTS"
PA_HOUSE_DISTRICTS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.PA_HOUSE_DISTRICTS_INTERNAL"
PA_SENATE_DISTRICTS_GIS = GIS + "\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_SENATE_DISTRICTS"
PA_SENATE_DISTRICTS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.PA_SENATE_DISTRICTS_INTERNAL"
POLLING_PLACES_GIS = GIS + "\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES"
POLLING_PLACES_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL"
POLLING_PLACES_WEB_RELATE = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Elections\\CCSDE.PUBLIC_WEB.POLLING_PLACES_RELATE"
US_CONGRESS_DISTRICTS_GIS = GIS + "\\CCSDE.GIS.Elections\\CCSDE.GIS.US_CONGRESS_DISTRICTS"
US_CONGRESS_DISTRICTS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.US_CONGRESS_DISTRICTS_INTERNAL"
US_SENATE_DISTRICTS_GIS = GIS + "\\CCSDE.GIS.Elections\\CCSDE.GIS.US_SENATE_DISTRICTS"
US_SENATE_DISTRICTS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.US_SENATE_DISTRICTS_INTERNAL"

start_time = time.time()

print ("============================================================================")
print (("Updating Election Datasets (no results): "+ str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\nMunicipal Election Districts Feature Class")
print ("PA House Districts Feature Class")
print ("PA Senate Districts Feature Class")
print ("Polling Places Feature Class")
print ("US Congressional Districts Feature Class")
print ("US Senate Districts Feature Class")
print ("\n From source to CRAW_INTERNAL (where applicable)")
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Election Datasets (no results): "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nMunicipal Election Districts Feature Class", logfile)  
write_log("PA House Districts Feature Class", logfile) 
write_log("PA Senate Districts Feature Class", logfile)
write_log("Polling Places Feature Class", logfile)
write_log("US Congressional Districts Feature Class", logfile) 
write_log("US Senate Districts Feature Class", logfile)
write_log("\n From source to CRAW_INTERNAL (where applicable)", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Muni Election Districts - CRAW_INTERNAL from GIS")
write_log("\n Updating Muni Election Districts - CRAW_INTERNAL from GIS: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete Rows from Muni Election Districts - CRAW_INTERNAL
    arcpy.DeleteRows_management(MUNI_ELECTION_DIST_INTERNAL)
except:
    print ("\n Unable to delete rows from Muni Election Districts - CRAW_INTERNAL")
    write_log("Unable to delete rows from Muni Election Districts - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Muni Election Districts - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:    
    # Append Muni Election Districts - CRAW_INTERNAL from GIS
    arcpy.Append_management(MUNI_ELECTION_DIST_GIS, MUNI_ELECTION_DIST_INTERNAL, "NO_TEST", "PRECINCT_NAME \"PRECINCT NAME\" true true false 150 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,PRECINCT_NAME,-1,-1;CITY_WARD \"CITY WARD\" true true false 2 Short 0 5 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,CITY_WARD,-1,-1;PRECINCT_DISTRICT \"PRECINCT DISTRICT\" true true false 2 Short 0 5 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,PRECINCT_DISTRICT,-1,-1;CITY_WARD_DISTRICT \"CITY WARD - DISTRICT\" true true false 10 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,CITY_WARD_DISTRICT,-1,-1;HSENUMBER \"ADDRESS #\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,HSENUMBER,-1,-1;FULL_STREET \"FULL STREET\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,FULL_STREET,-1,-1;POST_OFFICE \"POST OFFICE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,POST_OFFICE,-1,-1;ZIPCODE \"ZIPCODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,ZIPCODE,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,COUNTY_FIPS,-1,-1;LOCATION_DESCRIPTION \"LOCATION DESCRIPTION\" true true false 150 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,LOCATION_DESCRIPTION,-1,-1;UPDATED_DATE \"UPDATED DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,UPDATED_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.MUNICIPAL_ELECTION_DISTRICTS,SHAPE.STLength(),-1,-1", "")
    MuniDist_Internal_result = arcpy.GetCount_management(MUNI_ELECTION_DIST_INTERNAL)
    print (('{} has {} records'.format(MUNI_ELECTION_DIST_INTERNAL, MuniDist_Internal_result[0])))
except:
    print ("\n Unable to append Muni Election Districts - CRAW_INTERNAL from GIS")
    write_log("Unable to append Muni Election Districts - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Muni Election Districts - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Muni Election Districts - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Muni Election Districts - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Muni Election Dist Relate - WEB_RELATE from PUBLIC_WEB")
write_log("\n Updating Muni Election Dist Relate - WEB_RELATE from PUBLIC_WEB", logfile)

try:
    # Delete Rows from Muni Election Dist relate - PUBLIC_WEB
    arcpy.DeleteRows_management(MUNI_ELECTION_DIST_WEB_RELATE)
except:
    print ("\n Unable to delete rows from Muni Dist relate - PUBLIC_WEB")
    write_log("Unable to delete rows from Muni Dist relate - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Muni Election Dist relate - PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try: 
    # Append Muni Election Dist Relate - WEB_RELATE from PUBLIC_WEB
    arcpy.Append_management(MUNI_ELECTION_DIST_INTERNAL, MUNI_ELECTION_DIST_WEB_RELATE, "NO_TEST", "PRECINCT_NAME \"PRECINCT NAME\" true true false 150 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,PRECINCT_NAME,-1,-1;CITY_WARD \"CITY WARD\" true true false 2 Short 0 5 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,CITY_WARD,-1,-1;PRECINCT_DISTRICT \"PRECINCT DISTRICT\" true true false 2 Short 0 5 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,PRECINCT_DISTRICT,-1,-1;CITY_WARD_DISTRICT \"CITY WARD - DISTRICT\" true true false 10 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,CITY_WARD_DISTRICT,-1,-1;HSENUMBER \"ADDRESS #\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,HSENUMBER,-1,-1;FULL_STREET \"FULL STREET\" true true false 75 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,FULL_STREET,-1,-1;POST_OFFICE \"POST OFFICE\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,POST_OFFICE,-1,-1;ZIPCODE \"ZIPCODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,ZIPCODE,-1,-1;MUNI_NAME \"MUNICIPALITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,COUNTY_FIPS,-1,-1;LOCATION_DESCRIPTION \"LOCATION DESCRIPTION\" true true false 150 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,LOCATION_DESCRIPTION,-1,-1;UPDATED_DATE \"UPDATED DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,UPDATED_DATE,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.MUNI_ELECTION_DIST_INTERNAL,SHAPE.STLength(),-1,-1", "")
    MuniDistRelate_Web_result = arcpy.GetCount_management(MUNI_ELECTION_DIST_WEB_RELATE)
    print (('{} has {} records'.format(MUNI_ELECTION_DIST_WEB_RELATE, MuniDistRelate_Web_result[0])))
except:
    print ("\n Unable to append Muni Election Dist Relate - WEB_RELATE from PUBLIC_WEB")
    write_log("Unable to append Muni Election Dist Relate - WEB_RELATE from PUBLIC_WEB", logfile)
    logging.exception('Got exception on append Muni Election Dist Relate - WEB_RELATE from PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Muni Election Dist Relate - WEB_RELATE from PUBLIC_WEB completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Muni Election Dist Relate - WEB_RELATE from PUBLIC_WEB completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating PA House Districts - CRAW_INTERNAL from GIS")
write_log("\n Updating PA House Districts - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from PA House Districts - CRAW_INTERNAL
    arcpy.DeleteRows_management(PA_HOUSE_DISTRICTS_INTERNAL)
except:
    print ("\n Unable to delete rows from PA House Districts - CRAW_INTERNAL")
    write_log("Unable to delete rows from PA House Districts - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from PA House Districts - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try: 
    # Append PA House Districts - CRAW_INTERNAL from GIS
    arcpy.Append_management(PA_HOUSE_DISTRICTS_GIS, PA_HOUSE_DISTRICTS_INTERNAL, "NO_TEST", "DISTRICT \"DISTRICT\" true true false 2 Short 0 5 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_HOUSE_DISTRICTS,DISTRICT,-1,-1;REP_NAME \"REPRESENTATIVE NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_HOUSE_DISTRICTS,REP_NAME,-1,-1;WEBSITE \"WEBSITE\" true true false 200 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_HOUSE_DISTRICTS,WEBSITE,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_HOUSE_DISTRICTS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_HOUSE_DISTRICTS,COUNTY_FIPS,-1,-1;UPDATED_DATE \"UPDATED_DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_HOUSE_DISTRICTS,UPDATED_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_HOUSE_DISTRICTS,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_HOUSE_DISTRICTS,SHAPE.STLength(),-1,-1", "")
    PAHouse_Internal_result = arcpy.GetCount_management(PA_HOUSE_DISTRICTS_INTERNAL)
    print (('{} has {} records'.format(PA_HOUSE_DISTRICTS_INTERNAL, PAHouse_Internal_result[0])))
except:
    print ("\n Unable to append PA House Districts - CRAW_INTERNAL from GIS")
    write_log("Unable to append PA House Districts - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append PA House Districts - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating PA House Districts - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating PA House Districts - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating PA Senate Districts - CRAW_INTERNAL from GIS")
write_log("\n Updating PA Senate Districts - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from PA Senate Districts - CRAW_INTERNAL
    arcpy.DeleteRows_management(PA_SENATE_DISTRICTS_INTERNAL)
except:
    print ("\n Unable to delete rows from PA House Districts - CRAW_INTERNAL")
    write_log("Unable to delete rows from PA House Districts - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from PA House Districts - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try: 
    # Append PA Senate Districts - CRAW_INTERNAL from GIS
    arcpy.Append_management(PA_SENATE_DISTRICTS_GIS, PA_SENATE_DISTRICTS_INTERNAL, "NO_TEST", "DISTRICT \"DISTRICT\" true true false 2 Short 0 5 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_SENATE_DISTRICTS,DISTRICT,-1,-1;REP_NAME \"REPRESENTATIVE NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_SENATE_DISTRICTS,REP_NAME,-1,-1;WEBSITE \"WEBSITE\" true true false 200 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_SENATE_DISTRICTS,WEBSITE,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_SENATE_DISTRICTS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_SENATE_DISTRICTS,COUNTY_FIPS,-1,-1;UPDATED_DATE \"UPDATED DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_SENATE_DISTRICTS,UPDATED_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_SENATE_DISTRICTS,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.PA_SENATE_DISTRICTS,SHAPE.STLength(),-1,-1", "")
    PASenate_Internal_result = arcpy.GetCount_management(PA_SENATE_DISTRICTS_INTERNAL)
    print (('{} has {} records'.format(PA_SENATE_DISTRICTS_INTERNAL, PASenate_Internal_result[0])))
except:
    print ("\n Unable to append PA Senate Districts - CRAW_INTERNAL from GIS")
    write_log("Unable to append PA Senate Districts - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append PA Senate Districts - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating PA Senate Districts - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating PA Senate Districts - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Polling Places - CRAW_INTERNAL from GIS")
write_log("\n Updating Polling Places - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from Polling Places - CRAW_INTERNAL
    arcpy.DeleteRows_management(POLLING_PLACES_INTERNAL)
except:
    print ("\n Unable to delete rows from Polling Places - CRAW_INTERNAL")
    write_log("Unable to delete rows from Polling Places - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Polling Places - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try: 
    # Append Polling Places - CRAW_INTERNAL from GIS
    arcpy.Append_management(POLLING_PLACES_GIS, POLLING_PLACES_INTERNAL, "NO_TEST", "PRECINCT_NAME \"PRECINCT NAME\" true true false 150 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,PRECINCT_NAME,-1,-1;FULL_STREET \"FULL STREET\" true true false 75 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,FULL_STREET,-1,-1;POST_OFFICE \"POST OFFICE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,POST_OFFICE,-1,-1;ZIPCODE \"ZIPCODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,ZIPCODE,-1,-1;STATE \"STATE\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,STATE,-1,-1;MUNI_NAME \"MUNICIPLAITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,COUNTY_FIPS,-1,-1;LOCATION_DESCRIPTION \"LOCATION DESCRIPTION\" true true false 150 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,LOCATION_DESCRIPTION,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,UPDATE_DATE,-1,-1;HSENUMBER \"ADDRESS #\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.POLLING_PLACES,HSENUMBER,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#", "")
    PollingPlace_Internal_result = arcpy.GetCount_management(POLLING_PLACES_INTERNAL)
    print (('{} has {} records'.format(POLLING_PLACES_INTERNAL, PollingPlace_Internal_result[0])))
except:
    print ("\n Unable to append Polling Places - CRAW_INTERNAL from GIS")
    write_log("Unable to append Polling Places - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append Polling Places - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Polling Places - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Polling Places - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating Polling Places Relate - WEB_RELATE from PUBLIC_WEB")
write_log("\n Updating Polling Places Relate - WEB_RELATE from PUBLIC_WEB", logfile)

try:
    # Delete Rows from Polling Places Relate - PUBLIC_WEB
    arcpy.DeleteRows_management(POLLING_PLACES_WEB_RELATE)
except:
    print ("\n Unable to delete rows from Polling Places Relate - PUBLIC_WEB")
    write_log("Unable to delete rows from Polling Places Relate - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Polling Places Relate - PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try: 
    # Append - Polling Places Relate - WEB_RELATE from PUBLIC_WEB
    arcpy.Append_management(POLLING_PLACES_INTERNAL, POLLING_PLACES_WEB_RELATE, "NO_TEST", "PRECINCT_NAME \"PRECINCT NAME\" true true false 150 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,PRECINCT_NAME,-1,-1;FULL_STREET \"FULL STREET\" true true false 75 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,FULL_STREET,-1,-1;POST_OFFICE \"POST OFFICE\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,POST_OFFICE,-1,-1;ZIPCODE \"ZIPCODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,ZIPCODE,-1,-1;STATE \"STATE\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,STATE,-1,-1;MUNI_NAME \"MUNICIPLAITY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,MUNI_NAME,-1,-1;MUNI_FIPS \"MUNICIPALITY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,MUNI_FIPS,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,COUNTY_FIPS,-1,-1;LOCATION_DESCRIPTION \"LOCATION DESCRIPTION\" true true false 150 Text 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,LOCATION_DESCRIPTION,-1,-1;UPDATE_DATE \"UPDATE DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,UPDATE_DATE,-1,-1;HSENUMBER \"ADDRESS #\" true true false 8 Double 8 38 ,First,#,Database Connections\\craw_internal@ccsde.sde\\CCSDE.CRAW_INTERNAL.Elections\\CCSDE.CRAW_INTERNAL.POLLING_PLACES_INTERNAL,HSENUMBER,-1,-1", "")
    PollingPlaceRelate_Internal_result = arcpy.GetCount_management(POLLING_PLACES_WEB_RELATE)
    print (('{} has {} records'.format(POLLING_PLACES_WEB_RELATE, PollingPlaceRelate_Internal_result[0])))
except:
    print ("\n Unable to append Polling Places Relate - WEB_RELATE from PUBLIC_WEB")
    write_log("Unable to append Polling Places Relate - WEB_RELATE from PUBLIC_WEB", logfile)
    logging.exception('Got exception on append Polling Places Relate - WEB_RELATE from PUBLIC_WEB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating Polling Places Relate - WEB_RELATE from PUBLIC_WEB completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating Polling Places Relate - WEB_RELATE from PUBLIC_WEB completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating US Congress Districts - CRAW_INTERNAL from GIS")
write_log("\n Updating US Congress Districts - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from US Congress Districts - CRAW_INTERNAL
    arcpy.DeleteRows_management(US_CONGRESS_DISTRICTS_INTERNAL)
except:
    print ("\n Unable to delete rows from US Congress Districts - CRAW_INTERNAL")
    write_log("Unable to delete rows from US Congress Districts - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from US Congress Districts - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try: 
    # Append US Congress Districts - CRAW_INTERNAL from GIS
    arcpy.Append_management(US_CONGRESS_DISTRICTS_GIS, US_CONGRESS_DISTRICTS_INTERNAL, "NO_TEST", "DISTRICT \"DISTRICT\" true true false 2 Short 0 5 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_CONGRESS_DISTRICTS,DISTRICT,-1,-1;REP_NAME \"REPRESENTATIVE NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_CONGRESS_DISTRICTS,REP_NAME,-1,-1;WEBSITE \"WEBSITE\" true true false 200 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_CONGRESS_DISTRICTS,WEBSITE,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_CONGRESS_DISTRICTS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_CONGRESS_DISTRICTS,COUNTY_FIPS,-1,-1;UPDATED_DATE \"UPDATED DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_CONGRESS_DISTRICTS,UPDATED_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_CONGRESS_DISTRICTS,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_CONGRESS_DISTRICTS,SHAPE.STLength(),-1,-1", "")
    USCongress_Internal_result = arcpy.GetCount_management(US_CONGRESS_DISTRICTS_INTERNAL)
    print (('{} has {} records'.format(US_CONGRESS_DISTRICTS_INTERNAL, USCongress_Internal_result[0])))
except:
    print ("\n Unable to append US Congress Districts - CRAW_INTERNAL from GIS")
    write_log("Unable to append US Congress Districts - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append US Congress Districts - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating US Congress Districts - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating US Congress Districts - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

print ("\n Updating US Senate Districts - CRAW_INTERNAL from GIS")
write_log("\n Updating US Senate Districts - CRAW_INTERNAL from GIS", logfile)

try:
    # Delete Rows from US Senate Districts - CRAW_INTERNAL
    arcpy.DeleteRows_management(US_SENATE_DISTRICTS_INTERNAL)
except:
    print ("\n Unable to delete rows from US Senate Districts - CRAW_INTERNAL")
    write_log("Unable to delete rows from US Senate Districts - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from US Senate Districts - CRAW_INTERNAL logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try: 
    # Append US Senate Districts - CRAW_INTERNAL from GIS
    arcpy.Append_management(US_SENATE_DISTRICTS_GIS, US_SENATE_DISTRICTS_INTERNAL, "NO_TEST", "REP_NAME \"REPRESENTATIVE NAME\" true true false 100 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_SENATE_DISTRICTS,REP_NAME,-1,-1;WEBSITE \"WEBSITE\" true true false 200 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_SENATE_DISTRICTS,WEBSITE,-1,-1;DISTRICT \"DISTRICT\" true true false 254 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_SENATE_DISTRICTS,DISTRICT,-1,-1;COUNTY_NAME \"COUNTY NAME\" true true false 50 Text 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_SENATE_DISTRICTS,COUNTY_NAME,-1,-1;COUNTY_FIPS \"COUNTY FIPS CODE\" true true false 8 Double 8 38 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_SENATE_DISTRICTS,COUNTY_FIPS,-1,-1;UPDATED_DATE \"UPDATED DATE\" true true false 8 Date 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_SENATE_DISTRICTS,UPDATED_DATE,-1,-1;GLOBALID \"GLOBALID\" false false false 38 GlobalID 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_SENATE_DISTRICTS,SHAPE.STArea(),-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#,Database Connections\\GIS@ccsde.sde\\CCSDE.GIS.Elections\\CCSDE.GIS.US_SENATE_DISTRICTS,SHAPE.STLength(),-1,-1", "")
    USSenate_Internal_result = arcpy.GetCount_management(US_SENATE_DISTRICTS_INTERNAL)
    print (('{} has {} records'.format(US_SENATE_DISTRICTS_INTERNAL, USSenate_Internal_result[0])))
except:
    print ("\n Unable to append US Senate Districts - CRAW_INTERNAL from GIS")
    write_log("Unable to append US Senate Districts - CRAW_INTERNAL from GIS", logfile)
    logging.exception('Got exception on append US Senate Districts - CRAW_INTERNAL from GIS logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

print ("       Updating US Senate Districts - CRAW_INTERNAL from GIS completed at " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log("       Updating US Senate Districts - CRAW_INTERNAL from GIS completed at "+time.strftime("%I:%M:%S %p", time.localtime()), logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n ALL ELECTION COVERAGE DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("\n ALL ELECTION COVERAGE DATASETS UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)

write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
