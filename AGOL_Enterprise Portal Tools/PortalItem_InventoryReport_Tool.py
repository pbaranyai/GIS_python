# ---------------------------------------------------------------------------
# PortalItem_InventoryReport_Tool.py
# Created on: 2024-01-26
# Updated on: 2024-01-29
#
# Author: Phil Baranyai / GIS Analyst
#
# Description:
# Inventory all portal items within provided portal URL / Export out report into Microsoft Excel
#
#
# Works with Enterprise GIS & ArcGIS Online
#
#
# ---------------------------------------------------------------------------
print("This tool will load layers and applications (listed in script) from both portal sites (or AGOL if that URL is entered) entered below, then compare them, and export out an excel report to show what dependencies (if any) each layer has to a map/app.")
print("\nLoading python modules, please wait...")
from arcgis.gis import GIS
import pandas as pd
import os
import datetime
from openpyxl import load_workbook
import logging

# Comment out for manual run of script - Used for prompts within command window (Run with ArcGIS Pro)
print("Enter portal URL below: | Example: https://PORTALNAME.com/arcgis")
Portal = input('Enter URL here: ')
PortalUserName = input('Enter username for '+str(Portal)+'here: ')

# This can be used in leiu of CMD window, need to comment out CMD window portions of script at top and bottom, then un-comment out Portal variable here. 
#*********************************************************************************************************
##### Change portal address here  ##### 
#Portal = 'https://PORTALNAME.com/arcgis' <-- Used only for manual run of script
##### Change portal address here  #####

#*********************************************************************************************************

# Setup Date/time variables
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
logfile = LogDirectory + "\\PortalItemInventory_Reports_log.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
try:
    def write_log(text, file):
        f = open(file, 'a')           # 'a' will append to an existing file if it exists
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    print ("\n Unable to write log file")
    write_log("Unable to write log file", logfile)
    sys.exit ()

# Setup export path to *script location* PortalItemInventory_Reports folder
try:
    ReportDirectory = os.getcwd()+"\\PortalItemInventory_Reports"
    reportdirExists = os.path.exists(ReportDirectory)
    if not reportdirExists:
        os.makedirs(ReportDirectory)
        print(ReportDirectory+" was not found, so it was created")
        write_log(ReportDirectory+" was not found, so it was created",logfile)
except:
    print('\n Unable to establish PortalItemInventory_Reports folder within '+os.getcwd()+' folder')
    write_log('\n Unable to create PortalItemInventory_Reports folder within '+os.getcwd()+' folder',logfile)
    logging.exception('Got exception on create PortalItemInventory_Reports folder within '+os.getcwd()+' folder logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Confirm portal access was successful for Portal
try:
    for url in Portal:
        print("Attempting login on: "+str(url)+" | Password required for "+str(PortalUserName))
        gis = GIS(url,PortalUserName)
        LoggedInAs = gis.properties.user.username
        # Clean up Portal url for usable name in print statements and excel file name
        PortalName = Portal.replace('https://','',1).replace('.com/arcgis','',1)
        print("\nLogged into "+str(PortalName)+" as "+str(LoggedInAs)+" at "+str(Time)+" hrs, beginning report")
    else:
        print("Unable to login to "+str(Portal)+", check portal URL & password (if applicable) and try again, if portal URL is correct, ensure you have proper access via your login credentials")
except:
    print('\n Unable to establish connection to '+str(Portal))
    write_log('\n Unable to establish connection to '+str(Portal),logfile)
    logging.exception('Got exception on establish connection to '+str(Portal)+' logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()
# Set Excel spreadsheet output name
ExcelOutput = os.path.join(ReportDirectory,str(PortalName)+'__Item_Inventory_report__'+str(date)+"_"+str(Time)+'.xlsx')

# Grabbing Item Information (these item types will be reported and identified on the report)
print('\nCollecting Item types...')
write_log('\nCollecting Item Data...',logfile)

# Collect items from portal, in list call ItemList, also create empty list called PortalItems
ItemList = gis.content.search(query='NOT owner: esri*',item_type= '*',max_items=-1)
PortalItems = []

# Define item information fields, iterate through items in ItemList, append into PortalItems list as dictionary  
print('\n')  #<--just adds a carriage return for the on screen print statements for a cleaner look
for item in ItemList:
    try:
        # Item info
        item_info = item
        find_id = item_info.id
        find_url = gis.content.get(find_id).url
        item_title = item_info.title
        item_owner = item_info.owner
        item_type = item_info.type
        item_created = item_info.created
        item_created_formatted = datetime.datetime.fromtimestamp(item_created / 1000).strftime("%Y-%m-%d")
        item_modified = item_info.modified
        item_modified_formatted = datetime.datetime.fromtimestamp(item_modified / 1000).strftime("%Y-%m-%d")
        item_viewcount = item_info.numViews
        item_sharing = item_info.shared_with

        # If item has content status, write it into dictionary, if not, write N/A
        if hasattr(item, 'content_status'):
            item_status = item_info.content_status
        else:
            item_status = 'N/A'

        PortalItems.append({'Item Name': item_title,
                            'Item Type': item_type,
                            'Item ID': find_id,
                            'Item Url': find_url,
                            'Item Owner': item_owner,
                            'Item Status': item_status,
                            'Item Created Date': item_created_formatted,
                            'Item Last Modified Date': item_modified_formatted,
                            'Item Lifetime View Count': item_viewcount,
                            'Item Sharing Level': item_sharing})
        # Provides a visual indication on screen that it's working
        print("Captured: {} | {}".format(item_title,item_type))
                  
    except (AttributeError, KeyError) as e:
        print(f"Error capturing item: {e}")
        continue

    except Exception as e:
        print(f"Unexpected error capturing item: {e}")
        continue

# Provides final item count
print('\nYou have ' + str(len(PortalItems)) + ' items in '+Portal+' that have been inventoried.')
write_log('\nYou have ' + str(len(PortalItems)) + ' items in '+Portal+' that have been inventoried.',logfile)

# Create a dataframe from dictionary within PortalItems list
try:
    inventory_df = pd.DataFrame(PortalItems)

except:
    print('\n Unable to create dataframe from PortalItems list')
    write_log('\n Unable to create dataframe from PortalItems list',logfile)
    logging.exception('Got exception on create dataframe from PortalItems list logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()   

# Using dataframe masking, add URLs for items without URLs from portal.
WebMap_mask = inventory_df['Item Type'] == 'Web Map'
inventory_df.loc[WebMap_mask, 'Item Url'] = Portal+'/home/webmap/viewer.html?webmap='+ inventory_df['Item ID'].astype(str)
Form_mask = inventory_df['Item Type'] == 'Form'
inventory_df.loc[Form_mask, 'Item Url'] = 'https://survey123.arcgis.com/share/' + inventory_df['Item ID'].astype(str)+"?"+ Portal + '&open=native'
ExperienceBuilder_mask = inventory_df['Item Type'] == 'Web Experience'
inventory_df.loc[ExperienceBuilder_mask, 'Item Url'] = Portal+'/apps/experiencebuilder/experience/?id='+ inventory_df['Item ID'].astype(str)
Dashboard_mask = inventory_df['Item Type'] == 'Dashboard'
inventory_df.loc[Dashboard_mask, 'Item Url'] = Portal+'/apps/opsdashboard/index.html#/'+ inventory_df['Item ID'].astype(str)
WebScene_mask = inventory_df['Item Type'] == 'Web Scene'
inventory_df.loc[WebScene_mask, 'Item Url'] = Portal+'/home/webscene/viewer.html?webscene='+ inventory_df['Item ID'].astype(str)

# Sorting dataframe by Url
inventory_df1 = inventory_df.sort_values(by=['Item Name'], ascending=[True])
# Reindexing dataframe
inventory_df2 = inventory_df1.reset_index(drop=True)

# Creating the Final Dataframe to export to excel
try:
    new_inventory_df = inventory_df2.sort_index().reset_index(drop=True).iloc[:-1]
    print('\n    Finished Creating Data Frame')
    write_log('\n    Finished Creating Data Frame',logfile)
except:
    print('\n Unable to create dataframe')
    write_log('\n Unable to create dataframe',logfile)
    logging.exception('Got exception on create dataframe logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Exporting Dataframe to excel
try:
    print('\nExporting to Excel, located at: '+ExcelOutput)
    write_log('\nExporting to Excel, located at: '+ExcelOutput,logfile)
    new_inventory_df.to_excel(ExcelOutput, 'Items', index=False)
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

# Calculating run time and printing end statement
end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() -start_time
print("\nReporting process completed at " + str(end_time)+" taking "+time.strftime("%H hours %M minutes %S seconds", time.gmtime(elapsed_time)))
write_log("\nReporting process completed at " + str(end_time)+" taking "+time.strftime("%H hours %M minutes %S seconds", time.gmtime(elapsed_time)),logfile)
print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
write_log("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+",logfile)

# For command run, allows user to see all program print statements before closing the command window by pressing any key.
input("Press enter key to close program")
sys.exit()
