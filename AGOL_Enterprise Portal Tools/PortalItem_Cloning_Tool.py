# ---------------------------------------------------------------------------
# PortalItem_Cloning_Tool.py
# Created on: 2024-02-28
# Updated on: 2024-02-28
#
# Author: Phil Baranyai / GIS Analyst
#
# Description:
# Clone item(s) from one portal environment to another.  The following items can be cloned:
#
# + Hosted Web Applications built with WebAppBuilder or shared using Configuratable App Templates
# + Web maps
# + Hosted Feature Layers
# + Hosted Feature Layer Views
# + Feature Collections
# + Survey123 Forms
# + Workforce Projects
# + Story Maps
# + Operation Views
# + Dashboards
# + QuickCapture Projects
# + ArcGIS Notebooks
# + Simple Types (items with a download option)
#
#
# Works with Enterprise GIS & ArcGIS Online
#
#
# ---------------------------------------------------------------------------
print("This tool will clone ALL items (as provided by user entered IDs) from origin portal to target portal via URLs provided below.")
print("\nLoading python modules, please wait...")
from arcgis.gis import GIS
import os
import datetime
import logging

# For command window run, requests user imput for portal URL
print("Enter portal URL below: | Example: https://PORTALNAME.com/arcgis")
Portal = input('\nEnter Origin Portal URL: ')
Portal2 = input('Enter Target Portal URL: ')

# Enter Item ID(s) to clone from origin to target portal.   Apps will automatically bring maps and layers associated with them (maps/layers will need resourced
# requests user input for portal item ID(s)
print("\nEnter portal item(s) ID in below, for multiple items, separate by commas: | Example: 9a430848d1ef4c04b68c357673f732c3,d7c4882bc98d410cb216fda8927dd6a0")
ItemsToClone = input('\nEnter item(s) ID, if multiple items, separate each item with a comma: ')
ItemsToCloneList = ItemsToClone.split(",")

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
logfile = LogDirectory + "\\PortalItem_Clone_Report_log.log"
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

# Confirm portal access was successful for Portal 1
try:
    for url in Portal:
        print("Attempting login on: "+str(url)+" | Password required for "+str(PortalUserName))
        gis = GIS(url,PortalUserName)
        LoggedInAs = gis.properties.user.username
        # Clean up Portal url for usable name in print statements and excel file name
        PortalName = Portal.replace('https://','',1).replace('.com/arcgis','',1)
        print("\nLogged into "+str(PortalName)+" as "+str(LoggedInAs)+" at "+str(Time)+" hrs, beginning report")
        write_log("\nLogged into "+str(PortalName)+" as "+str(LoggedInAs)+" at "+str(Time)+" hrs, beginning report",logfile)
    else:
        print("Unable to login to "+str(Portal)+", check portal URL & password (if applicable) and try again, if portal URL is correct, ensure you have proper access via your login credentials")
except:
    print('\n Unable to establish connection to '+str(Portal))
    write_log('\n Unable to establish connection to '+str(Portal),logfile)
    logging.exception('Got exception on establish connection to '+str(Portal)+' logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()
    
# Confirm portal access was successful for Portal 2
try:
    for url2 in Portal2:
        print("Attempting login on: "+str(url2)+" | Password required for "+str(Portal2UserName))
        gis2 = GIS(url2,Portal2UserName)
        LoggedInAs = gis2.properties.user.username
        # Clean up Portal url for usable name in print statements and excel file name
        Portal2Name = Portal2.replace('https://','',1).replace('.com/arcgis','',1)
        print("\nLogged into "+str(Portal2Name)+" as "+str(LoggedInAs)+" at "+str(Time)+" hrs, beginning report")
        write_log("\nLogged into "+str(Portal2Name)+" as "+str(LoggedInAs)+" at "+str(Time)+" hrs, beginning report",logfile)
    else:
        print("Unable to login to "+str(Portal2)+", check portal URL & password (if applicable) and try again, if portal URL is correct, ensure you have proper access via your login credentials")
except:
    print('\n Unable to establish connection to '+str(Portal2))
    write_log('\n Unable to establish connection to '+str(Portal2),logfile)
    logging.exception('Got exception on establish connection to '+str(Portal2)+' logged at:' + time.strftime("%I:%M:%S %p", time.localtime()))
    raise
    sys.exit()

# Grabbing Item Information (these item types will be reported and identified on the report)
print('\nCollecting Items from provided IDs...')
write_log('\nCollecting Item from provide IDs...',logfile)

# Collect items from portal, in list call ItemList, also create empty list called PortalItems
for pitem in ItemsToCloneList:
    try:
        ItemList = gis.content.search(pitem)
        for citem in ItemList:
            print('\nCurrently Cloning: ',citem.title,' | ',citem.type,' from ',PortalName,' to ',Portal2Name)
            gis2.content.clone_items(ItemList, copy_data=False,search_existing_items=True, folder = 'Cloned from '+PortalName)
            print('Successfully Cloned: ',citem.title,' | ',citem.type,' from ',PortalName,' to ',Portal2Name)
    except Exception as e:
            print(f"Unexpected error cloning item: {e}")
            continue

# Calculating run time and printing end statement
end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() -start_time
print("\nCloning process completed at " + str(end_time)+" taking "+time.strftime("%H hours %M minutes %S seconds", time.gmtime(elapsed_time)))
write_log("\nCloning process completed at " + str(end_time)+" taking "+time.strftime("%H hours %M minutes %S seconds", time.gmtime(elapsed_time)),logfile)
print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
write_log("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+",logfile)

# For command run, allows user to see all program print statements before closing the command window by pressing any key.
input("Press enter key to close program")
sys.exit()

