echo. > \\FILELOCATION\GIS\GIS_LOGS\BatchLogs\Miscellaneous_Master_Updater_bat.log
::  Comment Line
:: 
date=date /t
time=time /t
set STARTTIME=%TIME%
::
Set wrkspce=\\FILELOCATION\GIS\ArcAutomations\GIS_Dept\Python
::Set wrkspce=\\FILELOCATION\GIS\ArcAutomations\GIS_Dept\Python
::
Set PLANwrkspce=\\FILELOCATION\GIS\ArcAutomations\Planning\Python
::Set PLANwrkspce=\\FILELOCATION\GIS\ArcAutomations\Planning\Python
::
Set batLogwrkspce=\\FILELOCATION\GIS\GIS_LOGS\BatchLogs
::
Set batLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
::::::::::::::::::::::: Run Boundaries Data Spreader (Boundaries_Data_Spreader.py) :::::::::::::::::::::::
::
echo _Miscellaneous_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Running Boundaries_Data_Spreader.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Boundaries_Data_Spreader.py >> %prgLog%
::
echo End Running Boundaries_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Education Data Spreader (Education_Data_Spreader.py) :::::::::::::::::::::::
::
echo _Miscellaneous_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Running Education_Data_Spreader.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Education_Data_Spreader.py >> %prgLog%
::
echo End Running Education_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Elections Data Spreader (Elections_Data_Spreader.py) :::::::::::::::::::::::
::
echo _Miscellaneous_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Running Elections_Data_Spreader.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Elections_Data_Spreader.py >> %prgLog%
::
echo End Running Elections_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Hydrography Data Spreader (Hydrography_Data_Spreader.py) :::::::::::::::::::::::
::
echo _Miscellaneous_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Running Hydrography_Data_Spreader.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Hydrography_Data_Spreader.py >> %prgLog%
::
echo End Running Hydrography_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Planning Data Spreader (Planning_Data_Spreader.py) :::::::::::::::::::::::
::
echo _Miscellaneous_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Running Planning_Data_Spreader.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %PLANwrkspce%\Planning_Data_Spreader.py >> %prgLog%
::
echo End Running Planning_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Recreational Data Spreader (Recreational_Data_Spreader.py) :::::::::::::::::::::::
::
echo _Miscellaneous_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Running Recreational_Data_Spreader.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Recreational_Data_Spreader.py >> %prgLog%
::
echo End Running Recreational_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Religon Data Spreader (Religon_Data_Spreader.py ) :::::::::::::::::::::::
::
echo _Start Religon_Data_Spreader.py, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Religon_Data_Spreader.py , %date%, %time% >> %prgLog%
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Religon_Data_Spreader.py >> %prgLog%
::
echo End Running Religon_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Transportation Data Spreader (Transportation_Data_Spreader.py ) :::::::::::::::::::::::
::
echo _Start Transportation Data Spreader, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Transportation_Data_Spreader.py , %date%, %time% >> %prgLog%
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Transportation_Data_Spreader.py >> %prgLog%
::
echo End Running Transportation_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Utilities Data Spreader (Utilities_Data_Spreader.py ) :::::::::::::::::::::::
::
echo Start Utilities Data Spreader , %date%, %time% >> %prgLog%
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Utilities_Data_Spreader.py , %date%, %time% >> %prgLog%
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Utilities_Data_Spreader.py >> %prgLog%
::
echo End Utilities Data Spreader %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Judicial Data Spreader (Judicial_Data_Spreader.py ) :::::::::::::::::::::::
::
echo _Start Judicial Data Spreader, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Judicial_Data_Spreader.py , %date%, %time% >> %prgLog%
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Judicial_Data_Spreader.py >> %prgLog%
::
echo End Running Judicial_Data_Spreader.py %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Community Services Data Spreader (Community_Services_Data_Spreader.py ) :::::::::::::::::::::::
::
echo _Start Community Services Data Spreader, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\Miscellaneous_Master_Updater_bat.log
::
echo Start Community_Services_Data_Spreader.py , %date%, %time% >> %prgLog%
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %wrkspce%\Community_Services_Data_Spreader.py >> %prgLog%
::
echo End Running Community_Services_Data_Spreader.py %date%, %time% >> %prgLog%
::
echo _Finish Miscellaneous_Master_Updater, %date%, %time% >> %batLog%
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
