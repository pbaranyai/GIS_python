#######################################################
#
# PortalItem_Dependancies_FullPortal.py --  STILL EDITING
# Will find a list of web maps and/or web applications where the referenced 
# layer is contained within a web map and/or a web mapping application
#
# Works with Enterprise GIS & ArcGIS Online
#
# Created 2023-03-27 // Phil Baranyai
#
# Works with:
# Map Image/Feature Layers
# Tables
# GP Tools
# Locators
# Tile Layers
#
#######################################################

from arcgis.gis import GIS
import pandas as pd
import os
import datetime

#*********************************************************************************************************
##### Change portal address here  #####
Portal = "PORTAL URL GOES HERE"
##### Change portal address here  #####

#*********************************************************************************************************

# Uncomment for CMD run
##print("Enter portal URL below")
##Portal = input()

# Setup Date/time variables
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%Y-%m-%d", time.localtime())
Time = time.strftime("%H%M", time.localtime())
start_time = time.time()
elapsed_time = time.time() - start_time


print("Begining reporting process at "+str(Day)+" "+str(Time))


# Confirm portal access was successful
try:
    gis = GIS(Portal)
    print("\nLogged into "+str(Portal))
except:
    print("Unable to login to "+str(Portal)+", check portal URL and try again, if portal URL is correct, ensure you have proper access via your login credentials")


# Setup export path to user's documents folder
userprofile = os.environ['USERPROFILE']
ReportDirectory = userprofile+"\\Documents\\PortalDependancies"
reportdirExists = os.path.exists(ReportDirectory)
if not reportdirExists:
    os.makedirs(ReportDirectory)
    print(ReportDirectory+" was not found, so it was created")
xlsexport = os.path.join(ReportDirectory,str(Portal[8:-21])+'__Dependancies_report__'+str(date)+"_"+str(Time)+'.xlsx')

# Data Frame Variable
DFrame = pd.DataFrame()

# Builds lists of portal item types and gets a count of each
# item type (for illustration of work to be done, displayed for end user)

FL = gis.content.search('',item_type='Feature Layer', max_items=-1)
FeatureLayers_result = len(FL)
print('\nThere are {} items in {} on {}'.format(FeatureLayers_result, 'Feature Layers',str(Portal[8:-21])))
IL = gis.content.search('',item_type='Tile', max_items=-1)
Imagery_result = len(IL)
print('There are {} items in {} on {}'.format(Imagery_result,'Imagery Services',str(Portal[8:-21])))
GCS = gis.content.search('',item_type='Geocoding Service', max_items=-1)
Locators_result = len(GCS)
print('There are {} items in {} on {}'.format(Locators_result,'Locator Services',str(Portal[8:-21])))
GPS = gis.content.search('',item_type='Geoprocessing Service', max_items=-1)
gpTools_result = len(GPS)
print('There are {} items in {} on {}'.format(gpTools_result,'Geoprocessing Tool Services',str(Portal[8:-21])))


# Search all web maps & apps in portal and make them a variable called "webmaps"
webmaps = gis.content.search('', item_type='Web Map%', max_items=-1)
webmaps_result = len(webmaps)
print('\nFrom the above content, checking against a total of {} web maps & web apps that were collected from {}'.format(webmaps_result, str(Portal[8:-21])))


# Search all web maps & apps in portal and make them a variable called "dashboards"
dashboards = gis.content.search('', item_type='Dashboard', max_items=-1)
dashboard_result = len(dashboards)
print('From the above content, checking against a total of {} dashboards that were collected from {}'.format(dashboard_result, str(Portal[8:-21])))

print("\nChecking web maps & apps for ID reference...")

# # Create empty item variable dictionaries and then iterate through data types collected above, break out each layer into individual item dictionaries
itemname_dict = {}
itemurl_dict = {}
itemowner_dict = {}
portalWMID_dict = {}
portalDBID_dict = {}

print("  Inventory all Feature Layers started at " + time.strftime("%I:%M:%S %p", time.localtime()))
for i in FL:
    URL = gis.content.get(i.id).url
    itemname_dict[i.id] = []
    itemurl_dict[i.id] = []
    itemowner_dict[i.id] = []
    portalWMID_dict[i.id] = []
    portalDBID_dict[i.id] = []
    itemname_dict[i.id].append(i.title)
    itemurl_dict[i.id].append(URL)
    itemowner_dict[i.id].append(i.owner)
print("  Inventory all Imagery Services started at " + time.strftime("%I:%M:%S %p", time.localtime()))
for i in IL:
    URL = gis.content.get(i.id).url
    itemname_dict[i.id] = []
    itemurl_dict[i.id] = []
    itemowner_dict[i.id] = []
    portalWMID_dict[i.id] = []
    portalDBID_dict[i.id] = []
    itemname_dict[i.id].append(i.title)
    itemurl_dict[i.id].append(URL)
    itemowner_dict[i.id].append(i.owner)
print("  Inventory all Locator Services started at " + time.strftime("%I:%M:%S %p", time.localtime()))
for i in GCS:
    URL = gis.content.get(i.id).url
    itemname_dict[i.id] = []
    itemurl_dict[i.id] = []
    itemowner_dict[i.id] = []
    portalWMID_dict[i.id] = []
    portalDBID_dict[i.id] = []
    itemname_dict[i.id].append(i.title)
    itemurl_dict[i.id].append(URL)
    itemowner_dict[i.id].append(i.owner)
print("  Inventory all Geoprocessing Tool Services started at " + time.strftime("%I:%M:%S %p", time.localtime()))
for i in GPS:
    URL = gis.content.get(i.id).url
    itemname_dict[i.id] = []
    itemurl_dict[i.id] = []
    itemowner_dict[i.id] = []
    portalWMID_dict[i.id] = []
    portalDBID_dict[i.id] = []
    itemname_dict[i.id].append(i.title)
    itemurl_dict[i.id].append(URL)
    itemowner_dict[i.id].append(i.owner)


    print("\nFinding web map/web app/dashboard matches at " + time.strftime("%I:%M:%S %p", time.localtime()))
    # Return subset of map IDs which contain the service URL we're looking for
    matches = [m.id for m in webmaps if str(m.get_data()).find(URL) > -1]

    # Return subset of map URLs which contain the service URL we're looking for
    dmatches = [dm.id for dm in dashboards if str(dm.get_data()).find(URL) > -1]

    # Ensure records with no id are not appended.
    if len(matches) > 0:
        portalWMID_dict.update({i.id:matches})
    if len(dmatches) > 0:
        portalWMID_dict.update({i.id:matches})
    else:
        pass

    # Check each web map/app for matches
    for w in webmaps:
    
        try:
            # Get the JSON as a string
            wdata = str(w.get_data())

            criteria = [
                wdata.find(URL) > -1, # Check if URL is directly referenced
                any([wdata.find(i) > -1 for i in matches]) # Check if any matching maps are in app
            ]
            print("Checking for matches with "+str(i.title))
            # If layer is referenced directly or indirectly, append app to list
            if any(criteria):
                portalWMID_dict[i.id].append(w.id)
                URL = gis.content.get(w.id).url
                itemname_dict[w.id].append(w.title)
                itemurl_dict[w.id].append(URL)
                itemowner_dict[w.id].append(w.owner)
                print("Webmap matches found...appended to list")
    
        # Some maps don't have data, so we'll just skip them if they throw a TypeError
        except:
            print("\nNo Web map / Web App matches occur")
            continue
    

    # Check each web app for matches
    for d in dashboards:
    
        try:
            # Get the JSON as a string
            ddata = str(d.get_data())

            criteria = [
                ddata.find(URL) > -1, # Check if URL is directly referenced
                any([ddata.find(i) > -1 for i in dmatches]) # Check if any matching maps are in app
            ]
            print("Checking for matches with "+str(i.title))
            # If layer is referenced directly or indirectly, append app to list
            if any(criteria):
                portalDBID_dict[i.id].append(m.id)
                URL = gis.content.get(w.id).url
                itemname_dict[w.id].append(w.title)
                itemurl_dict[w.id].append(URL)
                itemowner_dict[w.id].append(w.owner)
                print("Dashboard matches found...appended to list")
    
        # Some apps don't have data, so we'll just skip them if they throw a TypeError
        except:
            print("\nNo dashboard matches occur")
            continue

    print("Creating results dataframe for "+URL+" at " + time.strftime("%I:%M:%S %p", time.localtime()))

# Populating dataframe columns and rows
    DFrame['Item ID'] = itemname_dict.keys()
    DFrame['Item Name'] = itemname_dict.values()
    DFrame['Item URL'] = itemurl_dict.values()
    DFrame['Item Owner'] = itemowner_dict.values()

    
# Exporting to Microsoft Excel
print("Begining excel export at " + time.strftime("%I:%M:%S %p", time.localtime()))
DFrame.to_excel(xlsexport)
print("Report output located at: "+xlsexport)


end_time = time.strftime("%I:%M:%S %p", time.localtime())
print("Reporting process completed at " + str(end_time))

# Uncomment for CMD run
##input("Press any key to close program")
##sys.exit()
