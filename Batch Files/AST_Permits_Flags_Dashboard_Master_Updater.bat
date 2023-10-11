echo. > \\FILELOCATION\GIS\GIS_LOGS\BatchLogs\BuildingPermit_Tracks_CAMATables_Updater_bat.log
::  Comment Line
:: 
date=date /t
time=time /t
set STARTTIME=%TIME%
::
Set ASTwrkspce=\\FILELOCATION\GIS\ArcAutomations\Assessment\Python
::Set ASTwrkspce=\\FILELOCATION\GIS\ArcAutomations\Assessment\Python
::
Set batLogwrkspce=\\FILELOCATION\GIS\GIS_LOGS\BatchLogs
::
Set batLog=%batLogwrkspce%\BuildingPermit_Tracks_CAMATables_Updater_bat.log
::
::::::::::::::::::::::: Run BuildingPermits_CAMA Tables Updater (BuildingPermitOnly_Updater.py) :::::::::::::::::::::::
::
echo _BuildingPermitOnly_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\BuildingPermit_Tracks_CAMATables_Updater_bat.log
::
echo Start Running BuildingPermitOnly_Updater.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %ASTwrkspce%\BuildingPermitOnly_Updater.py >> %prgLog%
::
echo End BuildingPermitOnly_Updater.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Assessment Tracks Updater (Assessment_Historic_Tracks_Updater.py) :::::::::::::::::::::::
::
echo _BuildingPermitOnly_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\BuildingPermit_Tracks_CAMATables_Updater_bat.log
::
echo Start Running Assessment_Historic_Tracks_Updater.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %ASTwrkspce%\Assessment_Historic_Tracks_Updater.py >> %prgLog%
::
echo End Assessment_Historic_Tracks_Updater.py %date%, %time% >> %prgLog%
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
