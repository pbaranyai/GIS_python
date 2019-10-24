echo. > R:\GIS\GIS_LOGS\BatchLogs\SDE_Compress_Master_bat.log
::  Comment Line
:: 
date=date /t
time=time /t
set STARTTIME=%TIME%
::
Set wrkspce=R:\GIS\ArcAutomations\GIS_Dept
::Set wrkspce=R:\GIS\ArcAutomations\GIS_Dept
::
Set batLogwrkspce=R:\GIS\GIS_LOGS\BatchLogs
::
Set batLog=%batLogwrkspce%\SDE_Compress_Master_bat.log
::
::::::::::::::::::::::: Run SDE Compress Tools SDE_Compress_Tools.py) :::::::::::::::::::::::
::
echo _SDE_Compress_Master_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\SDE_Compress_Master_bat.log
::
echo Start Running SDE_Compress_Tools.py >> %prgLog% 
call %wrkspce%\Python\SDE_Compress_Tools.py >> %prgLog%
::
echo End Running SDE_Compress_Tools.py %date%, %time% >> %prgLog%
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