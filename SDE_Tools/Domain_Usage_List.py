# ---------------------------------------------------------------------------
# Domain_Usage_List.py
#
# Description:
# Once a database name is entered in the SDEConnection variable, an excel spreadsheet is created.
#
# Finds active & orphan domains used in SDE feature classes and tables that are used in fields not registered as domains in Geodatabase
#
# Author: Phil Baranyai
# Created on: 2022-12-19 
# Updated on 2024-03-29
# ---------------------------------------------------------------------------
print("This tool will check all domains within the SDE connection workspace entered below, and provide a list of active/orphan domains")
print("\nLoading python modules, please wait...")

# import required modules
import arcpy, os, logging, datetime,sys,time
from arcpy import env
import pandas as pd
from openpyxl import load_workbook

# Allows user to enter SDE connection name
print("Enter SDE Connection below): \n Example: **SDENAME** \n Leaving blank will run domain list for ALL '*.sde connections in SDE_Connection folder")
SDEConnection = input('Enter SDE Connection Name (not the path): ')

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%Y-%m-%d", time.localtime())
Time = time.strftime("%H%M", time.localtime())
start_time = time.time()
elapsed_time = time.time() - start_time

# Setup export path to *script location* log folder
try:
    LogDirectory = os.getcwd()+"\\log"
    logdirExists = os.path.exists(LogDirectory)
    if not logdirExists:
        os.makedirs(LogDirectory)
        print(LogDirectory+" was not found, so it was created")
except:
    print('\n Unable to create log folder within '+os.getcwd()+' folder')
    sys.exit()

# Setup export path to *script location* Domain_Usage_Reports folder
try:
    ReportDirectory = os.getcwd()+"\\Domain_Usage_Reports"
    reportdirExists = os.path.exists(ReportDirectory)
    if not reportdirExists:
        os.makedirs(ReportDirectory)
        print(ReportDirectory+" was not found, so it was created")
except:
    print('\n Unable to establish Domain_Usage_Reports folder within '+os.getcwd()+' folder')
    sys.exit()

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = LogDirectory +"\\OrphanDomains_List_Log.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
def write_log(text, file):
    f = open(file, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\n".format(text))  # write the text to the logfile and move to next line
    return

# Establish variables for SDE connection file folder, arcpy environment workspace, and workspace list (to iterate through)
SDEConnectionFilePath = r"\\FILEPATH\\SDEConnectionFiles"
arcpy.env.workspace = SDEConnectionFilePath
workspaces = arcpy.ListWorkspaces(SDEConnection+"*_SDE.sde", "SDE")

# Create an empty list to populate with the orphaned domains
orphanedDomains = []

# Create an empty list to populate with all the domains in each workspace (database connection)
allDomains = []

# Create an empty list to populate with the applied (non-orphaned) domains in each workspace (database connection)
appliedDomains = []
appliedDomainsDisplay = []

start_time = time.time()
print ("============================================================================")
print ("Creating list of orphaned domains from feature classes and tables within "+SDEConnection+" as of: "+ str(Day) + " " + str(Time)+" hrs")
print ("============================================================================")
write_log ("============================================================================", logfile)
write_log ("Creating list of orphaned domains from feature classes and tables within "+SDEConnection+" as of: "+ str(Day) + " " + str(Time)+" hrs", logfile)
write_log ("============================================================================", logfile)

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Define a function to list all domains in use and a printable one for the report
def ListAppliedDomains(table): # could also be a feature class
    """
    Returns a list of domain names applied in the FC or table
    """
    # create empty list for domain names
    appliedDomains = []
    applied_domains_display = []

    # add any applied domains to the list
    for f in arcpy.ListFields(table):
        if f.domain != "":
            appliedDomains.append(f.domain)

    return appliedDomains

# Define a function to list the domain names applied to each table or FC (to include subtypes)
def list_domains_by_subtype(fc):
    # Check if feature class has subtypes
    subtypes = arcpy.da.ListSubtypes(fc)
    if subtypes:
        # Loop through each subtype
        for subtype_code, subtype_properties in subtypes.items():
            # Get field value dictionary for each subtype
            field_values = subtype_properties["FieldValues"]
            # Loop through  field value pairs
            for field_name, field_domain in field_values.items():
                # Check if domain is assigned
                if field_domain[1] is not None and subtype_code > 0:
                    appliedDomains.append(field_domain[1].name)
                    appliedDomainsDisplay.append(f"{field_domain[1].name} --> within Feature Class/Table: {fc.lstrip(SDEConnectionFilePath)} --> within Field: {field_name} --> within Subtype code: {subtype_code}")
                    print('\t', f"{field_domain[1].name} --> within Feature Class/Table: {fc.lstrip(SDEConnectionFilePath)} --> within Field: {field_name} --> within Subtype code: {subtype_code}")
                if field_domain[1] is not None and subtype_code == 0:
                    appliedDomains.append(field_domain[1].name)
                    appliedDomainsDisplay.append(f"{field_domain[1].name} --> within Feature Class/Table: {fc.lstrip(SDEConnectionFilePath)} --> within Field: {field_name}")
                    print('\t', f"{field_domain[1].name} --> within Feature Class/Table: {fc.lstrip(SDEConnectionFilePath)} --> within Field: {field_name}")
    else:
        print(f" {fc} has no subtypes")

# Read all domains objects from SDE workspace(s), provide visual count & append all domains to addDomains list
try:
    for WKSP in workspaces:
        env.workspace = WKSP
        datasets = arcpy.ListDatasets()
        domainObjects = arcpy.da.ListDomains(WKSP)
        for domain in domainObjects:
            allDomains.append(domain.name)
        print(WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde')+" has {} domains.".format(str(len(domainObjects))))
        write_log(WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde')+" has {} domains.".format(str(len(domainObjects))),logfile)
except:
    print('\n Unable to list domain objects within SDE workspaces - check to make sure you have access to the SDE connection and/or the connection is spelled correctly.')
    write_log('\n Unable to list domain objects within SDE workspaces - check to make sure you have access to the SDE connection and/or the connection is spelled correctly.',logfile)
    logging.exception('Got exception on list domain objects within SDE workspaces - check to make sure you have access to the SDE connection and/or the connection is spelled correctly. logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Clean up the list of domain objects now that we are done with it to free up memory in script
del domainObjects

# Iterate through each workspace in workspaces list, in each workspace, find all datasets (and feature classes within), feature classes (in root), and tables
# For each feature class/table, examine with 'list_domains_by_subtype' function from above.  Write any domains in use to 'usedDomains' list.
try:
    allFcsAndTables = []
    for WKSP in workspaces:
        env.workspace = WKSP
        print('\n Collecting items within SDE connection:',WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde'))

        # Get lists of datasets, feature classes, tables, and rasters
        datasets = arcpy.ListDatasets()
        fcs = arcpy.ListFeatureClasses()
        tbls = arcpy.ListTables()
        
        # Processes feature/raster datasets
        for ds_name in datasets:
            print('\t', 'Processing data within Feature Dataset: ',WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde'),' | ',ds_name)

            # Processes feature classes & rasters within datasets, displays data as nested within dataset
            FC_in_DS=arcpy.ListFeatureClasses(feature_dataset=ds_name)
            for fc_ds_data in FC_in_DS:
                    list_domains_by_subtype(WKSP+"\\\\"+ds_name+"\\\\"+fc_ds_data)
                    usedDomains = ListAppliedDomains(fc_ds_data)
            else:
                pass

        # Checks for standalone feature classes (not within feature datasets)    
        for fc in fcs:
            list_domains_by_subtype(WKSP+"\\\\"+fc)
            usedDomains = ListAppliedDomains(fc)
        else:
            pass

        # Checks for tables            
        for tbl in tbls:
            list_domains_by_subtype(WKSP+"\\\\"+tbl)
            usedDomains = ListAppliedDomains(tbl)
        else:
            pass
except:
    print('\n Unable to list all feature classes and tables within SDE workspace')
    write_log('\n Unable to list all feature classes and tables within SDE workspace',logfile)
    logging.exception('Got exception on list all feature classes and tables within SDE workspace logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Compare domain values from allDomains list (all domains in connection) and appliedDomains list (only used domains).  If values exist in allDomains list that were not accounted 
# for in appliedDomains list append extra domain values into orphanedDomains list
for od in allDomains:
    if od not in appliedDomains:
        orphanedDomains.append(od)

# Alphabetically sort and print (within window) list of Actively used domains.
print("\n The following domains are CURRENTLY in use in your workspace!\n")
write_log("\n The following domains are CURRENTLY in use in your workspace!\n", logfile)
try:
    for item in appliedDomainsDisplay:
        appliedDomainsDisplay.sort()
        print(item)
        write_log(item,logfile)
except:
    print('\n Unable to create active domain results list (displayed with feature class/table)')
    write_log('\n Unable to create active domain results list (displayed with feature class/table)',logfile)
    logging.exception('Got exception on create active domain results list (displayed with feature class/table) logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Alphabetically sort and print (within window) list of Orphan domains.
print("\n The following domains are NOT in use in your workspace!\n")
write_log("\n The following domains are NOT in use in your workspace!\n", logfile)

try:
    for item in orphanedDomains:
        orphanedDomains.sort()
        print(item)
        write_log(item,logfile)
except:
    print('\n Unable to create orphan domain results list')
    write_log('\n Unable to create orphan domain results list',logfile)
    logging.exception('Got exception on create orphan domain results list logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()
    
# Creating Actively Used domains dataframe
AppliedDomains_df = pd.DataFrame({'Active Domains - These domains are in use within '+SDEConnection: appliedDomainsDisplay})
# Creating Orphan domains dataframe
OrphanDomains_df = pd.DataFrame({'Orphan Domains - These domains are not in use within '+SDEConnection: orphanedDomains})

# Set Excel spreadsheet output name
ExcelOutput = os.path.join(ReportDirectory,str(SDEConnection)+'__Domain_Usage_report__'+str(date)+"_"+str(Time)+'.xlsx')
XLWriter = pd.ExcelWriter(ExcelOutput)

# Exporting Actively Used domains dataframe & Orphan domains dataframe to excel
try:
    print('\nExporting to Excel, located at: '+ExcelOutput)
    write_log('\nExporting to Excel, located at: '+ExcelOutput,logfile)
    AppliedDomains_df.to_excel(XLWriter, sheet_name='Active Domains', index=False)
    OrphanDomains_df.to_excel(XLWriter, sheet_name='Orphan Domains', index=False)
    XLWriter.close()
except:
    print('\n Unable to export dataframes to excel')
    write_log('\n Unable to export dataframes to excel',logfile)
    logging.exception('Got exception on export dataframes to excel logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Access exported excel workbook, and auto-size columns for easier read
try:
    print("\n Resizing excel columns to autofit columns")
    write_log("\n Resizing excel columns to autofit columns",logfile)
    wb = load_workbook(ExcelOutput)
    for sheet in wb.worksheets:
        for column in sheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2) * 1.2
            sheet.column_dimensions[column_letter].width = adjusted_width
            sheet.auto_filter.ref = sheet.dimensions
    wb.save(ExcelOutput)
except:
    print('\n Unable to resize excel columns to fit data')
    write_log('\n Unable to resize excel columns to fit data',logfile)
    logging.exception('Got exception on resize excel columns to fit data logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Provide elapsed time calculation for completed statement below.
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n DOMAIN USAGE LIST WITHIN FC & TABLES HAS COMPLETED: " + str(Day) + " " + str(Time)+" hrs")
write_log("\n DOMAIN USAGE LIST WITHIN FC & TABLES HAS COMPLETED: " + str(Day) + " " + str(Time)+" hrs", logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M %p", time.localtime())+" hrs")
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M %p", time.localtime())+ "hrs"), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)
write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)

# Close program by depressing enter key on keyboard
input("Press enter key to close program")
sys.exit()
