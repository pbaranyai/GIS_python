# ---------------------------------------------------------------------------
# Portal_Group_Items_Report.py
# Created on: 2023-10-09
# Updated on: 2023-10-11
#
# Author: Phil Baranyai / DLC
#
# Description:
# Provides excel export report of all items within each group in portal/AGOL
#
#
# Works with Enterprise GIS & ArcGIS Online
#
########  ----> Designed to be run from CMD line
########  ----> Right click on .py file and "Run with ArcGIS Pro"
#
# ---------------------------------------------------------------------------

print("This tool will catalog all items (listed in script) within each group from portal site (or AGOL if that URL is entered) entered below, then export them to Microsoft Excel.")
print("\nLoading python modules, please wait...")

from arcgis.gis import GIS
import pandas as pd
import os,time,sys
import datetime
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidationList
import logging

print("Enter Portal or AGOL URL below: | Example: https://ORGANIZATIONALURL/arcgis")
print("\n  You MUST login with an administrator account to run this report")
Portal = input('Enter Portal or AGOL URL: ')

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
logfile = LogDirectory + "\\Portal_Group_Items_Report.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
try:
    def write_log(text, file):
        f = open(file, 'a')           # 'a' will append to an existing file if it exists
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    print ("\n Unable to write log file")
    sys.exit ()

# Setup export path to *script location* PortalDependencies_Reports folder
try:
    ReportDirectory = os.getcwd()+"\\Portal_Group_Items_Reports"
    reportdirExists = os.path.exists(ReportDirectory)
    if not reportdirExists:
        os.makedirs(ReportDirectory)
        print(ReportDirectory+" was not found, so it was created")
        write_log(ReportDirectory+" was not found, so it was created",logfile)
except:
    print('\n Unable to establish Portal_Group_Items_Reports folder within '+os.getcwd()+' folder')
    write_log('\n Unable to create Portal_Group_Items_Reports folder within '+os.getcwd()+' folder',logfile)
    logging.exception('Got exception on create Portal_Group_Items_Reports folder within '+os.getcwd()+' folder logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Login to portal, use token as "gis variable"
gis = GIS(Portal,UserName,Password)
PortalName = Portal.replace('https://','',1).replace('.com/arcgis','',1)
print("\nLogged into "+str(PortalName)+" as "+str(LoggedInAs)+" at "+str(Time)+" hrs, beginning report")
write_log("\nLogged into "+str(PortalName)+" as "+str(LoggedInAs)+" at "+str(Time)+" hrs, beginning report",logfile)

# Set Excel spreadsheet output name
ExcelOutput = os.path.join(ReportDirectory,str(PortalName)+'_GroupItems'+str(date)+"_"+str(Time)+'.xlsx')

# Get the portal groups into a list called "groups"
groups = gis.groups.search()

# Create writer for dataframe to export to Excel
writer = pd.ExcelWriter(ExcelOutput)

# Build fuction to add "Click here to open URL" in excel spreadsheet
def make_hyperlink(url):
    return '=HYPERLINK("%s", "Click here to open URL")' % url

# Build fuction to iterate over a single portal group, create a dataframe dictionary of items and add the item dictionary to the excel; with each group as it's own worksheet in the workbook. 
def build_group_df(groupname):
    # Get the group items
    items = groupname.content()
    # Create a pandas DataFrame to store the results
    df = pd.DataFrame(columns=['Group Name', 'Title', 'Item ID', 'Type','Sharing Level', 'URL','Link to Item'])
    print('\n Creating dataframe for '+str(groupname.title)+' group')
    write_log('\n Creating dataframe for '+str(groupname.title)+' group',logfile)
    
    # Add the items to the DataFrame
    for item in items:
        item_info = item
        find_id = item_info.id
        find_url = gis.content.get(item.id).url
        if(find_url):
            df = df.append({
                'Group Name': groupname.title,
                'Title': item.title,
                'Item ID': item.id,
                'Type': item.type,
                'Sharing Level': item.shared_with,
                'URL': find_url
            }, ignore_index=True)
            GroupName = (groupname.title).replace(" ","")[:30]
            df['Link to Item'] = df['URL'].apply(make_hyperlink)
            # Build masks to create custom URLs where the URL is not available from the item description in your portal/AGOL
            WebMap_mask = df['Type'] == 'Web Map'
            df.loc[WebMap_mask, 'URL'] = Portal+'/home/webmap/viewer.html?webmap='+ df['Item ID'].astype(str)
            Form_mask = df['Type'] == 'Form'
            df.loc[Form_mask, 'URL'] = 'https://survey123.arcgis.com/share/' + df['Item ID'].astype(str)+"?"+ Portal + '&open=native'
            ExperienceBuilder_mask = df['Type'] == 'Web Experience'
            df.loc[ExperienceBuilder_mask, 'URL'] = Portal+'/apps/experiencebuilder/experience/?id='+ df['Item ID'].astype(str)
            Dashboard_mask = df['Type'] == 'Dashboard'
            df.loc[Dashboard_mask, 'URL'] = Portal+'/apps/opsdashboard/index.html#/'+ df['Item ID'].astype(str)
            WebScene_mask = df['Type'] == 'Web Scene'
            df.loc[WebScene_mask, 'URL'] = Portal+'/home/webscene/viewer.html?webscene='+ df['Item ID'].astype(str)
            No_URL_Other_mask = df['URL'] == 'N/A'
            df.loc[No_URL_Other_mask, 'Link to Item'] = 'N/A'
        else:
            df = df.append({
                'Group Name': groupname.title,
                'Title': item.title,
                'Item ID': item.id,
                'Type': item.type,
                'URL': 'N/A',
                'Link to Item': 'N/A'
            }, ignore_index=True)
            GroupName = (groupname.title).replace(" ","")[:30]
        df.to_excel(writer, sheet_name=GroupName, index=False)
        print(str(groupname.title+' : '+item.title)+' created')
        writer.save()
        
# Call function from above, iterating each group through function to append each group's items result to excel workbook
try:
    for group in groups:
        build_group_df(group)
    print('\n  Items have been inventoried and dataframe has been created and exported to excel')
    write_log('\n  Items have been inventoried and dataframe has been created and exported to excel',logfile)
except:
    print('\n Unable to iterate through group and append each dictionary into the dataframe')
    write_log('\n Unable to iterate through group and append each dictionary into the dataframe',logfile)
    logging.exception('Got exception on iterate through group and append each dictionary into the dataframe logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
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
            sheet.data_validations = DataValidationList()
            sheet.auto_filter.ref = sheet.dimensions
    wb.save(ExcelOutput)
    print('\n    Report exported out to: '+ExcelOutput)
    write_log('\n    Report exported out to: '+ExcelOutput,logfile)
except:
    print('\n Unable to resize excel columns to fit data')
    write_log('\n Unable to resize excel columns to fit data',logfile)
    logging.exception('Got exception on resize excel columns to fit data logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Calculating run time and printing end statement
end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() -start_time
print("\n     Portal Group Items Report completed at " + str(end_time)+" taking "+time.strftime("%H hours %M minutes %S seconds", time.gmtime(elapsed_time)))
write_log("\n     Portal Group Items Report completed at " + str(end_time)+" taking "+time.strftime("%H hours %M minutes %S seconds", time.gmtime(elapsed_time)),logfile)
print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
write_log("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+",logfile)


# Allows user to view command window before closing
input("Press enter key to close program")
sys.exit()
