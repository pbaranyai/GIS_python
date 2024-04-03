# ---------------------------------------------------------------------------
# Enterprise_ServerManager_Service_Restart.py
# Created on: 2024-04-03
# Updated on: 2024-04-03
#
# Author: Phil Baranyai
#
# Description:
# List all services in given portal URL, stops and re-starts services.
#
#
# Works with Enterprise GIS
#
########  ----> Designed to be run from CMD line
########  ----> Right click on .py file and "Run with ArcGIS Pro"
#
#
# ---------------------------------------------------------------------------

print("This tool reads from portal URL entered below, stops and restarts services.")
print("\nLoading python modules, please wait...")
from arcgis.gis import GIS
import os,time,sys
import datetime
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

# Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
try:
    def write_log(text, file):
        f = open(file, 'a')           # 'a' will append to an existing file if it exists
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    print ("\n Unable to write log file")
    sys.exit ()

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
logfile = LogDirectory + "\\ServerManager_Service_Restart_log.log"
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Login to portal, use token as "gis variable"
gis = GIS(Portal)
PortalName = Portal.replace('https://','',1).replace('.com/arcgis','',1)
print("\nLogged into "+str(PortalName)+" at "+str(Time)+" hrs, beginning report")
write_log("\nLogged into "+str(PortalName)+" at "+str(Time)+" hrs, beginning report",logfile)

# Establish hosting server from portal URL
hosting_server = gis.admin.servers.list()

# Establish admin variable
admin = hosting_server[0].content.admin

#Create empty lists for folders and items
folderlist = []
servicesList = []

# Establish service variable
svcs = admin.services

# Establish folderDetails variable
folderDetails = svcs.foldersDetail

# Iterate through folders list and add to folderlist, then add in root folder
for fldr in folderDetails:
	folderlist.append(fldr.get("folderName"))
folderlist.append("/")

# Iterate through folders in folderlist, read services from each folder (incl root) and append to servicesList
for folder in folderlist:
    service = svcs.list(folder) # <-- uses all folders in server manager
##    service = svcs.list(folder = 'Hosted')  # <---specific folders can be chosen instead of ALL folders
    for iservice in service:
        servicesList.append(iservice)

# Iterate through items added to servicesList and restart or print each item
for item in servicesList:
    print(item)
##for item in servicesList:
##	item.restart()
##  	item.restart('<Service at https://PORTALMANAGERSITE.com:6443/arcgis/admin/services/SampleWorldCities.MapServer>') # <-- A specfic item can restarted instead of ALL items

# Calculating run time and printing end statement
end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() -start_time
print("\n     Portal service restart completed at " + str(end_time)+" taking "+time.strftime("%M minutes %S seconds", time.gmtime(elapsed_time)))
write_log("\n     Portal service restart completed at " + str(end_time)+" taking "+time.strftime("%M minutes %S seconds", time.gmtime(elapsed_time)),logfile)
print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
write_log("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+",logfile)

# For command run, allows user to see all program print statements before closing the command window by pressing any key.
input("Press enter key to close program")
sys.exit()
