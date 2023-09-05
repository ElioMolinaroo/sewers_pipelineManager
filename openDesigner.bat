@echo off

REM Changes the current working directory to the directory the bat file is in
cd /d %~dp0

REM opens QT Designer
start venv\Lib\site-packages\qt6_applications\Qt\bin\designer.exe

exit

