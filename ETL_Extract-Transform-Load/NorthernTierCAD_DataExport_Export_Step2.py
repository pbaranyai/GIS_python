# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# NortherTierCAD_DataExport_Export to Nothern Tier Server - Step 2.py
#  
# Description: 
# This tool will access the FGDB (Northern_Tier_County_Data_YYYYMMDD) from the last step, and export it to the Northern Tier Server (into the Crawford FDS).
# Then rename it with the current date stamp.
# Finally it will, compress (ZIP) the FGDB for archive storage and then open the folder for the user to delete older archives.
#
# Before this tool is started, you must connect to the Elk Co. VPN to run the next step
#
# STEP 2 of 2
# Author: Phil Baranyai/Crawford County GIS Manager
# Created on: 2019-04-02 
# Updated on 2021-09-21
# Works in ArcGIS Pro
# ---------------------------------------------------------------------------

import sys
import arcpy
import datetime
import os
import traceback
import logging
import shutil
import time
import zipfile

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- doesn't overwrite with every run, allows for step 2 to be appended to step 1 for a complete log)
logfile = r"R:\\GIS\\GIS_LOGS\\911\\NorthernTierCAD_DataExport.log"  # Run Log
logging.basicConfig(filename=logfile, filemode='a', level=logging.DEBUG)

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())

try:
    # Write Logfile (define logfile write process, each step will append to the log, if the program restarts, the log is wiped clean and restarts again)
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

# Define Work Paths for FGDB:
NORTHERN_TIER_CAD_FGDB = "R:\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier\\Northern_Tier_County_Data_YYYYMMDD.gdb"
NORTHERN_TIER_CAD_FLDR = "R:\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier"
NWPS_STAGING_SVR = Database_Connections + "\\Staging@NWPSRPT.sde\\NWPS_GIS_Staging_ElkCo_PA.DBO.Crawford_County"

# Local variables:
AddressPoint_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\AddressPoint_CrawfordCo"
Ambulance_Company_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Ambulance_Company_CrawfordCo"
Centerline_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Centerline_CrawfordCo"
Counties_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Counties_CrawfordCo"
EMS_Districts_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\EMS_Districts_CrawfordCo"
Fire_Department_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Fire_Department_CrawfordCo"
Fire_Response_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Fire_Response_CrawfordCo"
Fire_Stations_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Fire_Stations_CrawfordCo"
Hydrants_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\NWS_Hydrants_CrawfordCo"
LandingZones_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\LandingZones_CrawfordCo"
Landmarks_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Landmarks_CrawfordCo"
MilePosts_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\MilePosts_CrawfordCo"
Municipalities_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Municipalities_CrawfordCo"
Parcels_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Parcels_CrawfordCo"
Police_Department_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Police_Department_CrawfordCo"
Police_Reporting_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Police_Reporting_CrawfordCo"
Police_Response_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Police_Response_CrawfordCo"
Railroads_CrawfordCo = NORTHERN_TIER_CAD_FGDB + "\\Crawford_County\\Railroads_CrawfordCo"
NTCurrentZIP = NORTHERN_TIER_CAD_FLDR + "\\Northern_Tier_County_Data_" + date + ".gdb"

# NWPS GIS variables
NWPS_Staging_AddressPoint_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.AddressPoint_CrawfordCo"
NWPS_Staging_Ambulance_Company_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Ambulance_Company_CrawfordCo"
NWPS_Staging_Centerline_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Centerline_CrawfordCo"
NWPS_Staging_Counties_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Counties_CrawfordCo"
NWPS_Staging_EMS_Districts_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.EMS_Districts_CrawfordCo"
NWPS_Staging_Fire_Department_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Fire_Department_CrawfordCo"
NWPS_Staging_Fire_Response_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Fire_Response_CrawfordCo"
NWPS_Staging_Fire_Stations_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Fire_Stations_CrawfordCo"
NWPS_Staging_Hydrants_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.NWS_Hydrants_CrawfordCo"
NWPS_Staging_LandingZones_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.LandingZones_CrawfordCo"
NWPS_Staging_Landmarks_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Landmarks_CrawfordCo"
NWPS_Staging_MilePosts_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.MilePosts_CrawfordCo"
NWPS_Staging_Municipalities_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Municipalities_CrawfordCo"
NWPS_Staging_Parcels_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Parcels_CrawfordCo"
NWPS_Staging_Police_Department_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Police_Department_CrawfordCo"
NWPS_Staging_Police_Reporting_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Police_Reporting_CrawfordCo"
NWPS_Staging_Police_Response_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Police_Response_CrawfordCo"
NWPS_Staging_Railroads_CrawfordCo = NWPS_STAGING_SVR + "\\NWPS_GIS_Staging_ElkCo_PA.DBO.Railroads_CrawfordCo"

start_time = time.time()

print ("============================================================================")
print ("Updating Northern Tier CAD data: "+ str(Day) + " " + str(Time))
print ("Will update the following:")
print ("\nAddress Points")
print ("Ambulance Company")
print ("Centerlines")
print ("Counties")
print ("EMS Districts")
print ("Fire Departments")
print ("Fire Response")
print ("Fire Stations")
print ("Hydrants")
print ("Landing Zones")
print ("Landmarks")
print ("Mile Posts")
print ("Municipalities")
print ("Parcels")
print ("Police Department")
print ("Police Reporting")
print ("Police Response")
print ("\n From " + NORTHERN_TIER_CAD_FGDB + " to " + NWPS_STAGING_SVR)
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Northern Tier CAD data: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nAddress Points", logfile)
write_log("Ambulance Company", logfile)
write_log("Centerlines", logfile)
write_log("Counties", logfile)
write_log("EMS Districts", logfile)
write_log("Fire Departments", logfile)
write_log("Fire Response", logfile)
write_log("Fire Stations", logfile)
write_log("Hydrants", logfile)
write_log("Landing Zones", logfile)
write_log("Landmarks", logfile)
write_log("Mile Posts", logfile)
write_log("Municipalities", logfile)
write_log("Parcels", logfile)
write_log("Police Department", logfile)
write_log("Police Reporting", logfile)
write_log("Police Response", logfile)
write_log("\n From " + NORTHERN_TIER_CAD_FGDB + " to " + NWPS_STAGING_SVR, logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)


print ("\n Checking for connectivity to ELK Co server via VPN")
write_log("\n Checking for connectivity to ELK Co server via VPN", logfile)

try:
    # Check to see if VPN is connected (if VPN is connected, the database connection to the Northern Tier CAD - GIS staging server is available, if the VPN is not connected, it will not be available and program will exit)
    if arcpy.Exists(NWPS_STAGING_SVR):
        print ("Connection to ELK Co via VPN verified - beginging data update process")
        write_log("Connection to ELK Co via VPN verified - beginging data update process", logfile)
except:
    print ("\n Unable to connect to staging server - be sure to connect Elk Co VPN and restart program")
    write_log("Unable to connect to staging server - be sure to connect Elk Co VPN and restart program", logfile)
    logging.exception('Got exception on connect to staging server - be sure to connect Elk Co VPN logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Checking to see if ZIP file exists, if so, delete it
    if os.path.exists(NTCurrentZIP):
        os.remove(NTCurrentZIP)
        print ("\n Northern_Tier_County_Data_" + date + ".gdb.zip exists, deleting...")
        write_log("Northern_Tier_County_Data_" + date + ".gdb.zip exists, deleting...",logfile)
except:
    print ("\n Unable to delete Northern_Tier_County_Data_" + date + ".gdb.zip")
    write_log(" Unable to delete Northern_Tier_County_Data_" + date + ".gdb.zip", logfile)
    logging.exception('Got exception on delete Northern_Tier_County_Data_" + date + ".gdb.zip logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("\n Updating Address Points")
write_log("\n Updating Address Points", logfile)

try:
    # Delete Features - Staging Address Points
    arcpy.DeleteFeatures_management(NWPS_Staging_AddressPoint_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_AddressPoint_CrawfordCo")
    write_log("\n Unable to delete rows from NWPS_Staging_AddressPoint_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_AddressPoint_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Staging Address Points
    arcpy.Append_management(AddressPoint_CrawfordCo, NWPS_Staging_AddressPoint_CrawfordCo, "NO_TEST", 'DiscrpAgID "DiscrpAgID" true true false 75 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',DiscrpAgID,-1,-1;DateUpdate "DateUpdate" true true false 8 Date 0 0 ,First,#,'+AddressPoint_CrawfordCo+',DateUpdate,-1,-1;Effective "Effective" true true false 8 Date 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Effective,-1,-1;Expire "Expire" true true false 8 Date 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Expire,-1,-1;Site_NGUID "Site_NGUID" true true false 254 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Site_NGUID,-1,-1;Country "Country" true true false 2 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Country,-1,-1;State "State" true true false 2 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',State,-1,-1;County "County" true true false 40 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',County,-1,-1;AddCode "AddCode" true true false 506 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',AddCode,-1,-1;AddDataURI "AddDataURI" true true false 254 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',AddDataURI,-1,-1;Inc_Muni "Inc_Muni" true true false 100 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Inc_Muni,-1,-1;Uninc_Comm "Uninc_Comm" true true false 100 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Uninc_Comm,-1,-1;Nbrhd_Comm "Nbrhd_Comm" true true false 100 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Nbrhd_Comm,-1,-1;AddNum_Pre "AddNum_Pre" true true false 50 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',AddNum_Pre,-1,-1;Add_Number "Add_Number" true true false 4 Long 0 10 ,First,#,'+AddressPoint_CrawfordCo+',Add_Number,-1,-1;AddNum_Suf "AddNum_Suf" true true false 15 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',AddNum_Suf,-1,-1;St_PreMod "St_PreMod" true true false 15 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',St_PreMod,-1,-1;St_PreDir "ST_PreDir" true true false 9 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',St_PreDir,-1,-1;St_PreTyp "St_PreTyp" true true false 50 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',St_PreTyp,-1,-1;St_PreSep "St_PreSep" true true false 20 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',St_PreSep,-1,-1;St_Name "St_Name" true true false 60 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',St_Name,-1,-1;St_PosTyp "St_PosTyp" true true false 50 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',St_PosTyp,-1,-1;St_PosDir "St_PosDir" true true false 9 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',St_PosDir,-1,-1;St_PosMod "St_PosMod" true true false 25 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',St_PosMod,-1,-1;LSt_PreDir "LSt_PreDir" true true false 2 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',LSt_PreDir,-1,-1;LSt_Name "LSt_Name" true true false 75 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',LSt_Name,-1,-1;LSt_Type "LSt_Type" true true false 4 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',LSt_Type,-1,-1;LStPosDir "LStPosDir" true true false 2 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',LStPosDir,-1,-1;ESN "ESN" true true false 5 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',ESN,-1,-1;MSAGComm "MSAGComm" true true false 30 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',MSAGComm,-1,-1;Post_Comm "Post_Comm" true true false 40 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Post_Comm,-1,-1;Post_Code "Post_Code" true true false 7 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Post_Code,-1,-1;Post_Code4 "Post_Code4" true true false 4 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Post_Code4,-1,-1;Building "Building" true true false 75 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Building,-1,-1;Floor "Floor" true true false 75 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Floor,-1,-1;Unit "Unit" true true false 75 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Unit,-1,-1;Room "Room" true true false 75 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Room,-1,-1;Seat "Seat" true true false 75 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Seat,-1,-1;Addtl_Loc "Addtl_Loc" true true false 225 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Addtl_Loc,-1,-1;LandmkName "LandmkName" true true false 150 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',LandmkName,-1,-1;Mile_Post "Mile_Post" true true false 150 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Mile_Post,-1,-1;Place_Type "Place_Type" true true false 50 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Place_Type,-1,-1;Placement "Placement" true true false 25 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',Placement,-1,-1;Long "Long" true true false 8 Double 8 38 ,First,#,'+AddressPoint_CrawfordCo+',Long,-1,-1;Lat "Lat" true true false 8 Double 8 38 ,First,#,'+AddressPoint_CrawfordCo+',Lat,-1,-1;Elev "Elev" true true false 4 Long 0 10 ,First,#,'+AddressPoint_CrawfordCo+',Elev,-1,-1;JOIN_ID "JOIN_ID" true true false 4 Long 0 10 ,First,#,'+AddressPoint_CrawfordCo+',JOIN_ID,-1,-1;FullName "FullName" true true false 80 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',FullName,-1,-1;HouseNumberCombinedNwps "HouseNumberCombinedNwps" true true false 50 Text 0 0 ,First,#,'+AddressPoint_CrawfordCo+',FullName,-1,-1', "")
    AddressPoint_result = arcpy.GetCount_management(NWPS_Staging_AddressPoint_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_AddressPoint_CrawfordCo, AddressPoint_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_AddressPoint_CrawfordCo, AddressPoint_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_AddressPoint_CrawfordCo from AddressPoint_CrawfordCo")
    write_log("Unable to append NWPS_Staging_AddressPoint_CrawfordCo from AddressPoint_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_AddressPoint_CrawfordCo from AddressPoint_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Address Points completed")
write_log("     Updating Address Points completed", logfile)

print ("\n Updating Ambulance Company")
write_log("\n Updating Ambulance Company", logfile)

try:
    # Delete Features - Staging Ambulance Co
    arcpy.DeleteFeatures_management(NWPS_Staging_Ambulance_Company_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Ambulance_Company_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Ambulance_Company_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Ambulance_Company_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Staging Ambulance Co
    arcpy.Append_management(Ambulance_Company_CrawfordCo, NWPS_Staging_Ambulance_Company_CrawfordCo, "NO_TEST", "Description \"Description\" true true false 50 Text 0 0 ,First,#,"+Ambulance_Company_CrawfordCo+",Description,-1,-1;ID \"ID\" true true false 4 Long 0 10 ,First,#,"+Ambulance_Company_CrawfordCo+",ID,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Ambulance_Company_result = arcpy.GetCount_management(NWPS_Staging_Ambulance_Company_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Ambulance_Company_CrawfordCo, Ambulance_Company_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Ambulance_Company_CrawfordCo, Ambulance_Company_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Ambulance_Company_CrawfordCo from Ambulance_Company_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Ambulance_Company_CrawfordCo from Ambulance_Company_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Ambulance_Company_CrawfordCo from Ambulance_Company_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Ambulance Company completed")
write_log("     Updating Ambulance Company completed", logfile)

print ("\n Updating Centerlines")
write_log("\n Updating Centerlines", logfile)

try:
    # Delete Features - Staging Centerline
    arcpy.DeleteFeatures_management(NWPS_Staging_Centerline_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Centerline_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Centerline_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Centerline_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Staging Centerline
    arcpy.Append_management(Centerline_CrawfordCo, NWPS_Staging_Centerline_CrawfordCo, "NO_TEST", "DiscrpAgID \"DiscrpAgID\" true true false 75 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",DiscrpAgID,-1,-1;DateUpdate \"DateUpdate\" true true false 8 Date 0 0 ,First,#,"+Centerline_CrawfordCo+",DateUpdate,-1,-1;Effective \"Effective\" true true false 8 Date 0 0 ,First,#,"+Centerline_CrawfordCo+",Effective,-1,-1;Expire \"Expire\" true true false 8 Date 0 0 ,First,#,"+Centerline_CrawfordCo+",Expire,-1,-1;RCL_NGUID \"RCL_NGUID\" true true false 254 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",RCL_NGUID,-1,-1;AdNumPre_L \"AdNumPre_L\" true true false 15 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",AdNumPre_L,-1,-1;AdNumPre_R \"AdNumPre_R\" true true false 15 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",AdNumPre_R,-1,-1;FromAddr_L \"FromAddr_L\" true true false 4 Long 0 10 ,First,#,"+Centerline_CrawfordCo+",FromAddr_L,-1,-1;ToAddr_L \"ToAddr_L\" true true false 4 Long 0 10 ,First,#,"+Centerline_CrawfordCo+",ToAddr_L,-1,-1;FromAddr_R \"FromAddr_R\" true true false 4 Long 0 10 ,First,#,"+Centerline_CrawfordCo+",FromAddr_R,-1,-1;ToAddr_R \"ToAddr_R\" true true false 4 Long 0 10 ,First,#,"+Centerline_CrawfordCo+",ToAddr_R,-1,-1;Parity_L \"Parity_L\" true true false 1 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",Parity_L,-1,-1;Parity_R \"Parity_R\" true true false 1 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",Parity_R,-1,-1;St_PreMod \"St_PreMod\" true true false 15 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",St_PreMod,-1,-1;St_PreDir \"St_PreDir\" true true false 9 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",St_PreDir,-1,-1;St_PreTyp \"St_PreTyp\" true true false 50 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",St_PreTyp,-1,-1;St_PreSep \"St_PreSep\" true true false 20 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",St_PreSep,-1,-1;St_Name \"St_Name\" true true false 60 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",St_Name,-1,-1;St_PosTyp \"St_PosTyp\" true true false 50 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",St_PosTyp,-1,-1;St_PosDir \"St_PosDir\" true true false 9 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",St_PosDir,-1,-1;St_PosMod \"St_PosMod\" true true false 25 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",St_PosMod,-1,-1;LSt_PreDir \"LSt_PreDir\" true true false 2 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",LSt_PreDir,-1,-1;LSt_Name \"LSt_Name\" true true false 75 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",LSt_Name,-1,-1;LSt_Type \"LSt_Type\" true true false 4 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",LSt_Type,-1,-1;LStPosDir \"LStPosDir\" true true false 2 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",LStPosDir,-1,-1;ESN_L \"ESN_L\" true true false 5 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",ESN_L,-1,-1;ESN_R \"ESN_R\" true true false 5 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",ESN_R,-1,-1;MSAGComm_L \"MSAGComm_L\" true true false 30 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",MSAGComm_L,-1,-1;MSAGComm_R \"MSAGComm_R\" true true false 30 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",MSAGComm_R,-1,-1;Country_L \"Country_L\" true true false 2 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",Country_L,-1,-1;Country_R \"Country_R\" true true false 2 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",Country_R,-1,-1;State_L \"State_L\" true true false 2 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",State_L,-1,-1;State_R \"State_R\" true true false 2 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",State_R,-1,-1;County_L \"County_L\" true true false 40 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",County_L,-1,-1;County_R \"County_R\" true true false 40 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",County_R,-1,-1;AddCode_L \"AddCode_L\" true true false 6 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",AddCode_L,-1,-1;AddCode_R \"AddCode_R\" true true false 6 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",AddCode_R,-1,-1;IncMuni_L \"IncMuni_L\" true true false 100 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",IncMuni_L,-1,-1;IncMuni_R \"IncMuni_R\" true true false 100 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",IncMuni_R,-1,-1;UnincCom_L \"UnicCom_L\" true true false 100 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",UnincCom_L,-1,-1;UnincCom_R \"Uninc\" true true false 100 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",UnincCom_R,-1,-1;NbrhdCom_L \"NbrhdCom_L\" true true false 100 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",NbrhdCom_L,-1,-1;NbrhdCom_R \"NbrhdCom_R\" true true false 100 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",NbrhdCom_R,-1,-1;PostCode_L \"PostCode_L\" true true false 7 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",PostCode_L,-1,-1;PostCode_R \"PostCode_R\" true true false 7 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",PostCode_R,-1,-1;PostComm_L \"PostComm_L\" true true false 40 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",PostComm_L,-1,-1;PostComm_R \"PostComm_R\" true true false 40 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",PostComm_R,-1,-1;RoadClass \"RoadClass\" true true false 15 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",RoadClass,-1,-1;OneWay \"OneWay\" true true false 2 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",OneWay,-1,-1;SpeedLimit \"SpeedLimit\" true true false 2 Short 0 5 ,First,#,"+Centerline_CrawfordCo+",SpeedLimit,-1,-1;Valid_L \"Valid_L\" true true false 1 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",Valid_L,-1,-1;Valid_R \"Valid_R\" true true false 1 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",Valid_R,-1,-1;Time \"Time\" true true false 8 Double 8 38 ,First,#,"+Centerline_CrawfordCo+",Time,-1,-1;Max_Height \"Max_Height\" true true false 8 Double 8 38 ,First,#,"+Centerline_CrawfordCo+",Max_Height,-1,-1;Max_Weight \"Max_Weight\" true true false 8 Double 8 38 ,First,#,"+Centerline_CrawfordCo+",Max_Weight,-1,-1;T_ZLev \"T_ZLev\" true true false 2 Short 0 5 ,First,#,"+Centerline_CrawfordCo+",T_ZLev,-1,-1;F_ZLev \"F_ZLev\" true true false 2 Short 0 5 ,First,#,"+Centerline_CrawfordCo+",F_ZLev,-1,-1;JOIN_ID \"JOIN_ID\" true true false 4 Long 0 10 ,First,#,"+Centerline_CrawfordCo+",JOIN_ID,-1,-1;FullName \"FullName\" true true false 80 Text 0 0 ,First,#,"+Centerline_CrawfordCo+",FullName,-1,-1;Shape.STLength() \"Shape.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Centerline_result = arcpy.GetCount_management(NWPS_Staging_Centerline_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Centerline_CrawfordCo, Centerline_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Centerline_CrawfordCo, Centerline_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Centerline_CrawfordCo from Centerline_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Centerline_CrawfordCo from Centerline_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Centerline_CrawfordCo from Centerline_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Centerlines completed")
write_log("     Updating Centerlines completed", logfile)

print ("\n Updating EMS Districts")
write_log("\n Updating EMS Districts", logfile)

try:
    # Delete Features - Staging EMS Districts
    arcpy.DeleteFeatures_management(NWPS_Staging_EMS_Districts_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_EMS_Districts_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_EMS_Districts_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_EMS_Districts_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Append - Staging EMS Districts
    arcpy.Append_management(EMS_Districts_CrawfordCo, NWPS_Staging_EMS_Districts_CrawfordCo, "NO_TEST", "Description \"Description\" true true false 50 Text 0 0 ,First,#,"+EMS_Districts_CrawfordCo+",Description,-1,-1;ID \"ID\" true true false 4 Long 0 10 ,First,#,"+EMS_Districts_CrawfordCo+",ID,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    EMS_Districts_result = arcpy.GetCount_management(NWPS_Staging_EMS_Districts_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_EMS_Districts_CrawfordCo, EMS_Districts_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_EMS_Districts_CrawfordCo, EMS_Districts_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_EMS_Districts_CrawfordCo from EMS_Districts_CrawfordCo")
    write_log("Unable to append NWPS_Staging_EMS_Districts_CrawfordCo from EMS_Districts_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_EMS_Districts_CrawfordCo from EMS_Districts_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating EMS Districts completed")
write_log("     Updating EMS Districts completed", logfile)

print ("\n Updating Fire Department")
write_log("\n Updating Fire Department", logfile)

try:
    # Delete Features - Staging Fire Department
    arcpy.DeleteFeatures_management(NWPS_Staging_Fire_Department_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Fire_Department_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Fire_Department_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Fire_Department_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Staging Fire Department
    arcpy.Append_management(Fire_Department_CrawfordCo, NWPS_Staging_Fire_Department_CrawfordCo, "NO_TEST", "Description \"Description\" true true false 50 Text 0 0 ,First,#,"+Fire_Department_CrawfordCo+",Description,-1,-1;ID \"ID\" true true false 4 Long 0 10 ,First,#,"+Fire_Department_CrawfordCo+",ID,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Fire_Department_result = arcpy.GetCount_management(NWPS_Staging_Fire_Department_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Fire_Department_CrawfordCo, Fire_Department_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Fire_Department_CrawfordCo, Fire_Department_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Fire_Department_CrawfordCo from Fire_Department_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Fire_Department_CrawfordCo from Fire_Department_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Fire_Department_CrawfordCo from Fire_Department_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Fire Department completed")
write_log("     Updating Fire Department completed", logfile)

print ("\n Updating Fire Response")
write_log("\n Updating Fire Response", logfile)

try:
    # Delete Features - Staging Fire Response
    arcpy.DeleteFeatures_management(NWPS_Staging_Fire_Response_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Fire_Response_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Fire_Response_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Fire_Response_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Staging Fire Response
    arcpy.Append_management(Fire_Response_CrawfordCo, NWPS_Staging_Fire_Response_CrawfordCo, "NO_TEST", "Description \"Description\" true true false 50 Text 0 0 ,First,#,"+Fire_Response_CrawfordCo+",Description,-1,-1;ID \"ID\" true true false 4 Long 0 10 ,First,#,"+Fire_Response_CrawfordCo+",ID,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Fire_Response_result = arcpy.GetCount_management(NWPS_Staging_Fire_Response_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Fire_Response_CrawfordCo, Fire_Response_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Fire_Response_CrawfordCo, Fire_Response_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Fire_Department_CrawfordCo from Fire_Department_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Fire_Department_CrawfordCo from Fire_Department_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Fire_Department_CrawfordCo from Fire_Department_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Fire Response completed")
write_log("     Updating Fire Response completed", logfile)

print ("\n Updating Fire Stations")
write_log("\n Updating Fire Stations", logfile)

try:
    # Delete Features - Staging Fire Stations
    arcpy.DeleteFeatures_management(NWPS_Staging_Fire_Stations_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Fire_Stations_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Fire_Stations_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Fire_Stations_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Staging Fire Stations
    arcpy.Append_management(Fire_Stations_CrawfordCo, NWPS_Staging_Fire_Stations_CrawfordCo, "NO_TEST", "Description \"Description\" true true false 50 Text 0 0 ,First,#,"+Fire_Stations_CrawfordCo+",Description,-1,-1;ID \"ID\" true true false 4 Long 0 10 ,First,#,"+Fire_Stations_CrawfordCo+",ID,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Fire_Stations_result = arcpy.GetCount_management(NWPS_Staging_Fire_Stations_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Fire_Stations_CrawfordCo, Fire_Stations_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Fire_Stations_CrawfordCo, Fire_Stations_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Fire_Stations_CrawfordCo from Fire_Stations_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Fire_Stations_CrawfordCo from Fire_Stations_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Fire_Stations_CrawfordCo from Fire_Stations_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Fire Stations completed")
write_log("     Updating Fire Stations completed", logfile)

print ("\n Updating Police Department")
write_log("\n Updating Police Department", logfile)

try:
    # Delete Features - Staging Police Department
    arcpy.DeleteFeatures_management(NWPS_Staging_Police_Department_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Police_Department_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Police_Department_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Police_Department_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Append - Staging Police Department
    arcpy.Append_management(Police_Department_CrawfordCo, NWPS_Staging_Police_Department_CrawfordCo, "NO_TEST", "Description \"Description\" true true false 50 Text 0 0 ,First,#,"+Police_Department_CrawfordCo+",Description,-1,-1;ID \"ID\" true true false 4 Long 0 10 ,First,#,"+Police_Department_CrawfordCo+",ID,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Police_Department_result = arcpy.GetCount_management(NWPS_Staging_Police_Department_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Police_Department_CrawfordCo, Police_Department_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Police_Department_CrawfordCo, Police_Department_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Police_Department_CrawfordCo from Police_Department_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Police_Department_CrawfordCo from Police_Department_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Police_Department_CrawfordCo from Police_Department_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Police Department completed")
write_log("     Updating Police Department completed", logfile)

print ("\n Updating Police Reporting")
write_log("\n Updating Police Reporting", logfile)

try:
    # Delete Features - Staging Police Reporting
    arcpy.DeleteFeatures_management(NWPS_Staging_Police_Reporting_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Police_Reporting_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Police_Reporting_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Police_Reporting_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try: 
    # Append - Staging Police Reporting
    arcpy.Append_management(Police_Reporting_CrawfordCo, NWPS_Staging_Police_Reporting_CrawfordCo, "NO_TEST", "Description \"Description\" true true false 50 Text 0 0 ,First,#,"+Police_Reporting_CrawfordCo+",Description,-1,-1;ID \"ID\" true true false 4 Long 0 10 ,First,#,"+Police_Reporting_CrawfordCo+",ID,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Police_Reporting_result = arcpy.GetCount_management(NWPS_Staging_Police_Reporting_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Police_Reporting_CrawfordCo, Police_Reporting_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Police_Reporting_CrawfordCo, Police_Reporting_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Police_Reporting_CrawfordCo from Police_Reporting_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Police_Reporting_CrawfordCo from Police_Reporting_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Police_Reporting_CrawfordCo from Police_Reporting_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Police Reporting completed")
write_log("     Updating Police Reporting completed", logfile)

print ("\n Updating Police Response")
write_log("\n Updating Police Response", logfile)

try:
    # Delete Features - Staging Police Response
    arcpy.DeleteFeatures_management(NWPS_Staging_Police_Response_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Police_Response_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Police_Response_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Police_Response_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Staging Police Response
    arcpy.Append_management(Police_Response_CrawfordCo, NWPS_Staging_Police_Response_CrawfordCo, "NO_TEST", "Description \"Description\" true true false 50 Text 0 0 ,First,#,"+Police_Response_CrawfordCo+",Description,-1,-1;ID \"ID\" true true false 4 Long 0 10 ,First,#,"+Police_Response_CrawfordCo+",ID,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Police_Response_result = arcpy.GetCount_management(NWPS_Staging_Police_Response_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Police_Response_CrawfordCo, Police_Response_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Police_Response_CrawfordCo, Police_Response_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Police_Response_CrawfordCo from Police_Response_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Police_Response_CrawfordCo from Police_Response_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Police_Response_CrawfordCo from Police_Response_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Police Response completed")
write_log("     Updating Police Response completed", logfile)

print ("\n Updating Counties")
write_log("\n Updating Counties", logfile)

try:
    # Delete Features - Counties
    arcpy.DeleteFeatures_management(NWPS_Staging_Counties_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Counties_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Counties_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Counties_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Counties
    arcpy.Append_management(Counties_CrawfordCo, NWPS_Staging_Counties_CrawfordCo, "NO_TEST", "Shape_Leng \"Shape_Leng\" true true false 8 Double 8 38 ,First,#,"+Counties_CrawfordCo+",Shape_Leng,-1,-1;DiscrpAgID \"DiscrpAgID\" true true false 75 Text 0 0 ,First,#,"+Counties_CrawfordCo+",DiscrpAgID,-1,-1;DateUpdate \"DateUpdate\" true true false 8 Date 0 0 ,First,#,"+Counties_CrawfordCo+",DateUpdate,-1,-1;Effective \"Effective\" true true false 8 Date 0 0 ,First,#,"+Counties_CrawfordCo+",Effective,-1,-1;Expire \"Expire\" true true false 8 Date 0 0 ,First,#,"+Counties_CrawfordCo+",Expire,-1,-1;CntyNGUID \"CntyNGUID\" true true false 254 Text 0 0 ,First,#,"+Counties_CrawfordCo+",CntyNGUID,-1,-1;Country \"Country\" true true false 2 Text 0 0 ,First,#,"+Counties_CrawfordCo+",Country,-1,-1;State \"State\" true true false 2 Text 0 0 ,First,#,"+Counties_CrawfordCo+",State,-1,-1;County \"County\" true true false 75 Text 0 0 ,First,#,"+Counties_CrawfordCo+",County,-1,-1;Shape.STArea() \"Shape.STArea()\" false false true 0 Double 0 0 ,First,#;Shape.STLength() \"Shape.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Counties_result = arcpy.GetCount_management(NWPS_Staging_Counties_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Counties_CrawfordCo, Counties_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Counties_CrawfordCo, Counties_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Counties_CrawfordCo from Counties_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Counties_CrawfordCo from Counties_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Counties_CrawfordCo from Counties_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Counties completed")
write_log("     Updating Counties completed", logfile)

print ("\n Updating Hydrants")
write_log("\n Updating Hydrants", logfile)

try:
    # Delete Features - Hydrants
    arcpy.DeleteFeatures_management(NWPS_Staging_Hydrants_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Hydrants_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Hydrants_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Hydrants_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make Feature Layer - Hydrants
    NWS_HYDRANTS_Layer = arcpy.MakeFeatureLayer_management(Hydrants_CrawfordCo, "NWS_HYDRANTS_Layer", "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;ID ID VISIBLE NONE;NWS_ADDRESS_ID NWS_ADDRESS_ID VISIBLE NONE;NWS_HYDRANT_ID NWS_HYDRANT_ID VISIBLE NONE;NWS_HYDRANT_NUMBER NWS_HYDRANT_NUMBER VISIBLE NONE;NWS_HYDRANT_LOCATIONDESCRIPTION NWS_HYDRANT_LOCATIONDESCRIPTION VISIBLE NONE;NWS_HYDRANT_SERIAL_NUMBER NWS_HYDRANT_SERIAL_NUMBER VISIBLE NONE;NWS_HYDRANT_IN_SERVICE NWS_HYDRANT_IN_SERVICE VISIBLE NONE;NWS_HYDRANT_COLOR NWS_HYDRANT_COLOR VISIBLE NONE;SIZE SIZE VISIBLE NONE;TYPE TYPE VISIBLE NONE;GPM GPM VISIBLE NONE")
except:
    print ("\n Unable to make feature layer from Hydrants_CrawfordCo")
    write_log("Unable to make feature layer from Hydrants_CrawfordCo", logfile)
    logging.exception('Got exception on make feature layer from Hydrants_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append hydrants from layer file to NWPS_Staging_Hydrants_CrawfordCo - Hydrants
    arcpy.Append_management(NWS_HYDRANTS_Layer, NWPS_Staging_Hydrants_CrawfordCo, "TEST", "", "")
##    arcpy.Append_management(NWS_HYDRANTS_Layer, NWPS_Staging_Hydrants_CrawfordCo, "NO_TEST", 'ID "ID" true true false 4 Long 0 10 ,First,#,NWS_HYDRANTS_Layer,ID,-1,-1;NWS_ADDRESS_ID "NWS_ADDRESS_ID" true true false 4 Long 0 10 ,First,#,NWS_HYDRANTS_Layer,NWS_ADDRESS_ID,-1,-1;NWS_HYDRANT_ID "NWS_HYDRANT_ID" true true false 4 Long 0 10 ,First,#,NWS_HYDRANTS_Layer,NWS_HYDRANT_ID,-1,-1;NWS_HYDRANT_NUMBER "NWS_HYDRANT_NUMBER" true true false 20 Text 0 0 ,First,#,NWS_HYDRANTS_Layer,NWS_HYDRANT_NUMBER,-1,-1;NWS_HYDRANT_LOCATIONDESCRIPTION "NWS_HYDRANT_LOCATIONDESCRIPTION" true true false 50 Text 0 0 ,First,#,NWS_HYDRANTS_Layer,NWS_HYDRANT_LOCATIONDESCRIPTION,-1,-1;NWS_HYDRANT_SERIAL_NUMBER "NWS_HYDRANT_SERIAL_NUMBER" true true false 20 Text 0 0 ,First,#,NWS_HYDRANTS_Layer,NWS_HYDRANT_SERIAL_NUMBER,-1,-1;NWS_HYDRANT_IN_SERVICE "NWS_HYDRANT_IN_SERVICE" true true false 3 Text 0 0 ,First,#,NWS_HYDRANTS_Layer,NWS_HYDRANT_IN_SERVICE,-1,-1;NWS_HYDRANT_COLOR "NWS_HYDRANT_COLOR" true true false 30 Text 0 0 ,First,#,NWS_HYDRANTS_Layer,NWS_HYDRANT_COLOR,-1,-1;SIZE "SIZE" true true false 50 Text 0 0 ,First,#,NWS_HYDRANTS_Layer,SIZE,-1,-1;TYPE "TYPE" true true false 50 Text 0 0 ,First,#,NWS_HYDRANTS_Layer,TYPE,-1,-1;GPM "GPM" true true false 50 Text 0 0 ,First,#,NWS_HYDRANTS_Layer,GPM,-1,-1', "")
    Hydrants_result = arcpy.GetCount_management(NWPS_Staging_Hydrants_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Hydrants_CrawfordCo, Hydrants_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Hydrants_CrawfordCo, Hydrants_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Hydrants_CrawfordCo from Hydrants_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Hydrants_CrawfordCo from Hydrants_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Hydrants_CrawfordCo from Hydrants_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Hydrants completed")
write_log("     Updating Hydrants completed", logfile)

print ("\n Updating Landing Zones")
write_log("\n Updating Landing Zones", logfile)

try:
    # Delete Features Landing Zones
    arcpy.DeleteFeatures_management(NWPS_Staging_LandingZones_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_LandingZones_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_LandingZones_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_LandingZones_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Landing Zones
    arcpy.Append_management(LandingZones_CrawfordCo, NWPS_Staging_LandingZones_CrawfordCo, "NO_TEST", "DiscrpAgID \"Agency ID\" true true false 75 Text 0 0 ,First,#,"+LandingZones_CrawfordCo+",DiscrpAgID,-1,-1;DateUpdate \"Date Updated\" true true false 8 Date 0 0 ,First,#,"+LandingZones_CrawfordCo+",DateUpdate,-1,-1;Effective \"Effective\" true true false 8 Date 0 0 ,First,#,"+LandingZones_CrawfordCo+",Effective,-1,-1;Expire \"Expiration Date\" true true false 8 Date 0 0 ,First,#,"+LandingZones_CrawfordCo+",Expire,-1,-1;LZ_ID \"LZ Number\" true true false 2 Short 0 5 ,First,#,"+LandingZones_CrawfordCo+",LZ_ID,-1,-1;LZ_Name \"LZ Name\" true true false 254 Text 0 0 ,First,#,"+LandingZones_CrawfordCo+",LZ_Name,-1,-1;LAT \"LAT\" true true false 8 Double 8 38 ,First,#,"+LandingZones_CrawfordCo+",LAT,-1,-1;LONG \"LONG\" true true false 8 Double 8 38 ,First,#,"+LandingZones_CrawfordCo+",LONG,-1,-1", "")
    Landing_Zones_result = arcpy.GetCount_management(NWPS_Staging_LandingZones_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_LandingZones_CrawfordCo, Landing_Zones_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_LandingZones_CrawfordCo, Landing_Zones_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_LandingZones_CrawfordCo from LandingZones_CrawfordCo")
    write_log("Unable to append NWPS_Staging_LandingZones_CrawfordCo from LandingZones_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_LandingZones_CrawfordCo from LandingZones_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Landing Zones completed")
write_log("     Updating Landing Zones completed", logfile)

print ("\n Updating Landmarks")
write_log("\n Updating Landmarks", logfile)

try:
    # Delete Features - Landmarks
    arcpy.DeleteFeatures_management(NWPS_Staging_Landmarks_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Landmarks_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Landmarks_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Landmarks_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Landmarks
    arcpy.Append_management(Landmarks_CrawfordCo, NWPS_Staging_Landmarks_CrawfordCo, "NO_TEST", "DiscrpAgID \"Agency ID\" true true false 75 Text 0 0 ,First,#,"+Landmarks_CrawfordCo+",DiscrpAgID,-1,-1;DateUpdate \"Date Updated\" true true false 8 Date 0 0 ,First,#,"+Landmarks_CrawfordCo+",DateUpdate,-1,-1;Effective \"Effective Date\" true true false 8 Date 0 0 ,First,#,"+Landmarks_CrawfordCo+",Effective,-1,-1;Expire \"Expiration Date\" true true false 8 Date 0 0 ,First,#,"+Landmarks_CrawfordCo+",Expire,-1,-1;LMNP_NGUID \"Landmark Name GID\" true true false 254 Text 0 0 ,First,#,"+Landmarks_CrawfordCo+",LMNP_NGUID,-1,-1;Site_NGUID \"Site GID\" true true false 254 Text 0 0 ,First,#,"+Landmarks_CrawfordCo+",Site_NGUID,-1,-1;ACLMNNGUID \"Complete Landmark Name GID\" true true false 254 Text 0 0 ,First,#,"+Landmarks_CrawfordCo+",ACLMNNGUID,-1,-1;LMNamePart \"Landmark Name Part\" true true false 150 Text 0 0 ,First,#,"+Landmarks_CrawfordCo+",LMNamePart,-1,-1;LMNP_Order \"Landmark Name Part Order\" true true false 1 Text 0 0 ,First,#,"+Landmarks_CrawfordCo+",LMNP_Order,-1,-1", "")
    Landmarks_result = arcpy.GetCount_management(NWPS_Staging_Landmarks_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Landmarks_CrawfordCo, Landmarks_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Landmarks_CrawfordCo, Landmarks_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Landmarks_CrawfordCo from Landmarks_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Landmarks_CrawfordCo from Landmarks_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Landmarks_CrawfordCo from Landmarks_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Landmarks completed")
write_log("     Updating Landmarks completed", logfile)

print ("\n Updating Mile Posts")
write_log("\n Updating Mile Posts", logfile)

try:
    # Delete Features - Mile Posts
    arcpy.DeleteFeatures_management(NWPS_Staging_MilePosts_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_MilePosts_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_MilePosts_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_MilePosts_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Mile Posts
    arcpy.Append_management(MilePosts_CrawfordCo, NWPS_Staging_MilePosts_CrawfordCo, "NO_TEST", "DiscrpAgID \"Agency ID\" true true false 75 Text 0 0 ,First,#,"+MilePosts_CrawfordCo+",DiscrpAgID,-1,-1;DateUpdate \"Date Updated\" true true false 8 Date 0 0 ,First,#,"+MilePosts_CrawfordCo+",DateUpdate,-1,-1;MileMNGUID \"Mile Post GID\" true true false 254 Text 0 0 ,First,#,"+MilePosts_CrawfordCo+",MileMNGUID,-1,-1;MileM_Unit \"MP Unit\" true true false 15 Text 0 0 ,First,#,"+MilePosts_CrawfordCo+",MileM_Unit,-1,-1;MileMValue \"MP Measurement\" true true false 8 Double 8 38 ,First,#,"+MilePosts_CrawfordCo+",MileMValue,-1,-1;MileM_Rte \"MP Route Name\" true true false 100 Text 0 0 ,First,#,"+MilePosts_CrawfordCo+",MileM_Rte,-1,-1;MileM_Type \"MP Type\" true true false 15 Text 0 0 ,First,#,"+MilePosts_CrawfordCo+",MileM_Type,-1,-1;MileM_Ind \"MP Indicator\" true true false 1 Text 0 0 ,First,#,"+MilePosts_CrawfordCo+",MileM_Ind,-1,-1", "")
    MilePosts_result = arcpy.GetCount_management(NWPS_Staging_MilePosts_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_MilePosts_CrawfordCo, MilePosts_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_MilePosts_CrawfordCo, MilePosts_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_MilePosts_CrawfordCo from MilePosts_CrawfordCo")
    write_log("Unable to append NWPS_Staging_MilePosts_CrawfordCo from MilePosts_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_MilePosts_CrawfordCo from MilePosts_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Mile Posts completed")
write_log("     Updating Mile Posts completed", logfile)

print ("\n Updating Municipalites")
write_log("\n Updating Municipalites", logfile)

try:
    # Delete Features - Municipalites
    arcpy.DeleteFeatures_management(NWPS_Staging_Municipalities_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Municipalities_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Municipalities_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Municipalities_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Municipalities
    arcpy.Append_management(Municipalities_CrawfordCo, NWPS_Staging_Municipalities_CrawfordCo, "NO_TEST", "DiscrpAgID \"DiscrpAgID\" true true false 75 Text 0 0 ,First,#,"+Municipalities_CrawfordCo+",DiscrpAgID,-1,-1;DateUpdate \"DateUpdate\" true true false 8 Date 0 0 ,First,#,"+Municipalities_CrawfordCo+",DateUpdate,-1,-1;Effective \"Effective\" true true false 8 Date 0 0 ,First,#,"+Municipalities_CrawfordCo+",Effective,-1,-1;Expire \"Expire\" true true false 8 Date 0 0 ,First,#,"+Municipalities_CrawfordCo+",Expire,-1,-1;Shape_Leng \"Shape_Leng\" true true false 8 Double 8 38 ,First,#,"+Municipalities_CrawfordCo+",Shape_Leng,-1,-1;IncM_NGUID \"IncM_NGUID\" true true false 254 Text 0 0 ,First,#,"+Municipalities_CrawfordCo+",IncM_NGUID,-1,-1;Country \"Country\" true true false 2 Text 0 0 ,First,#,"+Municipalities_CrawfordCo+",Country,-1,-1;State \"State\" true true false 2 Text 0 0 ,First,#,"+Municipalities_CrawfordCo+",State,-1,-1;County \"County\" true true false 75 Text 0 0 ,First,#,"+Municipalities_CrawfordCo+",County,-1,-1;AddCode \"AddCode\" true true false 6 Text 0 0 ,First,#,"+Municipalities_CrawfordCo+",AddCode,-1,-1;Inc_Muni \"Inc_Muni\" true true false 100 Text 0 0 ,First,#,"+Municipalities_CrawfordCo+",Inc_Muni,-1,-1;Shape.STArea() \"Shape.STArea()\" false false true 0 Double 0 0 ,First,#;Shape.STLength() \"Shape.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Municipalities_result = arcpy.GetCount_management(NWPS_Staging_Municipalities_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Municipalities_CrawfordCo, Municipalities_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Municipalities_CrawfordCo, Municipalities_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Municipalities_CrawfordCo from Municipalities_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Municipalities_CrawfordCo from Municipalities_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Municipalities_CrawfordCo from Municipalities_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Municipalities completed")
write_log("     Updating Municipalities completed", logfile)

print ("\n Updating Parcels")
write_log("\n Updating Parcels", logfile)

try:
    # Delete Features - Parcels
    arcpy.DeleteFeatures_management(NWPS_Staging_Parcels_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Parcels_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Parcels_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Parcels_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Parcels
    arcpy.Append_management(Parcels_CrawfordCo, NWPS_Staging_Parcels_CrawfordCo, "NO_TEST", "ParcelID \"ParcelID\" true true false 25 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",ParcelID,-1,-1;Map_Num \"Map_Num\" true true false 50 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",Map_Num,-1,-1;Own \"Own\" true true false 100 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",Own,-1,-1;Add_Number \"Add_Number\" true true false 4 Long 0 10 ,First,#,"+Parcels_CrawfordCo+",Add_Number,-1,-1;AddNum_Suf \"AddNum_Suf\" true true false 15 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",AddNum_Suf,-1,-1;St_PreDir \"St_PreDir\" true true false 9 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",St_PreDir,-1,-1;St_Name \"St_Name\" true true false 60 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",St_Name,-1,-1;St_PostType \"St_PostType\" true true false 50 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",St_PostType,-1,-1;St_PostDir \"St_PostDir\" true true false 9 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",St_PostDir,-1,-1;City \"City\" true true false 50 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",City,-1,-1;Add_State \"Add_State\" true true false 2 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",Add_State,-1,-1;Zip \"Zip\" true true false 10 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",Zip,-1,-1;Muni \"Muni\" true true false 100 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",Muni,-1,-1;County \"County\" true true false 75 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",County,-1,-1;State \"State\" true true false 2 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",State,-1,-1;Contry \"Contry\" true true false 2 Text 0 0 ,First,#,"+Parcels_CrawfordCo+",Contry,-1,-1;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Parcels_result = arcpy.GetCount_management(NWPS_Staging_Parcels_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Parcels_CrawfordCo, Parcels_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Parcels_CrawfordCo, Parcels_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Parcels_CrawfordCo from Parcels_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Parcels_CrawfordCo from Parcels_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Parcels_CrawfordCo from Parcels_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Parcels completed")
write_log("     Updating Parcels completed", logfile)

print ("\n Updating Railroads")
write_log("\n Updating Railroads", logfile)

try:
    # Delete Features - Railroads
    arcpy.DeleteFeatures_management(NWPS_Staging_Railroads_CrawfordCo)
except:
    print ("\n Unable to delete rows from NWPS_Staging_Railroads_CrawfordCo")
    write_log("Unable to delete rows from NWPS_Staging_Railroads_CrawfordCo", logfile)
    logging.exception('Got exception on delete rows from NWPS_Staging_Railroads_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Append - Railroads
    arcpy.Append_management(Railroads_CrawfordCo, NWPS_Staging_Railroads_CrawfordCo, "NO_TEST", "DiscrpAgID \"DiscrpAgID\" true true false 75 Text 0 0 ,First,#,"+Railroads_CrawfordCo+",DiscrpAgID,-1,-1;DateUpdate \"DateUpdate\" true true false 8 Date 0 0 ,First,#,"+Railroads_CrawfordCo+",DateUpdate,-1,-1;RS_NGUID \"RS_NGUID\" true true false 254 Text 0 0 ,First,#,"+Railroads_CrawfordCo+",RS_NGUID,-1,-1;RLOWN \"RLOWN\" true true false 100 Text 0 0 ,First,#,"+Railroads_CrawfordCo+",RLOWN,-1,-1;RLOP \"RLOP\" true true false 100 Text 0 0 ,First,#,"+Railroads_CrawfordCo+",RLOP,-1,-1;Trck_Right \"Trck_Right\" true true false 100 Text 0 0 ,First,#,"+Railroads_CrawfordCo+",Trck_Right,-1,-1;RMPL \"RMPL\" true true false 8 Double 8 38 ,First,#,"+Railroads_CrawfordCo+",RMPL,-1,-1;RMPH \"RMPH\" true true false 8 Double 8 38 ,First,#,"+Railroads_CrawfordCo+",RMPH,-1,-1;Muni \"Muni\" true true false 100 Text 0 0 ,First,#,"+Railroads_CrawfordCo+",Muni,-1,-1;County \"County\" true true false 75 Text 0 0 ,First,#,"+Railroads_CrawfordCo+",County,-1,-1;State \"State\" true true false 2 Text 0 0 ,First,#,"+Railroads_CrawfordCo+",State,-1,-1;Contry \"Contry\" true true false 2 Text 0 0 ,First,#,"+Railroads_CrawfordCo+",Contry,-1,-1;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
    Railroads_result = arcpy.GetCount_management(NWPS_Staging_Railroads_CrawfordCo)
    print ('{} has {} records'.format(NWPS_Staging_Railroads_CrawfordCo, Railroads_result[0]))
    write_log('{} has {} records'.format(NWPS_Staging_Railroads_CrawfordCo, Railroads_result[0]), logfile)
except:
    print ("\n Unable to append NWPS_Staging_Railroads_CrawfordCo from Railroads_CrawfordCo")
    write_log("Unable to append NWPS_Staging_Railroads_CrawfordCo from Railroads_CrawfordCo", logfile)
    logging.exception('Got exception on append NWPS_Staging_Railroads_CrawfordCo from Railroads_CrawfordCo logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Updating Railroads completed")
write_log("     Updating Railroads completed", logfile)

print ("       Waiting for script to release schema lock on FGDB...taking a 3 minute intermission, please wait")
write_log("       Waiting for script to release schema lock on FGDB...taking a 3 minute intermission, please wait",logfile)

#Wait 180 seconds (3 minutes) to release lock from FGDB
time.sleep(180)

print ("\n Renaming Northern_Tier_County_Data_YYYYMMDD.gdb to Northern_Tier_County_Data_" + date + ".gdb")
write_log("\n Renaming Northern_Tier_County_Data_YYYYMMDD.gdb to Northern_Tier_County_Data_" + date + ".gdb",logfile)

try:
    # Rename Northern_Tier_County_Data_YYYYMMDD.gdb to FGDB with current date as file name (rename the YYYYMMDD portion of the FGDB name name to the current date in the same format)
    arcpy.management.Rename(NORTHERN_TIER_CAD_FGDB, r"R:\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier\\Northern_Tier_County_Data_" + date + ".gdb", "Workspace")
except: 
    print ("\n Unable to rename Northern_Tier_County_Data_YYYYMMDD.gdb to Northern_Tier_County_Data_" + date + ".gdb")
    write_log("Unable to rename Northern_Tier_County_Data_YYYYMMDD.gdb to  Northern_Tier_County_Data_" + date + ".gdb", logfile)
    logging.exception('Got exception on rename Northern_Tier_County_Data_YYYYMMDD.gdb to  Northern_Tier_County_Data_" + date + ".gdb logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("     Renaming Northern_Tier_County_Data_YYYYMMDD.gdb to Northern_Tier_County_Data_" + date + ".gdb completed")
write_log("     Renaming Northern_Tier_County_Data_YYYYMMDD.gdb to Northern_Tier_County_Data_" + date + ".gdb completed",logfile)

##print ("       Waiting for script to release schema lock on FGDB...taking another 3 minute intermission, please wait")
##write_log("       Waiting for script to release schema lock on FGDB...taking another 3 minute intermission, please wait",logfile)
##
###Wait 180 seconds (3 minutes) to release lock from FGDB
##time.sleep(180)
##
##print ("\n Compressing Northern_Tier_County_Data_" + date + ".gdb into ZIP file for archive")
##write_log("Compressing Northern_Tier_County_Data_" + date + ".gdb into ZIP file for archive",logfile)
##
##NTCurrentFGDB = NORTHERN_TIER_CAD_FLDR + "\\Northern_Tier_County_Data_" + date + ".gdb"
##
##try:
##    # Creating ZIP file from existing FGDB with current date stamp
##    if arcpy.Exists(NTCurrentFGDB):
##        shutil.make_archive(NTCurrentFGDB, 'zip', NORTHERN_TIER_CAD_FLDR)
##        print ("\n  Compressing Current FGDB into ZIP file...")
##        write_log("  Compressing Current FGDB into ZIP file...",logfile)
##except:
##    print ("\n Unable to compress Northern_Tier_County_Data_" + date + ".gdb into zipfile")
##    write_log("Unable to compress Northern_Tier_County_Data_" + date + ".gdb into zipfile", logfile)
##    logging.exception('Got exception on compress Northern_Tier_County_Data_" + date + ".gdb into zipfile logged at:'  + str(Day) + " " + str(Time))
##    raise
##    sys.exit ()
##
##
##try:
##    # Once FGDB is compressed into ZIP, delete source FGDB
##    if os.path.exists("R:\\GIS\\NorthernTierCAD_GIS\\Exported FGDB to NorthernTier\\Northern_Tier_County_Data_" + date + ".gdb.zip"):
##        arcpy.Delete_management(NTCurrentFGDB)
##        print ("\n   Deleting Northern_Tier_County_Data_" + date + ".gdb...")
##        write_log("   Deleting Northern_Tier_County_Data_" + date + ".gdb...",logfile)
##except:
##    print ("\n Unable to delete Northern_Tier_County_Data_" + date + ".gdb")
##    write_log("Unable to delete Northern_Tier_County_Data_" + date + ".gdb", logfile)
##    logging.exception('Got exception on delete Northern_Tier_County_Data_" + date + ".gdb logged at:'  + str(Day) + " " + str(Time))
##    raise
##    sys.exit ()
##
##print ("     Compressing Northern_Tier_County_Data_" + date + ".gdb into ZIP file for archive completed")
##write_log("     Compressing Northern_Tier_County_Data_" + date + ".gdb into ZIP file for archive completed",logfile)  

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n ALL NORTHERN TIER CAD DATA UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n ALL NORTHERN TIER CAD DATA UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("\n Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
write_log("\n Elapsed time: " + str (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))), logfile)
print ("==============================================================")

try:
    # Opening folder where Northern Tier FGDB exists, to allow user to archive/delete older versions
    print ("\n Opening "+NORTHERN_TIER_CAD_FLDR)
    print ("     You need to ZIP the  current FGDB, delete the orignal when that's completed, and then manually delete prior FGDBs in folder, leaving only Northern_Tier_County_Data_" + date + ".gdb.zip")
    NORTHERN_TIER_CAD_FLDR=os.path.realpath(NORTHERN_TIER_CAD_FLDR)
    os.startfile(NORTHERN_TIER_CAD_FLDR)
except: 
    print ("\n Unable to open "+NORTHERN_TIER_CAD_FLDR)
    write_log("Unable to open "+NORTHERN_TIER_CAD_FLDR, logfile)
    logging.exception('Got exception on Unable to open "+NORTHERN_TIER_CAD_FLDR logged at:'  + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("\n                   Northern Tier CAD Data Export from local staging DB to Elk Staging DB completed")
print ("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+")
write_log("\n                   Northern Tier CAD Data Export from local staging DB to Elk Staging DB completed", logfile)
write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+", logfile)

del arcpy
sys.exit()
