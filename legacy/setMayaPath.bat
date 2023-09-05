@echo off

title Get Maya Path

REM Changes the current working directory to the directory the bat file is in
cd /d %~dp0

REM Run file through the python exec
python utils/getMayaPath.py

exit