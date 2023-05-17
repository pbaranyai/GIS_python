# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# PortalItem_Dependencies_DualEnvironment_.py
# Created on: 2023-03-23
# Updated on: 2023-05-16
# Works in ArcGIS Pro
#
# Author: Andrew Parkin/GIS Manager with a lot of help and support of Phil Baranyai #SpatialAF
#
# Description:
# Will show FCs and all their dependencies across your enterprise or AGOL environments
#
#
# Works with Enterprise GIS & ArcGIS Online
#
#
# ---------------------------------------------------------------------------
print("This tool will will load layers and applications (listed in script) from both portal sites (or AGOL if that URL is entered) entered below, then compare them, and export out an excel report to show what dependencies (if any) each layer has to a map/app.")
print("\nLoading python modules, please wait...")
from arcgis.gis import GIS
import pandas as pd
import os
import datetime

### Comment out for manual run of script - Used for prompts within command window (Run with ArcGIS Pro)
print("Enter Portal/AGOL URLs below: | Example: https://PORTALNAME.com/arcgis")
Portal = input('Enter 1st URL: ')
PortalUserName = input('Enter username for '+str(Portal)+': ')
Portal2 = input('Enter 2nd URL: ')
Portal2UserName = input('Enter username for '+str(Portal2)+': ')

# This can be used in leiu of command window, need to comment out command window portions of script at top and bottom, then un-comment out Portal & Portal 2 variables here. 
#*********************************************************************************************************
##### Change portal address here  #####  
##Portal = 'https://PORTALNAME.com/arcgis'  # <-- Used only for manual run of script
##Portal2 = 'https://PORTALNAME.com/arcgis' # <-- Used only for manual run of script
##### Change portal address here  ##### 

#*********************************************************************************************************

# Setup Date/time variables
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%Y-%m-%d", time.localtime())
Time = time.strftime("%H%M", time.localtime())
start_time = time.time()
elapsed_time = time.time() - start_time

# Setup export path to user's documents folder
userprofile = os.environ['USERPROFILE']
ReportDirectory = userprofile+"\\Documents\\PortalDependencies"
reportdirExists = os.path.exists(ReportDirectory)
if not reportdirExists:
    os.makedirs(ReportDirectory)
    print(ReportDirectory+" was not found, so it was created")

# Confirm portal access was successful for Portal 1
for url in Portal:
    print("Attempting login on: "+str(url)+" | Password required for "+str(PortalUserName))
    gis = GIS(url,PortalUserName)
    LoggedInAs = gis.properties.user.username
    # Clean up Portal url for usable name in print statements and excel file name
    PortalName = Portal.replace('https://','',1).replace('.com/arcgis','',1)
    print("\nLogged into "+str(PortalName)+" as "+str(LoggedInAs)+" at "+str(Time)+" hrs, beginning report")
else:
    print("Unable to login to "+str(Portal)+", check portal URL & password (if applicable) and try again, if portal URL is correct, ensure you have proper access via your login credentials")

# Confirm portal access was successful for Portal 2
for url2 in Portal2:
    print("Attempting login on: "+str(url2)+" | Password required for "+str(Portal2UserName))
    gis2 = GIS(url2,Portal2UserName)
    LoggedInAs = gis2.properties.user.username
    # Clean up Portal url for usable name in print statements and excel file name
    Portal2Name = Portal2.replace('https://','',1).replace('.com/arcgis','',1)
    print("\nLogged into "+str(Portal2Name)+" as "+str(LoggedInAs)+" at "+str(Time)+" hrs, beginning report")
else:
    print("Unable to login to "+str(Portal2)+", check portal URL & password (if applicable) and try again, if portal URL is correct, ensure you have proper access via your login credentials")

# Set Excel spreadsheet output name
ExcelOutput = os.path.join(ReportDirectory,str(PortalName)+' - '+str(Portal2Name)+'__Dependencies_report__'+str(date)+"_"+str(Time)+'.xlsx')

# Gathering Item Information (these item types will be reported and identified on the report)
print('\nCollecting Item Data...')

ItemList = ['Administrative Report', 'Apache Parquet', 'CAD Drawing', 'CSV', 'Color Set', 'Content Category Set',
            'Document Link', 'Esri Classifier Definition', 'Export Package', 'Feature Collection',
            'Feature Collection Template', 'Feature Service', 'File Geodatabase', 'GeoJson', 'GML', 'GeoPackage',
            'Geocoding Service', 'Geodata Service', 'Geometry Service', 'Geoprocessing Service', 'Globe Service',
            'Image', 'KML', 'KML CollectionMap Service', 'Microsoft Excel', 'Microsoft Powerpoint',
            'Microsoft Word', 'Network Analysis Service', 'OGCFeatureServer', 'Oriented Imagery Catalog', 'PDF',
            'Relational Database Connection', 'Relational Database Connection', 'Report Template', 'SQLite Geodatabase',
            'Scene Service', 'Shapefile', 'Statistical Data Collection', 'StoryMap Theme',
            'Style', 'Symbol SetImage Service', 'Vector Tile Service', 'Visio Document', 'WFS', 'WMS', 'WMTS',
            'Workflow Manager Service', 'iWork Keynote', 'iWork Numbers', 'iWork Pages']



# Gathering Application Information (these application types will be reported and identified on the report)
AppList = ['360 VR Experience', 'AppBuilder Extension', 'AppBuilder Widget Package', 'CityEngine Web Scene',
           'Code Attachment', 'Dashboard', 'Deep Learning Studio Project', 'Esri Classification Schema',
           'Excalibur Imagery Project', 'Experience Builder Widget', 'Experience Builder Widget Package', 'Form',
           'GeoBIM Application', 'GeoBIM Project', 'Hub Event', 'Hub Initiative', 'Hub Initiative Template', 'Hub Page',
           'Hub Project', 'Hub Site Application', 'Insights Data Engineering Model',
           'Insights Data Engineering Workbook', 'Insights Model', 'Insights Page', 'Insights Theme',
           'Insights Workbook', 'Insights Workbook Package', 'Investigation', 'Mission', 'Mobile Application',
           'Native Application', 'Native Application Installer', 'Notebook', 'Notebook Code Snippet Library',
           'Operation View', 'Operations Dashboard Add In', 'Operations Dashboard Extension', 'Ortho Mapping Project',
           'Ortho Mapping Template', 'Pro Map', 'StoryMap', 'Web AppBuilder WidgetSolution', 'Web Experience',
           'Web Experience Template', 'Web Map', 'Web Mapping Application', 'Web Scene', 'Workforce Project']

# Creating empty lists for combining all Item/App types into a lists per type/portal
PortalItems = []
PortalApps = []
Portal2Items = []
Portal2Apps = []

# Creating empty list to store all gather_info function Results
FuncResults = []


# Defining function that will gather the information needed for comparison.
def gather_info(connection, connection_type, item, webapps):

    # For some reason script won't pull in certain Urls so try and except added to prevent script breaking.
    # If url cant be pulled it will still collect as much as the item info added.
    try:
        # Item info variables
        item_info = item
        find_id = item_info.id
        find_url = connection.content.get(find_id).url
        item_title = item_info.title
        item_owner = item_info.owner
        item_type = item_info.type

        # Collects Web maps then return subset of map IDs which contain the service URL we're looking for
        webmaps = connection.content.search(query='NOT owner: esri', item_type='Web Map', max_items=-1)
        matches = [m.id for m in webmaps if str(m.get_data()).find(find_url) > -1]

        # Create empty list to populate with results
        app_list = []

        # Check each web app for matches
        for w in webapps:

            try:
                # Get the JSON as a string
                wdata = str(w.get_data())

                criteria = [
                    wdata.find(find_url) > -1,  # Check if URL is directly referenced
                    any([wdata.find(m) > -1 for m in matches])  # Check if any matching maps are in app
                ]

                # If layer is referenced directly or indirectly, append app to list
                if any(criteria):
                    app_list.append(w)

            # Some apps don't have data, so skip them if they throw a TypeError
            except:
                continue

        if len(app_list) > 0:
            for a in app_list:
                FuncResults.append({'Environment': connection_type, 'Item Name': item_title, 'Item Type': item_type,
                                    'Item ID': find_id, 'Item Url': find_url, 'Item Owner': item_owner,
                                    'Application Name': a.title, 'Application Type': a.type, 'Application ID': a.id,
                                    'Application Owner': a.owner})

        if len(app_list) == 0:
            FuncResults.append({'Environment': connection_type, 'Item Name': item_title, 'Item Type': item_type,
                                'Item ID': find_id, 'Item Url': find_url, 'Item Owner': item_owner,
                                'Application Name': 'N/A', 'Application Type': 'N/A', 'Application ID': 'N/A',
                                'Application Owner': 'N/A'})

    except:
        print("Exception found gathering baseline item info.")
        item_info = item
        find_id = item_info.id
        item_title = item_info.title
        item_owner = item_info.owner
        item_type = item_info.type

        FuncResults.append({'Environment': connection_type, 'Item Name': item_title, 'Item Type': item_type,
                            'Item ID': find_id, 'Item Url': 'Cant find Url', 'Item Owner': item_owner,
                            'Application Name': 'N/A', 'Application Type': 'N/A', 'Application ID': 'N/A',
                            'Application Owner': 'N/A'})


# Assembling list of all items based off of defined types (and not owned by ESRI)
print('\nStarting Item inventory')
for i in ItemList:
    P1Temp = gis.content.search(query='NOT owner: esri',item_type=i,max_items=-1)
    P2Temp = gis2.content.search(query='NOT owner: esri',item_type=i,max_items=-1)
    if len(P1Temp) > 0:
        for P1i in P1Temp:
            PortalItems.append(P1i)
    if len(P2Temp) > 0:
        for P2i in P2Temp:
            Portal2Items.append(P2i)
print('\nYou have ' + str(len(PortalItems)) + ' items in '+Portal+'.' + ' You have ' + str(len(Portal2Items)) + ' items in '+Portal2+'.')
print('    Finished Items')

# Assembling list of all apps based off of defined types (and not owned by ESRI)
print('\nStarting App inventory')
for app in AppList:
    P1aTemp = gis.content.search(query='NOT owner: esri',item_type=app,max_items=-1)
    P2aTemp = gis2.content.search(query='NOT owner: esri',item_type=app,max_items=-1)
    if len(P1aTemp) > 0:
        for P1a in P1aTemp:
            PortalApps.append(P1a)
    if len(P2aTemp) > 0:
        for P2a in P2aTemp:
            Portal2Apps.append(P2a)
print('\nYou have ' + str(len(PortalApps)) + ' apps in '+Portal+'.' + ' You have ' + str(len(Portal2Apps)) + ' apps in '+Portal2+'.')
print('    Finished Apps')

# Running gather_info function through a loop for Portal
print('\n****Starting '+Portal+' Items')
for i in PortalItems:
    print('Working on ' + str(i.title))
    gather_info(gis, Portal, i, PortalApps)
print('    Finished '+Portal+' Items')

# Running gather_info function through a loop for Portal2
print('\n****Starting '+Portal2+' Items')
for i in Portal2Items:
    print('Working on ' + str(i.title))
    gather_info(gis2, Portal2, i, PortalApps)
print('    Finished '+Portal2+' Items')

# Creating a dataframe to organize the results
df = pd.DataFrame(FuncResults)
# # Sorting dataframe by Url and Environment name (portal urls)
df1 = df.sort_values(by=['Item Url', 'Environment'], ascending=[True,False])
# Reindexing dataframe
df2 = df1.reset_index(drop=True)

# Creating Mask that will put a line of separation between each Item
mask = df2['Item Url'].ne(df2['Item Url'].shift(-1))
df3 = pd.DataFrame('', index=mask.index[mask] + .5, columns=df.columns)

# Creating the Final Dataframe.
new_df = pd.concat([df2, df3]).sort_index().reset_index(drop=True).iloc[:-1]
print('\n    Finished Creating Data Frame')

print("+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
# Exporting Dataframe to excel
print('\nExporting to Excel, located at: '+ExcelOutput)
new_df.to_excel(ExcelOutput, index=False)

# Calculating run time and printing end statement
end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() -start_time
print("\nReporting process completed at " + str(end_time)+" taking "+time.strftime("%H hours %M minutes %S seconds", time.gmtime(elapsed_time)))

# For command run, allows user to see all program print statements before closing the command window by pressing enter key.
input("Press enter key to close program")
sys.exit()
