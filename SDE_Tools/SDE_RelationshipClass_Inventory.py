# ---------------------------------------------------------------------------
# SDE_RelationshipClass_Inventory.py
#
# Description:
# Catalogs and reports relationship classes within SDE, exports to Microsoft Excel
#
# Author: Phil Baranyai
# Created on: 2022-12-20 
# Updated on 2023-03-25
# ---------------------------------------------------------------------------

import arcpy, os, sys,time,logging
from arcpy import env
from datetime import datetime
import pandas as pd
from openpyxl import load_workbook

SDEConnection = "SDEConnectionName"

# Setup Date (and day/time)
date = datetime.today().strftime("%Y%m%d")
Day = datetime.today().strftime("%Y-%m-%d")
Time = datetime.today().strftime("%H%M")
start_time = time.time()

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
logfile = LogDirectory + "\\SDE_RelationshipClass_Inventory_log.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

try:
    # Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
    def write_log(text, file):
        f = open(file, 'a')           # 'a' will append to an existing file if it exists
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    print ("\n Unable to write log file")
    sys.exit ()

# Setup export path to *script location* SDEInventory_Reports folder
try:
    ReportDirectory = os.getcwd()+"\\SDE_RelationshipClass_Reports"
    reportdirExists = os.path.exists(ReportDirectory)
    if not reportdirExists:
        os.makedirs(ReportDirectory)
        print(ReportDirectory+" was not found, so it was created")
        write_log(ReportDirectory+" was not found, so it was created",logfile)
except:
    print('\n Unable to establish SDE_RelationshipClass_Reports folder within '+os.getcwd()+' folder')
    write_log('\n Unable to create SDE_RelationshipClass_Reports folder within '+os.getcwd()+' folder',logfile)
    logging.exception('Got exception on create SDE_RelationshipClass_Reports folder within '+os.getcwd()+' folder logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

print ("============================================================================")
print ("Creating Relationship Class Inventory for "+SDEConnection+" as of: "+ str(Day) + " " + time.strftime("%I:%M:%S %p", time.localtime()))
print ("============================================================================")
write_log ("============================================================================", logfile)
write_log ("Creating Relationship Class Inventory for "+SDEConnection+" as of: "+ str(Day) + " " + time.strftime("%I:%M:%S %p", time.localtime()))
write_log ("============================================================================", logfile)

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

SDEConnectionFilePath = r"\\CONNECTIONFILE PATH\\SDEConnectionFiles"
arcpy.env.workspace = r"\\CONNECTIONFILE PATH\\SDEConnectionFiles"
workspaces = arcpy.ListWorkspaces(SDEConnection+"*SDE.sde", "SDE")

# Set Excel spreadsheet output name
ExcelOutput = os.path.join(ReportDirectory,str(SDEConnection)+'__SDE_RelationshipClass_report__'+str(date)+"_"+str(Time)+'.xlsx')

# Empty list to store information
relationship_data = []

def detectRelationship(item): 
     rc_list = [c.name for c in arcpy.Describe(item).children if c.datatype == "RelationshipClass"]
     rc_list 
     for rc in rc_list: 
         rc_path = item + "\\" + rc 
         des_rc = arcpy.Describe(rc_path) 
         origin = des_rc.originClassNames 
         destination = des_rc.destinationClassNames
         Cardinality = des_rc.cardinality
         KeyType = des_rc.keyType
         RelateFields = des_rc.originClassKeys
         Attachments = des_rc.isAttachmentRelationship
         Composite = des_rc.isComposite
         Direction = des_rc.notification
         Dest_Origin_label = des_rc.backwardPathLabel
         ClassKey = des_rc.classKey
         DestClassKey = des_rc.destinationClassKeys
         Origin_Dest_label = des_rc.forwardPathLabel
         Attributed = des_rc.isAttributed
         Reflexive = des_rc.isReflexive
         Rules = des_rc.relationshipRules
         SplitPolicy = des_rc.splitPolicy
         relationship_data.append({'Relationship Class': rc, 'Origin': origin, 'Desintation': destination, 'Cardinality': Cardinality, 'KeyType': KeyType, 'Relate Fields': RelateFields, 'Is this an attachment relationship?': Attachments, 'Is this a composite relationship?': Composite, 'Direction': Direction, 'Destination to Origin Label': Dest_Origin_label, 'Origin to Destination Label': Origin_Dest_label, 'Class Key': ClassKey, 'Destination Class Key': DestClassKey, 'Is attributed?': Attributed, 'Is reflexive?': Reflexive, 'Relationship Rules': Rules, 'Split Policy': SplitPolicy})
         print ("Relationship Class: %s \n Origin: %s \n Desintation: %s \n Cardinality: %s \n KeyType: %s \n Relate Fields: %s \n Is this an attachment relationship?: %s \n Is this a composite relationship?: %s \n Direction: %s \n Destination to Origin Label: %s \n Origin to Destination Label: %s \n Class Key: %s \n Destination Class Key: %s \n Is attributed?: %s \n Is reflexive?: %s \n Relationship Rules: %s \n Split Policy: %s" %(rc, origin, destination, Cardinality, KeyType, RelateFields,Attachments,Composite,Direction,Dest_Origin_label,Origin_Dest_label,ClassKey,DestClassKey,Attributed,Reflexive,Rules,SplitPolicy))

for WKSP in workspaces:
    try:
        # Get lists of datasets
        env.workspace = WKSP
        datasets = arcpy.ListDatasets()

        # Processes feature classes/tables within feature datasets
        for ds_name in datasets:
            print('\t', 'Looking for relationship classes within Feature Dataset: ',WKSP.lstrip(SDEConnectionFilePath).rstrip('.sde'),' | ',ds_name)
            detectRelationship(ds_name)

        # Processes feature classes/tables within "root" SDE connection (not inside feature datasets)
        detectRelationship(WKSP)

    except:
        print("\n Error detecting relationships - did not capture all relationships")
        write_log("\n Error detecting relationships - did not capture all relationships", logfile)
        logging.exception('Got exception on detect relationshps logged at:' + str(Day) + " " + str(Time))
        continue

# Create DataFrame from list of dictionaries of SDE_RelationshipClasses
try:
    SDERC_df = pd.DataFrame(relationship_data)
except:
    print('\n Unable to create dataframe from SDE_RelationshipClasses list')
    write_log('\n Unable to create dataframe from SDE_RelationshipClasses list',logfile)
    logging.exception('Got exception on create dataframe from SDE_RelationshipClasses list logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Exporting Dataframe to excel
try:
    print('\nExporting to Excel, located at: '+ExcelOutput)
    write_log('\nExporting to Excel, located at: '+ExcelOutput,logfile)
    SDERC_df.to_excel(ExcelOutput, 'Items', index=False)
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
print ("\n RELATIONSHIP CLASS INVENTORY LIST HAS COMPLETED: " + str(Day) + " " + str(end_time))
write_log("\n RELATIONSHIP CLASS INVENTORY LIST HAS COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M:%S %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M:%S %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
# For command run, allows user to see all program print statements before closing the command window by pressing any key.
input("Press enter key to close program")
sys.exit()
