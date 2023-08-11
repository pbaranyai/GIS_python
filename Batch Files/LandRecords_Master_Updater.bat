echo. > R:\GIS\GIS_LOGS\BatchLogs\LandRecords_Master_Updater_bat.log
::  Comment Line
:: 
date=date /t
time=time /t
set STARTTIME=%TIME%
::
Set wrkspce=R:\GIS\ArcAutomations\GIS_Dept\Python
::Set wrkspce=R:\GIS\ArcAutomations\GIS_Dept\Python
::
Set ASTwrkspce=R:\GIS\ArcAutomations\Assessment\Python
::Set ASTwrkspce=R:\GIS\ArcAutomations\Assessment\Python
::
Set PLANwrkspce=R:\GIS\ArcAutomations\Planning\Python
::Set PLANwrkspce=R:\GIS\ArcAutomations\Planning\Python
::
Set batLogwrkspce=R:\GIS\GIS_LOGS\BatchLogs
::
Set batLog=%batLogwrkspce%\LandRecords_Master_Updater_bat.log
::
::::::::::::::::::::::: Run Parcel Builder (Parcel_Builder.py) :::::::::::::::::::::::
::
echo _LandRecords_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\LandRecords_Master_Updater_bat.log
::
echo Start Running Parcel_Builder.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %ASTwrkspce%\Parcel_Builder.py >> %prgLog%
::
echo End Running Parcel_Builder.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Land Records Data Spreader (LandRecords_Data_Spreader.py) :::::::::::::::::::::::
::
echo _LandRecords_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\LandRecords_Master_Updater_bat.log
::
echo Start Running LandRecords_Data_Spreader.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\LandRecords_Data_Spreader.py >> %prgLog%
::
echo End Running LandRecords_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Locator Rebuilder (Locator_Rebuilder.py) :::::::::::::::::::::::
::
echo _LandRecords_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\LandRecords_Master_Updater_bat.log
::
echo Start Running Locator_Rebuilder.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Locator_Rebuilder.py >> %prgLog%
::
echo End Running Locator_Rebuilder.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Land Use Data Spreader (LandUse_Data_Spreader.py) :::::::::::::::::::::::
::
echo _LandRecords_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\LandRecords_Master_Updater_bat.log
::
echo Start Running LandUse_Data_Spreader.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %PLANwrkspce%\LandUse_Data_Spreader.py >> %prgLog%
::
echo End Running LandUse_Data_Spreader.py %date%, %time% >> %prgLog%
::
echo _Finish Land Records Master Updater, %date%, %time% >> %batLog%
::
::::::::::::::::::::::: Run Missing VISION records report (Active_VISION_Missing_GIS.py) :::::::::::::::::::::::
::
echo _LandRecords_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\LandRecords_Master_Updater_bat.log
::
echo Start Running Active_VISION_Missing_GIS.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %ASTwrkspce%\Active_VISION_Missing_GIS.py >> %prgLog%
::
echo End Running Active_VISION_Missing_GIS.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run GIS not in VISION records report (Active_GIS_Missing_VISION.py) :::::::::::::::::::::::
::
echo _LandRecords_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\LandRecords_Master_Updater_bat.log
::
echo Start Running Active_GIS_Missing_VISION.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %ASTwrkspce%\Active_GIS_Missing_VISION.py >> %prgLog%
::
echo End Running Active_GIS_Missing_VISION.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Mismatched Air Parcel records report (AirParcel_VISION_Mismatch.py) :::::::::::::::::::::::
::
echo _LandRecords_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\LandRecords_Master_Updater_bat.log
::
echo Start Running AirParcel_VISION_Mismatch.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %ASTwrkspce%\AirParcel_VISION_Mismatch.py >> %prgLog%
::
echo End Running AirParcel_VISION_Mismatch.py %date%, %time% >> %prgLog%
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
