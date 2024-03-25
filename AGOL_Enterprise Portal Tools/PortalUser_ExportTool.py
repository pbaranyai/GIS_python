# ---------------------------------------------------------------------------
# PortalUser_ExportTool.py
# Created on: 2023-10-12
# Updated on: 2023-10-12
#
# Author: Phil Baranyai
#
# Description:
# List all users in portal/AGOL and provide output list of details.
#
#
# Works with Enterprise GIS & ArcGIS Online
#
########  ----> Designed to be run from CMD line
########  ----> Right click on .py file and "Run with ArcGIS Pro"
#
#
# ---------------------------------------------------------------------------
print("This tool reads from portal URL entered below, lists all users and details, and exports out results an excel report.")
print("\nLoading python modules, please wait...")
from arcgis.gis import GIS
import pandas as pd
import os,time,sys
import datetime
from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidationList
import logging

# Comment out for manual run of script - Used for prompts within command window (Run with ArcGIS Pro)
print("Enter portal URL below: | Example: https://PORTALNAME.com/arcgis")
print("\n  You MUST login with an administrator account to run this report")
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

# Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
try:
    def write_log(text, file):
        f = open(file, 'a')           # 'a' will append to an existing file if it exists
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    print ("\n Unable to write log file")
    sys.exit ()

# Setup export path to *script location* PortalGroupMembers_Reports folder
try:
    ReportDirectory = os.getcwd()+"\\PortalUsers_Reports"
    reportdirExists = os.path.exists(ReportDirectory)
    if not reportdirExists:
        os.makedirs(ReportDirectory)
        print(ReportDirectory+" was not found, so it was created")
except:
    print('\n Unable to establish PortalUsers_Reports folder within '+os.getcwd()+' folder')
    raise
    sys.exit()

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
logfile = LogDirectory + "\\PortalUsers_Export_Reports_log.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Setup export path to *script location* PortalGroupMembers_Reports folder
try:
    ReportDirectory = os.getcwd()+"\\PortalUsers_Reports"
    reportdirExists = os.path.exists(ReportDirectory)
    if not reportdirExists:
        os.makedirs(ReportDirectory)
        print(ReportDirectory+" was not found, so it was created")
except:
    print('\n Unable to establish PortalUsers_Reports folder within '+os.getcwd()+' folder')
    write_log('\n Unable to create PortalUsers_Reports folder within '+os.getcwd()+' folder',logfile)
    logging.exception('Got exception on create PortalUsers_Reports folder within '+os.getcwd()+' folder logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

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

# Establish a variable called portalusers (iterating through the established portal, and listing users)
portalusers = gis.users.search(max_users = 3000)

# Set Excel spreadsheet output name
ExcelOutput = os.path.join(ReportDirectory,str(PortalName)+'__Portal_User_Members_report__'+str(date)+"_"+str(Time)+'.xlsx')

# Create writer for dataframe to export to Excel
writer = pd.ExcelWriter(ExcelOutput)

# Create a pandas DataFrame to store the results
df = pd.DataFrame(columns=['Full Name', 'User Name', 'Email', 'Last Login Date', 'Role','Level','Description', 'Identity Provider','Group Membership'])
print('\n Creating dataframe with column headings')
write_log('\n Creating dataframe with column headings',logfile)

# Iterate through portal, establish variable called user (each user in portal), append results to dictionary
print("\n Iterating through portal to collect users and details")
write_log("\n Iterating through group to collect users and details",logfile)
    
# Create a dataframe with a list of users and descriptions, then save to excel.
for user in portalusers:
                      df = df.append({
                          'Full Name': user.fullName,
                          'User Name': user.username,
                          'Email': user.email,
                          'Last Login Date': user.lastLogin,
                          'Role': user.role,
                          'Level': user.level,
                          'Description': user.description,
                          'Identity Provider': user.provider,
                          'Group Membership': user.groups
                          }, ignore_index=True)
                      print(str(user.fullName)+' added to dataframe')
# Change level #s to readable values
df['Level'].replace('2', 'Creator',inplace=True)
df['Level'].replace('11', 'Field Worker', inplace = True)
df['Level'].replace('1', 'Viewer', inplace = True)
# Calculate from UNIX Epoch time value to readable time (calculate into new column, copy values to original column, remove new column)
df['Last Login - New']=(pd.to_datetime(df['Last Login Date'],unit='ms'))
df['Last Login Date'] = df['Last Login - New']
df = df.drop('Last Login - New',axis=1)
# New Last Login column is created at end of dataframe, reorganizing columns to original order
df = df.reindex(columns=['Full Name', 'User Name', 'Email', 'Last Login Date', 'Role','Level','Description', 'Identity Provider','Group Membership'])
df.sort_values('Full Name')
df.to_excel(writer, sheet_name='User List', index=False)
writer.save()

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
print("\n     Portal user report completed at " + str(end_time)+" taking "+time.strftime("%M minutes %S seconds", time.gmtime(elapsed_time)))
write_log("\n     Portal user report completed at " + str(end_time)+" taking "+time.strftime("%M minutes %S seconds", time.gmtime(elapsed_time)),logfile)
print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
write_log("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+",logfile)

# For command run, allows user to see all program print statements before closing the command window by pressing any key.
input("Press enter key to close program")
sys.exit()
