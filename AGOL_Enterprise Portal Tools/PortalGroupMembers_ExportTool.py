# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# PortalGroupMembers_ExportTool.py
# Created on: 2023-05-25
# Updated on: 2023-07-10
#
# Author: Phil Baranyai/DLC
#
# Description:
# List all groups in portal/AGOL and provide output list of groups and members within.
#
#
# Works with Enterprise GIS & ArcGIS Online
#
# ---------------------------------------------------------------------------
print("This tool reads from portal URL entered below, lists all groups and members within by username, and export out results an excel report.")
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

# Iterate through groups list, establish variable called groupMembers (users from each group), append results to dictionary
print("\n Iterating through group to collect group/user names")
write_log("\n Iterating through group to collect group/user names",logfile)
try:
    for group in groups:
        groupMembers = group.get_members()
        for member in groupMembers['users']:
            grpuser = gis.users.get(member)
            group_members_list.append({'Group Name':group.title,'Group Owner':group.owner,'Member Username':member})
except:
    print('\n Unable to iterate through group to collect group/user names')
    write_log('\n Unable to iterate through group to collect group/user names',logfile)
    logging.exception('Got exception on iterate through group to collect group/user names logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Create dataframe from dictionary entries
print("\n Creating and formating dataframe with group/user data")
write_log("\n Creating and formating dataframe with group/user data",logfile)
try:
    # Establishing group_members_list as dataframe
    predf = pd.DataFrame(group_members_list)
    # Sorting by Group Name
    srtdf = predf.sort_values(by=['Group Name'],ascending=[True])
    # Reindexing dataframe
    rstdf = srtdf.reset_index(drop=True)
    # Creating maskt hat adds line of separate between each Group Name
    mask = rstdf['Group Name'].ne(rstdf['Group Name'].shift(-1))
    coldf = pd.DataFrame('',index=mask.index[mask]+.5, columns = predf.columns)
    # Creating final version of dataframe for export
    df = pd.concat([rstdf,coldf]).sort_index().reset_index(drop=True).iloc[:-1]
except:
    print('\n Unable to assemble dataframe to structure data')
    write_log('\n Unable to assemble dataframe to structure data',logfile)
    logging.exception('Got exception on assemble dataframe to structure data logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Set Excel spreadsheet output name
ExcelOutput = os.path.join(ReportDirectory,str(PortalName)+'__Portal_Group_Members_report__'+str(date)+"_"+str(Time)+'.xlsx')

# Exporting Dataframe to excel
try:
    print('\nExporting to Excel, located at: '+ExcelOutput)
    write_log('\nExporting to Excel, located at: '+ExcelOutput,logfile)
    df.to_excel(ExcelOutput, 'Groups', index=False)
except:
    print('\n Unable to export dataframe to excel')
    write_log('\n Unable to export dataframe to excel',logfile)
    logging.exception('Got exception on export dataframe to excel logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Access exported excel workbook, and auto-size columns for easier read
try:
    print("\n Resizing excel columns to autofit columns")
    write_log("\n Resizing excel columns to autofit columns",logfile)
    wb = load_workbook(ExcelOutput)
    ws = wb['Groups']
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
print("\nReporting process completed at " + str(end_time)+" taking "+time.strftime("%M minutes %S seconds", time.gmtime(elapsed_time)))

# For command run, allows user to see all program print statements before closing the command window by pressing any key.
input("Press enter key to close program")
sys.exit()
