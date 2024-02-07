@echo off

REM Changes the current working directory to the directory the bat file is in
cd /d %~dp0

REM opens QT Designer
start %USERPROFILE%\anaconda3\envs\sewers\Lib\site-packages\QtDesigner\designer.exe

exit

