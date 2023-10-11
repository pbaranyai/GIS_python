# ---------------------------------------------------------------------------
# PortalGroupMembers_ExportTool.py
# Created on: 2023-05-25
# Updated on: 2023-10-11
#
# Author: Phil Baranyai/DLC
#
# Description:
# List all groups in portal/AGOL and provide output list of groups and members within.
#
#
# Works with Enterprise GIS & ArcGIS Online
#
########  ----> Designed to be run from CMD line
########  ----> Right click on .py file and "Run with ArcGIS Pro"
#
#
# ---------------------------------------------------------------------------
print("This tool reads from portal URL entered below, lists all groups and members within by username, and export out results an excel report.")
print("\nLoading python modules, please wait...")
from arcgis.gis import GIS
import pandas as pd
import os
import datetime
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidationList
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
logfile = LogDirectory + "\\PortalGroupMembers_Export_Reports_log.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Setup export path to *script location* PortalGroupMembers_Reports folder
try:
    ReportDirectory = os.getcwd()+"\\PortalGroupMembers_Reports"
    reportdirExists = os.path.exists(ReportDirectory)
    if not reportdirExists:
        os.makedirs(ReportDirectory)
        print(ReportDirectory+" was not found, so it was created")
except:
    print('\n Unable to establish PortalGroupMembers_Reports folder within '+os.getcwd()+' folder')
    write_log('\n Unable to create PortalGroupMembers_Reports folder within '+os.getcwd()+' folder',logfile)
    logging.exception('Got exception on create PortalGroupMembers_Reports folder within '+os.getcwd()+' folder logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
try:
    def write_log(text, file):
        f = open(file, 'a')           # 'a' will append to an existing file if it exists
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    print ("\n Unable to write log file")
    sys.exit ()

# Confirm portal access was successful for Portal
for url in Portal:
    print("Attempting login on: "+str(url)+" | Password required for "+str(PortalUserName))
    gis = GIS(url,PortalUserName)
    LoggedInAs = gis.properties.user.username
    # Clean up Portal url for usable name in print statements and excel file name
    PortalName = Portal.replace('https://','',1).replace('.com/arcgis','',1)
    print("\nLogged into "+str(PortalName)+" as "+str(LoggedInAs)+" at "+str(Time)+" hrs, beginning report")
else:
    print("Unable to login to "+str(Portal)+", check portal URL & password (if applicable) and try again, if portal URL is correct, ensure you have proper access via your login credentials")

#Create empty list to store group members within
group_members_list = []

# Establish a variable called groups (iterating through the established portal, and listing groups)
groups = gis.groups.search('*', max_groups=1000)

# Set Excel spreadsheet output name
ExcelOutput = os.path.join(ReportDirectory,str(PortalName)+'__Portal_Group_Members_report__'+str(date)+"_"+str(Time)+'.xlsx')

# Create writer for dataframe to export to Excel
writer = pd.ExcelWriter(ExcelOutput)

# Create a pandas DataFrame to store the results
df = pd.DataFrame(columns=['Group Name', 'Group Owner', 'Member Username'])
print('\n Creating dataframe with column headings')
write_log('\n Creating dataframe with column headings',logfile)


# Iterate through groups list, establish variable called groupMembers (users from each group), append results to dictionary
print("\n Iterating through group to collect group/user names")
write_log("\n Iterating through group to collect group/user names",logfile)
    

# Function to interate through each group and create a list, enter into dataframe, and write out to excel
def user_inventory(groupname):
    # Create a pandas DataFrame to store the results
    df = pd.DataFrame(columns=['Group Name', 'Group Owner', 'Member Username'])

    for member in groupMembers['users']:
        grpuser = gis.users.get(member)
        df = df.append({
            'Group Name':groupname.title,
            'Group Owner':groupname.owner,
            'Member Username':member
            }, ignore_index=True)
        GroupName = (groupname.title).replace(" ","")[:30]
        df.to_excel(writer, sheet_name=GroupName, index=False)
        print(str(groupname.title+' : '+member)+' created')
        writer.save()

# Call function from above, iterating each group through function to append each group's member list result to excel workbook
try:
    for group in groups:
        groupMembers = group.get_members()
        user_inventory(group)
    print('\n   Dataframe has been created with group members and exported to excel - spreadsheet cleanup is next')
    write_log('\n   Dataframe has been created with group members and exported to excel - spreadsheet cleanup is next',logfile)
except:
    print('\n Unable to iterate through group to collect group/user names')
    write_log('\n Unable to iterate through group to collect group/user names',logfile)
    logging.exception('Got exception on iterate through group to collect group/user names logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
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
print("\n     Group member report completed at " + str(end_time)+" taking "+time.strftime("%M minutes %S seconds", time.gmtime(elapsed_time)))
write_log("\n     Group member report completed at " + str(end_time)+" taking "+time.strftime("%M minutes %S seconds", time.gmtime(elapsed_time)),logfile)
print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
write_log("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+",logfile)

# For command run, allows user to see all program print statements before closing the command window by pressing any key.
input("Press enter key to close program")
sys.exit()
