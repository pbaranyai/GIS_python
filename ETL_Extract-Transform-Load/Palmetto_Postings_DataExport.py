# ---------------------------------------------------------------------------
# Palmetto_Postings_DataExport.py
# Created on: 2021-07-05 
# Updated on 2021-09-21
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Export Tax Parcels, Building Only, Street Centerlines, & Address Points feature classes to FGDB in schema that Palmetto Postings requires.
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
# ---------------------------------------------------------------------------

# Import modules
import sys,arcpy,datetime,os,time,logging,shutil

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"\\FILELOCATION\\GIS\\GIS_LOGS\\Treasurers\\TaxClaim_Data_Spreader.log"  
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

start_time = time.time()

print ("============================================================================")
print (("Creating GIS deliverable for Palmetto Posting: "+ str(Day) + " " + str(Time)))
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Creating GIS deliverable for Palmetto Posting: "+ str(Day) + " " + str(Time), logfile)
write_log("============================================================================", logfile)

# Define Work Paths for FGDB:
PALMETTO_POSTING_FLDR = r"\\FILELOCATION\\GIS\\County office projects\\Treasurers_Office\\PalmettoPosting\\Workspace\\FGDB"
PALMETTO_POSTING_DATA_XML = r"\\FILELOCATION\\GIS\\County office projects\\Treasurers_Office\\PalmettoPosting\\Workspace\\XML\\PALMETTOPOSTING.XML"
PALMETTO_POSTING_FGDB_OLD = r"\\FILELOCATION\\GIS\\County office projects\\Treasurers_Office\\PalmettoPosting\\Workspace\\FGDB\\CrawfordCoPA_PalmettoPosting.gdb"

print ("=====================================================================================================================")
print ("Checking for existing PalmettoPosting FGDB, delete and rebuild fresh if exists.")
print ("Works in ArcGIS Pro")
write_log("Works in ArcGIS Pro", logfile)
print ("=====================================================================================================================")
write_log("\n Checking for existing NorthernTier FGDB, delete and rebuild fresh if exists.", logfile)

try:
    # Pre-clean old FGDB, if exists (if old CrawfordCoPA_PalmettoPosting.gdb exists and was never renamed, the program will delete it, so it will be able to run without failure, henceforth providing the newest data)
    if arcpy.Exists(PALMETTO_POSTING_FGDB_OLD):
        arcpy.Delete_management(PALMETTO_POSTING_FGDB_OLD, "Workspace")
        print (" CrawfordCoPA_PalmettoPosting.gdb found - FGDB deleted")
        write_log(" CrawfordCoPA_PalmettoPosting.gdb found - FGDB deleted", logfile)
except:
    print ("\n Unable to delete CrawfordCoPA_PalmettoPosting.gdb, need to delete existing FGDB manually and/or close program locking the FGDB")
    write_log("Unable to create new CrawfordCoPA_PalmettoPosting.gdb, need to delete existing FGDB manually and/or close program locking the FGDB", logfile)
    logging.exception('Got exception on delete CrawfordCoPA_PalmettoPosting.gdb logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()
    
print ("  Creating fresh version of CrawfordCoPA_PalmettoPosting FGDB")
write_log("  Creating fresh version of CrawfordCoPA_PalmettoPosting FGDB", logfile)

try:
    # Create new File GDB called CrawfordCoPA_PalmettoPosting.gdb (creates new FGDB each time to avoid corruption)
    arcpy.CreateFileGDB_management(PALMETTO_POSTING_FLDR, "CrawfordCoPA_PalmettoPosting", "CURRENT")
except:
    print ("\n Unable to create new CrawfordCoPA_PalmettoPosting.gdb, need to close program locking the FGDB workspace")
    write_log("Unable to create new CrawfordCoPA_PalmettoPosting.gdb, need to close program locking the FGDB workspace", logfile)
    logging.exception('Got exception on create CrawfordCoPA_PalmettoPosting.gdb logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

#Database Connection Folder
Database_Connections = r"\\\FILELOCATION\\GIS\\ArcAutomations\\Database_Connections"

# Define Work Paths for Databases:
PALMETTO_POSTING_FLDR = r"\\FILELOCATION\\GIS\\County office projects\\Treasurers_Office\\PalmettoPosting\\Workspace\\FGDB"
PALMETTO_POSTING_FGDB = PALMETTO_POSTING_FLDR + "\\CrawfordCoPA_PalmettoPosting.gdb"
GIS_DB = Database_Connections + "\\craw_internal@ccsde.sde"

print ("   Importing XML workspace to PalmettoPosting FGDB for schema structure")
write_log("   Importing XML workspace to PalmettoPosting FGDB for schema structure", logfile)

try:
    # Import XML Workspace for PalmettoPosting FGDB Schema (if PalmettoPostings makes changes, this XML will need to be updated)
    arcpy.ImportXMLWorkspaceDocument_management(PALMETTO_POSTING_FGDB, PALMETTO_POSTING_DATA_XML, "SCHEMA_ONLY", "")
    print ("    CrawfordCoPA_PalmettoPosting FGDB schema import completed at "+ time.strftime("%I:%M:%S %p", time.localtime()))
except:
    print ("\n Unable to import XML workspace file")
    write_log("Unable to import XML workspace file", logfile)
    logging.exception('Got exception on import XML workspace file logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

# Local variables:
ADDRESS_POINTS_INTERNAL = GIS_DB + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.ADDRESS_POINTS_INTERNAL"
ADDRESS_POINTS_PPFGDB = PALMETTO_POSTING_FGDB + "\\Address_Points"
BUILDING_ONLY_INTERNAL = GIS_DB + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.BUILDING_ONLY_JOINED_INTERNAL"
BUILDING_ONLY_PPFGDB = PALMETTO_POSTING_FGDB + "\\BuildingOnly"
STREET_CENTERLINE_INTERNAL = GIS_DB + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.STREET_CENTERLINE_INTERNAL"
STREET_CENTERLINE_PPFGDB = PALMETTO_POSTING_FGDB + "\\StreetCenterline"
TAX_PARCELS_INTERNAL = GIS_DB + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.TAX_PARCELS_INTERNAL"
TAX_PARCELS_PPFGDB = PALMETTO_POSTING_FGDB + "\\TaxParcels"

try:
    # Import Address Points from CRAW_INTERNAL into PalmettoPosting FGDB
    arcpy.Append_management(ADDRESS_POINTS_INTERNAL, ADDRESS_POINTS_PPFGDB, "NO_TEST", 'SitusAddress1 "SitusAddress1" true true false 50 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_HSE_STREET,-1,-1;SitusAddress2 "SitusAddress2" true true false 50 Text 0 0 ,First,#;SitusAddressCity "SitusAddressCity" true true false 50 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_POST_OFFICE,-1,-1;SitusAddressZip "SitusAddressZip" true true false 20 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_ZIPCODE,-1,-1;PID "PID" true true false 50 Text 0 0 ,First,#;StateID "StateID" true true false 2 Text 0 0 ,First,#,'+ADDRESS_POINTS_INTERNAL+',AD_STATE,-1,-1;CountyID "CountyID" true true false 4 Long 0 0 ,First,#;PostingYear "PostingYear" true true false 4 Long 0 0 ,First,#', "")
    print ("     Import Address Points from CRAW_INTERNAL into PalmettoPosting FGDB completed at "+ time.strftime("%I:%M:%S %p", time.localtime()))
except:
    print ("\n Unable to import Address Points from CRAW_INTERNAL into PalmettoPosting FGDB")
    write_log("Unable to import Address Points from CRAW_INTERNAL into PalmettoPosting FGDB", logfile)
    logging.exception('Got exception on import Address Points from CRAW_INTERNAL into PalmettoPosting FGDB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Calculate County Code and Posting Year in Address Points - PalmettoPosting FGDB
    arcpy.CalculateField_management(ADDRESS_POINTS_PPFGDB, "CountyID", "20", "PYTHON", "")
    arcpy.CalculateField_management(ADDRESS_POINTS_PPFGDB, "PostingYear", "datetime.datetime.now().year", "PYTHON", "")
    print ("      Calculate County Code and Posting Year in Address Points - PalmettoPosting FGDB completed at "+ time.strftime("%I:%M:%S %p", time.localtime()))
except:
    print ("\n Unable to Calculate County Code and Posting Year in Address Points - PalmettoPosting FGDB")
    write_log("Unable to Calculate County Code and Posting Year in Address Points - PalmettoPosting FGDB", logfile)
    logging.exception('Got exception on Calculate County Code and Posting Year in Address Points - PalmettoPosting FGDB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Import Building Only from CRAW_INTERNAL into PalmettoPosting FGDB
    arcpy.Append_management(BUILDING_ONLY_INTERNAL, BUILDING_ONLY_PPFGDB, "NO_TEST", 'PID "PID" true true false 50 Text 0 0 ,First,#,'+BUILDING_ONLY_INTERNAL+',PID_TEXT,-1,-1;StateID "StateID" true true false 2 Text 0 0 ,First,#;CountyID "CountyID" true true false 3 Text 0 0 ,First,#;SitusAddress1 "SitusAddress1" true true false 50 Text 0 0 ,First,#,'+BUILDING_ONLY_INTERNAL+',REM_PRCL_LOCN,-1,-1;SitusAddress2 "SitusAddress2" true true false 50 Text 0 0 ,First,#;SitusAddressCity "SitusAddressCity" true true false 50 Text 0 0 ,First,#,'+BUILDING_ONLY_INTERNAL+',REM_PRCL_LOCN_CITY,-1,-1;SitusAddressZip "SitusAddressZip" true true false 20 Text 0 0 ,First,#,'+BUILDING_ONLY_INTERNAL+',REM_PRCL_LOCN_ZIP,-1,-1;PostingYear "PostingYear" true true false 50 Text 0 0 ,First,#', "")
    print ("       Import Building Only from CRAW_INTERNAL into PalmettoPosting FGDB at "+ time.strftime("%I:%M:%S %p", time.localtime()))
except:
    print ("\n Unable to import Building Only from CRAW_INTERNAL into PalmettoPosting FGDB")
    write_log("Unable to import Building Only from CRAW_INTERNAL into PalmettoPosting FGDB", logfile)
    logging.exception('Got exception on import Building Only from CRAW_INTERNAL into PalmettoPosting FGDB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Calculate County Code, Posting Year, and State Code in Building Only - PalmettoPosting FGDB
    arcpy.CalculateField_management(BUILDING_ONLY_PPFGDB, "CountyID", "20", "PYTHON", "")
    arcpy.CalculateField_management(BUILDING_ONLY_PPFGDB, "PostingYear", "datetime.datetime.now().year", "PYTHON", "")
    arcpy.CalculateField_management(BUILDING_ONLY_PPFGDB, "StateID", '"PA"', "PYTHON", "")
    print ("        Calculate County Code and Posting Year in Building Only - PalmettoPosting FGDB completed at "+ time.strftime("%I:%M:%S %p", time.localtime()))
except:
    print ("\n Unable to Calculate County Code, Posting Year, and State Code in Building Only - PalmettoPosting FGDB")
    write_log("Unable to Calculate County Code, Posting Year, and State Code in Building Only - PalmettoPosting FGDB", logfile)
    logging.exception('Got exception on Calculate County Code, Posting Year, and State Code in Building Only - PalmettoPosting FGDB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Import Street Centerline from CRAW_INTERNAL into PalmettoPosting FGDB
    arcpy.Append_management(STREET_CENTERLINE_INTERNAL, STREET_CENTERLINE_PPFGDB, "NO_TEST", 'StateID "StateID" true true false 2 Text 0 0 ,First,#,'+STREET_CENTERLINE_INTERNAL+',CL_STATE_L,-1,-1;CountyID "CountyID" true true false 4 Long 0 0 ,First,#;PostingYear "PostingYear" true true false 4 Long 0 0 ,First,#;StreetName "StreetName" true true false 50 Text 0 0 ,First,#,'+STREET_CENTERLINE_INTERNAL+',CL_FULL_NAME,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#', "")
    print ("         Import Street Centerline from CRAW_INTERNAL into PalmettoPosting FGDB completed at "+ time.strftime("%I:%M:%S %p", time.localtime()))
except:
    print ("\n Unable to import Street Centerline from CRAW_INTERNAL into PalmettoPosting FGDB")
    write_log("Unable to import Street Centerline from CRAW_INTERNAL into PalmettoPosting FGDB", logfile)
    logging.exception('Got exception on import Street Centerline from CRAW_INTERNAL into PalmettoPosting FGDB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Calculate County Code and Posting Year in Street Centerline - PalmettoPosting FGDB
    arcpy.CalculateField_management(STREET_CENTERLINE_PPFGDB, "CountyID", "20", "PYTHON", "")
    arcpy.CalculateField_management(STREET_CENTERLINE_PPFGDB, "PostingYear", "datetime.datetime.now().year", "PYTHON", "")
    print ("          Calculate County Code and Posting Year Street Centerline - PalmettoPosting FGDB completed at "+ time.strftime("%I:%M:%S %p", time.localtime()))
except:
    print ("\n Unable to Calculate County Code and Posting Year Street Centerline - PalmettoPosting FGDB")
    write_log("Unable to Calculate County Code and Posting Year Street Centerline - PalmettoPosting FGDB", logfile)
    logging.exception('Got exception on Calculate County Code and Posting Year Street Centerline - PalmettoPosting FGDB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Import Tax Parcels from CRAW_INTERNAL into PalmettoPosting FGDB
    arcpy.Append_management(TAX_PARCELS_INTERNAL, TAX_PARCELS_PPFGDB, "NO_TEST", 'PID "PID" true true false 4 Long 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',PID,-1,-1;StateID "StateID" true true false 2 Text 0 0 ,First,#;CountyID "CountyID" true true false 4 Long 0 0 ,First,#;SitusAddress1 "SitusAddress1" true true false 50 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',REM_PRCL_LOCN,-1,-1;SitusAddress2 "SitusAddress2" true true false 50 Text 0 0 ,First,#;SitusAddressCity "SitusAddressCity" true true false 50 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',REM_PRCL_LOCN_CITY,-1,-1;SitusAddressZip "SitusAddressZip" true true false 20 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',REM_PRCL_LOCN_ZIP,-1,-1;PostingYear "PostingYear" true true false 4 Long 0 0 ,First,#;CAMA_PIN "CAMA_PIN" true true false 50 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',CAMA_PIN,-1,-1;SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#', "")
    print ("           Import Tax Parcels from CRAW_INTERNAL into PalmettoPosting FGDB completed at "+ time.strftime("%I:%M:%S %p", time.localtime()))
except:
    print ("\n Unable to import Tax Parcels from CRAW_INTERNAL into PalmettoPosting FGDB")
    write_log("Unable to import Tax Parcels from CRAW_INTERNAL into PalmettoPosting FGDB", logfile)
    logging.exception('Got exception on import Tax Parcels from CRAW_INTERNAL into PalmettoPosting FGDB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Calculate County Code, Posting Year, and State Code in Tax Parcels - PalmettoPosting FGDB
    arcpy.CalculateField_management(TAX_PARCELS_PPFGDB, "CountyID", "20", "PYTHON", "")
    arcpy.CalculateField_management(TAX_PARCELS_PPFGDB, "PostingYear", "datetime.datetime.now().year", "PYTHON", "")
    arcpy.CalculateField_management(TAX_PARCELS_PPFGDB, "StateID", '"PA"', "PYTHON", "")
    print ("            Calculate County Code, Posting Year, and State Code in Tax Parcels - PalmettoPosting FGDB completed at "+ time.strftime("%I:%M:%S %p", time.localtime()))
except:
    print ("\n Unable to Calculate County Code, Posting Year, and State Code in Tax Parcels - PalmettoPosting FGDB")
    write_log("Unable to Calculate County Code, Posting Year, and State Code in Tax Parcels - PalmettoPosting FGDB", logfile)
    logging.exception('Got exception on Calculate County Code, Posting Year, and State Code in Tax Parcels - PalmettoPosting FGDB logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

try:
    # Creating ZIP file from existing FGDB
    if arcpy.Exists(PALMETTO_POSTING_FGDB):
        shutil.make_archive(PALMETTO_POSTING_FGDB, 'zip', PALMETTO_POSTING_FGDB)
        print ("\n  Compressing Palmetto Posting FGDB into ZIP file...")
        write_log("  Compressing Palmetto Posting FGDB into ZIP file...",logfile)
except:
    print ("\n Unable to compress Palmetto Posting_" + date + ".gdb into zipfile")
    write_log("Unable to compress Palmetto Posting_" + date + ".gdb into zipfile", logfile)
    logging.exception('Got exception on compress Palmetto Posting_" + date + ".gdb into zipfile logged at:'  + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n Palmetto Posting FGDB export created and Completed | Be sure to delete CrawfordCoPA_PalmettoPosting when upload to Palmetto Posting website is complete: " + str(Day) + " " + str(end_time)))
write_log("\n Palmetto Posting FGDB export created and Completed | Be sure to delete CrawfordCoPA_PalmettoPosting when upload to Palmetto Posting website is complete: " + str(Day) + " " + str(end_time), logfile)

print (("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")

try:
    # Opening folder where Palmetto Posting FGDB exists, to allow user to upload to FTP and then delete files
    print ("\n Opening "+PALMETTO_POSTING_FLDR)
    print ("     You need to manually delete prior FGDBs and ZIP files in folder after uploading to Palmetto Postings website.  Non-zip folder was kept to QC the output before upload")
    NORTHERN_TIER_CAD_FLDR=os.path.realpath(PALMETTO_POSTING_FLDR)
    os.startfile(PALMETTO_POSTING_FLDR)
except: 
    print ("\n Unable to open "+PALMETTO_POSTING_FLDR)
    write_log("Unable to open "+PALMETTO_POSTING_FLDR, logfile)
    logging.exception('Got exception on Unable to open '+PALMETTO_POSTING_FLDR+' logged at:'  + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit ()

write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
