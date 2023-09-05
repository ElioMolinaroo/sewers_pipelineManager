@echo off

title Sewers

REM Changes the current working directory to the directory the bat file is in
cd /d %~dp0

REM Run __init__.py file through the python exec
python __init__.py

pause