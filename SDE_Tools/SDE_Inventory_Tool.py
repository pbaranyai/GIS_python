# ---------------------------------------------------------------------------
# SDEDataInventory.py
#
# Description:
# Once a database name is entered in the SDEConnection variable, an excel file is created for the following items.
#
# Author: Phil Baranyai
# Created on: 2022-12-16 
# Updated on 2024-03-08
# ---------------------------------------------------------------------------

print("This tool will iterate through the user provided SDE connection, and provide a report of all items, within it.")
print("\nLoading python modules, please wait...")
import arcpy, os, sys, logging, datetime
import pandas as pd
from openpyxl import load_workbook
from arcpy import env

print("Enter SDE Connection below (no need to add _SDE, the script will do this automatically): \n Example: YOUR_DATABASE_NAME \n ****Leaving blank will run domain list for ALL 'SDE Connection'_SDE*.sde connections in SDE_Connection folder****")
SDEConnection = input('\n    Enter SDE Connection Name (not the path): ')

##^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^##


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

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = LogDirectory + "\\SDE_Inventory_Reports_log.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

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

# Setup export path to *script location* SDEInventory_Reports folder
try:
    ReportDirectory = os.getcwd()+"\\SDEInventory_Reports"
    reportdirExists = os.path.exists(ReportDirectory)
    if not reportdirExists:
        os.makedirs(ReportDirectory)
        print(ReportDirectory+" was not found, so it was created")
        write_log(ReportDirectory+" was not found, so it was created",logfile)
except:
    print('\n Unable to establish PortalDependencies_Reports folder within '+os.getcwd()+' folder')
    write_log('\n Unable to create PortalDependencies_Reports folder within '+os.getcwd()+' folder',logfile)
    logging.exception('Got exception on create PortalDependencies_Reports folder within '+os.getcwd()+' folder logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

print ("\n============================================================================")
print ("Creating Inventory for "+SDEConnection+" as of: "+ str(Day) + " " + str(Time))
print ("============================================================================")
write_log ("\n============================================================================", logfile)
write_log ("Creating Inventory for "+SDEConnection+" as of: "+ str(Day) + " " + str(Time), logfile)
write_log ("============================================================================", logfile)

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Path to SDE connectionfiles
SDEConnectionFilePath = r"\\PATHNAME\\SDEConnectionFiles"
arcpy.env.workspace = SDEConnectionFilePath
workspaces = arcpy.ListWorkspaces(SDEConnection+"*_SDE.sde", "SDE")

# Set Excel spreadsheet output name
ExcelOutput = os.path.join(ReportDirectory,str(SDEConnection)+'__SDE_Inventory_report__'+str(date)+"_"+str(Time)+'.xlsx')

# Create empty list for SDE items to be appended to
SDE_Items = []

# Iterate through each workspace (_SDE connection) within database instance, load items into SDE_Items list 
for WKSP in workspaces:
    env.workspace = WKSP
    print('\n Collecting items within SDE connection:',WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde'))

    # Get lists of datasets, feature classes, tables, and rasters
    datasets = arcpy.ListDatasets()
    fcs = arcpy.ListFeatureClasses()
    tbls = arcpy.ListTables()
    rst = arcpy.ListRasters()
    
    # Processes feature/raster datasets
    for ds_name in datasets:
        SDE_Items.append({'Feature/Raster Dataset': WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde')+' | '+ds_name})
        print('\t', 'Feature/Raster Dataset: ',WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde'),' | ',ds_name)

        # Processes feature classes & rasters within feature datasets, displays data as nested within dataset
        FC_in_DS=arcpy.ListFeatureClasses(feature_dataset=ds_name)
        RST_in_DS=arcpy.ListRasters(raster_type=ds_name)
        for fc_ds_data in FC_in_DS:
            SDE_Items.append({'Feature Classes within Dataset':'Feature Class within '+WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde')+' | '+ds_name+' dataset '+fc_ds_data})
            print('\t', 'Feature Class within '+WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde'),' | ',ds_name,' dataset: ',fc_ds_data)   
        for rst_ds_data in RST_in_DS:
            SDE_Items.append({'Raster within Dataset':'Raster within '+WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde')+' | '+ds_name+' dataset '+rst_ds_data})
            print('\t', 'Raster within '+WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde'),' | ',ds_name,' dataset: ',rst_ds_data)

    # Checks for standalone feature classes (not within feature datasets)    
    for fc in fcs:
        SDE_Items.append({'Standalone Feature Class': WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde')+' | '+fc})
        print('\t', 'Standalone Feature Class: ',WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde'),' | ',fc)

    # Checks for tables            
    for tbl in tbls:
        SDE_Items.append({'Tables': WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde')+' | '+tbl})
        print('\t', 'Tables: ',WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde'),' | ',tbl)

    # Checks for standalone rasters (not within raster datasets)    
    for rasters in rst:
        SDE_Items.append({'Rasters': WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde')+' | '+rasters})
        print('\t', 'Rasters: ',WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde'),' | ',rasters)

# Create a dataframe from dictionary within SDE_Items list
try:
    SDEinventory_df = pd.DataFrame(SDE_Items)
except:
    print('\n Unable to create dataframe from SDE_Items list')
    write_log('\n Unable to create dataframe from SDE_Items list',logfile)
    logging.exception('Got exception on create dataframe from SDE_Items list logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Exporting Dataframe to excel
try:
    print('\nExporting to Excel, located at: '+ExcelOutput)
    write_log('\nExporting to Excel, located at: '+ExcelOutput,logfile)
    SDEinventory_df.to_excel(ExcelOutput, 'Items', index=False)
except:
    print('\n Unable to export excel spreadsheet to: '+ExcelOutput)
    write_log('\n Unable to export excel spreadsheet to: '+ExcelOutput,logfile)
    logging.exception('Got exception on export excel spreadsheet to: '+ExcelOutput+' logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Access exported excel workbook, and auto-size columns for easier read
try:
    print("\n Resizing excel columns to autofit columns")
    write_log("\n Resizing excel columns to autofit columns",logfile)
    wb = load_workbook(ExcelOutput)
    ws = wb['Items']
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column_letter].width = adjusted_width
        ws.auto_filter.ref = ws.dimensions
    wb.save(ExcelOutput)
except:
    print('\n Unable to resize excel columns to fit data')
    write_log('\n Unable to resize excel columns to fit data',logfile)
    logging.exception('Got exception on resize excel columns to fit data logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Provides stop time and elapsed time variables
end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print ("\n SDE INVENTORY LIST HAS COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n SDE INVENTORY LIST HAS COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)

# For command run, allows user to see all program print statements before closing the command window by pressing any key.
input("Press enter key to close program")
sys.exit()
