# ---------------------------------------------------------------------------
# Active_TaxClaim_Missing_GIS.py
# Created on: 2022-01-21
# Updated on 2022-01-21
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
#
# Description: 
# Geocode the GSSCrawford.dbo.CollTaxSaleWeb, filter out unmatched records and export to R:\GIS\Assessment\Reports as excel file
#
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
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\Assessment\\Active_TaxClaim_Missing_GIS.log"  
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
ASMT_REPORT_WORKSPACE = r"\\FILELOCATION\\GIS\\Assessment\\Workspace"
AUTOWORKSPACE = Database_Connections + "\\auto_workspace@ccsde.sde"
ASMT_REPORT_FLDR = r"\\\FILELOCATION\\GIS\\Assessment\\Reports"
GSS_DB = Database_Connections + "\\GSS_Database.sde"
LOCATOR_WKSP = r"\\FILELOCATION\\GIS\\CurrentWebsites\\Locators\\Intranet_Locators"
ASMT_TEMP_FGDB = ASMT_REPORT_WORKSPACE + "\\Assessment_TCReport_TempFGDB.gdb"

# Local variables:
MISSING_GIS_REPORT = ASMT_REPORT_FLDR + "\\Active_TaxClaim_Missing_GIS.xls"
CC_PARCEL_LOC = LOCATOR_WKSP + "\\CAMA_PID_Locator"
TaxClaim_TBL = GSS_DB + "\\dtaGSSCrawford.dbo.CollTaxSaleWeb"
TaxClaim_TBL_GEOCODE = ASMT_TEMP_FGDB + "\\TaxClaim_TBL_GEOCODE"

# Local variables - tables:
VISION_REALMAST_TBL_SDE = AUTOWORKSPACE + "\\CCSDE.AUTO_WORKSPACE.VIS_REALMAST_TBL"

start_time = time.time()

print ("============================================================================")
print ("Creating Active Tax Claim records missing from GIS Report: "+ str(Day) + " " + str(Time))
print ("Located at: "+ASMT_REPORT_FLDR)
print ("Works in ArcGIS Pro")
print ("============================================================================")
write_log("============================================================================", logfile)
write_log("Creating Active Tax Claim records missing from GIS Report: "+ str(Day) + " " + str(Time), logfile)
write_log("Located at: "+ASMT_REPORT_FLDR, logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Deleting excel file & Geocoding all Tax Claim records")
write_log("\n Deleting excel file & Geocoding all Tax Claim records",logfile)

try:
    # Delete excel file so it can be replaced
    if arcpy.Exists(MISSING_GIS_REPORT):
        os.remove(MISSING_GIS_REPORT)
        print (MISSING_GIS_REPORT + " found - table deleted")
        write_log(MISSING_GIS_REPORT + " found - table deleted", logfile)
except:
    print ("\n Unable to delete "+MISSING_GIS_REPORT+", need to delete existing FGDB manually and/or close program locking the tables")
    write_log("\n Unable to delete "+MISSING_GIS_REPORT+", need to delete existing FGDB manually and/or close program locking the tables", logfile)
    logging.exception('Got exception on Unable to delete '+MISSING_GIS_REPORT+', need to delete existing FGDB manually and/or close program locking the tables logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Ensure ASMT_TEMP_FGDB doesn't exist, if so, delete it
    if arcpy.Exists(ASMT_TEMP_FGDB):
        arcpy.Delete_management(ASMT_TEMP_FGDB)
        print ("ASMT_TEMP_FGDB found - FGDB deleted")
        write_log("ASMT_TEMP_FGDB found - FGDB deleted", logfile)
except:
    print ("\n Unable to delete ASMT_TEMP_FGDB, need to delete existing FGDB manually and/or close program locking the FGDB")
    write_log("Unable to delete ASMT_TEMP_FGDB, need to delete existing FGDB manually and/or close program locking the FGDB", logfile)
    logging.exception('Got exception on delete ASMT_TEMP_FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Create new File GDB called Assessment_TCReport_TempFGDB.gdb (creating new temporary FGDB for each run, to avoid corruption)
    ASMT_TEMP_FGDB = arcpy.CreateFileGDB_management(ASMT_REPORT_WORKSPACE, "Assessment_TCReport_TempFGDB", "CURRENT")
except:
    print ("\n Unable to create new Assessment_GISReport_TempFGDB.gdb, need to close program locking the FGDB workspace")
    write_log("Unable to create new Assessment_GISReport_TempFGDB.gdb, need to close program locking the FGDB workspace", logfile)
    logging.exception('Got exception on create Assessment_GISReport_TempFGDB.gdb logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Copy GSS Tax Claim table to Assessment_TCReport_TempFGDB.gdb
    GSS_TaxClaim_Temp_Tbl = arcpy.conversion.TableToTable(TaxClaim_TBL, ASMT_TEMP_FGDB, "GSS_TaxClaim_Temp_Tbl", '', r'Certmail "Certmail" false false false 22 Text 0 0,First,#,'+TaxClaim_TBL+',Certmail,0,22;Salenum "Salenum" false false false 4 Long 0 10,First,#,'+TaxClaim_TBL+',Salenum,-1,-1;District "District" false false false 2 Text 0 0,First,#,'+TaxClaim_TBL+',District,0,2;Ward "Ward" false false false 1 Text 0 0,First,#,'+TaxClaim_TBL+',Ward,0,1;Control "Control" false false false 6 Text 0 0,First,#,'+TaxClaim_TBL+',Control,0,6;EtuxID "EtuxID" false false false 4 Long 0 10,First,#,'+TaxClaim_TBL+',EtuxID,-1,-1;Year "Year" false false false 4 Text 0 0,First,#,'+TaxClaim_TBL+',Year,0,4;SaleYear "SaleYear" false true false 4 Text 0 0,First,#,'+TaxClaim_TBL+',SaleYear,0,4;Map "Map" false true false 50 Text 0 0,First,#,'+TaxClaim_TBL+',Map,0,50;Map3 "Map3" false true false 4 Text 0 0,First,#,'+TaxClaim_TBL+',Map3,0,4;Map4 "Map4" false true false 3 Text 0 0,First,#,'+TaxClaim_TBL+',Map4,0,3;Map5 "Map5" false true false 5 Text 0 0,First,#,'+TaxClaim_TBL+',Map5,0,5;Name "Name" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',Name,0,75;CoOwner "CoOwner" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',CoOwner,0,75;CareOf "CareOf" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',CareOf,0,75;Addr1 "Addr1" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',Addr1,0,75;Addr2 "Addr2" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',Addr2,0,75;Addr3 "Addr3" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',Addr3,0,75;City "City" false true false 50 Text 0 0,First,#,'+TaxClaim_TBL+',City,0,50;State "State" false true false 2 Text 0 0,First,#,'+TaxClaim_TBL+',State,0,2;ZipCode "ZipCode" false true false 5 Text 0 0,First,#,'+TaxClaim_TBL+',ZipCode,0,5;ZipCode2 "ZipCode2" false true false 4 Text 0 0,First,#,'+TaxClaim_TBL+',ZipCode2,0,4;MastName "MastName" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',MastName,0,75;MastCoOwner "MastCoOwner" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',MastCoOwner,0,75;MastAddr1 "MastAddr1" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',MastAddr1,0,75;MastAddr2 "MastAddr2" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',MastAddr2,0,75;MastCity "MastCity" false true false 50 Text 0 0,First,#,'+TaxClaim_TBL+',MastCity,0,50;MastState "MastState" false true false 2 Text 0 0,First,#,'+TaxClaim_TBL+',MastState,0,2;MastZipCode "MastZipCode" false true false 5 Text 0 0,First,#,'+TaxClaim_TBL+',MastZipCode,0,5;MastZipCode2 "MastZipCode2" false true false 4 Text 0 0,First,#,'+TaxClaim_TBL+',MastZipCode2,0,4;BName "BName" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',BName,0,75;Acreage "Acreage" false true false 20 Text 0 0,First,#,'+TaxClaim_TBL+',Acreage,0,20;Landuse "Landuse" false true false 4 Text 0 0,First,#,'+TaxClaim_TBL+',Landuse,0,4;LDesc "LDesc" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',LDesc,0,75;Desc1 "Desc1" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',Desc1,0,75;Desc2 "Desc2" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',Desc2,0,75;Desc3 "Desc3" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',Desc3,0,75;SitusDesc "SitusDesc" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',SitusDesc,0,75;AssLand "AssLand" false true false 4 Long 0 10,First,#,'+TaxClaim_TBL+',AssLand,-1,-1;AssImpr "AssImpr" false true false 4 Long 0 10,First,#,'+TaxClaim_TBL+',AssImpr,-1,-1;MVLand "MVLand" false true false 4 Long 0 10,First,#,'+TaxClaim_TBL+',MVLand,-1,-1;MVImpr "MVImpr" false true false 4 Long 0 10,First,#,'+TaxClaim_TBL+',MVImpr,-1,-1;DeedRef "DeedRef" false true false 50 Text 0 0,First,#,'+TaxClaim_TBL+',DeedRef,0,50;DeedBook "DeedBook" false true false 9 Text 0 0,First,#,'+TaxClaim_TBL+',DeedBook,0,9;DeedPage "DeedPage" false true false 4 Text 0 0,First,#,'+TaxClaim_TBL+',DeedPage,0,4;Amount "Amount" false true false 8 Double 4 19,First,#,'+TaxClaim_TBL+',Amount,-1,-1;CurrentCounty "CurrentCounty" false true false 8 Double 4 19,First,#,'+TaxClaim_TBL+',CurrentCounty,-1,-1;CurrentTwp "CurrentTwp" false true false 8 Double 4 19,First,#,'+TaxClaim_TBL+',CurrentTwp,-1,-1;CurrentSchool "CurrentSchool" false true false 8 Double 4 19,First,#,'+TaxClaim_TBL+',CurrentSchool,-1,-1;CurrentFee "CurrentFee" false true false 8 Double 4 19,First,#,'+TaxClaim_TBL+',CurrentFee,-1,-1;Lien "Lien" false true false 8 Double 4 19,First,#,'+TaxClaim_TBL+',Lien,-1,-1;LienDesc "LienDesc" false true false 75 Text 0 0,First,#,'+TaxClaim_TBL+',LienDesc,0,75;SignedFor "SignedFor" false true false 1 Text 0 0,First,#,'+TaxClaim_TBL+',SignedFor,0,1;SheriffService "SheriffService" false true false 1 Text 0 0,First,#,'+TaxClaim_TBL+',SheriffService,0,1;PostFlag "PostFlag" false true false 1 Text 0 0,First,#,'+TaxClaim_TBL+',PostFlag,0,1;SentToPalmetto "SentToPalmetto" false true false 1 Text 0 0,First,#,'+TaxClaim_TBL+',SentToPalmetto,0,1;PalmettoIneligible "PalmettoIneligible" false true false 1 Text 0 0,First,#,'+TaxClaim_TBL+',PalmettoIneligible,0,1;SaleType "SaleType" false true false 1 Text 0 0,First,#,'+TaxClaim_TBL+',SaleType,0,1;CarrierRoute "CarrierRoute" false true false 4 Text 0 0,First,#,'+TaxClaim_TBL+',CarrierRoute,0,4;DeliveryPoint "DeliveryPoint" false true false 2 Text 0 0,First,#,'+TaxClaim_TBL+',DeliveryPoint,0,2;CheckDigit "CheckDigit" false true false 1 Text 0 0,First,#,'+TaxClaim_TBL+',CheckDigit,0,1;Job "Job" false true false 2 Text 0 0,First,#,'+TaxClaim_TBL+',Job,0,2;Tray "Tray" false true false 5 Text 0 0,First,#,'+TaxClaim_TBL+',Tray,0,5;Package "Package" false true false 5 Text 0 0,First,#,'+TaxClaim_TBL+',Package,0,5;Sequence "Sequence" false true false 13 Text 0 0,First,#,'+TaxClaim_TBL+',Sequence,0,13;ZipCodeNumber "ZipCodeNumber" false true false 4 Long 0 10,First,#,'+TaxClaim_TBL+',ZipCodeNumber,-1,-1;ZipCodeNumber2 "ZipCodeNumber2" false true false 4 Long 0 10,First,#,'+TaxClaim_TBL+',ZipCodeNumber2,-1,-1;IMBNumeric "IMBNumeric" false true false 31 Text 0 0,First,#,'+TaxClaim_TBL+',IMBNumeric,0,31;IMBAlpha "IMBAlpha" false true false 65 Text 0 0,First,#,'+TaxClaim_TBL+',IMBAlpha,0,65', '')
except:
    print ("\n Unable to copy GSS Tax Claim table to Assessment_TCReport_TempFGDB.gdb")
    write_log("Unable to copy GSS Tax Claim table to Assessment_TCReport_TempFGDB.gdb", logfile)
    logging.exception('Got exception on copy GSS Tax Claim table to Assessment_TCReport_TempFGDB.gdb logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Add field to Assessment_TCReport_TempFGDB.gdb and calculate Control to PID (to drop leading zeros that interfere with geocoding)
    arcpy.management.AddField(GSS_TaxClaim_Temp_Tbl, "PID", "LONG", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')
    arcpy.management.CalculateField(GSS_TaxClaim_Temp_Tbl, "PID", "!Control!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
    print ("\n Added new field to Assessment_TCReport_TempFGDB.gdb and calculate Control to PID")
    write_log("\n Added new field to Assessment_TCReport_TempFGDB.gdb and calculate Control to PID",logfile)
except:
    print ("\n Unable to add field to Assessment_TCReport_TempFGDB.gdb and calculate Control to PID")
    write_log("Unable to add field to Assessment_TCReport_TempFGDB.gdb and calculate Control to PID", logfile)
    logging.exception('Got exception on add field to Assessment_TCReport_TempFGDB.gdb and calculate Control to PID logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Geocode GSS_TaxClaim_Temp_Tbl in ASMT_TEMP_FGDB against CC_PARCEL_Locator, into ASMT_TEMP_FGDB
    TaxClaim_TBL_GEOCODE = arcpy.geocoding.GeocodeAddresses(GSS_TaxClaim_Temp_Tbl, CC_PARCEL_LOC, "'Single Line Input' PID VISIBLE NONE", TaxClaim_TBL_GEOCODE, "STATIC", None, '', None, "ALL")
    print ("\n Geocoding REALMAST Table into ASMT_TEMP_FGDB")
    write_log ("\n Geocoding REALMAST Table into ASMT_TEMP_FGDB", logfile)
except:
    print ("\n Unable to Geocode GSS_TaxClaim_Temp_Tbl in ASMT_TEMP_FGDB against CC_PARCEL_Locator, into ASMT_TEMP_FGDB")
    write_log("\n Unable to Geocode GSS_TaxClaim_Temp_Tbl in ASMT_TEMP_FGDB against CC_PARCEL_Locator, into ASMT_TEMP_FGDB", logfile)
    logging.exception('Got exception on Geocode GSS_TaxClaim_Temp_Tbl in ASMT_TEMP_FGDB against CC_PARCEL_Locator, into ASMT_TEMP_FGDB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Make Feature Layer of MISSING_GIS_GEOCODE, selecting only unmatched records
    Unmatched_Geocoded_TaxClaim_Records = arcpy.management.MakeFeatureLayer(TaxClaim_TBL_GEOCODE, "Unmatched_Geocoded_TaxClaim_Records", "Status = 'U'", None, "ObjectID ObjectID HIDDEN NONE;Loc_name Loc_name HIDDEN NONE;Shape Shape HIDDEN NONE;Status Status VISIBLE NONE;Score Score HIDDEN NONE;Match_type Match_type HIDDEN NONE;Match_addr Match_addr HIDDEN NONE;LongLabel LongLabel HIDDEN NONE;ShortLabel ShortLabel HIDDEN NONE;Addr_type Addr_type HIDDEN NONE;Type Type HIDDEN NONE;PlaceName PlaceName HIDDEN NONE;Place_addr Place_addr HIDDEN NONE;Phone Phone HIDDEN NONE;URL URL HIDDEN NONE;Rank Rank HIDDEN NONE;AddBldg AddBldg HIDDEN NONE;AddNum AddNum HIDDEN NONE;AddNumFrom AddNumFrom HIDDEN NONE;AddNumTo AddNumTo HIDDEN NONE;AddRange AddRange HIDDEN NONE;Side Side HIDDEN NONE;StPreDir StPreDir HIDDEN NONE;StPreType StPreType HIDDEN NONE;StName StName HIDDEN NONE;StType StType HIDDEN NONE;StDir StDir HIDDEN NONE;BldgType BldgType HIDDEN NONE;BldgName BldgName HIDDEN NONE;LevelType LevelType HIDDEN NONE;LevelName LevelName HIDDEN NONE;UnitType UnitType HIDDEN NONE;UnitName UnitName HIDDEN NONE;SubAddr SubAddr HIDDEN NONE;StAddr StAddr HIDDEN NONE;Block Block HIDDEN NONE;Sector Sector HIDDEN NONE;Nbrhd Nbrhd HIDDEN NONE;District District HIDDEN NONE;City City HIDDEN NONE;MetroArea MetroArea HIDDEN NONE;Subregion Subregion HIDDEN NONE;Region Region HIDDEN NONE;RegionAbbr RegionAbbr HIDDEN NONE;Territory Territory HIDDEN NONE;Zone Zone HIDDEN NONE;Postal Postal HIDDEN NONE;PostalExt PostalExt HIDDEN NONE;Country Country HIDDEN NONE;LangCode LangCode HIDDEN NONE;Distance Distance HIDDEN NONE;X X HIDDEN NONE;Y Y HIDDEN NONE;DisplayX DisplayX HIDDEN NONE;DisplayY DisplayY HIDDEN NONE;Xmin Xmin HIDDEN NONE;Xmax Xmax HIDDEN NONE;Ymin Ymin HIDDEN NONE;Ymax Ymax HIDDEN NONE;ExInfo ExInfo HIDDEN NONE;IN_SingleLine IN_SingleLine HIDDEN NONE;USER_Certmail USER_Certmail HIDDEN NONE;USER_Salenum USER_Salenum HIDDEN NONE;USER_District USER_District HIDDEN NONE;USER_Ward USER_Ward HIDDEN NONE;USER_Control USER_Control VISIBLE NONE;USER_EtuxID USER_EtuxID HIDDEN NONE;USER_Year USER_Year HIDDEN NONE;USER_SaleYear USER_SaleYear HIDDEN NONE;USER_Map USER_Map HIDDEN NONE;USER_Map3 USER_Map3 HIDDEN NONE;USER_Map4 USER_Map4 HIDDEN NONE;USER_Map5 USER_Map5 HIDDEN NONE;USER_Name USER_Name HIDDEN NONE;USER_CoOwner USER_CoOwner HIDDEN NONE;USER_CareOf USER_CareOf HIDDEN NONE;USER_Addr1 USER_Addr1 HIDDEN NONE;USER_Addr2 USER_Addr2 HIDDEN NONE;USER_Addr3 USER_Addr3 HIDDEN NONE;USER_City USER_City HIDDEN NONE;USER_State USER_State HIDDEN NONE;USER_ZipCode USER_ZipCode HIDDEN NONE;USER_ZipCode2 USER_ZipCode2 HIDDEN NONE;USER_MastName USER_MastName HIDDEN NONE;USER_MastCoOwner USER_MastCoOwner HIDDEN NONE;USER_MastAddr1 USER_MastAddr1 HIDDEN NONE;USER_MastAddr2 USER_MastAddr2 HIDDEN NONE;USER_MastCity USER_MastCity HIDDEN NONE;USER_MastState USER_MastState HIDDEN NONE;USER_MastZipCode USER_MastZipCode HIDDEN NONE;USER_MastZipCode2 USER_MastZipCode2 HIDDEN NONE;USER_BName USER_BName HIDDEN NONE;USER_Acreage USER_Acreage HIDDEN NONE;USER_Landuse USER_Landuse HIDDEN NONE;USER_LDesc USER_LDesc HIDDEN NONE;USER_Desc1 USER_Desc1 HIDDEN NONE;USER_Desc2 USER_Desc2 HIDDEN NONE;USER_Desc3 USER_Desc3 HIDDEN NONE;USER_SitusDesc USER_SitusDesc HIDDEN NONE;USER_AssLand USER_AssLand HIDDEN NONE;USER_AssImpr USER_AssImpr HIDDEN NONE;USER_MVLand USER_MVLand HIDDEN NONE;USER_MVImpr USER_MVImpr HIDDEN NONE;USER_DeedRef USER_DeedRef HIDDEN NONE;USER_DeedBook USER_DeedBook HIDDEN NONE;USER_DeedPage USER_DeedPage HIDDEN NONE;USER_Amount USER_Amount HIDDEN NONE;USER_CurrentCounty USER_CurrentCounty HIDDEN NONE;USER_CurrentTwp USER_CurrentTwp HIDDEN NONE;USER_CurrentSchool USER_CurrentSchool HIDDEN NONE;USER_CurrentFee USER_CurrentFee HIDDEN NONE;USER_Lien USER_Lien HIDDEN NONE;USER_LienDesc USER_LienDesc HIDDEN NONE;USER_SignedFor USER_SignedFor HIDDEN NONE;USER_SheriffService USER_SheriffService HIDDEN NONE;USER_PostFlag USER_PostFlag HIDDEN NONE;USER_SentToPalmetto USER_SentToPalmetto HIDDEN NONE;USER_PalmettoIneligible USER_PalmettoIneligible HIDDEN NONE;USER_SaleType USER_SaleType VISIBLE NONE;USER_CarrierRoute USER_CarrierRoute HIDDEN NONE;USER_DeliveryPoint USER_DeliveryPoint HIDDEN NONE;USER_CheckDigit USER_CheckDigit HIDDEN NONE;USER_Job USER_Job HIDDEN NONE;USER_Tray USER_Tray HIDDEN NONE;USER_Package USER_Package HIDDEN NONE;USER_Sequence USER_Sequence HIDDEN NONE;USER_ZipCodeNumber USER_ZipCodeNumber HIDDEN NONE;USER_ZipCodeNumber2 USER_ZipCodeNumber2 HIDDEN NONE;USER_IMBNumeric USER_IMBNumeric HIDDEN NONE;USER_IMBAlpha USER_IMBAlpha HIDDEN NONE;USER_PID USER_PID VISIBLE NONE")
except:
    print ("\n Unable to Append VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT")
    write_log("\n Unable to Append VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT", logfile)
    logging.exception('Got exception on Append VIS_REALMAST_GEOCODE from memory to MISSING_GIS_GEOCODE in AUTOWORKSPACE/ASSESSMENT logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:
    # Export unmatched records to excel
    arcpy.TableToExcel_conversion(Unmatched_Geocoded_TaxClaim_Records, MISSING_GIS_REPORT, "ALIAS", "DESCRIPTION")
    print ("\n Exporting unmatched records report to: \\FILELOCATION\GIS\Assessment\Reports")
    write_log("\n Exporting unmatched records report to: \\FILELOCATION\GIS\Assessment\Reports", logfile)
except:
    print ("\n Unable to Export unmatched records to excel")
    write_log("\n Unable to Export unmatched records to excel", logfile)
    logging.exception('Got exception on Export unmatched records to excel logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("         Exporting update table to excel file at "+ASMT_REPORT_FLDR+ " completed")
write_log("         Exporting update table to excel file at " +ASMT_REPORT_FLDR+ " completed", logfile)


end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n Active Active Tax Claim records missing from GIS REPORT HAS BEEN UPDATED: " + str(Day) + " " + str(end_time))
write_log("\n Active Active Tax Claim records missing from GIS REPORT HAS BEEN UPDATED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
