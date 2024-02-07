@echo off

title Flush Databases

REM Changes the current working directory to the directory the bat file is in
cd /d %~dp0

REM Run files through the python exec
"C:\Users\Elio\anaconda3\envs\sewers\python.exe" utils/flushDatabases.py

pause
