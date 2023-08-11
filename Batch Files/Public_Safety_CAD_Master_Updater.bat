echo. > R:\GIS\GIS_LOGS\BatchLogs\Public_Safety_CAD_Master_Updater_bat.log
::  Comment Line
:: 
date=date /t
time=time /t
set STARTTIME=%TIME%
::
Set wrkspce=R:\GIS\ArcAutomations
::Set wrkspce=R:\GIS\ArcAutomations
::
Set batLogwrkspce=R:\GIS\GIS_LOGS\BatchLogs
::
Set batLog=%batLogwrkspce%\Public_Safety_CAD_Master_Updater_bat.log
::
::::::::::::::::::::::: Run Public Safety Data Spreader (PublicSafety_Data_Spreader.py) :::::::::::::::::::::::
::
echo _Public_Safety_CAD_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Public_Safety_CAD_Master_Updater_bat.log
::
echo Start Running PublicSafety_Data_Spreader.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\GIS_Dept\Python\PublicSafety_Data_Spreader.py >> %prgLog%
::
echo End Running PublicSafety_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run NorthernTierCAD_DataExport_Process - Step 1 (NorthernTierCAD_DataExport_Process_Step1.py) :::::::::::::::::::::::
::
echo _Public_Safety_CAD_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Public_Safety_CAD_Master_Updater_bat.log
::
echo Start Running NorthernTierCAD_DataExport_Process_Step1.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Public_Safety\Python\NorthernTierCAD_DataExport_Process_Step1.py >> %prgLog%
::
echo End Running NorthernTierCAD_DataExport_Process_Step1.py %date%, %time% >> %prgLog%
::
echo _Finish Public Safety CAD Master Updater, %date%, %time% >> %batLog%
::
set ENDTIME=%TIME%
rem Change formatting for the start and end times
    for /F "tokens=1-4 delims=:.," %%a in ("%STARTTIME%") do (
       set /A "start=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
    )

    for /F "tokens=1-4 delims=:.," %%a in ("%ENDTIME%") do (
       set /A "end=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
    )

    rem Calculate the elapsed time by subtracting values
    set /A elapsed=end-start

    rem Format the results for output
    set /A hh=elapsed/(60*60*100), rest=elapsed%%(60*60*100), mm=rest/(60*100), rest%%=60*100, ss=rest/100, cc=rest%%100
    if %hh% lss 10 set hh=0%hh%
    if %mm% lss 10 set mm=0%mm%
    if %ss% lss 10 set ss=0%ss%
    if %cc% lss 10 set cc=0%cc%

    set DURATION=%hh%:%mm%:%ss%.%cc%

    echo Start    : %STARTTIME% >> %prgLog%
    echo Finish   : %ENDTIME% >> %prgLog%
    echo          --------------- >> %prgLog%
    echo Duration : %DURATION% >> %prgLog%
::
exit
