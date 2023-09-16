@echo off

REM Changes the current working directory to the directory the bat file is in
cd /d %~dp0

REM opens QT Designer
start %LOCALAPPDATA%\Programs\Python\Python3.11.4\Lib\site-packages\qt6_applications\Qt\bin\designer.exe

exit

