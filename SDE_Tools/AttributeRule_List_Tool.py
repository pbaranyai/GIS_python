# ---------------------------------------------------------------------------
# AttributeRule_List_Tool.py
#
# Description:
# Once a database name is entered in the SDEConnection variable, an excel spreadsheet is created.
#
# Attribute rules used in SDE feature classes and tables 
#
# Author: Phil Baranyai
# Created on: 2023-03-29
# Updated on 2024-03-29
# ---------------------------------------------------------------------------
print("This tool will check all attribute rules within the SDE connection workspace entered below, and provide a list of exported in excel")
print("\nLoading python modules, please wait...")

# import required modules
import arcpy,os,logging,datetime,sys,time
from arcpy import env
import pandas as pd
from openpyxl import load_workbook

# Allows user to enter SDE connection name
print("Enter SDE Connection below (no need to add _SDE, the script will do this automatically): \n Example: SDENAME \n ****Leaving blank will run domain list for ALL 'SDE Connection'_SDE*.sde connections in SDE_Connection folder****")
SDEConnection = input('\n    Enter SDE Connection Name (not the path): ')

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

# Setup export path to *script location*  AttributeRule_List_Reports folder
try:
    ReportDirectory = os.getcwd()+"\\ AttributeRule_List_Reports"
    reportdirExists = os.path.exists(ReportDirectory)
    if not reportdirExists:
        os.makedirs(ReportDirectory)
        print(ReportDirectory+" was not found, so it was created")
except:
    print('\n Unable to establish  AttributeRule_List_Reports folder within '+os.getcwd()+' folder')
    sys.exit()

# Setup error logging (configure error logging location, type, and filemode -- overwrite every run)
logfile = LogDirectory +"\\ AttributeRule_List_Log.log"
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

# Create an empty list to populate with all the domains in each workspace (database connection)
attributeRules_Calculation = []
attributeRules_Constraint = []
attributeRules_Validation = []

start_time = time.time()
print ("============================================================================")
print ("Creating list of attribute rules from feature classes and tables within "+SDEConnection+" as of: "+ str(Day) + " " + str(Time)+" hrs")
print ("============================================================================")
write_log ("============================================================================", logfile)
write_log ("Creating list of attribute rules from feature classes and tables within "+SDEConnection+" as of: "+ str(Day) + " " + str(Time)+" hrs", logfile)
write_log ("============================================================================", logfile)

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Define a function to list the attribute rules applied to each table or FC (to include subtypes)
def list_attribute_rules(fc):
    # Check if feature class has subtypes
    fc_desc = arcpy.Describe(fc)
    if fc_desc.attributeRules:
        print(f"Feature Class: {fc} as attribute rules")
 
        # Access individual rule properties (based on rule type) using a loop
        for rule in fc_desc.attributeRules:
            if 'Calculation' in rule.type:
                ruleType = rule.type
                ruleName = rule.name
                ruleCreationtime = rule.creationTime
                ruleField = rule.fieldName
                ruleSTcode = rule.subtypeCode
                ruleDesc = rule.description
                ruleEditable = rule.userEditable
                ruleEnabled = rule.isEnabled
                ruleEval = rule.evaluationOrder
                ruleExclClientEval = rule.excludeFromClientEvaluation
                ruleTriggerEvent = rule.triggeringEvents
                ruleScriptExp = rule.scriptExpression
                ruleBatchFlag = rule.batch
                ruleSeverity = rule.severity
                ruleTags = rule.tags
                attributeRules_Calculation.append({'Rule Type': ruleType, 'Name': ruleName, 'Creation Time': ruleCreationtime, 'Field': ruleField, 'Subtype code': ruleSTcode, 'Description': ruleDesc,
                                              'Is Editable?':ruleEditable, 'Is Enabled?': ruleEnabled, 'Evaluation Order': ruleEval, 'Exclude from client evaluation': ruleExclClientEval, 'Triggering events': ruleTriggerEvent,
                                              'Script expression': ruleScriptExp, 'Is flagged as a batch rule?': ruleBatchFlag, 'Severity': ruleSeverity, 'Tags': ruleTags})
                print('Rule Type: %s \n Field: %s \n Name: %s' %(ruleType,ruleField,ruleName))
            elif "Constraint" in rule.type:
                ruleType = rule.type
                ruleName = rule.name
                ruleCreationtime = rule.creationTime
                ruleSTcode = rule.subtypeCode
                ruleDesc = rule.description
                ruleEditable = rule.userEditable
                ruleEnabled = rule.isEnabled
                ruleErrorNum = rule.errorNumber
                ruleErrorMsg = rule.errorMessage
                ruleExclClientEval = rule.excludeFromClientEvaluation
                ruleTriggerEvent = rule.triggeringEvents
                ruleScriptExp = rule.scriptExpression
                ruleTags = rule.tags
                attributeRules_Constraint.append({'Rule Type': ruleType, 'Name': ruleName, 'Creation Time': ruleCreationtime,'Subtype code': ruleSTcode, 'Description': ruleDesc,'Is Editable?':ruleEditable, 'Is Enabled?': ruleEnabled,
                                              'Error Number':ruleErrorNum, 'Error Message': ruleErrorMsg,'Exclude from client evaluation': ruleExclClientEval, 'Triggering events': ruleTriggerEvent,'Script expression': ruleScriptExp,'Tags': ruleTags})
                print('Rule Type: %s \n Name: %s' %(ruleType,ruleName))
            elif "Validation" in rule.type:
                ruleType = rule.type
                ruleName = rule.name
                ruleCreationtime = rule.creationTime
                ruleSTcode = rule.subtypeCode
                ruleDesc = rule.description
                ruleEnabled = rule.isEnabled
                ruleErrorNum = rule.errorNumber
                ruleErrorMsg = rule.errorMessage
                ruleScriptExp = rule.scriptExpression
                ruleBatchFlag = rule.batch
                ruleSeverity = rule.severity
                ruleTags = rule.tags
                attributeRules_Validation.append({'Rule Type': ruleType, 'Name': ruleName, 'Creation Time': ruleCreationtime,'Subtype code': ruleSTcode, 'Description': ruleDesc, 'Is Enabled?': ruleEnabled, 'Error Number':ruleErrorNum,
                                              'Error Message': ruleErrorMsg,'Script expression': ruleScriptExp,'Is flagged as a batch rule?': ruleBatchFlag, 'Severity': ruleSeverity, 'Tags': ruleTags})
                print('Rule Type: %s \n Name: %s' %(ruleType,ruleName))
                

          # Just print to screen to advise no attribute rules on FC
        else:
            print(f" {fc} has no attribute rules")


# Iterate through each workspace in workspaces list, in each workspace, find all datasets (and feature classes within), feature classes (in root), and tables
# For each feature class/table, examine with 'list_attribute_rules' function from above.  Write any rules into corresponding list.
try:
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
                    list_attribute_rules(WKSP+"\\\\"+ds_name+"\\\\"+fc_ds_data)
            else:
                print('\n',fc_ds_data,' was skipped, unable to process or no attribute rules in use')
                continue

        # Checks for standalone feature classes (not within feature datasets)    
        for fc in fcs:
            list_attribute_rules(WKSP+"\\\\"+fc)
        else:
            print('\n',fc,' was skipped, unable to process or no attribute rules in use')
            continue

        # Checks for tables            
        for tbl in tbls:
            list_attribute_rules(WKSP+"\\\\"+tbl)
        else:
            print('\n',tbl,' was skipped, unable to process or no attribute rules in use')
            continue
except:
    print('\n Unable to list all feature classes and tables within ', WKSP,' workspace')
    write_log('\n Unable to list all feature classes and tables within '+ WKSP+' workspace',logfile)
    logging.exception('Got exception on list all feature classes and tables within '+ WKSP+' workspace logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Establishing dataframes from lists/dictionaries created above
attributeRules_Calculation_df = pd.DataFrame(attributeRules_Calculation)   
attributeRules_Constraint_df = pd.DataFrame(attributeRules_Constraint)
attributeRules_Validation_df = pd.DataFrame(attributeRules_Validation)

# Set Excel spreadsheet output name
ExcelOutput = os.path.join(ReportDirectory,str(SDEConnection)+'__Attribute_Rules_Usage_report__'+str(date)+"_"+str(Time)+'.xlsx')
XLWriter = pd.ExcelWriter(ExcelOutput)

# Exporting attribute rules dataframes to excel
try:
    print('\nExporting to Excel, located at: '+ExcelOutput)
    write_log('\nExporting to Excel, located at: '+ExcelOutput,logfile)
    attributeRules_Calculation_df.to_excel(XLWriter, sheet_name='Calculation Rules', index=False)
    attributeRules_Constraint_df.to_excel(XLWriter, sheet_name='Constraint Rules', index=False)
    attributeRules_Validation_df.to_excel(XLWriter, sheet_name='Validation Rules', index=False)
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
print ("\n ATTRIBUTE RULES LIST WITHIN FC & TABLES HAS COMPLETED: " + str(Day) + " " + str(Time)+" hrs")
write_log("\n ATTRIBUTE RULES LIST WITHIN FC & TABLES HAS COMPLETED: " + str(Day) + " " + str(Time)+" hrs", logfile)

print ("Elapsed time: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: "  +time.strftime("%I:%M %p", time.localtime()))
write_log("Elapsed time: " + (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " +time.strftime("%I:%M %p", time.localtime())), logfile)
print ("===========================================================")
write_log("===========================================================",logfile)
write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)

# Close program by depressing enter key on keyboard
input("Press enter key to close program")
sys.exit()
