# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Locator_Rebuilder.py
# Created on: 2019-03-06 
# Updated on: 2019-09-22
# Added logging and try/except blocks for troubleshooting
#
# Author: Phil Baranyai/GIS Manager
# 
# Description: 
#  Rebuild the following locators (from individual locators - where applicable):
#
#  CC_Roads_Locator
#       CL_Number_CCLocator //  CL_Name_CCLocator
#  CC_Parcel_Locator
#       BuildingOnly_MBLU_CCLocator // BuildingOnly_PID_CCLocator
#       BuildingOnly_UPI_CCLocator // TaxParcel_UPI_CCLocator
#       TaxParcel_PID_CCLocator // TaxParcel_CAMA_CCLocator   
#       TaxParcel_ALTPRCLID_CCLocator
#  CC_Name_Locator
#       ADDR_Name_CCLocator // BuildingOnly_Name_CCLocator
#       BuildingOnly_ADDR1 // TaxParcel_ADDR1_CCLocator
#       TaxParcel_Name_CCLocator // ADDR_FName_CCLocator
#  CC_Address_Search
#       ADDR_PriAdd_CCLocator // ADDR_OldAdd_CCLocator
#       BuildingOnly_ADDR1_CCLocator // ADDR_HSESTREET_CCLocator
#       BuildingOnly_ADDR2_CCLocator // TaxParcel_ADDR1_CCLocator
#       TaxParcel_ADDR2_CCLocator
#  Crawford_Roads_Locator
#       CL_Number_PubLocator //  CL_Name_PubLocator
#  Crawford_Parcel_Locator
#       BuildingOnly_MBLU_PubLocator // BuildingOnly_PID_PubLocator
#       BuildingOnly_UPI_PubLocator // TaxParcel_UPI_PubLocator
#       TaxParcel_PID_PubLocator // TaxParcel_CAMA_PubLocator   
#       TaxParcel_ALTPRCLID_PubLocator
#  Crawford_Name_Locator
#       ADDR_Name_PubLocator // BuildingOnly_Name_PubLocator
#       BuildingOnly_ADDR1_PubLocator // TaxParcel_ADDR1_PubLocator
#       TaxParcel_Name_PubLocator // ADDR_FName_PubLocator
#  Crawford_Address_Search
#       ADDR_PriAdd_PubLocator // ADDR_OldAdd_PubLocator
#       BuildingOnly_ADDR1_PubLocator // ADDR_HSESTREET_PubLocator
#       BuildingOnly_ADDR2_PubLocator // TaxParcel_ADDR1_PubLocator
#       TaxParcel_ADDR2_PubLocator
#  Crawford_Landmarks_Locator
#  Crawford_Cemeteries_Locator
# ---------------------------------------------------------------------------

# import modules
import arcpy
import sys
import datetime
import os
import traceback
import logging
import pprint

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\Locator_Rebuilder.log"  
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Set up Time/Date
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

# Locator location
Locators = r"\\CCFILE\\anybody\\GIS\\CurrentWebsites\\Locators"
IntranetLocatorsWorkspace = Locators + "\\Intranet_Locators\\Locator_workspace"
PublicLocatorsWorkspace = Locators + "\\Public_Locators\\Locator_workspace"
IntranetLocators =  Locators + "\\Intranet_Locators"
PublicLocators = Locators + "\\Public_Locators"

# Staging location
#ArcServer_Admin = r"C:\\Users\\pbaranyai\\AppData\\Roaming\\ESRI\\Desktop10.7\\ArcCatalog\\arcgis on ccgis.crawfordcountypa.net (admin).ags" #GIS01 Machine
ArcServer_Admin = r"C:\\Users\\arcadmin\\AppData\\Roaming\\ESRI\\Desktop10.7\\ArcCatalog\\arcgis on ccgis.crawfordcountypa.net (admin).ags" #CCORBWEAVER Machine
#ArcServer_Staging = r"C:\\Users\\pbaranyai\\AppData\\Local\\ESRI\\Desktop10.7\\Staging\\arcgis on ccgis.crawfordcountypa.net (admin)" #GIS01 Machine
ArcServer_Staging = r"C:\\Users\\arcadmin\\AppData\\Roaming\\ESRI\\Desktop10.7\\Staging\\arcgis on ccgis.crawfordcountypa.net (admin)" #CCORBWEAVER Machine
Draft_Staging = r"\\CCFILE\\anybody\\GIS\\CurrentWebsites\\Locators\\Draft_Services"

# Local variables:
CC_Roads_Locator = IntranetLocators + "\\CC_Roads_Locator"
CC_Parcel_Locator = IntranetLocators + "\\CC_Parcel_Locator"
CC_Name_Locator = IntranetLocators + "\\CC_Name_Locator"
CC_Address_Search = IntranetLocators + "\\CC_Address_Search"
BuildingOnly_UPI_CCLocator = IntranetLocatorsWorkspace + "\\BuildingOnly_UPI_CCLocator"
BuildingOnly_PID_CCLocator = IntranetLocatorsWorkspace + "\\BuildingOnly_PID_CCLocator"
BuildingOnly_Name_CCLocator = IntranetLocatorsWorkspace + "\\BuildingOnly_Name_CCLocator"
BuildingOnly_ADDR3_CCLocator = IntranetLocatorsWorkspace + "\\BuildingOnly_ADDR3_CCLocator"
BuildingOnly_ADDR2_CCLocator = IntranetLocatorsWorkspace + "\\BuildingOnly_ADDR2_CCLocator"
BuildingOnly_ADDR1_CCLocator = IntranetLocatorsWorkspace + "\\BuildingOnly_ADDR1_CCLocator"
BuildingOnly_Control_CCLocator = IntranetLocatorsWorkspace + "\\BuildingOnly_Control_CCLocator"
TaxParcel_UPI_CCLocator = IntranetLocatorsWorkspace + "\\TaxParcel_UPI_CCLocator"
TaxParcel_PID_CCLocator = IntranetLocatorsWorkspace + "\\TaxParcel_PID_CCLocator"
TaxParcel_Name_CCLocator = IntranetLocatorsWorkspace + "\\TaxParcel_Name_CCLocator"
TaxParcel_CAMA_CCLocator = IntranetLocatorsWorkspace + "\\TaxParcel_CAMA_CCLocator"
TaxParcel_ADDR3_CCLocator = IntranetLocatorsWorkspace + "\\TaxParcel_ADDR3_CCLocator"
TaxParcel_ADDR2_CCLocator = IntranetLocatorsWorkspace + "\\TaxParcel_ADDR2_CCLocator"
TaxParcel_ADDR1_CCLocator = IntranetLocatorsWorkspace + "\\TaxParcel_ADDR1_CCLocator"
TaxParcel_ALTPRCLID_CCLocator = IntranetLocatorsWorkspace + "\\TaxParcel_ALTPRCLID_CCLocator"
TaxParcel_Control_CCLocator = IntranetLocatorsWorkspace + "\\TaxParcel_Control_CCLocator"
ADDR_OldAdd_CCLocator = IntranetLocatorsWorkspace + "\\ADDR_OldAdd_CCLocator"
ADDR_Name_CCLocator = IntranetLocatorsWorkspace + "\\ADDR_Name_CCLocator"
ADDR_FName_CCLocator = IntranetLocatorsWorkspace + "\\ADDR_FName_CCLocator"
ADDR_HSESTREET_CCLocator = IntranetLocatorsWorkspace + "\\ADDR_HSESTREET_CCLocator"
Crawford_Roads_Locator = PublicLocators + "\\Crawford_Roads_Locator"
Crawford_Parcel_Locator = PublicLocators + "\\Crawford_Parcel_Locator"
Crawford_Name_Locator = PublicLocators + "\\Crawford_Name_Locator"
Crawford_Address_Search = PublicLocators + "\\Crawford_Address_Search"
Crawford_Landmarks_Locator = PublicLocators + "\\Crawford_Landmarks_Locator"
Crawford_Cemeteries_Locator = PublicLocators + "\\Crawford_Cemeteries_Locator"
BuildingOnly_UPI_PubLocator = PublicLocatorsWorkspace + "\\BuildingOnly_UPI_PubLocator"
BuildingOnly_PID_PubLocator = PublicLocatorsWorkspace + "\\BuildingOnly_PID_PubLocator"
BuildingOnly_Name_PubLocator = PublicLocatorsWorkspace + "\\BuildingOnly_Name_PubLocator"
BuildingOnly_ADDR3_PubLocator = PublicLocatorsWorkspace + "\\BuildingOnly_ADDR3_PubLocator"
BuildingOnly_ADDR2_PubLocator = PublicLocatorsWorkspace + "\\BuildingOnly_ADDR2_PubLocator"
BuildingOnly_ADDR1_PubLocator = PublicLocatorsWorkspace + "\\BuildingOnly_ADDR1_PubLocator"
BuildingOnly_Control_PubLocator = PublicLocatorsWorkspace + "\\BuildingOnly_Control_PubLocator"
TaxParcel_UPI_PubLocator = PublicLocatorsWorkspace + "\\TaxParcel_UPI_PubLocator"
TaxParcel_PID_PubLocator = PublicLocatorsWorkspace + "\\TaxParcel_PID_PubLocator"
TaxParcel_Name_PubLocator = PublicLocatorsWorkspace + "\\TaxParcel_Name_PubLocator"
TaxParcel_CAMA_PubLocator = PublicLocatorsWorkspace + "\\TaxParcel_CAMA_PubLocator"
TaxParcel_ADDR3_PubLocator = PublicLocatorsWorkspace + "\\TaxParcel_ADDR3_PubLocator"
TaxParcel_ADDR2_PubLocator = PublicLocatorsWorkspace + "\\TaxParcel_ADDR2_PubLocator"
TaxParcel_ADDR1_PubLocator = PublicLocatorsWorkspace + "\\TaxParcel_ADDR1_PubLocator"
TaxParcel_ALTPRCLID_PubLocator = PublicLocatorsWorkspace + "\\TaxParcel_ALTPRCLID_PubLocator"
TaxParcel_Control_PubLocator = PublicLocatorsWorkspace + "\\TaxParcel_Control_PubLocator"
ADDR_OldAdd_PubLocator = PublicLocatorsWorkspace + "\\ADDR_OldAdd_PubLocator"
ADDR_Name_PubLocator = PublicLocatorsWorkspace + "\\ADDR_Name_PubLocator"
ADDR_FName_PubLocator = PublicLocatorsWorkspace + "\\ADDR_FName_PubLocator"
ADDR_HSESTREET_PubLocator = PublicLocatorsWorkspace + "\\ADDR_HSESTREET_PubLocator"
TAX_PARCELS_PID_AUTO = IntranetLocatorsWorkspace + "\\TAX_PARCELS_PID_AUTOMATION_LOC"
BUILDINGONLY_PID_AUTO = IntranetLocatorsWorkspace + "\\BUILDINGONLY_PID_AUTOMATION_LOC"

# Publishing variables
gis_server_connection_file = ArcServer_Admin
CRAWROAD_locator_path = Crawford_Roads_Locator
CRAWROAD_sddraft_file = Draft_Staging +"\\Service_Def_Draft\\Crawford_Roads_Locator.sddraft"
CRAWROAD_sd_file = Draft_Staging + "\\Service_Def\\Crawford_Roads_Locator.sd"
CRAWROAD_service_name = "Crawford_Roads_Locator"
CRAWROAD_summary = "Roads composite locator"
CRAWROAD_tags = "Centerlines, roads, Crawford County PA, locator"
CCADD_locator_path = CC_Address_Search
CCADD_sddraft_file = Draft_Staging +"\\Service_Def_Draft\\CC_Address_Search.sddraft"
CCADD_sd_file = Draft_Staging + "\\Service_Def\\CC_Address_Search.sd"
CCADD_service_name = "CC_Address_Search"
CCADD_summary = "Composite Address locator - Internal use only"
CCADD_tags = "Address, Crawford County PA, intranet, locator"
CCNAME_locator_path = CC_Name_Locator
CCNAME_sddraft_file = Draft_Staging +"\\Service_Def_Draft\\CC_Name_Locator.sddraft"
CCNAME_sd_file = Draft_Staging + "\\Service_Def\\CC_Name_Locator.sd"
CCNAME_service_name = "CC_Name_Locator"
CCNAME_summary = "Composite Name - Internal use only"
CCNAME_tags = "name, Crawford County PA, intranet, locator"
CCPARCEL_locator_path = CC_Parcel_Locator
CCPARCEL_sddraft_file = Draft_Staging +"\\Service_Def_Draft\\CC_Parcel_Locator.sddraft"
CCPARCEL_sd_file = Draft_Staging + "\\Service_Def\\CC_Parcel_Locator.sd"
CCPARCEL_service_name = "CC_Parcel_Locator"
CCPARCEL_summary = "Composite Parcel locator - Internal use only"
CCPARCEL_tags = "tax parcels, building only, Crawford County PA, intranet, locator"
CCROAD_locator_path = CC_Roads_Locator
CCROAD_sddraft_file = Draft_Staging +"\\Service_Def_Draft\\CC_Roads_Locator.sddraft"
CCROAD_sd_file = Draft_Staging + "\\Service_Def\\CC_Roads_Locator.sd"
CCROAD_service_name = "CC_Roads_Locator"
CCROAD_summary = "Composite Roads locator - Internal use only"
CCROAD_tags = "Roads, Street, Centerline, Crawford County PA, intranet, locator"
CRAWADD_locator_path = Crawford_Address_Search
CRAWADD_sddraft_file = Draft_Staging +"\\Service_Def_Draft\\Crawford_Address_Search.sddraft"
CRAWADD_sd_file = Draft_Staging + "\\Service_Def\\Crawford_Address_Search.sd"
CRAWADD_service_name = "Crawford_Address_Search"
CRAWADD_summary = "Composite Address locator"
CRAWADD_tags = "Address, Crawford County PA, locator"
CRAWCEM_locator_path = Crawford_Cemeteries_Locator
CRAWCEM_sddraft_file = Draft_Staging +"\\Service_Def_Draft\\Crawford_Cemeteries_Locator.sddraft"
CRAWCEM_sd_file = Draft_Staging + "\\Service_Def\\Crawford_Cemeteries_Locator.sd"
CRAWCEM_service_name = "Crawford_Cemeteries_Locator"
CRAWCEM_summary = "Cemetery locator"
CRAWCEM_tags = "Cemetery, Crawford County PA, locator"
CRAWLMKS_locator_path = Crawford_Landmarks_Locator
CRAWLMKS_sddraft_file = Draft_Staging +"\\Service_Def_Draft\\Crawford_Landmarks_Locator.sddraft"
CRAWLMKS_sd_file = Draft_Staging + "\\Service_Def\\Crawford_Landmarks_Locator.sd"
CRAWLMKS_service_name = "Crawford_Landmarks_Locator"
CRAWLMKS_summary = "Landmark locator"
CRAWLMKS_tags = "Landmarks, Crawford County PA, locator"
CRAWNAME_locator_path = Crawford_Name_Locator
CRAWNAME_sddraft_file = Draft_Staging +"\\Service_Def_Draft\\Crawford_Name_Locator.sddraft"
CRAWNAME_sd_file = Draft_Staging + "\\Service_Def\\Crawford_Name_Locator.sd"
CRAWNAME_service_name = "Crawford_Name_Locator"
CRAWNAME_summary = "Name Composite Locator"
CRAWNAME_tags = "Name, Crawford County PA, locator"
CRAWPCL_locator_path = Crawford_Parcel_Locator
CRAWPCL_sddraft_file = Draft_Staging +"\\Service_Def_Draft\\Crawford_Parcel_Locator.sddraft"
CRAWPCL_sd_file = Draft_Staging + "\\Service_Def\\Crawford_Parcel_Locator.sd"
CRAWPCL_service_name = "Crawford_Parcel_Locator"
CRAWPCL_summary = "Parcel composite locator"
CRAWPCL_tags = "tax parcels, Crawford County PA, locator"

start_time = time.time()

print ("======================================================================================================================================")
print ("Updating Locators: "+ str(Day) + " " + str(Time))
print ("Will rebuild the following locators:")
print ("\nCC_Roads_Locator")
print ("CC_Parcel_Locator")
print ("CC_Name_Locator")
print ("CC_Address_Search")
print ("Crawford_Roads_Locator")
print ("Crawford_Parcel_Locator")
print ("Crawford_Name_Locator")
print ("Crawford_Address_Search")
print ("Crawford_Landmarks_Locator")
print ("Crawford_Cemeteries_Locator")
print ("\n From source of CRAW_INTERNAL / PUBLIC_WEB (where applicable) and publish (overwrite) existing locator services in AGOL and Portal")
print ("======================================================================================================================================")

write_log("======================================================================================================================================", logfile)
write_log("Updating Locators: "+ str(Day) + " " + str(Time), logfile)
write_log("Will rebuild the following locators:", logfile)
write_log("\nCC_Roads_Locator", logfile)  
write_log("CC_Parcel_Locator", logfile) 
write_log("CC_Name_Locator", logfile) 
write_log("CC_Address_Search", logfile) 
write_log("Crawford_Roads_Locator", logfile)
write_log("Crawford_Parcel_Locator", logfile)
write_log("Crawford_Name_Locator", logfile)
write_log("Crawford_Address_Search", logfile)
write_log("Crawford_Landmarks_Locator", logfile)
write_log("Crawford_Cemeteries_Locator", logfile)
write_log("\n From source of CRAW_INTERNAL / PUBLIC_WEB (where applicable) and publish (overwrite) existing locator services in AGOL and Portal", logfile)
write_log("======================================================================================================================================", logfile)

print ("Rebuilding Spatial Locators: " + str(Day) + " " + str(Time))
write_log("Rebuilding Spatial Locators: " + str(Day) + " " + str(Time), logfile)

print ("\n Rebuild Individual Public Locators")
print ("=======================================")
write_log("\n Rebuild Individual Public Locators", logfile)
write_log("=======================================", logfile)

print ("\n Rebuilding ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB")
write_log("\n Rebuilding ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB", logfile)

try:
    # Rebuild ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(ADDR_HSESTREET_PubLocator)
except:
    print ("\n Unable to rebuild ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB")
    write_log("Unable to rebuild ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB completed")
write_log("       Rebuilding ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding ADDR_Name Locator from Address_Points - PUBLIC_WEB")
write_log("\n Rebuilding ADDR_Name Locator from Address_Points - PUBLIC_WEB ", logfile)

try:
    # Rebuild ADDR_Name Locator from Address_Points - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(ADDR_Name_PubLocator)
except:
    print ("\n Unable to rebuild ADDR_Name Locator from Address_Points - PUBLIC_WEB")
    write_log("\n Unable to rebuild ADDR_Name Locator from Address_Points - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild ADDR_Name Locator from Address_Points - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB completed")
write_log("       Rebuilding ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding ADDR_FName Locator from Address_Points - PUBLIC_WEB")
write_log("\n Rebuilding ADDR_FName Locator from Address_Points - PUBLIC_WEB ", logfile)

try:
    # Rebuild ADDR_FName Locator from Address_Points - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(ADDR_FName_PubLocator)
except:
    print ("\n Unable to rebuild ADDR_FName Locator from Address_Points - PUBLIC_WEB")
    write_log("\n Unable to rebuild ADDR_FName Locator from Address_Points - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild ADDR_FName Locator from Address_Points - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB completed")
write_log("       Rebuilding ADDR_HSESTREET Locator from Address_Points - PUBLIC_WEB completed", logfile)
    
print ("\n Rebuilding ADDR_OldAdd Locator - Public")
write_log("\n Rebuilding ADDR_OldAdd Locator - Public", logfile)

try:
    # Rebuild ADDR_OldAdd Locator from Address_Points - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(ADDR_OldAdd_PubLocator)
except:
    print ("\n Unable to rebuild ADDR_OldAdd Locator from Address_Points - PUBLIC_WEB")
    write_log("\n Unable to rebuild ADDR_OldAdd Locator from Address_Points - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild ADDR_OldAdd Locator from Address_Points - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding ADDR_OldAdd Locator from Address_Points - PUBLIC_WEB completed")
write_log("       Rebuilding ADDR_OldAdd Locator from Address_Points - PUBLIC_WEB completed", logfile)
    
print ("\n Rebuilding Crawford_Roads_Locator - Public")
write_log("\n Rebuilding Crawford_Roads_Locator - Public", logfile)

try:
    # Rebuild Crawford_Roads_Locator from Street Centerline - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(Crawford_Roads_Locator)
except:
    print ("\n Unable to rebuild Crawford_Roads_Locator from Street Centerline - PUBLIC_WEB")
    write_log("\n Unable to rebuild Crawford_Roads_Locator from Street Centerline - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild Crawford_Roads_Locator from Street Centerline - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding Crawford_Roads_Locator from Street Centerline - PUBLIC_WEB completed")
write_log("       Rebuilding Crawford_Roads_Locator from Street Centerline - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding TaxParcel_ADDR1 Locator from Tax Parcels - PUBLIC_WEB")
write_log("\n Rebuilding TaxParcel_ADDR1 Locator from Tax Parcels - PUBLIC_WEB", logfile)

try:
    # Rebuild TaxParcel_ADDR1 Locator
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_ADDR1_PubLocator)
except:
    print ("\n Unable to rebuild TaxParcel_ADDR1 Locator from Tax Parcels - PUBLIC_WEB")
    write_log("\n Unable to rebuild TaxParcel_ADDR1 Locator from Tax Parcels - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild TaxParcel_ADDR1 Locator from Tax Parcels - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_ADDR1 Locator from Tax Parcels - PUBLIC_WEB completed")
write_log("       Rebuilding TaxParcel_ADDR1 Locator from Tax Parcels - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding TaxParcel_ADDR2 Locator - Public")
write_log("\n Rebuilding TaxParcel_ADDR2 Locator - Public", logfile)

try:
    # Rebuild TaxParcel_ADDR2 Locator from Tax Parcels - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_ADDR2_PubLocator)
except:
    print ("\n Unable to rebuild TaxParcel_ADDR2 Locator from Tax Parcels - PUBLIC_WEB")
    write_log("\n Unable to rebuild TaxParcel_ADDR2 Locator from Tax Parcels - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild TaxParcel_ADDR2 Locator from Tax Parcels - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_ADDR2 Locator from Tax Parcels - PUBLIC_WEB completed")
write_log("       Rebuilding TaxParcel_ADDR2 Locator from Tax Parcels - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding TaxParcel_ADDR3 Locator - Public")
write_log("\n Rebuilding TaxParcel_ADDR3 Locator - Public", logfile)

try:
    # Rebuild TaxParcel_ADDR3 Locator from Tax Parcels - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_ADDR3_PubLocator)
except:
    print ("\n Unable to rebuild TaxParcel_ADDR3 Locator from Tax Parcels - PUBLIC_WEB")
    write_log("\n Unable to rebuild TaxParcel_ADDR3 Locator from Tax Parcels - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild TaxParcel_ADDR3 Locator from Tax Parcels - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_ADDR3 Locator from Tax Parcels - PUBLIC_WEB completed")
write_log("       Rebuilding TaxParcel_ADDR3 Locator from Tax Parcels - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding TaxParcel_CAMA(MBLU) Locator - Public")
write_log("\n Rebuilding TaxParcel_CAMA(MBLU) Locator - Public", logfile)

try:
    # Rebuild TaxParcel_CAMA(MBLU) Locator from Tax Parcels - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_CAMA_PubLocator)
except:
    print ("\n Unable to rebuild TaxParcel_CAMA(MBLU) Locator from Tax Parcels - PUBLIC_WEB")
    write_log("\n Unable to rebuild TaxParcel_CAMA(MBLU) Locator from Tax Parcels - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild TaxParcel_CAMA(MBLU) Locator from Tax Parcels - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_CAMA(MBLU) Locator from Tax Parcels - PUBLIC_WEB completed")
write_log("       Rebuilding TaxParcel_CAMA(MBLU) Locator from Tax Parcels - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding TaxParcel_Name Locator - Public")
write_log("\n Rebuilding TaxParcel_Name Locator - Public", logfile)

try:
    # Rebuild TaxParcel_Name Locator from Tax Parcels - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_Name_PubLocator)
except:
    print ("\n Unable to rebuild TaxParcel_Name Locator from Tax Parcels - PUBLIC_WEB")
    write_log("\n Unable to rebuild TaxParcel_Name Locator from Tax Parcels - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild TaxParcel_Name Locator from Tax Parcels - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_Name Locator from Tax Parcels - PUBLIC_WEB completed")
write_log("       Rebuilding TaxParcel_Name Locator from Tax Parcels - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding TaxParcel_PID Locator from Tax Parcels - PUBLIC_WEB")
write_log("\n Rebuilding TaxParcel_PID Locator from Tax Parcels - PUBLIC_WEB", logfile)

try:
    # TaxParcel_PID Locator from Tax Parcels - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_PID_PubLocator)
except:
    print ("\n Unable to rebuild TaxParcel_PID Locator from Tax Parcels - PUBLIC_WEB")
    write_log("\n Unable to rebuild TaxParcel_PID Locator from Tax Parcels - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild TaxParcel_PID Locator from Tax Parcels - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_PID Locator from Tax Parcels - PUBLIC_WEB completed")
write_log("       Rebuilding TaxParcel_PID Locator from Tax Parcels - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding TaxParcel_UPI Locator from Tax Parcels - PUBLIC_WEB")
write_log("\n Rebuilding TaxParcel_UPI Locator from Tax Parcels - PUBLIC_WEB", logfile)

try:
    # TaxParcel_UPI Locator from Tax Parcels - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_UPI_PubLocator)
except:
    print ("\n Unable to rebuild TaxParcel_UPI Locator from Tax Parcels - PUBLIC_WEB")
    write_log("\n Unable to rebuild TaxParcel_UPI Locator from Tax Parcels - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild TaxParcel_UPI Locator from Tax Parcels - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_UPI Locator from Tax Parcels - PUBLIC_WEB completed")
write_log("       Rebuilding TaxParcel_UPI Locator from Tax Parcels - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding TaxParcel_Control Locator from Tax Parcels - PUBLIC_WEB")
write_log("\n Rebuilding TaxParcel_Control Locator from Tax Parcels - PUBLIC_WEB", logfile)

try:
    # TaxParcel_Control Locator from Tax Parcels - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_Control_PubLocator)
except:
    print ("\n Unable to rebuild TaxParcel_Control Locator from Tax Parcels - PUBLIC_WEB")
    write_log("\n Unable to rebuild TaxParcel_Control Locator from Tax Parcels - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild TaxParcel_Control Locator from Tax Parcels - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_Control Locator from Tax Parcels - PUBLIC_WEB completed")
write_log("       Rebuilding TaxParcel_Control Locator from Tax Parcels - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding TaxParcel_ALTPRCLID Locator from Tax Parcels - PUBLIC_WEB")
write_log("\n Rebuilding TaxParcel_ALTPRCLID Locator from Tax Parcels - PUBLIC_WEB", logfile)

try:
    # Rebuild TaxParcel_ALTPRCLID Locator from Tax Parcels - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_ALTPRCLID_PubLocator)
except:
    print ("\n Unable to rebuild TaxParcel_ALTPRCLID Locator from Tax Parcels - PUBLIC_WEB")
    write_log("\n Unable to rebuild TaxParcel_ALTPRCLID Locator from Tax Parcels - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild TaxParcel_ALTPRCLID Locator from Tax Parcels - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_ALTPRCLID Locator from Tax Parcels - PUBLIC_WEB completed")
write_log("       Rebuilding TaxParcel_ALTPRCLID Locator from Tax Parcels - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding BuildingOnly_ADDR1 Locator from Building/Trailer Only - PUBLIC_WEB")
write_log("\n Rebuilding BuildingOnly_ADDR1 Locator from Building/Trailer Only - PUBLIC_WEB", logfile)

try:
    # BuildingOnly_ADDR1 Locator from Building/Trailer Only - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_ADDR1_PubLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_ADDR1 Locator from Building/Trailer Only - PUBLIC_WEB")
    write_log("\n Unable to rebuild BuildingOnly_ADDR1 Locator from Building/Trailer Only - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_ADDR1 Locator from Building/Trailer Only - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_ADDR1 Locator from Building/Trailer Only - PUBLIC_WEB completed")
write_log("       Rebuilding BuildingOnly_ADDR1 Locator from Building/Trailer Only - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding BuildingOnly_Control Locator from Building/Trailer Only - PUBLIC_WEB")
write_log("\n Rebuilding BuildingOnly_Control Locator from Building/Trailer Only - PUBLIC_WEB", logfile)

try:
    # BuildingOnly_Control Locator from Building/Trailer Only - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_Control_PubLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_Control Locator from Building/Trailer Only - PUBLIC_WEB")
    write_log("\n Unable to rebuild BuildingOnly_Control Locator from Building/Trailer Only - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_Control Locator from Building/Trailer Only - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_Control Locator from Building/Trailer Only - PUBLIC_WEB completed")
write_log("       Rebuilding BuildingOnly_Control Locator from Building/Trailer Only - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding BuildingOnly_ADDR2 Locator from Building/Trailer Only - PUBLIC_WEB")
write_log("\n Rebuilding BuildingOnly_ADDR2 Locator from Building/Trailer Only - PUBLIC_WEB", logfile)

try:
    # BuildingOnly_ADDR2 Locator from Building/Trailer Only - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_ADDR2_PubLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_ADDR2 Locator from Building/Trailer Only - PUBLIC_WEB")
    write_log("\n Unable to rebuild BuildingOnly_ADDR2 Locator from Building/Trailer Only - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_ADDR2 Locator from Building/Trailer Only - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_ADDR2 Locator from Building/Trailer Only - PUBLIC_WEB completed")
write_log("       Rebuilding BuildingOnly_ADDR2 Locator from Building/Trailer Only - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding BuildingOnly_ADDR3 Locator from Building/Trailer Only - PUBLIC_WEB")
write_log("\n Rebuilding BuildingOnly_ADDR3 Locator from Building/Trailer Only - PUBLIC_WEB", logfile)

try:
    # BuildingOnly_ADDR3 Locator from Building/Trailer Only - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_ADDR3_PubLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_ADDR3 Locator from Building/Trailer Only - PUBLIC_WEB")
    write_log("\n Unable to rebuild BuildingOnly_ADDR3 Locator from Building/Trailer Only - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_ADDR3 Locator from Building/Trailer Only - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_ADDR3 Locator from Building/Trailer Only - PUBLIC_WEB completed")
write_log("       Rebuilding BuildingOnly_ADDR3 Locator from Building/Trailer Only - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding BuildingOnly_Name Locator from Building/Trailer Only - PUBLIC_WEB")
write_log("\n Rebuilding BuildingOnly_Name Locator from Building/Trailer Only - PUBLIC_WEB", logfile)

try:
    # BuildingOnly_Name Locator from Building/Trailer Only - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_Name_PubLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_Name Locator from Building/Trailer Only - PUBLIC_WEB")
    write_log("\n Unable to rebuild BuildingOnly_Name Locator from Building/Trailer Only - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_Name Locator from Building/Trailer Only - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_Name Locator from Building/Trailer Only - PUBLIC_WEB completed")
write_log("       Rebuilding BuildingOnly_Name Locator from Building/Trailer Only - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding BuildingOnly_PID Locator from Building/Trailer Only - PUBLIC_WEB")
write_log("\n Rebuilding BuildingOnly_PID Locator from Building/Trailer Only - PUBLIC_WEB", logfile)

try:
    # BuildingOnly_PID Locator from Building/Trailer Only - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_PID_PubLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_PID Locator from Building/Trailer Only - PUBLIC_WEB")
    write_log("\n Unable to rebuild BuildingOnly_PID Locator from Building/Trailer Only - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_PID Locator from Building/Trailer Only - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_PID Locator from Building/Trailer Only - PUBLIC_WEB completed")
write_log("       Rebuilding BuildingOnly_PID Locator from Building/Trailer Only - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding BuildingOnly_UPI Locator from Building/Trailer Only - PUBLIC_WEB")
write_log("\n Rebuilding BuildingOnly_UPI Locator from Building/Trailer Only - PUBLIC_WEB", logfile)

try:
    # Rebuild BuildingOnly_UPI Locator from Building/Trailer Only - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_UPI_PubLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_UPI Locator from Building/Trailer Only - PUBLIC_WEB")
    write_log("\n Unable to rebuild BuildingOnly_UPI Locator from Building/Trailer Only - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_UPI Locator from Building/Trailer Only - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_UPI Locator from Building/Trailer Only - PUBLIC_WEB completed")
write_log("       Rebuilding BuildingOnly_UPI Locator from Building/Trailer Only - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding Crawford Cemeteries locator from Cemeteries - PUBLIC_WEB")
write_log("\n Rebuilding Crawford Cemeteries locator from Cemeteries - PUBLIC_WEB", logfile)

try:
    # Rebuild Crawford Cemeteries from Cemeteries - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(Crawford_Cemeteries_Locator)
except:
    print ("\n Unable to rebuild Crawford Cemeteries locator from Cemeteries - PUBLIC_WEB")
    write_log("\n Unable to rebuild Crawford Cemeteries locator from Cemeteries - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild Crawford Cemeteries locator from Cemeteries - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding Crawford Cemeteries locator from Cemeteries - PUBLIC_WEB completed")
write_log("       Rebuilding Crawford Cemeteries locator from Cemeteries - PUBLIC_WEB completed", logfile)

print ("\n Rebuilding Crawford Landmarks locator from Landmarks - PUBLIC_WEB")
write_log("\n Rebuilding Crawford Landmarks locator from Landmarks - PUBLIC_WEB", logfile)

try:
    # Rebuild Crawford Landmarks locator from Landmarks - PUBLIC_WEB
    arcpy.RebuildAddressLocator_geocoding(Crawford_Landmarks_Locator)
except:
    print ("\n Unable to rebuild Crawford Landmarks locator from Landmarks - PUBLIC_WEB")
    write_log("\n Unable to rebuild Crawford Landmarks locator from Landmarks - PUBLIC_WEB", logfile)
    logging.exception('Got exception on rebuild Crawford Landmarks locator from Landmarks - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding Crawford Landmarks locator from Landmarks - PUBLIC_WEB completed")
write_log("       Rebuilding Crawford Landmarks locator from Landmarks - PUBLIC_WEB completed", logfile)

print ("\n Rebuild Composite Public Locators")
print ("=======================================")

write_log("\n Rebuild Composite Public Locators", logfile)
write_log("=======================================", logfile)

print ("\n Rebuilding Crawford Address Search Locator from individual locators")
write_log("\n Rebuilding Crawford Address Search Locator from individual locators", logfile)

try:
    # Rebuild Crawford Address Search Locator from individual locators
    arcpy.RebuildAddressLocator_geocoding(Crawford_Address_Search)
except:
    print ("\n Unable to rebuild Crawford Address Search Locator from individual locators")
    write_log("\n Unable to rebuild Crawford Address Search Locator from individual locators", logfile)
    logging.exception('Got exception on rebuild Crawford Address Search Locator from individual locators logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding Crawford Address Search Locator from individual locators completed")
write_log("       Rebuilding Crawford Address Search Locator from individual locators completed", logfile)

print ("\n Rebuilding Crawford Name Locator from individual locators")
write_log("\n Rebuilding Crawford Name Locator from individual locators", logfile)

try:
    # Rebuild Crawford Name Locator from individual locators
    arcpy.RebuildAddressLocator_geocoding(Crawford_Name_Locator)
except:
    print ("\n Unable to rebuild Crawford Name Locator from individual locators")
    write_log("\n Unable to rebuild Crawford Name Locator from individual locators", logfile)
    logging.exception('Got exception on rebuild Crawford Name Locator from individual locators logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding Crawford Name Locator from individual locators completed")
write_log("       Rebuilding Crawford Name Locator from individual locators completed", logfile)

print ("\n Rebuilding Crawford Parcel Locator from individual locators")
write_log("\n Rebuilding Crawford Parcel Locator from individual locators", logfile)

try:
    # Crawford Parcel Locator from individual locators
    arcpy.RebuildAddressLocator_geocoding(Crawford_Parcel_Locator)
except:
    print ("\n Unable to rebuild Crawford Parcel Locator from individual locators")
    write_log("\n Unable to rebuild Crawford Parcel Locator from individual locators", logfile)
    logging.exception('Got exception on rebuild Crawford Parcel Locator from individual locators logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding Crawford Parcel Locator from individual locators completed")
write_log("       Rebuilding Crawford Parcel Locator from individual locators completed", logfile)

print ("\n Rebuild Individual Intranet Locators")
print ("=======================================")

write_log("\n Rebuild Individual Intranet Locators", logfile)
write_log("=======================================", logfile)

print ("\n Rebuilding HSESTREET_INTRA Locator from Address_Points - CRAW_INTERNAL")
write_log("\n Rebuilding HSESTREET_INTRA Locator from Address_Points - CRAW_INTERNAL", logfile)

try:
    # Rebuild HSESTREET_INTRA Locator from Address_Points - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(ADDR_HSESTREET_CCLocator)
    arcpy.RebuildAddressLocator_geocoding(in_address_locator="R:/GIS/CurrentWebsites/Locators/Intranet_Locators/Locator_workspace/ADDR_HSESTREET_CCLocator")
except:
    print ("\n Unable to rebuild HSESTREET_INTRA Locator from Address_Points - CRAW_INTERNAL")
    write_log("Unable to rebuild HSESTREET_INTRA Locator from Address_Points - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild HSESTREET_INTRA Locator from Address_Points - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding HSESTREET_INTRA Locator from Address_Points - CRAW_INTERNAL completed")
write_log("       Rebuilding HSESTREET_INTRA Locator from Address_Points - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding ADDR_NAME_INTRA from Address_Points - CRAW_INTERNAL")
write_log("\n Rebuilding ADDR_NAME_INTRA from Address_Points - CRAW_INTERNAL", logfile)

try:
    # Rebuild ADDR_NAME_INTRA Locator from Address_Points - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(ADDR_Name_CCLocator)
except:
    print ("\n Unable to rebuild ADDR_NAME_INTRA Locator from Address_Points - CRAW_INTERNAL")
    write_log("\n Unable to rebuild ADDR_NAME_INTRA Locator from Address_Points - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild ADDR_NAME_INTRA Locator from Address_Points - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding ADDR_NAME_INTRA Locator from Address_Points - CRAW_INTERNAL completed")
write_log("       Rebuilding ADDR_NAME_INTRA Locator from Address_Points - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding ADDR_FNAME_INTRA from Address_Points - CRAW_INTERNAL")
write_log("\n Rebuilding ADDR_FNAME_INTRA from Address_Points - CRAW_INTERNAL", logfile)

try:
    # Rebuild ADDR_FNAME_INTRA Locator from Address_Points - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(ADDR_FName_CCLocator)
except:
    print ("\n Unable to rebuild ADDR_FNAME_INTRA Locator from Address_Points - CRAW_INTERNAL")
    write_log("\n Unable to rebuild ADDR_FNAME_INTRA Locator from Address_Points - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild ADDR_FNAME_INTRA Locator from Address_Points - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding ADDR_FNAME_INTRA Locator from Address_Points - CRAW_INTERNAL completed")
write_log("       Rebuilding ADDR_FNAME_INTRA Locator from Address_Points - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding ADDR_OldAdd_INTRA from Address_Points - CRAW_INTERNAL")
write_log("\n Rebuilding ADDR_OldAdd_INTRA from Address_Points - CRAW_INTERNAL", logfile)

try:
    # ADDR_OldAdd_INTRA locator from Address_Points - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(ADDR_OldAdd_CCLocator)
except:
    print ("\n Unable to rebuild ADDR_OldAdd_INTRA locator from Address_Points - CRAW_INTERNAL")
    write_log("\n Unable to rebuild ADDR_OldAdd_INTRA locator from Address_Points - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild ADDR_OldAdd_INTRA locator from Address_Points - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding ADDR_OldAdd_INTRA locator from Address_Points - CRAW_INTERNAL completed")
write_log("       Rebuilding ADDR_OldAdd_INTRA locator from Address_Points - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding CL_Name_INTRA Locator from Street Centerline - CRAW_INTERNAL")
write_log("\n Rebuilding CL_Name_INTRA Locator from Street Centerline - CRAW_INTERNAL", logfile)

try:
    # CC_Roads_Locator_INTRA Locator from Street Centerline - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(CC_Roads_Locator)
except:
    print ("\n Unable to rebuild CC_Roads_Locator_INTRA Locator from Street Centerline - CRAW_INTERNAL")
    write_log("\n Unable to rebuild CC_Roads_Locator_INTRA Locator from Street Centerline - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild CC_Roads_Locator_INTRA Locator from Street Centerline - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding CC_Roads_Locator_INTRA Locator from Street Centerline - CRAW_INTERNAL completed")
write_log("       Rebuilding CC_Roads_Locator_INTRA Locator from Street Centerline - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding TaxParcel_ADDR1_INTRA Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding TaxParcel_ADDR1_INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # Rebuild TaxParcel_ADDR1_INTRA Locator from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_ADDR1_CCLocator)
except:
    print ("\n Unable to rebuild TaxParcel_ADDR1_INTRA Locator from Tax Parcels - CRAW_INTERNAL")
    write_log("\n Unable to rebuild TaxParcel_ADDR1_INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild TaxParcel_ADDR1_INTRA Locator from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_ADDR1_INTRA Locator from Tax Parcels - CRAW_INTERNAL completed")
write_log("       Rebuilding TaxParcel_ADDR1_INTRA Locator from Tax Parcels-  CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding TaxParcel_ADDR2_INTRA Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding TaxParcel_ADDR2_INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # Rebuild TaxParcel_ADDR2_INTRA Locator from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_ADDR2_CCLocator)
except:
    print ("\n Unable to rebuild TaxParcel_ADDR2_INTRA Locator from Tax Parcel s- CRAW_INTERNAL")
    write_log("\n Unable to rebuild TaxParcel_ADDR2_INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild TaxParcel_ADDR2_INTRA Locator from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_ADDR2_INTRA Locator from Tax Parcels - CRAW_INTERNAL completed")
write_log("       Rebuilding TaxParcel_ADDR2_INTRA Locator from Tax Parcels - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding TaxParcel_ADDR3_INTRA Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding TaxParcel_ADDR3_INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # Rebuild TaxParcel_ADDR3_INTRA Locator from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_ADDR3_CCLocator)
except:
    print ("\n Unable to rebuild TaxParcel_ADDR3_INTRA Locator from Tax Parcel s- CRAW_INTERNAL")
    write_log("\n Unable to rebuild TaxParcel_ADDR3_INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild TaxParcel_ADDR3_INTRA Locator from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_ADDR3_INTRA Locator from Tax Parcels - CRAW_INTERNAL completed")
write_log("       Rebuilding TaxParcel_ADDR3_INTRA Locator from Tax Parcels - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding TaxParcel_CAMA_INTRA Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding TaxParcel_CAMA_INTRA from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # Rebuild TaxParcel_CAMA_INTRA Locator from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_CAMA_CCLocator)
except:
    print ("\n Unable to rebuild TaxParcel_CAMA_INTRA Locator from Tax Parcels - CRAW_INTERNAL")
    write_log("Unable to rebuild TaxParcel_CAMA_INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild TaxParcel_CAMA_INTRA Locator from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_ADDR2_INTRA Locator from Tax Parcels- CRAW_INTERNAL completed")
write_log("       Rebuilding TaxParcel_ADDR2_INTRA Locator from Tax Parcels- CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding TaxParcel_Name_INTRA Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding TaxParcel_Name_INTRA from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # Rebuild TaxParcel_Name_INTRA from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_Name_CCLocator)
except:
    print ("\n Unable to rebuild TaxParcel_Name_INTRA from Tax Parcels - CRAW_INTERNAL")
    write_log("\n Unable to rebuild TaxParcel_Name_INTRA from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild TaxParcel_Name_INTRA from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_Name_INTRA from Tax Parcels - CRAW_INTERNAL completed")
write_log("       Rebuilding TaxParcel_Name_INTRA from Tax Parcels - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding TaxParcel_PID_INTRA Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding TaxParcel_PID_INTRA from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # Rebuild TaxParcel_PID_INTRA from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_PID_CCLocator)
except:
    print ("\n Unable to rebuild TaxParcel_PID_INTRA from Tax Parcels - CRAW_INTERNAL")
    write_log("\n Unable to rebuild TaxParcel_PID_INTRA from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild TaxParcel_PID_INTRA from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_Name_INTRA from Tax Parcels - CRAW_INTERNAL completed")
write_log("       Rebuilding TaxParcel_Name_INTRA from Tax Parcels - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding TaxParcel_UPI_INTRA Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding TaxParcel_UPI_INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # TaxParcel_UPI_INTRA Locator from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_UPI_CCLocator)
except:
    print ("\n Unable to rebuild TaxParcel_UPI_INTRA Locator from Tax Parcels - CRAW_INTERNAL")
    write_log("\n Unable to rebuild TaxParcel_UPI_INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild TaxParcel_UPI_INTRA Locator from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_UPI_INTRA Locator from Tax Parcels - CRAW_INTERNAL completed")
write_log("       Rebuilding TaxParcel_UPI_INTRA Locator from Tax Parcels - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding TaxParcel_Control Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding TaxParcel_Control Locator from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # TaxParcel_Control Locator from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_Control_CCLocator)
except:
    print ("\n Unable to rebuild TaxParcel_Control Locator from Tax Parcels - CRAW_INTERNAL")
    write_log("\n Unable to rebuild TaxParcel_Control Locator from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild TaxParcel_Control Locator from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TaxParcel_Control Locator from Tax Parcels - CRAW_INTERNAL completed")
write_log("       Rebuilding TaxParcel_Control Locator from Tax Parcels - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding Tax Parcel ALTPRCLID INTRA Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding Tax Parcel ALTPRCLID INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # Rebuild Tax Parcel ALTPRCLID INTRA Locator from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(TaxParcel_ALTPRCLID_CCLocator)
except:
    print ("\n Unable to rebuild Tax Parcel ALTPRCLID INTRA Locator from Tax Parcels - CRAW_INTERNAL")
    write_log("\n Unable to rebuild Tax Parcel ALTPRCLID INTRA Locator from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild Tax Parcel ALTPRCLID INTRA Locator from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding Tax Parcel ALTPRCLID INTRA Locator from Tax Parcels - CRAW_INTERNAL completed")
write_log("       Rebuilding Tax Parcel ALTPRCLID INTRA Locator from Tax Parcels - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding BuildingOnly_Control_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
write_log("\n Rebuilding BuildingOnly_Control_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)

try:
    # BuildingOnly_ADDR1_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_Control_CCLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_Control_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
    write_log("\n Unable to rebuild BuildingOnly_Control_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_Control_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_Control_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed")
write_log("       Rebuilding BuildingOnly_Control_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding BuildingOnly_ADDR1_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
write_log("\n Rebuilding BuildingOnly_ADDR1_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)

try:
    # BuildingOnly_ADDR1_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_ADDR1_CCLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_ADDR1_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
    write_log("\n Unable to rebuild BuildingOnly_ADDR1_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_ADDR1_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_ADDR1_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed")
write_log("       Rebuilding BuildingOnly_ADDR1_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding BuildingOnly_ADDR2_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
write_log("\n Rebuilding BuildingOnly_ADDR2_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)

try:
    # BuildingOnly_ADDR2_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_ADDR2_CCLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_ADDR2_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
    write_log("\n Unable to rebuild BuildingOnly_ADDR2_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_ADDR2_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_ADDR2_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed")
write_log("       Rebuilding BuildingOnly_ADDR2_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding BuildingOnly_ADDR3_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
write_log("\n Rebuilding BuildingOnly_ADDR3_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)

try:
    # BuildingOnly_ADDR2_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_ADDR3_CCLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_ADDR3_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
    write_log("\n Unable to rebuild BuildingOnly_ADDR3_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_ADDR3_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_ADDR3_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed")
write_log("       Rebuilding BuildingOnly_ADDR3_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding BuildingOnly_Name_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
write_log("\n Rebuilding BuildingOnly_Name_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)

try:
    # BuildingOnly_Name_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_Name_CCLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_Name_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
    write_log("\n Unable to rebuild BuildingOnly_Name_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_Name_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_Name_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed")
write_log("       Rebuilding BuildingOnly_Name_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding BuildingOnly_PID_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
write_log("\n Rebuilding BuildingOnly_PID_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)

try:
    # BuildingOnly_PID_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_PID_CCLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_PID_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
    write_log("\n Unable to rebuild BuildingOnly_PID_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_PID_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_PID_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed")
write_log("       Rebuilding BuildingOnly_PID_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding BuildingOnly_UPI_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
write_log("\n Rebuilding BuildingOnly_UPI_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)

try:
    # BuildingOnly_UPI_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(BuildingOnly_UPI_CCLocator)
except:
    print ("\n Unable to rebuild BuildingOnly_UPI_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL")
    write_log("\n Unable to rebuild BuildingOnly_UPI_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild BuildingOnly_UPI_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BuildingOnly_UPI_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed")
write_log("       Rebuilding BuildingOnly_UPI_INTRA Locator from Building/Trailer Only - CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding TAX_PARCELS_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding TAX_PARCELS_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # Rebuild TAX_PARCELS_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(TAX_PARCELS_PID_AUTO)
except:
    print ("\n Unable to rebuild TAX_PARCELS_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL")
    write_log("\n Unable to rebuild TAX_PARCELS_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild TAX_PARCELS_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding TAX_PARCELS_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL completed")
write_log("       Rebuilding TAX_PARCELS_PID_AUTOMATION Locator from Tax Parcels-  CRAW_INTERNAL completed", logfile)

print ("\n Rebuilding BUILDINGONLY_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL")
write_log("\n Rebuilding BUILDINGONLY_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL", logfile)

try:
    # Rebuild BUILDINGONLY_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL
    arcpy.RebuildAddressLocator_geocoding(BUILDINGONLY_PID_AUTO)
except:
    print ("\n Unable to rebuild BUILDINGONLY_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL")
    write_log("\n Unable to rebuild BUILDINGONLY_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on rebuild BUILDINGONLY_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding BUILDINGONLY_PID_AUTOMATION Locator from Tax Parcels - CRAW_INTERNAL completed")
write_log("       Rebuilding BUILDINGONLY_PID_AUTOMATION Locator from Tax Parcels-  CRAW_INTERNAL completed", logfile)

print ("\n Rebuild Composite Intranet Locators from individual locators")
print ("==================================================================")

write_log("\n Rebuild Composite Intranet Locators from individual locators", logfile)
write_log("==================================================================", logfile)

print ("\n Rebuilding CC Address Search Locator from individual locators")
write_log("\n Rebuilding CC Address Search Locator from individual locators", logfile)

try:
    # Rebuild CC Address Search Locator from individual locators
    arcpy.RebuildAddressLocator_geocoding(CC_Address_Search)
except:
    print ("\n Unable to rebuild CC Address Search Locator from individual locators")
    write_log("Unable to rebuild CC Address Search Locator from individual locators", logfile)
    logging.exception('Got exception on rebuild CC Address Search Locator from individual locators logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding CC Address Search Locator from individual locators completed")
write_log("       Rebuilding CC Address Search Locator from individual locators completed", logfile)

print ("\n Rebuilding CC Name Locator from individual locators")
write_log("\n Rebuilding CC Name Locator from individual locators", logfile)

try:
    # Rebuild CC Name Locator from individual locators
    arcpy.RebuildAddressLocator_geocoding(CC_Name_Locator)
except:
    print ("\n Unable to rebuild CC Name Locator from individual locators")
    write_log("\n Unable to rebuild CC Name Locator from individual locators", logfile)
    logging.exception('Got exception on rebuild CC Name Locator from individual locators logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding CC Name Locator from individual locators completed")
write_log("       Rebuilding CC Name Locator from individual locators completed", logfile)

print ("\n Rebuilding CC Parcel Locator from individual locators")
write_log("\n Rebuilding CC Parcel Locator from individual locators", logfile)

try:
    # Rebuild CC Parcel Locator from individual locators
    arcpy.RebuildAddressLocator_geocoding(CC_Parcel_Locator)
except:
    print ("\n Unable to rebuild CC Parcel Locator Locator from individual locators")
    write_log("Unable to rebuild CC Parcel Locator Locator from individual locators", logfile)
    logging.exception('Got exception on rebuild CC Parcel Locator Locator from individual locators logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Rebuilding CC Parcel Locator Locator from individual locators completed")
write_log("       Rebuilding CC Parcel Locator Locator from individual locators completed", logfile)


##print ("\n Publishing Intranet Locators Services")
##write_log("\n Publishing Intranet Locators Services", logfile)
##print ("===========================================")
##write_log("===========================================", logfile)
##
##print ("\n Publishing (overwrite existing) CC Address Search service")
##write_log("\n Publishing (overwrite existing) CC Address Search service", logfile)
##
##try:
##    # Overwrite any existing outputs
##    arcpy.env.overwriteOutput = True
##except:
##    print ("Unable to overwrite existing outputs")
##    write_log("Unable to overwrite existing outputs", logfile)
##
##try:
##    # Create the sd draft file
##    analyze_messages = arcpy.CreateGeocodeSDDraft(CCADD_locator_path, CCADD_sddraft_file, CCADD_service_name,
##                                                  connection_file_path=gis_server_connection_file,
##                                                  copy_data_to_server=True,
##                                                  summary=CCADD_summary, tags=CCADD_tags, max_result_size=20,
##                                                  max_batch_size=500, suggested_batch_size=150,
##                                                  overwrite_existing_service=True)
##
##except:
##    print ("Unable to create the CC Address Search SD draft file")
##    write_log("Unable to create the CC Address Search SD draft file", logfile)
##
### Stage and upload the service if the sddraft analysis did not contain errors
##if analyze_messages['errors'] == {}:
##    try:
##        # Execute StageService to convert sddraft file to a service definition 
##        # (sd) file 
##        arcpy.server.StageService(CCADD_sddraft_file, CCADD_sd_file)
##
##        # Execute UploadServiceDefinition to publish the service definition 
##        # file as a service
##        arcpy.server.UploadServiceDefinition(CCADD_sd_file, gis_server_connection_file)
##        print("     The CC Address Search geocode service was successfully published")
##        write_log("     The CC Address Search geocode service was successfully published", logfile)
##    except arcpy.ExecuteError:
##        print("An error occurred")
##        print(arcpy.GetMessages(2))
##        write_log("Unable to publish CC Address Search geocode service", logfile)
##        write_log(arcpy.GetMessages(2),logfile)
##        logging.exception('Got exception on Unable to publish CC Address Search geocode service logged at:' + str(Day) + " " + str(Time))
##        raise
##else: 
##    # If the sddraft analysis contained errors, display them
##    print("Errors were returned when creating CC Address Search geocode service definition draft")
##    write_log("Errors were returned when creating CC Address Search geocode service definition draft", logfile)
##    pprint.pprint(analyze_messages['errors'], indent=2)
##
##print ("\n Publishing (overwrite existing) CC Name Locator service")
##write_log("\n Publishing (overwrite existing) CC Name Locator service", logfile)
##
##try:
##    # Overwrite any existing outputs
##    arcpy.env.overwriteOutput = True
##except:
##    print ("Unable to overwrite existing outputs")
##    write_log("Unable to overwrite existing outputs", logfile)
##
##try:
##    # Create the sd draft file
##    analyze_messages = arcpy.CreateGeocodeSDDraft(CCNAME_locator_path, CCNAME_sddraft_file, CCNAME_service_name,
##                            connection_file_path=gis_server_connection_file, 
##                            copy_data_to_server=True,
##                            summary=CCNAME_summary, tags=CCNAME_tags, max_result_size=20,
##                            max_batch_size=500, suggested_batch_size=150, 
##                            overwrite_existing_service=True)
##
##except:
##    print ("Unable to create the CC Name Locator SD draft file")
##    write_log("Unable to create the CC Name Locator SD draft file", logfile)
##
### Stage and upload the service if the sddraft analysis did not contain errors
##if analyze_messages['errors'] == {}:
##    try:
##        # Execute StageService to convert sddraft file to a service definition 
##        # (sd) file 
##        arcpy.server.StageService(CCNAME_sddraft_file, CCNAME_sd_file)
##
##        # Execute UploadServiceDefinition to publish the service definition 
##        # file as a service
##        arcpy.server.UploadServiceDefinition(CCNAME_sd_file, gis_server_connection_file)
##        print("     The CC Name search geocode service was successfully published")
##        write_log("     The CC Name Search geocode service was successfully published", logfile)
##    except arcpy.ExecuteError:
##        print("An error occurred")
##        write_log("Errors were returned when creating CC Name Search geocode service definition draft", logfile)
##        print(arcpy.GetMessages(2))
##        write_log(arcpy.GetMessages(2),logfile)
##else: 
##    # If the sddraft analysis contained errors, display them
##    print("Errors were returned when creating CC Name Search geocode service definition draft")
##    write_log("Errors were returned when creating CC Name Search geocode service definition draft", logfile)
##    pprint.pprint(analyze_messages['errors'], indent=2)
##
##print ("\n Publishing (overwrite existing) CC Parcel Locator service")
##write_log("\n Publishing (overwrite existing) CC Parcel Locator service", logfile)
##
##try:
##    # Overwrite any existing outputs
##    arcpy.env.overwriteOutput = True
##except:
##    print ("Unable to overwrite existing outputs")
##    write_log("Unable to overwrite existing outputs", logfile)
##
##try:
##    # Create the sd draft file
##    analyze_messages = arcpy.CreateGeocodeSDDraft(CCPARCEL_locator_path, CCPARCEL_sddraft_file, CCPARCEL_service_name,
##                            connection_file_path=gis_server_connection_file, 
##                            copy_data_to_server=True,
##                            summary=CCPARCEL_summary, tags=CCPARCEL_tags, max_result_size=20,
##                            max_batch_size=500, suggested_batch_size=150, 
##                            overwrite_existing_service=True)
##
##except:
##    print ("Unable to create the CC Parcel Locator SD draft file")
##    write_log("Unable to create the CC Parcel Locator SD draft file", logfile)
##
### Stage and upload the service if the sddraft analysis did not contain errors
##if analyze_messages['errors'] == {}:
##    try:
##        # Execute StageService to convert sddraft file to a service definition 
##        # (sd) file 
##        arcpy.server.StageService(CCPARCEL_sddraft_file, CCPARCEL_sd_file)
##
##        # Execute UploadServiceDefinition to publish the service definition 
##        # file as a service
##        arcpy.server.UploadServiceDefinition(CCPARCEL_sd_file, gis_server_connection_file)
##        print("     The CC Parcel search geocode service was successfully published")
##        write_log("     The CC Parcel Search geocode service was successfully published", logfile)
##    except arcpy.ExecuteError:
##        print("An error occurred")
##        print(arcpy.GetMessages(2))
##        write_log(arcpy.GetMessages(2),logfile)
##else: 
##    # If the sddraft analysis contained errors, display them
##    print("Errors were returned when creating CC Parcel Search geocode service definition draft")
##    write_log("Errors were returned when creating CC Parcel Search geocode service definition draft", logfile)
##    pprint.pprint(analyze_messages['errors'], indent=2)
##
##print ("\n Publishing (overwrite existing) CC Roads Locator service")
##write_log("\n Publishing (overwrite existing) CC Roads Locator service", logfile)
##
##try:
##    # Overwrite any existing outputs
##    arcpy.env.overwriteOutput = True
##except:
##    print ("Unable to overwrite existing outputs")
##    write_log("Unable to overwrite existing outputs", logfile)
##
##try:
##    # Create the sd draft file
##    analyze_messages = arcpy.CreateGeocodeSDDraft(CCROAD_locator_path, CCROAD_sddraft_file, CCROAD_service_name,
##                            connection_file_path=gis_server_connection_file, 
##                            copy_data_to_server=True,
##                            summary=CCROAD_summary, tags=CCROAD_tags, max_result_size=20,
##                            max_batch_size=500, suggested_batch_size=150, 
##                            overwrite_existing_service=True)
##
##except:
##    print ("Unable to create the CC Roads Locator SD draft file")
##    write_log("Unable to create the CC Roads Locator SD draft file", logfile)
##
### Stage and upload the service if the sddraft analysis did not contain errors
##if analyze_messages['errors'] == {}:
##    try:
##        # Execute StageService to convert sddraft file to a service definition 
##        # (sd) file 
##        arcpy.server.StageService(CCROAD_sddraft_file, CCROAD_sd_file)
##
##        # Execute UploadServiceDefinition to publish the service definition 
##        # file as a service
##        arcpy.server.UploadServiceDefinition(CCROAD_sd_file, gis_server_connection_file)
##        print("     The CC Roads search geocode service was successfully published")
##        write_log("     The CC Roads Search geocode service was successfully published", logfile)
##    except arcpy.ExecuteError:
##        print("An error occurred")
##        print(arcpy.GetMessages(2))
##        write_log(arcpy.GetMessages(2),logfile)
##else: 
##    # If the sddraft analysis contained errors, display them
##    print("Errors were returned when creating CC Roads Search geocode service definition draft")
##    write_log("Errors were returned when creating CC Roads Search geocode service definition draft", logfile)
##    pprint.pprint(analyze_messages['errors'], indent=2)
##
##print ("\n Publishing Public Locators Services")
##write_log("\n Publishing Public Locators Services", logfile)
##print ("=======================================")
##write_log("=======================================", logfile)
##
##print ("\n Publishing (overwrite existing) Crawford Address Search service")
##write_log("\n Publishing (overwrite existing) Crawford Address Search service", logfile)
##
##try:
##    # Overwrite any existing outputs
##    arcpy.env.overwriteOutput = True
##except:
##    print ("Unable to overwrite existing outputs")
##    write_log("Unable to overwrite existing outputs", logfile)
##
##try:
##    # Create the sd draft file
##    analyze_messages = arcpy.CreateGeocodeSDDraft(CRAWADD_locator_path, CRAWADD_sddraft_file, CRAWADD_service_name,
##                            connection_file_path=gis_server_connection_file, 
##                            copy_data_to_server=True,
##                            summary=CRAWADD_summary, tags=CRAWADD_tags, max_result_size=20,
##                            max_batch_size=500, suggested_batch_size=150, 
##                            overwrite_existing_service=True)
##except:
##    print ("Unable to create the Crawford Address Search SD draft file")
##    write_log("Unable to create the Crawford Address Search SD draft file", logfile)
##
### Stage and upload the service if the sddraft analysis did not contain errors
##if analyze_messages['errors'] == {}:
##    try:
##        # Execute StageService to convert sddraft file to a service definition 
##        # (sd) file 
##        arcpy.server.StageService(CRAWADD_sddraft_file, CRAWADD_sd_file)
##
##        # Execute UploadServiceDefinition to publish the service definition 
##        # file as a service
##        arcpy.server.UploadServiceDefinition(CRAWADD_sd_file, gis_server_connection_file)
##        print("     The Crawford Address search geocode service was successfully published")
##        write_log("     The Crawford Address Search geocode service was successfully published", logfile)
##    except arcpy.ExecuteError:
##        print("An error occurred")
##        print(arcpy.GetMessages(2))
##        write_log(arcpy.GetMessages(2),logfile)
##else: 
##    # If the sddraft analysis contained errors, display them
##    print("Errors were returned when creating Crawford Address Search geocode service definition draft")
##    write_log("Errors were returned when creating Crawford Address Search geocode service definition draft", logfile)
##    pprint.pprint(analyze_messages['errors'], indent=2)
##
##print ("\n Publishing (overwrite existing) Crawford Cemetery Locator service")
##write_log("\n Publishing (overwrite existing) Crawford Cemetery Locator service", logfile)
##
##try:
##    # Overwrite any existing outputs
##    arcpy.env.overwriteOutput = True
##except:
##    print ("Unable to overwrite existing outputs")
##    write_log("Unable to overwrite existing outputs", logfile)
##
##try:
##    # Create the sd draft file
##    analyze_messages = arcpy.CreateGeocodeSDDraft(CRAWCEM_locator_path, CRAWCEM_sddraft_file, CRAWCEM_service_name,
##                            connection_file_path=gis_server_connection_file, 
##                            copy_data_to_server=True,
##                            summary=CRAWCEM_summary, tags=CRAWCEM_tags, max_result_size=20,
##                            max_batch_size=500, suggested_batch_size=150, 
##                            overwrite_existing_service=True)
##
##except:
##    print ("Unable to create the Crawford Cemetery Locator SD draft file")
##    write_log("Unable to create the Crawford Cemetery Locator SD draft file", logfile)
##
### Stage and upload the service if the sddraft analysis did not contain errors
##if analyze_messages['errors'] == {}:
##    try:
##        # Execute StageService to convert sddraft file to a service definition 
##        # (sd) file 
##        arcpy.server.StageService(CRAWCEM_sddraft_file, CRAWCEM_sd_file)
##
##        # Execute UploadServiceDefinition to publish the service definition 
##        # file as a service
##        arcpy.server.UploadServiceDefinition(CRAWCEM_sd_file, gis_server_connection_file)
##        print("     The Crawford Cemetery search geocode service was successfully published")
##        write_log("     The Crawford Cemetery Search geocode service was successfully published", logfile)
##    except arcpy.ExecuteError:
##        print("An error occurred")
##        print(arcpy.GetMessages(2))
##        write_log(arcpy.GetMessages(2),logfile)
##else: 
##    # If the sddraft analysis contained errors, display them
##    print("Errors were returned when creating Crawford Cemetery Search geocode service definition draft")
##    write_log("Errors were returned when creating Crawford Cemetery Search geocode service definition draft", logfile)
##    pprint.pprint(analyze_messages['errors'], indent=2)
##
##print ("\n Publishing (overwrite existing) Crawford Landmarks Locator service")
##write_log("\n Publishing (overwrite existing) Crawford Landmarks Locator service", logfile)
##
##try:
##    # Overwrite any existing outputs
##    arcpy.env.overwriteOutput = True
##except:
##    print ("Unable to overwrite existing outputs")
##    write_log("Unable to overwrite existing outputs", logfile)
##
##try:
##    # Create the sd draft file
##    analyze_messages = arcpy.CreateGeocodeSDDraft(CRAWLMKS_locator_path, CRAWLMKS_sddraft_file, CRAWLMKS_service_name,
##                            connection_file_path=gis_server_connection_file, 
##                            copy_data_to_server=True,
##                            summary=CRAWLMKS_summary, tags=CRAWLMKS_tags, max_result_size=20,
##                            max_batch_size=500, suggested_batch_size=150, 
##                            overwrite_existing_service=True)
##
##except:
##    print ("Unable to create the Crawford Landmarks Locator SD draft file")
##    write_log("Unable to create the Crawford Landmarks Locator SD draft file", logfile)
##
### Stage and upload the service if the sddraft analysis did not contain errors
##if analyze_messages['errors'] == {}:
##    try:
##        # Execute StageService to convert sddraft file to a service definition 
##        # (sd) file 
##        arcpy.server.StageService(CRAWLMKS_sddraft_file, CRAWLMKS_sd_file)
##
##        # Execute UploadServiceDefinition to publish the service definition 
##        # file as a service
##        arcpy.server.UploadServiceDefinition(CRAWLMKS_sd_file, gis_server_connection_file)
##        print("     The Crawford Landmarks search geocode service was successfully published")
##        write_log("     The Crawford Landmarks Search geocode service was successfully published", logfile)
##    except arcpy.ExecuteError:
##        print("An error occurred")
##        print(arcpy.GetMessages(2))
##        write_log(arcpy.GetMessages(2),logfile)
##else: 
##    # If the sddraft analysis contained errors, display them
##    print("Errors were returned when creating Crawford Landmarks Search geocode service definition draft")
##    write_log("Errors were returned when creating Crawford Landmarks Search geocode service definition draft", logfile)
##    pprint.pprint(analyze_messages['errors'], indent=2)
##
##print ("\n Publishing (overwrite existing) Crawford Name Locator service")
##write_log("\n Publishing (overwrite existing) Crawford Name Locator service", logfile)
##
##try:
##    # Overwrite any existing outputs
##    arcpy.env.overwriteOutput = True
##except:
##    print ("Unable to overwrite existing outputs")
##    write_log("Unable to overwrite existing outputs", logfile)
##
##try:
##    # Create the sd draft file
##    analyze_messages = arcpy.CreateGeocodeSDDraft(CRAWNAME_locator_path, CRAWNAME_sddraft_file, CRAWNAME_service_name,
##                            connection_file_path=gis_server_connection_file, 
##                            copy_data_to_server=True,
##                            summary=CRAWNAME_summary, tags=CRAWNAME_tags, max_result_size=20,
##                            max_batch_size=500, suggested_batch_size=150, 
##                            overwrite_existing_service=True)
##
##except:
##    print ("Unable to create the Crawford Name Locator SD draft file")
##    write_log("Unable to create the Crawford Name Locator SD draft file", logfile)
##
### Stage and upload the service if the sddraft analysis did not contain errors
##if analyze_messages['errors'] == {}:
##    try:
##        # Execute StageService to convert sddraft file to a service definition 
##        # (sd) file 
##        arcpy.server.StageService(CRAWNAME_sddraft_file, CRAWNAME_sd_file)
##
##        # Execute UploadServiceDefinition to publish the service definition 
##        # file as a service
##        arcpy.server.UploadServiceDefinition(CRAWNAME_sd_file, gis_server_connection_file)
##        print("     The Crawford Name search geocode service was successfully published")
##        write_log("     The Crawford Name Search geocode service was successfully published", logfile)
##    except arcpy.ExecuteError:
##        print("An error occurred")
##        print(arcpy.GetMessages(2))
##        write_log(arcpy.GetMessages(2),logfile)
##else: 
##    # If the sddraft analysis contained errors, display them
##    print("Errors were returned when creating Crawford Name Search geocode service definition draft")
##    write_log("Errors were returned when creating Crawford Name Search geocode service definition draft", logfile)
##    pprint.pprint(analyze_messages['errors'], indent=2)
##
##print ("\n Publishing (overwrite existing) Crawford Parcel Locator service")
##write_log("\n Publishing (overwrite existing) Crawford Parcel Locator service", logfile)
##
##try:
##    # Overwrite any existing outputs
##    arcpy.env.overwriteOutput = True
##except:
##    print ("Unable to overwrite existing outputs")
##    write_log("Unable to overwrite existing outputs", logfile)
##
##try:
##    # Create the sd draft file
##    analyze_messages = arcpy.CreateGeocodeSDDraft(CRAWPCL_locator_path, CRAWPCL_sddraft_file, CRAWPCL_service_name,
##                            connection_file_path=gis_server_connection_file, 
##                            copy_data_to_server=True,
##                            summary=CRAWPCL_summary, tags=CRAWPCL_tags, max_result_size=20,
##                            max_batch_size=500, suggested_batch_size=150, 
##                            overwrite_existing_service=True)
##
##except:
##    print ("Unable to create the Crawford Parcel Locator SD draft file")
##    write_log("Unable to create the Crawford Parcel Locator SD draft file", logfile)
##
### Stage and upload the service if the sddraft analysis did not contain errors
##if analyze_messages['errors'] == {}:
##    try:
##        # Execute StageService to convert sddraft file to a service definition 
##        # (sd) file 
##        arcpy.server.StageService(CRAWPCL_sddraft_file, CRAWPCL_sd_file)
##
##        # Execute UploadServiceDefinition to publish the service definition 
##        # file as a service
##        arcpy.server.UploadServiceDefinition(CRAWPCL_sd_file, gis_server_connection_file)
##        print("     The Crawford Parcel search geocode service was successfully published")
##        write_log("     The Crawford Parcel Search geocode service was successfully published", logfile)
##    except arcpy.ExecuteError:
##        print("An error occurred")
##        print(arcpy.GetMessages(2))
##        write_log(arcpy.GetMessages(2),logfile)
##else: 
##    # If the sddraft analysis contained errors, display them
##    print("Errors were returned when creating Crawford Parcel Search geocode service definition draft")
##    write_log("Errors were returned when creating Crawford Parcel Search geocode service definition draft", logfile)
##    pprint.pprint(analyze_messages['errors'], indent=2)
##
##print ("\n Publishing (overwrite existing) Crawford Roads Locator service")
##write_log("\n Publishing (overwrite existing) Crawford Roads Locator service", logfile)
##
##try:
##    # Overwrite any existing outputs
##    arcpy.env.overwriteOutput = True
##except:
##    print ("Unable to overwrite existing outputs")
##    write_log("Unable to overwrite existing outputs", logfile)
##
##try:
##    # Create the sd draft file
##    analyze_messages = arcpy.CreateGeocodeSDDraft(CRAWROAD_locator_path, CRAWROAD_sddraft_file, CRAWROAD_service_name,
##                           connection_file_path=gis_server_connection_file, 
##                           copy_data_to_server=True,
##                           summary=CRAWROAD_summary, tags=CRAWROAD_tags, max_result_size=20,
##                           max_batch_size=500, suggested_batch_size=150, 
##                           overwrite_existing_service=True)
##except:
##    print ("Unable to create the Crawford Roads Locator SD draft file")
##    write_log("Unable to create the Crawford Roads Locator SD draft file", logfile)
##
### Stage and upload the service if the sddraft analysis did not contain errors
##if analyze_messages['errors'] == {}:
##    try:
##        # Execute StageService to convert sddraft file to a service definition 
##        # (sd) file 
##        arcpy.server.StageService(CRAWROAD_sddraft_file, CRAWROAD_sd_file)
##
##        # Execute UploadServiceDefinition to publish the service definition 
##        # file as a service
##        arcpy.server.UploadServiceDefinition(CRAWROAD_sd_file, gis_server_connection_file)
##        print("     The Crawford Roads search geocode service was successfully published")
##        write_log("     The Crawford Roads Search geocode service was successfully published", logfile)
##    except arcpy.ExecuteError:
##        print("An error occurred")
##        print(arcpy.GetMessages(2))
##        write_log(arcpy.GetMessages(2),logfile)
##else: 
##    # If the sddraft analysis contained errors, display them
##    print("Errors were returned when creating Crawford Roads Search geocode service definition draft")
##    write_log("Errors were returned when creating Crawford Roads Search geocode service definition draft", logfile)
##    pprint.pprint(analyze_messages['errors'], indent=2)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("===========================================================")
print ("\n LOCATOR REBUILDS ARE COMPLETED AND PUBLISHED: " + str(Day) + " " + str(end_time))
write_log("ALL LOCATOR REBUILDS ARE COMPLETED AND PUBLISHED: " + str(Day) + " " + str(end_time), logfile)

print (time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
write_log("Elapsed time: " + str (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))), logfile)
print ("===========================================================")

write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
