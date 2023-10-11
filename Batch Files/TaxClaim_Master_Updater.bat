echo. > \\FILELOCATION\GIS\GIS_LOGS\BatchLogs\TaxClaim_Master_Updater_bat.log
::  Comment Line
:: 
date=date /t
time=time /t
set STARTTIME=%TIME%
::
Set SVRwrkspce=\\ccmeteor\gss
::Set SVRwrkspce=\\ccmeteor\gss
::
Set PYwrkspce=\\FILELOCATION\GIS\ArcAutomations\GIS_Dept\Python
::Set PYwrkspce=\\FILELOCATION\GIS\ArcAutomations\GIS_Dept\Python
::
Set batLogwrkspce=\\FILELOCATION\GIS\GIS_LOGS\BatchLogs
::
Set batLog=%batLogwrkspce%\TaxClaim_Master_Updater_bat.log
::
::::::::::::::::::::::: Run GSS Tax Claim Updater (CrawfordGISTaxSale.exe) :::::::::::::::::::::::
::
echo _TaxClaim_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\TaxClaim_Master_Updater_bat.log
::
echo Start Running CrawfordGISTaxSale.exe >> %prgLog% 
call %SVRwrkspce%\CrawfordGISTaxSale.exe >> %prgLog%
::
echo End Running CrawfordGISTaxSale.exe %date%, %time% >> %prgLog%
::
::::::::::::::::::::::: Run Tax Claim Data Spreader (TaxClaim_Data_Spreader.py) :::::::::::::::::::::::
::
echo _TaxClaim_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\TaxClaim_Master_Updater_bat.log
::
echo Start Running TaxClaim_Data_Spreader.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %PYwrkspce%\TaxClaim_Data_Spreader.py >> %prgLog%
::
echo End Running TaxClaim_Data_Spreader.py %date%, %time% >> %prgLog%
::
echo _Finish Tax Claim Master Updater, %date%, %time% >> %batLog%
::
::::::::::::::::::::::: Run Active Tax Claim Missing GIS Report tool (Active_TaxClaim_Missing_GIS.py) :::::::::::::::::::::::
::
echo _TaxClaim_Master_Updater_bat, %date%, %time% >> %batLog% 
::
Set prgLog=%batLogwrkspce%\TaxClaim_Master_Updater_bat.log
::
echo Start Running Active_TaxClaim_Missing_GIS.py >> %prgLog% 
call "%PROGRAMFILES%\ArcGIS\Pro\bin\Python\Scripts\propy" %PYwrkspce%\Active_TaxClaim_Missing_GIS.py >> %prgLog%
::
echo End Running Active_TaxClaim_Missing_GIS.py %date%, %time% >> %prgLog%
::
echo _Finish Active Tax Claim Missing GIS Report tool, %date%, %time% >> %batLog%
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
