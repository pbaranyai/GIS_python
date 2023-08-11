# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# LandRecords_Data_Spreader.py
# Created on: 2020-10-19 
# Updated on 2021-09-21
# Works in ArcGIS Pro
#
# Author: Phil Baranyai/GIS Manager
#
# Description: 
#  Update the following FC from source data to CRAW_INTERNAL -> PUBLIC_WEB as needed:
#
# LANDUSE_PARCELS  
#
#   All processes have general components, delete rows, append from another source - due to most layers are connected to services
# ---------------------------------------------------------------------------

# Import modules
import sys
import arcpy
import datetime
import os
import traceback
import logging
import builtins

# Stop geoprocessing log history in metadata (stops program from filling up geoprocessing history in metadata with every run)
arcpy.SetLogHistory(False)

# Setup error logging (configure logging location, type, and filemode -- overwrite every run)
logfile = r"R:\\GIS\\GIS_LOGS\\LandUse_Data_Spreader.log"  
logging.basicConfig(filename= logfile, filemode='w', level=logging.DEBUG)

# Setup Date (and day/time)
date = datetime.date.today().strftime("%Y%m%d")
Day = time.strftime("%m-%d-%Y", time.localtime())
Time = time.strftime("%I:%M:%S %p", time.localtime())

try:
    # Write Logfile (define logfile write process, each step will append to the log, if program is started over, it will wipe the log and re-start fresh)
    def write_log(text, file):
        f = open(file, 'a')           # 'a' will append to an existing file if it exists
        f.write("{}\n".format(text))  # write the text to the logfile and move to next line
        return
except:
    print ("\n Unable to write log file")
    write_log("Unable to write log file", logfile)
    sys.exit ()

#Database Connection Folder
Database_Connections = r"\\CCFILE\\anybody\\GIS\\ArcAutomations\\Database_Connections"

# Database variables:
AUTO_WKSP = Database_Connections + "\\auto_workspace@ccsde.sde"
CRAW_INTERNAL = Database_Connections + "\\craw_internal@ccsde.sde"
PUBLIC_WEB = Database_Connections + "\\public_web@ccsde.sde"

# Local variables:
LANDUSE_PARCELS_WKSP = AUTO_WKSP + "\\CCSDE.AUTO_WORKSPACE.Planning\\CCSDE.AUTO_WORKSPACE.LANDUSE_PARCELS_WKSP"
LANDUSE_PARCELS_INTERNAL = CRAW_INTERNAL +"\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.LANDUSE_PARCELS_INTERNAL"
LANDUSE_PARCELS_WEB = PUBLIC_WEB + "\\CCSDE.PUBLIC_WEB.Land_Records\\CCSDE.PUBLIC_WEB.LANDUSE_PARCELS_WEB"
TAX_PARCELS_INTERNAL = CRAW_INTERNAL + "\\CCSDE.CRAW_INTERNAL.Land_Records\\CCSDE.CRAW_INTERNAL.TAX_PARCELS_INTERNAL"

start_time = time.time()

print ("============================================================================")
print (("Updating Land Records: "+ str(Day) + " " + str(Time)))
print ("Will update the following:")
print ("\nLand Use Parcels Feature Class")
print ("\n From source to CRAW_INTERNAL -> PUBLIC_WEB (where applicable)")
print ("Works in ArcGIS Pro")
print ("============================================================================")

write_log("============================================================================", logfile)
write_log("Updating Land Records: "+ str(Day) + " " + str(Time), logfile)
write_log("Will update the following:", logfile)
write_log("\nLand Use Parcels Feature Class", logfile)  

write_log("\n From source to CRAW_INTERNAL -> PUBLIC_WEB", logfile)
write_log("Works in ArcGIS Pro", logfile)
write_log("============================================================================", logfile)

print ("\n Updating Land Use Parcels - AUTO_WORKSPACE from Tax Parcels - CRAW_INTERNAL")
write_log("\n Updating Land Use Parcels - AUTO_WORKSPACE from Tax Parcels - CRAW_INTERNAL: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete rows from Land Use Parcels - AUTO WORKSPACE
    arcpy.DeleteRows_management(LANDUSE_PARCELS_WKSP)
except:
    print ("\n Unable to delete rows from Land Use Parcels - AUTO WORKSPACE")
    write_log("Unable to delete rows from Land Use Parcels - AUTO WORKSPACE", logfile)
    logging.exception('Got exception on delete rows from Land Use Parcels - AUTO WORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Append Land Use Parcels - AUTO WORKSPACE from Tax Parcels - CRAW_INTERNAL
    arcpy.Append_management(TAX_PARCELS_INTERNAL, LANDUSE_PARCELS_WKSP, "NO_TEST", 'CAMA_PIN "MBLU (Map Block Lot Unit)" true true false 50 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',CAMA_PIN,-1,-1;SEC_MUNI_NAME "Municipal Name" true true false 50 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',SEC_MUNI_NAME,-1,-1;PID "PID Number" true true false 4 Long 0 10 ,First,#,'+TAX_PARCELS_INTERNAL+',PID,-1,-1;LND_USE_CODE "Assessment Land Use Code" true true false 4 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',LND_USE_CODE,-1,-1;LND_USE_DESC "Assessment Land Use Description" true true false 40 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',LND_DSTRCT,-1,-1;LAND_USE_CATEGORY "Planning Land Use Category" true true false 100 Text 0 0 ,First,#;LBCS_ACTIVITY "LBCS Activity Code" true true false 8 Double 8 38 ,First,#;LBCS_FUNCTION "LBCS Function" true true false 8 Double 8 38 ,First,#;LBCS_STRUCTURE "LBCS Structure Type" true true false 8 Double 8 38 ,First,#;LBCS_SITE_CHARACTER "LBCS site character" true true false 8 Double 8 38 ,First,#;LBCS_OWNERSHIP "LBCS Ownership" true true false 8 Double 8 38 ,First,#;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',SHAPE.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+TAX_PARCELS_INTERNAL+',SHAPE.STLength(),-1,-1', "")
    LU_Parcels_WKSP_result = arcpy.GetCount_management(LANDUSE_PARCELS_WKSP)
    print (('{} has {} records'.format(LANDUSE_PARCELS_WKSP, LU_Parcels_WKSP_result[0])))
    write_log('{} has {} records'.format(LANDUSE_PARCELS_WKSP, LU_Parcels_WKSP_result[0]), logfile)
except:
    print ("\n Unable to append Land Use Parcels - AUTO WORKSPACE from Tax Parcels - CRAW_INTERNAL")
    write_log("Unable to append Land Use Parcels - AUTO WORKSPACE from Tax Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Land Use Parcels - AUTO WORKSPACE from Tax Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Calculate Land Use Codes (Planning) from Land Use Codes (Assessment) - lines are grouped in 50 count 
    AST_LandUse = [None,"1050","1000","105A","102A","500A","180A","150A","151A","182A","100A","5000","1500","1820","1800","1510","1020","105B","102B","500B","150B","151B","182B","180B","100B","5200","5400","LLLL","MMMM","KKKK","JJJJ","I","4200","AAAA","0850","HH","098V","0989","098B","OO","4010","401B","YYY","4300","XXX","4000","4020","VVV","DDDD","4800",
                   "IIII","4700","9995","B","0100","010A","010B","010V","010C","010T","0453","0450","0350","0400","T","S","R","NN","M","025T","025V","025C","MM","0980","4100","ZZZ","0452","4310","EEEE","CCCC","4250","0960","KK","9300","RRRR","0900","090V","190V","1900","SSS","II","4200","FFFF","0202","J","3000","TTT","UUU","3020","0520",
                   "Z","0970","097V","LL","2000","1200","9150","1100","G","EEE","016B","DDD","FFF","9000","0999","NNNN","VV","0996","PP","0990","1070","1080","0998","0451","U","BB","0600","0800","0650","0550","CC","DD","GG","0750","FF","0700","EE","L","0500","X","013B","0300","O","AAA","BBB","YY","9100","OOOO","4210","A",
                   "WW","XX","1010","CCC","0210","0301","1600","1850","1830","1810","GGGG","OOO","III","HHH","MMM","QQQ","RRR","LLL","JJJ","NNN","PPP","0985","D","0150","015C","015V","C","0125","012B","012C","012V","4600","HHHH","0200","020B","020C","020T","020V","1060","4410","H","910V","ZZZZ","0151","0950","095V","JJ","095A","095B","095C",
                   "095E","SS","0302","Q","0995","0992","4400","020A","0201"]
    Planning_LandUse = ["To be determined","Dwelling, Attached","Dwelling, Detached","Dwelling, Attached","Farmstead","Farmstead","Farmstead","Homestead","Dwelling, Attached","Homestead","Dwelling, Detached","Farmstead","Homestead","Homestead","Farmstead","Dwelling, Attached","Farmstead","Dwelling, Attached","Farmstead","Farmstead","Homestead","Dwelling, Attached","Homestead","Farmstead","Homestead","Farmstead","Agricultural","Farmstead","Agricultural","Farmstead","Agricultural","Airport","Dwelling, Multifamily","Dwelling, Multifamily","Cemetery","Cemetery","Dwelling, Institutional","Dwelling, Institutional","Dwelling, Institutional","Dwelling, Institutional","Dwelling, Detached","Commercial","Commercial","Commercial","Commercial","Commercial","Commercial","Commercial","Commercial","Vacant land",
                        "Utility","Utility","Dwelling, Attached","To be determined","Dwelling, Detached","Dwelling, Detached","Dwelling, Detached","Vacant land","To be determined","Dwelling, Detached","Dwelling, Institutional","School","School","School","School","School","School","Social or civic organization","Nature conservation","To be determined","Vacant land","To be determined","Emergency services","Emergency services","Social or civic organization","Social or civic organization","Social or civic organization","Agricultural","Agricultural","Dwelling, Institutional","Dwelling, Institutional","To be determined","To be determined","Recreation or entertainment","Recreation or entertainment","Medical facility","Medical facility","Medical facility","Medical facility","Medical facility","Medical facility","Lodging","Lodging","Dwelling, Detached","Dwelling, Detached","Industrial","Industrial","Industrial","Industrial","Industrial",
                        "Industrial","Government or public services","Government or public services","Government or public services","Vacant land","Dwelling, Detached","Manufactured home park","Dwelling, Detached","To be determined","Dwelling, Detached","To be determined","Dwelling, Detached","Dwelling, Detached","To be determined","To be determined","To be determined","To be determined","Utility","To be determined","To be determined","To be determined","To be determined","To be determined","Dwelling, Detached","Dwelling, Detached","Utility","Utility","Railroad","Utility","Utility","Utility","Utility","Railroad","Utility","Utility","Utility","Utility","Railroad","Recreation or entertainment","Recreation or entertainment","Dwelling, Detached","Religious organization","Religious organization","Dwelling, Attached","Dwelling, Attached","Farmstead","Vacant land","Vacant land","Lodging","Dwelling, Detached",
                        "Dwelling, Detached","Dwelling, Detached","Homestead","Dwelling, Multifamily","Railroad","Social or civic organization","Homestead","Homestead","Vacant land","Vacant land","Lodging","Homestead","Dwelling, Attached","Dwelling, Detached","Farmstead","Homestead","Homestead","Dwelling, Detached","Dwelling, Detached","Vacant land","Vacant land","Social or civic organization","Government or public services","Dwelling, Detached","Nature conservation","Nature conservation","To be determined","Dwelling, Detached","Dwelling, Detached","To be determined","Vacant land","Recreation or entertainment","Recreation or entertainment","To be determined","To be determined","Government or public services","To be determined","Government or public services","Dwelling, Multifamily","Lodging","Government or public services","Vacant land","Vacant land","Industrial","Dwelling, Detached","Vacant land","Dwelling, Detached","Dwelling, Detached","Dwelling, Detached","To be determined",
                        "To be determined","Social or civic organization","Dwelling, Institutional","Dwelling, Institutional","Social or civic organization","Social or civic organization","Lodging","To be determined","Airport"]
    LBCS_Activity = ["9900","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","8000","1100","8000","1100","8000","5600","1100","1100","4600","4600","1300","1300","1300","1300","1100","2000","2000","2000","2000","2000","2000","2000","2000","9000",
                     "4340","4340","1100","9900","9900","9900","9900","9900","9900","9900","1300","4110","4110","4110","4110","4110","4110","6600","9900","9900","9000","9900","4210","4210","6600","6600","6600","8100","8100","1300","1300","9990","9900","7100","7100","4500","4500","4500","4500","4500","4500","1200","1200","1100","1100","3000","3000","3000","3000","3000",
                     "3000","4130","4130","4130","9000","1100","1100","1100","9900","1100","9900","1100","1100","9900","9900","9900","9900","4300","9900","9900","9900","9900","9900","1100","1100","4300","4300","4300","4300","4300","4300","4300","4300","4300","4300","4300","4300","5400","7000","7000","9900","6600","6600","1100","1100","1100","9000","9000","1200","1100",
                     "9900","1100","1100","1100","5400","6600","1100","1100","9000","9000","9900","1100","1100","1100","1100","1100","1100","1100","1100","9000","9000","6600","9900","1100","9900","9000","9900","9900","9900","9900","9000","7000","7000","9900","9900","9900","9900","9900","1100","1200","9900","9000","9000","3000","1100","9000","9900","1100","1100","9900",
                     "9900","6600","1300","1300","6600","6600","1200","9900","5600"]
    LBCS_Function = ["9990","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","1100","9000","1100","9000","1100","9000","4113","1100","1100","6720","6720","1230","1230","1230","1230","1100","2000","2000","2000","2000","2000","2000","2000","2000","9990",
                     "4233","4233","1100","9990","9990","9990","9990","9990","9990","9990","1300","6130","6120","6120","6130","6120","6120","6830","9990","9990","9990","9990","6410","6410","6830","6830","6830","9140","9140","1230","1230","9990","9990","9990","9990","6530","6530","6530","6530","6530","6530","1300","1300","1100","1100","3000","3000","3000","3000","3000",
                     "3000","6100","6100","6100","9990","1100","1100","1100","9990","1100","9990","1100","1100","9990","9990","9990","9990","4300","9990","9990","9990","9990","9990","1100","1100","4300","4300","4300","4300","4300","4300","4300","4300","4300","4300","4300","4300","4300","9990","9990","9990","6600","6600","1100","1100","1100","9990","9990","1300","1100",
                     "9990","1100","1100","1100","4300","6830","1100","1100","9990","9990","9990","1100","1100","1100","1100","1100","1100","1100","1100","9990","9990","6830","9990","1100","9990","9990","9990","9990","9990","9990","9990","9990","9990","9990","9990","9990","9990","9990","1100","1300","9990","9990","9990","3000","1100","9990","9990","1100","1100","9990",
                     "9990","6830","1200","1200","6830","6830","1300","9990","4113"]
    LBCS_Structure = ["9900","1121","1110","1121","1110","1110","1110","1110","1121","1110","1110","1110","1110","1110","1110","1121","1110","1121","1110","1110","1110","1121","1110","1110","1110","1150","9000","1150","9000","1150","8000","5600","1200","1200","4700","4700","1300","1300","1300","1300","1110","2000","2000","2000","2000","2000","2000","2000","2000","9000",
                      "6000","6000","1120","9900","9900","9900","9900","9900","9900","9900","1320","4220","4210","4210","4220","4210","4210","9900","9900","9900","9000","9900","4510","4510","3800","3800","3800","8500","8500","1300","1300","9900","9900","9900","9900","4110","4110","4110","4110","4110","4110","1330","1330","1120","1120","2600","2600","2600","2600","2600",
                      "2600","4300","4300","4300","9000","1150","1150","1150","9900","1150","9900","1150","1150","9900","9900","9900","9900","6000","9900","9900","9900","9900","9900","1110","1110","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","5150","9900","9900","9900","3500","3500","1120","1121","1110","9000","9000","1330","1110",
                      "9900","1150","1150","1140","5150","9900","1150","1150","9000","9000","9900","1110","1121","1110","1110","1150","1150","1150","1150","9000","9000","9900","9900","1110","9900","9000","9900","9900","9900","9900","9000","9900","9900","9900","9900","9900","9900","9900","1140","1330","9900","9000","9000","2600","1110","9000","9900","1110","1110","9900",
                      "9900","9900","1300","1300","9900","9900","1330","9900","5600"]
    LBCS_Site = ["9900","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","3000","6000","3000","6000","3000","6000","6000","6000","5000","5000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","4000",
                 "5000","5000","6000","9900","9900","9900","9900","9900","9900","9900","6000","6000","6000","6000","6000","6000","6000","6000","9900","9900","1000","9900","6000","6000","6000","6000","6000","6000","6000","6000","6000","9900","9900","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000","6000",
                 "6000","6000","6000","6000","1000","6000","6000","6000","9900","6000","9900","6000","6000","9900","9900","9900","9900","6000","9900","9900","6000","6000","6000","6000","6000","5000","5000","5000","5000","5000","5000","5000","5000","5000","5000","5000","5000","5300","9900","9900","9900","6000","6000","6000","6000","6000","1000","1000","6000","6000",
                 "9900","6000","6000","6000","5300","6000","6000","6000","1000","1000","9900","6000","6000","6000","6000","6000","6000","6000","6000","1000","1000","6000","9900","6000","9900","1000","9900","9900","9900","9900","1000","9900","9900","9900","9900","9900","9900","9900","6000","6000","9900","1000","1000","6000","6000","1000","9900","6000","6000","9900",
                 "9900","6000","6000","6000","6000","6000","6000","9900","6000"]
    LBCS_Ownership = ["9900","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","5200","3000","3000","6400","6400","6200","6200","6200","6200","1000","8000","8000","8000","8000","8000","8000","8000","8000","1000",
                      "8000","8000","3000","4120","4120","4120","4120","4120","4120","4120","6100","6100","6100","6100","6100","6100","6100","6200","4300","9900","4300","4300","4100","4100","8000","8000","8000","1000","1000","9900","9900","9900","9900","1000","1000","6200","6200","8000","8000","8000","6200","1000","1000","4100","4100","1000","1000","1000","1000","1000",
                      "1000","4100","4100","4100","1000","1200","3000","1000","9900","1200","9900","1000","1000","9900","9900","9900","9900","4100","9900","9900","1000","1000","1000","6100","6100","9900","9900","9900","9900","9900","9900","9900","9900","9900","9900","9900","9900","2100","1000","1000","9900","6300","6300","3000","1000","1000","1000","1000","1000","1000",
                      "9900","1000","1000","1000","2100","6200","1000","1000","1000","1000","9900","1000","1000","1000","1000","1000","1000","1000","1000","1000","1000","6200","4200","4200","4200","4200","9900","9900","9900","9900","1000","1000","1000","4110","4110","4110","4110","4110","1000","1000","4110","1000","1000","1000","1000","1000","9900","1000","1000","9900",
                      "9900","6200","6300","6300","6200","6200","1000","4110","5200"]
       
    print ("\n Converting Assessment Land Use codes to Planning Land Use categories and LBCS codes")
    write_log("Converting Assessment Land Use codes to Planning Land Use categories and LBCS codes", logfile)
    with arcpy.da.UpdateCursor(LANDUSE_PARCELS_WKSP,['LND_USE_CODE','LAND_USE_CATEGORY','LBCS_ACTIVITY','LBCS_FUNCTION','LBCS_STRUCTURE','LBCS_SITE_CHARACTER','LBCS_OWNERSHIP','PID']) as cursor:
        for row in cursor:
            if row[0] in AST_LandUse:
                row[1] = Planning_LandUse[AST_LandUse.index(row[0])]
            if row[0] in AST_LandUse:
                row[2] = LBCS_Activity[AST_LandUse.index(row[0])]
            if row[0] in AST_LandUse:
                row[2] = LBCS_Activity[AST_LandUse.index(row[0])]
            if row[0] in AST_LandUse:
                row[2] = LBCS_Activity[AST_LandUse.index(row[0])]
            if row[0] in AST_LandUse:
                row[3] = LBCS_Function[AST_LandUse.index(row[0])]
            if row[0] in AST_LandUse:
                row[4] = LBCS_Structure[AST_LandUse.index(row[0])]
            if row[0] in AST_LandUse:
                row[5] = LBCS_Site[AST_LandUse.index(row[0])]
            if row[0] in AST_LandUse:
                row[6] = LBCS_Ownership[AST_LandUse.index(row[0])]                
            cursor.updateRow(row)
        del row 
        del cursor
except:
    print ("\n Unable to Convert Assessment Land Use codes to Planning Land Use categories and LBCS codes")
    write_log("Unable to Convert Assessment Land Use codes to Planning Land Use categories and LBCS codes", logfile)
    logging.exception('Got exception on Convert Assessment Land Use codes to Planning Land Use categories and LBCS codes logged at:'  + str(Day) + " " + str(Time))
    raise
    pass
    sys.exit ()

print ("\n  Converting Assessment Land Use codes to Planning Land Use categories and LBCS codes completed")
write_log(" Converting Assessment Land Use codes to Planning Land Use categories and LBCS codes completed", logfile)

print ("\n Updating Land Use Parcels - CRAW_INTERNAL from AUTO_WORKSPACE")
write_log("\n Updating Land Use Parcels - CRAW_INTERNAL from AUTO_WORKSPACE: " + str(Day) + " " + str(Time), logfile)
    
try:
    # Delete rows from Land Use Parcels - CRAW_INTERNAL
    arcpy.DeleteRows_management(LANDUSE_PARCELS_INTERNAL)
except:
    print ("\n Unable to delete rows from Land Use Parcels - CRAW_INTERNAL")
    write_log("Unable to delete rows from Land Use Parcels - CRAW_INTERNAL", logfile)
    logging.exception('Got exception on delete rows from Land Use Parcels - CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Append Land Use Parcels - CRAW_INTERNAL from Land Use Parcels - AUTO_WORKSPACE
    arcpy.Append_management(LANDUSE_PARCELS_WKSP, LANDUSE_PARCELS_INTERNAL, "NO_TEST", 'CAMA_PIN "MBLU (Map Block Lot Unit)" true true false 50 Text 0 0 ,First,#,'+LANDUSE_PARCELS_WKSP+',CAMA_PIN,-1,-1;SEC_MUNI_NAME "Municipal Name" true true false 50 Text 0 0 ,First,#,'+LANDUSE_PARCELS_WKSP+',SEC_MUNI_NAME,-1,-1;PID "PID Number" true true false 4 Long 0 10 ,First,#,'+LANDUSE_PARCELS_WKSP+',PID,-1,-1;LND_USE_CODE "Assessment Land Use Code" true true false 4 Text 0 0 ,First,#,'+LANDUSE_PARCELS_WKSP+',LND_USE_CODE,-1,-1;LND_USE_DESC "Assessment Land Use Description" true true false 40 Text 0 0 ,First,#,'+LANDUSE_PARCELS_WKSP+',LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,'+LANDUSE_PARCELS_WKSP+',LND_DSTRCT,-1,-1;LAND_USE_CATEGORY "Planning Land Use Category" true true false 100 Text 0 0 ,First,#,'+LANDUSE_PARCELS_WKSP+',LAND_USE_CATEGORY,-1,-1;LBCS_ACTIVITY "LBCS Activity Code" true true false 8 Double 8 38 ,First,#,'+LANDUSE_PARCELS_WKSP+',LBCS_ACTIVITY,-1,-1;LBCS_FUNCTION "LBCS Function" true true false 8 Double 8 38 ,First,#,'+LANDUSE_PARCELS_WKSP+',LBCS_FUNCTION,-1,-1;LBCS_STRUCTURE "LBCS Structure Type" true true false 8 Double 8 38 ,First,#,'+LANDUSE_PARCELS_WKSP+',LBCS_STRUCTURE,-1,-1;LBCS_SITE_CHARACTER "LBCS site character" true true false 8 Double 8 38 ,First,#,'+LANDUSE_PARCELS_WKSP+',LBCS_SITE_CHARACTER,-1,-1;LBCS_OWNERSHIP "LBCS Ownership" true true false 8 Double 8 38 ,First,#,'+LANDUSE_PARCELS_WKSP+',LBCS_OWNERSHIP,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+LANDUSE_PARCELS_WKSP+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+LANDUSE_PARCELS_WKSP+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+LANDUSE_PARCELS_WKSP+',Shape.STLength(),-1,-1', "")
    LU_Parcels_Internal_result = arcpy.GetCount_management(LANDUSE_PARCELS_INTERNAL)
    print (('{} has {} records'.format(LANDUSE_PARCELS_INTERNAL, LU_Parcels_Internal_result[0])))
    write_log('{} has {} records'.format(LANDUSE_PARCELS_INTERNAL, LU_Parcels_Internal_result[0]), logfile)
except:
    print ("\n Unable to append Land Use Parcels - CRAW_INTERNAL from Land Use Parcels - AUTO_WORKSPACE")
    write_log("Unable to append Land Use Parcels - CRAW_INTERNAL from Land Use Parcels - AUTO_WORKSPACE", logfile)
    logging.exception('Got exception on append Land Use Parcels - CRAW_INTERNAL from Land Use Parcels - AUTO_WORKSPACE logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Land Use Parcels - CRAW_INTERNAL from Land Use Parcels - AUTO_WORKSPACE completed")
write_log("       Updating Land Use Parcels - CRAW_INTERNAL from Land Use Parcels - AUTO_WORKSPACE completed", logfile)

print ("\n Updating Land Use Parcels - PUBLIC_WEB from CRAW_INTERNAL")
write_log("\n Updating Land Use Parcels - PUBLIC_WEB from CRAW_INTERNAL: " + str(Day) + " " + str(Time), logfile)

try:
    # Delete rows from Land Use Parcels - PUBLIC_WEB
    arcpy.DeleteRows_management(LANDUSE_PARCELS_WEB)
except:
    print ("\n Unable to delete rows from Land Use Parcels - PUBLIC_WEB")
    write_log("Unable to delete rows from Land Use Parcels - PUBLIC_WEB", logfile)
    logging.exception('Got exception on delete rows from Land Use Parcels - PUBLIC_WEB logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

try:    
    # Append Land Use Parcels - PUBLIC_WEB from CRAW_INTERNAL
    arcpy.Append_management(LANDUSE_PARCELS_INTERNAL, LANDUSE_PARCELS_WEB, "NO_TEST", 'CAMA_PIN "MBLU (Map Block Lot Unit)" true true false 50 Text 0 0 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',CAMA_PIN,-1,-1;SEC_MUNI_NAME "Municipal Name" true true false 50 Text 0 0 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',SEC_MUNI_NAME,-1,-1;PID "PID Number" true true false 4 Long 0 10 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',PID,-1,-1;LND_USE_CODE "Assessment Land Use Code" true true false 4 Text 0 0 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',LND_USE_CODE,-1,-1;LND_USE_DESC "Assessment Land Use Description" true true false 40 Text 0 0 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',LND_USE_DESC,-1,-1;LND_DSTRCT "District Number" true true false 6 Text 0 0 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',LND_DSTRCT,-1,-1;LAND_USE_CATEGORY "Planning Land Use Category" true true false 100 Text 0 0 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',LAND_USE_CATEGORY,-1,-1;LBCS_ACTIVITY "LBCS Activity Code" true true false 8 Double 8 38 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',LBCS_ACTIVITY,-1,-1;LBCS_FUNCTION "LBCS Function" true true false 8 Double 8 38 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',LBCS_FUNCTION,-1,-1;LBCS_STRUCTURE "LBCS Structure Type" true true false 8 Double 8 38 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',LBCS_STRUCTURE,-1,-1;LBCS_SITE_CHARACTER "LBCS site character" true true false 8 Double 8 38 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',LBCS_SITE_CHARACTER,-1,-1;LBCS_OWNERSHIP "LBCS Ownership" true true false 8 Double 8 38 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',LBCS_OWNERSHIP,-1,-1;GlobalID "GlobalID" false false false 38 GlobalID 0 0 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',GlobalID,-1,-1;Shape.STArea() "Shape.STArea()" false false true 0 Double 0 0 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',Shape.STArea(),-1,-1;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#,'+LANDUSE_PARCELS_INTERNAL+',Shape.STLength(),-1,-1', "")
    LU_Parcels_Web_result = arcpy.GetCount_management(LANDUSE_PARCELS_WEB)
    print (('{} has {} records'.format(LANDUSE_PARCELS_WEB, LU_Parcels_Web_result[0])))
    write_log('{} has {} records'.format(LANDUSE_PARCELS_WEB, LU_Parcels_Web_result[0]), logfile)
except:
    print ("\n Unable to append Land Use Parcels - PUBLIC_WEB from CRAW_INTERNAL")
    write_log("Unable to append Land Use Parcels - PUBLIC_WEB from CRAW_INTERNAL", logfile)
    logging.exception('Got exception on append Land Use Parcels - PUBLIC_WEB from CRAW_INTERNAL logged at:' + str(Day) + " " + str(Time))
    raise
    sys.exit ()

print ("       Updating Land Use Parcels - PUBLIC_WEB from CRAW_INTERNAL completed")
write_log("       Updating Land Use Parcels - PUBLIC_WEB from CRAW_INTERNAL completed", logfile)

end_time = time.strftime("%I:%M:%S %p", time.localtime())
elapsed_time = time.time() - start_time

print ("==============================================================")
print (("\n ALL LAND USE UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time)))
write_log("\n ALL LAND USE UPDATES ARE COMPLETED: " + str(Day) + " " + str(end_time), logfile)

print (("Elapsed time: " + time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)))
write_log("Elapsed time: " + str (time.strftime(" %H:%M:%S", time.gmtime(elapsed_time))+" // Program completed: " + str(Day) + " " + str(end_time)), logfile)
print ("==============================================================")


write_log("\n           +#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#+#", logfile)
del arcpy
sys.exit()
