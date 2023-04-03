#######################################################
#
# PortalItem_Dependancies_FullPortal.py ( STILL EDITING - NOT WORKING)
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
Portal = "PORTAL URL"
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
    print("Unable to login to "+str(Portal)+", check portal URL and try again")


# Setup export path to user's documents folder
userprofile = os.environ['USERPROFILE']
ReportDirectory = userprofile+"\\Documents\\PortalDependancies"
reportdirExists = os.path.exists(ReportDirectory)
if not reportdirExists:
    os.makedirs(ReportDirectory)
    print(ReportDirectory+" was not found, so it was created")
xlsexport = os.path.join(ReportDirectory,str(Portal[8:-21])+'__Dependancies_report__'+str(date)+"_"+str(Time)+'.xlsx')


# Establish reportable portal item types, then iterate through them and add to a list called "portalitems" 

itypes = ['Feature Service','Tile','Geocoding Service','Geoprocessing Service']

portalitems = []
for t in itypes:
    if t == 'Feature Service':
        portalitems.append(gis.content.search('',item_type='Feature Service', max_items=-1))
        FeatureServices_result = len(t)
        print('\nThere are {} items in {} on {}'.format(FeatureServices_result, 'Feature Services',str(Portal[8:-21])))
    if t == 'Tile':
        portalitems.append(gis.content.search('',item_type='Tile', max_items=-1))
        Imagery_result = len(t)
        print('There are {} items in {} on {}'.format(Imagery_result,'Imagery Services',str(Portal[8:-21])))
    if t == 'Geocoding Service':
        portalitems.append(gis.content.search('',item_type='Geocoding Service', max_items=-1))
        Locators_result = len(t)
        print('There are {} items in {} on {}'.format(Locators_result,'Locator Services',str(Portal[8:-21])))
    if t== 'Geoprocessing Service':
        portalitems.append(gis.content.search('',item_type='Geoprocessing Service', max_items=-1))
        gpTools_result = len(t)
        print('There are {} items in {} on {}'.format(gpTools_result,'Locator Services',str(Portal[8:-21])))       
        

    
# Search all web maps & apps in portal and make them a variable called "webmaps"
webmaps = gis.content.search('', item_type='Web Map%', max_items=-1)
webmaps_result = len(webmaps)
print('\nFrom the above content, checking against a total of {} web maps & web apps that were collected from {}'.format(webmaps_result, str(Portal[8:-21])))


# Search all web maps & apps in portal and make them a variable called "dashboards"
dashboards = gis.content.search('', item_type='Dashboard', max_items=-1)
dashboard_result = len(dashboards)
print('From the above content, checking against a total of {} dashboards that were collected from {}'.format(dashboard_result, str(Portal[8:-21])))

print("\nChecking web maps & apps for ID reference...")

# Create empty item variable lists and then iterate through data types collected above, break out each layer into individual item lists
itemname = []
itemid = []
itemurl = []
itemowner = []


for i in portalitems:
#    URL = gis.content.get(i.id).url
    itemname.append(i.title)
    itemid.append(i.id)
    itemurl.append(gis.content.get(i.id).url)
    itemowner.append(i.owner)
    print("Inventory all Portal Services completed at " + time.strftime("%I:%M:%S %p", time.localtime()))


    print("Finding web map/web app/dashboard matches at " + time.strftime("%I:%M:%S %p", time.localtime()))
    for URL in itemurl:
        # Return subset of map IDs which contain the service URL we're looking for
        matches = [m.id for m in webmaps if str(m.get_data()).find(URL) > -1]

        # Return subset of map URLs which contain the service URL we're looking for
        dmatches = [dm.id for dm in dashboards if str(dm.get_data()).find(URL) > -1]

        # Check each web map/app for matches
        for w in webmaps:
        
            try:
                # Get the JSON as a string
                wdata = str(w.get_data())

                criteria = [
                    wdata.find(URL) > -1, # Check if URL is directly referenced
                    any([wdata.find(i) > -1 for i in matches]) # Check if any matching maps are in app
                ]
                print("Checking for matches with "+str(item.title))
                # If layer is referenced directly or indirectly, append app to list
                if any(criteria):
                    itemid.append(itemname+" | "+URL)
                    itemid.append(w)
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
                print("Checking for matches with "+str(item.title))
                # If layer is referenced directly or indirectly, append app to list
                if any(criteria):
                    itemid.append(itemname+" | "+URL)
                    itemid.append(d)
                    print("Dashboard matches found...appended to list")
        
            # Some apps don't have data, so we'll just skip them if they throw a TypeError
            except:
                print("\nNo dashboard matches occur")
                continue

        print("Creating results dataframe for "+URL+" at " + time.strftime("%I:%M:%S %p", time.localtime()))
        output = pd.DataFrame([['Item Name',itemname], ['Item ID', itemid], ['Item URL',itemurl], ['Item Owner', itemowner]])
        pd.DataFrame([None,None,None, None])
print("Begining excel export at " + time.strftime("%I:%M:%S %p", time.localtime()))
pd.ExcelWriter(xlsexport)
print("Report output located at: "+xlsexport)
print(output)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
print("Reporting process completed at " + str(end_time))

# Uncomment for CMD run
##input("Press any key to close program")
##sys.exit()
