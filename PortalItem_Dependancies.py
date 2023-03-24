#######################################################
#
# PortalItem_Dependancies.py
# Will find a list of web maps and/or web applications where the referenced 
# layer is contained within a web map and/or a web mapping application
#
# Works with Enterprise GIS & ArcGIS Online
#
# Created 2023-03-23 // Phil Baranyai
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

#*********************************************************************************************************

##### Change portal address here  #####  You may omit username and/or password and the script will prompt you
#  when run.  If you code your password here, it will be plain language and viewable by anyone with access to this script
gis = GIS('SERVER_URL_GOES_HERE', 'USERNAME_GOES_HERE', 'PASSWORD GOES HERE')
print("Logged into "+str(gis)+" portal")

##### Change URL of layer to search for (from bottom of content overview page) here #####
find_url = 'URL_OF_CONTENT_GOES_HERE'
print("Preparing to locate references to "+find_url)

#*********************************************************************************************************

# Pull list of all web maps in portal
webmaps = gis.content.search('', item_type='Web Map', max_items=-1)
print("Full list of webmaps collected")

# Return subset of map IDs which contain the service URL we're looking for
matches = [m.id for m in webmaps if str(m.get_data()).find(find_url) > -1]
print("Map IDs with layer matches collected")

# Pull list of all web apps in portal
webapps = gis.content.search('', item_type='Application', max_items=-1)
print("Full list of web apps collected")

# Create empty list to populate with results
app_list = []
print("Checking web maps & apps for URL reference...")

# Check each web map for matches
for w in webmaps:
    
    try:
        # Get the JSON as a string
        wdata = str(w.get_data())

        criteria = [
            wdata.find(find_url) > -1, # Check if URL is directly referenced
            any([wdata.find(i) > -1 for i in matches]) # Check if any matching maps are in app
        ]

        # If layer is referenced directly or indirectly, append app to list
        if any(criteria):
            app_list.append(w)
    
    # Some maps don't have data, so we'll just skip them if they throw a TypeError
    except:
        continue

# Check each web app for matches
for w in webapps:
    
    try:
        # Get the JSON as a string
        wdata = str(w.get_data())

        criteria = [
            wdata.find(find_url) > -1, # Check if URL is directly referenced
            any([wdata.find(i) > -1 for i in matches]) # Check if any matching maps are in app
        ]

        # If layer is referenced directly or indirectly, append app to list
        if any(criteria):
            app_list.append(w)
    
    # Some apps don't have data, so we'll just skip them if they throw a TypeError
    except:
        continue

output = pd.DataFrame([{'title':a.title, 'id':a.id, 'type':a.type} for a in app_list])
print(output)
